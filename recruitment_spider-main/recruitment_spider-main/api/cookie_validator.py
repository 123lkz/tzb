from fastapi import FastAPI, HTTPException
import uvicorn
import requests
import logging
from urllib.parse import quote

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Cookie Validator API",
    description="API service for validating recruitment website cookies",
    version="1.0.0"
)

def valid_cookie_zhilian() -> dict:
    """
    检查智联招聘cookie是否有效
    通过发送一个职位搜索请求来验证

    Returns:
        dict: 包含验证结果和相关参数的字典
    """
    try:
        base_url = "https://fe-api.zhaopin.com"
        search_api = "/c/i/search/positions"
        
        # 构造一个测试请求
        params = {
            "MmEwMD": "5EZdEOFFcC4TpBcDNpuxuU5J44jzvIbgqzyiRXsycHiaAnaKMfS7bGLToqVihJ3oHvqOaTF4ggpBdL9MquwNP8XuI688u4yOXOw9QKcIHk_q2.6u7TRnrser.y8xSmwOXxsH3rcSWTyxpk_rGN6yY_GrCm.yraqf7auoyOd.Ziqv.GZWzx0XgijWUxBsd1OyPzKJnKF3AYC71lAN0zICQoLv4IOlBj0MXt.Z4cCqyjOCho44WNJAWtGoRyCu4PGWEw_xtxHRBwoEmv91MheSjY3z2p9NIoupphhKeEeC3NaIZDdybTRclXQ7jJJFIM._SV91lGD3X5xpoL4u0Arytnaq1.uygJyxhoZ8MeU_9OBFkeTVZvsMjYI1omPKH19mmoph0Kvj6QuFDG3ucg4Mk0a",
            "c1K5tw0w6_": "466EXKRr06gWXidhc5dYAPNhctsr48iCa.fWOA.L2yp9wCXnQAAPYnjQbt__M3nZpjrhxycinGNuLlB.SbrCt8sJ_QcTgI_gYOadOJl7.VGWWQZyU3tchpzNIQgYuMAIh_9id1qsR01rNm_UXPU73yMAbXW9PSCYXE.gReVRQRMgD9NtURkl5Qz5ezUH7jqwUD5Sg8OSvPW2aa_LLHW46BqbuPhnlq33TeMtNiwFFEA35hFN0q39_OKVHD6O.Ob7YxifEKyYEWuGUFMkL.Ft9dJDYewfUta0WlEQp4.7q1K2nk.Io3AEDVxYLWVWL6x4eozJGZlc_0wa9ohB5p1wC7HhWq03JtZCh8qidribFTL9I_onvESNGHsS7NrOTFs0UD4I0mSIczLLTfCrnZ9hzMXDjM1VgmtqKnwQGGMRQv5rtMOPMLlCMA3NBdiuXGDfwZslsTJtbsms6_LJuNrBpuA"
        }
        
        data = {
            "S_SOU_WORK_CITY": "530",  # 北京
            "order": 4,
            "anonymous": 0,
            "cvNumber": "0B1FB7FA21E74B7837344A88A751A7495C2234C85637032AEA89700001C764F11BDE583730CE6B69C2B2B22F5C63F159_A0001",
            "eventScenario": "pcSearchedSouSearch",
            "pageIndex": 20,
            "pageSize": 20
        }
        
        url = f"{base_url}{search_api}"
        
        # 使用最新的cookie
        cookies = {
            "x-zp-client-id": "d09654ca-afff-4b02-84a8-d09fa537de95",
            "sensorsdata2015jssdkchannel": "%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D",
            "locationInfo_search": "{%22code%22:%22%22}",
            "selectCity_search": "489",
            "sts_deviceid": "197526723501f38-0ed9e0ca58d37b8-26011e51-1328640-19752672351299a",
            "rt": "0e6fb304fe2244a1b5a909d3ef1979db",
            "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%221229631833%22%2C%22first_id%22%3A%22196f067b1d7754-0e25ff0448c2f78-26011c51-1327104-196f067b1d8157b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk2ZjA2N2IxZDc3NTQtMGUyNWZmMDQ0OGMyZjc4LTI2MDExYzUxLTEzMjcxMDQtMTk2ZjA2N2IxZDgxNTdiIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMTIyOTYzMTgzMyJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221229631833%22%7D%2C%22%24device_id%22%3A%22196f067b1d7754-0e25ff0448c2f78-26011c51-1327104-196f067b1d8157b%22%7D",
            "Hm_lvt_7fa4effa4233f03d11c7e2c710749600": "1752055254,1752662907",
            "HMACCOUNT": "55B60FA1F020E7A1",
            "at": "258a2692fe704a24a98d9d97ea5f2f5a",
            "LastCity": "%E6%B5%8E%E5%8D%97",
            "LastCity_id": "702",
            "Hm_lpvt_7fa4effa4233f03d11c7e2c710749600": "1753083019"
        }
        
        # 创建session并设置cookie
        session = requests.Session()
        for key, value in cookies.items():
            session.cookies.set(key, value)
        
        response = session.post(url, params=params, json=data)
        
        # 检查响应状态码
        if response.status_code != 200:
            logger.error(f"Cookie可能已过期，响应状态码: {response.status_code}")
            return {
                "is_valid": False,
                "message": f"Cookie可能已过期，响应状态码: {response.status_code}"
            }
        
        # 检查响应内容
        result = response.json()
        if result.get('code') != 200:
            logger.error(f"Cookie可能已过期，API返回错误: {result.get('message')}")
            return {
                "is_valid": False,
                "message": f"Cookie可能已过期，API返回错误: {result.get('message')}"
            }
            
        # 检查是否有数据返回
        if not result.get('data', {}).get('list'):
            logger.error("Cookie可能已过期，未能获取到数据")
            return {
                "is_valid": False,
                "message": "Cookie可能已过期，未能获取到数据"
            }
        
        logger.info("Cookie验证成功")
        logger.info(cookies)
        logger.info(len(result['data']['list']))
        logger.info(result['data']['list'][-1])
        return {
            "is_valid": True,
            "message": "Cookie验证成功",
            "cookies": cookies,
            "params": params,
            "cvNumber": data["cvNumber"]
        }
        
    except Exception as e:
        logger.error(f"验证Cookie时发生错误: {str(e)}")
        return {
            "is_valid": False,
            "message": f"验证Cookie时发生错误: {str(e)}"
        }

