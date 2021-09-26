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
    speak = win32com.client.Dispatch('SAPI.SPVOICE')

    for y in range(1980, 2022):
        print(str(y)+"=======================================")
        animes = bangumi.getfrombangumi(y)
        animes.sort(key=lambda x: int(x.bgm_rank))
        for ani in animes:
            ani.print_3()
        db.write_all_animes(animes)

        winsound.Beep(1000, 1000)
        speak.Speak(str(y)+'年数据导入数据库完成!')
        print(str(y)+'年数据导入数据库完成！')

    winsound.Beep(1000, 1000)
    speak.Speak('导入数据库全部完成!')
    print('导入数据库全部完成！')


if __name__ == "__main__":
    main()
