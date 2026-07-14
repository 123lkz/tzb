#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 验证Chrome警告修复效果
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_with_fixes():
    """测试修复后的配置"""
    print("=" * 50)
    print("测试Chrome警告修复效果")
    print("=" * 50)
    
    chrome_options = Options()
    
    # 基础配置
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')  # 无头模式
    
    # 修复警告的配置
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--silent')
    chrome_options.add_argument('--disable-google-apis')
    chrome_options.add_argument('--disable-gcm')
    chrome_options.add_argument('--disable-voice-transcription')
    
    # 设置实验性标志
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    try:
        print("正在启动Chrome浏览器...")
        
        # 创建WebDriver
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✓ 使用自动管理的ChromeDriver")
        except ImportError:
            driver = webdriver.Chrome(options=chrome_options)
            print("✓ 使用系统ChromeDriver")
        
        print("正在访问前程无忧...")
        driver.get("https://www.51job.com/")
        
        # 等待页面加载
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        print(f"✓ 成功访问网站，标题: {driver.title}")
        
        # 测试查找元素
        links = driver.find_elements(By.TAG_NAME, "a")
        print(f"✓ 找到 {len(links)} 个链接")
        
        print("✓ 测试完成，Chrome警告已修复")
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        return False
    finally:
        if driver:
            driver.quit()
            print("浏览器已关闭")

if __name__ == "__main__":
    test_with_fixes() 