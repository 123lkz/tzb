from datetime import datetime
import re
from typing import Dict, Any, Optional, Tuple

class DataCleaner:
    """数据清洗器，作为原始数据到清洗数据的唯一入口"""
    
    def __init__(self):
        self.salary_pattern = re.compile(r'(\d+)[K千k]?-(\d+)[K千k]?')
    
    def clean_job_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        清洗职位数据的主入口函数
        
        Args:
            raw_data: 原始职位数据
            
        Returns:
            清洗后的标准化数据
        """
        try:
            # 1. 基础字段清洗
            clean_data = {
                # 统一ID
                'unified_job_id': self._generate_unified_id(raw_data),
                
                # 基础信息清洗
                'title': self._clean_title(raw_data.get('title', '')),
                'company_name': self._clean_company_name(raw_data.get('company', '')),
                'city': self._clean_city(raw_data.get('city', '')),
                'district': self._clean_district(raw_data.get('district', '')),
                
                # 薪资处理
                'salary_raw': raw_data.get('salary', ''),
                **self._parse_salary(raw_data.get('salary', '')),
                
                # 要求信息清洗
                'experience': self._clean_experience(raw_data.get('experience', '')),
                'education': self._clean_education(raw_data.get('education', '')),
                'skills': self._extract_skills(raw_data),
                
                # 公司信息清洗
                'company_type': self._clean_company_type(raw_data.get('company_type', '')),
                'company_size': self._clean_company_size(raw_data.get('company_size', '')),
                'company_industry': self._clean_industry(raw_data.get('company_industry', '')),
                
                # 职位详情清洗
                'job_type': self._clean_job_type(raw_data.get('job_type', '')),
                'job_tags': self._extract_job_tags(raw_data),
                'job_description': self._clean_description(raw_data.get('job_description', '')),
                'job_highlights': self._extract_highlights(raw_data),
                
                # 地址信息处理
                'work_address': self._clean_address(raw_data.get('work_address', '')),
                'location': self._get_location(raw_data),
                
                # 来源信息（保持不变）
                'source': raw_data.get('source', ''),
                'source_job_id': raw_data.get('job_id', ''),
                'job_url': raw_data.get('job_url', ''),
                
                # 时间信息处理
                'publish_time': self._parse_time(raw_data.get('publish_time')),
                'update_time': self._parse_time(raw_data.get('update_time')),
                'crawl_time': datetime.now(),
                
                # 状态信息
                'status': 'active',
                'is_verified': False,
                'verification_time': None,
                'verification_note': ''
            }
            
            # 2. 数据验证
            if not self._validate_clean_data(clean_data):
                raise ValueError("数据验证失败")
            
            return clean_data
            
        except Exception as e:
            # 记录错误并返回None或引发异常
            print(f"数据清洗错误: {str(e)}, raw_data: {raw_data}")
            raise
    
    def _generate_unified_id(self, raw_data: Dict[str, Any]) -> str:
        """生成统一ID"""
        return f"{raw_data['source']}_{raw_data['job_id']}"
    
    def _clean_title(self, title: str) -> str:
        """清洗职位名称"""
        if not title:
            return ''
        title = title.strip()
        # 移除特殊字符
        title = re.sub(r'[^\w\s\-\/]', '', title)
        return title
    
    def _parse_salary(self, salary: str) -> Dict[str, int]:
        """解析薪资信息"""
        try:
            if not salary:
                return {'salary_min': 0, 'salary_max': 0}
                
            # 处理 "15k-25k" 格式
            match = self.salary_pattern.search(salary.lower())
            if match:
                min_salary = int(match.group(1)) * 1000
                max_salary = int(match.group(2)) * 1000
                return {
                    'salary_min': min_salary,
                    'salary_max': max_salary
                }
            
            return {'salary_min': 0, 'salary_max': 0}
            
        except Exception:
            return {'salary_min': 0, 'salary_max': 0}
    
    def _clean_experience(self, exp: str) -> str:
        """清洗经验要求"""
        if not exp:
            return '不限'
        exp = exp.strip()
        # 标准化经验格式
        exp_map = {
            '应届毕业生': '应届生',
            '无工作经验': '无经验',
            '在校生': '在校生'
        }
        return exp_map.get(exp, exp)
    
    def _extract_skills(self, raw_data: Dict[str, Any]) -> list:
        """从职位描述中提取技能要求"""
        skills = []
        description = raw_data.get('job_description', '')
        
        # 常见技能关键词
        skill_keywords = [
            'Python', 'Java', 'JavaScript', 'SQL', 'Linux',
            'Docker', 'Kubernetes', 'React', 'Vue', 'Angular',
            'Spring', 'Django', 'Flask', 'MySQL', 'MongoDB',
            'Redis', 'AWS', 'Git', 'AI', '机器学习'
        ]
        
        for skill in skill_keywords:
            if skill.lower() in description.lower():
                skills.append(skill)
        
        return list(set(skills))  # 去重
    
    def _validate_clean_data(self, data: Dict[str, Any]) -> bool:
        """验证清洗后的数据"""
        required_fields = [
            'unified_job_id', 'title', 'company_name',
            'city', 'source', 'source_job_id'
        ]
        
        # 检查必填字段
        for field in required_fields:
            if not data.get(field):
                print(f"缺少必填字段: {field}")
                return False
        
        # 验证薪资
        if data['salary_max'] < data['salary_min']:
            print("薪资范围无效")
            return False
        
        return True
    
    def _parse_time(self, time_str: Optional[str]) -> Optional[datetime]:
        """解析时间字符串"""
        if not time_str:
            return None
            
        try:
            # 处理常见的时间格式
            formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d',
                '%Y/%m/%d %H:%M:%S',
                '%Y/%m/%d'
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(time_str, fmt)
                except ValueError:
                    continue
                    
            return None
            
        except Exception:
            return None
    
    # ... 其他清洗方法 ... 