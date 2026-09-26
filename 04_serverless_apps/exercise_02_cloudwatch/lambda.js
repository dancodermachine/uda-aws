import {
  CloudWatchClient,
  PutMetricDataCommand
} from '@aws-sdk/client-cloudwatch'
import axios from 'axios'

// Name of a service, any string
const serviceName = process.env.SERVICE_NAME
// URL of a service to test
const url = process.env.URL

// CloudWatch client
const cloudwatch = new CloudWatchClient()

export async function handler(event) {
  // Use these variables to record metric values
  let endTime
  let requestWasSuccessful

  const startTime = timeInMs()
  try {
    await axios.get(url)
    requestWasSuccessful = true
  } catch (error) {
    // axios throws on network errors and HTTP error status codes
    requestWasSuccessful = false
  } finally {
    endTime = timeInMs()
  }

  const latencyInMs = endTime - startTime

  // Record time it took to get a response
  const latencyMetricCommand = new PutMetricDataCommand({
    MetricData: [
      {
        MetricName: 'Latency',
        Dimensions: [
          {
            Name: 'ServiceName',
            Value: serviceName
          }
        ],
        Unit: 'Milliseconds',
        Value: latencyInMs
      }
    ],
    Namespace: 'Udacity/Serveless'
  })
  await cloudwatch.send(latencyMetricCommand)

  // Record if a response was successful or not
  const successMetricCommand = new PutMetricDataCommand({
    MetricData: [
      {
        MetricName: 'Success',
        Dimensions: [
          {
            Name: 'ServiceName',
            Value: serviceName
          }
        ],
        Unit: 'Count',
        Value: requestWasSuccessful ? 1 : 0
      }
    ],
    Namespace: 'Udacity/Serveless'
  })
  await cloudwatch.send(successMetricCommand)
}

function timeInMs() {
  return new Date().getTime()
}