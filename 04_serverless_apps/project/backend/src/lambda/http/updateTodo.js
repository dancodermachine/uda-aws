import middy from '@middy/core'
import cors from '@middy/http-cors'
import httpErrorHandler from '@middy/http-error-handler'
import { getUserId } from '../utils.mjs'
import { updateTodo } from '../../businessLogic/todos.mjs'
import { createLogger } from '../../utils/logger.mjs'

const logger = createLogger('updateTodo')

export const handler = middy()
  // Turns any thrown http-errors error (404, ...) into a proper response
  .use(httpErrorHandler())
  .use(cors({ credentials: true }))
  .handler(async (event) => {
    const todoId = event.pathParameters.todoId
    const userId = getUserId(event)

    // Fields the client is allowed to change: name, dueDate, done
    const updatedTodo = JSON.parse(event.body)

    logger.info('Updating todo', { todoId, userId, updatedTodo })

    await updateTodo(userId, todoId, updatedTodo)

    logger.info('Todo updated', { todoId, userId })

    return {
      statusCode: 200,
      body: ''
    }
  })
