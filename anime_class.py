import time


class Anime:
    name = ''
    jp_name = ''

    bangumi_id = ''
    moe_no_page = False
    bgm_no_page = False

    country = ''

    img_url = ''

    year = -1
    season = -1  # 0,1,2,3
    housou_date = time.strptime("1975.01.01", "%Y.%m.%d")

    episode = ''

    officialpage = ''
    playpage = ''
    ani_type = ''  # anime ova movie

    bgm_rank = -1

    def __init__(self, name, year):
        self.name = name
        self.year = year

    def print_(self):
        print("{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}".format(
            self.name,
            self.jp_name,
            self.bangumi_id,
            self.country,
            self.img_url,
            self.year, self.season, self.housou_date, self.episode,
            self.officialpage, self.playpage
        ))

    def print_2(self):  # for moe
        print("{:^10}{:^5}{:^10}{:^15}".format(
            self.year, self.season, self.ani_type, self.name
        ))

    def print_3(self):  # for bgm
        print("{:^12}{:^3}{:^5}{:^5}{:^5}{:^8}{:^5}{:^15}{:^15}".format(
            time.strftime(
                "%Y-%m-%d", self.housou_date), self.season, self.bgm_rank, self.country, self.ani_type, self.bangumi_id, self.episode, self.name, self.jp_name
        ))
