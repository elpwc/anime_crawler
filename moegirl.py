import requests
from bs4 import BeautifulSoup
import anime_class
import winsound
import win32com.client


def getfrommoegirl(year):
    if(year >= 2000 & year <= 2012):
        return getfrom2000to2012(year)
    elif(year >= 2013):
        return getafter2013(year)
    else:
        return None


def getfrom2000to2012(year):
    res = []
    url = R"https://zh.moegirl.org.cn/Template:日本"+str(year)+"年动画"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, "html.parser")
    anitable = soup.find_all(name='table', attrs={"class": "navbox"})
    if(len(anitable) == 0):
        speak = win32com.client.Dispatch('SAPI.SPVOICE')
        winsound.Beep(1000, 1000)
        speak.Speak('爬取'+str(year)+'年时出现了验证码，请尽快处理!')
        print('CAPTCHAが しゅつげん しました！はやく つかまえろ！')
    else:
        anitable = anitable[0]
        trs = anitable.tbody.tr.td.table.tbody.find_all(
            name='tr', attrs={"style": ""})
        if(len(trs) > 0):
            '''
            a=0
            for tr in trs:
              a+=1
              print(tr.text+"\r\n"+str(a)+"-------------------------------------------\r\n")
            '''
            # 第2 3 4 5 6ova 7movie个(0 kara)
            for i in range(2, 8, 1):
                #2004年的查论辩没有OVA和电影列表
                if(year == 2004 and i >= 6):
                    break
                anis = trs[i].find_all('a')
                if(len(anis) != 0):
                    for ani in anis:
                        anime = anime_class.Anime(ani.text, year)
                        anime.country = "ja"
                        # 标记页面不存在
                        if(ani.attrs['title'].find('（页面不存在）') != -1):
                            anime.moe_no_page = False
                        if(i == 6):  # ova
                            anime.ani_type = 'ova'
                        elif(i == 7):  # movie
                            anime.ani_type = 'movie'
                        else:
                            anime.season = str(int(i-2))
                            anime.ani_type = 'anime'
                        res.append(anime)
    return res


def getafter2013(year):
    res = []
    url = R"https://zh.moegirl.org.cn/Template:日本"+str(year)+"年动画"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'

    '''
    fo = open(R"E:\Develop\Web\Project_Anime_Seiri\anime_crawler\test.txt","w+", encoding='utf-8')
    fo.write(r.text)
    fo.close()
    '''
    # print(r.text)

    soup = BeautifulSoup(r.text, "html.parser")
    anitable = soup.find_all(name='table', attrs={"class": "navbox"})
    if(len(anitable) == 0):
        speak = win32com.client.Dispatch('SAPI.SPVOICE')
        winsound.Beep(1000, 1000)
        speak.Speak('爬取'+str(year)+'年时出现了验证码，请尽快处理!')
        print('CAPTCHAが しゅつげん しました！はやく つかまえろ！')
    else:
        anitable = anitable[0]
        trs = anitable.tbody.tr.td.table.tbody.find_all(
            name='tr', attrs={"style": ""})
        if(len(trs) >= 40):
            '''
            a=0
            for tr in trs:
              a+=1
              print(tr.text+"\r\n"+str(a)+"-------------------------------------------\r\n")
            '''
            # 第4-10 14-20 24-30 34-40个(0 kara)
            for i in range(4, 35, 10):
                for j in range(i, i+8, 1):
                    anis = trs[j].find_all('a')
                    if(len(anis) != 0):
                        for ani in anis:
                            anime = anime_class.Anime(ani.text, year)
                            anime.country = "ja"
                            # 标记页面不存在
                            if(ani.attrs['title'].find('（页面不存在）') == -1):
                                anime.moe_no_page = True
                            # 一周七天
                            if(j == i+7):
                                anime.season = str(int((i-4)/10))
                                anime.ani_type = 'anime'
                            # OVA
                            else:
                                anime.ani_type = 'ova'
                            res.append(anime)
    return res
