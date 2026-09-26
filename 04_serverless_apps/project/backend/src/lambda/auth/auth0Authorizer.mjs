import Axios from 'axios'
import jsonwebtoken from 'jsonwebtoken'
import { createLogger } from '../../utils/logger.mjs'

const logger = createLogger('auth')

const jwksUrl = 'https://dev-c7yi45bfp3zkitnj.us.auth0.com/.well-known/jwks.json'

export async function handler(event) {
  try {
    const jwtToken = await verifyToken(event.authorizationToken)
    logger.info('User was authorized', { jwtToken })

    return {
      principalId: jwtToken.sub,
      policyDocument: {
        Version: '2012-10-17',
        Statement: [
          {
            Action: 'execute-api:Invoke',
            Effect: 'Allow',
            Resource: '*'
          }
        ]
      }
    }
  } catch (e) {
    logger.error('User not authorized', { error: e.message })

    return {
      principalId: 'user',
      policyDocument: {
        Version: '2012-10-17',
        Statement: [
          {
            Action: 'execute-api:Invoke',
            Effect: 'Deny',
            Resource: '*'
          }
        ]
      }
    }
  }
}

async function verifyToken(authHeader) {
  const token = getToken(authHeader)
  const jwt = jsonwebtoken.decode(token, { complete: true })

  // Auth0 signs tokens with a key from its JWKS endpoint, identified by "kid".
  // Fetch the JWKS and find the certificate matching this token's key id.
  const response = await Axios.get(jwksUrl)
  const signingKey = response.data.keys.find(key => key.kid === jwt.header.kid)

  if (!signingKey) {
    throw new Error(`No signing key found for kid ${jwt.header.kid}`)
  }

  const cert = certToPEM(signingKey.x5c[0])

  return jsonwebtoken.verify(token, cert, { algorithms: ['RS256'] })
}

// The JWKS endpoint returns the certificate as a bare base64 string;
// jsonwebtoken.verify needs it wrapped as a PEM-encoded certificate
function certToPEM(cert) {
  const formatted = cert.match(/.{1,64}/g).join('\n')
  return `-----BEGIN CERTIFICATE-----\n${formatted}\n-----END CERTIFICATE-----\n`
}

function getToken(authHeader) {
  if (!authHeader) throw new Error('No authentication header')

  if (!authHeader.toLowerCase().startsWith('bearer '))
    throw new Error('Invalid authentication header')

  const split = authHeader.split(' ')
  const token = split[1]

  return token
}
