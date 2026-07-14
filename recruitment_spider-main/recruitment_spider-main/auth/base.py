from abc import ABC, abstractmethod
import logging

class BaseAuthHelper(ABC):
    """认证助手基类"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def get_auth_info(self):
        """获取认证信息"""
        pass
    
    @abstractmethod
    def refresh_auth(self):
        """刷新认证"""
        pass
    
    @abstractmethod
    def is_valid(self):
        """检查认证是否有效"""
        pass 