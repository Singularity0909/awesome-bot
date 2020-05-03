import http.client
import json
import urllib

import requests
from bs4 import BeautifulSoup


async def get_weather(city_name):
    city_code = get_city_code(city_name)
    weather_info = get_info(city_code)
    if weather_info:
        res = city_name + '的天气预报如下\n'
        for each in weather_info:
            res += '\n' + each[0] + ' ' + each[1] + ' '
            if each[2]:
                res += each[2] + '/'
            res += each[3]
        return res
    else:
        return '查询失败'


def get_info(city_code):
    try:
        url = 'http://www.weather.com.cn/weather/' + city_code + '.shtml'
        r = requests.get(url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        div = soup.find('div', {'id': '7d'})
        li = div.find('ul').find_all('li')
        week_info = []
        for each in li:
            day_info = []
            day_info.append(each.find('h1').string)
            p = each.find_all('p')
            day_info.append(p[0].string)
            if p[1].find('span') is None:
                temp_high = None
            else:
                temp_high = p[1].find('span').string
            temp_low = p[1].find('i').string
            day_info.append(temp_high)
            day_info.append(temp_low)
            week_info.append(day_info)
        return week_info
    except:
        return None


def get_city_code(city_name):
    try:
        parameter = urllib.parse.urlencode({'cityname': city_name})
        conn = http.client.HTTPConnection('toy1.weather.com.cn', 80, timeout=5)
        conn.request('GET', '/search?' + parameter)
        r = conn.getresponse()
        data = r.read().decode()[1: -1]
        json_data = json.loads(data)
        code = json_data[0]['ref'].split('~')[0]
        return code
    except:
        return None
