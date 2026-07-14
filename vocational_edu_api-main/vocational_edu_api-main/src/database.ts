import mongoose from 'mongoose'
import config from './config/config'
import { createConnectionByName } from './utils/DatabaseUtils'

createConnectionByName('main', () => mongoose.connect(config.DATABASE.main.uri))
createConnectionByName('da', () => mongoose.createConnection(config.DATABASE.da.uri))
