# Serverless TODO App

A TODO application built on AWS serverless services. Users log in with Auth0,
then create, complete, edit and delete their own TODO items and attach an image
to any of them. Each user only ever sees their own items.

- **Backend:** AWS Lambda functions behind API Gateway, written in Node.js and
  deployed with the Serverless Framework. Data is stored in DynamoDB, images in
  S3, and requests are traced with AWS X-Ray.
- **Frontend:** a React app that authenticates with Auth0 and calls the
  backend REST API with the user's token.

```
Browser (React + Auth0)
   │  Authorization: Bearer <Auth0 ID token>
   ▼
API Gateway ── Lambda authorizer (verifies the token against Auth0's JWKS)
   │
   ▼
Lambda handlers ──► business logic ──► DynamoDB (TODO items)
                                   └─► S3 (presigned upload URLs for images)
```

## Backend

### Structure

```
backend
├── serverless.yml                  # All AWS resources, functions and permissions
├── package.json
└── src
    ├── lambda                      # AWS Lambda layer: HTTP in, HTTP out
    │   ├── auth
    │   │   └── auth0Authorizer.mjs # Custom API Gateway authorizer
    │   ├── http
    │   │   ├── getTodos.js         # GET    /todos
    │   │   ├── createTodo.js       # POST   /todos
    │   │   ├── updateTodo.js       # PATCH  /todos/{todoId}
    │   │   ├── deleteTodo.js       # DELETE /todos/{todoId}
    │   │   └── generateUploadUrl.js  # POST /todos/{todoId}/attachment
    │   └── utils.mjs               # Reads the user id from the request
    ├── auth
    │   └── utils.mjs               # Decodes a JWT and returns the user id (sub)
    ├── businessLogic
    │   └── todos.mjs               # Application rules, independent of AWS
    ├── dataLayer
    │   └── todosAccess.mjs         # All DynamoDB access
    ├── fileStorage
    │   └── attachmentUtils.mjs     # All S3 access
    ├── models
    │   ├── createTodoRequest.json  # JSON schema for POST /todos
    │   └── updateTodoRequest.json  # JSON schema for PATCH /todos/{todoId}
    └── utils
        └── logger.mjs              # Winston JSON logger
```

### `serverless.yml`

Defines everything the app needs, so nothing is created by hand in the AWS
console:

- **Functions and HTTP routes** on API Gateway, each protected by the `Auth`
  authorizer and with CORS enabled.
- **Request validation:** `POST /todos` and `PATCH /todos/{todoId}` attach the
  JSON schemas in `src/models`, so API Gateway rejects invalid bodies (for
  example a missing or empty `name`) with a 400 before any Lambda runs.
- **Resources:** the `Todos-<stage>` DynamoDB table and the S3 attachments
  bucket with its CORS rules and a public-read bucket policy.
- **Per-function IAM permissions** using the
  `serverless-iam-roles-per-function` plugin. Each function gets its own role
  with only the actions it needs, for example `GetTodos` can only `Query` the
  `CreatedAtIndex` index and `CreateTodo` can only `PutItem`.
- **Tracing:** X-Ray is enabled for both Lambda and API Gateway.

### Lambda layer: `src/lambda`

The only code that knows about the Lambda event format.

- **`auth/auth0Authorizer.mjs`**: a custom API Gateway authorizer. It takes
  the bearer token from the `Authorization` header, downloads Auth0's public
  keys (JWKS), finds the key matching the token's `kid`, and verifies the
  RS256 signature with `jsonwebtoken`. A valid token returns an IAM policy that
  allows the request; anything else returns a deny, so API Gateway answers
  401/403 without calling the handler.
