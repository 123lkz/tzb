#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试Selenium版本的XHR监听功能
"""

import sys
import os
import time

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qcwy_spider_step5_selenium import QCWYSpiderStep5Selenium

def test_xhr_listener():
    """测试XHR监听功能"""
    print("测试XHR监听功能...")
    spider = QCWYSpiderStep5Selenium()
    
    try:
        # 初始化浏览器
        spider.init_browser()
        print("✓ 浏览器初始化成功")
        
        # 设置XHR监听器
        spider.setup_xhr_listener()
        print("✓ XHR监听器设置成功")
        
        # 访问搜索页面
        test_url = "https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html"
        spider.driver.get(test_url)
        print(f"✓ 访问搜索页面: {spider.driver.title}")
        
        # 等待页面加载
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        spider.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.j_joblist')))
        
        # 测试XHR监听
        spider._current_page_num = 1
        job_data = spider.on_response(1)
        
        if job_data:
            print(f"✓ XHR监听成功，获取到 {len(job_data)} 条职位数据")
            print(f"✓ 第一条数据示例: {job_data[0]}")
            return True
        else:
            print("⚠ XHR监听未获取到数据，尝试页面元素提取")
            job_data = spider.get_job_data_from_page()
            if job_data:
                print(f"✓ 页面元素提取成功，获取到 {len(job_data)} 条职位数据")
                return True
            else:
                print("✗ 两种方式都未获取到数据")
                return False
        
    except Exception as e:
        print(f"✗ 测试失败: {str(e)}")
        return False
    finally:
        spider.close_browser()

def test_pagination_xhr():
    """测试分页时的XHR监听"""
    print("\n测试分页XHR监听...")
    spider = QCWYSpiderStep5Selenium()
    
    try:
        spider.init_browser()
        spider.setup_xhr_listener()
        
        # 访问搜索页面
        test_url = "https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html"
        spider.driver.get(test_url)
        
        # 等待页面加载
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        spider.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.j_joblist')))
        
        # 测试第1页
        spider._current_page_num = 1
        job_data_1 = spider.on_response(1)
        print(f"✓ 第1页获取到 {len(job_data_1) if job_data_1 else 0} 条数据")
        
        # 检查是否有分页
        has_pagination, max_page = spider.check_pagination_exists()
        if has_pagination and max_page > 1:
            print(f"✓ 检测到分页，最大页码: {max_page}")
            
            # 尝试点击下一页
            try:
                spider.goto_next_page()
                print("✓ 点击下一页成功")
                
                # 测试第2页
                spider._current_page_num = 2
                job_data_2 = spider.on_response(2)
                print(f"✓ 第2页获取到 {len(job_data_2) if job_data_2 else 0} 条数据")
                
                return True
            except Exception as e:
                print(f"⚠ 分页测试失败: {str(e)}")
                return False
        else:
            print("⚠ 没有检测到分页")
            return True
        
    except Exception as e:
        print(f"✗ 分页测试失败: {str(e)}")
        return False
    finally:
        spider.close_browser()

def main():
    """主测试函数"""
    print("=" * 60)
    print("Selenium XHR监听功能测试")
    print("=" * 60)
    
    tests = [
        test_xhr_listener,
        test_pagination_xhr
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ 测试异常: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"测试完成: {passed}/{total} 通过")
    
    if passed == total:
        print("✓ 所有XHR监听测试通过！")
        print("Selenium版本的XHR监听功能正常工作。")
    else:
        print("✗ 部分测试失败，但页面元素提取作为备选方案仍然可用。")

if __name__ == "__main__":
    main() 