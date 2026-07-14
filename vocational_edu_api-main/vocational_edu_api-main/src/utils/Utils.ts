import { FastifyRequest } from 'fastify'
// import * as xlsx from 'xlsx'

export function blurLargeNumber(count: number): string {
  if (typeof count !== 'number') {
    return count
  }
  if (count <= 0) {
    return '0'
  }
  if (count <= 1000) {
    return '少于1000'
  }
  if (count <= 5000) {
    return '1000+'
  }
  if (count <= 10000) {
    return '5000+'
  }
  if (count <= 100000) {
    return Math.floor((count - 1) / 10000) + '万+'
  }
  if (count <= 1000000) {
    return Math.floor((count - 1) / 100000) + '0万+'
  }
  return Math.floor((count - 1) / 1000000) + '00万+'
}

export function blurSmallNumber(count: number): number {
  if (count <= 50) {
    return count
  }
  if (count <= 100) {
    return 51
  }
  if (count <= 1000) {
    return Math.floor((count - 1) / 100) * 100
  }
  if (count <= 10000) {
    return Math.floor((count - 1) / 1000) * 1000
  }
  return Math.floor((count - 1) / 10000) * 10000
}

export function getIp(req: FastifyRequest) {
  const ip = req.headers['x-forwarded-for'] || req.headers['x-real-ip'] || req.ip || ''
  if (typeof ip === 'string' && ip.includes(',')) {
    return ip.split(',')[0]
  }
  return Array.isArray(ip) ? ip[0] : ip
}

export function randomString(len: number, alpha?: string) {
  alpha = alpha || 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  const maxPos = alpha.length
  let str = ''
  for (let i = 0; i < len; i++) {
    str += alpha.charAt(Math.floor(Math.random() * maxPos))
  }
  return str
}

// export function readExcelToJson(xlsxFilePath: string) {
//   const workbook = xlsx.readFile(xlsxFilePath)
//   const sheetNames = workbook.SheetNames
//   const sheet = workbook.Sheets[sheetNames[0]]
//   return xlsx.utils.sheet_to_json(sheet)
// }
