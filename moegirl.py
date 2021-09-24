import requests
from bs4 import BeautifulSoup
import anime_class


def getfrom2000to2012(year):
    return


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
        print('yanzhenma')
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
                for j in range(i, i+7, 1):
                    anis = trs[j].find_all('a')
                    if(len(anis) != 0):
                        for ani in anis:
                            ani = anime_class.Anime(ani.text, year)
                            ani.season = str(int((i-4)/10))
                            ani.country = "ja"
                            res.append(ani)
    return res
