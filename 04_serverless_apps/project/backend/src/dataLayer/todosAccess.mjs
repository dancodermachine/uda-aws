import { DynamoDBClient } from '@aws-sdk/client-dynamodb'
import {
  DynamoDBDocumentClient,
  QueryCommand,
  PutCommand,
  GetCommand,
  UpdateCommand,
  DeleteCommand
} from '@aws-sdk/lib-dynamodb'
import AWSXRay from 'aws-xray-sdk-core'
import { createLogger } from '../utils/logger.mjs'

const logger = createLogger('TodosAccess')

export class TodoAccess {
  constructor(
    docClient = DynamoDBDocumentClient.from(AWSXRay.captureAWSv3Client(new DynamoDBClient())),
    todosTable = process.env.TODOS_TABLE,
    createdAtIndex = process.env.TODOS_CREATED_AT_INDEX
  ) {
    this.docClient = docClient
    this.todosTable = todosTable
    this.createdAtIndex = createdAtIndex
  }

  async getTodosForUser(userId) {
    logger.info('Querying todos for user', { userId })

    const result = await this.docClient.send(
      new QueryCommand({
        TableName: this.todosTable,
        IndexName: this.createdAtIndex,
        KeyConditionExpression: 'userId = :userId',
        ExpressionAttributeValues: {
          ':userId': userId
        },
        // false = descending order, so the newest todos come first
        ScanIndexForward: false
      })
    )

    return result.Items
  }

  async getTodo(userId, todoId) {
    const result = await this.docClient.send(
      new GetCommand({
        TableName: this.todosTable,
        Key: { userId, todoId }
      })
    )

    return result.Item
  }

  async createTodo(todoItem) {
    logger.info('Creating todo', { todoItem })

    await this.docClient.send(
      new PutCommand({
        TableName: this.todosTable,
        Item: todoItem
      })
    )

    return todoItem
  }

  async updateTodo(userId, todoId, todoUpdate) {
    logger.info('Updating todo', { userId, todoId, todoUpdate })

    await this.docClient.send(
      new UpdateCommand({
        TableName: this.todosTable,
        Key: { userId, todoId },
        // Only touch the three editable fields, leaving createdAt
        // and attachmentUrl untouched
        UpdateExpression: 'set #name = :name, dueDate = :dueDate, done = :done',
        ExpressionAttributeNames: {
          '#name': 'name'
        },
        ExpressionAttributeValues: {
          ':name': todoUpdate.name,
          ':dueDate': todoUpdate.dueDate,
          ':done': todoUpdate.done
        }
      })
    )
  }

  async updateAttachmentUrl(userId, todoId, attachmentUrl) {
    logger.info('Updating attachment url', { userId, todoId, attachmentUrl })

    await this.docClient.send(
      new UpdateCommand({
        TableName: this.todosTable,
        Key: { userId, todoId },
        UpdateExpression: 'set attachmentUrl = :attachmentUrl',
        ExpressionAttributeValues: {
          ':attachmentUrl': attachmentUrl
        }
      })
    )
  }

  async deleteTodo(userId, todoId) {
    logger.info('Deleting todo', { userId, todoId })

    await this.docClient.send(
      new DeleteCommand({
        TableName: this.todosTable,
        Key: { userId, todoId }
      })
    )
  }
}
