import moegirl
import bangumi
import anime_class


def main():
    animes = moegirl.getafter2013(2021)
    for ani in animes:
        ani.print_2()


if __name__ == "__main__":
    main()
