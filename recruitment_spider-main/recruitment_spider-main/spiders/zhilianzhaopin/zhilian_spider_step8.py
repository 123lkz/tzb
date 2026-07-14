#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智联招聘爬虫 - 第七步
功能：从zhilian_job_raw集合中获取去重后的公司信息，为后续天眼查API调用做准备

主要步骤：
1. 从MongoDB读取zhilian_job_raw集合的数据
2. 使用聚合管道获取去重后的公司名称
3. 将去重后的公司信息保存到MongoDB和JSON文件
4. 检查公司是否已被天眼查API查询过
5. 使用Playwright模拟浏览器操作访问天眼查

数据存储：
- 输入集合：zhilian_job_raw
- 输出集合：zhilian_company_unique（只保存公司基本信息）
- 进度记录集合：zhilian_company_unique_log（保存处理状态和时间）

数据过滤规则：
1. 过滤掉空的公司名称
2. 统计每个公司名称出现的次数
3. 按出现次数降序排序
4. 过滤掉已经查询过的公司
"""

# ==================== 机器配置 ====================
# 请根据实际情况修改机器ID
MACHINE_ID = 1  # 修改为1或2，对应不同的机器
# ================================================

import os
import sys
import json
import logging
import time
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from tqdm import tqdm
from playwright.async_api import async_playwright
import requests
import asyncio
import aiohttp
import base64
from account_manager import AccountManager

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.append(project_root)

# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    logger = get_logger(__name__, "zhilian_spider_step7")
except ImportError:
    # 如果无法导入log_manager，则使用基本配置
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger("spiders.zhilian_spider")

class ZhilianSpiderStep7:
    """智联招聘公司信息处理爬虫"""
    
    def __init__(self, machine_id=1):
        # 机器ID
        self.machine_id = machine_id
        
        # MongoDB配置
        self.mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
        self.mongo_db = "MOOC123_DA"
        self.input_collection = "zhilian_company_part1"
        self.output_collection = "zhilian_company_unique_part1"
        self.progress_collection = "zhilian_company_unique_log_part1"
        
        # 输出目录配置
        self.output_dir = Path("output/company_info")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # MongoDB连接
        self.mongo_client = None
        self.db = None
        
        # 天眼查配置
        self.tianyancha_base_url = "https://www.tianyancha.com/nsearch"
        # 滑块识别API KEY
        self.slide_api_key = "A9xtDLlxZlN4fdFwI7Bx"
        
        # 初始化MongoDB连接
        self._init_mongodb()
        
        self.account_manager = AccountManager(
            host="210.14.140.50",
            port=10308,
            password="TsjklgjJOerigjsrigqoijhklejgqirjgh",
            db=9,
            machine_id=machine_id
        )
        self.account_info = None
        
        logger.info(f"机器{machine_id}初始化完成")
    
    def _init_mongodb(self):
        """初始化MongoDB连接"""
        try:
            self.mongo_client = MongoClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            logger.info("MongoDB连接成功")
        except Exception as e:
            logger.error(f"MongoDB连接失败: {str(e)}")
            raise
    
    def get_unique_companies(self) -> List[Dict]:
        """从MongoDB获取去重后的公司名称"""
        try:
            # 获取已处理的公司
            processed = self.db[self.progress_collection].find(
                {},
                {"company_name": 1}
            )
            processed_companies = {doc["company_name"]: 1 for doc in processed}
            logger.info(f"已加载 {len(processed_companies)} 个已处理的公司")
            
            # 获取所有公司
            pipeline = [
                {
                    "$match": {
                        "company_name": {"$exists": True, "$ne": ""}
                    }
                },
                {
                    "$group": {
                        "_id": "$company_name",
                        "count": {"$sum": 1}
                    }
                },
                {
                    "$sort": {"count": -1}
                }
            ]
            
            all_companies = list(self.db[self.input_collection].aggregate(pipeline))
            logger.info(f"成功获取 {len(all_companies)} 个不同的公司")
            
            # 过滤掉已处理的公司
            unprocessed_companies = [
                company for company in all_companies 
                if company['_id'] not in processed_companies
            ]
            logger.info(f"未处理的公司数量: {len(unprocessed_companies)}")
            
            return unprocessed_companies
            
        except Exception as e:
            logger.error(f"获取公司信息失败: {str(e)}")
            return []
    
    async def _init_browser(self, playwright):
        """初始化浏览器配置（增强反爬虫）"""
        browser_args = [
            '--disable-blink-features=AutomationControlled',
            '--disable-infobars',
            '--window-size=1280,800',
            '--start-maximized',
            '--disable-gpu',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
            '--lang=zh-CN,zh',
            '--disable-extensions',
            '--disable-notifications',
            '--disable-popup-blocking',
            '--disable-save-password-bubble',
            '--disable-translate',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-breakpad',
            '--disable-component-extensions-with-background-pages',
            '--disable-features=TranslateUI,BlinkGenPropertyTrees',
            '--disable-ipc-flooding-protection',
            '--disable-renderer-backgrounding',
            '--enable-features=NetworkService,NetworkServiceInProcess',
            '--force-color-profile=srgb',
            '--metrics-recording-only',
            '--mute-audio',
        ]
        
        browser = await playwright.chromium.launch(
            headless=False,
            args=browser_args
        )
        
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='zh-CN',
            timezone_id='Asia/Shanghai',
            geolocation={'latitude': 31.2304, 'longitude': 121.4737},
            permissions=['geolocation'],
            color_scheme='light',
            reduced_motion='no-preference',
            forced_colors='none',
            accept_downloads=False,
            has_touch=False,
            is_mobile=False,
            device_scale_factor=1,
            extra_http_headers={
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0',
                'Sec-CH-UA': '"Chromium";v="120", "Not:A-Brand";v="99"',
                'Sec-CH-UA-Mobile': '?0',
                'Sec-CH-UA-Platform': '"Windows"',
                'Sec-CH-UA-Platform-Version': '"10.0.0"',
                'Sec-CH-UA-Full-Version': '"120.0.6099.130"',
                'Sec-CH-UA-Full-Version-List': '"Chromium";v="120.0.6099.130", "Not:A-Brand";v="99.0.0.0"',
                'Sec-CH-UA-Bitness': '"64"',
                'Sec-CH-UA-Model': '""',
                'Sec-CH-UA-Arch': '"x86"',
                'Sec-CH-UA-Wow64': '?0',
                'Sec-CH-UA-Full-Version-List': '"Chromium";v="120.0.6099.130", "Not:A-Brand";v="99.0.0.0"',
                'Sec-CH-UA-Full-Version': '"120.0.6099.130"',
                'Sec-CH-UA-Platform-Version': '"10.0.0"',
                'Sec-CH-UA-Platform': '"Windows"',
                'Sec-CH-UA-Mobile': '?0',
                'Sec-CH-UA': '"Chromium";v="120", "Not:A-Brand";v="99"',
                'Sec-CH-UA-Bitness': '"64"',
                'Sec-CH-UA-Arch': '"x86"',
                'Sec-CH-UA-Model': '""',
                'Sec-CH-UA-Wow64': '?0',
            }
        )
        
        # 注入更丰富的反检测脚本
        context.add_init_script("""
            // 基础属性
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {
                get: () => [
                    {
                        0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format"},
                        description: "Portable Document Format",
                        filename: "internal-pdf-viewer",
                        length: 1,
                        name: "Chrome PDF Plugin"
                    },
                    {
                        0: {type: "application/pdf", suffixes: "pdf", description: "Portable Document Format"},
                        description: "Portable Document Format",
                        filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
                        length: 1,
                        name: "Chrome PDF Viewer"
                    },
                    {
                        0: {type: "application/x-nacl", suffixes: "", description: "Native Client Executable"},
                        1: {type: "application/x-pnacl", suffixes: "", description: "Portable Native Client Executable"},
                        description: "Native Client",
                        filename: "internal-nacl-plugin",
                        length: 2,
                        name: "Native Client"
                    }
                ]
            });
            Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en-US', 'en']});
            Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
            
            // 模拟Chrome运行时
            window.navigator.chrome = {
                runtime: {},
                loadTimes: function(){},
                csi: function(){},
                app: {}
            };
            
            // 模拟屏幕属性
            Object.defineProperty(window, 'outerWidth', {get: () => window.innerWidth + 100});
            Object.defineProperty(window, 'outerHeight', {get: () => window.innerHeight + 100});
            Object.defineProperty(window, 'screenX', {get: () => 0});
            Object.defineProperty(window, 'screenY', {get: () => 0});
            Object.defineProperty(window, 'devicePixelRatio', {get: () => 1});
            
            // 模拟WebGL
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) {
                    return 'Intel Inc.';
                }
                if (parameter === 37446) {
                    return 'Intel Iris OpenGL Engine';
                }
                return getParameter.apply(this, arguments);
            };
            
            // 模拟Canvas指纹
            const originalGetContext = HTMLCanvasElement.prototype.getContext;
            HTMLCanvasElement.prototype.getContext = function(type) {
                const context = originalGetContext.apply(this, arguments);
                if (type === '2d') {
                    const originalGetImageData = context.getImageData;
                    context.getImageData = function() {
                        const imageData = originalGetImageData.apply(this, arguments);
                        // 添加一些随机噪声
                        for (let i = 0; i < imageData.data.length; i += 4) {
                            imageData.data[i] = imageData.data[i] + Math.random() * 2 - 1;
                        }
                        return imageData;
                    };
                }
                return context;
            };
            
            // 模拟字体
            Object.defineProperty(navigator, 'fonts', {
                get: () => ({
                    ready: Promise.resolve(),
                    check: () => true,
                    load: () => Promise.resolve([])
                })
            });
        """)
        
        page = await context.new_page()
        page.set_default_timeout(30000)
        return browser, context, page

    async def simulate_human_action(self, page):
        """模拟用户操作，增强反爬"""
        # 随机滚动
        for _ in range(random.randint(1, 3)):
            await page.mouse.wheel(0, random.randint(100, 800))
            await asyncio.sleep(random.uniform(0.1, 0.3))
        # 随机鼠标移动
        for _ in range(random.randint(1, 3)):
            x, y = random.randint(0, 1200), random.randint(0, 700)
            await page.mouse.move(x, y, steps=random.randint(5, 20))
            await asyncio.sleep(random.uniform(0.1, 0.3))

    async def _save_company_data(self, company_name: str, company_data: Dict) -> bool:
        """保存公司数据到zhilian_company_unique集合"""
        try:
            # 添加爬取时间
            company_data['crawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 这是关于公司名称的来源，就是我通过那个公司名称搜到的这个
            company_data['originName'] = company_name
            # 保存到zhilian_company_unique集合
            self.db[self.output_collection].update_one(
                {"name": company_data.get('name', company_name)},
                {"$set": company_data},
                upsert=True
            )
            
            logger.info(f"公司 {company_name} 数据保存成功")
            return True
            
        except Exception as e:
            logger.error(f"保存公司数据失败: {str(e)}")
            return False

    async def _update_company_status(self, company_name: str, status: str, error: str = None):
        """更新公司处理状态到zhilian_company_unique_log集合"""
        try:
            update_data = {
                "company_name": company_name,
                "status": status,
                "account": self.account_info['username'],
                "process_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            if error:
                update_data["error"] = error
                
            self.db[self.progress_collection].update_one(
                {"company_name": company_name},
                {"$set": update_data},
                upsert=True
            )
            
            logger.info(f"公司 {company_name} 状态更新为: {status}")
            return True
            
        except Exception as e:
            logger.error(f"更新公司状态失败: {str(e)}")
            return False

    async def _handle_verify_image(self, image_paths: list) -> dict:
        """处理验证码图片，调用得塔云API"""
        try:
            import base64
            import json
            import requests
            
            # 准备请求数据
            headers = {
                "Content-Type": "application/json"
            }
            
            # 读取所有图片并转换为base64（包含图片头）
            img_base64_list = []
            for img_path in image_paths:
                with open(img_path, 'rb') as f:
                    img_data = f.read()
                    # 添加图片头
                    img_base64 = f"data:image/jpeg;base64,{base64.b64encode(img_data).decode('utf-8')}"
                    img_base64_list.append(img_base64)
            
            # 构建请求数据
            data = {
                "key": "A9xtDLlxZlN4fdFwI7Bx",
                "verify_idf_id": "47",
                "img1": img_base64_list[0],  # 背景大图
                "img2": img_base64_list[1],  # 小图1
                "img3": img_base64_list[2],  # 小图2
                "img4": img_base64_list[3]   # 小图3
            }
            
            # 发送请求
            response = requests.post(
                "http://bq1gpmr8.xiaomy.net/openapi/verify_code_identify/",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 200:
                    logger.info("验证码识别成功")
                    return result
                else:
                    logger.error("验证码识别失败")
                    return None
            else:
                logger.error(f"验证码识别请求失败: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"验证码识别过程出错: {str(e)}")
            return None

    async def _handle_captcha(self, page) -> bool:
        """处理验证码"""
        try:
            # 检查是否存在验证码
            try:
                verify_element = await page.wait_for_selector('text=请进行身份验证以继续使用', timeout=5000)
                if not verify_element:
                    return False
            except:
                return False
                
            logger.info("检测到验证码，开始处理...")
            
            # 点击验证按钮
            logger.info("点击验证按钮...")
            await page.click('div.geetest_btn_click')
            await asyncio.sleep(2)
            
            # 等待验证码图片加载
            logger.info("等待验证码图片加载...")
            await page.wait_for_selector('div.geetest_bg')
            await page.wait_for_selector('div.geetest_ques_tips')
            
            # 获取背景图片URL
            bg_element = await page.query_selector('div.geetest_bg')
            if not bg_element:
                logger.error("未找到背景图片元素")
                return False
                
            bg_style = await bg_element.get_attribute('style')
            if not bg_style:
                logger.error("未找到背景图片样式")
                return False
                
            bg_url = bg_style.split('url("')[1].split('")')[0]
            logger.info(f"背景图片URL: {bg_url}")
            
            # 获取三个提示图片URL
            tip_elements = await page.query_selector_all('div.geetest_ques_tips img')
            if not tip_elements:
                logger.error("未找到提示图片元素")
                return False
                
            tip_urls = []
            for img in tip_elements:
                src = await img.get_attribute('src')
                if src:
                    tip_urls.append(src)
                    logger.info(f"提示图片URL: {src}")
            
            if not tip_urls:
                logger.error("未获取到任何提示图片URL")
                return False
            
            # 创建temp目录
            import os
            temp_dir = os.path.join(project_root, 'recruitment_spider', 'temp')
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            
            # 下载图片
            image_paths = []
            try:
                async with aiohttp.ClientSession() as session:
                    # 下载背景图片
                    bg_path = os.path.join(temp_dir, f"bg_{int(time.time())}.jpg")
                    async with session.get(bg_url) as response:
                        if response.status == 200:
                            with open(bg_path, 'wb') as f:
                                f.write(await response.read())
                            image_paths.append(bg_path)
                        else:
                            logger.error(f"下载背景图片失败: HTTP {response.status}")
                            return False
                    
                    # 下载提示图片
                    for i, url in enumerate(tip_urls):
                        tip_path = os.path.join(temp_dir, f"tip_{i}_{int(time.time())}.jpg")
                        async with session.get(url) as response:
                            if response.status == 200:
                                with open(tip_path, 'wb') as f:
                                    f.write(await response.read())
                                image_paths.append(tip_path)
                            else:
                                logger.error(f"下载提示图片失败: HTTP {response.status}")
                                return False
            except Exception as e:
                logger.error(f"下载图片失败: {str(e)}")
                return False
            
            try:
                # 调用得塔云验证码识别服务
                result = await self._handle_verify_image(image_paths)                
                # 解析坐标
                try:
                    coords_str = result['data']['res_str']
                    # 移除首尾的方括号，并按逗号分割
                    coords_str = coords_str.strip('[]')
                    coord_pairs = coords_str.split('), (')
                    # 处理每个坐标对
                    coords = []
                    for pair in coord_pairs:
                        # 移除括号并分割坐标
                        x, y = pair.strip('()').split(', ')
                        coords.append((int(x), int(y)))
                    
                    logger.info(f"解析到的坐标: {coords}")
                    
                    # 获取验证码图片元素的位置
                    bg_box = await bg_element.bounding_box()
                    if not bg_box:
                        logger.error("无法获取验证码图片位置")
                        return False
                        
                    # 点击每个坐标
                    for x, y in coords:
                        # 计算相对于验证码图片的点击位置
                        click_x = bg_box['x'] + x
                        click_y = bg_box['y'] + y
                        
                        # 移动鼠标到位置并点击
                        await page.mouse.move(click_x, click_y)
                        await asyncio.sleep(0.5)  # 短暂延迟
                        await page.mouse.click(click_x, click_y)
                        await asyncio.sleep(0.5)  # 点击后等待
                        
                    # 点击登录按钮重新触发验证码（使用更稳定的选择器）
                    await page.click('div.geetest_submit')
                    await asyncio.sleep(3)
                    
                    # 检查是否验证成功（通过检查验证码弹窗是否消失）
                    try:
                        # 等待验证码弹窗消失
                        await page.wait_for_selector('div.geetest_submit', timeout=5000, state='hidden')
                        logger.info("验证码验证成功")
                        return True
                    except:
                        logger.error("验证码验证失败")
                        return False
                        
                except Exception as e:
                    logger.error(f"处理验证码坐标失败: {str(e)}")
                    return False
                else:
                    logger.error("验证码识别失败")
                    return False
                    
            finally:
                # 清理临时文件
                for image_path in image_paths:
                    try:
                        if os.path.exists(image_path):
                            os.remove(image_path)
                            logger.info(f"删除临时文件: {image_path}")
                    except Exception as e:
                        logger.error(f"删除临时文件失败: {str(e)}")
            
        except Exception as e:
            logger.error(f"验证码处理失败: {str(e)}")
            return False

    async def _handle_login_captcha(self, page) -> bool:
        """处理登录验证码"""
        while True:
            try:
                logger.info("开始处理登录验证码...")                
                # 等待验证码加载
                logger.info("等待验证码加载...")
                await page.wait_for_selector('div.geetest_bg', timeout=10000)
                
                # 循环检测验证码类型，直到遇到滑块验证码
                max_attempts = 999  # 最多尝试5次
                for attempt in range(max_attempts):
                    logger.info(f"第{attempt + 1}次检测验证码类型...")
                    
                    # 获取验证码类型
                    captcha_type = await self._detect_login_captcha_type(page)
                    logger.info(f"检测到验证码类型: {captcha_type}")
                    
                    if captcha_type == "slide":
                        logger.info("检测到滑块验证码，开始处理...")
                        return await self._handle_login_slide_captcha(page)
                    elif captcha_type == "word":
                        logger.info("检测到文字点选验证码，点击(50,50)坐标并重新检测...")
                        # 点击坐标(50,50)
                        await page.mouse.click(50, 50)
                        await asyncio.sleep(1)
                        
                        # 点击登录按钮重新触发验证码（使用更稳定的选择器）
                        await page.click('button:has-text("登录")')
                        await asyncio.sleep(3)
                        
                        # 等待验证码重新加载
                        try:
                            await page.wait_for_selector('div.geetest_bg', timeout=5000)
                        except:
                            logger.info("验证码重新加载失败，可能已经通过")
                            return True
                    else:
                        logger.warning(f"未知的验证码类型: {captcha_type}")
                        return False
                
                logger.error(f"尝试{max_attempts}次后仍未遇到滑块验证码")
                return False
                
            except Exception as e:
                logger.error(f"登录验证码处理失败: {str(e)}")
                time.sleep(10)
                continue
                

    async def _detect_login_captcha_type(self, page) -> str:
        """检测登录验证码类型"""
        try:
            
            # 检查是否有"确定"按钮（文字点选验证码的特征）
            submit_button = await page.query_selector('.geetest_submit')
            if submit_button:
                logger.info("检测到文字点选验证码（存在确定按钮）")
                return "word"
            else:
                logger.info("检测到滑块验证码（无确定按钮）")
                return "slide"
            
        except Exception as e:
            logger.error(f"检测验证码类型失败: {str(e)}")
            return ""

    async def _handle_login_slide_captcha(self, page) -> bool:
        """处理登录时的滑块验证码（集成第三方接口识别滑动距离，带重试）"""
        import base64
        import aiohttp
        import re
        max_attempts = 10
        for attempt in range(max_attempts):
            try:
                logger.info(f"开始处理登录滑块验证码...（第{attempt+1}次尝试）")
                # 等待滑块元素出现（模糊匹配 class，避免 hash 干扰）
                await page.wait_for_selector('div[class*="geetest_btn"]', timeout=10000)
                # 获取滑块和轨道元素（模糊匹配 class）
                slider = await page.query_selector('div[class*="geetest_btn"]')
                track = await page.query_selector('div[class*="geetest_track"]')
                if not slider or not track:
                    logger.error("未找到滑块或轨道元素")
                    return False
                # 获取轨道宽度
                track_box = await track.bounding_box()
                slider_box = await slider.bounding_box()
                if not track_box or not slider_box:
                    logger.error("无法获取滑块或轨道位置")
                    return False
                # 获取验证码原图URL
                bg_element = await page.query_selector('div[class*="geetest_bg"]')
                if not bg_element:
                    logger.error("未找到验证码背景元素")
                    return False
                # 获取背景图片URL
                bg_style = await bg_element.get_attribute('style')
                if not bg_style or 'background-image' not in bg_style:
                    logger.error("未找到背景图片URL")
                    return False
                url_match = re.search(r'url\("([^"]+)"\)', bg_style)
                if not url_match:
                    logger.error("无法提取背景图片URL")
                    return False
                bg_image_url = url_match.group(1)
                logger.info(f"获取到验证码原图URL: {bg_image_url}")
                # 下载原图
                async with aiohttp.ClientSession() as session:
                    async with session.get(bg_image_url) as resp:
                        if resp.status != 200:
                            logger.error(f"下载验证码图片失败: HTTP {resp.status}")
                            return False
                        img_bytes = await resp.read()
                # 调用第三方接口识别滑动距离
                url = "http://bq1gpmr8.xiaomy.net/openapi/verify_code_identify/"
                headers = {"Content-Type": "application/json"}
                img_base64 = "data:image/png;base64," + base64.b64encode(img_bytes).decode()
                payload = {
                    "key": self.slide_api_key,
                    "verify_idf_id": "23",
                    "img_base64": img_base64
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json=payload, timeout=15) as resp:
                        res = await resp.json()
                        if res.get("code") == 200:
                            data = res.get("data")
                            if isinstance(data, str):
                                data = json.loads(data)
                            distance = int(data.get("distance")) -12
                            logger.info(f"接口识别滑动距离: {distance} 像素")
                        else:
                            logger.error(f"验证码识别接口错误: {res.get('msg')}")
                            continue
                # 页面实际滑动距离（如截图与页面1:1则直接用distance）
                slide_distance = distance
                logger.info(f"开始滑动，距离: {slide_distance}")
                # 执行滑动操作
                start_x = slider_box['x'] + slider_box['width']/2
                start_y = slider_box['y'] + slider_box['height']/2
                await page.mouse.move(start_x, start_y)
                await asyncio.sleep(0.5)
                await page.mouse.down()
                await asyncio.sleep(0.2)
                steps = 10
                step_distance = slide_distance / steps
                for i in range(steps):
                    current_x = start_x + (i + 1) * step_distance
                    await page.mouse.move(current_x, start_y)
                    await asyncio.sleep(random.uniform(0.05, 0.15))
                await page.mouse.up()
                await asyncio.sleep(2)
                # 检查验证码是否还在（如滑块按钮还在则说明未通过）
                try:
                    await page.wait_for_selector('div[class*="geetest_btn"]', timeout=2000)
                    logger.warning("滑动后验证码还在，准备重试...")
                    continue
                except Exception:
                    logger.info("滑块验证通过")
                    return True
            except Exception as e:
                logger.error(f"登录滑块验证码处理失败: {str(e)}，准备重试...")
                continue
        logger.error(f"滑块验证码连续{max_attempts}次未通过，放弃")
        return False

    async def _process_company(self, page, company_name: str) -> bool:
        """处理单个公司"""
        try:
            logger.info(f"开始处理公司: {company_name}")                                               
            
            # 获取公司数据
            company_data = await self._get_company_data(page, company_name)
            if not company_data:
                logger.error(f"获取公司 {company_name} 数据失败")
                await self._update_company_status(company_name, "failed", "获取公司数据失败")
                return False            
            
            # 保存公司数据
            if not await self._save_company_data(company_name, company_data):
                logger.error(f"保存公司 {company_name} 数据失败")
                await self._update_company_status(company_name, "failed", "保存公司数据失败")
                return False
            
            # 更新处理状态为成功
            await self._update_company_status(company_name, "success")
            return True
            
        except Exception as e:
            logger.error(f"处理公司 {company_name} 时发生错误: {str(e)}")
            await self._update_company_status(company_name, "failed", str(e))
            return False

    async def _get_company_data(self, page, company_name: str) -> dict:
        """获取公司数据"""
        try:
            # 访问公司页面            
            await page.goto(f"https://www.tianyancha.com/search?key={company_name}")
            await page.wait_for_load_state("networkidle")
            await self.simulate_human_action(page)
            await asyncio.sleep(random.uniform(1, 3))
            
            # 处理可能出现的验证码
            if await self._handle_captcha(page):
                logger.info("验证码处理完成，继续获取数据...")                
                # 重新访问公司页面
                # await page.goto(f"https://www.tianyancha.com/search?key={company_name}")
                # await page.wait_for_load_state("networkidle")
                # await self.simulate_human_action(page)
                # await asyncio.sleep(random.uniform(2, 5))
            # 使用evaluate检查数据是否存在
            next_data = await page.evaluate('''() => {
                const script = document.getElementById("__NEXT_DATA__");
                return script ? script.textContent : null;
            }''')
            await asyncio.sleep(random.uniform(1, 3))
            
            if not next_data:
                logger.error(f"未找到公司 {company_name} 的数据")
                return None
                
            # 解析数据
            data = json.loads(next_data)
            company_list = data.get('props', {}).get('pageProps', {}).get('dehydratedState', {}).get('queries', [{}])[-1].get('state', {}).get('data', {}).get('data', {}).get('companyList', [])
            
            if not company_list:
                logger.error(f"未找到公司 {company_name} 的列表数据")
                return None
                
            return company_list[0]
            
        except Exception as e:
            logger.error(f"获取公司 {company_name} 数据失败: {str(e)}")
            return None

    async def _login_tianyancha(self, page) -> bool:
        """自动登录天眼查"""
        max_login_attempts = 99  # 最大登录尝试次数
        
        for attempt in range(max_login_attempts):
            try:
                logger.info(f"开始第{attempt + 1}次登录天眼查...")
                await page.goto("https://www.tianyancha.com")
                await page.wait_for_load_state("networkidle")
                logger.info("点击登录/注册按钮...")
                await page.click('.tyc-nav-user-btn')
                await asyncio.sleep(2)
                logger.info("点击密码登录...")
                await page.click('.login-toggle.-scan')
                await asyncio.sleep(1)
                logger.info("点击密码登录标签...")
                await page.click('.title-password')
                await asyncio.sleep(1)
                logger.info("输入手机号...")
                await page.fill('input[placeholder="请输入中国大陆手机号"]', self.account_info['username'])
                await asyncio.sleep(1)
                logger.info("输入密码...")
                await page.fill('input[placeholder="请输入登录密码"]', self.account_info['password'])
                await asyncio.sleep(1)
                logger.info("勾选同意协议...")
                await page.check('input[type="checkbox"]')
                await asyncio.sleep(1)
                logger.info("点击登录按钮...")
                await page.click('button:has-text("登录")')
                
                # 处理验证码
                if await self._handle_login_captcha(page):
                    logger.info("登录验证码处理完成")
                
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(2)  # 等待页面稳定
                
                # 验证登录是否成功
                logger.info("验证登录状态...")
                current_url = page.url
                logger.info(f"当前页面URL: {current_url}")
                
                # 访问个人中心页面验证登录状态
                await page.goto("https://www.tianyancha.com/usercenter/personalcenter", wait_until="networkidle")
                await asyncio.sleep(3)  # 等待页面加载和可能的重定向
                
                final_url = page.url
                logger.info(f"访问个人中心后的URL: {final_url}")
                
                # 判断是否登录成功
                if final_url == "https://www.tianyancha.com/usercenter/personalcenter":
                    logger.info("登录成功！成功访问个人中心页面")
                    return True
                elif final_url == "https://www.tianyancha.com/login" or final_url == "https://www.tianyancha.com/":
                    logger.warning(f"登录失败，被重定向到: {final_url}")
                    if attempt < max_login_attempts - 1:
                        logger.info(f"准备第{attempt + 2}次登录尝试...")
                        await asyncio.sleep(2)  # 等待一段时间后重试
                        continue
                    else:
                        logger.error("已达到最大登录尝试次数，登录失败")
                        return False
            except Exception as e:
                logger.error(f"第{attempt + 1}次登录过程发生错误: {str(e)}")
                if attempt < max_login_attempts - 1:
                    logger.info(f"准备第{attempt + 2}次登录尝试...")
                    await asyncio.sleep(2)
                    continue
                else:
                    logger.error("已达到最大登录尝试次数，登录失败")
                    return False
        
        return False

    async def process_data(self):
        """处理数据主函数（支持账号自动轮换和中断恢复）"""
        import time
        try:
            # 启动时清理可能卡住的账号
            self.account_manager.cleanup_stale_accounts()
            
            # 获取未处理的公司
            unprocessed_companies = self.get_unique_companies()
            if not unprocessed_companies:
                logger.error("未获取到任何未处理的公司信息")
                return
            company_idx = 0
            total_companies = len(unprocessed_companies)
            async with async_playwright() as p:
                browser = context = page = None
                while company_idx < total_companies:
                    # 1. 获取可用账号（支持中断恢复）
                    if not self.account_info:
                        self.account_info = self.account_manager.get_available_account()
                        if not self.account_info:
                            logger.error(f"机器{self.machine_id}无可用账号，等待30秒后重试...")
                            await asyncio.sleep(30)
                            continue
                        logger.info(f"机器{self.machine_id}使用账号: {self.account_info['username']}")
                    
                    # 2. 初始化浏览器并登录（如果是新账号）
                    if not browser:
                        browser, context, page = await self._init_browser(p)
                        if not await self._login_tianyancha(page):
                            logger.error(f"机器{self.machine_id}登录失败，标记账号冷却并重试")
                            self.account_manager.mark_account_cooldown(self.account_info, hours=72)
                            self.account_info = None
                            await browser.close()
                            browser = context = page = None
                            continue
                        logger.info(f"机器{self.machine_id}登录成功，开始处理数据")
                    
                    # 3. 处理公司
                    with tqdm(total=total_companies, initial=company_idx, desc=f"机器{self.machine_id}处理进度", unit="个") as pbar:
                        while company_idx < total_companies:
                            # 定期更新账号心跳（每处理10个公司更新一次）
                            if company_idx % 10 == 0:
                                if not self.account_manager.update_account_heartbeat(self.account_info):
                                    logger.info(f"机器{self.machine_id}账号 {self.account_info['username']} 使用时长已达上限，切换账号")
                                    # 关闭浏览器
                                    if browser:
                                        await browser.close()
                                    # 标记账号冷却
                                    self.account_manager.mark_account_cooldown(self.account_info, hours=72)
                                    # 切换账号
                                    self.account_info = None
                                    browser = context = page = None
                                    break  # 跳出内层while，重新获取账号
                            
                            company = unprocessed_companies[company_idx]
                            company_name = company['_id']
                            logger.info(f"机器{self.machine_id}当前账号: {self.account_info['username']}，开始处理公司: {company_name}")
                            
                            if await self._process_company(page, company_name):
                                logger.info(f"机器{self.machine_id}当前账号: {self.account_info['username']}，公司 {company_name} 处理成功")
                            else:
                                logger.error(f"机器{self.machine_id}当前账号: {self.account_info['username']}，公司 {company_name} 处理失败")
                            
                            company_idx += 1
                            pbar.update(1)
                            pbar.set_postfix({
                                "当前公司": company_name,
                                "成功率": f"{pbar.n}/{pbar.total}",
                                "账号": self.account_info['username'],
                                "机器": self.machine_id
                            })
                            
                            # 每处理完一个公司后短暂休息
                            await asyncio.sleep(random.uniform(1, 3))
                
                logger.info(f"机器{self.machine_id}所有公司处理完成")
        except Exception as e:
            logger.error(f"机器{self.machine_id}数据处理失败: {str(e)}")
        finally:
            # 程序结束时释放当前账号锁
            if self.account_info:
                self.account_manager.release_account_lock(self.account_info)
            self.close()
    
    def close(self):
        """关闭MongoDB连接"""
        if hasattr(self, 'mongo_client'):
            self.mongo_client.close()
            logger.info(f"机器{self.machine_id} MongoDB连接已关闭")

async def main():
    """主函数"""
    # 验证机器ID
    if MACHINE_ID < 1 or MACHINE_ID > 2:
        logger.error("机器ID必须在1-2之间")
        return
    
    spider = ZhilianSpiderStep7(machine_id=MACHINE_ID)
    try:
        await spider.process_data()
    except Exception as e:
        logger.error(f"机器{MACHINE_ID}程序执行失败: {str(e)}")
    finally:
        spider.close()

if __name__ == "__main__":
    asyncio.run(main()) 