import middy from '@middy/core'
import cors from '@middy/http-cors'
import { getUserId } from '../utils.mjs'
import { createTodo } from '../../businessLogic/todos.mjs'
import { createLogger } from '../../utils/logger.mjs'

const logger = createLogger('createTodo')

export const handler = middy()
  .use(cors({ credentials: true }))
  .handler(async (event) => {
    const userId = getUserId(event)
    const newTodo = JSON.parse(event.body)

    const newItem = await createTodo(userId, newTodo)

    logger.info('Todo created', { todoId: newItem.todoId, userId })

    return {
      statusCode: 201,
      body: JSON.stringify({
        item: newItem
      })
    }
  })
