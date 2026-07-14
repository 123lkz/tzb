#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
应届生爬虫 - 使用Playwright实现
"""
import traceback
import asyncio
import json
import logging
import random
import time
import argparse
import os
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import traceback
import pymongo
from dotenv import load_dotenv
import uuid
import urllib.parse

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

from playwright.async_api import Page, async_playwright
from recruitment_spider.spiders.base_spider import BaseSpider
from recruitment_spider.utils.proxy_manager import ProxyManager

# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    # 配置日志，第一个参数是日志器名称，第二个参数是爬虫名称
    logger = get_logger(__name__, "yingjiesheng_spider")
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
    logger.debug("应届生爬虫调试模式已启用")

class YingjieshengSpider(BaseSpider):
    """应届生爬虫，继承自BaseSpider"""
    name = 'yingjiesheng_spider'
    
    def __init__(self, headless: bool = True, browser_count: int = 1, tabs_per_browser: int = 1, city: str = "全国", 
                 block_resources: bool = True, resource_filter_level: str = "medium", *args, **kwargs):
        """初始化爬虫"""
        # 调用父类初始化
        super().__init__(
            headless=headless,
            browser_count=browser_count,
            tabs_per_browser=tabs_per_browser,
            city=city,
            block_resources=block_resources,
            resource_filter_level=resource_filter_level,
            *args, **kwargs
        )
        
        # 应届生特有配置
        self.base_url = "https://q.yingjiesheng.com"
        
        # 基础数据文件路径
        self.job_type_path = Path("recruitment_spider/data/yingjieshengqiuzhiwang/job_type.json")
        self.city_code_path = Path("recruitment_spider/data/yingjieshengqiuzhiwang/city_code.json")
        
        # 爬虫配置
        self.min_delay = random.uniform(1, 3)  # 增加最小等待时间
        self.max_delay = random.uniform(1, 5)  # 增加最大等待时间
        self.max_retry_delay = 15  # 增加最大重试等待时间
        self.request_interval = random.uniform(8, 12)  # 增加请求间隔
        
        # 加载岗位代码
        self.job_codes = self.load_job_codes()
        # 加载城市代码
        self.city_code_map = self.load_city_codes()
        
        self.uploader = "单永旭"

        # 随机设备配置
        self.device_configs = [
            # Windows 设备
            {
                'platform': 'Windows',
                'os_version': random.choice(['10.0', '11.0']),
                'cpu_cores': random.choice([4, 8, 12, 16]),
                'memory': random.choice([8, 16, 32]),
                'screen': random.choice([
                    {'width': 1920, 'height': 1080},
                    {'width': 2560, 'height': 1440},
                    {'width': 1366, 'height': 768}
                ])
            },
            # macOS 设备
            {
                'platform': 'MacIntel',
                'os_version': random.choice(['10.15.7', '11.6.8', '12.6.7']),
                'cpu_cores': random.choice([8, 16, 24, 32]),
                'memory': random.choice([16, 32, 64]),
                'screen': random.choice([
                    {'width': 1440, 'height': 900},
                    {'width': 2560, 'height': 1600},
                    {'width': 3456, 'height': 2234}
                ])
            },
            # Linux 设备
            {
                'platform': 'Linux x86_64',
                'os_version': random.choice(['5.15.0', '6.1.0', '6.5.0']),
                'cpu_cores': random.choice([4, 8, 16, 32]),
                'memory': random.choice([8, 16, 32, 64]),
                'screen': random.choice([
                    {'width': 1920, 'height': 1080},
                    {'width': 2560, 'height': 1440},
                    {'width': 3840, 'height': 2160}
                ])
            },
            # Chrome OS 设备
            {
                'platform': 'CrOS x86_64',
                'os_version': random.choice(['14541.0.0', '14500.0.0', '14469.59.0']),
                'cpu_cores': random.choice([2, 4, 8]),
                'memory': random.choice([4, 8, 16]),
                'screen': random.choice([
                    {'width': 1366, 'height': 768},
                    {'width': 1920, 'height': 1080},
                    {'width': 2256, 'height': 1504}
                ])
            },
            # 高性能工作站
            {
                'platform': 'Windows',
                'os_version': '11.0',
                'cpu_cores': random.choice([32, 64, 128]),
                'memory': random.choice([64, 128, 256]),
                'screen': random.choice([
                    {'width': 3840, 'height': 2160},
                    {'width': 5120, 'height': 2880},
                    {'width': 7680, 'height': 4320}
                ])
            }
        ]

        # 随机语言配置
        self.language_configs = [
            ['zh-CN', 'zh', 'en-US', 'en'],
            ['zh-CN', 'en-US'],
            ['zh-CN', 'zh-TW', 'en-US'],
            ['zh-CN', 'ja', 'en-US'],
            ['zh-CN', 'ko', 'en-US'],
            ['zh-CN', 'zh-HK', 'en-US', 'ja'],
            ['zh-CN', 'zh-SG', 'en-SG', 'ms-MY'],
            ['zh-CN', 'fr-FR', 'en-US', 'de-DE'],
            ['zh-CN', 'ru-RU', 'en-US', 'uk-UA'],
            ['zh-CN', 'es-ES', 'en-US', 'pt-BR']
        ]

        # 随机字体配置
        self.font_configs = [
            ['Arial', 'Helvetica', 'sans-serif'],
            ['Microsoft YaHei', 'SimSun', 'sans-serif'],
            ['PingFang SC', 'Hiragino Sans GB', 'sans-serif'],
            ['Segoe UI', 'Tahoma', 'sans-serif'],
            ['Source Han Sans CN', 'Noto Sans CJK SC', 'sans-serif'],
            ['Roboto', 'Ubuntu', 'Droid Sans', 'sans-serif'],
            ['SF Pro Text', 'SF Pro Display', '-apple-system'],
            ['Inter', 'Helvetica Neue', 'Arial', 'sans-serif'],
            ['Noto Sans SC', 'Noto Sans', 'sans-serif'],
            ['HarmonyOS Sans SC', 'HarmonyOS Sans', 'sans-serif']
        ]

        # 随机 WebGL 配置
        self.webgl_vendors = [
            'Google Inc. (NVIDIA)',
            'Google Inc. (Intel)',
            'Google Inc. (AMD)',
            'Apple Computer, Inc.',
            'Intel Inc.',
            'NVIDIA Corporation',
            'ATI Technologies Inc.',
            'Microsoft Corporation',
            'Qualcomm',
            'ARM',
            'Mesa/X.org',
            'WebKit'
        ]

        self.webgl_renderers = [
            'ANGLE (NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0)',
            'ANGLE (Intel(R) UHD Graphics 630 Direct3D11 vs_5_0)',
            'ANGLE (AMD Radeon RX 6800 XT Direct3D11 vs_5_0)',
            'Apple M1 Pro',
            'Intel Iris OpenGL Engine',
            'NVIDIA GeForce GPU',
            'ANGLE (NVIDIA GeForce RTX 4090 Direct3D12 vs_6_7)',
            'ANGLE (AMD Radeon RX 7900 XTX Direct3D12 vs_6_7)',
            'ANGLE (Intel Arc A770 Direct3D12 vs_6_7)',
            'Apple M2 Ultra',
            'Mesa DRI Intel(R) UHD Graphics (ADL GT2)',
            'Qualcomm Adreno 740'
        ]

        # 随机媒体编解码器配置
        self.codec_configs = [
            ['audio/ogg; codecs="vorbis"', 'audio/mpeg', 'audio/aac'],
            ['video/mp4; codecs="avc1.42E01E"', 'video/webm; codecs="vp8"'],
            ['application/x-mpegURL', 'application/dash+xml'],
            ['audio/wav', 'audio/flac', 'audio/opus'],
            ['video/mp4; codecs="hevc"', 'video/webm; codecs="vp9"'],
            ['video/mp4; codecs="av01"', 'video/webm; codecs="vp9.2"'],
            ['audio/webm; codecs="opus"', 'audio/mp4; codecs="mp4a.40.2"'],
            ['video/x-matroska; codecs="avc1.42E01E"']
        ]

        # 随机电池状态
        self.battery_configs = [
            {'charging': True, 'level': random.uniform(0.8, 1.0)},
            {'charging': False, 'level': random.uniform(0.2, 0.9)},
            {'charging': True, 'level': random.uniform(0.95, 1.0), 'chargingTime': 0, 'dischargingTime': None},
            {'charging': False, 'level': random.uniform(0.1, 0.3), 'chargingTime': None, 'dischargingTime': 3600},
            {'charging': True, 'level': random.uniform(0.4, 0.7), 'chargingTime': 1800, 'dischargingTime': None},
            None  # 某些设备可能不支持电池API
        ]

        # 随机网络配置
        self.network_configs = [
            {'type': '4g', 'downlink': random.uniform(5, 15), 'rtt': random.randint(50, 100)},
            {'type': '5g', 'downlink': random.uniform(20, 100), 'rtt': random.randint(10, 30)},
            {'type': 'wifi', 'downlink': random.uniform(10, 50), 'rtt': random.randint(20, 50)},
            {'type': 'ethernet', 'downlink': random.uniform(50, 1000), 'rtt': random.randint(1, 10)},
            {'type': '3g', 'downlink': random.uniform(1, 4), 'rtt': random.randint(100, 200)},
            {'type': 'slow-2g', 'downlink': random.uniform(0.1, 0.5), 'rtt': random.randint(300, 500)},
            {'type': 'wifi', 'downlink': random.uniform(100, 500), 'rtt': random.randint(5, 15), 'saveData': True},
            {'type': '5g', 'downlink': random.uniform(200, 1000), 'rtt': random.randint(1, 5), 'saveData': False}
        ]

        # 随机时区配置
        self.timezone_configs = [
            'Asia/Shanghai',
            'Asia/Hong_Kong',
            'Asia/Taipei',
            'Asia/Tokyo',
            'Asia/Seoul',
            'Asia/Singapore',
            'Europe/London',
            'America/New_York',
            'Australia/Sydney',
            'Pacific/Auckland',
            'Europe/Paris',
            'America/Los_Angeles',
            'Asia/Dubai',
            'Europe/Moscow',
            'America/Sao_Paulo'
        ]

        # 多组User-Agent配置
        self.user_agents = [
            # 桌面端Chrome
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            # 桌面端Firefox
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
            # 桌面端Edge
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36",
            # 移动端
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.0.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            # 新增配置 - 桌面端 Chrome 最新版
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            # 新增配置 - Firefox 最新版
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0",
            # 新增配置 - Edge 最新版
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
            # 新增配置 - Opera
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0",
            # 新增配置 - Safari
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15",
            # 新增配置 - 移动端最新版
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
            # 新增配置 - 平板设备
            "Mozilla/5.0 (iPad; CPU OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 14; SM-X900) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            # 新增配置 - 其他浏览器
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Brave/1.62.153",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Vivaldi/6.5.3206.63"
        ]

        # 多组浏览器启动参数配置
        self.browser_configs = [
            # 配置1：最小化配置
            {
                'args': [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-javascript',
                    '--disable-gpu'
                ]
            },
            # 配置2：模拟普通用户配置
            {
                'args': [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-gpu',
                    '--disable-extensions',
                    '--disable-sync',
                    '--disable-translate',
                    '--metrics-recording-only',
                    '--mute-audio',
                    '--no-first-run',
                    '--safebrowsing-disable-auto-update'
                ]
            },
            # 配置3：高级用户配置
            {
                'args': [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-gpu',
                    '--disable-extensions',
                    '--disable-background-networking',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-breakpad',
                    '--disable-client-side-phishing-detection',
                    '--disable-component-update',
                    '--disable-default-apps',
                    '--disable-dev-shm-usage',
                    '--disable-domain-reliability',
                    '--disable-hang-monitor',
                    '--disable-ipc-flooding-protection',
                    '--disable-popup-blocking',
                    '--disable-prompt-on-repost',
                    '--disable-renderer-backgrounding',
                    '--disable-sync',
                    '--disable-translate',
                    '--metrics-recording-only',
                    '--no-first-run',
                    '--safebrowsing-disable-auto-update',
                    '--enable-automation',
                    '--password-store=basic',
                    '--use-mock-keychain'
                ]
            },
            # 配置4：性能优化配置
            {
                'args': [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-gpu',
                    '--disable-extensions',
                    '--disable-software-rasterizer',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--disable-accelerated-jpeg-decoding',
                    '--disable-accelerated-mjpeg-decode',
                    '--disable-accelerated-video-decode',
                    '--disable-gpu-compositing',
                    '--disable-gpu-memory-buffer-compositor-resources',
                    '--disable-gpu-rasterization',
                    '--disable-gpu-vsync',
                    '--ignore-gpu-blocklist',
                    '--enable-zero-copy',
                    '--enable-gpu-rasterization',
                    '--enable-native-gpu-memory-buffers'
                ]
            },
            # 配置5：安全性配置
            {
                'args': [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-gpu',
                    '--disable-extensions',
                    '--disable-background-networking',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-breakpad',
                    '--disable-client-side-phishing-detection',
                    '--disable-default-apps',
                    '--disable-dev-shm-usage',
                    '--disable-domain-reliability',
                    '--disable-features=IsolateOrigins,site-per-process',
                    '--disable-hang-monitor',
                    '--disable-ipc-flooding-protection',
                    '--disable-popup-blocking',
                    '--disable-prompt-on-repost',
                    '--disable-renderer-backgrounding',
                    '--disable-sync',
                    '--disable-translate',
                    '--disable-web-security',
                    '--disable-webgl',
                    '--disable-xss-auditor',
                    '--no-experiments',
                    '--no-first-run',
                    '--no-default-browser-check'
                ]
            },
            # 配置6：移动设备模拟配置
            {
                'args': [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-gpu',
                    '--disable-extensions',
                    '--enable-features=NetworkService,NetworkServiceInProcess',
                    '--force-color-profile=srgb',
                    '--force-device-scale-factor=2',
                    '--force-raster-color-profile=srgb',
                    '--enable-viewport',
                    '--enable-features=TouchEventFeatureDetection',
                    '--enable-touch-drag-drop',
                    '--enable-touchpad-three-finger-click',
                    '--touch-events=enabled'
                ]
            },
            # 配置7：内存优化配置
            {
                'args': [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-gpu',
                    '--disable-extensions',
                    '--disable-software-rasterizer',
                    '--disable-dev-shm-usage',
                    '--single-process',
                    '--process-per-site',
                    '--renderer-process-limit=1',
                    '--disable-remote-fonts',
                    '--disable-remote-playback-api',
                    '--js-flags="--max-old-space-size=512"'
                ]
            }
        ]

        # 多组请求头配置
        self.header_configs = [
            # 配置1：模拟移动端
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                'Connection': 'keep-alive',
                'User-Agent': random.choice([ua for ua in self.user_agents if 'Mobile' in ua]),
                'X-Requested-With': 'XMLHttpRequest',
                'Sec-Ch-Ua-Platform': '"Android"',
                'Sec-Ch-Ua-Mobile': '?1'
            },
            # 配置2：模拟普通PC浏览器
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'DNT': '1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': random.choice([ua for ua in self.user_agents if 'Windows' in ua]),
                'Sec-Ch-Ua': '"Chromium";v="120", "Google Chrome";v="120"',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Ch-Ua-Mobile': '?0'
            },
            # 配置3：模拟curl
            {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'User-Agent': 'curl/7.88.1',
                'Connection': 'keep-alive'
            },
            # 配置4：模拟Safari浏览器
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-cn',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-Mode': 'navigate'
            },
            # 配置5：模拟Firefox浏览器
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                'DNT': '1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': random.choice([ua for ua in self.user_agents if 'Firefox' in ua]),
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1'
            },
            # 配置6：模拟iPhone Safari
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9,en-US;q=0.8',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1',
                'Sec-Ch-Ua-Platform': '"iOS"',
                'Sec-Ch-Ua-Mobile': '?1',
                'Sec-Ch-Ua-Platform-Version': '"17.3.1"'
            },
            # 配置7：模拟Edge浏览器
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
                'Sec-Ch-Ua': '"Microsoft Edge";v="120", "Chromium";v="120"',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Ch-Ua-Mobile': '?0'
            },
            # 配置8：模拟iPad
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1',
                'Sec-Ch-Ua-Platform': '"iPadOS"',
                'Sec-Ch-Ua-Mobile': '?1',
                'Viewport-Width': '1024'
            },
            # 配置9：模拟Chrome最新版本（Windows）
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Sec-Ch-Ua': '"Chromium";v="122", "Google Chrome";v="122"',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Ch-Ua-Mobile': '?0'
            },
            # 配置10：模拟Chrome最新版本（macOS）
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Sec-Ch-Ua': '"Chromium";v="122", "Google Chrome";v="122"',
                'Sec-Ch-Ua-Platform': '"macOS"',
                'Sec-Ch-Ua-Mobile': '?0'
            },
            # 配置11：模拟Android Chrome
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
                'Sec-Ch-Ua': '"Chromium";v="122", "Google Chrome";v="122"',
                'Sec-Ch-Ua-Platform': '"Android"',
                'Sec-Ch-Ua-Mobile': '?1',
                'Sec-Ch-Ua-Platform-Version': '"14.0.0"'
            },
            # 配置12：模拟 Samsung Galaxy S23 Ultra
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
                'Sec-Ch-Ua': '"Chromium";v="122", "Google Chrome";v="122"',
                'Sec-Ch-Ua-Platform': '"Android"',
                'Sec-Ch-Ua-Mobile': '?1',
                'Sec-Ch-Ua-Platform-Version': '"13.0.0"',
                'Viewport-Width': '412'
            },
            # 配置13：模拟 Opera 浏览器
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0',
                'Sec-Ch-Ua': '"Opera";v="108", "Chromium";v="122"',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Ch-Ua-Mobile': '?0'
            },
            # 配置14：模拟 Safari on macOS Sonoma
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Dest': 'document'
            },
            # 配置15：模拟 Brave 浏览器
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Brave/122.0.0.0',
                'Sec-Ch-Ua': '"Brave";v="122", "Chromium";v="122"',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Ch-Ua-Mobile': '?0'
            },
            # 配置16：模拟 Xiaomi 13 Pro
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 13; 2210132C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
                'Sec-Ch-Ua': '"Chromium";v="122", "Google Chrome";v="122"',
                'Sec-Ch-Ua-Platform': '"Android"',
                'Sec-Ch-Ua-Mobile': '?1',
                'Sec-Ch-Ua-Platform-Version': '"13.0.0"'
            },
            # 配置17：模拟 Firefox on Linux
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'DNT': '1'
            },
            # 配置18：模拟 Chrome on Chrome OS
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Sec-Ch-Ua': '"Chromium";v="122", "Google Chrome";v="122"',
                'Sec-Ch-Ua-Platform': '"Chrome OS"',
                'Sec-Ch-Ua-Mobile': '?0'
            },
            # 配置19：模拟 Huawei P60 Pro
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 13; ART-AL00x) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
                'Sec-Ch-Ua': '"Chromium";v="122", "Google Chrome";v="122"',
                'Sec-Ch-Ua-Platform': '"Android"',
                'Sec-Ch-Ua-Mobile': '?1',
                'Sec-Ch-Ua-Platform-Version': '"13.0.0"'
            },
            # 配置20：模拟 Microsoft Edge on macOS
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
                'Sec-Ch-Ua': '"Microsoft Edge";v="122", "Chromium";v="122"',
                'Sec-Ch-Ua-Platform': '"macOS"',
                'Sec-Ch-Ua-Mobile': '?0'
            },
            # 配置21：模拟 Vivaldi 浏览器
            {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Vivaldi/6.5.3206.63',
                'Sec-Ch-Ua': '"Vivaldi";v="6.5", "Chromium";v="122"',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Ch-Ua-Mobile': '?0'
            }
        ]
        
        # 随机选择设备配置
        selected_device = random.choice(self.device_configs)
        
        # 浏览器配置
        self.browser_args = random.choice(self.browser_configs)['args']
        
        # 浏览器上下文配置
        self.context_options = {
            'java_script_enabled': True,  # 启用 JavaScript 以注入指纹
            'bypass_csp': True,  # 绕过内容安全策略
            'ignore_https_errors': True,  # 忽略 HTTPS 错误
            'user_agent': random.choice(self.user_agents),  # 随机选择 User-Agent
            'viewport': selected_device['screen'],  # 使用随机设备的屏幕尺寸
            'locale': random.choice(['zh-CN', 'en-US', 'zh-TW']),
            'timezone_id': random.choice(self.timezone_configs),
            'color_scheme': random.choice(['dark', 'light', 'no-preference']),
            'reduced_motion': random.choice(['reduce', 'no-preference']),
            'forced_colors': random.choice(['active', 'none']),
            'device_scale_factor': random.choice([1, 1.25, 1.5, 2]),
            'is_mobile': False,
            'has_touch': random.choice([True, False]),
            'extra_http_headers': random.choice(self.header_configs)  # 随机选择请求头配置
        }

        # 保存浏览器指纹配置，用于后续注入
        self.fingerprint_config = {
            'languages': random.choice(self.language_configs),
            'fonts': random.choice(self.font_configs),
            'audio': random.choice(self.codec_configs),
            'video': random.choice(self.codec_configs),
            'webgl_vendor': random.choice(self.webgl_vendors),
            'webgl_renderer': random.choice(self.webgl_renderers),
            'platform': selected_device['platform'],
            'hardware_concurrency': selected_device['cpu_cores'],
            'device_memory': selected_device['memory'],
            'battery': random.choice(self.battery_configs),
            'network': random.choice(self.network_configs)
        }
        
    
    def load_city_codes(self) -> Dict:
        """从JSON文件中加载城市代码映射"""
        # 默认的城市代码映射
        default_city_codes = {
            "北京": "010000",
            "上海": "020000",
            "广州": "030200",
            "深圳": "040000",
            "全国": "000000"
        }
            
        try:                        
            # 加载城市代码文件
            with open(self.city_code_path, 'r', encoding='utf-8') as f:
                city_codes = json.load(f)
                
            if not city_codes:
                logger.warning("城市代码数据为空，使用默认值")
                return default_city_codes
                
            logger.info(f"成功加载 {len(city_codes)} 个城市代码")
            return city_codes
            
        except Exception as e:
            logger.error(f"加载城市代码失败: {str(e)}")
            return default_city_codes
    
    def load_job_codes(self) -> List[Dict]:
        """从JSON文件中加载职位代码"""
        try:
            # 加载职位类型数据
            job_types_path = str(self.job_type_path)
            
            try:
                with open(job_types_path, 'r', encoding='utf-8') as f:
                    job_types = json.load(f)
            except Exception as e:
                logger.error(f"加载JSON文件失败: {str(e)}")
                return []
            
            if not job_types:
                logger.error("职位类型数据为空")
                return []
            
            # 获取第三级职位
            third_level_jobs = []
            for first_level in job_types.get('items', []):
                for second_level in first_level.get('items', []):
                    for third_level in second_level.get('items', []):
                        third_level_jobs.append({
                            'code': third_level.get('code', ''),
                            'value': third_level.get('value', '')
                        })
            
            logger.info(f"成功加载 {len(third_level_jobs)} 个第三级职位代码")
            return third_level_jobs
        
        except Exception as e:
            logger.error(f"加载职位代码失败: {str(e)}")
            return []
    
    
    async def process_job_type(self, job_code: Dict, page_index: int = 0):
        """处理单个职位类型"""
        try:
            job_name = job_code.get("name", "")
            if not job_name:
                job_name = job_code.get("value", "")
            
            logger.info(f"开始处理职位类型: {job_name}")
            # 构建搜索URL
            page = self.pages[page_index]
            url = self._build_search_url(job_code)
            # 获取职位列表
            job_list = await self.get_job_list(url, page)
            
            if not job_list:
                logger.warning(f"未找到职位或获取职位列表失败: {job_name}")
                return 0  # 返回0表示没有处理任何职位
            
            logger.info(f"找到 {len(job_list)} 个职位")
            
            # 保存职位数据
            processed_jobs = [self.process_job_data(job) for job in job_list]                        
            # 使用基类的方法保存到MongoDB
            await self.save_to_mongodb(processed_jobs, source="yingjiesheng")
        except Exception as e:
            logger.error(f"处理职位类型 {job_code.get('name', '')} 失败: {str(e)}")
            return 0
    
    async def run(self):
        """运行爬虫"""
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
            total_jobs = len(self.job_codes)            
            logger.info(f"总共需要处理 {total_jobs} 个岗位类型")
            
            # 初始化计数器
            completed_jobs = 0
            
            # 处理所有岗位类型
            tasks = []
            for i, job_type_code in enumerate(self.job_codes):
                # 为每个任务分配一个页面
                page_index = i % len(self.pages)
                task = asyncio.create_task(self.process_job_type(job_type_code, page_index))
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
    
    def _build_search_url(self, job_type: Dict) -> str:
        """构建搜索URL"""
        job_name = job_type.get("value", "").replace("/", "%2F")
        job_code = job_type.get("code", "")
        # 处理岗位名称中的特殊字符，只保留基本字符
        job_name_safe = ''.join(char for char in job_name if char.isalnum() or char in ' -')
        job_name_safe = job_name_safe.strip()
        
        # 使用 quote 进行基本的 URL 编码
        # encoded_job_name = quote(job_name_safe)

        # 获取城市代码，默认使用全国
        city_code = self.city_code_map.get(self.city, "000000")
        
        # 构建最简单的 URL 格式
        # https://q.yingjiesheng.com/jobs/search/%E9%94%80%E5%94%AE%E4%B8%93%E5%91%98?keywordType&jobarea=120200&pageCode=home%7Csearch%7Cjobsearchlb&funcCode=A0N7&isFromHomeKW=%E9%94%80%E5%94%AE%E4%B8%93%E5%91%98
        # https://q.yingjiesheng.com/jobs/search/%E9%94%80%E5%94%AE%E4%B8%93%E5%91%98?keywordType=&jobarea=120200&pageCode=home|search|jobsearchlb&funcCode=A0N7&isFromHomeKW=%E9%94%80%E5%94%AE%E4%B8%93%E5%91%98
        url = f"https://q.yingjiesheng.com/jobs/search/{job_name}?keywordType=&jobarea={city_code}&pageCode=home|search|jobsearchlb&funcCode={job_code}&isFromHomeKW={job_name}"        
        logger.info(f"构建搜索URL: {url}")
        return url
        
    async def get_job_list(self, url: str, page: Page) -> List[Dict]:
        """获取职位列表"""
        max_retries = float('inf')  # 无限重试
        retry_count = 0
        retry_interval = 600
        logger.info(f"开始获取职位列表，URL: {url}")

        # 随机选择请求头配置
        headers = random.choice(self.header_configs)
        logger.info(f"为页面设置请求头配置: {headers['User-Agent'][:30]}...")
        await page.set_extra_http_headers(headers)
        
        while retry_count < max_retries:
            try:                                
                # 确保页面是活跃的
                logger.info("确保页面处于活跃状态...")                
                # 检查页面是否已关闭或不可用
                await self._check_page_availability(page, f"获取职位列表 {url}")

                # 为新创建的页面设置请求头
                headers = random.choice(self.header_configs)
                logger.info(f"为页面设置请求头配置: {headers['User-Agent']}")
                await page.set_extra_http_headers(headers)
                # 首先使用curl检查API状态
                logger.info("使用curl.exe检查API状态...")
                api_url = "https://youngapi.yingjiesheng.com/job/search_discovery"
                params = {
                    "version": "2.3.5",
                    "api_key": "xy",
                    "timestamp": str(int(time.time())),
                    "keyword_type": "0"
                }
                
                # 构建API请求URL
                api_check_url = f"{api_url}?{urllib.parse.urlencode(params)}"
                
                # 使用固定通用的请求头配置，而不是随机选择
                # 构建完整的curl命令，使用固定标准请求头
                curl_command = f'''curl.exe -s -i "{api_check_url}" ''' + \
                    '''-H "accept: application/json, text/plain, */*" ''' + \
                    '''-H "accept-encoding: gzip, deflate, br" ''' + \
                    '''-H "accept-language: zh-CN,zh;q=0.9,en;q=0.8" ''' + \
                    '''-H "from-domain: yjs_web" ''' + \
                    '''-H "origin: https://q.yingjiesheng.com" ''' + \
                    '''-H "referer: https://q.yingjiesheng.com/" ''' + \
                    '''-H "sec-ch-ua: \"Chromium\";v=\"122\", \"Google Chrome\";v=\"122\"" ''' + \
                    '''-H "sec-ch-ua-mobile: ?0" ''' + \
                    '''-H "sec-ch-ua-platform: \"Windows\"" ''' + \
                    '''-H "sec-fetch-dest: empty" ''' + \
                    '''-H "sec-fetch-mode: cors" ''' + \
                    '''-H "sec-fetch-site: same-site" ''' + \
                    '''-H "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36" '''
                
                
                
                # 使用curl.exe命令检查API状态                
                process = await asyncio.create_subprocess_shell(
                    curl_command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                response_headers = stdout.decode()

                # 不管curl成功与否，都尝试访问页面
                logger.info(f"正在访问URL: {url}")
                
                # 访问页面时的局部重试逻辑
                goto_retry_count = 0
                goto_max_retries = 5
                goto_success = False
                
                while goto_retry_count < goto_max_retries and not goto_success:
                    try:
                        # 设置较长的超时时间
                        await page.goto(url, timeout=60000, wait_until='load')
                        # 等待页面加载完成
                        await page.wait_for_load_state('load')
                        logger.info("页面成功加载，等待页面内容加载完成...")
                        goto_success = True
                    except Exception as goto_error:
                        goto_retry_count += 1
                        error_msg = str(goto_error)
                        logger.error(f"第 {goto_retry_count}/{goto_max_retries} 次访问页面失败: {error_msg}")                                                
                        
                        if goto_retry_count >= goto_max_retries:
                            logger.error(f"访问页面已重试 {goto_max_retries} 次，仍然失败")
                            # 到达最大重试次数，抛出异常让外层处理
                            raise Exception(f"访问页面 {url} 已重试 {goto_max_retries} 次，仍然失败: {error_msg}")
                        
                        # 等待一段时间后重试
                        retry_wait_time = 10  # 递增等待时间
                        logger.info(f"等待 {retry_wait_time} 秒后重试访问页面...")
                        await asyncio.sleep(retry_wait_time)
                
                # 如果成功加载了页面，继续处理
                if goto_success:
                    # 等待一段时间让页面元素加载完成
                    await asyncio.sleep(random.uniform(1, 3))

                logger.info(f"执行API状态检查，第 {retry_count+1} 次尝试...")
                # 检查响应状态码
                if "HTTP/1.1 405" in response_headers:
                    logger.error("检测到爬虫被ban（API返回405），等待一段时间后重试...")
                    raise Exception("爬虫被ban，需要等待后重试")                                                        
                                
                try:                                
                    # 滚动页面以加载更多内容
                    # 使用更稳定的方式滚动页面
                    try:
                        # 方法1：使用多次小范围滚动
                        for i in range(3):
                            await page.mouse.wheel(0, 300)
                            await asyncio.sleep(0.5)
                        
                        # 方法2：使用键盘滚动作为备选方案
                        # for i in range(5):
                        #     await page.keyboard.press("PageDown")
                        #     await asyncio.sleep(0.5)
                            
                        # 方法3：滚动到页面底部确保所有内容加载
                        # await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        # await asyncio.sleep(1)
                        
                        logger.info("页面滚动完成")
                    except Exception as scroll_error:
                        logger.warning(f"页面滚动过程中出现错误: {str(scroll_error)}，但将继续处理")                    
                    
                    # 再等待一段时间让动态内容加载
                    # await asyncio.sleep(2)
                    
                    # 获取页面内容
                    content = await page.content()
                    
                    # 检查是否成功获取到内容
                    if "search-list-item-wrapper" not in content:
                        logger.warning("未找到职位列表内容，这可能是真的没有数据了")
                        
                        # 检查是否有"暂无符合条件的数据"提示，==>暂无符合条件的职位，建议修改您的筛选条件～
                        if "暂无符合条件的职位" in content or "抱歉没有找到满足您要求的职位" in content:
                            logger.info("确认是真的没有数据")
                            return []
                        
                    logger.info("页面内容已加载，开始解析职位项")
                    
                    # 尝试使用多种选择器来获取职位项
                    job_items = await page.query_selector_all('.search-list-item-wrapper')
                    logger.info(f"找到 {len(job_items)} 个职位项，开始解析...")
                    
                    job_list = []
                    for item in job_items:
                        try:
                            # 提取职位信息
                            title_elem = await item.query_selector('.left-title-name .text-cut')
                            title_text = await title_elem.text_content() if title_elem else ""
                            
                            # 获取链接
                            link_elem = await item.query_selector('xpath=./ancestor::a')
                            link = await link_elem.get_attribute('href') if link_elem else ""
                            
                            # 从链接中提取 job_id
                            job_id = ""
                            if link:
                                job_id_match = re.search(r'jobdetail/(\d+)\.html', link)
                                if job_id_match:
                                    job_id = job_id_match.group(1)
                            
                            # 获取标签信息
                            tags = await item.query_selector_all('.left-tag-item')
                            tag_texts = []
                            for tag in tags:
                                tag_text = await tag.text_content()
                                tag_texts.append(tag_text.strip())
                            
                            # 解析位置、经验、学历
                            location = tag_texts[0] if len(tag_texts) > 0 else ""
                            experience = tag_texts[1] if len(tag_texts) > 1 else ""
                            education = tag_texts[2] if len(tag_texts) > 2 else ""
                            
                            # 获取公司信息
                            company_elem = await item.query_selector('.left-detail-company')
                            company_name = await company_elem.text_content() if company_elem else ""
                            
                            # 获取公司性质
                            company_nature_elem = await item.query_selector('.left-detail-nature')
                            company_nature = await company_nature_elem.text_content() if company_nature_elem else ""
                            
                            # 获取行业
                            industry_elem = await item.query_selector('.left-detail-nature:last-child')
                            industry = await industry_elem.text_content() if industry_elem else ""
                            
                            # 获取薪资
                            salary_elem = await item.query_selector('.right-salary')
                            salary = await salary_elem.text_content() if salary_elem else ""
                            
                            job = {
                                                'job_id': job_id,
                                                'title': title_text.strip(),
                                                'link': link,
                                                'company_name': company_name.strip(),
                                                'salary': salary.strip(),
                                                'location': location.strip(),
                                                'experience': experience.strip(),
                                                'education': education.strip(),
                                                'company_nature': company_nature.strip(),
                                                'company_industry': industry.strip(),
                                                'tags': tag_texts
                            }
                            job_list.append(job)
                                
                        except Exception as e:
                            logger.error(f"解析职位项时出错: {str(e)}")                    
                
                    if not job_list:
                        logger.warning("未找到职位列表")
                        raise Exception("解析到的职位列表为空")
                    
                    logger.info(f"成功解析 {len(job_list)} 个职位")
                    return job_list
                
                except Exception as page_error:
                    logger.error(f"访问或解析页面失败: {str(page_error)}")
                    raise page_error
                
            except Exception as e:
                retry_count += 1
                logger.error(f"第 {retry_count} 次获取职位列表失败: {str(e)}")                                               
                logger.info(f"等待 {retry_interval} 秒后重试...")
                await asyncio.sleep(retry_interval)                
        
        return []

    
    def process_job_data(self, job_data: Dict) -> Dict:
        """处理职位数据，按照数据库模式进行格式化"""
        try:
            # 从职位链接中提取job_id
            job_id = ""
            if "link" in job_data and job_data["link"]:
                # 使用正则表达式从URL中提取job_id
                job_id_match = re.search(r'/jobdetail/(\d+)\.html', job_data["link"])
                if job_id_match:
                    job_id = job_id_match.group(1)
                else:
                    # 如果无法从URL中提取，则生成随机ID
                    job_id = ""
                    logger.warning(f"无法从链接中提取job_id，使用随机生成的ID: {job_id}")
            else:
                # 如果没有链接，生成随机ID
                job_id = ""
                logger.warning(f"职位链接为空，使用随机生成的ID: {job_id}")
            
            source = "yingjiesheng"
            
            # 提取薪资范围
            salary_min, salary_max = 0, 0
            if "salary" in job_data and job_data["salary"]:
                salary_text = job_data["salary"]
                # 尝试提取薪资范围，例如"8千-1万"
                salary_match = re.search(r'(\d+)([千万])-(\d+)([千万])', salary_text)
                if salary_match:
                    min_num = int(salary_match.group(1))
                    min_unit = salary_match.group(2)
                    max_num = int(salary_match.group(3))
                    max_unit = salary_match.group(4)
                    
                    # 转换为元
                    if min_unit == '千':
                        salary_min = min_num * 1000
                    elif min_unit == '万':
                        salary_min = min_num * 10000
                    
                    if max_unit == '千':
                        salary_max = max_num * 1000
                    elif max_unit == '万':
                        salary_max = max_num * 10000
            
            # 提取城市和区域
            city = ""
            district = ""
            if "location" in job_data and job_data["location"]:
                location_parts = job_data["location"].split('-')
                if len(location_parts) >= 1:
                    city = location_parts[0]
                if len(location_parts) >= 2:
                    district = location_parts[1]
            
            # 构建符合数据库模式的数据
            processed_data = {
                "job_id": job_id,
                "title": job_data.get("title", ""),
                "company": job_data.get("company_name", ""),
                "salary": job_data.get("salary", ""),
                "city": city,
                "district": district,
                "experience": job_data.get("experience", ""),
                "education": job_data.get("education", ""),
                "company_type": job_data.get("company_nature", ""),
                "company_size": "",
                "company_industry": job_data.get("company_industry", ""),
                "job_type": "",
                "job_tags": job_data.get("tags", []),
                "job_url": job_data.get("link", ""),
                "hr_name": "",
                "hr_position": "",
                "hr_active": "",
                "publish_time": "",
                "update_time": "",
                "source": source,
                "crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "company_url": "",
                "uploader": "单永旭",
                
                # 添加清洗后的数据字段
                "salary_min": salary_min,
                "salary_max": salary_max,
                "salary_raw": job_data.get("salary", ""),
            }
            
            return processed_data
        except Exception as e:
            logger.error(f"处理职位数据时出错: {str(e)}")
            return job_data

    async def init_browser1(self):
        """初始化浏览器，使用类似 curl 的配置"""
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
            logger.error(f"浏览器初始化失败: {str(e)}")            
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

    async def init_browser(self):
        """初始化浏览器，使用类似 curl 的配置"""
        try:
            logger.info("开始初始化Playwright...")
            self.playwright = await async_playwright().start()
            logger.info("Playwright启动成功")
            
            # 创建浏览器实例
            browser = await self.playwright.chromium.launch(
                headless=False,  # 强制使用无头模式
                args=self.browser_args
            )
            self.browsers = [browser]
            logger.info("浏览器实例创建成功")
            
            # 创建上下文
            context = await browser.new_context(**self.context_options)
            self.contexts = [context]
            logger.info("浏览器上下文创建成功")
            
            # 创建页面
            page = await context.new_page()
            self.pages = [page]
            logger.info("页面创建成功")
            
            # 为新创建的页面设置请求头
            headers = random.choice(self.header_configs)
            logger.info(f"为页面设置请求头配置: {headers['User-Agent']}")
            await page.set_extra_http_headers(headers)
            
            # 注入浏览器指纹模拟脚本
            page.add_init_script(f"""
                // 修改 navigator 属性
                const originalNavigator = window.navigator;
                window.navigator = new Proxy(originalNavigator, {{
                    has: (target, key) => true,
                    get: (target, key) => {{
                        switch (key) {{
                            case 'languages':
                                return {self.fingerprint_config['languages']};
                            case 'platform':
                                return '{self.fingerprint_config['platform']}';
                            case 'hardwareConcurrency':
                                return {self.fingerprint_config['hardware_concurrency']};
                            case 'deviceMemory':
                                return {self.fingerprint_config['device_memory']};
                            case 'userAgent':
                                return target.userAgent.replace('Headless', '');
                            default:
                                return target[key];
                        }}
                    }}
                }});
            """)
            
            logger.info("浏览器指纹模拟脚本注入成功")
            
            # 设置请求拦截
            await page.route("**/*", lambda route: route.continue_(
                headers={
                    "User-Agent": self.context_options['user_agent'],
                    "Accept": "*/*"
                }
            ))
            
            logger.info("浏览器初始化完成")
            
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
# 主函数
async def main():
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
    spider = YingjieshengSpider(
            headless=headless,
            browser_count=browser_count,
            tabs_per_browser=tabs_per_browser,
            city=city,
            resource_filter_level="low"
        )
        
    # 运行爬虫
    await spider.run()

if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main())

