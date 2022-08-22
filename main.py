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


#彩虹屁
def caihongpi():
    if (caihongpi_API="881f7875de906babe0a4f40ef212e829"):
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

#励志名言
def lizhi():
    if (lizhi_API="881f7875de906babe0a4f40ef212e829"):
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
        
    #获取彩虹屁API
    caihongpi_API=config["caihongpi_API"]
    #获取励志古言API
    lizhi_API=config["lizhi_API"]
    #彩虹屁
    pipi = caihongpi()
    #励志名言
    lizhi = lizhi()
    
client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea,"color":get_random_color()},"temperature":{"value":temperature,"color":get_random_color()},"love_days":{"value":get_count(),"color":get_random_color()},"birthday_left":{"value":get_birthday(),"color":get_random_color()},"words":{"value":get_words(), "color":get_random_color()},"pipi":{"value":caihongpi()}, "lizhi":{"value":lizhi()},"lucky":{"value":lucky()}}
res = wm.send_template(user_id, template_id, data)
print(res)
