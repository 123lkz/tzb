import requests
import logging
from typing import Dict

logger = logging.getLogger(__name__)

def valid_cookie_zhilian(cookies: Dict[str, str]) -> bool:
    """
    检查智联招聘cookie是否有效
    通过发送一个职位搜索请求来验证

    Args:
        cookies: 包含cookie信息的字典

    Returns:
        bool: cookie是否有效
    """
    try:
        base_url = "https://www.zhaopin.com"
        search_api = "/api/sou"
        
        # 构造一个测试请求
        params = {
            "MmEwMD": "5DyKsT_0eeMgtH6eyNbScqP21.FaNPLvp_CpknVsO9IkEuUnVxRjpuTh184bUDoqDhMk6_R6Rj_tSXRJXFELaCJMRL8DZNGuoLL_tw438tjZYy.SD2SvTAoNtabvcU484KcrK9biJF2ydjItNBayoVLsdJxLBvuRARfTdsyjMPcHICZVGdib38ILkddDYVZqLxF4ebkDPBWro3F8sRGTyEJvNlSUNx610mHeAHX4jSTDCYmv8zdNEncjQQnRC_I0lG6FnpoHRckHhkrv6Uh_QAY5tqFGZDGdv8EC7gkP0rLUerLlhErygOmpxgUy1L4XJL0ytxTFxYTbHRQ.rCdB6r7en0zRxrAE40qduwAvBRsttpJlTjHt3t0Y7DWQXUGrolDfTgbOFkgRL0aBUJQHWVq",
            "c1K5tw0w6_": "4_7cxgK11RgVh1a0tSaEIVE5sdqyqK_bXQcKFT9Jj_CujE06oaxqaz7XbuzGEYkRCaw4nJ3j1H6_clLsHI__4XqL_c9bBRBGCt7lVo7IjhX2JNQlxdTCj2mcwpbfEkrvBhSgMuHzfa_iNxd1h2FTtD0Z5kL49XylmcHYwlQN6VZZkFf3taOYea0WXTWPSPM6INGMmFwprJr8Dn8p7cw3UxDnDv9GAzHtxYPsEO9TCm67aD7SwdPNOzxQZiyfY8uh_ZmVtO5AshRCBWZc5S6dHGQIKpIOZbBhZEHGLpVuuPi9.LbH9B21uaY.oCdAQcdERKYagMG4U4W09BM7wpkQSglbYPmrSMxzCtI_iMKS56oC4rhsfoas1xyxDLUyTLwJc9gLK5mSotNt4jb3RW2uBjs4ABFSuqT8fexmj3CuAKflx3Oj_yFir8ab9UNlS3NRUCFz_RZIIp4a4KdvmL08kFq"
        }
        
        data = {
            "S_SOU_WORK_CITY": "530",  # 北京
            "order": 4,
            "anonymous": 0,
            "cvNumber": "0B1FB7FA21E74B7837344A88A751A7495C2234C85637032AEA89700001C764F1877D1C3809F53036DED747947787C304_A0001",
            "eventScenario": "pcSearchedSouSearch",
            "pageIndex": 20,
            "pageSize": 20
        }
        
        url = f"{base_url}{search_api}"
        
        # 创建session并设置cookie
        session = requests.Session()
        for key, value in cookies.items():
            session.cookies.set(key, value)
        
        response = session.post(url, params=params, json=data)
        
        # 检查响应状态码
        if response.status_code != 200:
            logger.error(f"Cookie可能已过期，响应状态码: {response.status_code}")
            return False
        
        # 检查响应内容
        result = response.json()
        if result.get('code') != 200:
            logger.error(f"Cookie可能已过期，API返回错误: {result.get('message')}")
            return False
            
        # 检查是否有数据返回
        if not result.get('data', {}).get('list'):
            logger.error("Cookie可能已过期，未能获取到数据")
            return False
        
        logger.info("Cookie验证成功")
        return True
        
    except Exception as e:
        logger.error(f"验证Cookie时发生错误: {str(e)}")
        return False

