#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智联招聘爬虫主程序
按顺序运行四个步骤：
1. 生成step1的URL
2. 验证step1的URL并生成step2的URL
3. 爬取step2的URL获取职位列表
4. 爬取职位详情
"""

import logging
import time
from datetime import datetime
from tqdm import tqdm
import os
import sys
# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.append(project_root)
# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    logger = get_logger(__name__, "zhilian_spider_main")
except ImportError:
    # 如果无法导入log_manager，则使用基本配置
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger("spiders.zhilian_spider_main")

def run_step1():
    """运行第一步：生成step1的URL"""
    try:
        logger.info("开始运行第一步：生成step1的URL")
        from zhilian_spider_step1 import ZhilianSpiderStep1
        spider = ZhilianSpiderStep1()
        spider.run()
        logger.info("第一步完成：step1的URL生成完成")
        return True
    except Exception as e:
        logger.error(f"第一步运行失败: {str(e)}")
        return False

def run_step2():
    """运行第二步：验证step1的URL并生成step2的URL"""
    try:
        logger.info("开始运行第二步：验证step1的URL并生成step2的URL")
        from zhilian_spider_step2 import ZhilianSpiderStep2
        spider = ZhilianSpiderStep2()
        spider.run()
        logger.info("第二步完成：step2的URL生成完成")
        return True
    except Exception as e:
        logger.error(f"第二步运行失败: {str(e)}")
        return False

def run_step3():
    """运行第三步：爬取step2的URL获取职位列表"""
    try:
        logger.info("开始运行第三步：爬取step2的URL获取职位列表")
        from zhilian_spider_step3 import ZhilianSpiderStep3
        spider = ZhilianSpiderStep3()
        spider.run()
        logger.info("第三步完成：职位列表爬取完成")
        return True
    except Exception as e:
        logger.error(f"第三步运行失败: {str(e)}")
        return False

def run_step4():
    """运行第四步：爬取职位详情"""
    try:
        logger.info("开始运行第四步：爬取职位详情")
        from zhilian_spider_step4 import ZhilianSpiderStep4
        spider = ZhilianSpiderStep4()
        spider.run()
        logger.info("第四步完成：职位详情爬取完成")
        return True
    except Exception as e:
        logger.error(f"第四步运行失败: {str(e)}")
        return False

def main():
    """主函数"""
    try:
        start_time = datetime.now()
        logger.info(f"开始运行智联招聘爬虫，开始时间：{start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 创建进度条
        steps = [
            ("第一步：生成step1的URL", run_step1),
            ("第二步：验证step1的URL并生成step2的URL", run_step2),
            ("第三步：爬取step2的URL获取职位列表", run_step3),
            ("第四步：爬取职位详情", run_step4)
        ]
        
        pbar = tqdm(steps, desc="总体进度", unit="步骤")
        
        for step_name, step_func in pbar:
            pbar.set_description(f"正在执行{step_name}")
            if not step_func():
                logger.error(f"{step_name}执行失败，程序终止")
                break
            time.sleep(2)  # 每个步骤之间暂停2秒
        
        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"智联招聘爬虫运行完成，结束时间：{end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"总运行时间：{duration}")
        
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()
