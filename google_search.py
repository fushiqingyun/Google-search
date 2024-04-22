from tls_get import tls_get
from selenium import webdriver
import time
import json
import os
import ujson
import base64
import sys
import multiprocessing
import threading
import requests
import re
from queue import Queue
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue, Value
import random
# import var_dump
from queue import Queue
from urllib3.exceptions import SSLError, MaxRetryError

option = webdriver.ChromeOptions()
option.add_argument("--user-data-dir="+r"C:/Users/ax.Liu/AppData/Local/Google/Chrome_new/User Data/")


cookies = {
    '__Secure-ENID': '18.SE=fuOAB6b0i2dx-FzJtATn2_zDGAb0q4e1QRgKeq3wjRva1a_-OQZuZvraXxm4e_VEVIG_wTzW3gtlHQMjHTYsiBIFt6gBWudXdR-EjiSwZVJktjCV3YvgLWe0qGAt5BuzJvsKvt1XGUWVH_r4LqVoeoN9o9URwE60JSEuLm88Xz8',
    'SID': 'g.a000iAiWY63FPJFgMp_OnWgzrWH0BhiDYjGzHS0KfojIVdKOI8UBzHun6y1m2L62Y2wm8iyoegACgYKAfISAQASFQHGX2MiARZw3S4XeFrDsQXjFzsc-RoVAUF8yKrVM4W1J4q3PC4cYxFEFtYV0076',
    '__Secure-1PSID': 'g.a000iAiWY63FPJFgMp_OnWgzrWH0BhiDYjGzHS0KfojIVdKOI8UBZJYvgoGMLCVG4FyIt5duWwACgYKAfQSAQASFQHGX2MiF-Fkr5g9kGXfLKTYxOhwHxoVAUF8yKqcjWVMsGF2D323InRGE9wA0076',
    '__Secure-3PSID': 'g.a000iAiWY63FPJFgMp_OnWgzrWH0BhiDYjGzHS0KfojIVdKOI8UBtdVCESAJAwXPMtI0n3j1WQACgYKARUSAQASFQHGX2MiQJPKXd2IvFeBwKWk0Qh9uxoVAUF8yKqCK56CXcB-BVpP_cqjNVTS0076',
    'HSID': 'A3YEeEvRO4x_33zwA',
    'SSID': 'AwaKVwxatB1_zQP3j',
    'APISID': 'JyjXg_wRoXQeF5q2/A4uFW2BTqCuokk-3f',
    'SAPISID': '-6ir5tZV8-WkGK5m/A4pZlyFZ_2aVyQhmU',
    '__Secure-1PAPISID': '-6ir5tZV8-WkGK5m/A4pZlyFZ_2aVyQhmU',
    '__Secure-3PAPISID': '-6ir5tZV8-WkGK5m/A4pZlyFZ_2aVyQhmU',
    'AEC': 'AQTF6Hy-KOhvroTeerO04GN4hJBH3zoZrTFdcIV8W_uNIgMrUvEt6TnU5G0',
    'SEARCH_SAMESITE': 'CgQI9poB',
    'NID': '513=hsW1JCZi6ZRW1NkRTA2uVnOhF7Sm04BbwHozzj98zoZS56CmDL8xTxHs5ZpW4ipzAQmHZkhi6CGKP4LEivRXY1I540WLcuDKWtA51juJkeVzP9ypKvDikz_zf2PGhVYbB4C7P2Bse2NuIkdlegHCDsij4kSHVikSyuaGriDmVB08dgHdEXCkRPCq-xkuvn9kPNAPqUajWGxjd0B2LDLFLBlFQ9SbqP1v7xMPUJZF8JFMkcFyAHyFJer1JZFxDjqvtndHyOppkAlT6PIvmYmJXd1swevXGiKnLya6wDCY5Plb5Ux136Cu9DymuyhT2Nuh6jHQAfUwIsOPUwBqe7UbT3cpA4xDlplZ7YSQTeE1rCFffGw',
    '1P_JAR': '2024-04-18-08',
    'DV': 'k9WP7f0f72JXECBuCtWvdH13cO4E7xgaJsH45ZPKwwMAAJAGHw3XbxbXEAEAANSC5f3q3bq_SwAAAPob2FmvhbQoFgAAAA',
    'UULE': 'a+cm9sZTogMQpwcm9kdWNlcjogMTIKdGltZXN0YW1wOiAxNzEzNDI4Nzc0MTk4MDAwCmxhdGxuZyB7CiAgbGF0aXR1ZGVfZTc6IDM5OTk5OTA5MwogIGxvbmdpdHVkZV9lNzogMTE2MzE1MDU3Mgp9CnJhZGl1czogODAxNjQxNy4yMzY1MjU4OTcKcHJvdmVuYW5jZTogNgo=',
}

