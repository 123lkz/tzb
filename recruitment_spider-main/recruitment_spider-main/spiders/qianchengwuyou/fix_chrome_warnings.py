#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复Chrome浏览器警告的配置
"""

def get_chrome_options_with_fixes():
    """获取修复了警告的Chrome选项"""
    from selenium.webdriver.chrome.options import Options
    
    chrome_options = Options()
    
    # 基础配置
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # 修复警告的配置
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--disable-gpu-logging')
    chrome_options.add_argument('--disable-logging-redirect')
    chrome_options.add_argument('--log-level=3')  # 只显示致命错误
    chrome_options.add_argument('--silent')
    chrome_options.add_argument('--disable-background-networking')
    chrome_options.add_argument('--disable-background-timer-throttling')
    chrome_options.add_argument('--disable-backgrounding-occluded-windows')
    chrome_options.add_argument('--disable-renderer-backgrounding')
    chrome_options.add_argument('--disable-features=TranslateUI')
    chrome_options.add_argument('--disable-ipc-flooding-protection')
    chrome_options.add_argument('--disable-default-apps')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-plugins-discovery')
    chrome_options.add_argument('--disable-sync')
    chrome_options.add_argument('--disable-translate')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--mute-audio')
    chrome_options.add_argument('--no-default-browser-check')
    chrome_options.add_argument('--no-pings')
    chrome_options.add_argument('--disable-field-trial-config')
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
    
    # 禁用Google服务
    chrome_options.add_argument('--disable-google-apis')
    chrome_options.add_argument('--disable-gcm')
    chrome_options.add_argument('--disable-voice-transcription')
    
    # 设置实验性标志
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    return chrome_options

def test_fixed_chrome():
    """测试修复后的Chrome配置"""
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    print("测试修复后的Chrome配置...")
    
    try:
        # 获取修复后的选项
        chrome_options = get_chrome_options_with_fixes()
        
        # 创建WebDriver
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✓ 使用自动管理的ChromeDriver")
        except ImportError:
            driver = webdriver.Chrome(options=chrome_options)
            print("✓ 使用系统ChromeDriver")
        
        # 测试访问网页
        driver.get("https://www.51job.com/")
        print(f"✓ 成功访问前程无忧，标题: {driver.title}")
        
        # 等待页面加载
        wait = WebDriverWait(driver, 10)
        
        # 测试查找元素
        try:
            elements = driver.find_elements(By.TAG_NAME, "a")
            print(f"✓ 找到 {len(elements)} 个链接")
        except Exception as e:
            print(f"⚠ 查找元素时出现问题: {str(e)}")
        
        print("✓ 修复后的Chrome配置测试通过")
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        return False
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    test_fixed_chrome() 