- **`http/*.js`**: one handler per route. Each reads the path parameters and
  body, gets the user id from the token, calls the business layer and builds
  the HTTP response. They use **Middy** middleware:
  - `@middy/http-cors` adds CORS headers to every response.
  - `@middy/http-error-handler` turns errors thrown with `http-errors` (such
    as a 404 for a TODO that doesn't exist) into proper HTTP responses.
- **`utils.mjs`**: extracts the token from the request headers and passes it to
  `auth/utils.mjs` to get the user id.

### Business logic: `src/businessLogic/todos.mjs`

The application rules, with no AWS SDK code:

- Creates new items with a generated `uuid`, a `createdAt` timestamp and
  `done: false`.
- Checks that a TODO exists for the current user before updating, deleting or
  attaching a file to it, and throws a 404 otherwise. Because items are looked
  up by `userId` and `todoId` together, one user can never read or change
  another user's items.
- Generates an upload URL by combining the file storage layer (the presigned
  URL) and the data layer (saving `attachmentUrl` on the item).

### Data layer: `src/dataLayer/todosAccess.mjs`

The `TodoAccess` class is the only code that talks to **DynamoDB**, through the
AWS SDK v3 `DynamoDBDocumentClient` wrapped with **X-Ray** so every database
call appears in traces.

- The table uses a composite key: `userId` (partition key) and `todoId` (sort
  key), which models the one-to-many relationship between users and TODOs.
- A local secondary index, `CreatedAtIndex` (`userId` + `createdAt`), lets the
  list of a user's TODOs be read with a **`Query`** sorted by creation date,
  never with a `Scan`.
- Updates only touch `name`, `dueDate` and `done`, or `attachmentUrl`.

### File storage: `src/fileStorage/attachmentUtils.mjs`

The `AttachmentUtils` class is the only code that talks to **S3**, with the
client also wrapped with **X-Ray**.

- `getUploadUrl` creates a **presigned `PUT` URL** valid for 5 minutes, so the
  browser uploads the image directly to S3 without it passing through Lambda.
- `getAttachmentUrl` returns the public URL the image is served from. Each
  TODO has at most one attachment, stored under a key equal to its `todoId`.

### Auth utilities and logging

- **`src/auth/utils.mjs`**: decodes a JWT and returns its `sub` claim, which
  is used as the `userId` everywhere.
- **`src/utils/logger.mjs`**: creates **Winston** loggers that write JSON log
  lines to **CloudWatch Logs**. Every layer logs what it does, tagged with its
  own name.

All asynchronous work uses `async`/`await` with Promises; there are no
callbacks.

## Frontend

### Structure

```
client
├── .env                        # API endpoint and Auth0 settings
├── package.json
├── public
└── src
    ├── index.js                # Wraps the app in Auth0Provider
    ├── App.jsx                 # Menu, log in / log out, routes
    ├── api
    │   └── todos-api.js        # Axios calls to the backend
    ├── auth
    │   └── useIdToken.js       # Hook that returns the Auth0 ID token
    └── components
        ├── Todos.jsx           # TODO list: load, complete, delete, images
        ├── NewTodoInput.jsx    # Input for creating a TODO
        ├── EditTodo.jsx        # Pencil page: upload an image for a TODO
        ├── LogIn.jsx           # Shown when the user isn't logged in
        ├── Callback.jsx        # Loading spinner
        └── NotFound.jsx        # 404 page
```

### How it works

- **`.env`** configures the app:

  | Variable | Purpose |
  |---|---|
  | `REACT_APP_API_ENDPOINT` | Base URL of the deployed API Gateway stage |
  | `REACT_APP_AUTH0_DOMAIN` | Auth0 tenant domain |
  | `REACT_APP_AUTH0_CLIENT_ID` | Auth0 application client ID |

- **`index.js`** sets up **Auth0** with `@auth0/auth0-react`. It uses refresh
  tokens stored in local storage, so the user stays logged in across reloads.
- **`App.jsx`** shows the menu and the log in / log out button. Until the user
  is authenticated it only renders the `LogIn` page, so the app can't be used
  anonymously. Pages are routed with `react-router-dom`.
- **`auth/useIdToken.js`** refreshes the session when needed and returns the
  user's Auth0 **ID token**. The app sends this token, a signed RS256 JWT, as
  the bearer token that the backend authorizer verifies.
- **`api/todos-api.js`** makes the HTTP calls with **Axios**: get, create,
  update and delete TODOs, request an upload URL, and upload the file to S3.
- **`Todos.jsx`** loads the user's TODOs, lets them tick an item as done,
  delete it, or click the pencil to edit it, and shows attached images.
- **`EditTodo.jsx`** asks the backend for a presigned URL, then uploads the
  selected file straight to S3. The image appears in the list on the home page.

The UI is built with **Semantic UI React**.

## Running the project

### Prerequisites

- Node.js 20 or later and npm.
- An AWS account, with credentials configured for the AWS CLI
  (`aws configure`).
- The Serverless Framework v4: `npm install -g serverless`, then
  `serverless login` (v4 requires a free Serverless account).
- An Auth0 **Single Page Application**. In its settings, add the URL the
  frontend runs on (for example `http://localhost:3000`) to **Allowed Callback
  URLs**, **Allowed Logout URLs** and **Allowed Web Origins**.

### Deploy the backend

```bash
cd backend
npm install
serverless deploy
```

The Auth0 tenant used to verify tokens is set by `jwksUrl` in
`src/lambda/auth/auth0Authorizer.mjs`. The attachments bucket name in
`serverless.yml` must be unique across all of AWS, so change its suffix if the
deploy reports that the bucket already exists.

When the deploy finishes it prints the API endpoints, for example:

```
POST - https://<apiId>.execute-api.us-east-1.amazonaws.com/dev/todos
```

### Run the frontend

1. Set the values in `client/.env`:

   ```
   REACT_APP_API_ENDPOINT=https://<apiId>.execute-api.us-east-1.amazonaws.com/dev
   REACT_APP_AUTH0_DOMAIN=<your-tenant>.us.auth0.com
   REACT_APP_AUTH0_CLIENT_ID=<your-auth0-client-id>
   ```

2. Install and start the development server:

   ```bash
   cd client
   npm install
   npm start
   ```

3. Open [http://localhost:3000](http://localhost:3000) and log in.

Restart `npm start` after changing `.env`, because the values are only read
when the server starts.