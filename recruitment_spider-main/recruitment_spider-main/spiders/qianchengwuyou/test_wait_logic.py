#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试职位列表等待逻辑
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

def wait_for_page_load(driver, wait, timeout: int = 30) -> bool:
    """
    等待页面加载完成（参考Playwright的networkidle，测试版本）
    :param driver: WebDriver实例
    :param wait: WebDriverWait实例
    :param timeout: 超时时间（秒）
    :return: 是否加载成功
    """
    try:
        # 等待页面基本元素加载
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.j_joblist')))
        
        # 等待网络空闲（类似Playwright的networkidle）
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # 检查是否有职位卡片
                job_cards = driver.find_elements(By.CSS_SELECTOR, '.j_joblist .e')
                if job_cards:
                    # 检查第一个职位卡片是否包含必要信息
                    first_card = job_cards[0]
                    job_name = first_card.find_element(By.CSS_SELECTOR, 'a.jname')
                    if job_name.text.strip():
                        # 如果职位数据已加载，再等待一小段时间确保网络空闲
                        time.sleep(1)
                        logger.info(f"页面加载完成，找到 {len(job_cards)} 个职位")
                        return True
                
                # 检查是否有加载中的提示
                loading_elements = driver.find_elements(By.CSS_SELECTOR, '.loading, .spinner, .el-loading-mask')
                if loading_elements:
                    logger.debug("页面仍在加载中...")
                    time.sleep(1)
                    continue
                
                # 检查是否有"暂无数据"提示
                no_data_elements = driver.find_elements(By.CSS_SELECTOR, '.no-data, .empty, .el-empty')
                if no_data_elements:
                    logger.info("页面显示暂无数据")
                    return True
                
                time.sleep(0.5)
                
            except Exception as e:
                logger.debug(f"等待页面加载时出现异常: {e}")
                time.sleep(0.5)
        
        logger.warning(f"等待页面加载超时（{timeout}秒）")
        return False
        
    except Exception as e:
        logger.error(f"等待页面加载失败: {e}")
        return False

def test_wait_logic():
    """测试等待逻辑"""
    driver = None
    try:
        logger.info("=" * 50)
        logger.info("开始测试职位列表等待逻辑")
        logger.info("=" * 50)
        
        # 创建浏览器驱动
        driver = setup_chrome_driver()
        if not driver:
            logger.error("无法创建浏览器驱动")
            return False
        
        # 创建WebDriverWait
        wait = WebDriverWait(driver, 30)
        
        # 访问前程无忧搜索页面
        logger.info("访问前程无忧搜索页面...")
        test_url = "https://search.51job.com/list/000000,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25BC%2580%25E5%258F%2591,2,1.html"
        driver.get(test_url)
        
        # 测试等待逻辑
        logger.info("开始测试等待逻辑...")
        start_time = time.time()
        
        success = wait_for_page_load(driver, wait, timeout=30)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        if success:
            logger.info(f"✓ 等待逻辑测试成功，耗时 {elapsed_time:.2f} 秒")
            
            # 获取职位数量
            job_cards = driver.find_elements(By.CSS_SELECTOR, '.j_joblist .e')
            logger.info(f"找到 {len(job_cards)} 个职位卡片")
            
            # 显示前几个职位信息
            for i, card in enumerate(job_cards[:3]):
                try:
                    job_name = card.find_element(By.CSS_SELECTOR, 'a.jname').text.strip()
                    company_name = card.find_element(By.CSS_SELECTOR, '.cname a').text.strip()
                    salary = card.find_element(By.CSS_SELECTOR, '.sal').text.strip()
                    logger.info(f"职位 {i+1}: {job_name} | {company_name} | {salary}")
                except Exception as e:
                    logger.warning(f"获取职位 {i+1} 信息失败: {e}")
            
        else:
            logger.error(f"✗ 等待逻辑测试失败，耗时 {elapsed_time:.2f} 秒")
            
            # 检查页面状态
            try:
                # 检查是否有职位列表容器
                job_list = driver.find_elements(By.CSS_SELECTOR, '.j_joblist')
                if job_list:
                    logger.info("找到职位列表容器")
                    
                    # 检查是否有职位卡片
                    job_cards = driver.find_elements(By.CSS_SELECTOR, '.j_joblist .e')
                    logger.info(f"找到 {len(job_cards)} 个职位卡片")
                    
                    # 检查是否有加载提示
                    loading_elements = driver.find_elements(By.CSS_SELECTOR, '.loading, .spinner, .el-loading-mask')
                    if loading_elements:
                        logger.info("页面仍在加载中")
                    
                    # 检查是否有空数据提示
                    no_data_elements = driver.find_elements(By.CSS_SELECTOR, '.no-data, .empty, .el-empty')
                    if no_data_elements:
                        logger.info("页面显示暂无数据")
                        
                else:
                    logger.warning("未找到职位列表容器")
                    
            except Exception as e:
                logger.error(f"检查页面状态失败: {e}")
        
        logger.info("=" * 50)
        logger.info("等待逻辑测试完成！")
        logger.info("=" * 50)
        
        return success
        
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}")
        return False
        
    finally:
        if driver:
            try:
                driver.quit()
                logger.info("浏览器已关闭")
            except:
                pass

