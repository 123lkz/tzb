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
from bs4 import BeautifulSoup
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, UpdateOne
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from tqdm import tqdm
from captcha_recognizer.recognizer import Recognizer
# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.append(project_root)
# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    # 配置日志，第一个参数是日志器名称，第二个参数是爬虫名称
    logger = get_logger(__name__, "lagou_spider_step4")
except ImportError:
    # 配置基本日志，以防日志管理模块未安装
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

class LagouSpiderStep4:
    """拉勾网爬虫"""
    name = 'lagou_spider'
    
    def __init__(self, headless: bool = True, browser_count: int = 1):
        # 加载环境变量
        load_dotenv()
        
        self.base_url = "https://www.lagou.com"
        
        # MongoDB配置从环境变量读取
        self.mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
        self.mongo_db = "MOOC123_DA"
        self.collection_name = "lagou_job_raw_part1" #数据存储集合
        self.url_collection_name = f"lagou_step2_urls_202504_log_part1"  # 已经爬取URL记录集合
        self.lagou_urls_part = "lagou_step2_urls_part1"  # 需要爬取URL集合名称
        self.lagou_urls = None  # 初始化为None，在init_db中设置
        self.mongo_client = None
        self.db = None
        
        # URL缓存字典
        self.crawled_urls = {}
        
        if not all([self.mongo_uri, self.mongo_db, self.collection_name]):
            raise ValueError("MongoDB配置信息不完整，请检查环境变量")
        
        # 基础数据文件路径
        self.cookie_path = Path("recruitment_spider/data/lagou/lagou_cookie.json")
        logger.info(f"基础数据文件路径: {self.cookie_path.absolute()}")
        
        # 加载cookie配置
        self.cookies = self.load_cookies()
        
        # 上传者信息
        self.uploader = "单永旭"
        
        # Selenium配置
        self.headless = headless
        self.browser_count = browser_count
        self.driver = None
        self.wait = None    

    def load_cookies(self) -> Dict[str, str]:
        """加载cookie配置"""
        try:
            with open(self.cookie_path, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
                logger.info(f"成功加载cookie配置，共{len(cookies)}个账号")
                return cookies
        except Exception as e:
            logger.error(f"加载cookie配置失败: {e}")
            return {}

    async def init_db(self):
        """初始化数据库连接"""
        try:
            self.mongo_client = AsyncIOMotorClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            self.lagou_urls = self.db[self.lagou_urls_part]
            # 删除旧的索引
            try:
                await self.db[self.url_collection_name].drop_indexes()
            except:
                pass                        
            # 创建索引，使用复合索引确保唯一性
            await self.db[self.collection_name].create_index([("positionId", ASCENDING)], unique=True)
            # 使用复合索引替代单一的url索引
            # await self.db[self.url_collection_name].create_index([
            #     ("job_type_code", ASCENDING),
            #     ("job_type_name", ASCENDING),
            #     ("industry_name", ASCENDING),
            #     ("city_name", ASCENDING),
            #     ("city_code", ASCENDING),
            # ], unique=True)
            # 使用单一的url索引
            await self.db[self.url_collection_name].create_index([("url", ASCENDING)], unique=True)
            await self.db[self.url_collection_name].create_index([("crawl_time", ASCENDING)])
            
            # 加载已爬取的URL到缓存
            await self.load_crawled_urls()
            
            logger.info("MongoDB连接和索引初始化成功")
        except Exception as e:
            logger.error(f"MongoDB初始化失败: {e}")
            raise

    async def close_db(self):
        """关闭数据库连接"""
        if self.mongo_client:
            self.mongo_client.close()
            logger.info("MongoDB连接已关闭")

    async def is_url_crawled(self, job_type_code: str, job_type_name: str, city: str, industry: str) -> bool:
        """检查URL是否已经爬取过，只从内存缓存中检查"""
        url_key = f"{city}-{job_type_name}-{industry}"
        return url_key in self.crawled_urls
    
    async def mark_url_crawled(self, full_url: dict, status:bool,job_count:int,page:int, job_type_name:str,job_type_code:str,city_name:str,city_code:str,industry:str):
        
        """
        标记URL为已爬取，并根据状态存入不同的集合        
        """
        try:            
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 构造要保存的文档
            document = {
                'url':full_url,
                'city_name':city_name,
                'city_code':city_code,
                "job_type_code": job_type_code,
                "job_type_name": job_type_name,
                "industry_name": industry,
                "page": str(page),
                "job_count":job_count,
                "crawl_time": current_time,
                "status": status,
                "update_time": current_time
            }
            
            # 更新数据库中的进度记录
            url_collection = self.db[self.url_collection_name]
            try:
                result = await url_collection.update_one(
                    {
                        'city_name': city_name,
                        'city_code': city_code,
                        "job_type_code": job_type_code,
                        "job_type_name": job_type_name,
                        "industry_name": industry,
                    },
                    {
                        "$set": document,
                        "$setOnInsert": {"first_crawl_time": current_time}
                    },
                    upsert=True
                )
                
                # 记录操作结果
                if result.upserted_id:
                    logger.info(f"新增URL记录: {city_name}-{job_type_name}-{industry}, 状态: {status}")
                else:
                    logger.info(f"更新URL记录: {city_name}-{job_type_name}-{industry}, 状态: {status}")
            except Exception as e:
                logger.error(f"标记URL状态失败: {str(e)}")
                logger.error(f"URL文档: {full_url}")
                logger.error(f"状态: {status}")
            
        except Exception as e:
            logger.error(f"标记URL状态失败: {str(e)}")
            logger.error(f"URL文档: {full_url}")
            logger.error(f"状态: {status}")
            # 不抛出异常，让爬虫继续运行
            return

    async def load_crawled_urls(self):
        """
        从数据库一次性加载所有已爬取的URL到内存中
        包含爬取时间、职位数量和页码信息
        """
        try:
            url_collection = self.db[self.url_collection_name]
            cursor = url_collection.find(
                {},
                {
                    "_id": 0,
                    "city_name": 1,
                    "job_type_name": 1,
                    "industry_name": 1,                    
                }
            )
            
            self.crawled_urls.clear()
            async for doc in cursor:
                self.crawled_urls[f"{doc.get('city_name', '')}-{doc.get('job_type_name', '')}-{doc.get('industry_name', '')}"] = 1
            
            logger.info(f"已加载 {len(self.crawled_urls)} 个已爬取的URL到缓存")
        except Exception as e:
            logger.error(f"加载已爬取URL失败: {str(e)}")
            self.crawled_urls = {}

    def init_selenium(self):
        """初始化Selenium"""
        try:
            # 创建Chrome选项
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument('--headless')
            
            # 设置窗口大小为普通用户常用的尺寸
            chrome_options.add_argument('--window-size=1024,768')
            chrome_options.add_argument('--start-maximized')
            
            # 设置中文语言环境
            chrome_options.add_argument('--lang=zh-CN')
            
            # 添加一些常见的用户代理字符串
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            ]
            chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
            
            # 创建WebDriver
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 30)
            
            # 设置页面加载超时
            self.driver.set_page_load_timeout(30)
            self.driver.set_script_timeout(30)
            
            # 注入JavaScript代码来绕过检测
            self.driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
                Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en'] });
            """)
            
            logger.info("Selenium初始化成功")
            
            # 执行登录
            if not self.login():
                logger.error("登录失败")
                raise Exception("登录失败")
            
        except Exception as e:
            logger.error(f"Selenium初始化失败: {e}")
            raise

    def login(self) -> bool:
        """使用账号密码登录"""
        try:
            # 随机选择一个账号
            account = random.choice(list(self.cookies.keys()))
            password = self.cookies[account]
            logger.info(f"已随机选择账号 {account} 进行登录")
            
            # 访问登录页面
            self.driver.get("https://passport.lagou.com/login/login.html")
            # time.sleep(2)
            
            # 检查页面是否加载完成
            max_retries = 3
            for attempt in range(max_retries):
                if "登录" in self.driver.page_source:
                    break
                time.sleep(1)
                if attempt == max_retries - 1:
                    logger.error("登录页面加载失败")
                    return False
            
            # 切换到密码登录
            try:
                # 查找包含"密码登录"的元素并点击
                elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '密码登录')]")
                if elements:
                    elements[0].click()
                    time.sleep(1)
            except Exception as e:
                logger.warning(f"切换到密码登录失败: {e}")
            
            # 输入账号
            try:
                username_input = self.driver.find_element(By.NAME, "account")
                username_input.clear()
                username_input.send_keys(account)
                time.sleep(1)
            except Exception as e:
                logger.error(f"输入账号失败: {e}")
                return False
            
            # 输入密码
            try:
                password_input = self.driver.find_element(By.NAME, "password")
                password_input.clear()
                password_input.send_keys(password)
                time.sleep(1)
            except Exception as e:
                logger.error(f"输入密码失败: {e}")
                return False
            
            # 勾选协议
            try:
                # 查找协议复选框并点击
                agreement_checkbox = self.driver.find_element(By.CSS_SELECTOR, ".sc-furwcr.bVYGWy")
                agreement_checkbox.click()
                time.sleep(0.5)
            except Exception as e:
                logger.warning(f"勾选协议失败: {e}")
            
            # 点击登录按钮
            try:
                # 查找包含"登录"的按钮并点击
                # 使用更精确的CSS选择器查找登录按钮
                login_button = self.driver.find_element(By.CSS_SELECTOR, "button.ant-btn.ant-btn-primary")                
                login_button.click()
            except Exception as e:
                logger.error(f"点击登录按钮失败: {e}")
                return False
            
            # 等待登录完成
            time.sleep(2)
            if not self.retry_with_captcha():
                logger.error("验证码处理失败")
                return False                        
            
            # 检查登录状态
            if self.verify_login():
                logger.info("登录成功")
                return True
            else:
                logger.error("登录失败")
                return False
                
        except Exception as e:
            logger.error(f"登录过程出错: {e}")
            return False

    def verify_login(self) -> bool:
        """验证登录状态"""
        try:
            # 检查是否存在登录按钮或其他未登录标识
            login_button = self.driver.find_elements(By.CSS_SELECTOR, '.login, .btn-login, [data-lg-tj-id="1810"]')
            user_avatar = self.driver.find_elements(By.CSS_SELECTOR, '.user-avatar, .avatar, .user-head-img')
            unick = self.driver.find_elements(By.CSS_SELECTOR, '.unick, .user-name, .user-info')
            
            # 检查当前URL是否在登录页面
            is_login_page = 'login' in self.driver.current_url
            
            # 综合判断登录状态
            is_logged_in = (
                not login_button and
                (user_avatar or unick) and
                not is_login_page
            )
            
            if is_logged_in:
                logger.info("登录状态验证成功")
            else:
                logger.warning(f"登录状态验证失败，当前URL: {self.driver.current_url}")
            
            return is_logged_in
            
        except Exception as e:
            logger.error(f"验证登录状态失败: {e}")
            return False

    async def run(self):
        """运行爬虫"""
        try:
            # 初始化数据库
            await self.init_db()
            logger.info("数据库初始化完成")

            # 初始化Selenium
            self.init_selenium()
            logger.info("Selenium初始化完成")

            # 获取所有未爬取的URL
            all_docs = self.lagou_urls.find({},{'_id':0,'create_time':0})         
            total_pending = await self.lagou_urls.count_documents({})
            logger.info(f"实际需要爬取 {total_pending} 个URL组合")
            
            # 创建进度条，设置更详细的格式
            pbar = tqdm(
                total=total_pending,
                desc="爬取进度",
                unit="个",
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
            )

            # URL计数器
            url_counter = 0
            success_count = 0
            fail_count = 0

            async for url_doc in all_docs:
                job_type_code = url_doc.get('job_type_code', '')
                job_type_name = url_doc.get('job_type_name', '')
                city_name = url_doc.get('city_name', '')
                city_code = url_doc.get('city_code', '')
                industry = url_doc.get('industry_name', '')
                try:
                    current_task = f"{city_name}-{job_type_name}-{industry}"
                    pbar.set_postfix({
                        "当前任务": current_task,
                        "成功": success_count,
                        "失败": fail_count
                    })
                    
                    # 检查URL是否已经爬取过
                    if await self.is_url_crawled(job_type_code, job_type_name, city_name, industry):
                        logger.info(f"URL已爬取过，跳过: {current_task}")
                        pbar.update(1)
                        continue

                    url_counter += 1
                    # 每5个URL重启浏览器
                    if url_counter > 0 and url_counter % 7 == 0:
                        logger.info("已爬取7个URL，准备重启浏览器...")
                        self.driver.quit()
                        self.init_selenium()
                        logger.info("浏览器重启完成")

                    # 构建查询URL
                    base_url = "https://www.lagou.com/wn/jobs"
                    for page in range(1, 31):       
                        job_type_name_enc = job_type_name.replace("/", "%2F")
                        params = {
                            'pn': page,
                            'kd': job_type_name_enc,
                            'hy': industry,
                            'px': 'new',
                            'cl': 'false',
                            'fromSearch': 'true',
                            'labelWords': 'sug',
                            'city': city_name
                        }
                        query_string = urllib.parse.urlencode(params, safe='=')
                        full_url = f"{base_url}?{query_string}"
                        logger.info(f"正在爬取第{page}页: {full_url}")

                        # 访问目标页面
                        if not await self.handle_page_navigation(full_url):
                            logger.error(f"无法访问页面: {full_url}")
                            fail_count += 1
                            pbar.set_postfix({
                                "当前任务": current_task,
                                "成功": success_count,
                                "失败": fail_count
                            })
                            should_break = True
                            break
                        # 增加一些模拟真实用户的操作，比如滚动页面
                        try:
                            # 获取页面高度
                            page_height = self.driver.execute_script("return document.documentElement.scrollHeight")
                            logger.info(f"页面高度: {page_height}")
                            # 随机滚动几次
                            scroll_times = random.randint(1, 3)
                            for i in range(scroll_times):
                                # 随机滚动位置
                                scroll_position = random.randint(300, page_height - 200)
                                # logger.info(f"滚动到位置: {scroll_position}")
                                self.driver.execute_script(f"window.scrollTo(0, {scroll_position})")
                                time.sleep(random.uniform(1, 1.5))
                        # 增加一些模拟真实用户的操作，比如滚动页面  
                        except Exception as e:
                            logger.warning(f"模拟滚动页面时出错: {e}")

                        # 获取页面内容
                        page_source = self.driver.page_source
                        job_list = self.parse_job_list(page_source)
                        clean_job_list = []
                        should_break = False
                        for job in job_list:
                            if job.get('createTime') > '2025-01-01':
                                clean_job_list.append(job)
                            else:
                                should_break = True
                                break                        
                        
                        if clean_job_list:
                            save_success = await self.save_job_list(clean_job_list)
                            if save_success:
                                success_count += 1
                                await self.mark_url_crawled(full_url, True, len(clean_job_list), page, job_type_name, job_type_code, city_name, city_code, industry)
                                logger.info(f"第{page}页数据保存成功，职位数量：{len(clean_job_list)}")
                            else:
                                fail_count += 1
                                await self.mark_url_crawled(full_url, False, 0, page, job_type_name, job_type_code, city_name, city_code, industry)
                                logger.error(f"第{page}页数据保存失败")
                        else:
                            fail_count += 1
                            await self.mark_url_crawled(full_url, False, 0, page, job_type_name, job_type_code, city_name, city_code, industry)
                            logger.warning(f"页面 {full_url} 未解析到职位信息")
                            break
                        
                        if should_break:
                            break
                        if len(job_list) < 15:
                            break
                            
                    pbar.update(1)
                    pbar.set_postfix({
                        "当前任务": current_task,
                        "成功": success_count,
                        "失败": fail_count
                    })
                    
                except Exception as e:
                    logger.error(f"爬取页面失败: {str(e)}")
                    fail_count += 1
                    pbar.set_postfix({
                        "当前任务": current_task,
                        "成功": success_count,
                        "失败": fail_count
                    })
                    continue

            pbar.close()
            logger.info(f"爬取完成 - 总计: {total_pending}, 成功: {success_count}, 失败: {fail_count}")

        except Exception as e:
            logger.error(f"爬虫运行出错: {e}")
            raise
        finally:
            # 关闭Selenium资源
            if hasattr(self, 'driver'):
                self.driver.quit()
            await self.close_db()
            logger.info("爬虫运行结束，资源已清理")

    def parse_job_list(self, html_content: str) -> List[Dict]:
        """
        解析职位列表页面，包含所有拉勾网字段
        :param html_content: 页面HTML内容
        :return: 职位信息列表
        """
        try:
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 查找所有script标签
            script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
            position_result = None
            if script_tag:
                # 提取 JSON 字符串
                json_string = script_tag.string

                # 解析 JSON 数据
                data = json.loads(json_string)

                # 按路径访问 positionResult
                try:
                    position_result = data['props']['pageProps']['initData']['content']['positionResult']
                except KeyError as e:
                    logger.error(f"在 JSON 数据中找不到指定的键路径: {e}")
                    return []
                except TypeError as e:
                    logger.error(f"访问路径中的某个键对应的值不是字典类型: {e}")
                    return []

            else:
                logger.error("未找到 <script id='__NEXT_DATA__'> 标签")
                return []
                        
            if not position_result:
                logger.error("未找到职位数据")
                return []
            
            # 获取职位列表
            position_list = position_result.get('result', [])
            jobs = []
            for position in position_list:
                job = {
                    # 基本信息
                    'positionId': position.get('positionId'),  # 职位ID
                    'positionName': position.get('positionName'),  # 职位名称
                    'positionType': position.get('positionType'),  # 职位类型
                    'positionStatus': position.get('positionStatus'),  # 职位状态
                    'positionDesc': position.get('positionDesc'),  # 职位描述
                    'positionDetail': position.get('positionDetail'),  # 职位详情
                    'positionAddress': position.get('positionAddress'),  # 工作地址
                    'positionAdvantage': position.get('positionAdvantage'),  # 职位诱惑
                    'positionHighlight': position.get('positionHighlight'),  # 职位亮点
                    'positionLables': position.get('positionLables', []),  # 职位标签
                    'positionRequirements': position.get('positionRequirements'),  # 职位要求
                    'positionUrl': position.get('positionUrl'),  # 职位链接
                    'positionSourceType': position.get('positionSourceType'),  # 职位来源类型
                    'positionSourceId': position.get('positionSourceId'),  # 职位来源ID
                    'positionSourceUrl': position.get('positionSourceUrl'),  # 职位来源链接
                    'positionFirstType': position.get('firstType'),  # 一级职位类型
                    'positionSecondType': position.get('secondType'),  # 二级职位类型
                    'positionThirdType': position.get('thirdType'),  # 三级职位类型
                    'positionCategory': position.get('positionCategory'),  # 职位类别
                    
                    # 公司信息
                    'companyId': position.get('companyId'),  # 公司ID
                    'companyFullName': position.get('companyFullName'),  # 公司全称
                    'companyShortName': position.get('companyShortName'),  # 公司简称
                    'companyLogo': position.get('companyLogo'),  # 公司logo
                    'companySize': position.get('companySize'),  # 公司规模
                    'companyStatus': position.get('companyStatus'),  # 公司状态
                    'companyUrl': position.get('companyUrl'),  # 公司主页
                    'companyFeatures': position.get('companyFeatures'),  # 公司特色
                    'companyIntroduce': position.get('companyIntroduce'),  # 公司介绍
                    'companyRemark': position.get('companyRemark'),  # 公司备注
                    'companyStage': position.get('financeStage'),  # 融资阶段
                    'companyIndustry': position.get('industryField'),  # 所属行业
                    'companyZone': position.get('companyZone'),  # 公司所在区域
                    'companyAddress': position.get('companyAddress'),  # 公司地址
                    'companyLabelList': position.get('companyLabelList', []),  # 公司标签
                    
                    # 工作要求
                    'workYear': position.get('workYear'),  # 工作年限要求
                    'education': position.get('education'),  # 学历要求
                    'jobNature': position.get('jobNature'),  # 工作性质
                    'salary': position.get('salary'),  # 薪资范围
                    'salaryMonth': position.get('salaryMonth'),  # 薪资月数
                    'salaryMin': position.get('salaryMin'),  # 最低薪资
                    'salaryMax': position.get('salaryMax'),  # 最高薪资
                    'salaryType': position.get('salaryType'),  # 薪资类型
                    'salaryTips': position.get('salaryTips'),  # 薪资说明
                    
                    # 技能要求
                    'skillLables': position.get('skillLables', []),  # 技能标签
                    'skillDesc': position.get('skillDesc'),  # 技能描述
                    'requireSkills': position.get('requireSkills', []),  # 要求技能
                    'requireYears': position.get('requireYears'),  # 要求年限
                    'requireDesc': position.get('requireDesc'),  # 要求描述
                    
                    # 地理信息
                    'city': position.get('city'),  # 城市
                    'district': position.get('district'),  # 区域
                    'businessZones': position.get('businessZones', []),  # 商圈
                    'locationPlaces': position.get('locationPlaces', []),  # 地标
                    'longitude': position.get('longitude'),  # 经度
                    'latitude': position.get('latitude'),  # 纬度
                    'stationname': position.get('stationname'),  # 地铁站
                    'subwayline': position.get('subwayline'),  # 地铁线路
                    'linestaion': position.get('linestaion'),  # 地铁线路站点
                    'distance': position.get('distance'),  # 距离
                    'mapInfo': position.get('mapInfo'),  # 地图信息
                    
                    # 行业信息
                    'industryLables': position.get('industryLables', []),  # 行业标签
                    'industryField': position.get('industryField'),  # 行业领域
                    'industryCategory': position.get('industryCategory'),  # 行业类别
                    'industryDescription': position.get('industryDescription'),  # 行业描述
                    
                    # 时间相关
                    'createTime': position.get('createTime'),  # 创建时间
                    'formatCreateTime': position.get('formatCreateTime'),  # 格式化创建时间
                    'updateTime': position.get('updateTime'),  # 更新时间
                    'formatUpdateTime': position.get('formatUpdateTime'),  # 格式化更新时间
                    'lastLogin': position.get('lastLogin'),  # 最后登录时间
                    'refreshTime': position.get('refreshTime'),  # 刷新时间
                    'showTime': position.get('showTime'),  # 显示时间
                    'deadline': position.get('deadline'),  # 截止时间
                    
                    # 发布者信息
                    'publisherId': position.get('publisherId'),  # 发布者ID
                    'publisherName': position.get('publisherName'),  # 发布者姓名
                    'publisherPosition': position.get('publisherPosition'),  # 发布者职位
                    'publisherAvatar': position.get('publisherAvatar'),  # 发布者头像
                    'publisherIntroduce': position.get('publisherIntroduce'),  # 发布者介绍
                    
                    # 统计信息
                    'resumeProcessRate': position.get('resumeProcessRate'),  # 简历处理率
                    'resumeProcessDay': position.get('resumeProcessDay'),  # 简历处理天数
                    'score': position.get('score'),  # 职位分数
                    'countView': position.get('countView'),  # 浏览次数
                    'countResume': position.get('countResume'),  # 简历投递数
                    'countProcessed': position.get('countProcessed'),  # 已处理简历数
                    'countProcessing': position.get('countProcessing'),  # 处理中简历数
                    'countInterview': position.get('countInterview'),  # 面试数
                    'countOffer': position.get('countOffer'),  # offer数
                    'countHire': position.get('countHire'),  # 入职数
                    
                    # 状态信息
                    'approve': position.get('approve'),  # 审核状态
                    'status': position.get('status'),  # 职位状态
                    'isEnable': position.get('isEnable'),  # 是否启用
                    'isHot': position.get('isHot'),  # 是否热门
                    'isNew': position.get('isNew'),  # 是否新发布
                    'isUrgent': position.get('isUrgent'),  # 是否急聘
                    'isRecommend': position.get('isRecommend'),  # 是否推荐
                    'isSchoolJob': position.get('isSchoolJob'),  # 是否校招
                    'isInternship': position.get('isInternship'),  # 是否实习
                    'isOverSea': position.get('isOverSea'),  # 是否海外
                    
                    # 爬虫相关信息
                    'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 爬取时间
                    'source': 'lagou',  # 来源
                    'uploader': self.uploader  # 上传者
                }
                jobs.append(job)
            
            logger.info(f"成功解析到 {len(jobs)} 个职位信息")
            return jobs
            
        except Exception as e:
            logger.error(f"解析职位列表失败: {e}")
            return []

    def handle_captcha(self) -> bool:
        """处理验证码"""
        try:
            # 等待验证码元素出现
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "geetest_captcha"))
            )
            # 检查验证码类型
            retry_count = 0
            max_retry = 999
            while retry_count < max_retry:
                if "geetest_slider" in self.driver.page_source:
                    return self.handle_slider_captcha()
                else:
                    logger.warning("不是滑块认证，尝试点击左上角(50,50)并重新点击登录按钮")
                    webdriver.ActionChains(self.driver).move_by_offset(50, 50).click().perform()
                    time.sleep(0.5)
                    # 点击登录按钮
                    try:
                        login_button = self.driver.find_element(By.CSS_SELECTOR, "button.ant-btn.ant-btn-primary")
                        login_button.click()
                        time.sleep(1)
                    except Exception as e:
                        logger.error(f"点击登录按钮失败: {e}")
                    retry_count += 1
            logger.error("未知的验证码类型，重试多次后仍未出现滑块认证")
            return False
                
        except Exception as e:
            logger.error(f"验证码处理失败: {e}")
            return False

    def handle_slider_captcha(self) -> bool:
        """处理滑块验证码"""
        max_retries = 10
        for attempt in range(max_retries):
            try:
                # 等待验证码完全加载
                time.sleep(2)
                
                # 创建保存目录
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_dir = os.path.join("captcha_images", 'lagou')
                os.makedirs(save_dir, exist_ok=True)
                # 优化：只对可见的.geetest_window截图
                window_elements = self.driver.find_elements(By.CLASS_NAME, "geetest_window")
                window_elem = None
                for elem in window_elements:
                    size = elem.size
                    if size['width'] > 0 and size['height'] > 0 and elem.is_displayed():
                        window_elem = elem
                        break
                if not window_elem:
                    logger.error("未找到可见的.geetest_window区域，所有高度都为0")
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                    return False
                logger.info(f"选中的.geetest_window尺寸: width={window_elem.size['width']}, height={window_elem.size['height']}")
                window_png = window_elem.screenshot_as_png
                with open(os.path.join(save_dir, "window.png"), "wb") as f:
                    f.write(window_png)
                
                # 1. 调用识别器识别window.png缺口坐标
                recognizer = Recognizer()
                box, confidence = recognizer.identify_gap(source=os.path.join(save_dir, 'window.png'), verbose=False)
                if not box or not isinstance(box, (list, tuple)) or len(box) < 1:
                    logger.error(f'识别缺口失败，box结果异常: {box}，将删除本次截图并重试')
                    # 删除本次截图
                    try:
                        window_path = os.path.join(save_dir, "window.png")
                        if os.path.exists(window_path):
                            os.remove(window_path)
                            logger.info(f"已删除识别失败的验证码截图: {window_path}")
                    except Exception as e:
                        logger.warning(f"删除验证码截图失败: {e}")
                    # 点击(50,50)并点击登录按钮，重新进入滑块认证流程
                    # webdriver.ActionChains(self.driver).move_by_offset(50, 50).click().perform()
                    # time.sleep(0.5)
                    try:
                        # 使用更可靠的选择器查找刷新按钮
                        refresh_button = None
                        refresh_selectors = [
                            (By.CSS_SELECTOR, "[class^='geetest_refresh']"),  # 以geetest_refresh开头的class
                            (By.CSS_SELECTOR, "button[class*='geetest_refresh']"),  # 包含geetest_refresh的class
                            (By.CSS_SELECTOR, "button[aria-label='刷新验证']")  # 使用aria-label属性
                        ]
                        
                        for by, selector in refresh_selectors:
                            elements = self.driver.find_elements(by, selector)
                            for elem in elements:
                                if elem.is_displayed() and elem.size['width'] > 0:
                                    refresh_button = elem
                                    break
                            if refresh_button:
                                break
                        
                        if refresh_button:
                            refresh_button.click()
                            logger.info("成功点击刷新验证按钮")
                            time.sleep(1)
                        else:
                            logger.error("未找到刷新验证按钮")
                    except Exception as e:
                        logger.error(f"点击登录按钮失败: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                    return False
                logger.info(f'识别到缺口坐标: {box}, 可信度: {confidence}')
                gap_x = box[0]  # 缺口左上角x坐标

                # 2. 获取滑块按钮元素和初始位置
                try:
                    # 使用更可靠的选择器组合
                    slider_elem = None
                    selectors = [
                        (By.CSS_SELECTOR, "[class^='geetest_btn']"),  # 以geetest_btn开头的class
                        (By.CSS_SELECTOR, ".geetest_slider_button"),   # 另一种可能的class
                        (By.CSS_SELECTOR, "div[class*='geetest_btn']") # 包含geetest_btn的class
                    ]
                    
                    for by, selector in selectors:
                        elements = self.driver.find_elements(by, selector)
                        for elem in elements:
                            if elem.is_displayed() and elem.size['width'] > 0 and elem.size['height'] > 0:
                                slider_elem = elem
                                break
                        if slider_elem:
                            break
                    
                    if not slider_elem:
                        logger.error("未找到可用的滑块按钮")
                        return False
                        
                    logger.info(f"成功找到滑块按钮，大小: {slider_elem.size}")
                except Exception as e:
                    logger.error(f"查找滑块按钮失败: {e}")
                    return False

                # 3. 计算需要移动的距离（window.png截图区域的左上角为原点，需考虑偏移）
                window_location = window_elem.location
                move_distance = gap_x - (slider_elem.location['x'] - window_location['x'])
                logger.info(f'滑块初始x: {slider_elem.location['x']}, window原点x: {window_location['x']}, 需要移动距离: {move_distance}')

                # 4. 滑动
                action_chains = webdriver.ActionChains(self.driver)
                action_chains.move_to_element(slider_elem).perform()
                time.sleep(0.5)
                action_chains.click_and_hold(slider_elem).perform()
                time.sleep(0.5)
                # 模拟人类滑动轨迹
                track = self.get_track(move_distance-13)
                for x in track:
                    action_chains.move_by_offset(xoffset=x, yoffset=0).perform()
                    time.sleep(random.uniform(0.01, 0.05))
                action_chains.release().perform()
                
                # 等待页面跳转完成
                try:
                    # 等待页面URL发生变化或者特定元素出现/消失
                    current_url = self.driver.current_url
                    WebDriverWait(self.driver, 30).until(
                        lambda driver: driver.current_url != current_url or
                        not driver.find_elements(By.CLASS_NAME, "geetest_window")  # 验证码窗口消失
                    )
                    logger.info("验证码验证完成，页面已跳转")
                    # 把保存的截图删除就可以了
                    try:
                        window_path = os.path.join(save_dir, "window.png")
                        if os.path.exists(window_path):
                            os.remove(window_path)
                            logger.info(f"已删除验证码截图: {window_path}")
                    except Exception as e:
                        logger.warning(f"删除验证码截图失败: {e}")
                    
                    return self.check_captcha_result()
                except TimeoutException:
                    logger.error("等待页面跳转超时")
                    return False
                
            except Exception as e:
                logger.error(f"滑块验证码处理失败 (尝试 {attempt + 1}/{max_retries}): {e}")                                
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return False
        
        return False    

    def check_captcha_result(self) -> bool:
        """检查验证码结果"""
        try:
            if "请拖动滑块完成拼图" in self.driver.page_source:
                logger.info("验证码验证失败")
                return False
            else:
                logger.warning("验证码验证成功")
                return True
        except Exception as e:
            logger.error(f"检查验证码结果失败: {e}")
            return False

    def get_track(self, distance) -> list:
        """生成滑动轨迹"""
        """生成滑动轨迹"""
        # 减少轨迹点数，直接计算几个关键点
        track = []
        # 初始加速
        track.append(int(distance * 0.3))
        # 匀速
        track.append(int(distance * 0.4))
        # 减速
        track.append(int(distance * 0.3))
        return track
        # try:
        #     # 初始位置
        #     current = 0
        #     # 减速阈值（根据距离动态调整）
        #     mid = distance * random.uniform(0.4, 0.6)  # 增加减速点的位置
        #     # 轨迹列表
        #     track = []
        #     # 当前位移
        #     t = 0.2
        #     # 初速度
        #     v = 0
            
        #     while current < distance:
        #         if current < mid:
        #             # 加速度为正，根据距离调整加速度
        #             a = random.uniform(5, 7) * (distance / 100)  # 根据距离调整加速度
        #         else:
        #             # 加速度为负，根据距离调整减速度
        #             a = -random.uniform(2, 3) * (distance / 100)  # 根据距离调整减速度
                
        #         # 初速度v0
        #         v0 = v
        #         # 当前速度v = v0 + at
        #         v = v0 + a * t
        #         # 移动距离x = v0t + 1/2 * a * t^2
        #         move = v0 * t + 1 / 2 * a * t * t
        #         # 当前位移
        #         current += move
        #         # 加入轨迹
        #         track.append(round(move))
            
        #     # 对超出范围的位置进行修正
        #     while sum(track) > distance:
        #         if not track:
        #             logger.error("轨迹列表为空，无法修正")
        #             return []
        #         track.pop()
            
        #     # 如果总位移小于distance，则补足
        #     if sum(track) < distance:
        #         track.append(distance - sum(track))
            
        #     logger.info(f"生成的滑动轨迹: {track}, 总距离: {sum(track)}")
        #     return track
            
        # except Exception as e:
        #     logger.error(f"生成滑动轨迹失败: {e}")
        #     return []

    def retry_with_captcha(self, max_retries=3) -> bool:
        """处理验证码的重试机制"""
        for attempt in range(max_retries):
            try:
                if self.handle_captcha():
                    return True
                else:
                    logger.warning(f"验证码处理失败，正在进行第{attempt + 1}次重试")
                    time.sleep(random.uniform(2, 4))
            except Exception as e:
                logger.error(f"第{attempt + 1}次处理验证码时出错: {e}")
        
        logger.error(f"验证码处理失败，已达到最大重试次数{max_retries}")
        return False

    async def handle_page_navigation(self, url: str, max_retries: int = 3) -> bool:
        """处理页面导航"""
        for attempt in range(max_retries):
            try:
                self.driver.get(url)
                return True
                
            except Exception as e:
                logger.error(f"访问页面失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(2, 4))
                    continue
                return False
        
        return False

    async def save_job_list(self, job_list: list) -> bool:
        """
        批量保存职位信息到MongoDB
        :param job_list: 职位信息列表
        :return: 是否保存成功
        """
        try:
            if not job_list:
                logger.warning("职位列表为空，无需保存")
                return False

            # 构建批量更新操作
            operations = []
            for job in job_list:
                position_id = job.get('positionId')
                if not position_id:
                    logger.warning(f"职位信息缺少positionId，跳过保存: {job.get('positionName', 'unknown')}")
                    continue

                processed_job = job.copy()
                processed_job['updateTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                operations.append(
                    UpdateOne(
                        {'positionId': position_id},
                        {'$set': processed_job},
                        upsert=True
                    )
                )

            if operations:
                result = await self.db[self.collection_name].bulk_write(operations)
                logger.info(
                    f"职位信息保存成功 - 匹配数: {result.matched_count}, "
                    f"修改数: {result.modified_count}, "
                    f"插入数: {result.upserted_count}, "
                    f"总数: {len(operations)}"
                )
                return True
            else:
                logger.warning("没有有效的职位信息需要保存")
                return False

        except Exception as e:
            logger.error(f"保存职位信息失败: {str(e)}")
            return False

async def main():
    """主函数"""
    try:        
        # 创建爬虫实例
        spider = LagouSpiderStep4(headless=False)
        
        # 运行爬虫
        await spider.run()
        
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        # 确保资源被正确释放
        try:
            await spider.close_db()
        except Exception as e:
            logger.error(f"清理资源时出错: {str(e)}")

if __name__ == "__main__":
    # 运行异步主函数
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序异常退出: {str(e)}")
        import traceback
        logger.error(traceback.format_exc()) 