update_cookies_lock = threading.Lock()

task_lock = threading.Lock()


COOKIES_UPDATE_FLAG = True

def update_cookies():
    """
    如果报如下错误：
    selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH. Please see https://sites.google.com/a/chromium.org/chromedriver/home

    原因是在执行时，没有在path中找到驱动，这里的解决办法是实例化driver对象时，添加executable_path参数，引用驱动的绝对路径
    """
    # driver = webdriver.Chrome(executable_path="C:\Python36\Scripts\chromedriver.exe") # 解决如上报错
    global cookies
    global COOKIES_UPDATE_FLAG
    driver = webdriver.Chrome(options =option)
    driver.implicitly_wait(time_to_wait=5)
    driver.get('https://www.google.com.hk/search?q=site%3Abaidu.com')
    while True:
        time.sleep(1)
        page_source = driver.page_source
        if "搜索结果" in page_source:
            print("验证码通过")
            break
    cookies = driver.get_cookies()
    cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
    cookies = cookies_dict
    COOKIES_UPDATE_FLAG = True
    driver.quit()
    

def get_random_ua():
        web_uas = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36	29.73",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58	10.55",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.1	8.38",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36	7.67",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0	5.82",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.3	3.07",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51	3.01",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15	2.88",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.6 Safari/605.1.1	2.75",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.3	2.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6,2 Safari/605.1.1	1.85",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.	1.28",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58	1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.	1.02",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3	1.02",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36	0.96",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15	0.9",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15	0.83",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36	0.77",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36	0.7",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36	0.64",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43	0.64",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15	0.64",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15	0.58",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36	0.51",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0	0.51",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15	0.51",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.	0.51",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67	0.51",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Geck	0.51",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0	0.51",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36	0.45",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36	0.45",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36	0.45",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.37	0.32",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36	0.32",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.5	0.26",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0	0.26",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.	0.26",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0	0.26",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36	0.26",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35	0.26",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36	0.19",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36	0.19",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36	0.19",
            "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko	0.19",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.2.625 Yowser/2.5 Safari/537.36	0.13",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54	0.13",
            "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0 SeaMonkey/2.49.5	0.13",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.55	0.13",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0	0.13",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50	0.13",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763	0.13",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76	0.13",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36	0.13",
            "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0	0.06",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36	0.06",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0	0.06",
            "Mozilla/5.0 (Windows NT 6.3; rv:102.0) Gecko/20100101 Firefox/102.0	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.67	0.06",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36	0.06",
            "Mozilla/5.0 (X11; Linux x86_64; Chromium GOST) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36	0.06",
            "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0	0.06",
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.36	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.64	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.2.623 Yowser/2.5 Safari/537.36	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0 (Edition Campaign 34)	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0 (Edition std-1)	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Unique/100.7.1046.47	0.06",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48	0.06",
            # macos
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.4; rv:109.0) Gecko/20100101 Firefox/114.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.4; rv:102.0) Gecko/20100101 Firefox/102.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
        ]
        return random.choice(web_uas)



