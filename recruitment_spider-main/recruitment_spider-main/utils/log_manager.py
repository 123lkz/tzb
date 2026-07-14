#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日志管理模块 - 提供统一的日志配置和管理功能
支持每次运行生成新的日志文件
"""


import os
import logging
from datetime import datetime
from pathlib import Path


class LogManager:
    """日志管理类，提供统一的日志配置和管理功能"""
    
    def __init__(self, project_root=None):
        """
        初始化日志管理器
        
        Args:
            project_root: 项目根目录路径，如果为None则使用环境变量PROJECT_ROOT
        """
        if project_root is None:
            self.project_root = os.environ.get('PROJECT_ROOT', os.getcwd())
        else:
            self.project_root = project_root
            
        # 创建日志目录
        self.logs_dir = os.path.join(self.project_root, "logs")
        Path(self.logs_dir).mkdir(exist_ok=True, parents=True)
        
        # 记录已配置的日志器
        self.configured_loggers = set()
        
    def get_log_file_path(self, spider_name):
        """
        获取日志文件路径，基于爬虫名称和当前时间生成唯一文件名
        
        Args:
            spider_name: 爬虫名称
            
        Returns:
            日志文件的完整路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"{spider_name}_{timestamp}.log"
        return os.path.join(self.logs_dir, log_filename)
    
    def configure_logger(self, logger_name, spider_name=None, level=logging.INFO, console=True):
        """
        配置指定的日志器
        
        Args:
            logger_name: 日志器名称
            spider_name: 爬虫名称，用于生成日志文件名，如果为None则使用logger_name
            level: 日志级别
            console: 是否输出到控制台
            
        Returns:
            配置好的日志器
        """
        # 避免重复配置
        if logger_name in self.configured_loggers:
            return logging.getLogger(logger_name)
            
        # 如果没有提供爬虫名称，使用日志器名称
        if spider_name is None:
            spider_name = logger_name
            
        # 获取或创建日志器
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        
        # 如果已经有处理器，先清除
        if logger.handlers:
            logger.handlers.clear()
            
        # 禁止向上传播日志消息，防止重复输出
        logger.propagate = False
            
        # 创建格式化器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # 添加文件处理器
        log_file_path = self.get_log_file_path(spider_name)
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # 添加控制台处理器
        if console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            
        # 记录已配置的日志器
        self.configured_loggers.add(logger_name)
        logger.info(f"日志配置完成，输出到文件: {log_file_path}")
        
        return logger
    
    def get_logger(self, name, spider_name=None, level=None):
        """
        获取已配置的日志器，如果不存在则进行配置
        
        Args:
            name: 日志器名称
            spider_name: 爬虫名称，用于生成日志文件名
            level: 日志级别，默认为INFO
            
        Returns:
            日志器实例
        """
        if name not in self.configured_loggers:
            if level is None:
                level = logging.INFO
            return self.configure_logger(name, spider_name, level)
        else:
            return logging.getLogger(name)


# 创建默认日志管理器实例
default_log_manager = LogManager()


def get_logger(name, spider_name=None, level=None):
    """
    获取日志器的便捷函数
    
    Args:
        name: 日志器名称
        spider_name: 爬虫名称，用于生成日志文件名
        level: 日志级别，默认为INFO
        
    Returns:
        日志器实例
    """
    return default_log_manager.get_logger(name, spider_name, level)


def configure_root_logger(spider_name="general", level=logging.INFO):
    """
    配置根日志器
    
    Args:
        spider_name: 爬虫名称，用于生成日志文件名
        level: 日志级别
        
    Returns:
        配置好的根日志器
    """
    # 清除之前的配置
    root_logger = logging.getLogger()
    if root_logger.handlers:
        root_logger.handlers.clear()
    
    # 设置日志级别
    root_logger.setLevel(level)
    
    # 获取日志文件路径
    log_file_path = default_log_manager.get_log_file_path(spider_name)
    
    # 创建处理器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # 文件处理器
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    root_logger.info(f"根日志器配置完成，输出到文件: {log_file_path}")
    return root_logger 