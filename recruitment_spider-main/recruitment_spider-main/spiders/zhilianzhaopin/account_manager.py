import redis
import json
import time
from datetime import datetime

class AccountManager:
    def __init__(self, host, port, password, db, machine_id=1):
        self.r = redis.Redis(
            host=host,
            port=port,
            password=password,
            db=db,
            decode_responses=True
        )
        self.machine_id = machine_id
        self.logger = self._get_logger()

    def _get_logger(self):
        """获取日志记录器"""
        import logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(f"AccountManager-Machine{self.machine_id}")

    def _format_timestamp(self, timestamp):
        """格式化时间戳为可读字符串"""
        if timestamp == 0:
            return "未设置"
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def init_account_pool(self, account_list, machine_id=None):
        """
        初始化账号池（只需运行一次）
        machine_id: 机器ID，用于分配不同的账号给不同机器
        """
        if machine_id is None:
            machine_id = self.machine_id
            
        # 根据机器ID分配账号（2台机器）
        total_accounts = len(account_list)
        accounts_per_machine = total_accounts // 2  # 2台机器平均分配
        
        start_idx = (machine_id - 1) * accounts_per_machine
        end_idx = start_idx + accounts_per_machine if machine_id < 2 else total_accounts
        
        machine_accounts = account_list[start_idx:end_idx]
        
        self.logger.info(f"机器{machine_id}分配账号: {len(machine_accounts)}个")
        
        for acc in machine_accounts:
            acc_obj = {
                "username": acc[0],
                "password": acc[1],
                "status": "可用",
                "cooldown_until": 0,
                "cooldown_until_str": "未设置",  # 格式化时间
                "machine_id": machine_id,
                "usage_start_time": 0,  # 开始使用时间戳
                "usage_start_time_str": "未设置",  # 格式化时间
                "usage_duration": 0,    # 已使用时长（秒）
                "max_usage_duration": 7 * 3600,  # 最大使用时长（7小时）
                "last_heartbeat": 0,     # 最后心跳时间
                "last_heartbeat_str": "未设置",  # 格式化时间
                "create_time": time.time(),  # 账号创建时间
                "create_time_str": self._format_timestamp(time.time())  # 格式化创建时间
            }
            self.r.hset('tianyancha_accounts', acc[0], json.dumps(acc_obj))
        
        self.logger.info(f"机器{machine_id}账号池初始化完成！")

    def get_available_account(self):
        """
        获取一个可用账号，支持中断恢复
        """
        now = time.time()
        accounts = self.r.hgetall('tianyancha_accounts')
        
        # 只获取本机器的账号
        machine_accounts = []
        for k, v in accounts.items():
            acc = json.loads(v)
            if acc.get('machine_id') == self.machine_id:
                machine_accounts.append((k, acc))
        
        self.logger.info(f"机器{self.machine_id}可用账号数量: {len(machine_accounts)}")
        
        # 首先检查并自动解封已冷却完成的账号
        for k, acc in machine_accounts:
            if acc['status'] == '冷却' and acc['cooldown_until'] <= now:
                # 自动解封冷却完成的账号
                acc['status'] = '可用'
                acc['cooldown_until'] = 0
                acc['cooldown_until_str'] = "未设置"
                self.r.hset('tianyancha_accounts', acc['username'], json.dumps(acc))
                self.logger.info(f"机器{self.machine_id}自动解封账号: {acc['username']}")
        
        # 重新获取账号列表（包含刚解封的账号）
        accounts = self.r.hgetall('tianyancha_accounts')
        machine_accounts = []
        for k, v in accounts.items():
            acc = json.loads(v)
            if acc.get('machine_id') == self.machine_id:
                machine_accounts.append((k, acc))
        
        # 优先检查是否有中断恢复的账号
        for k, acc in machine_accounts:
            if acc['status'] == '使用中':
                # 检查使用时长是否超限
                current_usage = acc['usage_duration']  # 直接使用记录的使用时长
                
                if current_usage < acc['max_usage_duration']:
                    # 更新心跳时间，但保持原有使用时长
                    acc['last_heartbeat'] = now
                    acc['last_heartbeat_str'] = self._format_timestamp(now)
                    self.r.hset('tianyancha_accounts', acc['username'], json.dumps(acc))
                    
                    self.logger.info(f"机器{self.machine_id}恢复使用账号: {acc['username']} (已使用: {current_usage/3600:.2f}小时)")
                    return acc
                else:
                    # 使用时长已超限，标记为冷却
                    self.logger.info(f"机器{self.machine_id}账号{acc['username']}使用时长已超限，标记冷却")
                    self.mark_account_cooldown(acc, hours=72)
        
        # 如果没有可恢复的账号，获取新的可用账号
        for k, acc in machine_accounts:
            if acc['status'] == '可用':
                # 设置账号为使用中状态
                acc['status'] = '使用中'
                acc['usage_start_time'] = now
                acc['usage_start_time_str'] = self._format_timestamp(now)
                acc['usage_duration'] = 0
                acc['last_heartbeat'] = now
                acc['last_heartbeat_str'] = self._format_timestamp(now)
                acc['cooldown_until'] = now + acc['max_usage_duration']
                acc['cooldown_until_str'] = self._format_timestamp(now + acc['max_usage_duration'])
                
                self.r.hset('tianyancha_accounts', acc['username'], json.dumps(acc))
                self.logger.info(f"机器{self.machine_id}获取新账号: {acc['username']}")
                return acc
        
        # 如果没有可用账号，显示详细信息
        available_count = sum(1 for k, acc in machine_accounts if acc['status'] == '可用')
        in_use_count = sum(1 for k, acc in machine_accounts if acc['status'] == '使用中')
        cooldown_count = sum(1 for k, acc in machine_accounts if acc['status'] == '冷却')
        
        self.logger.warning(f"机器{self.machine_id}无可用账号 - 可用:{available_count}, 使用中:{in_use_count}, 冷却:{cooldown_count}")
        
        # 显示冷却账号的剩余时间
        for k, acc in machine_accounts:
            if acc['status'] == '冷却':
                remaining_time = acc['cooldown_until'] - now
                if remaining_time > 0:
                    remaining_hours = remaining_time / 3600
                    self.logger.info(f"账号{acc['username']}冷却中，剩余{remaining_hours:.1f}小时")
        
        return None

    def update_account_heartbeat(self, account_info):
        """
        更新账号心跳时间（定期调用，用于跟踪使用时长）
        """
        try:
            now = time.time()
            accounts = self.r.hgetall('tianyancha_accounts')
            
            if account_info['username'] in accounts:
                acc = json.loads(accounts[account_info['username']])
                if acc.get('machine_id') == self.machine_id and acc['status'] == '使用中':
                    # 更新使用时长 - 只在程序运行时累计
                    if acc['usage_start_time'] > 0:
                        # 计算本次心跳间隔的使用时长
                        last_heartbeat = acc.get('last_heartbeat', acc['usage_start_time'])
                        interval_duration = now - last_heartbeat
                        # 累加到总使用时长
                        acc['usage_duration'] = acc.get('usage_duration', 0) + interval_duration
                    
                    acc['last_heartbeat'] = now
                    acc['last_heartbeat_str'] = self._format_timestamp(now)
                    self.r.hset('tianyancha_accounts', acc['username'], json.dumps(acc))
                    
                    # 检查是否超时
                    if acc['usage_duration'] >= acc['max_usage_duration']:
                        self.logger.info(f"账号 {acc['username']} 使用时长已达上限，自动切换")
                        self.mark_account_cooldown(acc, hours=72)
                        return False
                    
                    return True
        except Exception as e:
            self.logger.error(f"更新账号心跳失败: {str(e)}")
        
        return False

    def mark_account_cooldown(self, acc, hours=72):
        """
        标记账号为冷却（用完或被封后调用）
        """
        now = time.time()
        
        acc['status'] = '冷却'
        acc['cooldown_until'] = now + hours*3600
        acc['cooldown_until_str'] = self._format_timestamp(now + hours*3600)
        acc['usage_start_time'] = 0
        acc['usage_start_time_str'] = "未设置"
        acc['usage_duration'] = 0  # 重置使用时长
        acc['last_heartbeat'] = 0
        acc['last_heartbeat_str'] = "未设置"
        self.r.hset('tianyancha_accounts', acc['username'], json.dumps(acc))
        self.logger.info(f"机器{self.machine_id}标记账号{acc['username']}冷却{hours}小时")

    def release_account_lock(self, acc):
        """
        主动释放账号锁（异常退出时兜底用）
        """
        try:
            accounts = self.r.hgetall('tianyancha_accounts')
            if acc['username'] in accounts:
                account_data = json.loads(accounts[acc['username']])
                if account_data.get('machine_id') == self.machine_id:
                    # 保存当前使用时长，以便下次恢复
                    now = time.time()
                    if account_data['usage_start_time'] > 0:
                        account_data['usage_duration'] = now - account_data['usage_start_time'] + account_data.get('usage_duration', 0)
                    
                    account_data['status'] = '可用'  # 重置为可用状态
                    account_data['last_heartbeat'] = 0
                    account_data['last_heartbeat_str'] = "未设置"
                    self.r.hset('tianyancha_accounts', acc['username'], json.dumps(account_data))
                    
                    self.logger.info(f"机器{self.machine_id}释放账号{acc['username']}锁，已使用时长: {account_data['usage_duration']/3600:.2f}小时")
        except Exception as e:
            self.logger.error(f"释放账号锁失败: {str(e)}")

    def unlock_all(self):
        """
        仅测试用，解锁所有账号
        """
        accounts = self.r.hgetall('tianyancha_accounts')
        for k in accounts:
            acc = json.loads(accounts[k])
            if acc.get('machine_id') == self.machine_id:
                acc['status'] = '可用'
                acc['usage_start_time'] = 0
                acc['usage_start_time_str'] = "未设置"
                acc['usage_duration'] = 0
                acc['last_heartbeat'] = 0
                acc['last_heartbeat_str'] = "未设置"
                # 注意：不重置total_usage_duration，保留历史使用记录
                self.r.hset('tianyancha_accounts', k, json.dumps(acc))
        self.logger.info(f"机器{self.machine_id}解锁所有账号")

    def get_machine_accounts_status(self):
        """
        获取本机器账号状态统计
        """
        accounts = self.r.hgetall('tianyancha_accounts')
        machine_accounts = []
        for k, v in accounts.items():
            acc = json.loads(v)
            if acc.get('machine_id') == self.machine_id:
                machine_accounts.append(acc)
        
        available = sum(1 for acc in machine_accounts if acc['status'] == '可用')
        in_use = sum(1 for acc in machine_accounts if acc['status'] == '使用中')
        cooldown = sum(1 for acc in machine_accounts if acc['status'] == '冷却')
        
        # 计算使用时长统计
        total_usage = sum(acc.get('usage_duration', 0) for acc in machine_accounts)
        avg_usage = total_usage / len(machine_accounts) if machine_accounts else 0
        
        self.logger.info(f"机器{self.machine_id}账号状态: 可用{available}个, 使用中{in_use}个, 冷却{cooldown}个")
        self.logger.info(f"机器{self.machine_id}平均使用时长: {avg_usage/3600:.2f}小时")
        
        return {
            'available': available, 
            'in_use': in_use,
            'cooldown': cooldown, 
            'total': len(machine_accounts),
            'avg_usage_hours': avg_usage/3600
        }

    def cleanup_stale_accounts(self):
        """
        清理可能因为程序异常退出而卡在"使用中"状态的账号
        """
        now = time.time()
        accounts = self.r.hgetall('tianyancha_accounts')
        cleaned_count = 0
        
        for k, v in accounts.items():
            acc = json.loads(v)
            if acc.get('machine_id') == self.machine_id and acc['status'] == '使用中':
                # 如果心跳时间超过30分钟，认为账号卡住了
                if now - acc.get('last_heartbeat', 0) > 30 * 60:
                    acc['status'] = '可用'
                    acc['usage_start_time'] = 0
                    acc['usage_start_time_str'] = "未设置"
                    acc['usage_duration'] = 0
                    acc['last_heartbeat'] = 0
                    acc['last_heartbeat_str'] = "未设置"
                    
                    self.r.hset('tianyancha_accounts', k, json.dumps(acc))
                    cleaned_count += 1
                    self.logger.info(f"清理卡住的账号: {k}")
        
        if cleaned_count > 0:
            self.logger.info(f"机器{self.machine_id}清理了{cleaned_count}个卡住的账号")

