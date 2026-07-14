#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
账号状态监控脚本
用于查看所有账号的详细状态，包括使用时长、心跳时间等
支持多种监控模式和异常检测
"""

import redis
import json
import time
import argparse
from datetime import datetime, timedelta

def get_account_status(detail=False, machine_id=None):
    """获取所有账号状态"""
    # 连接Redis
    r = redis.Redis(
        host="210.14.140.50",
        port=10308,
        password="TsjklgjJOerigjsrigqoijhklejgqirjgh",
        db=9,
        decode_responses=True
    )
    
    # 获取所有账号
    accounts = r.hgetall('tianyancha_accounts')
    
    if not accounts:
        print("未找到任何账号数据，请先运行账号初始化脚本")
        return
    
    print("=" * 100)
    print("账号状态监控报告")
    print("=" * 100)
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 按机器ID分组
    machine_accounts = {1: [], 2: []}
    
    for username, account_data in accounts.items():
        acc = json.loads(account_data)
        acc_machine_id = acc.get('machine_id', 0)
        if acc_machine_id in machine_accounts:
            machine_accounts[acc_machine_id].append(acc)
    
    # 显示每台机器的账号状态
    machines_to_show = [machine_id] if machine_id else [1, 2]
    
    for mid in machines_to_show:
        if mid not in machine_accounts:
            print(f"机器 {mid} 无账号分配")
            continue
            
        print(f"机器 {mid} 账号状态:")
        print("-" * 60)
        
        if not machine_accounts[mid]:
            print("  无账号分配")
            print()
            continue
        
        # 统计状态
        status_count = {'可用': 0, '使用中': 0, '冷却': 0}
        total_usage = 0
        now = time.time()
        
        # 异常检测
        abnormal_accounts = []
        
        for acc in machine_accounts[mid]:
            status = acc.get('status', '未知')
            status_count[status] = status_count.get(status, 0) + 1
            
            # 计算使用时长
            usage_hours = acc.get('usage_duration', 0) / 3600
            total_usage += usage_hours
            
            # 异常检测
            if status == '使用中':
                # 检查心跳是否超时
                last_heartbeat = acc.get('last_heartbeat', 0)
                if now - last_heartbeat > 30 * 60:  # 30分钟无心跳
                    abnormal_accounts.append(f"{acc['username']} (心跳超时)")
                
                # 检查使用时长是否异常
                if usage_hours > 7:
                    abnormal_accounts.append(f"{acc['username']} (使用时长超限: {usage_hours:.2f}小时)")
            
            elif status == '冷却':
                # 检查冷却时间是否异常
                cooldown_until = acc.get('cooldown_until', 0)
                if cooldown_until > 0 and cooldown_until < now:
                    abnormal_accounts.append(f"{acc['username']} (冷却时间已过)")
            
            # 显示账号详情（仅在详细模式或指定机器时显示）
            if detail or machine_id:
                print(f"  {acc['username']}:")
                print(f"    状态: {status}")
                print(f"    已使用: {usage_hours:.2f}小时")
                print(f"    创建时间: {acc.get('create_time_str', '未知')}")
                
                if status == '使用中':
                    print(f"    开始使用: {acc.get('usage_start_time_str', '未知')}")
                    print(f"    最后心跳: {acc.get('last_heartbeat_str', '未知')}")
                    print(f"    预计结束: {acc.get('cooldown_until_str', '未知')}")
                    
                    # 计算剩余使用时间
                    remaining_hours = 7 - usage_hours
                    if remaining_hours > 0:
                        print(f"    剩余时间: {remaining_hours:.2f}小时")
                    
                elif status == '冷却':
                    print(f"    冷却至: {acc.get('cooldown_until_str', '未知')}")
                    if acc.get('usage_start_time_str') != '未设置':
                        print(f"    上次使用: {acc.get('usage_start_time_str', '未知')}")
                    
                    # 计算剩余冷却时间
                    cooldown_until = acc.get('cooldown_until', 0)
                    if cooldown_until > now:
                        remaining_cooldown = (cooldown_until - now) / 3600
                        print(f"    剩余冷却: {remaining_cooldown:.2f}小时")
                
                print()
        
        # 显示统计信息
        print(f"  统计信息:")
        print(f"    总账号数: {len(machine_accounts[mid])}")
        print(f"    可用: {status_count.get('可用', 0)}个")
        print(f"    使用中: {status_count.get('使用中', 0)}个")
        print(f"    冷却: {status_count.get('冷却', 0)}个")
        print(f"    平均使用时长: {total_usage/len(machine_accounts[mid]):.2f}小时")
        
        # 计算使用效率
        if status_count.get('使用中', 0) > 0:
            efficiency = (status_count.get('使用中', 0) / len(machine_accounts[mid])) * 100
            print(f"    当前使用率: {efficiency:.1f}%")
        
        # 显示异常账号
        if abnormal_accounts:
            print(f"    异常账号: {len(abnormal_accounts)}个")
            for abnormal in abnormal_accounts:
                print(f"      ⚠️  {abnormal}")
        
        print()
    
    # 显示总体统计
    if not machine_id:
        print("总体统计:")
        print("-" * 60)
        total_accounts = len(accounts)
        total_available = sum(1 for acc in accounts.values() 
                             if json.loads(acc).get('status') == '可用')
        total_in_use = sum(1 for acc in accounts.values() 
                          if json.loads(acc).get('status') == '使用中')
        total_cooldown = sum(1 for acc in accounts.values() 
                            if json.loads(acc).get('status') == '冷却')
        
        print(f"总账号数: {total_accounts}")
        print(f"可用账号: {total_available}")
        print(f"使用中账号: {total_in_use}")
        print(f"冷却账号: {total_cooldown}")
        
        # 计算可用性
        if total_accounts > 0:
            availability = (total_available / total_accounts) * 100
            print(f"账号可用率: {availability:.1f}%")
            
            # 计算总体使用效率
            total_efficiency = (total_in_use / total_accounts) * 100
            print(f"总体使用率: {total_efficiency:.1f}%")
    
    print("=" * 100)

def cleanup_stale_accounts(machine_id=None):
    """清理卡住的账号"""
    r = redis.Redis(
        host="210.14.140.50",
        port=10308,
        password="TsjklgjJOerigjsrigqirjgh",
        db=9,
        decode_responses=True
    )
    
    now = time.time()
    accounts = r.hgetall('tianyancha_accounts')
    cleaned_count = 0
    
    for username, account_data in accounts.items():
        acc = json.loads(account_data)
        acc_machine_id = acc.get('machine_id', 0)
        
        # 如果指定了机器ID，只清理该机器的账号
        if machine_id and acc_machine_id != machine_id:
            continue
            
        if acc['status'] == '使用中':
            # 如果心跳时间超过30分钟，认为账号卡住了
            if now - acc.get('last_heartbeat', 0) > 30 * 60:
                acc['status'] = '可用'
                acc['usage_start_time'] = 0
                acc['usage_start_time_str'] = "未设置"
                acc['usage_duration'] = 0
                acc['last_heartbeat'] = 0
                acc['last_heartbeat_str'] = "未设置"
                r.hset('tianyancha_accounts', username, json.dumps(acc))
                cleaned_count += 1
                print(f"清理卡住的账号: {username} (机器{acc_machine_id})")
    
    if cleaned_count > 0:
        print(f"共清理了 {cleaned_count} 个卡住的账号")
    else:
        print("没有发现卡住的账号")

def reset_machine_accounts(machine_id):
    """重置指定机器的所有账号状态"""
    r = redis.Redis(
        host="210.14.140.50",
        port=10308,
        password="TsjklgjJOerigjsrigqirjgh",
        db=9,
        decode_responses=True
    )
    
    accounts = r.hgetall('tianyancha_accounts')
    reset_count = 0
    
    for username, account_data in accounts.items():
        acc = json.loads(account_data)
        if acc.get('machine_id') == machine_id:
            acc['status'] = '可用'
            acc['usage_start_time'] = 0
            acc['usage_start_time_str'] = "未设置"
            acc['usage_duration'] = 0
            acc['last_heartbeat'] = 0
            acc['last_heartbeat_str'] = "未设置"
            acc['cooldown_until'] = 0
            acc['cooldown_until_str'] = "未设置"
            r.hset('tianyancha_accounts', username, json.dumps(acc))
            reset_count += 1
    
    print(f"机器{machine_id}重置了{reset_count}个账号状态")

def get_usage_analysis():
    """获取账号使用情况分析"""
    r = redis.Redis(
        host="210.14.140.50",
        port=10308,
        password="TsjklgjJOerigjsrigqirjgh",
        db=9,
        decode_responses=True
    )
    
    accounts = r.hgetall('tianyancha_accounts')
    
    print("=" * 80)
    print("账号使用情况分析")
    print("=" * 80)
    
    # 按机器分组分析
    for machine_id in [1, 2]:
        machine_accounts = [json.loads(v) for v in accounts.values() 
                           if json.loads(v).get('machine_id') == machine_id]
        
        if not machine_accounts:
            continue
            
        print(f"\n机器 {machine_id} 使用分析:")
        print("-" * 40)
        
        total_usage = sum(acc.get('usage_duration', 0) for acc in machine_accounts)
        avg_usage = total_usage / len(machine_accounts) if machine_accounts else 0
        
        # 使用时长分布
        usage_distribution = {'0-1h': 0, '1-3h': 0, '3-5h': 0, '5-7h': 0, '7h+': 0}
        for acc in machine_accounts:
            hours = acc.get('usage_duration', 0) / 3600
            if hours < 1:
                usage_distribution['0-1h'] += 1
            elif hours < 3:
                usage_distribution['1-3h'] += 1
            elif hours < 5:
                usage_distribution['3-5h'] += 1
            elif hours < 7:
                usage_distribution['5-7h'] += 1
            else:
                usage_distribution['7h+'] += 1
        
        print(f"总账号数: {len(machine_accounts)}")
        print(f"平均使用时长: {avg_usage/3600:.2f}小时")
        print(f"使用时长分布:")
        for range_name, count in usage_distribution.items():
            percentage = (count / len(machine_accounts)) * 100
            print(f"  {range_name}: {count}个 ({percentage:.1f}%)")
    
    print("=" * 80)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='账号状态监控脚本')
    parser.add_argument('--action', choices=['status', 'cleanup', 'reset', 'analysis'], 
                       default='status', help='操作类型')
    parser.add_argument('--detail', action='store_true', help='显示详细账号信息')
    parser.add_argument('--machine-id', type=int, choices=[1, 2], help='指定机器ID')
    
    args = parser.parse_args()
    
    if args.action == 'status':
        get_account_status(detail=args.detail, machine_id=args.machine_id)
    elif args.action == 'cleanup':
        print("清理卡住的账号...")
        cleanup_stale_accounts(machine_id=args.machine_id)
    elif args.action == 'reset':
        if args.machine_id is None:
            print("重置操作需要指定机器ID")
        else:
            confirm = input(f"确定要重置机器{args.machine_id}的所有账号状态吗？(y/N): ")
            if confirm.lower() == 'y':
                reset_machine_accounts(args.machine_id)
            else:
                print("操作已取消")
    elif args.action == 'analysis':
        get_usage_analysis() 