import moegirl
import bangumi
import anime_class
import winsound
import win32com.client


def main():
    #animes = moegirl.getafter2013(2021)
    #animes = moegirl.getfrom2000to2012(2000)
    animes = bangumi.getfrombangumi(1995)
    animes.sort(key=lambda x: int(x.bgm_rank))
    for ani in animes:
        ani.print_3()


if __name__ == "__main__":
    main()
