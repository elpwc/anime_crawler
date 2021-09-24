import moegirl
import bangumi
import anime_class
import winsound
import win32com.client
import db
import time



def main():
    animes = []
    a=anime_class.Anime('test', '2012')
    a.housou_date = time.strptime("2012-3-9", "%Y-%m-%d")
    a.ani_type = 'ova'

    animes.append(a)

    db.write_all_animes(animes)

    '''
    animes = bangumi.getfrombangumi(1995)
    animes.sort(key=lambda x: int(x.bgm_rank))
    for ani in animes:
        ani.print_3()
    '''


if __name__ == "__main__":
    main()
