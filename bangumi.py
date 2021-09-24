import requests
from bs4 import BeautifulSoup
import anime_class


def getfrombangumi(year):
    return


def getfrombangumi_pageat(year, page):
    url = "https://bgm.tv/anime/browser/airtime/"+str(year)+"?page="+str(page)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, "html.parser")
    aniul = soup.find_all(name='ul', attrs={"id": "browserItemList"})
    if(len(aniul) != 0):
        aniul = aniul[0]
        lis = aniul.find_all("li")
        if(len(lis) == 0):
            # 最后一页的下一页（空页
            return None
        else:
            # 不是空页

            #
            return