# 账号列表（只在初始化时用）
accounts = [
    ("18810514438", "pingtai2025"),
    ("18010219955", "pingtai2025"),
    ("13318742095", "pingtai2025"),
    ("15623925177", "pingtai2025"),
    ("15927630121", "pingtai2025"),
    ("13260213962", "pingtai2025"),
    ("13975162012", "pingtai2025"),
    ("13683313420", "pingtai2025"),
    ("19333175551", "pingtai2025"),
    ("18877110802", "pingtai2025"),
    ("17357752424", "pingtai2025"),
    ("15613676198", "pingtai2025"),
    ("15153998651", "pingtai2025"),
    ("18519026350", "pingtai2025"),
    ("15735187239", "pingtai2025"),
    ("13154712841", "pingtai2025"),
    ("17852863187", "pingtai2025"),
    ("15023501653", "pingtai2025"),
    ("16645136331", "pingtai2025"),
    ("15863890060", "pingtai2025"),
    ("13276412835", "pingtai2025"),
    ("15666448289", "pingtai2025"),
    ("18954524883", "pingtai2025"),
    ("17662651990", "pingtai2025"),
    ("13051516351", "pingtai2025"),
    ("13520421072", "pingtai2025"),
    ("15510584955", "pingtai2025")
]

if __name__ == '__main__':
    # 为每台机器初始化账号池
    for machine_id in range(1, 3):
        am = AccountManager(
            host="210.14.140.50",
            port=10308,
            password="TsjklgjJOerigjsrigqoijhklejgqirjgh",
            db=9,
            machine_id=machine_id
        )
        am.init_account_pool(accounts, machine_id)
        print(f"机器{machine_id}账号池初始化完成")
    
    # 显示分配统计
    print("\n=== 账号分配统计 ===")
    total_accounts = len(accounts)
    accounts_per_machine = total_accounts // 2
    print(f"总账号数: {total_accounts}")
    print(f"每台机器账号数: {accounts_per_machine}")
    print(f"机器1: {accounts_per_machine}个账号")
    print(f"机器2: {total_accounts - accounts_per_machine}个账号")
    
    # 计算连续运行时间
    hours_per_account = 7  # 每个账号使用7小时
    print(f"\n=== 连续运行时间计算 ===")
    print(f"每个账号使用时间: {hours_per_account}小时")
    print(f"机器1连续运行: {accounts_per_machine * hours_per_account}小时")
    print(f"机器2连续运行: {(total_accounts - accounts_per_machine) * hours_per_account}小时")
    print(f"是否支持24小时不间断: {'是' if (total_accounts - accounts_per_machine) * hours_per_account >= 24 else '否'}")