#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
招聘网站爬虫统一启动脚本
支持智联招聘、BOSS直聘、应届生求职网爬虫
"""

import os
import sys
import asyncio
import logging
import argparse
import traceback
from pathlib import Path

# 统一设置Python路径
# 获取当前文件的绝对路径
current_file = os.path.abspath(__file__)
# 获取当前文件所在目录
current_dir = os.path.dirname(current_file)
# 获取项目根目录
project_root = current_dir
# 获取spiders目录
spiders_dir = os.path.join(project_root, 'spiders')

# 添加各种路径到Python路径
sys.path.append(project_root)  # 添加项目根目录
sys.path.append(spiders_dir)   # 添加spiders目录
sys.path.append(os.path.dirname(project_root))  # 添加项目父目录

# 设置环境变量，让爬虫知道项目根目录
os.environ['PROJECT_ROOT'] = project_root

# 导入日志管理模块
from utils.log_manager import configure_root_logger

# 配置日志
logger = configure_root_logger("recruitment_spider")

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='招聘网站爬虫统一启动脚本')
    parser.add_argument('--platform', type=str, default='all', choices=['zhilian', 'boss', 'yingjiesheng', 'liepin', 'qianchengwuyou', '58tongcheng', 'lagou', 'all'],
                        help='爬取平台: zhilian(智联招聘), boss(BOSS直聘), yingjiesheng(应届生求职网), liepin(猎聘网), qianchengwuyou(前程无忧), 58tongcheng(58同城), lagou(拉勾网), all(所有平台)')
    parser.add_argument('--city', type=str, default='全国',
                        help='搜索城市（默认：全国）')
    parser.add_argument('--headless', action='store_true', default=False,
                        help='是否使用无头模式运行浏览器（默认：否）')
    parser.add_argument('--browser-count', type=int, default=1,
                        help='浏览器实例数量（默认：1）')
    parser.add_argument('--tabs-per-browser', type=int, default=1,
                        help='每个浏览器的标签页数量（默认：1）')
    parser.add_argument('--debug', action='store_true',
                        help='启用调试模式')
    return parser.parse_args()

async def run_zhilian_spider(args):
    """运行智联招聘爬虫"""
    try:
        logger.info("开始运行智联招聘爬虫...")
        
        # 检查必要的目录是否存在
        data_dir = Path(os.path.join(project_root, "data/zhilian"))
        if not data_dir.exists():
            logger.error(f"数据目录不存在: {data_dir}")
            logger.info("正在创建数据目录...")
            data_dir.mkdir(parents=True, exist_ok=True)
        
        # 检查base_data.json是否存在
        base_data_path = data_dir / "base_data.json"
        if not base_data_path.exists():
            logger.error(f"基础数据文件不存在: {base_data_path}")
            logger.info("请确保base_data.json文件存在于正确的位置")
            return
        
        # 设置环境变量
        os.environ['HEADLESS'] = str(args.headless).lower()
        os.environ['BROWSER_COUNT'] = str(args.browser_count)
        os.environ['TABS_PER_BROWSER'] = str(args.tabs_per_browser)
        os.environ['CITY'] = args.city
        
        # 导入爬虫模块
        try:
            from spiders.zhilian_spider import main as zhilian_main
            logger.info("成功导入智联招聘爬虫模块")
        except ImportError as e:
            logger.error(f"导入智联招聘爬虫模块失败: {str(e)}")
            logger.info("请确保项目结构正确，并且已安装所有依赖")
            traceback.print_exc()
            return
        
        # 运行爬虫
        logger.info(f"使用城市: {args.city} 运行智联招聘爬虫")
        await zhilian_main()
        logger.info("智联招聘爬虫运行完成")
        
    except Exception as e:
        logger.error(f"运行智联招聘爬虫时出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

async def run_boss_spider(args):
    """运行BOSS直聘爬虫"""
    try:
        logger.info("开始运行BOSS直聘爬虫...")
        
        # 检查必要的目录是否存在
        data_dir = Path(os.path.join(project_root, "data/bosszhipin"))
        if not data_dir.exists():
            logger.error(f"数据目录不存在: {data_dir}")
            logger.info("正在创建数据目录...")
            data_dir.mkdir(parents=True, exist_ok=True)
        
        # 检查job_type.json是否存在
        job_type_file = data_dir / "job_type.json"
        if not job_type_file.exists():
            logger.error(f"职位类型文件不存在: {job_type_file}")
            logger.info("请确保job_type.json文件存在于正确的位置")
            return
        
        # 设置环境变量
        os.environ['HEADLESS'] = str(args.headless).lower()
        os.environ['BROWSER_COUNT'] = str(args.browser_count)
        os.environ['TABS_PER_BROWSER'] = str(args.tabs_per_browser)
        os.environ['CITY'] = args.city
        
        # 导入爬虫模块
        try:
            from spiders.boss_spider_part1 import main as boss_main
            logger.info("成功导入BOSS直聘爬虫模块")
        except ImportError as e:
            logger.error(f"导入BOSS直聘爬虫模块失败: {str(e)}")
            logger.info("请确保项目结构正确，并且已安装所有依赖")
            traceback.print_exc()
            return
        
        # 运行爬虫
        logger.info(f"使用城市: {args.city} 运行BOSS直聘爬虫")
        await boss_main()
        logger.info("BOSS直聘爬虫运行完成")
        
    except Exception as e:
        logger.error(f"运行BOSS直聘爬虫时出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

async def run_yingjiesheng_spider(args):
    """运行应届生求职网爬虫"""
    try:
        logger.info("开始运行应届生求职网爬虫...")
        
        # 检查必要的目录是否存在
        data_dir = Path(os.path.join(project_root, "data/yingjieshengqiuzhiwang"))
        if not data_dir.exists():
            logger.error(f"数据目录不存在: {data_dir}")
            logger.info("正在创建数据目录...")
            data_dir.mkdir(parents=True, exist_ok=True)
        
        # 检查job_type.json是否存在
        job_type_file = data_dir / "job_type.json"
        if not job_type_file.exists():
            logger.error(f"职位类型文件不存在: {job_type_file}")
            logger.info("请确保job_type.json文件存在于正确的位置")
            return
        
        # 设置环境变量
        os.environ['HEADLESS'] = str(args.headless).lower()
        os.environ['BROWSER_COUNT'] = str(args.browser_count)
        os.environ['TABS_PER_BROWSER'] = str(args.tabs_per_browser)
        os.environ['CITY'] = args.city
        
        # 导入爬虫模块
        try:
            from spiders.yingjiesheng_spider import main as yingjiesheng_main
            logger.info("成功导入应届生求职网爬虫模块")
        except ImportError as e:
            logger.error(f"导入应届生求职网爬虫模块失败: {str(e)}")
            logger.info("请确保项目结构正确，并且已安装所有依赖")
            traceback.print_exc()
            return
        
        # 运行爬虫
        logger.info(f"使用城市: {args.city} 运行应届生求职网爬虫")
        await yingjiesheng_main()
        logger.info("应届生求职网爬虫运行完成")
        
    except Exception as e:
        logger.error(f"运行应届生求职网爬虫时出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

async def run_liepin_spider(args):
    """运行猎聘网爬虫"""
    try:
        logger.info("开始运行猎聘网爬虫...")
        
        # 检查必要的目录是否存在
        data_dir = Path(os.path.join(project_root, "data/liepin"))
        if not data_dir.exists():
            logger.error(f"数据目录不存在: {data_dir}")
            logger.info("正在创建数据目录...")
            data_dir.mkdir(parents=True, exist_ok=True)
        
        # 检查city_code.json是否存在
        province_type_code_file = data_dir / "province_type_code.json"        
        if not province_type_code_file.exists():
            logger.error(f"配置文件不存在: {province_type_code_file}")
            logger.info(f"请确保{province_type_code_file.name}文件存在于正确的位置")
            return
        
        # 设置环境变量
        os.environ['HEADLESS'] = str(args.headless).lower()
        os.environ['BROWSER_COUNT'] = str(args.browser_count)
        os.environ['TABS_PER_BROWSER'] = str(args.tabs_per_browser)
        os.environ['CITY'] = args.city
        
        # 导入爬虫模块
        try:
            from spiders.liepin_spider import LiepinSpider
            logger.info("成功导入猎聘网爬虫模块")
        except ImportError as e:
            logger.error(f"导入猎聘网爬虫模块失败: {str(e)}")
            logger.info("请确保项目结构正确，并且已安装所有依赖")
            traceback.print_exc()
            return
        
        # 运行爬虫
        logger.info(f"使用城市: {args.city} 运行猎聘网爬虫")
        spider = LiepinSpider(
            headless=args.headless,
            browser_count=args.browser_count,
            tabs_per_browser=args.tabs_per_browser,
            city=args.city
        )
        await spider.run()
        logger.info("猎聘网爬虫运行完成")
        
    except Exception as e:
        logger.error(f"运行猎聘网爬虫时出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

async def run_qianchengwuyou_spider(args):
    """运行前程无忧爬虫"""
    try:
        logger.info("开始运行前程无忧爬虫...")
        
        # 检查必要的目录是否存在
        data_dir = Path(os.path.join(project_root, "data/qianchengwuyou"))
        if not data_dir.exists():
            logger.error(f"数据目录不存在: {data_dir}")
            logger.info("正在创建数据目录...")
            data_dir.mkdir(parents=True, exist_ok=True)
        
        # 检查city_code.json是否存在
        city_code_file = data_dir / "city_code.json"
        if not city_code_file.exists():
            logger.error(f"城市代码文件不存在: {city_code_file}")
            logger.info("请确保city_code.json文件存在于正确的位置")
            return
        
        # 设置环境变量
        os.environ['HEADLESS'] = str(args.headless).lower()
        os.environ['BROWSER_COUNT'] = str(args.browser_count)
        os.environ['TABS_PER_BROWSER'] = str(args.tabs_per_browser)
        os.environ['CITY'] = args.city
        
        # 导入爬虫模块
        try:
            from spiders.qianchengwuyou import QianchengwuyouSpider
            logger.info("成功导入前程无忧爬虫模块")
        except ImportError as e:
            logger.error(f"导入前程无忧爬虫模块失败: {str(e)}")
            logger.info("请确保项目结构正确，并且已安装所有依赖")
            traceback.print_exc()
            return
        
        # 运行爬虫
        logger.info(f"使用城市: {args.city} 运行前程无忧爬虫")
        spider = QianchengwuyouSpider(
            headless=args.headless,
            browser_count=args.browser_count,
            tabs_per_browser=args.tabs_per_browser,
            city=args.city,
            resource_filter_level="none"
        )
        await spider.run()
        logger.info("前程无忧爬虫运行完成")
        
    except Exception as e:
        logger.error(f"运行前程无忧爬虫时出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

async def run_58tongcheng_spider(args):
    """运行58同城爬虫"""
    try:
        logger.info("开始运行58同城爬虫...")
        
        # 检查必要的目录是否存在
        data_dir = Path(os.path.join(project_root, "data/58tongcheng"))
        if not data_dir.exists():
            logger.error(f"数据目录不存在: {data_dir}")
            logger.info("正在创建数据目录...")
            data_dir.mkdir(parents=True, exist_ok=True)
        
        # 检查city_codes.json是否存在
        city_code_file = data_dir / "city_codes.json"
        if not city_code_file.exists():
            logger.error(f"城市代码文件不存在: {city_code_file}")
            logger.info("请确保city_codes.json文件存在于正确的位置")
            return
        
        # 设置环境变量
        os.environ['HEADLESS'] = str(args.headless).lower()
        os.environ['BROWSER_COUNT'] = str(args.browser_count)
        os.environ['TABS_PER_BROWSER'] = str(args.tabs_per_browser)
        os.environ['CITY'] = args.city
        
        # 导入爬虫模块
        try:
            from spiders.tongcheng58 import Tongcheng58Spider
            logger.info("成功导入58同城爬虫模块")
        except ImportError as e:
            logger.error(f"导入58同城爬虫模块失败: {str(e)}")
            logger.info("请确保项目结构正确，并且已安装所有依赖")
            traceback.print_exc()
            return
        
        # 运行爬虫
        logger.info(f"使用城市: {args.city} 运行58同城爬虫")
        spider = Tongcheng58Spider(
            headless=args.headless,
            browser_count=args.browser_count,
            tabs_per_browser=args.tabs_per_browser,
            city=args.city,
            resource_filter_level="none"
        )
        await spider.run()
        logger.info("58同城爬虫运行完成")
        
    except Exception as e:
        logger.error(f"运行58同城爬虫时出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

async def run_lagou_spider(args):
    """运行拉勾网爬虫"""
    try:
        logger.info("开始运行拉勾网爬虫...")        
        # 检查必要的目录是否存在
        # data_dir = Path(os.path.join(project_root, "data/lagou"))
        # if not data_dir.exists():
        #     logger.error(f"数据目录不存在: {data_dir}")
        #     logger.info("正在创建数据目录...")
        #     data_dir.mkdir(parents=True, exist_ok=True)
        
        # # 检查必要的配置文件是否存在
        # job_type_file = data_dir / "job_type.json"
        # city_file = data_dir / "city.json"
        # industry_file = data_dir / "industry.json"
        
        # required_files = [
        #     (job_type_file, "职位类型"),
        #     (city_file, "城市代码"),
        #     (industry_file, "行业代码")
        # ]
        
        # for file_path, file_desc in required_files:
        #     if not file_path.exists():
        #         logger.error(f"{file_desc}文件不存在: {file_path}")
        #         logger.info(f"请确保{file_path.name}文件存在于正确的位置")
        #         return
        
        # 设置环境变量
        os.environ['HEADLESS'] = str(args.headless).lower()
        os.environ['BROWSER_COUNT'] = str(args.browser_count)
        os.environ['TABS_PER_BROWSER'] = str(args.tabs_per_browser)
        os.environ['CITY'] = args.city
        
        # 导入爬虫模块
        try:
            from spiders.lagou_spider_part1 import LagouSpider
            logger.info("成功导入拉勾网爬虫模块")
        except ImportError as e:
            logger.error(f"导入拉勾网爬虫模块失败: {str(e)}")
            logger.info("请确保项目结构正确，并且已安装所有依赖")
            traceback.print_exc()
            return
        
        # 运行爬虫
        # logger.info(f"使用城市: {args.city} 运行拉勾网爬虫")
        spider = LagouSpider(
            headless=args.headless,
            browser_count=args.browser_count,
            tabs_per_browser=args.tabs_per_browser,
            city=args.city
        )
        await spider.run()
        logger.info("拉勾网爬虫运行完成")
        
    except Exception as e:
        logger.error(f"运行拉勾网爬虫时出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

async def main():
    """主函数"""
    try:
        args = parse_arguments()
        
        # 设置调试模式环境变量
        if args.debug:
            os.environ['DEBUG_MODE'] = '1'
            logger.info("已启用调试模式")
        
        # 创建调试目录
        debug_dir = Path(os.path.join(project_root, "debug"))
        debug_dir.mkdir(exist_ok=True)
        
        # 创建任务列表
        tasks = []
        
        # 根据选择的平台创建相应的爬虫任务
        if args.platform == 'all':
            logger.info("将并行运行所有平台的爬虫...")
            # tasks.append(asyncio.create_task(run_zhilian_spider(args)))
            # tasks.append(asyncio.create_task(run_boss_spider(args)))
            # tasks.append(asyncio.create_task(run_yingjiesheng_spider(args)))
            # tasks.append(asyncio.create_task(run_liepin_spider(args)))
            # tasks.append(asyncio.create_task(run_qianchengwuyou_spider(args)))
            # tasks.append(asyncio.create_task(run_58tongcheng_spider(args)))
            tasks.append(asyncio.create_task(run_lagou_spider(args)))
        elif args.platform == 'zhilian':
            tasks.append(asyncio.create_task(run_zhilian_spider(args)))
        elif args.platform == 'boss':
            tasks.append(asyncio.create_task(run_boss_spider(args)))
        elif args.platform == 'yingjiesheng':
            tasks.append(asyncio.create_task(run_yingjiesheng_spider(args)))
        elif args.platform == 'liepin':
            tasks.append(asyncio.create_task(run_liepin_spider(args)))
        elif args.platform == 'qianchengwuyou':
            tasks.append(asyncio.create_task(run_qianchengwuyou_spider(args)))
        elif args.platform == '58tongcheng':
            tasks.append(asyncio.create_task(run_58tongcheng_spider(args)))
        elif args.platform == 'lagou':
            tasks.append(asyncio.create_task(run_lagou_spider(args)))
        
        # 并行执行所有任务
        if tasks:
            await asyncio.gather(*tasks)
        
        logger.info("所有爬虫任务完成")
        
    except Exception as e:
        logger.error(f"运行爬虫时出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    try:                
        # 运行主函数
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("用户中断，程序退出")
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc()) 