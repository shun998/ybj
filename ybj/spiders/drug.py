import pymysql
import requests

url = 'https://fw.ybj.beijing.gov.cn/drug/druginfo/findChiledLimit'
data = {"line": 1,
        "levelnum": 0,
        "cpage": 1}
for i in range(1, 194):
    data["cpage"] = i
    drugs = requests.post(url=url, params=data).json()
    drugs_list = drugs["chiled"]
    for j in drugs_list:
        # ID = j['ID']
        # DRUGNAME = j['DRUGNAME']
        # DRUGFACTS = j['DRUGFACTS']
        # DRUGTYPE = j['DRUGTYPE']
        # DRUGDOSAGE = j['DRUGDOSAGE']
        # DRUGNUMS = j['DRUGNUMS']
        # print(j)

        try:
            conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='ybj',
                                   charset="utf8")

            cursor = conn.cursor()
            # 数据

            insert_sql = """
                        insert into `t_drug`(`ID`,  `DRUGNAME`,  `DRUGFACTS`,  `DRUGTYPE`,   `DRUGDOSAGE`, `DRUGNUMS`)
                        values(%s, %s,%s, %s,%s, %s)
                    """
            cursor.execute(insert_sql,
                           (j['ID'], j['DRUGNAME'], j['DRUGFACTS'], j['DRUGTYPE'], j['DRUGDOSAGE'], j['DRUGNUMS']))

            print('save to mysql')
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print('wrong' + str(e))
