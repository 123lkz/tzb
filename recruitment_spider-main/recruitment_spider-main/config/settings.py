import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量（从项目根目录的.env文件）
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

# MongoDB配置
MONGODB = {
    'uri': os.getenv('MONGO_URI'),  # 从.env获取
    'database': os.getenv('MONGO_DB'),
    'collection_raw': os.getenv('MONGO_COLLECTION_RAW'),
    'collection_clean': os.getenv('MONGO_COLLECTION_CLEAN')
}

# MongoDB连接设置
MONGODB_SETTINGS = {
    'serverSelectionTimeoutMS': 5000,
    'connectTimeoutMS': 5000,
    'socketTimeoutMS': 5000,
    'heartbeatFrequencyMS': 30000,
    'retryWrites': True,
    'maxPoolSize': 1,
    'minPoolSize': 1,
    'maxIdleTimeMS': 60000,
    'appname': 'recruitment_spider',
    'retryReads': True,
    'w': 'majority',
    'readPreference': 'primaryPreferred'
}

# 添加MongoDB重试设置
MONGODB_RETRY_TIMES = 3
MONGODB_RETRY_INTERVAL = 5

# Scrapy设置
BOT_NAME = 'recruitment_spider'
SPIDER_MODULES = ['recruitment_spider.spiders']
NEWSPIDER_MODULE = 'recruitment_spider.spiders'

# 爬虫配置
SPIDER_SETTINGS = {
    'DOWNLOAD_DELAY': 8,
    'CONCURRENT_REQUESTS': 1,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'RANDOMIZE_DOWNLOAD_DELAY': True,
}

# 中间件和Pipeline配置
DOWNLOADER_MIDDLEWARES = {
    # 'middlewares.proxy_middleware.ProxyMiddleware': 100,
    'recruitment_spider.middlewares.retry_middleware.RetryMiddleware': 200,
}

ITEM_PIPELINES = {
    'recruitment_spider.pipelines.data_clean.DataCleanPipeline': 300,
    'recruitment_spider.pipelines.storage.StoragePipeline': 400,
}

# 重试设置
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429, 301, 302]

# 添加此行
ROBOTSTXT_OBEY = False

# 启用Cookie
COOKIES_ENABLED = True

# 日志设置
LOG_ENABLED = False
import logging
logging.getLogger('pymongo.topology').setLevel(logging.ERROR) 
