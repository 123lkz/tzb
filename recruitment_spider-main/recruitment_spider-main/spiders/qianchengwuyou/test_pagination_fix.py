#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试分页功能修复
"""

import sys
import os
import time
import logging

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_chrome_driver():
    """设置Chrome浏览器"""
    chrome_options = Options()
    
    # 基本设置
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    # 修复Chrome警告
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--silent')
    
    # 设置用户代理
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36')
    
    # 设置窗口大小
    chrome_options.add_argument('--window-size=1280,720')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        logger.error(f"创建Chrome驱动失败: {e}")
        return None

def test_pagination_elements(driver):
    """测试分页元素查找"""
    try:
        logger.info("开始测试分页元素查找...")
        
        # 等待页面加载
        time.sleep(3)
        
        # 测试下一页按钮查找（基于实际HTML结构）
        next_button_selectors = [
            '.el-pagination .btn-next:not([disabled])',  # 主要选择器
            '.btn-next:not([disabled])',                 # 备选选择器
            '.pageation .btn-next:not([disabled])',      # 包含父容器
            '.btn-next'                                  # 最后备选
        ]
        
        logger.info("查找下一页按钮...")
        for selector in next_button_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                logger.info(f"选择器 '{selector}' 找到 {len(elements)} 个元素")
                for i, element in enumerate(elements):
                    try:
                        is_displayed = element.is_displayed()
                        is_enabled = element.is_enabled()
                        text = element.text
                        logger.info(f"  元素 {i+1}: 显示={is_displayed}, 启用={is_enabled}, 文本='{text}'")
                    except:
                        logger.info(f"  元素 {i+1}: 无法获取属性")
            except Exception as e:
                logger.error(f"选择器 '{selector}' 查找失败: {e}")
        
        # 测试跳转输入框查找（基于实际HTML结构）
        jump_input_selectors = [
            '#jump_page',                    # 主要选择器（根据HTML中的id）
            '.pageation #jump_page',         # 包含父容器
            'input[type="number"]',          # 备选选择器
            'input.mytxt'                    # 根据HTML中的class
        ]
        
        logger.info("查找跳转输入框...")
        for selector in jump_input_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                logger.info(f"选择器 '{selector}' 找到 {len(elements)} 个元素")
                for i, element in enumerate(elements):
                    try:
                        is_displayed = element.is_displayed()
                        is_enabled = element.is_enabled()
                        placeholder = element.get_attribute('placeholder')
                        logger.info(f"  元素 {i+1}: 显示={is_displayed}, 启用={is_enabled}, placeholder='{placeholder}'")
                    except:
                        logger.info(f"  元素 {i+1}: 无法获取属性")
            except Exception as e:
                logger.error(f"选择器 '{selector}' 查找失败: {e}")
        
        # 测试跳转按钮查找（基于实际HTML结构）
        jump_button_selectors = [
            '.jumpPage',                     # 主要选择器（根据HTML中的class）
            '.pageation .jumpPage',          # 包含父容器
            'span.jumpPage',                 # 指定元素类型
            'span[data-v-2a7f3c1e].jumpPage' # 包含data属性
        ]
        
        logger.info("查找跳转按钮...")
        for selector in jump_button_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                logger.info(f"选择器 '{selector}' 找到 {len(elements)} 个元素")
                for i, element in enumerate(elements):
                    try:
                        is_displayed = element.is_displayed()
                        is_enabled = element.is_enabled()
                        text = element.text
                        title = element.get_attribute('title')
                        logger.info(f"  元素 {i+1}: 显示={is_displayed}, 启用={is_enabled}, 文本='{text}', title='{title}'")
                    except:
                        logger.info(f"  元素 {i+1}: 无法获取属性")
            except Exception as e:
                logger.error(f"选择器 '{selector}' 查找失败: {e}")
        
        logger.info("分页元素查找测试完成")
        
    except Exception as e:
        logger.error(f"分页元素查找测试失败: {e}")

def test_page_navigation(driver):
    """测试页面导航功能"""
    try:
        logger.info("开始测试页面导航功能...")
        
        # 等待页面加载
        time.sleep(3)
        
        # 获取当前页面信息
        current_url = driver.current_url
        logger.info(f"当前页面URL: {current_url}")
        
        # 尝试点击下一页
        logger.info("尝试点击下一页...")
        try:
            # 查找下一页按钮
            next_btn = None
            next_button_selectors = [
                '.el-pagination .btn-next:not([disabled])',  # 主要选择器
                '.btn-next:not([disabled])',                 # 备选选择器
                '.pageation .btn-next:not([disabled])',      # 包含父容器
                '.btn-next'                                  # 最后备选
            ]
            
            for selector in next_button_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            next_btn = element
                            logger.info(f"找到下一页按钮，使用选择器: {selector}")
                            break
                    if next_btn:
                        break
                except:
                    continue
            
            if next_btn:
                # 滚动到按钮位置
                driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
                time.sleep(1)
                
                # 点击按钮
                next_btn.click()
                logger.info("成功点击下一页按钮")
                
                # 等待页面加载
                time.sleep(3)
                
                # 检查URL是否变化
                new_url = driver.current_url
                if new_url != current_url:
                    logger.info(f"页面已跳转，新URL: {new_url}")
                else:
                    logger.info("URL未变化，可能在同一页面")
                    
            else:
                logger.info("未找到可用的下一页按钮")
                
        except Exception as e:
            logger.error(f"点击下一页失败: {e}")
        
        logger.info("页面导航功能测试完成")
        
    except Exception as e:
        logger.error(f"页面导航功能测试失败: {e}")

def main():
    """主函数"""
    driver = None
    try:
        logger.info("=" * 50)
        logger.info("开始分页功能测试")
        logger.info("=" * 50)
        
        # 创建浏览器驱动
        driver = setup_chrome_driver()
        if not driver:
            logger.error("无法创建浏览器驱动")
            return
        
        # 访问前程无忧搜索页面
        logger.info("访问前程无忧搜索页面...")
        test_url = "https://search.51job.com/list/000000,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25BC%2580%25E5%258F%2591,2,1.html"
        driver.get(test_url)
        
        # 等待页面加载
        time.sleep(5)
        
        # 测试分页元素查找
        test_pagination_elements(driver)
        
        # 测试页面导航功能
        test_page_navigation(driver)
        
        logger.info("=" * 50)
        logger.info("分页功能测试完成！")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}")
        
    finally:
        if driver:
            try:
                driver.quit()
                logger.info("浏览器已关闭")
            except:
                pass

if __name__ == "__main__":
    main() 