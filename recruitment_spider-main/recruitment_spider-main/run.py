import logging
import sys
import os
from pathlib import Path
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# 获取项目根目录并添加到系统路径
ROOT_DIR = Path(__file__).parent.parent.absolute()
PROJECT_DIR = Path(__file__).parent.absolute()
sys.path.append(str(ROOT_DIR))
from recruitment_spider.spiders.zhilian_spider import ZhilianSpider

def setup_project():
    """设置项目环境"""
    # 设置工作目录
    os.chdir(PROJECT_DIR)
    
    # 设置环境变量
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'recruitment_spider.config.settings')

def setup_logging():
    """配置日志系统"""
    logger = logging.getLogger()
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
        # 添加文件日志
        file_handler = logging.FileHandler('debug.log', encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        logger.addHandler(file_handler)

def get_spider_settings():
    """获取爬虫设置"""
    settings = get_project_settings()
    settings.update({
        'LOG_ENABLED': False,
        'LOG_LEVEL': 'INFO',
        'DOWNLOAD_DELAY': 8,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1
    })
    return settings

def run_spider():
    """运行爬虫"""
    try:
        # 初始化项目
        setup_project()
        setup_logging()
        
        # 获取设置并创建爬虫进程
        settings = get_spider_settings()
        process = CrawlerProcess(settings)
        
        # 运行爬虫
        logging.info('开始运行智联招聘爬虫')
        process.crawl(ZhilianSpider)
        process.start()
        
    except Exception as e:
        logging.error(f'爬虫运行错误: {str(e)}', exc_info=True)

if __name__ == '__main__':
    run_spider() 