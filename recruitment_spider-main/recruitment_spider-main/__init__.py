import os
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent.absolute()

# 版本信息
VERSION = '0.1.0'

# 确保能够正确导入项目模块
def setup_environment():
    """设置项目环境"""
    import sys
    sys.path.append(str(ROOT_DIR))
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'config.settings') 