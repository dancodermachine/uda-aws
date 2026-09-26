// const data = [
//   {
//     id: '1',
//     name: 'Dogs',
//     description: 'Only dog images here!'
//   },
//   {
//     id: '2',
//     name: 'Nature',
//     description: 'What can be a better object for photography'
//   },
//   {
//     id: '3',
//     name: 'Cities',
//     description: 'Creative display of urban settings'
//   }
// ]

import { DynamoDB } from '@aws-sdk/client-dynamodb'
import { DynamoDBDocument } from  '@aws-sdk/lib-dynamodb'

const dynamoDbClient = DynamoDBDocument.from(new DynamoDB())
const groupsTable = process.env.GROUPS_TABLE

export async function handler(event) {
  console.log('Processing event: ', event)

  const result = await dynamoDbClient.scan({
    TableName: groupsTable
  })
  const items = result.Items

  return {
    statusCode: 200,
    headers: {
      'Access-Control-Allow-Origin': '*'
    },
    body: JSON.stringify({
      items: items
    })
  }
}