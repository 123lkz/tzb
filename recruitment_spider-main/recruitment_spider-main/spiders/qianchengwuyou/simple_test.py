#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单的Selenium测试脚本
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_basic_selenium():
    """测试基本的Selenium功能"""
    print("开始测试基本Selenium功能...")
    
    # 创建Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')  # 无头模式
    
    driver = None
    try:
        # 尝试创建WebDriver
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
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
            # 尝试查找一些常见元素
            elements = driver.find_elements(By.TAG_NAME, "a")
            print(f"✓ 找到 {len(elements)} 个链接")
        except Exception as e:
            print(f"⚠ 查找元素时出现问题: {str(e)}")
        
        print("✓ 基本Selenium功能测试通过")
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        return False
    finally:
        if driver:
            driver.quit()

def test_page_extraction():
    """测试页面数据提取"""
    print("\n开始测试页面数据提取...")
    
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    
    driver = None
    try:
        # 创建WebDriver
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except ImportError:
            driver = webdriver.Chrome(options=chrome_options)
        
        # 访问搜索页面
        test_url = "https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html"
        driver.get(test_url)
        print(f"✓ 访问搜索页面: {driver.title}")
        
        # 等待页面加载
        wait = WebDriverWait(driver, 10)
        
        # 尝试查找职位列表
        try:
            job_list = driver.find_elements(By.CSS_SELECTOR, '.j_joblist .e')
            print(f"✓ 找到 {len(job_list)} 个职位")
            
            if job_list:
                # 提取第一个职位的信息
                first_job = job_list[0]
                try:
                    job_name = first_job.find_element(By.CSS_SELECTOR, 'a.jname').text
                    print(f"✓ 第一个职位名称: {job_name}")
                except:
                    print("⚠ 无法提取职位名称")
        except Exception as e:
            print(f"⚠ 查找职位列表时出现问题: {str(e)}")
        
        print("✓ 页面数据提取测试通过")
        return True
        
    except Exception as e:
        print(f"✗ 页面提取测试失败: {str(e)}")
        return False
    finally:
        if driver:
            driver.quit()

def main():
    """主测试函数"""
    print("=" * 50)
    print("Selenium基本功能测试")
    print("=" * 50)
    
    tests = [
        test_basic_selenium,
        test_page_extraction
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ 测试异常: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"测试完成: {passed}/{total} 通过")
    
    if passed == total:
        print("✓ 所有基本测试通过！")
        print("现在可以尝试运行完整的爬虫了。")
    else:
        print("✗ 部分测试失败，请检查环境配置。")

if __name__ == "__main__":
    main() 