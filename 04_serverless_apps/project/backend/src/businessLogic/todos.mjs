import { v4 as uuidv4 } from 'uuid'
import createHttpError from 'http-errors'
import { TodoAccess } from '../dataLayer/todosAccess.mjs'
import { AttachmentUtils } from '../fileStorage/attachmentUtils.mjs'
import { createLogger } from '../utils/logger.mjs'

const logger = createLogger('businessLogic-todos')

const todoAccess = new TodoAccess()
const attachmentUtils = new AttachmentUtils()

export async function getTodosForUser(userId) {
  return todoAccess.getTodosForUser(userId)
}

export async function createTodo(userId, createTodoRequest) {
  const todoId = uuidv4()

  const newItem = {
    todoId,
    userId,
    createdAt: new Date().toISOString(),
    done: false,
    name: createTodoRequest.name,
    dueDate: createTodoRequest.dueDate
  }

  logger.info('Creating a new todo', { newItem })

  return todoAccess.createTodo(newItem)
}

export async function updateTodo(userId, todoId, updateTodoRequest) {
  await assertTodoExists(userId, todoId)

  await todoAccess.updateTodo(userId, todoId, updateTodoRequest)
}

export async function deleteTodo(userId, todoId) {
  await assertTodoExists(userId, todoId)

  await todoAccess.deleteTodo(userId, todoId)
}

export async function generateUploadUrl(userId, todoId) {
  await assertTodoExists(userId, todoId)

  const attachmentUrl = attachmentUtils.getAttachmentUrl(todoId)
  await todoAccess.updateAttachmentUrl(userId, todoId, attachmentUrl)

  return attachmentUtils.getUploadUrl(todoId)
}

// The table's primary key is (userId, todoId), so looking an item up by
// both together only finds it if it belongs to this user
async function assertTodoExists(userId, todoId) {
  const existingTodo = await todoAccess.getTodo(userId, todoId)

  if (!existingTodo) {
    logger.error('Todo not found', { userId, todoId })
    throw createHttpError(404, 'Todo does not exist')
  }
}
