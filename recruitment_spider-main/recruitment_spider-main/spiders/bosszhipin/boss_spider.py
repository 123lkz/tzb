import json
import logging
import os
import re
import sys
import time
import argparse
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import asyncio
import urllib.parse
from dotenv import load_dotenv

from scrapy import Request
from scrapy.http import HtmlResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, UpdateOne
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from spiders.base_spider import BaseSpider

# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    # 配置日志，第一个参数是日志器名称，第二个参数是爬虫名称
    logger = get_logger(__name__, "boss_spider")
except ImportError:
    # 配置基本日志，以防日志管理模块未安装
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

# 设置调试模式
debug_mode = os.environ.get('DEBUG_MODE', '0') == '1'
if debug_mode:
    logger.setLevel(logging.DEBUG)
    logger.debug("BOSS直聘爬虫调试模式已启用")

# 城市代码映射
CITY_MAP = {
    '全国': '100010000',
    '北京': '101010100',
    '上海': '101020100',
    '广州': '101280100',
    '深圳': '101280600',
    '杭州': '101210100',
    '成都': '101270100',
    '武汉': '101200100',
    '南京': '101190100',
    '西安': '101110100',
    '长沙': '101250100',
}

class BossSpider(BaseSpider):
    """BOSS直聘爬虫，继承自BaseSpider"""
    name = 'boss_spider'
    
    def __init__(self, headless: bool = True, browser_count: int = 1, tabs_per_browser: int = 1, city: str = "全国", 
                 block_resources: bool = True, resource_filter_level: str = "medium", *args, **kwargs):
        super(BossSpider, self).__init__(
            headless=headless,
            browser_count=browser_count,
            tabs_per_browser=tabs_per_browser,
            city=city,
            block_resources=block_resources,
            resource_filter_level=resource_filter_level,
            *args, **kwargs
        )
        
        # 加载环境变量
        load_dotenv()
        
        # BOSS直聘特有配置
        self.city_code = CITY_MAP.get(city, '100010000')  # 默认全国
        self.base_url = "https://www.zhipin.com"
        
        # MongoDB配置从环境变量读取
        self.mongo_uri = os.getenv('BOSS_MONGO_URI')
        self.mongo_db = os.getenv('BOSS_MONGO_DB')
        self.collection_name = os.getenv('BOSS_MONGO_COLLECTION_RAW')
        self.url_collection_name = f"{self.collection_name}_urls"  # URL记录集合
        self.mongo_client = None
        self.db = None
        
        # URL缓存字典
        self.crawled_urls = {}
        
        if not all([self.mongo_uri, self.mongo_db, self.collection_name]):
            raise ValueError("MongoDB配置信息不完整，请检查环境变量")
        
        # 基础数据文件路径
        self.job_type_path = Path("recruitment_spider/data/bosszhipin/job_type.json")
        self.city_code_path = Path("recruitment_spider/data/bosszhipin/city_code.json")
        self.industry_code_path = Path("recruitment_spider/data/bosszhipin/industry_code.json")
        logger.info(f"基础数据文件路径: {self.job_type_path.absolute()}")
        
        # 爬虫配置
        self.min_delay = 3  # 最小等待时间（秒）
        self.max_delay = 7  # 最大等待时间（秒）
        self.max_retry_delay = 10  # 最大重试等待时间（秒）
        self.request_interval = 5  # 两次请求之间的最小间隔（秒）
        
        # 加载岗位代码
        self.job_codes = self.load_job_codes()
        # 加载公司行业代码
        self.company_industry_codes = self.load_company_industry_codes()
        # 加载城市代码
        self.city_codes = self.load_city_codes()
        
        # 上传者信息
        self.uploader = "单永旭"
    
    def load_job_codes(self) -> List[str]:
        """
        从JSON文件中加载职位代码
        只获取第三级职位代码
        """
        job_code_groups = []
        try:
            # 确保数据目录存在
            data_dir = Path("recruitment_spider/data/bosszhipin")
            if not data_dir.exists():
                logger.error(f"数据目录不存在: {data_dir}")
                data_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"已创建数据目录: {data_dir}")
                return []
            
            # 加载职位类型数据
            if not self.job_type_path.exists():
                logger.error(f"职位类型文件不存在: {self.job_type_path}")
                return []
            
            with open(self.job_type_path, 'r', encoding='utf-8') as f:
                job_type_data = json.load(f)
            
            # 只提取第三级职位代码
            for first_level in job_type_data.get('zpData', {}).get('position', []):
                for second_level in first_level.get('subLevelModelList', []):
                    for third_level in second_level.get('subLevelModelList', []):
                        third_code = third_level.get('code')
                        if third_code:
                            # 只添加三级职位代码
                            tmp_data = {
                                f"{third_code}":third_level.get('name')
                            }
                            job_code_groups.append(tmp_data)
            
            logger.info(f"成功加载 {len(job_code_groups)} 个第三级职位代码")
            return job_code_groups
        
        except Exception as e:
            logger.error(f"加载职位代码失败: {str(e)}")
            return []
    
    def load_city_codes(self) -> List[dict]:
        """
        从JSON文件中加载所有城市代码
        返回格式：[{code: name}, ...]
        """
        city_code_path = Path("recruitment_spider/data/bosszhipin/city_code.json")
        city_code_groups = []
        try:
            if not city_code_path.exists():
                logger.error(f"城市代码文件不存在: {city_code_path}")
                return []
            with open(city_code_path, 'r', encoding='utf-8') as f:
                city_data = json.load(f)
            for group in city_data:
                for city in group.get('cityList', []):
                    code = str(city.get('code'))
                    name = city.get('name')
                    if code and name:
                        city_code_groups.append({'name':name,'code': code})
            logger.info(f"成功加载 {len(city_code_groups)} 个城市代码")
            return city_code_groups
        except Exception as e:
            logger.error(f"加载城市代码失败: {str(e)}")
            return []
    
    def load_company_industry_codes(self) -> List[dict]:
        """
        从JSON文件中加载公司行业代码
        只获取子行业的代码和名称
        返回格式：[{code: name}, ...]
        """
        industry_code_groups = []
        try:
            # 确保数据目录存在
            data_dir = Path("recruitment_spider/data/bosszhipin")
            if not data_dir.exists():
                logger.error(f"数据目录不存在: {data_dir}")
                data_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"已创建数据目录: {data_dir}")
                return []
            
            # 加载行业类型数据
            if not self.industry_code_path.exists():
                logger.error(f"行业类型文件不存在: {self.industry_code_path}")
                return []
            
            with open(self.industry_code_path, 'r', encoding='utf-8') as f:
                industry_data = json.load(f)
            
            # 遍历所有父行业
            for parent_industry in industry_data.get('zpData', []):
                # 遍历子行业列表
                for sub_industry in parent_industry.get('subLevelModelList', []):
                    code = str(sub_industry.get('code'))
                    name = sub_industry.get('name')
                    if code and name:
                        industry_code_groups.append({'name':name,'code': code})
            
            logger.info(f"成功加载 {len(industry_code_groups)} 个子行业代码")
            return industry_code_groups
            
        except Exception as e:
            logger.error(f"加载行业代码失败: {str(e)}")
            return []
    
    async def init_browser(self):
        try:
            # 调用父类的初始化方法
            await super().init_browser()
            logger.info("浏览器初始化成功")            
            # 检查是否成功创建页面
            if not self.pages or len(self.pages) == 0:
                raise Exception("没有成功创建任何浏览器页面")                
            # 初始化成功，退出循环
            return
            
        except Exception as e:                        
            # 确保关闭已创建的资源
            if hasattr(self, 'browsers') and self.browsers:
                for browser in self.browsers:
                    try:
                        await browser.close()
                    except:
                        pass
                        
            if hasattr(self, 'playwright') and self.playwright:
                try:
                    await self.playwright.stop()
                except:
                    pass
            
            # 重置资源列表
            self.playwright = None
            self.browsers = []
            self.contexts = []
            self.pages = []            
            logger.error("浏览器初始化失败，已达到最大重试次数")
            raise
    
    
    async def run(self):
        """运行爬虫的主方法"""
        try:
            # 初始化数据库
            await self.init_db()
            logger.info("数据库初始化成功")
            
            # 初始化浏览器
            await self.init_browser()
            
            # 检查页面是否成功创建
            if not self.pages or len(self.pages) == 0:
                logger.error("没有可用的浏览器页面，请检查浏览器初始化是否成功")
                return
                
            logger.info(f"成功创建 {len(self.pages)} 个浏览器页面")
            
            # 获取总任务数量
            total_jobs = len(self.company_industry_codes)*len(self.city_codes)
            logger.info(f"总共需要处理 {total_jobs} 个岗位类型")
            
            # 初始化计数器
            completed_jobs = 0
            
            # 处理所有岗位类型
            tasks = []
            for i, industry in enumerate(self.company_industry_codes):
                for j, city in enumerate(self.city_codes):
                    # 为每个任务分配一个页面
                    page_index = i % len(self.pages)
                    task = asyncio.create_task(self.process_job_type(industry, city, page_index))
                    tasks.append(task)
                    
                    # 控制并发数量，避免过多任务同时执行
                    if len(tasks) >= len(self.pages):
                        await asyncio.gather(*tasks)
                        tasks = []
                        
                        # 更新完成数量
                        completed_jobs += len(self.pages)
                        progress = (completed_jobs / total_jobs) * 100
                        logger.info(f"进度: {completed_jobs}/{total_jobs} ({progress:.2f}%)")
                        
                        # 随机等待一段时间，避免请求过于频繁
                        await asyncio.sleep(random.uniform(self.min_delay, self.max_delay))
            
            # 处理剩余的任务
            if tasks:
                await asyncio.gather(*tasks)
                # 更新最终完成数量
                completed_jobs += len(tasks)
                progress = (completed_jobs / total_jobs) * 100
                logger.info(f"进度: {completed_jobs}/{total_jobs} ({progress:.2f}%)")
                
            logger.info("所有岗位类型处理完成")
            
        except Exception as e:
            logger.error(f"爬虫运行出错: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
        finally:
            # 关闭浏览器和数据库连接
            await self.close_browser()
    
    async def process_job_type(self, industry: str, city: str, page_index: int = 0):
        """处理特定职位类型"""
        try:
            # 检查页面索引是否有效
            if page_index >= len(self.pages) or not self.pages[page_index]:
                logger.error(f"无效的页面索引: {page_index}, 当前页面数量: {len(self.pages)}")
                return
                
            page = self.pages[page_index]
            
            # 检查页面是否已关闭
            if page.is_closed():
                logger.error(f"页面已关闭，无法处理岗位类型: {industry.get('name')}, {city.get('name')}")
                return
            
            # 构造URL
            industry_code = industry.get('code')
            industry_name = industry.get('name')
            city_name = city.get('name')
            city_code = city.get('code')
            url = self._build_search_url(industry_code, city_code)
            
            # 检查URL是否已经爬取过
            if await self.is_url_crawled(url):
                logger.info(f"URL已爬取过，跳过: {url}")
                return
                
            logger.info(f"处理行业: {industry_name}, 代码: {industry_code}, 城市名称：{city_name}, 代码: {city_code}, URL: {url}")
            
            # 获取职位列表
            jobs = await self.get_job_list(url, page)
            
            if not jobs:
                logger.warning(f"未找到岗位: {url}")
                await self.mark_url_crawled(url, success=False, job_count=0)
                return
            
            logger.info(f"获取到 {len(jobs)} 个岗位，直接保存到数据库")
            
            # 处理职位数据并保存到MongoDB
            processed_jobs = [self.process_job_data(job,city,industry) for job in jobs]
            await self.save_to_mongodb(processed_jobs, "boss")
            
            # 标记URL为已爬取
            await self.mark_url_crawled(url, success=True, job_count=len(jobs))
            
        except Exception as e:
            logger.error(f"获取或处理职位列表失败: {str(e)}")
            # 标记URL为爬取失败
            await self.mark_url_crawled(url, success=False, job_count=0)
            import traceback
            logger.error(traceback.format_exc())
    
    def _build_search_url(self, industry_code: str, city_code: str) -> str:
        """构建搜索URL"""
        # BOSS直聘的URL格式
        # 使用指定的URL格式: https://www.zhipin.com/web/geek/job?city=100010000&position=100101
        
        # 直接构建URL，不再使用随机选择的方式
        url = f"{self.base_url}/web/geek/job?city={city_code}&industry={industry_code}"
        logger.info(f"构建搜索URL: {url}")
        
        return url
    
    async def get_job_list(self, url: str, page: Page) -> List[Dict]:
        """获取职位列表"""
        try:

            # 确保页面是活跃的
            logger.info("确保页面处于活跃状态...")
            # 检查页面是否已关闭或不可用
            await self._check_page_availability(page, f"获取职位列表 {url}")
            # 访问URL
            logger.info(f"正在访问URL: {url}")            
            # 使用更可靠的加载策略，不等待networkidle
            try:
                await page.goto(url, wait_until='load', timeout=30000)
                logger.info("页面基本加载完成")
            except Exception as e:
                logger.warning(f"页面加载超时，但继续处理: {str(e)}")
                # 即使超时也继续处理，因为页面可能已经部分加载
            
            # 等待页面加载完成
            logger.info("等待页面加载完成...")
            await asyncio.sleep(random.uniform(3, 8))
            
            # 尝试滚动页面以加载更多内容
            logger.info("滚动页面以加载更多内容...")
            try:
                await page.evaluate("""
                    () => {
                        return new Promise((resolve) => {
                            let totalHeight = 0;
                            let distance = 300;
                            let timer = setInterval(() => {
                                window.scrollBy(0, distance);
                                totalHeight += distance;
                                
                                if(totalHeight >= 1500){
                                    clearInterval(timer);
                                    resolve();
                                }
                            }, 200);
                        });
                    }
                """)
                logger.info("页面滚动完成")
            except Exception as e:
                logger.warning(f"页面滚动失败: {str(e)}")
            
            # 再等待一段时间
            # await asyncio.sleep(3)
            
            # 保存页面截图用于调试
            # debug_dir = Path("debug")
            # debug_dir.mkdir(exist_ok=True)
            # screenshot_path = debug_dir / f"boss_page_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            # await page.screenshot(path=str(screenshot_path))
            # logger.info(f"页面截图已保存到: {screenshot_path}")
            
            # 保存页面HTML用于调试
            # html_path = debug_dir / f"boss_page_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
            # html_content = await page.content()
            # with open(html_path, 'w', encoding='utf-8') as f:
            #     f.write(html_content)
            # logger.info(f"页面HTML已保存到: {html_path}")
            
            # 尝试查找各种可能的职位列表结构
            selectors = [
                '.job-list-wrapper .job-card-wrapper',  # 第一种结构
                '.job-list .job-primary',               # 第二种结构
                '.job-list-box .job-card-wrapper',      # 可能的变体
                '.search-job-result .job-card-wrapper', # 可能的变体
                '.job-list-wrapper li',                 # 更通用的选择器
                '.job-list li',                         # 更通用的选择器
                '.search-job-result li',                # 更通用的选择器
                'li.job-card-wrapper',                  # 直接选择li元素
                'li .job-primary',                      # 直接选择li下的job-primary
                '.job-card-body',                       # 职位卡片主体
                '.primary-box'                          # 另一种可能的结构
            ]
            
            # 尝试所有可能的选择器
            for selector in selectors:
                logger.info(f"尝试使用选择器: {selector}")
                try:
                    # 使用更长的超时时间
                    job_elements = await page.query_selector_all(selector)
                    if len(job_elements) > 0:
                        logger.info(f"使用选择器 {selector} 找到 {len(job_elements)} 个职位")
                        
                        # 根据选择器类型确定解析方法
                        if '.job-card-wrapper' in selector or 'job-card-body' in selector:
                            return await self._parse_job_list_v1(job_elements)
                        elif '.job-primary' in selector or 'primary-box' in selector:
                            return await self._parse_job_list_v2(job_elements)
                        else:
                            # 尝试检测元素类型
                            first_class = await job_elements[0].get_attribute('class')
                            if first_class and ('job-card-wrapper' in first_class or 'job-card-body' in first_class):
                                return await self._parse_job_list_v1(job_elements)
                            elif first_class and ('job-primary' in first_class or 'primary-box' in first_class):
                                return await self._parse_job_list_v2(job_elements)
                            else:
                                logger.warning(f"找到元素但无法确定类型: {first_class}")
                                # 尝试使用第一种解析方法
                                return await self._parse_job_list_v1(job_elements)
                except Exception as e:
                    logger.warning(f"使用选择器 {selector} 查找元素时出错: {str(e)}")
            
            # 如果所有选择器都失败，尝试直接从HTML中提取信息
            logger.warning("所有选择器都未找到职位列表，尝试从HTML中直接提取...")
            html_content = await page.content()
            
            # 检查HTML中是否包含职位信息的特征
            if 'job-card-wrapper' in html_content or 'job-card-body' in html_content:
                logger.info("HTML中包含第一种结构的特征")
                # 尝试再次使用选择器，但使用evaluate方法
                elements_count = await page.evaluate("""
                    () => {
                        const elements = document.querySelectorAll('.job-card-wrapper, .job-card-body');
                        return elements.length;
                    }
                """)
                logger.info(f"使用JavaScript找到 {elements_count} 个第一种结构的元素")
                
                if elements_count > 0:
                    # 重新尝试获取元素
                    job_elements = await page.query_selector_all('.job-card-wrapper, .job-card-body')
                    if len(job_elements) > 0:
                        return await self._parse_job_list_v1(job_elements)
                
            elif 'job-primary' in html_content or 'primary-box' in html_content:
                logger.info("HTML中包含第二种结构的特征")
                # 尝试再次使用选择器，但使用evaluate方法
                elements_count = await page.evaluate("""
                    () => {
                        const elements = document.querySelectorAll('.job-primary, .primary-box');
                        return elements.length;
                    }
                """)
                logger.info(f"使用JavaScript找到 {elements_count} 个第二种结构的元素")
                
                if elements_count > 0:
                    # 重新尝试获取元素
                    job_elements = await page.query_selector_all('.job-primary, .primary-box')
                    if len(job_elements) > 0:
                        return await self._parse_job_list_v2(job_elements)
            
            # 如果仍然找不到，记录错误并返回空列表
            logger.error("无法找到任何职位列表元素")
            return []
            
        except Exception as e:
            logger.error(f"获取职位列表失败: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return []
            
    async def _parse_job_list_v1(self, job_elements) -> List[Dict]:
        """解析第一种结构的职位列表（新版）"""
        jobs = []
        for job_element in job_elements:
            try:
                # 提取职位ID和URL
                job_link = await job_element.query_selector('.job-card-left')
                if not job_link:
                    continue
                
                job_url = await job_link.get_attribute('href')
                if job_url and not job_url.startswith('http'):
                    job_url = f"{self.base_url}{job_url}"
                
                # 从URL中提取job_id
                job_id_match = re.search(r'/job_detail/([^\.]+)\.html', job_url)
                job_id = job_id_match.group(1) if job_id_match else None
                
                if not job_id:
                    continue
                
                # 提取职位名称
                job_name_element = await job_element.query_selector('.job-name')
                job_name = await job_name_element.text_content() if job_name_element else ""
                
                # 提取薪资
                salary_element = await job_element.query_selector('.salary')
                salary = await salary_element.text_content() if salary_element else "面议"
                
                # 提取公司名称
                company_name_element = await job_element.query_selector('.company-name a')
                company_name = await company_name_element.text_content() if company_name_element else ""
                
                # 提取公司URL
                company_url = await company_name_element.get_attribute('href') if company_name_element else ""
                if company_url and not company_url.startswith('http'):
                    company_url = f"{self.base_url}{company_url}"
                
                # 提取工作地点
                location_element = await job_element.query_selector('.job-area')
                location = await location_element.text_content() if location_element else ""
                
                # 提取工作经验和学历要求
                tag_elements = await job_element.query_selector_all('.job-info .tag-list li')
                experience = ""
                education = ""
                
                for tag_element in tag_elements:
                    tag_text = await tag_element.text_content()
                    if "年" in tag_text:
                        experience = tag_text
                    elif "本科" in tag_text or "大专" in tag_text or "硕士" in tag_text or "博士" in tag_text:
                        education = tag_text
                
                # 提取公司类型和规模
                company_tag_elements = await job_element.query_selector_all('.company-tag-list li')
                company_industry = ""
                company_finance = ""
                company_size = ""
                
                if len(company_tag_elements) >= 1:
                    company_industry = await company_tag_elements[0].text_content()
                if len(company_tag_elements) >= 2:
                    company_finance = await company_tag_elements[1].text_content()
                if len(company_tag_elements) >= 3:
                    company_size = await company_tag_elements[2].text_content()
                
                # 提取职位标签
                job_tag_elements = await job_element.query_selector_all('.job-card-footer .tag-list li')
                job_tags = []
                for tag_element in job_tag_elements:
                    tag = await tag_element.text_content()
                    if tag:
                        job_tags.append(tag.strip())
                
                # 提取职位描述
                job_desc_element = await job_element.query_selector('.info-desc')
                job_desc = await job_desc_element.text_content() if job_desc_element else ""
                
                # 提取招聘人信息
                recruiter_element = await job_element.query_selector('.info-public')
                recruiter_info = await recruiter_element.text_content() if recruiter_element else ""
                
                recruiter_name = ""
                recruiter_position = ""
                if recruiter_info:
                    recruiter_parts = recruiter_info.split('招聘')
                    if len(recruiter_parts) > 0:
                        recruiter_name = recruiter_parts[0].strip()
                    
                    # 检查是否有职位信息
                    em_element = await recruiter_element.query_selector('em')
                    if em_element:
                        recruiter_position = await em_element.text_content()
                
                # 检查HR是否在线
                hr_online = False
                online_element = await job_element.query_selector('.boss-online-tag')
                if online_element:
                    hr_online = True
                
                # 构建职位数据
                job_data = {
                    'job_id': job_id,
                    'job_name': job_name.strip() if job_name else "",
                    'salary': salary.strip() if salary else "面议",
                    'company_name': company_name.strip() if company_name else "",
                    'company_url': company_url if company_url else "",
                    'location': location.strip() if location else "",
                    'experience': experience.strip() if experience else "",
                    'education': education.strip() if education else "",
                    'company_industry': company_industry.strip() if company_industry else "",
                    'company_finance': company_finance.strip() if company_finance else "",
                    'company_size': company_size.strip() if company_size else "",
                    'job_tags': job_tags,
                    'job_desc': job_desc.strip() if job_desc else "",
                    'recruiter_name': recruiter_name,
                    'recruiter_position': recruiter_position,
                    'hr_online': hr_online,
                    'job_url': job_url if job_url else "",
                }
                
                jobs.append(job_data)
                
            except Exception as e:
                logger.error(f"解析职位项出错: {str(e)}")
                continue
        
        return jobs
        
    async def _parse_job_list_v2(self, job_elements) -> List[Dict]:
        """解析第二种结构的职位列表（旧版）"""
        jobs = []
        for job_element in job_elements:
            try:
                # 提取职位ID和URL
                job_link = await job_element.query_selector('.primary-box')
                if not job_link:
                    continue
                
                job_url = await job_link.get_attribute('href')
                if job_url and not job_url.startswith('http'):
                    job_url = f"{self.base_url}{job_url}"
                
                # 从URL中提取job_id
                job_id_match = re.search(r'/job_detail/([^\.]+)\.html', job_url)
                job_id = job_id_match.group(1) if job_id_match else None
                
                if not job_id:
                    continue
                
                # 提取职位名称
                job_name_element = await job_element.query_selector('.job-name a')
                job_name = await job_name_element.text_content() if job_name_element else ""
                
                # 提取薪资
                salary_element = await job_element.query_selector('.job-limit .red')
                salary = await salary_element.text_content() if salary_element else "面议"
                
                # 提取公司名称
                company_name_element = await job_element.query_selector('.info-company .name a')
                company_name = await company_name_element.text_content() if company_name_element else ""
                
                # 提取公司URL
                company_url = await company_name_element.get_attribute('href') if company_name_element else ""
                if company_url and not company_url.startswith('http'):
                    company_url = f"{self.base_url}{company_url}"
                
                # 提取工作地点
                location_element = await job_element.query_selector('.job-area')
                location = await location_element.text_content() if location_element else ""
                
                # 提取工作经验和学历要求
                limit_info_element = await job_element.query_selector('.job-limit p')
                limit_info = await limit_info_element.text_content() if limit_info_element else ""
                
                experience = ""
                education = ""
                
                # 解析工作经验和学历
                if limit_info:
                    parts = limit_info.split('·')
                    for part in parts:
                        part = part.strip()
                        if "周" in part or "天" in part:
                            experience = part
                        elif "本科" in part or "大专" in part or "硕士" in part or "博士" in part:
                            education = part
                
                # 提取公司类型和规模
                company_info_element = await job_element.query_selector('.info-company p')
                company_info = await company_info_element.text_content() if company_info_element else ""
                
                company_industry = ""
                company_finance = ""
                company_size = ""
                
                if company_info:
                    parts = company_info.split('·')
                    if len(parts) >= 1:
                        company_industry = parts[0].strip()
                    if len(parts) >= 2:
                        company_finance = parts[1].strip()
                    if len(parts) >= 3:
                        company_size = parts[2].strip()
                
                # 提取职位标签
                job_tag_elements = await job_element.query_selector_all('.info-append .tags .tag-item')
                job_tags = []
                for tag_element in job_tag_elements:
                    tag = await tag_element.text_content()
                    if tag:
                        job_tags.append(tag.strip())
                
                # 提取职位描述
                job_desc_element = await job_element.query_selector('.info-desc')
                job_desc = await job_desc_element.text_content() if job_desc_element else ""
                
                # 提取招聘人信息
                recruiter_element = await job_element.query_selector('.info-publis .name')
                recruiter_info = await recruiter_element.text_content() if recruiter_element else ""
                
                recruiter_name = ""
                recruiter_position = ""
                if recruiter_info:
                    parts = recruiter_info.split('·')
                    if len(parts) >= 1:
                        recruiter_name = parts[0].strip().replace('牟先生', '').strip()
                    if len(parts) >= 2:
                        recruiter_position = parts[1].strip()
                
                # 构建职位数据
                job_data = {
                    'job_id': job_id,
                    'job_name': job_name.strip() if job_name else "",
                    'salary': salary.strip() if salary else "面议",
                    'company_name': company_name.strip() if company_name else "",
                    'company_url': company_url if company_url else "",
                    'location': location.strip() if location else "",
                    'experience': experience.strip() if experience else "",
                    'education': education.strip() if education else "",
                    'company_industry': company_industry.strip() if company_industry else "",
                    'company_finance': company_finance.strip() if company_finance else "",
                    'company_size': company_size.strip() if company_size else "",
                    'job_tags': job_tags,
                    'job_desc': job_desc.strip() if job_desc else "",
                    'recruiter_name': recruiter_name,
                    'recruiter_position': recruiter_position,
                    'hr_online': False,  # 旧版没有直接提供HR在线状态
                    'job_url': job_url if job_url else "",
                }
                
                jobs.append(job_data)
                
            except Exception as e:
                logger.error(f"解析职位项出错: {str(e)}")
                continue
        
        return jobs
    
    async def get_job_detail(self, job_data: Dict, page: Page) -> Dict:
        """获取职位详情"""
        try:
            job_url = job_data.get('job_url')
            if not job_url:
                logger.warning("职位URL为空，无法获取详情")
                return job_data
                
            # 访问详情页
            await page.goto(job_url, wait_until='networkidle')
            
            # 等待页面加载完成
            await asyncio.sleep(random.uniform(2, 4))
            
            # 获取职位描述
            job_description_element = await page.query_selector('.job-detail .job-sec .text')
            job_description = await job_description_element.text_content() if job_description_element else ""
            
            # 获取公司描述
            company_description_element = await page.query_selector('.job-detail .job-sec:nth-child(2) .text')
            company_description = await company_description_element.text_content() if company_description_element else ""
            
            # 获取职位亮点
            job_highlights_elements = await page.query_selector_all('.job-detail .job-sec:nth-child(3) .job-tags span')
            job_highlights = []
            for highlight_element in job_highlights_elements:
                highlight = await highlight_element.text_content()
                if highlight:
                    job_highlights.append(highlight.strip())
            
            # 更新职位数据
            job_data['job_description'] = job_description.strip() if job_description else ""
            job_data['company_description'] = company_description.strip() if company_description else ""
            job_data['job_highlights'] = job_highlights
            
            return job_data
            
        except Exception as e:
            logger.error(f"获取职位详情失败: {str(e)}")
            return job_data
    
    def process_job_data(self, job_data: Dict,city: Dict, industry: Dict) -> Dict:
        """处理职位数据，转换为统一格式"""
        try:
            city_name = city.get('name')
            city_code = city.get('code')
            industry_name = industry.get('name')
            industry_code = industry.get('code')
            
            # 提取城市和区域
            location = job_data.get('location', '')
            city_district = location.split('·')
            city = city_district[0].strip() if city_district else ''
            district = city_district[1].strip() if len(city_district) > 1 else ''
            
            # 提取薪资范围
            salary = job_data.get('salary', '')
            salary_min = 0
            salary_max = 0
            salary_unit = "千/月"
            
            if salary and salary != "面议":
                # 处理不同格式的薪资
                if "元/天" in salary or "元/日" in salary:
                    # 处理日薪格式，如"150-200元/天"
                    salary_match = re.search(r'(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)', salary)
                    if salary_match:
                        daily_min = float(salary_match.group(1))
                        daily_max = float(salary_match.group(2))
                        # 假设一个月工作22天，转换为月薪（千/月）
                        salary_min = daily_min * 22 / 1000
                        salary_max = daily_max * 22 / 1000
                        salary_unit = "千/月(换算)"
                else:
                    # 解析薪资格式，如"15-20K"、"15-20K·13薪"
                    salary_parts = salary.split('·')
                    salary_range = salary_parts[0]
                    
                    # 提取数字部分
                    salary_match = re.search(r'(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)(K|k|万|元)', salary_range)
                    if salary_match:
                        salary_min = float(salary_match.group(1))
                        salary_max = float(salary_match.group(2))
                        unit = salary_match.group(3).lower()
                        
                        # 确定单位
                        if unit == 'k' or unit == 'K':
                            salary_unit = "千/月"
                        elif unit == '万':
                            salary_unit = "万/月"
                            # 转换为千/月
                            salary_min *= 10
                            salary_max *= 10
                        elif unit == '元':
                            salary_unit = "元/月"
                            # 转换为千/月
                            salary_min /= 1000
                            salary_max /= 1000
            
            # 处理招聘人信息
            recruiter_name = job_data.get('recruiter_name', '')
            recruiter_position = job_data.get('recruiter_position', '')
            
            # 构造符合jobs_raw集合格式的数据
            processed_data = {
                'job_id': job_data.get('job_id', ''),
                'title': job_data.get('job_name', ''),
                'company': job_data.get('company_name', ''),
                'salary': salary,
                'city': city,
                'district': district,
                'experience': job_data.get('experience', ''),
                'education': job_data.get('education', ''),
                'company_type': job_data.get('company_finance', ''),  # 使用融资状态作为公司类型
                'company_size': job_data.get('company_size', ''),
                'company_industry': job_data.get('company_industry', ''),
                'job_type': job_data.get('job_type', '全职'),  # 默认为全职
                'job_tags': job_data.get('job_tags', []),
                'job_url': job_data.get('job_url', ''),
                'hr_name': recruiter_name,
                'hr_position': recruiter_position,
                'hr_active': job_data.get('hr_online', ''),
                'publish_time': job_data.get('publish_time', ''),
                'update_time': job_data.get('update_time', ''),
                'source': 'boss',
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'company_url': job_data.get('company_url', ''),
                'uploader': self.uploader,
                # 额外字段，用于存储解析后的薪资范围
                'salary_min': salary_min,
                'salary_max': salary_max,
                'salary_unit': salary_unit,
                'city_name':city_name,
                'city_code':city_code,
                'industry_name':industry_name,
                'industry_code':industry_code,
            }
            
            return processed_data
            
        except Exception as e:
            logger.error(f"处理职位数据失败: {str(e)}")
            # 返回原始数据，添加source和crawl_time
            job_data['source'] = 'boss'
            job_data['crawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            job_data['uploader'] = self.uploader
            return job_data

    async def init_db(self):
        """初始化MongoDB连接"""
        try:
            # 创建MongoDB客户端连接
            self.mongo_client = AsyncIOMotorClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            
            # 测试连接
            await self.db.command("ping")
            logger.info("MongoDB连接成功")
            
            # 创建索引
            collection = self.db[self.collection_name]
            await collection.create_index([("job_id", ASCENDING)], unique=True)
            
            # 创建URL集合的索引
            url_collection = self.db[self.url_collection_name]
            await url_collection.create_index([("url", ASCENDING)], unique=True)
            await url_collection.create_index([("crawl_time", ASCENDING)])
            
            # 加载已爬取的URL到缓存
            await self.load_crawled_urls()
            
            logger.info("MongoDB索引创建成功")
            
        except Exception as e:
            logger.error(f"MongoDB连接失败: {str(e)}")
            raise

    async def load_crawled_urls(self):
        """
        从数据库加载所有已爬取的URL到内存中
        """
        try:
            url_collection = self.db[self.url_collection_name]
            cursor = url_collection.find(
                {"success": True},  # 只加载成功爬取的URL
                {"url": 1, "crawl_time": 1, "job_count": 1}
            )
            
            self.crawled_urls.clear()
            async for doc in cursor:
                self.crawled_urls[doc["url"]] = {
                    "crawl_time": doc.get("crawl_time"),
                    "job_count": doc.get("job_count", 0)
                }
            
            logger.info(f"已加载 {len(self.crawled_urls)} 个已爬取的URL到缓存")
        except Exception as e:
            logger.error(f"加载已爬取URL失败: {str(e)}")
            self.crawled_urls = {}

    async def is_url_crawled(self, url: str) -> bool:
        """
        检查URL是否已经爬取过（使用内存缓存）
        :param url: 要检查的URL
        :return: 如果已爬取过返回True，否则返回False
        """
        return url in self.crawled_urls

    async def mark_url_crawled(self, url: str, success: bool = True, job_count: int = 0):
        """
        标记URL为已爬取，同时更新内存缓存和数据库
        :param url: 已爬取的URL
        :param success: 爬取是否成功
        :param job_count: 获取到的职位数量
        """
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 更新内存缓存
            if success:
                self.crawled_urls[url] = {
                    "crawl_time": current_time,
                    "job_count": job_count
                }
            
            # 更新数据库
            url_collection = self.db[self.url_collection_name]
            document = {
                "url": url,
                "crawl_time": current_time,
                "success": success,
                "job_count": job_count,
                "industry_code": url.split("industry=")[-1] if "industry=" in url else "",
                "city_code": url.split("city=")[-1].split("&")[0] if "city=" in url else ""
            }
            await url_collection.update_one(
                {"url": url},
                {"$set": document},
                upsert=True
            )
        except Exception as e:
            logger.error(f"标记URL状态失败: {str(e)}")

    async def save_to_mongodb(self, jobs: List[Dict], source: str):
        """
        将职位数据保存到MongoDB
        :param jobs: 职位数据列表
        :param source: 数据来源
        """
        if not jobs:
            logger.warning("没有数据需要保存")
            return
            
        try:
            collection = self.db[self.collection_name]
            
            # 批量更新操作
            operations = []
            for job in jobs:
                # 使用job_id作为唯一标识
                filter_query = {"job_id": job["job_id"]}
                update_query = {
                    "$set": job,
                    "$setOnInsert": {
                        "first_crawl_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                }
                operations.append(UpdateOne(filter_query, update_query, upsert=True))
            
            if operations:
                # 执行批量更新
                result = await collection.bulk_write(operations)
                logger.info(f"MongoDB保存成功 - 已插入: {result.upserted_count}, 已修改: {result.modified_count}, 总数: {len(operations)}")
            
        except Exception as e:
            logger.error(f"MongoDB保存失败: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

    async def close_spider(self):
        """关闭爬虫时的清理操作"""
        try:
            if self.mongo_client:
                self.mongo_client.close()
                logger.info("MongoDB连接已关闭")
        except Exception as e:
            logger.error(f"关闭MongoDB连接失败: {str(e)}")

# 解析命令行参数
def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='BOSS直聘爬虫')
    parser.add_argument('--headless', action='store_true', default=False,
                        help='是否使用无头模式运行浏览器（默认：否）')
    parser.add_argument('--browser-count', type=int, default=1,
                        help='浏览器实例数量（默认：1）')
    parser.add_argument('--tabs-per-browser', type=int, default=1,
                        help='每个浏览器的标签页数量（默认：1）')
    parser.add_argument('--city', type=str, default='全国',
                        help='搜索城市（默认：全国）')
    parser.add_argument('--debug', action='store_true',
                        help='启用调试模式')
    return parser.parse_args()

# 主函数
async def main():
    """主函数"""
    try:
        # 使用环境变量或默认值
        headless = os.environ.get('HEADLESS', 'false').lower() == 'true'
        browser_count = int(os.environ.get('BROWSER_COUNT', '1'))
        tabs_per_browser = int(os.environ.get('TABS_PER_BROWSER', '1'))
        city = os.environ.get('CITY', '全国')
        
        # 设置调试模式
        debug_mode = os.environ.get('DEBUG_MODE', '0') == '1'
        if debug_mode:
            logger.setLevel(logging.DEBUG)
            logger.debug("调试模式已启用")
        
        logger.info(f"启动参数: 浏览器数量={browser_count}, 每个浏览器标签页数量={tabs_per_browser}, "
                   f"无头模式={headless}, 城市={city}")
        
        # 创建爬虫实例
        spider = BossSpider(
            headless=headless,
            browser_count=browser_count,
            tabs_per_browser=tabs_per_browser,
            city=city,
            resource_filter_level="low"
        )
        
        # 运行爬虫
        await spider.run()
        
    except Exception as e:
        logger.error(f"爬虫运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    

if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main()) 