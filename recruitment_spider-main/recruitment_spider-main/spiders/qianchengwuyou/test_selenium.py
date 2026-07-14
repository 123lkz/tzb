#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试Selenium版本的前程无忧爬虫
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qcwy_spider_step5_selenium import QCWYSpiderStep5Selenium

def test_browser_init():
    """测试浏览器初始化"""
    print("测试浏览器初始化...")
    spider = QCWYSpiderStep5Selenium()
    
    try:
        spider.init_browser()
        print("✓ 浏览器初始化成功")
        
        # 测试访问前程无忧首页
        spider.driver.get("https://www.51job.com/")
        title = spider.driver.title
        print(f"✓ 成功访问前程无忧首页，标题: {title}")
        
        # 测试反爬虫脚本
        spider.execute_anti_detection_script()
        print("✓ 反爬虫脚本执行成功")
        
        # 测试模拟人类行为
        spider.simulate_human_behavior()
        print("✓ 模拟人类行为执行成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        return False
    finally:
        spider.close_browser()

def test_data_extraction():
    """测试数据提取功能"""
    print("\n测试数据提取功能...")
    spider = QCWYSpiderStep5Selenium()
    
    try:
        spider.init_browser()
        
        # 访问一个搜索页面
        test_url = "https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html"
        spider.driver.get(test_url)
        
        # 等待页面加载
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        spider.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.j_joblist')))
        
        # 测试从页面提取数据
        job_data = spider.get_job_data_from_page()
        print(f"✓ 从页面提取到 {len(job_data)} 条职位数据")
        
        if job_data:
            print(f"✓ 第一条数据示例: {job_data[0]}")
        
        return True
        
    except Exception as e:
        print(f"✗ 数据提取测试失败: {str(e)}")
        return False
    finally:
        spider.close_browser()

def test_pagination():
    """测试分页功能"""
    print("\n测试分页功能...")
    spider = QCWYSpiderStep5Selenium()
    
    try:
        spider.init_browser()
        
        # 访问一个搜索页面
        test_url = "https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html"
        spider.driver.get(test_url)
        
        # 检查分页
        has_pagination, max_page = spider.check_pagination_exists()
        print(f"✓ 分页检查: has_pagination={has_pagination}, max_page={max_page}")
        
        if has_pagination:
            # 测试下一页功能
            spider.goto_next_page()
            print("✓ 下一页功能正常")
        
        return True
        
    except Exception as e:
        print(f"✗ 分页测试失败: {str(e)}")
        return False
    finally:
        spider.close_browser()

def main():
    """主测试函数"""
    print("开始测试Selenium版本的前程无忧爬虫...")
    print("=" * 50)
    
    tests = [
        test_browser_init,
        test_data_extraction,
        test_pagination
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
        print("✓ 所有测试通过！Selenium版本爬虫可以正常使用。")
    else:
        print("✗ 部分测试失败，请检查配置和环境。")

if __name__ == "__main__":
    main() 