@app.get("/api/validate/zhilian")
async def validate_zhilian_cookie():
    """
    验证智联招聘的cookie是否有效
    
    Returns:
        dict: 包含验证结果的响应
    """
    try:
        result = valid_cookie_zhilian()
        
        return {
            "status": "success",
            "is_valid": result["is_valid"],
            "message": result["message"],
            "data": {
                "cookies": result.get("cookies"),
                "params": result.get("params"),
                "cvNumber": result.get("cvNumber")
            } if result["is_valid"] else None
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"验证过程中发生错误: {str(e)}"
        )

def valid_cookie_lagou() -> dict:
    """
    检查拉勾网cookie是否有效
    通过发送一个职位搜索请求来验证

    Returns:
        dict: 包含验证结果和相关参数的字典
    """
    try:
        # 使用写死的cookie
        cookies = {
            "RECOMMEND_TIP": "1",
            "index_location_city": "%E5%85%A8%E5%9B%BD",
            "JSESSIONID": "ABAACCCACFEAAAC6D6A64F66A67FF7B491888030B9642B4",
            "WEBTJ-ID": "20250414152846-19633335e0a51b-02d72c731a36c7-26011d51-1952424-19633335e0bbb9",
            "sensorsdata2015session": "%7B%7D",
            "user_trace_token": "20250414152850-5af7b9dc-b893-4f0f-9243-4268627be396",
            "LGUID": "20250414152850-4e9cd49d-019e-4673-83bb-29c4aeedb72d",
            "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1744615730",
            "HMACCOUNT": "0EBFC3A8F5B5C78A",
            "_ga": "GA1.2.208655005.1744615730",
            "LG_HAS_LOGIN": "1",
            "login": "true",
            "showExpriedIndex": "1",
            "showExpriedCompanyHome": "1",
            "showExpriedMyPublish": "1",
            "privacyPolicyPopup": "false",
            "X_MIDDLE_TOKEN": "841a762fc0d33539c075f869ff243f4b",
            "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1744709594",
            "LGRID": "20250415173314-e12e665a-0bcb-4058-8b86-b3f3bce56d85",
            "_ga_DDLTLJDLHH": "GS1.2.1744709595.2.0.1744709595.60.0.0",
            "__lg_stoken__": "9d1d169f253728652fb7fc18450c371ce453d3ef77c48dc066a0a0d6667bda1d785068a74c20325ba16c86a90239de4d176f9b1211f703c4ecfb197ca021e5de6083bd579091",
            "gate_login_token": "v1####2d173be9c329885fcefb4b010001729d63ea0ce21c1fe33bd78d7fb7dd1228a4",
            "LG_LOGIN_USER_ID": "v1####9aed6f727d2887c79bfeda18d979b25cb53af2d15433c77ae393d9b974c19696",
            "_putrc": "6BB4D6A5A9021AFB123F89F2B170EADC",
            "unick": "%E8%83%A1%E5%A5%B3%E5%A3%AB",
            "hasDeliver": "0",
            "__PWD_STRENGTH_CHECK__27656242": "1",
            "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%22196333364da1ba-00ea5f3aa7eb76-26011d51-1952424-196333364db4ea%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22PC_SEARCH%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%22135.0.0.0%22%7D%2C%22%24device_id%22%3A%22196333364da1ba-00ea5f3aa7eb76-26011d51-1952424-196333364db4ea%22%7D",
            "X_HTTP_TOKEN": "bf5cddb225d89f763285825471af00dfd9cec312e1"
        }

        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.lagou.com',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1'
        }

        # 构造测试请求
        url = "https://www.lagou.com/wn/jobs"
        params = {
            # 'tagCodeList': '200001',  # Python岗位代码
            'px': 'new',
            # 'hy': '电商平台',
            'cl': 'false',
            'fromSearch': 'true',
            # 'city': '北京',
            'pn': '10'
        }

        # 创建session并设置cookie
        session = requests.Session()
        session.headers.update(headers)
        for key, value in cookies.items():
            session.cookies.set(key, value)

        response = session.get(url, params=params)

        # 检查响应状态码
        if response.status_code != 200:
            logger.error(f"Cookie可能已过期，响应状态码: {response.status_code}")
            return {
                "is_valid": False,
                "message": f"Cookie可能已过期，响应状态码: {response.status_code}"
            }

        # 检查是否被重定向到登录页面
        if "login" in response.url.lower() or "sign" in response.url.lower():
            logger.error("Cookie已过期，被重定向到登录页面")
            return {
                "is_valid": False,
                "message": "Cookie已过期，被重定向到登录页面"
            }

        logger.info("Cookie验证成功")
        return {
            "is_valid": True,
            "message": "Cookie验证成功",
            "cookies": cookies,
            "headers": headers
        }

    except Exception as e:
        logger.error(f"验证Cookie时发生错误: {str(e)}")
        return {
            "is_valid": False,
            "message": f"验证Cookie时发生错误: {str(e)}"
        }

@app.get("/api/validate/lagou")
async def validate_lagou_cookie():
    """
    验证拉勾网的cookie是否有效
    
    Returns:
        dict: 包含验证结果的响应
    """
    try:
        result = valid_cookie_lagou()
        
        return {
            "status": "success",
            "is_valid": result["is_valid"],
            "message": result["message"],
            "data": {
                "cookies": result.get("cookies"),
                "headers": result.get("headers")
            } if result["is_valid"] else None
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"验证过程中发生错误: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(
        "cookie_validator:app",
        host="0.0.0.0",
        port=10330,
        reload=True
    ) 