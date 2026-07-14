#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速修复脚本：手动解锁所有账号
"""

import json
import time
from datetime import datetime
import redis

def fix_all_accounts():
    """修复所有账号状态"""
    
    # 连接Redis
    r = redis.Redis(
        host="210.14.140.50",
        port=10308,
        password="TsjklgjJOerigjsrigqoijhklejgqirjgh",
        db=9,
        decode_responses=True
    )
    
    print("=== 开始修复所有账号状态 ===")
    
    # 获取所有账号
    accounts = r.hgetall('tianyancha_accounts')
    print(f"总账号数: {len(accounts)}")
    
    fixed_count = 0
    for username, account_data in accounts.items():
        try:
            acc = json.loads(account_data)
            
            # 检查是否需要修复
            needs_fix = False
            if acc['status'] == '冷却':
                # 检查冷却时间是否已过
                if acc['cooldown_until'] <= time.time():
                    needs_fix = True
                    print(f"账号 {username} 冷却时间已过，自动解封")
            
            if needs_fix:
                # 修复账号状态
                acc['status'] = '可用'
                acc['cooldown_until'] = 0
                acc['cooldown_until_str'] = "未设置"
                acc['usage_start_time'] = 0
                acc['usage_start_time_str'] = "未设置"
                acc['usage_duration'] = 0
                acc['last_heartbeat'] = 0
                acc['last_heartbeat_str'] = "未设置"
                
                # 保存修复后的账号
                r.hset('tianyancha_accounts', username, json.dumps(acc))
                fixed_count += 1
                
        except Exception as e:
            print(f"修复账号 {username} 时出错: {str(e)}")
    
    print(f"\n=== 修复完成 ===")
    print(f"修复了 {fixed_count} 个账号")
    
    # 显示修复后的状态
    print("\n=== 修复后状态 ===")
    accounts = r.hgetall('tianyancha_accounts')
    available = 0
    in_use = 0
    cooldown = 0
    
    for username, account_data in accounts.items():
        acc = json.loads(account_data)
        if acc['status'] == '可用':
            available += 1
        elif acc['status'] == '使用中':
            in_use += 1
        elif acc['status'] == '冷却':
            cooldown += 1
    
    print(f"可用: {available}")
    print(f"使用中: {in_use}")
    print(f"冷却: {cooldown}")
    
    # 按机器ID分组显示
    print("\n=== 按机器分组 ===")
    machine1_available = 0
    machine2_available = 0
    
    for username, account_data in accounts.items():
        acc = json.loads(account_data)
        if acc['status'] == '可用':
            if acc.get('machine_id') == 1:
                machine1_available += 1
            elif acc.get('machine_id') == 2:
                machine2_available += 1
    
    print(f"机器1可用账号: {machine1_available}")
    print(f"机器2可用账号: {machine2_available}")

def force_unlock_all():
    """强制解锁所有账号（紧急情况使用）"""
    
    # 连接Redis
    r = redis.Redis(
        host="210.14.140.50",
        port=10308,
        password="TsjklgjJOerigjsrigqoijhklejgqirjgh",
        db=9,
        decode_responses=True
    )
    
    print("=== 强制解锁所有账号 ===")
    
    # 获取所有账号
    accounts = r.hgetall('tianyancha_accounts')
    unlocked_count = 0
    
    for username, account_data in accounts.items():
        try:
            acc = json.loads(account_data)
            
            # 强制设置为可用状态
            acc['status'] = '可用'
            acc['cooldown_until'] = 0
            acc['cooldown_until_str'] = "未设置"
            acc['usage_start_time'] = 0
            acc['usage_start_time_str'] = "未设置"
            acc['usage_duration'] = 0
            acc['last_heartbeat'] = 0
            acc['last_heartbeat_str'] = "未设置"
            
            # 保存
            r.hset('tianyancha_accounts', username, json.dumps(acc))
            unlocked_count += 1
            print(f"解锁账号: {username}")
            
        except Exception as e:
            print(f"解锁账号 {username} 时出错: {str(e)}")
    
    print(f"\n=== 强制解锁完成 ===")
    print(f"解锁了 {unlocked_count} 个账号")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "force":
        # 强制解锁所有账号
        force_unlock_all()
    else:
        # 正常修复（只修复冷却时间已过的账号）
        fix_all_accounts() 