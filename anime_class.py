class Anime:
    name = ''
    jp_name = ''

    bangumi_id = ''
    moegirl_link = ''
    no_page = ''

    country = ''

    img_url = ''

    year = -1
    season = -1  # 0,1,2,3
    housou_date = ''

    episode = ''

    officialpage = ''
    playpage = ''

    def __init__(self, name, year):
        self.name = name
        self.year = year

    def print_(self):
        print("{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}".format(
            self.name,
            self.jp_name,
            self.bangumi_id, self.moegirl_link, self.no_page,
            self.country,
            self.img_url,
            self.year, self.season, self.housou_date, self.episode,
            self.officialpage, self.playpage
        ))

    def print_2(self):
        print("{:^10}{:^5}{:^15}".format(
            self.year, self.season, self.name
        ))
