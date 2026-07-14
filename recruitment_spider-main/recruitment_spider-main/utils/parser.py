import re
from typing import Tuple, List, Optional

class Parser:
    @staticmethod
    def parse_job_info(html):
        # 解析工作信息的通用方法
        pass 

def extract_salary_range(salary_text: str) -> Tuple[Optional[int], Optional[int]]:
    """
    从薪资文本中提取最低和最高薪资
    
    Args:
        salary_text: 薪资文本，如 "10K-15K·14薪" 或 "10000-15000元/月"
        
    Returns:
        (最低薪资, 最高薪资) 单位为元/月
    """
    if not salary_text:
        return None, None
    
    # 移除所有空格
    salary_text = salary_text.replace(' ', '')
    
    # 尝试匹配 "数字K-数字K" 格式
    k_pattern = re.compile(r'(\d+\.?\d*)K-(\d+\.?\d*)K')
    k_match = k_pattern.search(salary_text)
    if k_match:
        min_salary = float(k_match.group(1)) * 1000
        max_salary = float(k_match.group(2)) * 1000
        return int(min_salary), int(max_salary)
    
    # 尝试匹配 "数字万-数字万" 格式
    wan_pattern = re.compile(r'(\d+\.?\d*)万-(\d+\.?\d*)万')
    wan_match = wan_pattern.search(salary_text)
    if wan_match:
        min_salary = float(wan_match.group(1)) * 10000
        max_salary = float(wan_match.group(2)) * 10000
        return int(min_salary), int(max_salary)
    
    # 尝试匹配 "数字-数字元/月" 格式
    yuan_pattern = re.compile(r'(\d+\.?\d*)-(\d+\.?\d*)元/月')
    yuan_match = yuan_pattern.search(salary_text)
    if yuan_match:
        min_salary = float(yuan_match.group(1))
        max_salary = float(yuan_match.group(2))
        return int(min_salary), int(max_salary)
    
    # 尝试匹配 "数字-数字" 格式
    num_pattern = re.compile(r'(\d+\.?\d*)-(\d+\.?\d*)')
    num_match = num_pattern.search(salary_text)
    if num_match:
        min_salary = float(num_match.group(1))
        max_salary = float(num_match.group(2))
        
        # 判断单位
        if '万' in salary_text:
            min_salary *= 10000
            max_salary *= 10000
        elif 'K' in salary_text or 'k' in salary_text:
            min_salary *= 1000
            max_salary *= 1000
            
        return int(min_salary), int(max_salary)
    
    # 尝试匹配单个数字
    single_pattern = re.compile(r'(\d+\.?\d*)')
    single_match = single_pattern.search(salary_text)
    if single_match:
        salary = float(single_match.group(1))
        
        # 判断单位
        if '万' in salary_text:
            salary *= 10000
        elif 'K' in salary_text or 'k' in salary_text:
            salary *= 1000
            
        return int(salary), int(salary)
    
    return None, None

def extract_location(location_text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    从地点文本中提取城市和区域
    
    Args:
        location_text: 地点文本，如 "北京·朝阳区" 或 "上海"
        
    Returns:
        (城市, 区域)
    """
    if not location_text:
        return None, None
    
    # 移除所有空格
    location_text = location_text.replace(' ', '')
    
    # 尝试匹配 "城市·区域" 格式
    pattern = re.compile(r'(.+?)[·-](.+)')
    match = pattern.search(location_text)
    if match:
        city = match.group(1)
        district = match.group(2)
        return city, district
    
    # 如果没有区域信息，只返回城市
    return location_text, None

def extract_education(text: str) -> Optional[str]:
    """
    从文本中提取学历要求
    
    Args:
        text: 包含学历信息的文本
        
    Returns:
        学历要求
    """
    if not text:
        return None
    
    education_keywords = [
        '博士', '硕士', '研究生', '本科', '大学本科', 
        '大专', '高中', '中专', '初中', '小学', '学历不限'
    ]
    
    for keyword in education_keywords:
        if keyword in text:
            return keyword
    
    return None

def extract_skills(description: str) -> List[str]:
    """
    从职位描述中提取技能要求
    
    Args:
        description: 职位描述文本
        
    Returns:
        技能列表
    """
    if not description:
        return []
    
    # 常见技能关键词
    skill_keywords = [
        'Python', 'Java', 'C++', 'C#', 'JavaScript', 'TypeScript',
        'HTML', 'CSS', 'SQL', 'MySQL', 'MongoDB', 'Redis',
        'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask',
        'Spring', 'SpringBoot', 'Hibernate', 'MyBatis',
        'Docker', 'Kubernetes', 'Linux', 'Git', 'SVN',
        'AWS', 'Azure', 'GCP', 'Alibaba Cloud', 'Tencent Cloud',
        'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy',
        'Hadoop', 'Spark', 'Flink', 'Kafka', 'RabbitMQ',
        'RESTful', 'GraphQL', 'gRPC', 'WebSocket', 'HTTP',
        'Android', 'iOS', 'Flutter', 'React Native', 'Xamarin',
        'Unity', 'Unreal Engine', 'Cocos2d', 'WebGL', 'Three.js'
    ]
    
    found_skills = []
    for skill in skill_keywords:
        # 使用正则表达式匹配整个单词
        pattern = re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE)
        if pattern.search(description):
            found_skills.append(skill)
    
    return found_skills 