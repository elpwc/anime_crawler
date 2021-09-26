import requests
from bs4 import BeautifulSoup
import anime_class
import math
import time
import re


def getfrombangumi(year, page=-1, moe_animes=None):
    res = []
    if(page > 0):
        res += getfrombangumi_page_at(year, page, moe_animes)
    else:
        crt_pg = 1
        while True:
            print(str(crt_pg)+"---------------------------------------------------")
            page = getfrombangumi_page_at(year, crt_pg, moe_animes)
            if(page == None):
                break
            res += page
            crt_pg += 1

            # 延时防BAN
            time.sleep(1)
    return res


def getfrombangumi_page_at(year, page, moe_animes=None):
    res = []
    url = "https://bgm.tv/anime/browser/airtime/"+str(year)+"?page="+str(page)
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
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
            for li in lis:
                # 名字 年份
                anime = anime_class.Anime(li.div.h3.a.text, year)
                # 外文名
                if(tag_exist(li.div.h3, 'small')):
                    anime.jp_name = li.div.h3.small.text

                else:
                    anime.jp_name = anime.name  # 后面再判断
                    if(anime.name == anime.jp_name):
                        anime.country = 'zh-cn'
                anime.country = get_country(anime.jp_name)
                if(anime.country == 'zh-cn' and anime.name != anime.jp_name):
                    anime.country = 'ja'
                if(anime.country == 'zh-cn'):
                    anime.jp_name = ""
                # RANK
                if(tag_exist(li.div, 'span', {'class': 'rank'})):
                    anime.bgm_rank = li.div.find_all('span', {'class': 'rank'})[
                        0].text.split(' ')[1]
                # 图像 页面存否
                if(tag_exist(li.a, 'span')):
                    src = li.a.span.img.attrs['src']
                    if(src == '/img/no_icon_subject.png'):
                        anime.bgm_no_page = True
                    else:
                        anime.img_url = src.split("/s/")[1]
                else:
                    anime.bgm_no_page = True
                # print(li.attrs['id'])
                # id
                anime.bangumi_id = li.attrs['id'].split('_')[1]

                crt = li.div.p.text.split(' / ')
                # print(anime.name)
                # print(crt)
                if(len(crt) == 1):
                    # 只有时间日期
                    anidate = gettimedate(
                        crt[0].replace(' ', '').replace('\n', ''))
                    if(anidate != None):
                        anime.housou_date = anidate
                        anime.season = math.floor(
                            anime.housou_date.tm_mon / 4.0)
                elif(len(crt) > 1):
                    #话数 / 时间日期 / ...
                    if(is_datetime(crt[0])):
                        anidate = gettimedate(
                            crt[0].replace(' ', '').replace('\n', ''))
                        if(anidate != None):
                            anime.housou_date = anidate
                            #anime.season = math.floor(anime.housou_date.tm_mon / 4.0)
                    else:
                        anidate = gettimedate(
                            crt[1].replace(' ', '').replace('\n', ''))
                        if(anidate != None):
                            anime.housou_date = anidate
                            #anime.season = math.floor(anime.housou_date.tm_mon / 4.0)
                        # 话数
                        if(crt[0].find('话') != -1):
                            anime.episode = crt[0].replace(
                                ' ', '').replace('\n', '').split('话')[0]
                            eps = int(anime.episode)
                            # 类型
                            if(eps >= 5):
                                anime.ani_type = 'anime'
                            else:
                                if(year<2000):
                                    anime.ani_type = 'movie'
                                else:
                                    anime.ani_type = 'ova'
                # 放送日期获取失败修正
                if(anime.housou_date.tm_year == 1975):
                    anime.housou_date = time.strptime(str(year), "%Y")
                # 参考moe数据修正
                if(moe_animes != None and year >= 2000 and year <= 2021):
                    index = index_(moe_animes[year-2000], anime.name)
                    if(index != -1):
                        anime.moe_no_page = moe_animes[year -
                                                       2000][index].moe_no_page
                        anime.ani_type = moe_animes[year-2000][index].ani_type
                        anime.country = 'ja'
                # 根据名称进行类型修正
                if(anime.name.find('电影') != -1 or anime.name.find('剧场版') != -1 or anime.name.find('映画') != -1 or anime.name.lower().find('movie') != -1 or anime.name.lower().find('film') != -1):
                    anime.ani_type = "movie"
                if(anime.name.lower().find('ova') != -1 or anime.name.find('番外') != -1 or anime.name.find('小剧场') != -1):
                    anime.ani_type = "ova"
                res.append(anime)
    return res


def is_datetime(s):
    if(s.find('年') != -1 and s.find('月') != -1):
        return True
    elif(s.find('日') != -1 and s.find('月') != -1):
        return True
    elif(len(s.split('-')) == 3):
        return True
    elif(len(s.split('/')) == 3):
        return True


def gettimedate(s):
    try:
        if(s.find('(') != -1):
            s = s.split('(')[0]
        if(s.find('（') != -1):
            s = s.split('（')[0]
        if(len(s.split('/')) == 2):
            s = s.split('/')[0]
        if(s.find('年') != -1 and s.find('月') != -1 and s.find('日') != -1):
            if(s.find('-') != -1):
                s = s.split('-')[0]
            if(s.find('—') != -1):
                s = s.split('—')[0]
            return time.strptime(s, "%Y年%m月%d日")
        elif(len(s.split('-')) == 3):
            return time.strptime(s, "%Y-%m-%d")
        elif(len(s.split('/')) == 3):
            return time.strptime(s, "%Y/%m/%d")
        elif(s.find('年') != -1 and s.find('月') != -1 and s.find('号') != -1):
            return time.strptime(s, "%Y年%m月%d号")
        elif(s.find('年') != -1 and s.find('月') != -1):
            if(s.split('月')[1] != ''):
                return time.strptime(s, "%Y年%m月%d")
            else:
                return time.strptime(s, "%Y年%m月")
        elif(s.find('日') != -1 and s.find('月') != -1):
            return time.strptime(s, "%Y月%m月%d日")
    except:
        return time.strptime("1975-1-1", "%Y-%m-%d")


def tag_exist(tag, child, attrs=None):
    if(attrs == None):
        return len(tag.find_all(child)) != 0
    else:
        return len(tag.find_all(child, attrs=attrs)) != 0


def get_country(s):
    ja = re.compile(r'[\u3040-\u309F\u30A0-\u30FF]')
    kr = re.compile(r'[\uAC00-\uD7A3]')
    en = re.compile(
        r'\b(([("]?[a-zA-Z0-9]+[):\'"]?)[\s])*([("]?[a-zA-Z0-9]+[):\'"]?)+[\.\?!,:~]?')
    if ja.search(s):
        return 'ja'
    elif kr.search(s):
        return 'ko'
    elif en.search(s):
        return 'en'
    else:
        return 'zh-cn'


def index_(arr, item):
    try:
        index = arr.index(item)
        return index
    except:
        return -1
