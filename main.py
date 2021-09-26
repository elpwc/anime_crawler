import moegirl
import bangumi
import anime_class
import winsound
import win32com.client
import db
import time

def main():

    '''
    animes = []
    a=anime_class.Anime('test', '2012')
    a.housou_date = time.strptime("2012-3-9", "%Y-%m-%d")
    a.ani_type = 'ova'

    animes.append(a)

    db.write_all_animes(animes)
    '''
    fo = open("error.log","a")
    fo.write("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +'] start. \n\n')
    fo.close()

    speak = win32com.client.Dispatch('SAPI.SPVOICE')

    moe_animes = []

    #萌百数据，用来参考国籍和类型
    for y in range(2000, 2021):
        moe_animes.append(moegirl.getfrommoegirl(y))
        print(str(y)+' moe')
    print('萌百数据获取完成！')
    winsound.Beep(1000, 1000)
    speak.Speak('萌百数据获取完成!')
    fo = open("error.log","a")
    fo.write("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +'] done with data from moegirlswiki. \n\n')
    fo.close()

    #正式获取bangumi数据
    for y in range(1980, 2022):
        print(str(y)+"=======================================")
        animes = bangumi.getfrombangumi(y, -1, moe_animes)
        animes.sort(key=lambda x: int(x.bgm_rank))
        for ani in animes:
            ani.print_3()
        #写入DB
        db.write_all_animes(animes)

        print(str(y)+'年数据导入数据库完成！')
        winsound.Beep(1000, 1000)
        speak.Speak(str(y)+'年数据导入数据库完成!')
        fo = open("error.log","a")
        fo.write("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +'] done with '+str(y)+' \n\n')
        fo.close()
        
    print('导入数据库全部完成！')
    winsound.Beep(1000, 1000)
    speak.Speak('导入数据库全部完成!')
    fo = open("error.log","a")
    fo.write("["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +'] complete. \n\n')
    fo.close()

if __name__ == "__main__":
    main()
