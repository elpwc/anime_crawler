import dbcfg
import anime_class
import time
import pymysql
import bangumi


def connect():
    return pymysql.connect(host=dbcfg.host, port=dbcfg.port, db=dbcfg.db, user=dbcfg.user, password=dbcfg.password)


def access(sql, cs):
    cs.execute(sql)
    data = cs.fetchone()
    print (data)
    return data


def write_anime(ani, cs):
    access(
      '''
      INSERT INTO anime (name, country, type, housou_date, episode, moe_no_page, bgm_no_page, image_url, bangumi_id, bangumi_rank) 
      VALUES ("'''+
      ani.name+'", "'+
      ani.country+'", "'+
      ani_type_to_dbtype(ani.ani_type)+'", "'+
      "to_date('"+ time.strftime("%Y-%m-%d", ani.housou_date) +"', ''YYYY-MM-DD)"+'", "'+
      str(ani.episode)+'", "'+
      str(ani.moe_no_page)+'", "'+
      str(ani.bgm_no_page)+'", "'+
      ani.img_url+'", "'+
      ani.bangumi_id+'", "'+
      ani.bangumi_rank+
      ');'
      ,
      cs
    )

    id = access("SELECT id FROM anime WHERE bangumi_id='" + ani.bangumi_id + "';")
    #TODO：加个判断空结果的在这，请

    id = id['id']

    access(
      '''
      INSERT INTO anime_name (anime_id, zh_cn, ja, en, ko) 
      VALUES ("'''+
      id+'", "'+
      ani.name if bangumi.get_country(ani.name) == 'zh-cn' or bangumi.get_country(ani.name) == 'en' else ''+'", "'+
      ani.jp_name if ani.country == 'ja' else ''+'", "'+
      ani.jp_name if ani.country == 'en' else ''+'", "'+
      ani.jp_name if ani.country == 'ko' else ''+
      ');'
      ,
      cs
    )
    

def write_all_animes(animes):
    conn = connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    for ani in animes:
      write_anime(ani , cursor)
    cursor.close()
    conn.close()

def ani_type_to_dbtype(anitype):
    if(anitype == 'anime'):
      return '0'
    elif(anitype == 'ova'):
      return '1'
    elif(anitype == 'movie'):
      return '2'
    else:
      return '0'
