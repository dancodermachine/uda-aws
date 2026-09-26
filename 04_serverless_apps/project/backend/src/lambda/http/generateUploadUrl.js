import middy from '@middy/core'
import cors from '@middy/http-cors'
import httpErrorHandler from '@middy/http-error-handler'
import { getUserId } from '../utils.mjs'
import { generateUploadUrl } from '../../businessLogic/todos.mjs'
import { createLogger } from '../../utils/logger.mjs'

const logger = createLogger('generateUploadUrl')

export const handler = middy()
  // Turns any thrown http-errors error (404, ...) into a proper response
  .use(httpErrorHandler())
  .use(cors({ credentials: true }))
  .handler(async (event) => {
    const todoId = event.pathParameters.todoId
    const userId = getUserId(event)

    logger.info('Generating upload url', { todoId, userId })

    const uploadUrl = await generateUploadUrl(userId, todoId)

    logger.info('Generated upload url', { todoId, userId })

    return {
      statusCode: 200,
      body: JSON.stringify({
        uploadUrl
      })
    }
  })
