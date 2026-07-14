#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Selenium版本前程无忧爬虫运行示例
"""

from qcwy_spider_step5_selenium import QCWYSpiderStep5Selenium

def main():
    """主函数 - 运行爬虫示例"""
    print("=" * 60)
    print("前程无忧爬虫 - Selenium版本")
    print("=" * 60)
    
    # 创建爬虫实例
    spider = QCWYSpiderStep5Selenium()
    
    try:
        # 运行爬虫
        # 参数说明：
        # enable_pagination=True: 启用分页爬取
        # page_range=(1, 5): 只爬取前5页（用于测试）
        spider.run(enable_pagination=True, page_range=(1, 5))
        
        print("\n爬虫运行完成！")
        
    except KeyboardInterrupt:
        print("\n用户中断爬虫运行")
    except Exception as e:
        print(f"\n爬虫运行出错: {str(e)}")
    finally:
        # 确保浏览器被正确关闭
        spider.close_browser()

if __name__ == "__main__":
    main() 