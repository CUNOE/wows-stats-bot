from typing import List
import httpx
import traceback
import json
import os
from .data_source import nations,shiptypes,levels
from .utils import match_keywords
from httpx import ConnectTimeout
from asyncio.exceptions import TimeoutError

cfgpath = os.path.join(os.path.dirname(__file__), 'config.json')
config = json.load(open(cfgpath, 'r', encoding='utf8'))

headers = {
    'Authorization': config['token']
}

async def get_nation_list():
    try:
        msg = ''
        url = 'https://api.wows.linxun.link/public/wows/encyclopedia/nation/list'
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, timeout=None)
            result = resp.json()
        for nation in result['data']:
            msg: str = msg + f"{nation['cn']}：{nation['nation']}\n"
        return msg
    except Exception:
        traceback.print_exc()
        
async def get_ship_name(infolist:List):
    try:
        msg = ''
        param_nation,infolist = await match_keywords(infolist,nations)
        if not param_nation:
            return '请检查国家名是否正确'
        
        param_shiptype,infolist = await match_keywords(infolist,shiptypes)
        if not param_shiptype:
            return '请检查船只类别是否正确'
        
        param_level,infolist = await match_keywords(infolist,levels)
        if not param_level:
            return '请检查船只等级是否正确'
        params = {
            "county":param_nation,
            "level":param_level,
            "shipName":'',
            "shipType":param_shiptype
        }
        url = 'https://api.wows.linxun.link/public/wows/encyclopedia/ship/search'
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=None)
            result = resp.json()
        if result['data']:
            for ship in result['data']:
                msg += f"{ship['shipNameCn']}：{ship['shipNameNumbers']}\n"
        else:
            msg = '没有符合的船只'
        return msg
    except Exception:
        traceback.print_exc()
        return msg
    
async def get_ship_byName(shipname:str):
    try:
        url = 'https://api.wows.linxun.link/public/wows/encyclopedia/ship/search'
        params = {
        "county":'',
        "level":'',
        "shipName":shipname,
        "shipType":''
    }
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=None)
            result = resp.json()
        List = []
        if result['code'] == 200 and result['data']:
            for each in result['data']:
                List.append([each['id'],each['shipNameCn'],each['shipNameNumbers'],each['tier']])
            return List
        else:
            return None
    except Exception:
        traceback.print_exc()
        return None
    
async def get_AccountIdByName(server:str,name:str):
    try:
        url = 'https://api.wows.linxun.link/public/wows/account/search/user'
        params = {
            "server": server,
            "userName": name
        }
        print(f"下面是本次请求的参数，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{params}")
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=None)
            result = resp.json()
        if result['code'] == 200 and result['data']:
            return result['data']['accountId']
        else:
            return result['message']
    except (TimeoutError, ConnectTimeout):
        traceback.print_exc()
        return '请求超时了，请过一会儿重试哦~'
    except Exception:
        traceback.print_exc()
        return '好像出了点问题呢，可能是网络问题，如果重试几次还不行的话，请联系麻麻解决'
    
async def get_ClanIdByName(server:str,tag:str):
    try:
        url = 'https://api.wows.linxun.link/public/wows/clan/search'
        params = {
            "server": server,
            "tag": tag
        }
        print(f"下面是本次请求的参数，如果遇到了问题，请将这部分连同报错日志一起发送给麻麻哦\n{params}")
        async with httpx.AsyncClient(headers=headers) as client:
            resp = await client.get(url, params=params, timeout=None)
            result = resp.json()
        List = []
        if result['code'] == 200 and result['data']:
            #for each in result['data']:
            #    List.append([each['clanId'],each['name'],each['serverName'],each['tag']])
            return result['data']
        else:
            return None
    except Exception:
        traceback.print_exc()
        return None