import asyncio
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import random
import sys
import time
import re

from scrapy import Spider
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from pymongo.operations import UpdateOne

# 尝试加载.env文件中的环境变量
from dotenv import load_dotenv
# 获取项目根目录
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
env_path = os.path.join(project_root, '.env')
# 加载.env文件
load_dotenv(dotenv_path=env_path)

# 从环境变量获取MongoDB配置
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('MONGO_DB', 'recruitment')
COLLECTION_NAME = os.environ.get('MONGO_COLLECTION_RAW', 'jobs_raw')

# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    # 配置日志
    logger = get_logger(__name__, "base_spider")
except ImportError:
    # 配置基本日志，以防日志管理模块未安装
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

class BaseSpider(Spider):
    """
    爬虫基类，提供通用功能：
    1. 浏览器管理（Playwright）
    2. 数据库连接（MongoDB）
    3. 反爬处理
    4. 错误处理
    """
    name = 'base_spider'
    
    def __init__(self, headless: bool = True, browser_count: int = 1, tabs_per_browser: int = 1, city: str = "全国", 
                 block_resources: bool = True, resource_filter_level: str = "medium", *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        
        # 爬虫配置
        self.headless = headless if isinstance(headless, bool) else headless.lower() == 'true'
        self.browser_count = int(browser_count)
        self.tabs_per_browser = int(tabs_per_browser)
        self.city = city
        self.block_resources = block_resources if isinstance(block_resources, bool) else block_resources.lower() == 'true'
        # 资源过滤级别: none, low, medium, high
        self.resource_filter_level = resource_filter_level.lower() if isinstance(resource_filter_level, str) else "medium"
        
        # 从环境变量初始化MongoDB连接
        mongo_uri = os.environ.get('MONGO_URI', MONGO_URI)
        db_name = os.environ.get('MONGO_DB', DB_NAME)
        collection_name = os.environ.get('MONGO_COLLECTION_RAW', COLLECTION_NAME)
        
        logger.info(f"MongoDB配置: URI={mongo_uri}, 数据库={db_name}, 集合={collection_name}")
        
        # 初始化MongoDB连接参数
        self.mongo_uri = mongo_uri
        self.mongo_db = db_name
        self.collection_name = collection_name
        
        # MongoDB客户端将在init_db中初始化
        self.client = None
        self.db = None
        self.collection = None
        
        # Playwright资源
        self.playwright = None
        self.browsers = []
        self.contexts = []
        self.pages = []
        
        # 上传者信息
        self.uploader = "单永旭"
        
        # 创建必要的目录
        self.debug_dir = Path("debug")
        self.debug_dir.mkdir(exist_ok=True)
        
        # 设置调试模式
        self.debug_mode = os.environ.get('DEBUG_MODE', '0') == '1'
        if self.debug_mode:
            logger.setLevel(logging.DEBUG)
            logger.debug("调试模式已启用")
    
    async def init_db(self):
        """初始化数据库连接和索引"""
        try:
            # 使用连接池配置初始化MongoDB连接
            self.client = AsyncIOMotorClient(
                self.mongo_uri,
                maxPoolSize=50,  # 设置连接池大小
                minPoolSize=10,  # 最小连接池大小
                maxIdleTimeMS=30000,  # 连接最大空闲时间
                socketTimeoutMS=20000,  # Socket超时时间
                connectTimeoutMS=10000,  # 连接超时时间
                serverSelectionTimeoutMS=10000,  # 服务器选择超时
                waitQueueTimeoutMS=10000,  # 等待队列超时
                retryWrites=True,  # 启用写操作重试
                w="majority",  # 写入确认级别
            )
            
            # 获取数据库和集合引用
            self.db = self.client[self.mongo_db]
            self.collection = self.db[self.collection_name]
            
            # 创建复合唯一索引，确保不同平台的相同job_id可以共存
            # await self.collection.create_index(
            #     [("source", ASCENDING), ("job_id", ASCENDING)],
            #     unique=True,
            #     background=True
            # )
            
            logger.info("数据库连接和索引初始化成功")
            
        except Exception as e:
            logger.error(f"初始化数据库出错: {str(e)}")
            raise
    
    async def init_browser(self):
        """初始化浏览器"""
        try:
            logger.info("开始初始化Playwright...")
            self.playwright = await async_playwright().start()
            logger.info("Playwright启动成功")
            
            for i in range(self.browser_count):
                try:
                    logger.info(f"正在启动浏览器实例 {i+1}/{self.browser_count}...")
                    
                    # 增加更多启动参数
                    browser_args = [
                        '--disable-blink-features=AutomationControlled',
                        '--disable-infobars',
                        '--disable-notifications',
                        '--disable-dev-shm-usage',
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-gpu',
                        '--disable-accelerated-2d-canvas',
                        '--disable-accelerated-jpeg-decoding',
                        '--disable-accelerated-mjpeg-decode',
                        '--disable-accelerated-video-decode',
                        '--disable-features=IsolateOrigins,site-per-process',
                        '--disable-web-security',
                        '--disable-site-isolation-trials',
                        '--ignore-certificate-errors',
                        '--disable-extensions',
                        '--disable-default-apps',
                        '--disable-sync',
                        '--disable-background-timer-throttling',
                        '--disable-backgrounding-occluded-windows',
                        '--disable-renderer-backgrounding',
                        '--disable-background-networking',
                        '--metrics-recording-only',
                        '--disable-prompt-on-repost',
                        '--disable-hang-monitor',
                        '--disable-client-side-phishing-detection',
                        '--disable-component-update',
                        '--disable-breakpad',
                        '--disable-domain-reliability',
                        '--disable-features=TranslateUI',
                        '--disable-speech-api',
                        '--hide-scrollbars',
                        '--mute-audio',
                        '--no-first-run',
                        '--no-default-browser-check',
                        '--no-pings',
                        '--password-store=basic',
                        '--use-mock-keychain',
                        '--force-color-profile=srgb',
                        '--disable-print-preview',
                        f'--window-size={random.choice([1920, 1366, 1536, 1440, 1280])},{random.choice([1080, 768, 864, 900, 720])}',
                        f'--user-agent={random.choice(self.user_agents) if hasattr(self, "user_agents") else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}'
                    ]
                    
                    # 启动浏览器
                    browser = await self.playwright.chromium.launch(
                        headless=self.headless,
                        slow_mo=50,  # 降低操作速度，模拟人类行为
                        args=browser_args
                    )
                    self.browsers.append(browser)
                    logger.info(f"浏览器实例 {i+1} 启动成功")
                    
                    # 创建上下文
                    logger.info(f"正在为浏览器实例 {i+1} 创建上下文...")
                    
                    # 随机化上下文配置
                    context_options = {
                        'viewport': {
                            'width': random.choice([1920, 1366, 1536, 1440, 1280]),
                            'height': random.choice([1080, 768, 864, 900, 720])
                        },
                        'locale': random.choice(['zh-CN', 'zh-TW', 'en-US']),
                        'timezone_id': random.choice([
                            'Asia/Shanghai',
                            'Asia/Hong_Kong',
                            'Asia/Taipei',
                            'Asia/Singapore'
                        ]),
                        'geolocation': {
                            'latitude': random.uniform(22.0, 45.0),
                            'longitude': random.uniform(110.0, 130.0),
                            'accuracy': random.uniform(1, 100)
                        },
                        'permissions': ['geolocation'],
                        'color_scheme': random.choice(['dark', 'light', 'no-preference']),
                        'reduced_motion': random.choice(['reduce', 'no-preference']),
                        'forced_colors': random.choice(['active', 'none']),
                        'device_scale_factor': random.choice([1, 1.25, 1.5, 2]),
                        'is_mobile': False,
                        'has_touch': random.choice([True, False]),
                        'bypass_csp': True,
                        'ignore_https_errors': True,
                        'java_script_enabled': True,
                        'offline': False,
                        'proxy': None  # 如果需要代理，在子类中设置
                    }
                    
                    context = await browser.new_context(**context_options)
                    self.contexts.append(context)
                    
                    # 增强反自动化检测
                    logger.info(f"正在为浏览器实例 {i+1} 添加反自动化检测脚本...")
                    context.add_init_script("""
                    // 隐藏webdriver
                    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                    
                    // 模拟正常浏览器特征
                    window.chrome = {
                        app: {
                            isInstalled: false,
                            InstallState: {
                                DISABLED: 'disabled',
                                INSTALLED: 'installed',
                                NOT_INSTALLED: 'not_installed'
                            },
                            RunningState: {
                                CANNOT_RUN: 'cannot_run',
                                READY_TO_RUN: 'ready_to_run',
                                RUNNING: 'running'
                            }
                        },
                        runtime: {
                            OnInstalledReason: {
                                CHROME_UPDATE: 'chrome_update',
                                INSTALL: 'install',
                                SHARED_MODULE_UPDATE: 'shared_module_update',
                                UPDATE: 'update'
                            },
                            OnRestartRequiredReason: {
                                APP_UPDATE: 'app_update',
                                OS_UPDATE: 'os_update',
                                PERIODIC: 'periodic'
                            },
                            PlatformArch: {
                                ARM: 'arm',
                                ARM64: 'arm64',
                                MIPS: 'mips',
                                MIPS64: 'mips64',
                                X86_32: 'x86-32',
                                X86_64: 'x86-64'
                            },
                            PlatformNaclArch: {
                                ARM: 'arm',
                                MIPS: 'mips',
                                MIPS64: 'mips64',
                                X86_32: 'x86-32',
                                X86_64: 'x86-64'
                            },
                            PlatformOs: {
                                ANDROID: 'android',
                                CROS: 'cros',
                                LINUX: 'linux',
                                MAC: 'mac',
                                OPENBSD: 'openbsd',
                                WIN: 'win'
                            },
                            RequestUpdateCheckStatus: {
                                NO_UPDATE: 'no_update',
                                THROTTLED: 'throttled',
                                UPDATE_AVAILABLE: 'update_available'
                            }
                        }
                    };
                    
                    // 修改navigator属性
                    const originalNavigator = window.navigator;
                    window.navigator = new Proxy(originalNavigator, {
                        has: (target, key) => true,
                        get: (target, key) => {
                            switch (key) {
                                case 'languages':
                                    return ['zh-CN', 'zh', 'en-US', 'en'];
                                case 'plugins':
                                    return [1, 2, 3, 4, 5].map(() => ({
                                        description: 'Chrome PDF Plugin',
                                        filename: 'internal-pdf-viewer',
                                        name: 'Chrome PDF Plugin',
                                        version: '1.0'
                                    }));
                                case 'webdriver':
                                    return undefined;
                                case 'platform':
                                    return 'Win32';
                                case 'hardwareConcurrency':
                                    return 8;
                                case 'deviceMemory':
                                    return 8;
                                case 'userAgent':
                                    return target.userAgent.replace('Headless', '');
                                default:
                                    return target[key];
                            }
                        }
                    });
                    
                    // 添加Canvas指纹
                    const originalGetContext = HTMLCanvasElement.prototype.getContext;
                    HTMLCanvasElement.prototype.getContext = function(contextType, contextAttributes) {
                        const context = originalGetContext.apply(this, arguments);
                        if (contextType === '2d') {
                            const originalGetImageData = context.getImageData;
                            context.getImageData = function() {
                                const imageData = originalGetImageData.apply(this, arguments);
                                // 添加轻微的随机噪声
                                for (let i = 0; i < imageData.data.length; i += 4) {
                                    imageData.data[i] += Math.random() * 2 - 1;
                                    imageData.data[i + 1] += Math.random() * 2 - 1;
                                    imageData.data[i + 2] += Math.random() * 2 - 1;
                                }
                                return imageData;
                            };
                        }
                        return context;
                    };
                    
                    // 添加WebGL指纹
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
                    """)
                    
                    # 创建多个标签页
                    logger.info(f"正在为浏览器实例 {i+1} 创建 {self.tabs_per_browser} 个标签页...")
                    for j in range(self.tabs_per_browser):
                        try:
                            logger.info(f"正在创建标签页 {j+1}/{self.tabs_per_browser}...")
                            page = await context.new_page()
                            
                            # 设置页面属性
                            await page.set_extra_http_headers({
                                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                                'sec-ch-ua-mobile': '?0',
                                'sec-ch-ua-platform': '"Windows"',
                                'sec-fetch-dest': 'document',
                                'sec-fetch-mode': 'navigate',
                                'sec-fetch-site': 'none',
                                'sec-fetch-user': '?1',
                                'upgrade-insecure-requests': '1'
                            })
                            
                            # 添加资源拦截逻辑，拦截图片、字体、视频、音频等不必要的资源请求，以加快网络速度
                            await self.enable_resource_interception(page)
                            
                            self.pages.append(page)
                            logger.info(f"标签页 {j+1} 创建成功")
                        except Exception as e:
                            logger.error(f"创建标签页 {j+1} 失败: {str(e)}")
                            
                except Exception as e:
                    logger.error(f"创建浏览器实例 {i+1} 失败: {str(e)}")
            
            if not self.pages:
                logger.error("没有成功创建任何浏览器页面")
                raise Exception("浏览器页面创建失败")
                
            logger.info(f"浏览器初始化完成: {len(self.browsers)} 个浏览器，共 {len(self.pages)} 个标签页")
            
        except Exception as e:
            logger.error(f"浏览器初始化失败: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
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
            raise
    
    async def close_browser_only(self):
        """只关闭浏览器资源，不关闭数据库连接"""
        try:
            # 先关闭所有页面
            for page in self.pages:
                try:
                    await page.close()
                except Exception as e:
                    logger.error(f"关闭页面时出错: {str(e)}")
            self.pages.clear()
            
            # 关闭所有浏览器上下文
            for context in self.contexts:
                try:
                    await context.close()
                except Exception as e:
                    logger.error(f"关闭浏览器上下文时出错: {str(e)}")
            self.contexts.clear()
            
            # 关闭所有浏览器
            for browser in self.browsers:
                try:
                    await browser.close()
                except Exception as e:
                    logger.error(f"关闭浏览器时出错: {str(e)}")
            self.browsers.clear()
            
            # 关闭 Playwright
            if self.playwright:
                try:
                    await self.playwright.stop()
                except Exception as e:
                    logger.error(f"关闭 Playwright 时出错: {str(e)}")
                self.playwright = None
            
            logger.info("已关闭所有浏览器资源")
            
        except Exception as e:
            logger.error(f"关闭浏览器资源时出错: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

    async def close_browser(self):
        """关闭浏览器和数据库连接"""
        try:
            # 先关闭浏览器资源
            await self.close_browser_only()
            
            # 等待一段时间，确保所有数据都已保存
            await asyncio.sleep(2)
            
            # 最后关闭数据库连接
            await self.close_db()
            
            logger.info("已关闭所有浏览器和数据库连接")
            
        except Exception as e:
            logger.error(f"关闭浏览器和数据库连接时出错: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())    
    
    async def save_to_mongodb(self, jobs: List[Dict], source: str):
        """保存职位信息到MongoDB，支持批量保存和单条保存"""
        if not jobs:
            logger.info("没有数据需要保存")
            return
        
        saved_count = 0
        updated_count = 0
        error_count = 0
        
        try:
            # 检查数据库连接是否有效
            if self.client is None or self.db is None or self.collection is None:
                logger.warning("数据库连接不可用，尝试重新初始化")
                await self.init_db()
            
            # 根据数据量决定使用批量操作还是单条操作
            if len(jobs) > 10:  # 超过10条数据时使用批量操作
                try:
                    # 创建批量操作列表
                    bulk_operations = []
                    for job in jobs:
                        if not job.get('job_id'):  # 跳过没有job_id的数据
                            continue
                        
                        # 添加到批量操作 - 修正格式为正确的pymongo批量操作格式
                        bulk_operations.append(
                            UpdateOne(
                                {"job_id": job['job_id'], "source": source},
                                {"$set": job},
                                upsert=True
                            )
                        )
                    
                    if bulk_operations:
                        # 执行批量操作
                        result = await self.collection.bulk_write(bulk_operations)
                        
                        # 更新计数
                        saved_count = result.upserted_count if hasattr(result, 'upserted_count') else 0
                        updated_count = result.modified_count if hasattr(result, 'modified_count') else 0
                        
                        logger.info(f"[{self.name}] 批量操作成功: 新增 {saved_count} 条，更新 {updated_count} 条 ({source})")
                except Exception as e:
                    logger.error(f"批量操作失败，切换到单条保存: {str(e)}")
                    # 如果批量操作失败，回退到单条保存
                    for job in jobs:
                        await self._save_single_job(job, source)
            else:
                # 数据量少，直接使用单条保存
                for job in jobs:
                    result = await self._save_single_job(job, source)
                    if result == 1:
                        saved_count += 1
                    elif result == 2:
                        updated_count += 1
                    elif result == 0:
                        error_count += 1
            
            logger.info(f"[{self.name}] 总计: 新增 {saved_count} 条，更新 {updated_count} 条，失败 {error_count} 条 ({source})")
            
        except Exception as e:
            logger.error(f"保存到MongoDB失败: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            
            # 重新抛出异常供调用者处理
            raise

    async def _save_single_job(self, job: Dict, source: str) -> int:
        """保存单条职位数据
        
        返回:
            1: 新插入的数据
            2: 更新的数据
            0: 保存失败
        """
        if not job.get('job_id'):  # 跳过没有job_id的数据
            return 0
        
        try:
            # 使用upsert操作，如果存在则更新，不存在则插入
            result = await self.collection.update_one(
                {"job_id": job['job_id'], "source": source},
                {"$set": job},
                upsert=True
            )
            
            if result.upserted_id:  # 新插入的文档
                return 1
            elif result.modified_count > 0:  # 更新的文档
                return 2
            return 0  # 未发生变化
            
        except Exception as e:
            logger.error(f"保存/更新单条文档失败 (job_id: {job.get('job_id')}): {str(e)}")
            return 0
    
    def parse(self, response):
        """Scrapy解析方法"""
        # 基础解析逻辑
        return self._parse_content(response)
    
    def _parse_content(self, response):
        """具体的解析逻辑由子类实现"""
        raise NotImplementedError
        
    async def process_job_type(self, job_type_code: str, page_index: int = 0):
        """处理特定职位类型的通用方法，由子类实现具体逻辑"""
        raise NotImplementedError
    
    async def get_job_list(self, url: str, page: Page) -> List[Dict]:
        """获取职位列表的通用方法，由子类实现具体逻辑"""
        raise NotImplementedError
    
    async def get_job_detail(self, job_data: Dict, page: Page) -> Dict:
        """获取职位详情的通用方法，由子类实现具体逻辑"""
        raise NotImplementedError
    
    def process_job_data(self, job_data: Dict) -> Dict:
        """处理职位数据，转换为数据库格式，由子类实现具体逻辑"""
        raise NotImplementedError
    
    def handle_error(self, failure):
        """统一的错误处理"""
        logger.error(f"爬取失败: {failure}")
    
    def is_banned(self, response):
        """检查是否被反爬，由子类实现具体逻辑"""
        return False
    
    def handle_ban(self, response):
        """处理被反爬的情况，由子类实现具体逻辑"""
        logger.warning("检测到反爬措施，暂停爬取")
        return []
    
    async def enable_resource_interception(self, page: Page):
        """设置资源拦截，加快网页加载速度
        
        参数:
            page: Playwright页面对象
            
        资源过滤级别:
            none: 不过滤任何资源
            low: 只过滤图片和视频
            medium: 过滤图片、视频、字体和大多数CSS
            high: 过滤几乎所有非必要资源，包括分析脚本和广告
        """
        if not self.block_resources or self.resource_filter_level == "none":
            logger.info("资源拦截功能已禁用或设置为不过滤任何资源")
            return
            
        try:
            if self.resource_filter_level in ["low", "medium", "high"]:
                # 所有级别都过滤图片和视频
                await page.route('**/*.{png,jpg,jpeg,gif,webp,svg,ico,mp4,webm,ogg,mp3,wav}', 
                    lambda route, _: route.abort())
                logger.info("已拦截图片和视频资源")
                
            if self.resource_filter_level in ["medium", "high"]:
                # 中高级别过滤字体和大多数CSS
                await page.route('**/*.{ttf,woff,woff2}',
                    lambda route, _: route.abort())
                    
                # 拦截大型CSS文件，只保留关键CSS
                async def handle_css(route, request):
                    if "main" in request.url or "critical" in request.url or "core" in request.url:
                        await route.continue_()
                    else:
                        await route.abort()
                await page.route('**/*.css', handle_css)
                logger.info("已拦截字体和非核心CSS资源")
                
            if self.resource_filter_level == "high":
                # 高级别过滤分析脚本和广告
                await page.route('**/{analy,analytics,stats,tongji,track,baidu,google-analytics,umeng}*.{js,php}',
                    lambda route, _: route.abort())
                    
                # 拦截广告相关资源
                await page.route('**/ad{s,v,vertisements,img}*.*',
                    lambda route, _: route.abort())
                    
                # 拦截社交媒体脚本和其他非必要JS
                await page.route('**/{social,share,connect,facebook,twitter,weibo,weixin}*.js',
                    lambda route, _: route.abort())
                logger.info("已拦截分析脚本、广告和社交媒体资源")
            
            logger.info(f"资源拦截设置完成，当前过滤级别: {self.resource_filter_level}")
        except Exception as e:
            logger.error(f"设置资源拦截失败: {str(e)}")
    
    async def close_db(self):
        """安全关闭数据库连接"""
        try:
            if hasattr(self, 'client') and self.client:
                logger.info("正在关闭数据库连接...")
                self.client.close()
                logger.info("数据库连接已关闭")
        except Exception as e:
            logger.error(f"关闭数据库连接时出错: {str(e)}") 