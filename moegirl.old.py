import requests
from bs4 import BeautifulSoup
import anime_class


def getafter2013_(year):
    res = []
    for i in range(0, 4):
        res += getafter2013season_(year, i)
    return res


def getafter2013season_(year, season):
    res = []
    url = ""
    if season == 0:
        url = "https://zh.moegirl.org.cn/日本"+str(year)+"年冬季动画"
    elif season == 1:
        url = "https://zh.moegirl.org.cn/日本"+str(year)+"年春季动画"
    elif season == 2:
        url = "https://zh.moegirl.org.cn/日本"+str(year)+"年夏季动画"
    elif season == 3:
        url = "https://zh.moegirl.org.cn/日本"+str(year)+"年秋季动画"
    else:
        return False

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'

    fo = open(R"E:\Develop\Web\Project_Anime_Seiri\anime_crawler\test.txt",
              "w+", encoding='utf-8')
    fo.write(r.text)
    fo.close()
    # print(r.text)

    soup = BeautifulSoup(r.text, "html.parser")
    anidiv = soup.find_all(name='div', attrs={"class": "toc"})
    if(len(anidiv) == 0):
        print('yanzhenma')
    else:
        anidiv = anidiv[0].ul
        lis = anidiv.find_all('li')
        for li in lis:
            if(len(li.find_all('ul')) != 0):
                spans = li.find_all('span')
                if(len(spans) >= 2):
                    if(spans[1].text != '导航'):
                        if(spans[1].text != '参见'):
                            ani = anime_class.Anime(spans[1].text, year)
                            ani.season = season
                            ani.country = "ja"
                            res.append(ani)
    return res
