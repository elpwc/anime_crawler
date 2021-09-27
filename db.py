import dbcfg
import anime_class
import time
import pymysql
import bangumi


def connect():
    return pymysql.connect(host=dbcfg.host, port=dbcfg.port, db=dbcfg.db, user=dbcfg.user, password=dbcfg.password)


def access(sql, cs, cursor):
    data = None
    try:
        cursor.execute(sql)
        cs.commit()
        data = cursor.fetchone()
        # print(data)
    except:
        print('error in \r\n:' + sql)
        fo = open("log/error.log", "a")
        fo.write("["+time.strftime("%Y-%m-%d %H:%M:%S",
                 time.localtime()) + '] error in \n:' + sql + "\n\n")
        fo.close()
        cs.rollback
    return data


def write_anime(ani, cs, cursor):
    sql = (R"""
    INSERT INTO anime (name, ori_name, country, type, housou_stat, housou_date, year, season, episode, episode_type, epi_length_type, moe_no_page, bgm_no_page, image_url, bangumi_id, bangumi_rank) 
    VALUES ('""" +
           ani.name.replace('\'', '\'\'')+"', '" +
           ani.jp_name.replace('\'', '\'\'')+"', " +
           str(country_to_dbtype(ani.country))+', ' +
           str(ani_type_to_dbtype(ani.ani_type))+', ' +
           str(ani.housou_stat)+', ' +
           "STR_TO_DATE('" + time.strftime("%Y-%m-%d", ani.housou_date) + "', '%Y-%m-%d')"+', ' +
           str(ani.year)+', ' +
           str(ani.season)+', ' +
           str(ani.episode)+', ' +
           str(get_episode_type(int(ani.episode)))+', ' +
           str(ani.len_)+', ' +
           str(ani.moe_no_page)+', ' +
           str(ani.bgm_no_page)+', "' +
           ani.img_url+'", ' +
           str(ani.bangumi_id)+', ' +
           str(ani.bgm_rank) +
           ');')
    # print(sql)
    access(sql, cs, cursor)

    id = access("SELECT id FROM anime WHERE bangumi_id=" +
                ani.bangumi_id + ";", cs, cursor)

    if(id != None):
        # print(id)
        # print(id[0])
        cn = ''
        ja = ''
        en = ''
        ko = ''

        if (bangumi.get_country(ani.name) == 'zh-cn' or bangumi.get_country(ani.name) == 'en'):
            cn = ani.name
        if ani.country == 'ja':
            ja = ani.jp_name
        if ani.country == 'en':
            en = ani.jp_name
        if ani.country == 'ko':
            ko = ani.jp_name

        sql = (
            R'''
        INSERT INTO anime_name (anime_id, zh_cn, ja, en, ko) 
        VALUES (''' +
            str(id[0])+", '" +
            cn.replace('\'', '\'\'') + "', '" +
            ja.replace('\'', '\'\'') + "', '" +
            en.replace('\'', '\'\'') + "', '" +
            ko.replace('\'', '\'\'') +
            "');")
        access(sql, cs, cursor)


def write_all_animes(animes):
    conn = connect()
    cursor = conn.cursor()
    i = 0
    for ani in animes:
        i += 1
        print(str(i)+" in "+str(len(animes))+": " +
              str(ani.year)+" "+ani.name)
        write_anime(ani, conn, cursor)
    cursor.close()
    conn.close()


def ani_type_to_dbtype(anitype):
    if(anitype == 'tv'):
        return '0'
    elif(anitype == 'web'):
        return '1'
    elif(anitype == 'ova'):
        return '2'
    elif(anitype == 'movie'):
        return '3'
    else:
        return '4'


def country_to_dbtype(c):
    if(c == 'ja'):
        return '0'
    elif(c == 'zh-cn'):
        return '1'
    elif(c == 'en'):
        return '2'
    elif(c == 'ko'):
        return '3'
    elif(c == 'zh-tw'):
        return '4'
    elif(c == 'other'):
        return '5'
    else:
        return '5'


def get_episode_type(epi):
    if(epi == 1):
        return 0
    elif(epi >= 2 and epi <= 5):
        return 1
    elif(epi >= 6 and epi <= 19):
        return 2
    elif(epi >= 20 and epi <= 50):
        return 3
    else:
        return 4
