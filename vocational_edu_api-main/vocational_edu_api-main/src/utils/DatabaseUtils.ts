import { ConsoleLogger } from '@nestjs/common'
import mongoose, { Connection } from 'mongoose'
import config from '../config/config'

export const connections: Record<string | keyof typeof config.DATABASE, Connection> = {}

const connectionStatus: Record<string, any> = {}

export function createConnectionByName(name: keyof typeof config.DATABASE, createConnection: () => any) {
  connections[name] = createConnection()
  if (name === 'main') {
    connections[name] = mongoose.connection
  }
  connections[name].on('error', (err: any) => {
    new ConsoleLogger().error(`MongoDB connection error: ${err}`)
    if (connectionStatus[name + 'Reject']) {
      connectionStatus[name + 'Reject'](err)
      connectionStatus[name + 'Reject'] = null
    }
    connectionStatus[name + 'Connected'] = false
  })
  connections[name].on('connected', () => {
    new ConsoleLogger().log('MongoDB connection connected')
    if (connectionStatus[name + 'Resolve']) {
      connectionStatus[name + 'Resolve']()
      connectionStatus[name + 'Resolve'] = null
    }
    connectionStatus[name + 'Connected'] = true
  })
  connections[name].on('disconnected', (err: any) => {
    new ConsoleLogger().log('MongoDB connection disconnected')
    connectionStatus[name + 'Connected'] = false
  })
}

function ensureConnection(name: keyof typeof config.DATABASE) {
  if (connectionStatus[name + 'Connected']) {
    return Promise.resolve()
  }
  return new Promise((resolve, reject) => {
    connectionStatus[name + 'Resolve'] = resolve
    connectionStatus[name + 'Reject'] = reject
  })
}

export async function connectDatabase(names: (keyof typeof config.DATABASE)[]) {
  const logger = new ConsoleLogger()
  logger.log('connecting to mongoose')
  for (const name of names) {
    if (!connections[name]) {
      throw new Error(`Database connection ${name} not found`)
    }
    await ensureConnection(name)
  }
}