def get_request(host_name):
    global COOKIES_UPDATE_FLAG
    retry_times = 0
    while True:
        try:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                # 'cookie': '__Secure-ENID=18.SE=fuOAB6b0i2dx-FzJtATn2_zDGAb0q4e1QRgKeq3wjRva1a_-OQZuZvraXxm4e_VEVIG_wTzW3gtlHQMjHTYsiBIFt6gBWudXdR-EjiSwZVJktjCV3YvgLWe0qGAt5BuzJvsKvt1XGUWVH_r4LqVoeoN9o9URwE60JSEuLm88Xz8; SID=g.a000iAiWY63FPJFgMp_OnWgzrWH0BhiDYjGzHS0KfojIVdKOI8UBzHun6y1m2L62Y2wm8iyoegACgYKAfISAQASFQHGX2MiARZw3S4XeFrDsQXjFzsc-RoVAUF8yKrVM4W1J4q3PC4cYxFEFtYV0076; __Secure-1PSID=g.a000iAiWY63FPJFgMp_OnWgzrWH0BhiDYjGzHS0KfojIVdKOI8UBZJYvgoGMLCVG4FyIt5duWwACgYKAfQSAQASFQHGX2MiF-Fkr5g9kGXfLKTYxOhwHxoVAUF8yKqcjWVMsGF2D323InRGE9wA0076; __Secure-3PSID=g.a000iAiWY63FPJFgMp_OnWgzrWH0BhiDYjGzHS0KfojIVdKOI8UBtdVCESAJAwXPMtI0n3j1WQACgYKARUSAQASFQHGX2MiQJPKXd2IvFeBwKWk0Qh9uxoVAUF8yKqCK56CXcB-BVpP_cqjNVTS0076; HSID=A3YEeEvRO4x_33zwA; SSID=AwaKVwxatB1_zQP3j; APISID=JyjXg_wRoXQeF5q2/A4uFW2BTqCuokk-3f; SAPISID=-6ir5tZV8-WkGK5m/A4pZlyFZ_2aVyQhmU; __Secure-1PAPISID=-6ir5tZV8-WkGK5m/A4pZlyFZ_2aVyQhmU; __Secure-3PAPISID=-6ir5tZV8-WkGK5m/A4pZlyFZ_2aVyQhmU; AEC=AQTF6Hy-KOhvroTeerO04GN4hJBH3zoZrTFdcIV8W_uNIgMrUvEt6TnU5G0; SEARCH_SAMESITE=CgQI9poB; NID=513=hsW1JCZi6ZRW1NkRTA2uVnOhF7Sm04BbwHozzj98zoZS56CmDL8xTxHs5ZpW4ipzAQmHZkhi6CGKP4LEivRXY1I540WLcuDKWtA51juJkeVzP9ypKvDikz_zf2PGhVYbB4C7P2Bse2NuIkdlegHCDsij4kSHVikSyuaGriDmVB08dgHdEXCkRPCq-xkuvn9kPNAPqUajWGxjd0B2LDLFLBlFQ9SbqP1v7xMPUJZF8JFMkcFyAHyFJer1JZFxDjqvtndHyOppkAlT6PIvmYmJXd1swevXGiKnLya6wDCY5Plb5Ux136Cu9DymuyhT2Nuh6jHQAfUwIsOPUwBqe7UbT3cpA4xDlplZ7YSQTeE1rCFffGw; 1P_JAR=2024-04-18-08; DV=k9WP7f0f72JXECBuCtWvdH13cO4E7xgaJsH45ZPKwwMAAJAGHw3XbxbXEAEAANSC5f3q3bq_SwAAAPob2FmvhbQoFgAAAA; UULE=a+cm9sZTogMQpwcm9kdWNlcjogMTIKdGltZXN0YW1wOiAxNzEzNDI4Nzc0MTk4MDAwCmxhdGxuZyB7CiAgbGF0aXR1ZGVfZTc6IDM5OTk5OTA5MwogIGxvbmdpdHVkZV9lNzogMTE2MzE1MDU3Mgp9CnJhZGl1czogODAxNjQxNy4yMzY1MjU4OTcKcHJvdmVuYW5jZTogNgo=',
                'pragma': 'no-cache',
                'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"123.0.6312.123"',
                'sec-ch-ua-full-version-list': '"Google Chrome";v="123.0.6312.123", "Not:A-Brand";v="8.0.0.0", "Chromium";v="123.0.6312.123"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'sec-ch-ua-wow64': '?0',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'x-client-data': 'CJa2yQEIpLbJAQipncoBCIPbygEIlKHLAQiFoM0BCN3uzQEIs4XOAQi4hs4BCPWJzgEIhdXMIgik7cwiGPbJzQEY1d3NARiY9c0BGNiGzgE=',
            }
            proxies = {
                "http":"http://127.0.0.1:7890",
                "https":"http://127.0.0.1:7890",
            }
            params = {
                'q': f'site:{host_name}',
            }
            response = requests.get('https://www.google.com.hk/search', params=params,headers=headers,cookies = cookies,proxies=proxies,timeout=10)
            response.encoding = 'utf-8'
            if response.status_code == 200 and '找到约' in response.text:
                # print(f"搜索成功====={i}")
                soup = BeautifulSoup(response.text,'html.parser')
                div_tag = soup.find_all('div', id='result-stats')
                for div_info in div_tag:
                    number_text = re.search(r'找到约(.*?)条结果', div_info.text)
                    number = number_text.group(1)
                    number = number.replace(",","")
                    print(f"当前任务{host_name}成功==========================，找到约{number}条结果")
                    base_info = {"host_name":host_name,"number":number}
                    s = json.dumps(base_info,ensure_ascii=False)
                    with task_lock:
                        with open('final_res.jsonl','a') as file:
                            file.write(s+"\n")    
                break
            elif response.status_code ==200 and '获得' in response.text :
                soup = BeautifulSoup(response.text,'html.parser')
                div_tag = soup.find_all('div', id='result-stats')
                for div_info in div_tag:
                    number_text = re.search(r'获得(.*?)条结果', div_info.text)
                    number = number_text.group(1)
                    number = number.replace(",","")
                    print(f"当前任务{host_name}成功==========================，获得{number}条结果")
                    base_info = {"host_name":host_name,"number":number}
                    s = json.dumps(base_info,ensure_ascii=False)
                    with task_lock:
                        with open('final_res.jsonl','a') as file:
                            file.write(s+"\n")    
                        # write_warc(response,full_file_name)
                break    
            else:
                print(f"出现验证码,休息五秒重试=============={host_name}")
                COOKIES_UPDATE_FLAG = False
                with update_cookies_lock:
                    if not COOKIES_UPDATE_FLAG :
                        update_cookies()
                    else:
                        if retry_times >=3:
                            break
                        retry_times +=1
                        continue
                if retry_times >=3:
                    break
                retry_times +=1
                continue
        except Exception as e:
            print(f"本次请求失败了{host_name}-------------------------失败原因为{e}")
            # raise e
            time.sleep(1)
            if retry_times >=3:
                    break
            retry_times +=1
            continue


def worker(task_q):
    while  not task_q.empty():
        try:
            print(f"当前剩余任务长度为========================={task_q.qsize()}")
            host_name = task_q.get()
            if host_name is None:
                break
            get_request(host_name)
            # queue.task_done()  # 标记任务完成
        except Exception as e:
            raise e
    


if __name__ == "__main__":
    task_q = Queue()
    threads = []

    with open('task_list.txt','r') as f:
        task_list = f.read().splitlines()
    

    with open('final_res.jsonl','r') as f:
        exist_list = f.read().splitlines()
    
    exist_host_list = set()
    for exist_info in exist_list:
        data_json = json.loads(exist_info)
        exist_host =data_json['host_name']
        exist_host_list.add(exist_host)
    
    real_task_list = list(set(task_list).difference(exist_host_list))

    top_5000_tasks = real_task_list[:200000]

    if len(top_5000_tasks) == 0:
        print("任务结束")
        time.sleep(5000000)

    for task_info in top_5000_tasks:
        task_q.put(task_info)
    
    # print(len(link_list))
    
    num_threads = 20
    for _ in range(num_threads):
        t = threading.Thread(target=worker,args=(task_q,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()  