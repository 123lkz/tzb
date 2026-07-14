import nodemailer from 'nodemailer'
import config from '../config/config'

type SendMailOptions = {
  to: string[]
  subject: string
  html: string
  attachments?: {
    filename: string
    path: string
  }[]
}

export class MailService {
  static async sendAccountMail({ to, subject, html, attachments }: SendMailOptions) {
    if (!config.SMTP.account.user) {
      throw new Error('邮件服务未配置：请在 .env 中配置')
    }
    return new Promise<boolean>((resolve, reject) => {
      const transporter = nodemailer.createTransport({
        host: 'smtpdm.aliyun.com',
        port: 465,
        secure: true,
        auth: {
          user: config.SMTP.account.user,
          pass: config.SMTP.account.pass
        }
      })
      transporter.sendMail(
        {
          from: `师智云<${config.SMTP.account.user}>`,
          to: to.join(', '),
          subject: subject,
          html,
          attachments
        },
        (error, info) => {
          if (error) {
            reject(error)
          } else {
            resolve(true)
          }
        }
      )
    })
  }
}
