#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试账号自动解封功能
"""

import time
from account_manager import AccountManager

def test_account_unlock():
    """测试账号自动解封功能"""
    
    # 创建账号管理器
    am = AccountManager(
        host="210.14.140.50",
        port=10308,
        password="TsjklgjJOerigjsrigqoijhklejgqirjgh",
        db=9,
        machine_id=1
    )
    
    print("=== 测试账号自动解封功能 ===")
    
    # 1. 显示当前账号状态
    print("\n1. 当前账号状态:")
    status = am.get_machine_accounts_status()
    print(f"可用: {status['available']}, 使用中: {status['in_use']}, 冷却: {status['cooldown']}")
    
    # 2. 尝试获取可用账号
    print("\n2. 尝试获取可用账号:")
    account = am.get_available_account()
    if account:
        print(f"获取到账号: {account['username']}")
        print(f"状态: {account['status']}")
        print(f"冷却时间: {account['cooldown_until_str']}")
        
        # 3. 模拟使用账号一段时间后标记冷却
        print(f"\n3. 模拟使用账号 {account['username']} 并标记冷却...")
        am.mark_account_cooldown(account, hours=72)
        print(f"账号 {account['username']} 已标记冷却72小时")
        
        # 4. 再次尝试获取账号（应该失败）
        print("\n4. 再次尝试获取账号（应该失败）:")
        account2 = am.get_available_account()
        if not account2:
            print("✓ 正确：无法获取冷却中的账号")
        else:
            print("✗ 错误：不应该获取到冷却中的账号")
        
        # 5. 显示冷却账号的详细信息
        print("\n5. 冷却账号详细信息:")
        accounts = am.r.hgetall('tianyancha_accounts')
        for k, v in accounts.items():
            acc = am.r.json().loads(v)
            if acc.get('machine_id') == 1 and acc['status'] == '冷却':
                print(f"账号: {acc['username']}")
                print(f"冷却时间: {acc['cooldown_until_str']}")
                print(f"剩余时间: {(acc['cooldown_until'] - time.time()) / 3600:.1f}小时")
    else:
        print("✗ 错误：无法获取任何账号")
    
    # 6. 测试手动解锁所有账号
    print("\n6. 手动解锁所有账号（测试用）:")
    am.unlock_all()
    print("所有账号已解锁")
    
    # 7. 验证解锁结果
    print("\n7. 验证解锁结果:")
    account3 = am.get_available_account()
    if account3:
        print(f"✓ 成功：获取到账号 {account3['username']}")
    else:
        print("✗ 错误：解锁后仍无法获取账号")

if __name__ == "__main__":
    test_account_unlock() 