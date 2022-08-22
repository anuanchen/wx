from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

#词霸每日一句
def get_ciba():
    if (Whether_Eng!="是"):
        url = "http://open.iciba.com/dsapi/"
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        r = get(url, headers=headers)
        note_en = r.json()["content"]
        note_ch = r.json()["note"]
        return note_ch, note_en
    else:
        return "",""


#彩虹屁
def caihongpi():
    if (caihongpi_API!="881f7875de906babe0a4f40ef212e829"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
        params = urllib.parse.urlencode({'key':caihongpi_API})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/caihongpi/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        data = data["newslist"][0]["content"]
        if("XXX" in data):
            data.replace("XXX","Oya")
        return data
    else:
        return ""

#健康小提示API
def health():
    if (health_API!="881f7875de906babe0a4f40ef212e829"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
        params = urllib.parse.urlencode({'key':health_API})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/healthtip/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        data = data["newslist"][0]["content"]
        return data
    else:
        return ""

#星座运势
def lucky():
    if (lucky_API!="881f7875de906babe0a4f40ef212e829"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
        params = urllib.parse.urlencode({'key':lucky_API,'astro':astro})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/star/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        data = "爱情指数："+str(data["newslist"][1]["content"])+"\n速配星座："+str(data["newslist"][7]["content"])+"\n工作指数："+str(data["newslist"][2]["content"])+"\n今日概述："+str(data["newslist"][8]["content"])
        return data
    else:
        return ""

#励志名言
def lizhi():
    if (lizhi_API!="881f7875de906babe0a4f40ef212e829"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
        params = urllib.parse.urlencode({'key':lizhi_API})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/lzmy/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        return data["newslist"][0]["saying"]
    else:
        return ""
        

#下雨概率和建议
def tip():
    if (tianqi_API!="881f7875de906babe0a4f40ef212e829"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
        params = urllib.parse.urlencode({'key':tianqi_API,'city':city})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/tianqi/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        pop = data["newslist"][0]["pop"]
        tips = data["newslist"][0]["tips"]
        return pop,tips
    else:
        return "",""
    
    # 获取词霸每日金句
    note_ch, note_en = get_ciba()
    #彩虹屁
    pipi = caihongpi()
    #健康小提示
    health_tip = health()
    #下雨概率和建议
    pop,tips = tip()
    #励志名言
    lizhi = lizhi()
    #星座运势
    lucky_ = lucky()
      
client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}, pipi, lizhi,pop,tips, note_en, note_ch, health_tip, lucky_}
res = wm.send_template(user_id, template_id, data)
print(res)
