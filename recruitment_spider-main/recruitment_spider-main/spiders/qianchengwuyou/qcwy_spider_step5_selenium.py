#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
前程无忧 Step5 爬虫 - Selenium版本
用于爬取前程无忧职位详情数据
"""

import json
import time
import random
import string
import traceback
from datetime import datetime
from typing import Dict, List, Optional
import platform
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo import UpdateOne
import logging
import urllib.parse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'qcwy_spider_step5_selenium_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class QCWYSpiderStep5Selenium:
    def __init__(self):
        # MongoDB配置
        self.mongo_client = MongoClient("mongodb://da_test:3g398GJIaaV43gEW@210.14.140.50:10387/da_test")
        self.db = self.mongo_client["da_test"]
        self.source_collection = self.db["qcwy_step2_urls_part1"]  # 源数据集合
        self.target_collection = self.db["qcwy_step2_job_raw_part1"]  # 目标集合（职位数据）
        self.log_collection = self.db["qcwy_step2_urls_202505_log_part1"]  # 日志集合
        
        # 初始化已爬取URL集合
        self.crawled_urls = {}
        self.load_crawled_urls()
        
        # Selenium配置
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        
        # 爬取配置
        self.delay_range = (3, 6)  # 随机延迟范围（秒）
        self.max_retries = 3  # 最大重试次数
        self.timeout = 30  # 页面加载超时时间（秒）
        
        # 反爬虫配置
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        # 统计信息
        self.job_results = []  # 全局队列，存储监听到的job数据
        self._current_page_num = None  # 当前监听的页码
        
        # 高级反爬虫配置
        self.screen_resolutions = [
            {'width': 1920, 'height': 1080},
            {'width': 1366, 'height': 768},
            {'width': 1440, 'height': 900},
            {'width': 1536, 'height': 864},
            {'width': 1280, 'height': 720},
            {'width': 1600, 'height': 900},
        ]
        
        self.color_depths = [24, 32]
        self.platforms = ['Win32', 'MacIntel', 'Linux x86_64']
        self.languages = ['zh-CN,zh;q=0.9,en;q=0.8', 'en-US,en;q=0.9', 'zh-CN,zh;q=0.8,en;q=0.6']
        self.timezones = ['Asia/Shanghai', 'Asia/Hong_Kong', 'Asia/Tokyo', 'America/New_York']
        
        # 网络配置
        self.network_conditions = [
            {'offline': False, 'latency': 20, 'download_throughput': 1024 * 1024, 'upload_throughput': 512 * 1024},
            {'offline': False, 'latency': 50, 'download_throughput': 512 * 1024, 'upload_throughput': 256 * 1024},
            {'offline': False, 'latency': 100, 'download_throughput': 256 * 1024, 'upload_throughput': 128 * 1024},
        ]
        
        # 代理配置（可选）
        self.proxy_list = [
            # 示例代理，实际使用时需要替换为真实代理
            # {'server': 'http://proxy1:port', 'username': 'user1', 'password': 'pass1'},
            # {'server': 'http://proxy2:port', 'username': 'user2', 'password': 'pass2'},
        ]
        self.current_proxy_index = 0
        
        # 会话管理
        self.request_count = 0
        self.max_requests_per_session = 100  # 每个会话最大请求数
        self.url_count = 0  # URL计数器
        self.max_urls_per_session = 20  # 每个会话最大URL数量

    def load_crawled_urls(self):
        """加载已爬取的URL"""
        try:
            logger.info("加载已爬取的URL列表...")
            cursor = self.log_collection.find({}, {"source_url": 1, "_id": 0})
            for doc in cursor:
                if doc.get("source_url"):
                    self.crawled_urls[doc.get("source_url")] = 1
            logger.info(f"已加载 {len(self.crawled_urls)} 个已爬取URL")
        except Exception as e:
            logger.error(f"加载已爬取URL失败: {str(e)}")
            self.crawled_urls = {}

    def get_random_user_agent(self) -> str:
        """获取随机User-Agent"""
        return random.choice(self.user_agents)

    def get_random_viewport(self):
        viewports = [
            {'width': 1024, 'height': 768},
            {'width': 1280, 'height': 720},
            {'width': 1366, 'height': 768},
            {'width': 1440, 'height': 900},
            {'width': 1536, 'height': 864},
        ]
        return random.choice(viewports)

    def get_random_locale(self):
        return random.choice(['zh-CN', 'zh', 'en-US'])

    def get_random_timezone(self):
        return random.choice(['Asia/Shanghai', 'Asia/Hong_Kong'])

    def get_random_screen_resolution(self):
        """获取随机屏幕分辨率"""
        return random.choice(self.screen_resolutions)
    
    def get_random_color_depth(self):
        """获取随机颜色深度"""
        return random.choice(self.color_depths)
    
    def get_random_platform(self):
        """获取随机平台"""
        return random.choice(self.platforms)
    
    def get_random_language(self):
        """获取随机语言设置"""
        return random.choice(self.languages)
    
    def get_random_timezone_id(self):
        """获取随机时区"""
        return random.choice(self.timezones)
    
    def get_random_network_condition(self):
        """获取随机网络条件"""
        return random.choice(self.network_conditions)
    
    def generate_random_fingerprint(self):
        """生成随机浏览器指纹"""
        return {
            'screen_resolution': self.get_random_screen_resolution(),
            'color_depth': self.get_random_color_depth(),
            'platform': self.get_random_platform(),
            'language': self.get_random_language(),
            'timezone': self.get_random_timezone_id(),
            'network': self.get_random_network_condition(),
        }

    def init_browser(self):
        """初始化浏览器"""
        try:
            # 生成随机浏览器指纹
            fingerprint = self.generate_random_fingerprint()
            viewport = fingerprint['screen_resolution']
            user_agent = self.get_random_user_agent()
            
            # 创建Chrome选项
            chrome_options = Options()
            
            # 启用性能日志
            chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
            
            # 基础配置
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins-discovery')
            chrome_options.add_argument('--disable-background-networking')
            chrome_options.add_argument('--disable-default-apps')
            chrome_options.add_argument('--disable-sync')
            chrome_options.add_argument('--disable-translate')
            chrome_options.add_argument('--hide-scrollbars')
            chrome_options.add_argument('--mute-audio')
            chrome_options.add_argument('--no-default-browser-check')
            chrome_options.add_argument('--no-pings')
            chrome_options.add_argument('--disable-field-trial-config')
            chrome_options.add_argument('--disable-ipc-flooding-protection')
            chrome_options.add_argument('--disable-background-timer-throttling')
            chrome_options.add_argument('--disable-backgrounding-occluded-windows')
            chrome_options.add_argument('--disable-renderer-backgrounding')
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            chrome_options.add_argument('--disable-histogram-customizer')
            chrome_options.add_argument('--disable-gl-extensions')
            chrome_options.add_argument('--disable-composited-antialiasing')
            chrome_options.add_argument('--disable-canvas-aa')
            chrome_options.add_argument('--disable-3d-apis')
            chrome_options.add_argument('--disable-accelerated-layers')
            chrome_options.add_argument('--disable-accelerated-plugins')
            chrome_options.add_argument('--disable-accelerated-video')
            chrome_options.add_argument('--disable-accelerated-2d-canvas')
            chrome_options.add_argument('--disable-accelerated-video-decode')
            chrome_options.add_argument('--disable-gpu-sandbox')
            chrome_options.add_argument('--disable-software-rasterizer')
            
            # 修复警告的配置
            chrome_options.add_argument('--disable-logging')
            chrome_options.add_argument('--disable-gpu-logging')
            chrome_options.add_argument('--disable-logging-redirect')
            chrome_options.add_argument('--log-level=3')  # 只显示致命错误
            chrome_options.add_argument('--silent')
            chrome_options.add_argument('--disable-google-apis')
            chrome_options.add_argument('--disable-gcm')
            chrome_options.add_argument('--disable-voice-transcription')
            
            # 设置实验性标志
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # 设置User-Agent
            chrome_options.add_argument(f'--user-agent={user_agent}')
            
            # 设置窗口大小
            chrome_options.add_argument(f'--window-size={viewport["width"]},{viewport["height"]}')
            
            # 设置语言
            chrome_options.add_argument('--lang=zh-CN')
            
            # 获取代理配置
            proxy = self.get_next_proxy()
            if proxy:
                chrome_options.add_argument(f'--proxy-server={proxy["server"]}')
                logger.info(f"使用代理: {proxy['server']}")
            
            # 创建WebDriver
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # 设置窗口大小
            self.driver.set_window_size(viewport['width'], viewport['height'])
            
            # 创建WebDriverWait
            self.wait = WebDriverWait(self.driver, self.timeout)
            
            # 设置cookie
            # cookies = self.get_cookies()
            # for cookie in cookies:
            #     self.driver.add_cookie(cookie)
            # logger.info(f"已设置 {len(cookies)} 个cookie")
            
            # 执行反爬虫脚本
            self.execute_anti_detection_script()
            
            # 设置XHR监听器
            self.setup_xhr_listener()
            
            logger.info(f"浏览器初始化成功 - User-Agent: {user_agent}, Viewport: {viewport}")
            
        except Exception as e:
            logger.error(f"浏览器初始化失败: {str(e)}\n{traceback.format_exc()}")
            # 确保清理资源
            self.close_browser()
            raise

    def execute_anti_detection_script(self):
        """执行反爬虫检测脚本"""
        try:
            fingerprint = self.generate_random_fingerprint()
            
            anti_detection_script = f"""
                // 基础反爬虫伪装
                Object.defineProperty(navigator, 'webdriver', {{
                    get: () => undefined,
                }});
                
                // 插件伪装
                Object.defineProperty(navigator, 'plugins', {{
                    get: () => [
                        {{
                            name: 'Chrome PDF Plugin',
                            filename: 'internal-pdf-viewer',
                            description: 'Portable Document Format',
                            length: 1
                        }},
                        {{
                            name: 'Chrome PDF Viewer',
                            filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai',
                            description: '',
                            length: 1
                        }},
                        {{
                            name: 'Native Client',
                            filename: 'internal-nacl-plugin',
                            description: 'Native Client Executable',
                            length: 1
                        }}
                    ],
                }});
                
                // 语言设置
                Object.defineProperty(navigator, 'languages', {{
                    get: () => ['{fingerprint["language"].split(",")[0]}', 'zh', 'en'],
                }});
                
                // 平台伪装
                Object.defineProperty(navigator, 'platform', {{
                    get: () => '{fingerprint["platform"]}',
                }});
                
                // 屏幕信息伪装
                Object.defineProperty(screen, 'colorDepth', {{
                    get: () => {fingerprint["color_depth"]},
                }});
                
                // Chrome对象伪装
                window.chrome = {{
                    runtime: {{}},
                    loadTimes: function() {{}},
                    csi: function() {{}},
                    app: {{}}
                }};
                
                // 时间戳随机化
                const originalGetTime = Date.prototype.getTime;
                Date.prototype.getTime = function() {{
                    return originalGetTime.call(this) + Math.floor(Math.random() * 100);
                }};
                
                // 禁用WebDriver检测
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                
                // 伪装WebGL
                const getParameter = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                    if (parameter === 37445) {{
                        return 'Intel Inc.';
                    }}
                    if (parameter === 37446) {{
                        return 'Intel(R) Iris(TM) Graphics 6100';
                    }}
                    return getParameter.call(this, parameter);
                }};
                
                // 伪装Canvas指纹
                const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
                HTMLCanvasElement.prototype.toDataURL = function(type) {{
                    if (type === 'image/png') {{
                        const canvas = this;
                        const ctx = canvas.getContext('2d');
                        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                        const data = imageData.data;
                        // 添加微小噪声
                        for (let i = 0; i < data.length; i += 4) {{
                            data[i] = data[i] + Math.floor(Math.random() * 2) - 1;
                            data[i + 1] = data[i + 1] + Math.floor(Math.random() * 2) - 1;
                            data[i + 2] = data[i + 2] + Math.floor(Math.random() * 2) - 1;
                        }}
                        ctx.putImageData(imageData, 0, 0);
                    }}
                    return originalToDataURL.call(this, type);
                }};
            """
            
            self.driver.execute_script(anti_detection_script)
            logger.info("反爬虫脚本执行成功")
            
        except Exception as e:
            logger.warning(f"反爬虫脚本执行失败: {str(e)}")

    def simulate_human_behavior(self):
        """模拟人类行为 - 简单滚动"""
        try:
            # 检查页面是否已初始化
            if not self.driver:
                logger.debug("浏览器未初始化，跳过模拟人类行为")
                return
            
            # 随机滚动2-4次
            scroll_count = random.randint(2, 4)
            for i in range(scroll_count):
                # 随机滚动距离
                scroll_y = random.randint(300, 600)
                
                # 使用JavaScript滚动，安全可靠
                self.driver.execute_script(f"window.scrollBy(0, {scroll_y});")
                
                # 随机暂停，模拟阅读
                time.sleep(random.uniform(1.0, 2.5))
                
                logger.debug(f"第{i+1}次滚动完成")
            
            logger.debug("模拟人类行为完成")
            
        except Exception as e:
            logger.debug(f"模拟人类行为失败: {str(e)}")

    def check_if_blocked(self) -> bool:
        """检查是否被封禁"""
        try:
            page_source = self.driver.page_source
            
            if "为保证您的正常访问,请进行如下验证" in page_source:                                  
                logger.warning("检测到验证码，重启浏览器...")
                current_url = self.driver.current_url  # 保存当前URL
                self.restart_browser()
                # 重新访问页面
                self.driver.get(current_url)
                self.random_delay()
                return False  # 重启后继续处理                
            
            # 检查页面是否正常加载
            # if len(page_source) < 1000:  # 页面内容过少
            #     logger.warning("页面内容过少，可能被封禁")
            #     return True
                
            return False
            
        except Exception as e:
            logger.error(f"检查封禁状态失败: {str(e)}")
            return True

    def restart_browser(self):
        """重启浏览器"""
        logger.info("正在重启浏览器...")
        self.close_browser()
        time.sleep(2)  # 等待一下
        self.init_browser()
        logger.info("浏览器重启完成")

    def random_delay(self):
        """随机延迟"""
        delay = random.uniform(*self.delay_range)
        time.sleep(delay)

    def smart_delay(self, page_type="normal"):
        """
        智能延迟策略
        :param page_type: 页面类型 ("normal", "search", "detail", "pagination")
        """
        try:
            if page_type == "search":
                # 搜索页面延迟较长，模拟思考时间
                base_delay = random.uniform(1, 3)
            elif page_type == "detail":
                # 详情页面延迟中等，模拟阅读时间
                base_delay = random.uniform(1, 3)
            elif page_type == "pagination":
                # 分页延迟较短，模拟快速浏览
                base_delay = random.uniform(1, 3)
            else:
                # 普通页面延迟
                base_delay = random.uniform(*self.delay_range)
            
            # 添加随机波动
            variation = random.uniform(-0.5, 0.5)
            final_delay = max(0.5, base_delay + variation)
            
            # 偶尔添加较长延迟，模拟人类行为
            if random.random() < 0.1:  # 10%概率
                final_delay += random.uniform(2, 5)
            
            logger.debug(f"智能延迟: {final_delay:.2f}秒 (类型: {page_type})")
            time.sleep(final_delay)
            
        except Exception as e:
            logger.warning(f"智能延迟失败，使用默认延迟: {str(e)}")
            self.random_delay()

    def check_request_frequency(self):
        """检查请求频率，避免过于频繁"""
        current_time = time.time()
        if hasattr(self, '_last_request_time'):
            time_diff = current_time - self._last_request_time
            if time_diff < 1.0:  # 如果距离上次请求不到1秒
                wait_time = 1.0 - time_diff
                time.sleep(wait_time)
        
        self._last_request_time = current_time

    def get_next_proxy(self):
        """获取下一个代理"""
        if not self.proxy_list:
            return None
        
        proxy = self.proxy_list[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_list)
        return proxy

    def should_rotate_session(self):
        """判断是否需要轮换会话"""
        # 只基于URL数量判断，不再考虑时间
        return self.url_count >= self.max_urls_per_session

    def rotate_session(self):
        """轮换会话"""
        logger.info("开始轮换会话...")
        self.restart_browser()
        self.request_count = 0
        self.url_count = 0  # 重置URL计数器
        logger.info("会话轮换完成")

    def increment_request_count(self):
        """增加请求计数"""
        self.request_count += 1
        if self.should_rotate_session():
            self.rotate_session()

    def increment_url_count(self):
        """增加URL计数"""
        self.url_count += 1
        logger.info(f"当前会话已处理 {self.url_count}/{self.max_urls_per_session} 个URL")
        if self.should_rotate_session():
            logger.info(f"达到会话限制，开始轮换会话")
            self.rotate_session()

    def get_source_urls(self) -> List[str]:
        """获取源URL数据，过滤掉已爬取的URL"""
        try:            
            logger.info("获取源URL数据...")
            all_urls = list(self.source_collection.find({},{"_id":0,"timestamp":0}))
            logger.info(f"源集合总URL数量: {len(all_urls)}")
            
            # 过滤掉已爬取的URL
            filtered_urls = []
            for url_data in all_urls:
                url = url_data
                if url.get('url') and url.get('url') not in self.crawled_urls:
                    filtered_urls.append(url)
            
            # 计算进度信息
            total_count = len(all_urls)
            crawled_count = len(self.crawled_urls)
            remaining_count = len(filtered_urls)
            
            logger.info(f"已爬取URL数量: {crawled_count}")
            logger.info(f"需要爬取的URL数量: {remaining_count}")
            
            if total_count > 0:
                progress_percent = (crawled_count / total_count) * 100
                logger.info(f"当前总体进度: {progress_percent:.2f}% ({crawled_count}/{total_count})")
                logger.info(f"剩余任务: {remaining_count} 个URL")
            
            return filtered_urls
            
        except Exception as e:
            logger.error(f"获取源URL数据失败: {str(e)}")
            return []

    def check_pagination_exists(self) -> tuple[bool, int]:
        """
        检查页面是否有分页数据，并返回最大页码数
        :return: (has_pagination, max_page_num)
        """
        try:
            # 等待分页元素加载
            pagination = self.driver.find_elements(By.CSS_SELECTOR, '.pageation, .el-pagination')
            if not pagination:
                logger.info("未找到分页元素")
                return False, 1

            # 获取所有页码li（根据实际HTML结构）
            page_numbers = self.driver.find_elements(By.CSS_SELECTOR, '.el-pager .number')
            if not page_numbers:
                logger.info("没有页码按钮")
                return False, 1

            # 获取所有页码文本，取最后一个数字
            max_page_num = 1
            for element in page_numbers:
                text = element.text.strip()
                if text.isdigit():
                    max_page_num = max(max_page_num, int(text))

            # 检查是否有下一页按钮（根据实际HTML结构）
            next_button = self.driver.find_elements(By.CSS_SELECTOR, '.el-pagination .btn-next:not([disabled]), .pageation .btn-next:not([disabled])')
            if not next_button and max_page_num == 1:
                logger.info("没有可用的下一页按钮")
                return False, 1

            logger.info(f"检测到分页数据，最大页码为 {max_page_num}")
            return True, max_page_num

        except Exception as e:
            logger.error(f"检查分页数据失败: {str(e)}")
            return False, 1

    def setup_xhr_listener(self):
        """设置XHR监听器，类似Playwright的page.on('response')"""
        try:
            # 启用网络监听
            self.driver.execute_cdp_cmd('Network.enable', {})
            logger.info("成功启用网络监听")
            
            # 清空之前的日志
            self.driver.get_log('performance')
            
            # 重置数据
            self.job_results = []
            self._current_page_num = None
            
        except Exception as e:
            logger.warning(f"设置XHR监听器失败: {str(e)}")

    def on_response(self, page_num: int) -> List[Dict]:
        """监听XHR响应，类似Playwright的on_response方法"""
        try:
            # 等待一段时间让网络请求完成
            time.sleep(3)
            
            # 获取网络日志
            logs = self.driver.get_log('performance')
            
            for log in logs:
                try:
                    message = json.loads(log['message'])
                    if (message['message']['method'] == 'Network.responseReceived' and
                        'api/job/search-pc' in message['message']['params']['response']['url'] and
                        f'pageNum={page_num}' in message['message']['params']['response']['url'] and
                        message['message']['params']['response']['status'] == 200):
                        
                        request_id = message['message']['params']['requestId']
                        response_body = self.driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                        
                        if response_body and 'body' in response_body:
                            json_data = json.loads(response_body['body'])
                            job_list = json_data.get('resultbody', {}).get('job', []).get('items', [])
                            if isinstance(job_list, list):
                                logger.info(f"[on_response] 监听到XHR，职位数: {len(job_list)}")
                                return job_list
                            else:
                                logger.error(f"[on_response] job_list不是列表，实际类型: {type(job_list)}，内容: {str(job_list)[:200]}")
                except Exception as e:
                    continue
            
            logger.warning(f"[on_response] 未找到第{page_num}页的XHR响应")
            return []
            
        except Exception as e:
            logger.error(f"[on_response] 解析XHR失败: {str(e)}")
            return []    

    def crawl_page_with_pagination(self, base_url: str, page_range: tuple = (1, 50)) -> dict:
        """
        爬取指定URL的所有页面（1-50页），用传统on/off监听方式，只监听当前pageNum的XHR。
        如果某一页岗位的updateDateTime字段小于2025年6月1日，则后续该url不再继续分页。
        返回all_page_data字典，异常时返回{}。
        """
        stop_due_to_date = False
        date_threshold = datetime(2025, 6, 1)
        try:
            logger.info(f"开始爬取: {base_url}")
            # 监听第一页
            self._current_page_num = 1
            self.job_results = []
            # 检查请求频率
            self.check_request_frequency()
            
            self.driver.get(base_url)
            
            # 增加请求计数
            self.increment_request_count()
            
            # 使用智能延迟
            self.smart_delay("search")
            if self.check_if_blocked():
                logger.warning(f"第1页出现验证码，轮换会话...")
                # 重新从第1页开始爬取
                return self.crawl_page_with_pagination(base_url, page_range)
            self.simulate_human_behavior()            
            
            # 获取第1页数据
            job_data = self.on_response(1)
            
            if not job_data:
                logger.info(f"第1页没有岗位了，停止后续分页")
                return {
                    'job_data':[],
                    'page_num':1,
                    'source_url':base_url,
                    'page_title':self.driver.title
                }
            clean_job_data = []
            # 日期判断：如果有岗位的updateDateTime小于2025-06-01，则后续不再分页
            for job in job_data:
                try:
                    update_str = str(job.get('updateDateTime', ''))
                    update_date = datetime.strptime(update_str[:10], '%Y-%m-%d')
                    if update_date < date_threshold:
                        stop_due_to_date = True
                        logger.info(f"第1页出现小于2025年6月的数据，停止后续分页。updateDateTime={update_str}")
                        break
                    else:
                        clean_job_data.append(job)
                except Exception:
                    pass
            
            has_pagination, max_page_num = self.check_pagination_exists()
            real_max_page = min(page_range[1], max_page_num)                        
            logger.info(f"第 1 页爬取成功")            
            if has_pagination and not stop_due_to_date:
                logger.info(f"检测到分页数据，最大页码为 {max_page_num}，开始分页爬取")
                for page_num in range(2, real_max_page + 1):
                    try:
                        logger.info(f"处理第 {page_num} 页")
                        self._current_page_num = page_num
                        self.job_results = []
                        self.goto_next_page(page_num)
                        # 增加请求计数
                        self.increment_request_count()
                        # 使用智能延迟
                        self.smart_delay("pagination")
                        self.simulate_human_behavior()
                        # 检查是否被封禁（验证码检测）
                        if self.check_if_blocked():
                            # 验证码处理：重启浏览器并重新从第1页开始
                            logger.warning(f"第{page_num}页出现验证码，重新从第1页开始...")
                            return self.crawl_page_with_pagination(base_url, page_range)
                        job_data = self.on_response(page_num)
                        # 日期判断：如果有岗位的updateDateTime小于2025-06-01，则后续不再分页
                        # 如果没有岗位了，则停止分页
                        if not job_data:
                            logger.info(f"第{page_num}页没有岗位了，停止后续分页")                            
                            break
                        for job in job_data:
                            try:
                                update_str = str(job.get('updateDateTime', ''))
                                update_date = datetime.strptime(update_str[:10], '%Y-%m-%d')
                                if update_date < date_threshold:
                                    stop_due_to_date = True
                                    logger.info(f"第{page_num}页出现小于2025年6月的数据，停止后续分页。updateDateTime={update_str}")
                                    break
                                else:
                                    clean_job_data.append(job)
                            except Exception:
                                pass                        
                        logger.info(f"第 {page_num} 页爬取成功")
                    
                        if stop_due_to_date:
                            break
                    except Exception as e:
                        logger.error(f"第 {page_num} 页爬取失败: {str(e)}")
                        try:                            
                            logger.info(f"尝试直接跳转到第 {page_num} 页")
                            self._current_page_num = page_num
                            self.jump_to_page(page_num)
                            self.random_delay()                            
                            # 检查是否被封禁（验证码检测）
                            if self.check_if_blocked():
                                # 验证码处理：重启浏览器并重新从第1页开始
                                logger.warning(f"跳转第{page_num}页出现验证码，重新从第1页开始...")
                                return self.crawl_page_with_pagination(base_url, page_range)
                            job_data = self.on_response(page_num)
                            # 日期判断：如果有岗位的updateDateTime小于2025-06-01，则后续不再分页
                            for job in job_data:
                                try:
                                    update_str = str(job.get('updateDateTime', ''))
                                    update_date = datetime.strptime(update_str[:10], '%Y-%m-%d')
                                    if update_date < date_threshold:
                                        stop_due_to_date = True
                                        logger.info(f"跳转第{page_num}页出现小于2025年6月的数据，停止后续分页。updateDateTime={update_str}")
                                        break
                                    else:
                                        clean_job_data.append(job)
                                except Exception:
                                    continue
                            
                            logger.info(f"第 {page_num} 页跳转成功")
                            
                            if stop_due_to_date:
                                break
                        except Exception as jump_error:
                            logger.error(f"跳转到第 {page_num} 页也失败: {str(jump_error)}")                            
                            break
                        continue
            else:
                logger.info("页面没有分页数据，只保存第1页")
            all_page_data = {
                'job_data': clean_job_data,
                'page_num': self._current_page_num,
                'source_url': base_url,
                'page_title': self.driver.title
            }
            return all_page_data
        except Exception as e:
            logger.error(f"爬取过程发生异常: {str(e)}")
            return {}

    def jump_to_page(self, page_num: int):
        """直接跳转到指定页面 - 基于实际HTML结构"""
        try:
            # 等待页面加载完成
            time.sleep(2)
            
            # 根据实际HTML结构，使用精确的选择器
            jump_input_selectors = [
                '#jump_page',                    # 主要选择器（根据HTML中的id）
                '.pageation #jump_page',         # 包含父容器
                'input[type="number"]',          # 备选选择器
                'input.mytxt'                    # 根据HTML中的class
            ]
            
            jump_input = None
            for selector in jump_input_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            jump_input = element
                            logger.debug(f"找到跳转输入框，使用选择器: {selector}")
                            break
                    if jump_input:
                        break
                except:
                    continue
            
            if not jump_input:
                raise Exception("找不到跳转输入框")
            
            # 清空输入框并输入页码
            jump_input.clear()
            time.sleep(0.5)
            jump_input.send_keys(str(page_num))
            time.sleep(0.5)
            
            # 根据实际HTML结构，使用精确的跳转按钮选择器
            jump_button_selectors = [
                '.jumpPage',                     # 主要选择器（根据HTML中的class）
                '.pageation .jumpPage',          # 包含父容器
                'span.jumpPage',                 # 指定元素类型
                'span[data-v-2a7f3c1e].jumpPage' # 包含data属性
            ]
            
            jump_button = None
            for selector in jump_button_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            jump_button = element
                            logger.debug(f"找到跳转按钮，使用选择器: {selector}")
                            break
                    if jump_button:
                        break
                except:
                    continue
            
            if not jump_button:
                # 尝试按回车键
                logger.info("未找到跳转按钮，尝试按回车键")
                jump_input.send_keys(Keys.RETURN)
            else:
                # 点击跳转按钮
                jump_button.click()
            
            self.random_delay()
            
            # 等待页面加载
            time.sleep(3)
            
            # 等待职位列表重新加载
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.j_joblist')))
                logger.info(f"成功跳转到第 {page_num} 页")
                return True
            except:
                logger.warning("等待职位列表超时，但继续执行")
                return True
                
        except Exception as e:
            logger.error(f"跳转到第 {page_num} 页失败: {str(e)}")
            # 尝试使用JavaScript跳转
            try:
                logger.info("尝试使用JavaScript跳转")
                self.driver.execute_script(f"""
                    var input = document.querySelector('#jump_page') || 
                               document.querySelector('input.mytxt');
                    var btn = document.querySelector('.jumpPage') || 
                             document.querySelector('span.jumpPage');
                    if (input) {{
                        input.value = '{page_num}';
                        if (btn) {{
                            btn.click();
                        }} else {{
                            input.dispatchEvent(new KeyboardEvent('keydown', {{key: 'Enter'}}));
                        }}
                        return true;
                    }}
                    return false;
                """)
                time.sleep(3)
                logger.info("JavaScript跳转完成")
                return True
            except Exception as js_error:
                logger.error(f"JavaScript跳转也失败: {js_error}")
                raise

    def goto_next_page(self, page_num: int = None):
        """
        点击"下一页"按钮 - 基于实际HTML结构
        """
        try:
            # 等待页面加载完成
            time.sleep(2)
            
            # 根据实际HTML结构，使用精确的选择器
            next_button_selectors = [
                '.el-pagination .btn-next:not([disabled])',  # 主要选择器
                '.btn-next:not([disabled])',                 # 备选选择器
                '.pageation .btn-next:not([disabled])',      # 包含父容器
                '.btn-next'                                  # 最后备选
            ]
            
            next_btn = None
            for selector in next_button_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            next_btn = element
                            logger.debug(f"找到下一页按钮，使用选择器: {selector}")
                            break
                    if next_btn:
                        break
                except:
                    continue
            
            if not next_btn:
                # 检查是否已经是最后一页（按钮被禁用）
                try:
                    disabled_next = self.driver.find_element(By.CSS_SELECTOR, '.btn-next[disabled]')
                    if disabled_next:
                        logger.info("已到达最后一页，没有更多页面")
                        return False
                except:
                    pass
                
                raise Exception("未找到可用的下一页按钮")
            
            # 滚动到按钮位置
            self.driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
            time.sleep(1)
            
            # 点击按钮
            next_btn.click()
            logger.info('点击"下一页"按钮')
            
            # 等待页面加载
            time.sleep(3)
            
            # 等待职位列表重新加载
            try:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.joblist')))
                logger.info("页面加载完成")
                return True
            except:
                logger.warning("等待职位列表超时，但继续执行")
                return True
                
        except Exception as e:
            logger.error(f"goto_next_page 点击下一页失败: {e}")
            # 尝试使用JavaScript点击
            try:
                logger.info("尝试使用JavaScript点击下一页按钮")
                self.driver.execute_script("""
                    var nextBtn = document.querySelector('.el-pagination .btn-next:not([disabled])') || 
                                 document.querySelector('.btn-next:not([disabled])') ||
                                 document.querySelector('.pageation .btn-next:not([disabled])');
                    if (nextBtn) {
                        nextBtn.click();
                        return true;
                    }
                    return false;
                """)
                time.sleep(3)
                logger.info("JavaScript点击完成")
                return True
            except Exception as js_error:
                logger.error(f"JavaScript点击也失败: {js_error}")
                raise

    def process_url_with_pagination(self, url: str, page_range: tuple = (1, 50)) -> bool:
        """处理单个URL的所有页面"""
        try:
            # 爬取所有页面
            all_page_data = self.crawl_page_with_pagination(url.get('url'), page_range)
            if not all_page_data:
                return False
            
            # 增加URL计数
            self.increment_url_count()

            # 1. 保存职位数据到目标集合
            for job in all_page_data['job_data']:
                job['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if all_page_data['job_data']:
                bulk_operations = []
                for job in all_page_data['job_data']:
                    filter_ = {'jobId': job.get('jobId')}
                    update = {
                        '$set': job,  # 更新所有字段
                        '$setOnInsert': {'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  # 只在插入时设置
                    }
                    bulk_operations.append(
                        UpdateOne(filter_, update, upsert=True)
                    )
                if bulk_operations:
                    self.target_collection.bulk_write(bulk_operations)

            # 2. 保存日志到日志集合
            log_data = {
                'source_url': all_page_data['source_url'],
                'industry': url.get('industry'),
                'jobArea': url.get('jobArea'),
                'keyword': url.get('keyword'),
                'page_num': all_page_data['page_num'],
                'page_title': all_page_data['page_title'],
                'job_count': len(all_page_data['job_data']),
                'crawl_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'job_update_date_range': '2025-06-01',
                'uploader':"ShanYongxu",
                'status': 'success',
            }
            log_filter = {'source_url': all_page_data['source_url']}
            log_update = {'$set': log_data}
            self.log_collection.update_one(log_filter, log_update, upsert=True)

            logger.info(f"URL {url} 处理完成，成功保存 {len(all_page_data['job_data'])} 条数据")
            return True

        except Exception as e:
            logger.error(f"处理URL失败 {url}: {str(e)}")
            return False

    def process_url(self, url: str) -> bool:
        """处理单个URL（保持向后兼容，只处理第1页）"""
        return self.process_url_with_pagination(url, page_range=(1, 1))

    def run(self, enable_pagination: bool = True, page_range: tuple = (1, 50)):
        """运行爬虫"""
        try:
            logger.info("开始运行前程无忧Step5爬虫 (Selenium版本)")
            if enable_pagination:
                logger.info(f"启用分页爬取，页面范围: {page_range[0]}-{page_range[1]}")
            else:
                logger.info("单页爬取模式")
            
            # 初始化浏览器
            self.init_browser()
            
            # 获取源URL数据
            urls = self.get_source_urls()
            if not urls:
                logger.warning("没有需要爬取的URL数据")
                return
            
            total_urls = len(urls)
            logger.info(f"开始处理 {total_urls} 个URL...")
            
            # 处理每个URL
            for i, url in enumerate(urls, 1):
                try:
                    # 计算实时进度
                    current_progress = (i / total_urls) * 100
                    logger.info(f"处理进度: {current_progress:.2f}% ({i}/{total_urls}) - URL: {url.get('url')[:100]}...")
                    
                    if enable_pagination:
                        success = self.process_url_with_pagination(url, page_range)
                    else:
                        success = self.process_url(url)
                    
                    logger.info(f"当前进度: {current_progress:.2f}% ({i}/{total_urls})")
                    
                except Exception as e:
                    logger.error(f"处理URL时发生异常: {str(e)}")
                    continue
            
            # 最终统计
            logger.info("=" * 50)
            logger.info("爬虫运行完成！")
            
        except Exception as e:
            logger.error(f"爬虫运行失败: {str(e)}")
        finally:
            self.close_browser()

    def close_browser(self):
        """关闭浏览器"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
            logger.info("浏览器已关闭")
        except Exception as e:
            logger.error(f"关闭浏览器失败: {str(e)}")
        finally:
            # 确保所有变量都设置为None
            self.driver = None
            self.wait = None

    def parse_cookie_string(self, cookie_string: str) -> List[Dict]:
        """
        解析cookie字符串为Selenium可用的格式
        :param cookie_string: cookie字符串
        :return: cookie列表
        """
        cookies = []
        for item in cookie_string.split('; '):
            if '=' in item:
                name, value = item.split('=', 1)
                cookies.append({
                    'name': name.strip(),
                    'value': value.strip(),
                    'domain': '.51job.com',
                    'path': '/'
                })
        return cookies

    def get_cookies(self) -> List[Dict]:
        """
        获取前程无忧的cookie配置
        :return: cookie列表
        """
        # 用户提供的新cookie字符串
        cookie_string = "_c_i_p=120200; 51job=cuid%3D260593881%26%7C%26cusername%3Dqy8BPeXZwk2kLbvQge6%252BKn7NmN%252Fjqn2VN1O9lDD1q2Q%253D%26%7C%26cpassword%3D%26%7C%26cname%3DEfTG3Hf6cG%252FkQDye68hodQ%253D%253D%26%7C%26cemail%3D%26%7C%26cemailstatus%3D0%26%7C%26cnickname%3D%26%7C%26ccry%3D.0eiSFexyfNis%26%7C%26cconfirmkey%3D%25241%2524Iq1Uem14%2524adR4BOkgLZyxT6KNw%252FESH.%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3D%25241%2524eNm%252F%252FIM2%2524323Gg5OPSmSCPtX2kag661%26%7C%26to%3Dfa293fd444bdf2d013c221706760b0f06867838e%26%7C%26; acw_sc__v2=686b9c29ad37ae361f7093a0fd5b67d3fedc46a0; acw_tc=ac11000117518827921201194e00992c248837522d772ac58b6f10ef77f15f; adv=ad_logid_url%3Dhttps%253A%252F%252Ftrace.51job.com%252Ftrace.php%253Fpartner%253Dsem_pcbingbd_42560%2526ajp%253DaHR0cHM6Ly9ta3QuNTFqb2IuY29tL3RnL3NlbS9scDIwMjUvTFBfMjAyNV9CQzIuaHRtbD9mcm9tPWJpbmdhZCZwYXJ0bmVyPXNlbV9wY2JpbmdiZF80MjU2MA%253D%253D%2526k%253D878e099aee01eaff342a93c50d4e0154%2526msclkid%253D6536928850d61d33f537fae3ccce20b3%26%7C%26; guid=7faaffb77d41dec9ea04dedd97ef882a; Hm_lpvt_1370a11171bd6f2d9b1fe98951541941=1751882788; Hm_lvt_1370a11171bd6f2d9b1fe98951541941=1751603280; HMACCOUNT=70BEDA251EA44150; jobs_search_req=dd0e3522bdffe691a244049cc8519671; JSESSIONID=D89612DF9EBFAD76EE4F2862E731D11D; partner=www_bing_com; ps=needv%3D0; sensor=createDate%3D2025-04-14%26%7C%26identityType%3D1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22260593881%22%2C%22first_id%22%3A%22197d3b0f89bc78-05835609215c5b4-4c657b58-1511158-197d3b0f89cc94%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.bing.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk3ZDNiMGY4OWJjNzgtMDU4MzU2MDkyMTVjNWI0LTRjNjU3YjU4LTE1MTExNTgtMTk3ZDNiMGY4OWNjOTQiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIyNjA1OTM4ODEifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22260593881%22%7D%2C%22%24device_id%22%3A%22197d3b1339c1600-062f2060a410934-4c657b58-1511158-197d3b1339d2139%22%7D; seo_refer_info_2023=%7B%22referUrl%22%3A%22https%3A%5C%2F%5C%2Fwww.bing.com%5C%2F%22%2C%22referHost%22%3A%22www.bing.com%22%2C%22landUrl%22%3A%22https%3A%5C%2F%5C%2Fwww.51job.com%5C%2F%22%2C%22landHost%22%3A%22www.51job.com%22%2C%22partner%22%3A%22www_bing_com%22%7D; slife=lastlogindate%3D20250707%26%7C%26securetime%3DUm4GMlQ3AGVUPg44W2INYQY8BzI%253D; ssxmod_itna=QqUx0QiQi=itTqiqYjWwD3dSDIxed+q0dGM0lDIqGQGcD8xiKDHKmoWPTYFbD0E5KhKSCY4btDl2ieDZDGIdDqx0orU+nuitD9CG5Npx5RP4RK0GhCM9KYuUPEhB3yF/lDSpVPreQrDU4GnD06xldxVDYAEDBYD74G+DDeDixGmKeDS0DD9DGPo2CTtEeDEDYPoxA3Di4D+mmrDmk4DGuEDx7QWmmGqfnDD0uD+=Y49QYaHqWFQR=uxC=hemeDMixGXFDkqmj9jy9Di1=SENPoKxB6nxBQt2YnxuaI3P6uTMd4mGhN6GE5rjDpAGzYxejP/QGsjD7WGPnwPY+qjpGDw67jCY46mD=34DDpr+AslTeb0FehS8yM+ylexDPAC+OCQ4xjAxF0FShiRx5o+NDbN3EXBwq8D4LoqMYQ8GDD; ssxmod_itna2=QqUx0QiQi=itTqiqYjWwD3dSDIxed+q0dGM0lDIqGQGcD8xiKDHKmoWPTYFbD0E5KhKSCY4+YDio8xjPdgx7P1Djx3uPDBdKWqbhcWk4E+wexkHKi5QDkiLeWuzS4ArKA9l+U0SUKkN2AkDulEf7euNdGx3HKii9tG2nbDx6/SUYSr6Kn8DGfqTt1hYLFnU0UTTV982aL4ru+gtHf8aKAdKaw=hYQCGFOwFoMdBYWqfEY0b=V3t6Fii7qT3wTlBx23hfDKdBim=/mRgcB4XV3Nx77YMPMk3j/p28xXdHzedzGdIIfu5wQi5gAdZ07rYxY4G3MGihGZTQWRoYYOZYke73+DK+0D8Q5oY5M05DhGSGDrGwknwznD4D"
        
        return self.parse_cookie_string(cookie_string)

def main():
    """主函数"""
    spider = QCWYSpiderStep5Selenium()
    spider.run()

if __name__ == "__main__":
    main()