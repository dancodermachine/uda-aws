import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3'
import { getSignedUrl } from '@aws-sdk/s3-request-presigner'
import AWSXRay from 'aws-xray-sdk-core'
import { createLogger } from '../utils/logger.mjs'

const logger = createLogger('AttachmentUtils')

// How long a presigned upload URL stays valid, in seconds
const URL_EXPIRATION = 300

export class AttachmentUtils {
  constructor(
    s3Client = AWSXRay.captureAWSv3Client(new S3Client()),
    bucketName = process.env.ATTACHMENTS_S3_BUCKET
  ) {
    this.s3Client = s3Client
    this.bucketName = bucketName
  }

  // Each todo has at most one attachment, stored under a key matching its todoId
  getAttachmentUrl(todoId) {
    return `https://${this.bucketName}.s3.amazonaws.com/${todoId}`
  }

  async getUploadUrl(todoId) {
    logger.info('Generating upload url', { todoId })

    return getSignedUrl(
      this.s3Client,
      new PutObjectCommand({
        Bucket: this.bucketName,
        Key: todoId
      }),
      { expiresIn: URL_EXPIRATION }
    )
  }
}
