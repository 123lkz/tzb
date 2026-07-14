#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
前程无忧反爬虫配置文件
"""

# 基础配置
BASIC_CONFIG = {
    'headless': False,  # 有头模式，方便调试
    'timeout': 30000,   # 页面加载超时时间（毫秒）
    'delay_range': (3, 6),  # 随机延迟范围（秒）
    'max_retries': 3,   # 最大重试次数
}

# 浏览器指纹配置
FINGERPRINT_CONFIG = {
    'screen_resolutions': [
        {'width': 1920, 'height': 1080},
        {'width': 1366, 'height': 768},
        {'width': 1440, 'height': 900},
        {'width': 1536, 'height': 864},
        {'width': 1280, 'height': 720},
        {'width': 1600, 'height': 900},
    ],
    'color_depths': [24, 32],
    'platforms': ['Win32', 'MacIntel', 'Linux x86_64'],
    'languages': [
        'zh-CN,zh;q=0.9,en;q=0.8',
        'en-US,en;q=0.9',
        'zh-CN,zh;q=0.8,en;q=0.6'
    ],
    'timezones': [
        'Asia/Shanghai',
        'Asia/Hong_Kong',
        'Asia/Tokyo',
        'America/New_York'
    ],
    'user_agents': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
}

# 网络配置
NETWORK_CONFIG = {
    'network_conditions': [
        {'offline': False, 'latency': 20, 'download_throughput': 1024 * 1024, 'upload_throughput': 512 * 1024},
        {'offline': False, 'latency': 50, 'download_throughput': 512 * 1024, 'upload_throughput': 256 * 1024},
        {'offline': False, 'latency': 100, 'download_throughput': 256 * 1024, 'upload_throughput': 128 * 1024},
    ],
    'min_request_interval': 1.0,  # 最小请求间隔（秒）
}

# 代理配置
PROXY_CONFIG = {
    'enabled': False,  # 是否启用代理
    'proxy_list': [
        # 示例代理，实际使用时需要替换为真实代理
        # {'server': 'http://proxy1:port', 'username': 'user1', 'password': 'pass1'},
        # {'server': 'http://proxy2:port', 'username': 'user2', 'password': 'pass2'},
    ],
    'rotation_interval': 50,  # 代理轮换间隔（请求数）
}

# 会话管理配置
SESSION_CONFIG = {
    'max_requests_per_session': 100,  # 每个会话最大请求数
    'max_session_duration': 1800,     # 最大会话时长（秒）
    'auto_rotate': True,              # 是否自动轮换会话
}

# 人类行为模拟配置
HUMAN_BEHAVIOR_CONFIG = {
    'mouse_movement': {
        'enabled': True,
        'min_moves': 2,
        'max_moves': 5,
        'move_interval': (0.1, 0.3),
    },
    'scrolling': {
        'enabled': True,
        'min_scrolls': 1,
        'max_scrolls': 4,
        'scroll_interval': (0.8, 2.0),
        'reverse_probability': 0.3,
        'pause_probability': 0.4,
        'pause_duration': (1.0, 3.0),
    },
    'clicking': {
        'enabled': True,
        'probability': 0.2,
        'click_interval': (0.5, 1.5),
    },
    'keyboard': {
        'enabled': True,
        'probability': 0.1,
        'keys': ['PageDown', 'PageUp', 'Home', 'End', 'ArrowDown', 'ArrowUp'],
        'key_interval': (0.2, 0.8),
    },
}

# 智能延迟配置
DELAY_CONFIG = {
    'search_page': (4, 8),      # 搜索页面延迟范围
    'detail_page': (2, 5),      # 详情页面延迟范围
    'pagination': (1, 3),       # 分页延迟范围
    'normal': (3, 6),           # 普通页面延迟范围
    'variation': (-0.5, 0.5),   # 延迟波动范围
    'extra_delay_probability': 0.1,  # 额外延迟概率
    'extra_delay_range': (2, 5),     # 额外延迟范围
}

# 浏览器启动参数
BROWSER_ARGS = [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-web-security',
    '--disable-extensions',
    '--disable-plugins-discovery',
    '--disable-background-networking',
    '--disable-default-apps',
    '--disable-sync',
    '--disable-translate',
    '--hide-scrollbars',
    '--mute-audio',
    '--no-default-browser-check',
    '--no-pings',
    '--disable-field-trial-config',
    '--disable-ipc-flooding-protection',
    '--disable-background-timer-throttling',
    '--disable-backgrounding-occluded-windows',
    '--disable-renderer-backgrounding',
    '--disable-features=VizDisplayCompositor',
    '--disable-histogram-customizer',
    '--disable-gl-extensions',
    '--disable-composited-antialiasing',
    '--disable-canvas-aa',
    '--disable-3d-apis',
    '--disable-accelerated-layers',
    '--disable-accelerated-plugins',
    '--disable-accelerated-video',
    '--disable-accelerated-2d-canvas',
    '--disable-accelerated-video-decode',
    '--disable-gpu-sandbox',
    '--disable-software-rasterizer',
    # 添加一些更真实的参数
    '--disable-blink-features=AutomationControlled',
    '--disable-features=VizDisplayCompositor',
    '--disable-ipc-flooding-protection',
    '--disable-renderer-backgrounding',
    '--disable-backgrounding-occluded-windows',
    '--disable-background-timer-throttling',
    '--disable-features=TranslateUI',
    '--disable-ipc-flooding-protection',
    '--disable-hang-monitor',
    '--disable-prompt-on-repost',
    '--disable-domain-reliability',
    '--disable-component-extensions-with-background-pages',
    '--disable-default-apps',
    '--disable-sync',
    '--disable-translate',
    '--disable-web-security',
    '--disable-features=VizDisplayCompositor',
    '--disable-ipc-flooding-protection',
    '--disable-renderer-backgrounding',
    '--disable-backgrounding-occluded-windows',
    '--disable-background-timer-throttling',
    '--disable-features=TranslateUI',
    '--disable-ipc-flooding-protection',
    '--disable-hang-monitor',
    '--disable-prompt-on-repost',
    '--disable-domain-reliability',
    '--disable-component-extensions-with-background-pages',
    '--disable-default-apps',
    '--disable-sync',
    '--disable-translate',
    '--disable-web-security',
]

# 请求头配置
HEADERS_CONFIG = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cache-Control': 'max-age=0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'Sec-Ch-Ua-Mobile': '?0',
}

# 验证码检测配置
CAPTCHA_CONFIG = {
    'keywords': [
        '为保证您的正常访问,请进行如下验证',
        '验证码',
        'captcha',
        'verification',
        'security check'
    ],
    'min_content_length': 1000,  # 最小页面内容长度
}

# 日志配置
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file_prefix': 'qcwy_spider_step5',
} 