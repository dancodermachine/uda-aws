import middy from '@middy/core'
import cors from '@middy/http-cors'
import { getUserId } from '../utils.mjs'
import { getTodosForUser } from '../../businessLogic/todos.mjs'
import { createLogger } from '../../utils/logger.mjs'

const logger = createLogger('getTodos')

export const handler = middy()
  .use(cors({ credentials: true }))
  .handler(async (event) => {
    const userId = getUserId(event)

    logger.info('Getting todos for user', { userId })

    const items = await getTodosForUser(userId)

    logger.info('Found todos', { userId, count: items.length })

    return {
      statusCode: 200,
      body: JSON.stringify({
        items
      })
    }
  })