def test_page_navigation_with_wait():
    """测试页面导航时的等待逻辑"""
    driver = None
    try:
        logger.info("=" * 50)
        logger.info("开始测试页面导航等待逻辑")
        logger.info("=" * 50)
        
        # 创建浏览器驱动
        driver = setup_chrome_driver()
        if not driver:
            logger.error("无法创建浏览器驱动")
            return False
        
        # 创建WebDriverWait
        wait = WebDriverWait(driver, 30)
        
        # 访问前程无忧搜索页面
        logger.info("访问前程无忧搜索页面...")
        test_url = "https://search.51job.com/list/000000,000000,0000,00,9,99,%25E8%25BD%25AF%25E4%25BB%25B6%25E5%25BC%2580%25E5%258F%2591,2,1.html"
        driver.get(test_url)
        
        # 等待第一页加载
        logger.info("等待第一页加载...")
        if not wait_for_page_load(driver, wait, timeout=30):
            logger.error("第一页加载失败")
            return False
        
        # 尝试点击下一页
        logger.info("尝试点击下一页...")
        try:
            # 查找下一页按钮
            next_btn = None
            next_button_selectors = [
                '.el-pagination .btn-next:not([disabled])',
                '.btn-next:not([disabled])',
                '.pageation .btn-next:not([disabled])'
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
                
                # 等待第二页加载
                logger.info("等待第二页加载...")
                if wait_for_page_load(driver, wait, timeout=15):
                    logger.info("✓ 第二页加载成功")
                    
                    # 获取第二页职位数量
                    job_cards = driver.find_elements(By.CSS_SELECTOR, '.j_joblist .e')
                    logger.info(f"第二页找到 {len(job_cards)} 个职位卡片")
                    
                    return True
                else:
                    logger.error("✗ 第二页加载失败")
                    return False
            else:
                logger.info("未找到可用的下一页按钮")
                return True
                
        except Exception as e:
            logger.error(f"点击下一页失败: {e}")
            return False
        
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}")
        return False
        
    finally:
        if driver:
            try:
                driver.quit()
                logger.info("浏览器已关闭")
            except:
                pass

if __name__ == "__main__":
    # 测试基本等待逻辑
    success1 = test_wait_logic()
    
    # 测试页面导航等待逻辑
    success2 = test_page_navigation_with_wait()
    
    logger.info("=" * 50)
    if success1 and success2:
        logger.info("所有测试都通过了！✓")
    else:
        logger.error("部分测试失败！✗")
    logger.info("=" * 50) 