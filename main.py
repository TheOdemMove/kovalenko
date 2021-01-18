import hashlib
import os
import time
import datetime
from fpdf import FPDF

import pymysql
from flask import Flask, render_template, request, redirect, session
from pymysql.cursors import DictCursor

app = Flask(__name__)
# app.permanent_session_lifetime = datetime.timedelta(minutes=59)
app.secret_key = os.urandom(24)


def get_info(id):
    global result_info
    result_info = []
    con = pymysql.connect(host='localhost', user='root', password='1111', db='user', charset='utf8mb4',
                          cursorclass=DictCursor)
    cur = con.cursor()
    cur.execute("SELECT * FROM bd_result WHERE id={}".format(id))
    result = cur.fetchall()
    for row in result:
        result_info.append(row["ID"])
        result_info.append(row["datet"])
        result_info.append(row["ssurname"])
        result_info.append(row["sname"])
        result_info.append(row["secname"])
        result_info.append(row["bdate"])
        result_info.append(row["timestart"])
        result_info.append(row["timefinish"])
        dost_2 = int(row["dostovirnist"])
        oap_2 = int(row["os_potencial"])
        pr_2 = int(row["regul"])
        kp_2 = int(row["commun"])
        mn_2 = int(row["moral"])
        vps_2 = int(row["militar"])
        dap_2 = int(row["deviant"])
        sz_2 = int(row["suicide"])
    analitics_admin(dost_2, oap_2, pr_2, kp_2, mn_2, vps_2, dap_2, sz_2)


def get_login():
    con = pymysql.connect(host='localhost', user='root', password='1111', db='user', charset='utf8mb4',
                          cursorclass=DictCursor)
    cur = con.cursor()
    cur.execute("SELECT * FROM user_root order by ID")
    result = cur.fetchall()
    return result


def getdb():
    con = pymysql.connect(host='localhost', user='root', password='1111', db='user', charset='utf8mb4',
                          cursorclass=DictCursor)
    cur = con.cursor()
    cur.execute("SELECT * FROM info order by ID")
    result = cur.fetchall()
    return result


def getdb_2():
    con = pymysql.connect(host='localhost', user='root', password='1111', db='user', charset='utf8mb4',
                          cursorclass=DictCursor)
    cur = con.cursor()
    cur.execute("SELECT * FROM bd_result order by ID")
    result = cur.fetchall()
    return result


def insert_bd_result():
    connection = pymysql.connect(host='localhost', user='root', password='1111', db='USER', charset='utf8mb4',
                                 cursorclass=DictCursor, autocommit=True)

    temp = datetime.datetime.now()
    datet = str(temp.strftime("%d.%m.%y"))

    cmd = "INSERT INTO bd_result (ssurname, sname, secname, bdate, descr, ooc, timestart, timefinish, datet, dostovirnist, os_potencial, regul, commun, moral, militar, deviant, suicide) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
        bd_result[0], bd_result[1], bd_result[2], bd_result[3], bd_result[4], bd_result[5], timestart, timefinish,
        datet, bd_result[6], bd_result[7], bd_result[8], bd_result[9], bd_result[10], bd_result[11], bd_result[12],
        bd_result[13])
    cursor = connection.cursor()
    cursor.execute(cmd)
    connection.close()  ######


def insert_user_root(uname, upass):
    connection = pymysql.connect(host='localhost', user='root', password='1111', db='USER', charset='utf8mb4',
                                 cursorclass=DictCursor, autocommit=True)
    cmd = "INSERT INTO user_root (username, upassword) values ('{}', '{}')".format(uname, upass)
    cursor = connection.cursor()
    cursor.execute(cmd)
    connection.close()


def delete_user_root(id):
    connection = pymysql.connect(host='localhost', user='root', password='1111', db='USER', charset='utf8mb4',
                                 cursorclass=DictCursor, autocommit=True)
    cmd = "DELETE FROM user_root WHERE id={}".format(id)
    cursor = connection.cursor()
    cursor.execute(cmd)
    connection.close()


def analitics_admin(dost_2, oap_2, pr_2, kp_2, mn_2, vps_2, dap_2, sz_2):
    # достовірність обстежень
    if dost_2 >= 0 and dost_2 <= 5:
        result_info.append(str(dost_2))
        result_info.append(sten_dost[0])
    elif dost_2 >= 6 and dost_2 <= 9:
        result_info.append(str(dost_2))
        result_info.append(sten_dost[1])
    elif dost_2 >= 10:
        result_info.append(str(dost_2))
        result_info.append(sten_dost[2])

    # Рівень бойової стійкості
    if oap_2 >= 87:
        result_info.append(str(oap_2))
        result_info.append(sten_oap[3])
    elif oap_2 >= 75 and oap_2 <= 86:
        result_info.append(str(oap_2))
        result_info.append(sten_oap[3])
    elif oap_2 >= 63 and oap_2 <= 74:
        result_info.append(str(oap_2))
        result_info.append(sten_oap[2])
    elif oap_2 >= 51 and oap_2 <= 62:
        result_info.append(str(oap_2))
        result_info.append(sten_oap[2])
    elif oap_2 >= 40 and oap_2 <= 50:
        result_info.append(str(oap_2))
        result_info.append(sten_oap[1])
    elif oap_2 >= 31 and oap_2 <= 39:
        result_info.append(str(oap_2))
        result_info.append(sten_oap[1])
    elif oap_2 >= 25 and oap_2 <= 30:
        result_info.append(str(oap_2))
        result_info.append(sten_oap[1])
    elif oap_2 >= 21 and oap_2 <= 24:
        result_info.append(str(oap_2))
        result_info.append(sten_oap[0])
    elif oap_2 >= 18 and oap_2 <= 20:
        result_info.append(str(oap_2))
        result_info.append(sten_oap[0])
    elif oap_2 < 17:
        result_info.append(str(oap_2))
        result_info.append(sten_oap[0])

    # поведінкова регуляція
    if pr_2 >= 57:
        result_info.append(str(pr_2))
        result_info.append(sten_pr[7])
    elif pr_2 >= 46 and pr_2 <= 56:
        result_info.append(str(pr_2))
        result_info.append(sten_pr[6])
    elif pr_2 >= 35 and pr_2 <= 45:
        result_info.append(str(pr_2))
        result_info.append(sten_pr[5])
    elif pr_2 >= 27 and pr_2 <= 34:
        result_info.append(str(pr_2))
        result_info.append(sten_pr[4])
    elif pr_2 >= 19 and pr_2 <= 26:
        result_info.append(str(pr_2))
        result_info.append(sten_pr[3])
    elif pr_2 >= 13 and pr_2 <= 18:
        result_info.append(str(pr_2))
        result_info.append(sten_pr[2])
    elif pr_2 >= 9 and pr_2 <= 12:
        result_info.append(str(pr_2))
        result_info.append(sten_pr[1])
    elif pr_2 >= 6 and pr_2 <= 8:
        result_info.append(str(pr_2))
        result_info.append(sten_pr[0])
    elif pr_2 == 5:
        result_info.append(str(pr_2))
        result_info.append(sten_pr[0])
    elif pr_2 >= 0 and pr_2 <= 4:
        result_info.append(str(pr_2))
        result_info.append(sten_pr[0])

    if kp_2 >= 23:
        result_info.append(str(kp_2))
        result_info.append(sten_kp[7])
    elif kp_2 >= 20 and kp_2 <= 22:
        result_info.append(str(kp_2))
        result_info.append(sten_kp[6])
    elif kp_2 >= 18 and kp_2 <= 19:
        result_info.append(str(kp_2))
        result_info.append(sten_kp[5])
    elif kp_2 >= 15 and kp_2 <= 17:
        result_info.append(str(kp_2))
        result_info.append(sten_kp[4])
    elif kp_2 >= 13 and kp_2 <= 14:
        result_info.append(str(kp_2))
        result_info.append(sten_kp[3])
    elif kp_2 >= 11 and kp_2 <= 12:
        result_info.append(str(kp_2))
        result_info.append(sten_kp[2])
    elif kp_2 >= 9 and kp_2 <= 10:
        result_info.append(str(kp_2))
        result_info.append(sten_kp[1])
    elif kp_2 >= 7 and kp_2 <= 8:
        result_info.append(str(kp_2))
        result_info.append(sten_kp[0])
    elif kp_2 == 6:
        result_info.append(str(kp_2))
        result_info.append(sten_kp[0])
    elif kp_2 >= 0 and kp_2 <= 5:
        result_info.append(str(kp_2))
        result_info.append(sten_kp[0])

    # морально-етична нормативність
    if mn_2 >= 17:
        result_info.append(str(mn_2))
        result_info.append(sten_mn[8])
    elif mn_2 == 16:
        result_info.append(str(mn_2))
        result_info.append(sten_mn[7])
    elif mn_2 >= 14 and mn_2 <= 15:
        result_info.append(str(mn_2))
        result_info.append(sten_mn[6])
    elif mn_2 >= 12 and mn_2 <= 13:
        result_info.append(str(mn_2))
        result_info.append(sten_mn[5])
    elif mn_2 >= 10 and mn_2 <= 11:
        result_info.append(str(mn_2))
        result_info.append(sten_mn[4])
    elif mn_2 >= 8 and mn_2 <= 9:
        result_info.append(str(mn_2))
        result_info.append(sten_mn[3])
    elif mn_2 == 7:
        result_info.append(str(mn_2))
        result_info.append(sten_mn[2])
    elif mn_2 >= 5 and mn_2 <= 6:
        result_info.append(str(mn_2))
        result_info.append(sten_mn[1])
    elif mn_2 == 4:
        result_info.append(str(mn_2))
        result_info.append(sten_mn[0])
    elif mn_2 >= 0 and mn_2 <= 3:
        result_info.append(str(mn_2))
        result_info.append(sten_mn[0])

    # Військово професійна спрямованість
    if vps_2 > 25:
        result_info.append(str(vps_2))
        result_info.append(sten_vps[4])
    elif vps_2 >= 18 and vps_2 <= 25:
        result_info.append(str(vps_2))
        result_info.append(sten_vps[4])
    elif vps_2 >= 16 and vps_2 <= 17:
        result_info.append(str(vps_2))
        result_info.append(sten_vps[4])
    elif vps_2 >= 14 and vps_2 <= 15:
        result_info.append(str(vps_2))
        result_info.append(sten_vps[4])
    elif vps_2 >= 11 and vps_2 <= 13:
        result_info.append(str(vps_2))
        result_info.append(sten_vps[3])
    elif vps_2 >= 8 and vps_2 <= 10:
        result_info.append(str(vps_2))
        result_info.append(sten_vps[2])
    elif vps_2 >= 5 and vps_2 <= 7:
        result_info.append(str(vps_2))
        result_info.append(sten_vps[1])
    elif vps_2 == 4:
        result_info.append(str(vps_2))
        result_info.append(sten_vps[1])
    elif vps_2 >= 2 and vps_2 <= 3:
        result_info.append(str(vps_2))
        result_info.append(sten_vps[0])
    elif vps_2 == 1:
        result_info.append(str(vps_2))
        result_info.append(sten_vps[0])
    elif vps_2 == 0:
        result_info.append(str(vps_2))
        result_info.append(sten_vps[0])

    # Девіантні форми поведінки
    if dap_2 >= 25:
        result_info.append(str(dap_2))
        result_info.append(sten_dap[3])
    elif dap_2 >= 21 and dap_2 <= 24:
        result_info.append(str(dap_2))
        result_info.append(sten_dap[3])
    elif dap_2 >= 18 and dap_2 <= 20:
        result_info.append(str(dap_2))
        result_info.append(sten_dap[2])
    elif dap_2 >= 15 and dap_2 <= 17:
        result_info.append(str(dap_2))
        result_info.append(sten_dap[2])
    elif dap_2 >= 12 and dap_2 <= 14:
        result_info.append(str(dap_2))
        result_info.append(sten_dap[1])
    elif dap_2 >= 10 and dap_2 <= 11:
        result_info.append(str(dap_2))
        result_info.append(sten_dap[0])
    elif dap_2 >= 8 and dap_2 <= 9:
        result_info.append(str(dap_2))
        result_info.append(sten_dap[0])
    elif dap_2 >= 6 and dap_2 <= 7:
        result_info.append(str(dap_2))
        result_info.append(sten_dap[0])
    elif dap_2 >= 4 and dap_2 <= 5:
        result_info.append(str(dap_2))
        result_info.append(sten_dap[0])
    elif dap_2 >= 0 and dap_2 <= 3:
        result_info.append(str(dap_2))
        result_info.append(sten_dap[0])

    # Суїцидальний ризик
    if sz_2 >= 15:
        result_info.append(str(sz_2))
        result_info.append(sten_sz[3])
    elif sz_2 >= 10 and sz_2 <= 14:
        result_info.append(str(sz_2))
        result_info.append(sten_sz[3])
    elif sz_2 >= 7 and sz_2 <= 9:
        result_info.append(str(sz_2))
        result_info.append(sten_sz[2])
    elif sz_2 >= 5 and sz_2 <= 6:
        result_info.append(str(sz_2))
        result_info.append(sten_sz[2])
    elif sz_2 == 4:
        result_info.append(str(sz_2))
        result_info.append(sten_sz[1])
    elif sz_2 == 3:
        result_info.append(str(sz_2))
        result_info.append(sten_sz[0])
    elif sz_2 == 2:
        result_info.append(str(sz_2))
        result_info.append(sten_sz[0])
    elif sz_2 == 1:
        result_info.append(str(sz_2))
        result_info.append(sten_sz[0])
    elif sz_2 == 0:
        result_info.append(str(sz_2))
        result_info.append(sten_sz[0])


def analitics():
    # достовірність обстежень
    if dost >= 0 and dost <= 5:
        print("Достовірність: " + str(dost))
        print(sten_dost[0])
    elif dost >= 6 and dost <= 9:
        print("Достовірність: " + str(dost))
        print(sten_dost[1])
    elif dost >= 10:
        print("Достовірність: " + str(dost))
        print(sten_dost[2])

    # Рівень бойової стійкості
    if oap >= 87:
        print("Особистий адаптаційний потенціал: " + str(oap))
        print(sten_oap[3])
    elif oap >= 75 and oap <= 86:
        print("Особистий адаптаційний потенціал: " + str(oap))
        print(sten_oap[3])
    elif oap >= 63 and oap <= 74:
        print("Особистий адаптаційний потенціал: " + str(oap))
        print(sten_oap[2])
    elif oap >= 51 and oap <= 62:
        print("Особистий адаптаційний потенціал: " + str(oap))
        print(sten_oap[2])
    elif oap >= 40 and oap <= 50:
        print("Особистий адаптаційний потенціал: " + str(oap))
        print(sten_oap[1])
    elif oap >= 31 and oap <= 39:
        print("Особистий адаптаційний потенціал: " + str(oap))
        print(sten_oap[1])
    elif oap >= 25 and oap <= 30:
        print("Особистий адаптаційний потенціал: " + str(oap))
        print(sten_oap[1])
    elif oap >= 21 and oap <= 24:
        print("Особистий адаптаційний потенціал: " + str(oap))
        print(sten_oap[0])
    elif oap >= 18 and oap <= 20:
        print("Особистий адаптаційний потенціал: " + str(oap))
        print(sten_oap[0])
    elif oap < 17:
        print("Особистий адаптаційний потенціал: " + str(oap))
        print(sten_oap[0])

    # поведінкова регуляція
    if pr >= 57:
        print("Поведінкова регуляція: " + str(pr))
        print(sten_pr[7])  # 1 sten
    elif pr >= 46 and pr <= 56:
        print("Поведінкова регуляція: " + str(pr))
        print(sten_pr[6])  # 2 sten
    elif pr >= 35 and pr <= 45:
        print("Поведінкова регуляція: " + str(pr))
        print(sten_pr[5])  # 3 sten
    elif pr >= 27 and pr <= 34:
        print("Поведінкова регуляція: " + str(pr))
        print(sten_pr[4])  # 4 sten
    elif pr >= 19 and pr <= 26:
        print("Поведінкова регуляція: " + str(pr))
        print(sten_pr[3])  # 5 sten
    elif pr >= 13 and pr <= 18:
        print("Поведінкова регуляція: " + str(pr))
        print(sten_pr[2])  # 6 sten
    elif pr >= 9 and pr <= 12:
        print("Поведінкова регуляція: " + str(pr))
        print(sten_pr[1])  # 7 sten
    elif pr >= 6 and pr <= 8:
        print("Поведінкова регуляція: " + str(pr))
        print(sten_pr[0])  # 8 sten
    elif pr == 5:
        print("Поведінкова регуляція: " + str(pr))
        print(sten_pr[0])  # 9 sten
    elif pr >= 0 and pr <= 4:
        print("Поведінкова регуляція: " + str(pr))
        print(sten_pr[0])  # 10 sten

    if kp >= 23:
        print("Комунікативний потенціал: " + str(kp))
        print(sten_kp[7])  # 1 sten
    elif kp >= 20 and kp <= 22:
        print("Комунікативний потенціал: " + str(kp))
        print(sten_kp[6])  # 2 sten
    elif kp >= 18 and kp <= 19:
        print("Комунікативний потенціал: " + str(kp))
        print(sten_kp[5])  # 3 sten
    elif kp >= 15 and kp <= 17:
        print("Комунікативний потенціал: " + str(kp))
        print(sten_kp[4])  # 4 sten
    elif kp >= 13 and kp <= 14:
        print("Комунікативний потенціал: " + str(kp))
        print(sten_kp[3])  # 5 sten
    elif kp >= 11 and kp <= 12:
        print("Комунікативний потенціал: " + str(kp))
        print(sten_kp[2])  # 6 sten
    elif kp >= 9 and kp <= 10:
        print("Комунікативний потенціал: " + str(kp))
        print(sten_kp[1])  # 7 sten
    elif kp >= 7 and kp <= 8:
        print("Комунікативний потенціал: " + str(kp))
        print(sten_kp[0])  # 8 sten
    elif kp == 6:
        print("Комунікативний потенціал: " + str(kp))
        print(sten_kp[0])  # 9 sten
    elif kp >= 0 and kp <= 5:
        print("Комунікативний потенціал: " + str(kp))
        print(sten_kp[0])  # 10 sten

    # морально-етична нормативність
    if mn >= 17:
        print("Морально-етична нормативність: " + str(mn))
        print(sten_mn[8])  # 1 sten
    elif mn == 16:
        print("Морально-етична нормативність: " + str(mn))
        print(sten_mn[7])  # 2 sten
    elif mn >= 14 and mn <= 15:
        print("Морально-етична нормативність: " + str(mn))
        print(sten_mn[6])  # 3 sten
    elif mn >= 12 and mn <= 13:
        print("Морально-етична нормативність: " + str(mn))
        print(sten_mn[5])  # 4 sten
    elif mn >= 10 and mn <= 11:
        print("Морально-етична нормативність: " + str(mn))
        print(sten_mn[4])  # 5 sten
    elif mn >= 8 and mn <= 9:
        print("Морально-етична нормативність: " + str(mn))
        print(sten_mn[3])  # 6 sten
    elif mn == 7:
        print("Морально-етична нормативність: " + str(mn))
        print(sten_mn[2])  # 7 sten
    elif mn >= 5 and mn <= 6:
        print("Морально-етична нормативність: " + str(mn))
        print(sten_mn[1])  # 8 sten
    elif mn == 4:
        print("Морально-етична нормативність: " + str(mn))
        print(sten_mn[0])  # 9 sten
    elif mn >= 0 and mn <= 3:
        print("Морально-етична нормативність: " + str(mn))
        print(sten_mn[0])  # 10 sten

    # Військово професійна спрямованість
    if vps > 25:
        print("Військово-професійна спрямованість: " + str(vps))
        print(sten_vps[4])  # 1 sten
    elif vps >= 18 and vps <= 25:
        print("Військово-професійна спрямованість: " + str(vps))
        print(sten_vps[4])  # 1 sten
    elif vps >= 16 and vps <= 17:
        print("Військово-професійна спрямованість: " + str(vps))
        print(sten_vps[4])  # 2 sten
    elif vps >= 14 and vps <= 15:
        print("Військово-професійна спрямованість: " + str(vps))
        print(sten_vps[4])  # 3 sten
    elif vps >= 11 and vps <= 13:
        print("Військово-професійна спрямованість: " + str(vps))
        print(sten_vps[3])  # 4 sten
    elif vps >= 8 and vps <= 10:
        print("Військово-професійна спрямованість: " + str(vps))
        print(sten_vps[2])  # 5 sten
    elif vps >= 5 and vps <= 7:
        print("Військово-професійна спрямованість: " + str(vps))
        print(sten_vps[1])  # 6 sten
    elif vps == 4:
        print("Військово-професійна спрямованість: " + str(vps))
        print(sten_vps[1])  # 7 sten
    elif vps >= 2 and vps <= 3:
        print("Військово-професійна спрямованість: " + str(vps))
        print(sten_vps[0])  # 8 sten
    elif vps == 1:
        print("Військово-професійна спрямованість: " + str(vps))
        print(sten_vps[0])  # 9 sten
    elif vps == 0:
        print("Військово-професійна спрямованість: " + str(vps))
        print(sten_vps[0])  # 10 sten

    # Девіантні форми поведінки
    if dap >= 25:
        print("Схильніть до девіантних форм поведінки: " + str(dap))
        print(sten_dap[3])  # 1 sten
    elif dap >= 21 and dap <= 24:
        print("Схильніть до девіантних форм поведінки: " + str(dap))
        print(sten_dap[3])  # 2 sten
    elif dap >= 18 and dap <= 20:
        print("Схильніть до девіантних форм поведінки: " + str(dap))
        print(sten_dap[2])  # 3 sten
    elif dap >= 15 and dap <= 17:
        print("Схильніть до девіантних форм поведінки: " + str(dap))
        print(sten_dap[2])  # 4 sten
    elif dap >= 12 and dap <= 14:
        print("Схильніть до девіантних форм поведінки: " + str(dap))
        print(sten_dap[1])  # 5 sten
    elif dap >= 10 and dap <= 11:
        print("Схильніть до девіантних форм поведінки: " + str(dap))
        print(sten_dap[0])  # 6 sten
    elif dap >= 8 and dap <= 9:
        print("Схильніть до девіантних форм поведінки: " + str(dap))
        print(sten_dap[0])  # 7 sten
    elif dap >= 6 and dap <= 7:
        print("Схильніть до девіантних форм поведінки: " + str(dap))
        print(sten_dap[0])  # 8 sten
    elif dap >= 4 and dap <= 5:
        print("Схильніть до девіантних форм поведінки: " + str(dap))
        print(sten_dap[0])  # 9 sten
    elif dap >= 0 and dap <= 3:
        print("Схильніть до девіантних форм поведінки: " + str(dap))
        print(sten_dap[0])  # 10 sten

    # Суїцидальний ризик
    if sz >= 15:
        print("Суїцидальний ризик: " + str(sz))
        print(sten_sz[3])  # 1 sten
    elif sz >= 10 and sz <= 14:
        print("Суїцидальний ризик: " + str(sz))
        print(sten_sz[3])  # 2 sten
    elif sz >= 7 and sz <= 9:
        print("Суїцидальний ризик: " + str(sz))
        print(sten_sz[2])  # 3 sten
    elif sz >= 5 and sz <= 6:
        print("Суїцидальний ризик: " + str(sz))
        print(sten_sz[2])  # 4 sten
    elif sz == 4:
        print("Суїцидальний ризик: " + str(sz))
        print(sten_sz[1])  # 5 sten
    elif sz == 3:
        print("Суїцидальний ризик: " + str(sz))
        print(sten_sz[0])  # 6 sten
    elif sz == 2:
        print("Суїцидальний ризик: " + str(sz))
        print(sten_sz[0])  # 7 sten
    elif sz == 1:
        print("Суїцидальний ризик: " + str(sz))
        print(sten_sz[0])  # 8 sten
    elif sz == 0:
        print("Суїцидальний ризик: " + str(sz))
        print(sten_sz[0])  # 9, 10 sten


def exp(sh):
    global oap
    global dost  # Достовірність
    global pr  # Поведінкова регуляція
    global kp  # Комунікативний потенціал
    global mn  # морально-етична нормативність
    global vps  # військово професійна спрямованість
    global dap  # схильність до девіантних форм поведінки
    global sz  # суїцидальний ризик
    oap = 0
    dost = 0
    pr = 0
    kp = 0
    mn = 0
    vps = 0
    dap = 0
    sz = 0

    # Достовірність
    if sh[6] == 'НІ':
        dost += 1
    if sh[15] == 'НІ':
        dost += 1
    if sh[24] == 'НІ':
        dost += 1
    if sh[36] == 'НІ':
        dost += 1
    if sh[56] == 'НІ':
        dost += 1
    if sh[74] == 'НІ':
        dost += 1
    if sh[83] == 'НІ':
        dost += 1
    if sh[97] == 'НІ':
        dost += 1
    if sh[106] == 'НІ':
        dost += 1
    if sh[121] == 'НІ':
        dost += 1
    if sh[133] == 'НІ':
        dost += 1
    if sh[143] == 'НІ':
        dost += 1
    if sh[153] == 'НІ':
        dost += 1

    #  поведінкова регулярія
    if sh[9] == "ТАК":
        pr += 1
    if sh[11] == "ТАК":
        pr += 1
    if sh[12] == "ТАК":
        pr += 1
    if sh[13] == "ТАК":
        pr += 1
    if sh[16] == "ТАК":
        pr += 1
    if sh[17] == "ТАК":
        pr += 1
    if sh[20] == "ТАК":
        pr += 1
    if sh[21] == "ТАК":
        pr += 1
    if sh[22] == "ТАК":
        pr += 1
    if sh[23] == "ТАК":
        pr += 1
    if sh[25] == "ТАК":
        pr += 1
    if sh[26] == "ТАК":
        pr += 1
    if sh[33] == "ТАК":
        pr += 1
    if sh[34] == "ТАК":
        pr += 1
    if sh[41] == "ТАК":
        pr += 1
    if sh[42] == "ТАК":
        pr += 1
    if sh[44] == "ТАК":
        pr += 1
    if sh[45] == "ТАК":
        pr += 1
    if sh[46] == "ТАК":
        pr += 1
    if sh[52] == "ТАК":
        pr += 1
    if sh[62] == "ТАК":
        pr += 1
    if sh[65] == "ТАК":
        pr += 1
    if sh[68] == "ТАК":
        pr += 1
    if sh[70] == "ТАК":
        pr += 1
    if sh[72] == "ТАК":
        pr += 1
    if sh[73] == "ТАК":
        pr += 1
    if sh[75] == "ТАК":
        pr += 1
    if sh[78] == "ТАК":
        pr += 1
    if sh[85] == "ТАК":
        pr += 1
    if sh[87] == "ТАК":
        pr += 1
    if sh[88] == "ТАК":
        pr += 1
    if sh[89] == "ТАК":
        pr += 1
    if sh[91] == "ТАК":
        pr += 1
    if sh[94] == "ТАК":
        pr += 1
    if sh[99] == "ТАК":
        pr += 1
    if sh[100] == "ТАК":
        pr += 1
    if sh[101] == "ТАК":
        pr += 1
    if sh[103] == "ТАК":
        pr += 1
    if sh[107] == "ТАК":
        pr += 1
    if sh[108] == "ТАК":
        pr += 1
    if sh[113] == "ТАК":
        pr += 1
    if sh[114] == "ТАК":
        pr += 1
    if sh[115] == "ТАК":
        pr += 1
    if sh[116] == "ТАК":
        pr += 1
    if sh[117] == "ТАК":
        pr += 1
    if sh[118] == "ТАК":
        pr += 1
    if sh[120] == "ТАК":
        pr += 1
    if sh[122] == "ТАК":
        pr += 1
    if sh[123] == "ТАК":
        pr += 1
    if sh[124] == "ТАК":
        pr += 1
    if sh[125] == "ТАК":
        pr += 1
    if sh[127] == "ТАК":
        pr += 1
    if sh[128] == "ТАК":
        pr += 1
    if sh[129] == "ТАК":
        pr += 1
    if sh[130] == "ТАК":
        pr += 1
    if sh[132] == "ТАК":
        pr += 1
    if sh[134] == "ТАК":
        pr += 1
    if sh[136] == "ТАК":
        pr += 1
    if sh[140] == "ТАК":
        pr += 1
    if sh[141] == "ТАК":
        pr += 1
    if sh[142] == "ТАК":
        pr += 1
    if sh[144] == "ТАК":
        pr += 1
    if sh[148] == "ТАК":
        pr += 1
    if sh[151] == "ТАК":
        pr += 1
    if sh[154] == "ТАК":
        pr += 1
    if sh[158] == "ТАК":
        pr += 1
    if sh[159] == "ТАК":
        pr += 1
    if sh[160] == "ТАК":
        pr += 1
    if sh[161] == "ТАК":
        pr += 1
    if sh[162] == "ТАК":
        pr += 1
    if sh[163] == "ТАК":
        pr += 1
    if sh[166] == "ТАК":
        pr += 1
    if sh[167] == "ТАК":
        pr += 1
    if sh[7] == "НІ":
        pr += 1
    if sh[8] == "НІ":
        pr += 1
    if sh[10] == "НІ":
        pr += 1
    if sh[28] == "НІ":
        pr += 1
    if sh[30] == "НІ":
        pr += 1
    if sh[37] == "НІ":
        pr += 1
    if sh[43] == "НІ":
        pr += 1
    if sh[49] == "НІ":
        pr += 1
    if sh[50] == "НІ":
        pr += 1
    if sh[57] == "НІ":
        pr += 1
    if sh[58] == "НІ":
        pr += 1
    if sh[59] == "НІ":
        pr += 1
    if sh[60] == "НІ":
        pr += 1
    if sh[63] == "НІ":
        pr += 1
    if sh[67] == "НІ":
        pr += 1
    if sh[71] == "НІ":
        pr += 1
    if sh[80] == "НІ":
        pr += 1
    if sh[92] == "НІ":
        pr += 1
    if sh[110] == "НІ":
        pr += 1
    if sh[137] == "НІ":
        pr += 1
    if sh[139] == "НІ":
        pr += 1
    if sh[145] == "НІ":
        pr += 1

    # комунікативний потенціал
    if sh[14] == "ТАК":
        kp += 1
    if sh[29] == "ТАК":
        kp += 1
    if sh[32] == "ТАК":
        kp += 1
    if sh[48] == "ТАК":
        kp += 1
    if sh[51] == "ТАК":
        kp += 1
    if sh[66] == "ТАК":
        kp += 1
    if sh[69] == "ТАК":
        kp += 1
    if sh[86] == "ТАК":
        kp += 1
    if sh[93] == "ТАК":
        kp += 1
    if sh[95] == "ТАК":
        kp += 1
    if sh[104] == "ТАК":
        kp += 1
    if sh[109] == "ТАК":
        kp += 1
    if sh[111] == "ТАК":
        kp += 1
    if sh[119] == "ТАК":
        kp += 1
    if sh[126] == "ТАК":
        kp += 1
    if sh[131] == "ТАК":
        kp += 1
    if sh[138] == "ТАК":
        kp += 1
    if sh[147] == "ТАК":
        kp += 1
    if sh[156] == "ТАК":
        kp += 1
    if sh[157] == "ТАК":
        kp += 1

    if sh[31] == "НІ":
        kp += 1
    if sh[39] == "НІ":
        kp += 1
    if sh[40] == "НІ":
        kp += 1
    if sh[53] == "НІ":
        kp += 1
    if sh[54] == "НІ":
        kp += 1
    if sh[79] == "НІ":
        kp += 1
    if sh[90] == "НІ":
        kp += 1
    if sh[112] == "НІ":
        kp += 1
    if sh[135] == "НІ":
        kp += 1
    if sh[149] == "НІ":
        kp += 1
    if sh[152] == "НІ":
        kp += 1
    if sh[164] == "НІ":
        kp += 1

    # морально-етична нормативність
    if sh[19] == "ТАК":
        mn += 1
    if sh[29] == "ТАК":
        mn += 1
    if sh[38] == "ТАК":
        mn += 1
    if sh[47] == "ТАК":
        mn += 1
    if sh[55] == "ТАК":
        mn += 1
    if sh[61] == "ТАК":
        mn += 1
    if sh[64] == "ТАК":
        mn += 1
    if sh[76] == "ТАК":
        mn += 1
    if sh[77] == "ТАК":
        mn += 1
    if sh[82] == "ТАК":
        mn += 1
    if sh[84] == "ТАК":
        mn += 1
    if sh[96] == "ТАК":
        mn += 1
    if sh[98] == "ТАК":
        mn += 1
    if sh[146] == "ТАК":
        mn += 1
    if sh[150] == "ТАК":
        mn += 1
    if sh[169] == "ТАК":
        mn += 1
    if sh[170] == "ТАК":
        mn += 1

    if sh[18] == "НІ":
        mn += 1
    if sh[81] == "НІ":
        mn += 1
    if sh[102] == "НІ":
        mn += 1
    if sh[105] == "НІ":
        mn += 1
    if sh[165] == "НІ":
        mn += 1
    if sh[168] == "НІ":
        mn += 1

    # Військово-професійна спрямованість
    if sh[171] == "ТАК":
        vps += 1
    if sh[172] == "ТАК":
        vps += 1
    if sh[173] == "ТАК":
        vps += 1
    if sh[174] == "ТАК":
        vps += 1
    if sh[175] == "ТАК":
        vps += 1
    if sh[177] == "ТАК":
        vps += 1
    if sh[178] == "ТАК":
        vps += 1
    if sh[179] == "ТАК":
        vps += 1
    if sh[180] == "ТАК":
        vps += 1
    if sh[181] == "ТАК":
        vps += 1
    if sh[182] == "ТАК":
        vps += 1
    if sh[184] == "ТАК":
        vps += 1
    if sh[185] == "ТАК":
        vps += 1
    if sh[186] == "ТАК":
        vps += 1
    if sh[188] == "ТАК":
        vps += 1
    if sh[189] == "ТАК":
        vps += 1
    if sh[190] == "ТАК":
        vps += 1
    if sh[191] == "ТАК":
        vps += 1
    if sh[192] == "ТАК":
        vps += 1
    if sh[193] == "ТАК":
        vps += 1
    if sh[195] == "ТАК":
        vps += 1
    if sh[176] == "НІ":
        vps += 1
    if sh[183] == "НІ":
        vps += 1
    if sh[187] == "НІ":
        vps += 1
    if sh[194] == "НІ":
        vps += 1

    # Схильність до девіантних форм поведінки (ДАП)

    if sh[11] == "ТАК":
        dap += 1
    if sh[14] == "ТАК":
        dap += 1
    if sh[19] == "ТАК":
        dap += 1
    if sh[20] == "ТАК":
        dap += 1
    if sh[27] == "ТАК":
        dap += 1
    if sh[41] == "ТАК":
        dap += 1
    if sh[44] == "ТАК":
        dap += 1
    if sh[47] == "ТАК":
        dap += 1
    if sh[52] == "ТАК":
        dap += 1
    if sh[55] == "ТАК":
        dap += 1
    if sh[61] == "ТАК":
        dap += 1
    if sh[64] == "ТАК":
        dap += 1
    if sh[76] == "ТАК":
        dap += 1
    if sh[77] == "ТАК":
        dap += 1
    if sh[96] == "ТАК":
        dap += 1
    if sh[98] == "ТАК":
        dap += 1
    if sh[122] == "ТАК":
        dap += 1
    if sh[132] == "ТАК":
        dap += 1
    if sh[146] == "ТАК":
        dap += 1
    if sh[150] == "ТАК":
        dap += 1
    if sh[156] == "ТАК":
        dap += 1
    if sh[157] == "ТАК":
        dap += 1
    if sh[169] == "ТАК":
        dap += 1
    if sh[196] == "ТАК":
        dap += 1
    if sh[197] == "ТАК":
        dap += 1
    if sh[198] == "ТАК":
        dap += 1
    if sh[199] == "ТАК":
        dap += 1
    if sh[200] == "ТАК":
        dap += 1
    if sh[201] == "ТАК":
        dap += 1
    if sh[202] == "ТАК":
        dap += 1
    if sh[203] == "ТАК":
        dap += 1
    if sh[204] == "ТАК":
        dap += 1
    if sh[205] == "ТАК":
        dap += 1

    if sh[13] == "НІ":
        dap += 1
    if sh[100] == "НІ":
        dap += 1
    if sh[163] == "НІ":
        dap += 1

    # Суїцидальний ризик

    if sh[9] == "ТАК":
        sz += 1
    if sh[13] == "ТАК":
        sz += 1
    if sh[15] == "ТАК":
        sz += 1
    if sh[33] == "ТАК":
        sz += 1
    if sh[34] == "ТАК":
        sz += 1
    if sh[44] == "ТАК":
        sz += 1
    if sh[46] == "ТАК":
        sz += 1
    if sh[52] == "ТАК":
        sz += 1
    if sh[75] == "ТАК":
        sz += 1
    if sh[89] == "ТАК":
        sz += 1
    if sh[120] == "ТАК":
        sz += 1
    if sh[124] == "ТАК":
        sz += 1
    if sh[129] == "ТАК":
        sz += 1
    if sh[141] == "ТАК":
        sz += 1
    if sh[142] == "ТАК":
        sz += 1
    if sh[154] == "ТАК":
        sz += 1
    if sh[159] == "ТАК":
        sz += 1
    if sh[160] == "ТАК":
        sz += 1

    if sh[37] == "НІ":
        sz += 1
    if sh[110] == "НІ":
        sz += 1

    oap = pr + kp + mn
    analitics()

    #####
    bd_result.append(dost)
    bd_result.append(oap)
    bd_result.append(pr)
    bd_result.append(kp)
    bd_result.append(mn)
    bd_result.append(vps)
    bd_result.append(dap)
    bd_result.append(sz)
    insert_bd_result()  #


def insert_mysql(sh):
    connection = pymysql.connect(host='localhost', user='root', password='1111', db='USER', charset='utf8mb4',
                                 cursorclass=DictCursor, autocommit=True)

    cmd = "INSERT INTO info (ssurname, sname , secname , bdate , descr , ooc , _1 , _2 , _3 , _4 , _5 , _6 , _7 , _8 , _9 , _10 , _11 , _12 , _13 , _14 , _15 , _16 , _17 , _18 , _19 , _20 , _21 , _22 , _23 , _24 , _25 , _26 , _27 , _28 , _29 , _30 , _31 , _32 , _33 , _34 , _35 , _36 , _37 , _38 , _39 , _40 , _41 , _42 , _43 , _44 , _45 , _46 , _47 , _48 , _49 , _50 , _51 , _52 , _53 , _54 , _55 , _56 , _57 , _58 , _59 , _60 , _61 , _62 , _63 , _64 , _65 , _66 , _67 , _68 , _69 , _70  , _71  , _72  , _73  , _74  , _75  , _76  , _77  , _78  , _79  , _80  , _81  , _82  , _83  , _84  , _85  , _86  , _87  , _88  , _89  , _90  , _91  , _92  , _93  , _94  , _95  , _96  , _97  , _98  , _99  , _100  , _101  , _102  , _103  , _104  , _105  , _106  , _107  , _108  , _109  , _110  , _111  , _112  , _113  , _114  , _115  , _116  , _117  , _118  , _119  , _120  , _121  , _122  , _123  , _124  , _125  , _126  , _127  , _128  , _129  , _130  , _131  , _132  , _133  , _134  , _135  , _136  , _137  , _138  , _139  , _140  , _141  , _142  , _143  , _144  , _145  , _146  , _147  , _148  , _149  , _150  , _151  , _152  , _153  , _154  , _155  , _156  , _157  , _158  , _159  , _160  , _161  , _162  , _163  , _164  , _165  , _166  , _167  , _168  , _169  , _170  , _171  , _172  , _173  , _174  , _175  , _176  , _177  , _178  , _179  , _180  , _181  , _182  , _183  , _184  , _185  , _186  , _187  , _188  , _189  , _190  , _191  , _192  , _193  , _194  , _195  , _196  , _197  , _198  , _199  , _200) values ('{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
        sh[0], sh[1], sh[2], sh[3], sh[4], sh[5], sh[6], sh[7], sh[8], sh[9], sh[10], sh[11], sh[12], sh[13], sh[14],
        sh[15], sh[16], sh[17], sh[18], sh[19], sh[20], sh[21], sh[22], sh[23], sh[24], sh[25], sh[26], sh[27], sh[28],
        sh[29], sh[30], sh[31], sh[32], sh[33], sh[34], sh[35], sh[36], sh[37], sh[38], sh[39], sh[40], sh[41], sh[42],
        sh[43], sh[44], sh[45], sh[46], sh[47], sh[48], sh[49], sh[50], sh[51], sh[52], sh[53], sh[54], sh[55], sh[56],
        sh[57], sh[58], sh[59], sh[60], sh[61], sh[62], sh[63], sh[64], sh[65], sh[66], sh[67], sh[68], sh[69], sh[70],
        sh[71], sh[72], sh[73], sh[74], sh[75], sh[76], sh[77], sh[78], sh[79], sh[80], sh[81], sh[82], sh[83], sh[84],
        sh[85], sh[86], sh[87], sh[88], sh[89], sh[90], sh[91], sh[92], sh[93], sh[94], sh[95], sh[96], sh[97], sh[98],
        sh[99], sh[100], sh[101], sh[102], sh[103], sh[104], sh[105], sh[106], sh[107], sh[108], sh[109], sh[110],
        sh[111], sh[112], sh[113], sh[114], sh[115], sh[116], sh[117], sh[118], sh[119], sh[120], sh[121], sh[122],
        sh[123], sh[124], sh[125], sh[126], sh[127], sh[128], sh[129], sh[130], sh[131], sh[132], sh[133], sh[134],
        sh[135], sh[136], sh[137], sh[138], sh[139], sh[140], sh[141], sh[142], sh[143], sh[144], sh[145], sh[146],
        sh[147], sh[148], sh[149], sh[150], sh[151], sh[152], sh[153], sh[154], sh[155], sh[156], sh[157], sh[158],
        sh[159], sh[160], sh[161], sh[162], sh[163], sh[164], sh[165], sh[166], sh[167], sh[168], sh[169], sh[170],
        sh[171], sh[172], sh[173], sh[174], sh[175], sh[176], sh[177], sh[178], sh[179], sh[180], sh[181], sh[182],
        sh[183], sh[184], sh[185], sh[186], sh[187], sh[188], sh[189], sh[190], sh[191], sh[192], sh[193], sh[194],
        sh[195], sh[196], sh[197], sh[198], sh[199], sh[200], sh[201], sh[202], sh[203], sh[204], sh[205])

    cursor = connection.cursor()
    cursor.execute(cmd)
    connection.close()
    exp(sh)


data_s = ["1. Буває, що я серджуся", "2. Зазвичай вранці я прокидаюся свіжим і відпочилим.",
          "3. Зараз я приблизно так само працездатний, як і завжди.", "4. Доля безумовно несправедлива до мене.",
          "5. Запори у мене бувають дуже рідко.", "6. Часом мені дуже хотілося покинути свій дім.",
          "7. Часом у мене бувають напади сміху або плачу, з якими я ніяк не можу справитися.",
          "8. Мені здається, що мене ніхто не розуміє.",
          "9. Вважаю, що якщо хтось заподіяв мені зло, я повинен йому відповісти тим же.",
          "10. Іноді мені в голову приходять такі нехороші думки, що краще про них нікому не розказувати.",
          "11. Мені важко зосередитися на якому-небудь завданні або роботі.",
          "12. У мене бувають дуже дивні і незвичайні переживання.",
          "13. У мене були відсутні неприємності через мою поведінку.",
          "14. В дитинстві я у свій час скоював дрібні крадіжки.",
          "15. Буває, у мене з’являється бажання ламати або крушити все навколо.",
          "16. Бувало, що я цілими днями або навіть тижнями нічого не міг робити, тому що ніяк не міг примусити себе взятися до роботи.",
          "17. Сон у мене переривистий і неспокійний.",
          "18. Моя сім'я відноситися з несхваленням до тієї роботи, яку я обрав.",
          "19. Бували випадки, що я не виконував своїх обіцянок.", "20. Голова у мене болить часто.",
          "21. Раз на тиждень або частіше я без жодної видимої причини раптово відчуваю жар у всьому тілі.",
          "22. Було б добре, якби майже всі закони відмінили.",
          "23. Стан мого здоров’я майже такий же, як у більшості моїх знайомих (не гірше).",
          "24. Зустрічаючи на вулиці своїх знайомих або шкільних друзів, з якими я давно не бачився, я вважаю за краще проходити мимо, якщо вони зі мною не заговорюють першими.",
          "25. Більшості людей, які мене знають, я подобаюся.", "26. Я людина товариська.",
          "27. Іноді я так наполягаю на своєму, що люди втрачають терпіння.",
          "28. Значну частину часу настрій у мене пригнічений.",
          "29. Тепер мені важко сподіватися на те, що я чого-небудь досягну у житті",
          "30. У мене мало впевненості в собі.", "31. Іноді я кажу неправду.",
          "32. Зазвичай я вважаю, що життя – гарна річ.",
          "33. Я вважаю, що більшість людей здатна збрехати, щоб просунутися по службі.",
          "34. Я охоче беру участь у зібраннях, зборах і інших суспільних заходах.",
          "35. Я сварюся з членами моєї сім’ї дуже рідко.",
          "36. Іноді у мене виникає сильне бажання порушити правила пристойності або кому-небудь нашкодити.",
          "37. Найважча боротьба для мене - це боротьба з самим собою.",
          "38. М’язові судоми або сіпання у мене бувають украй рідко (або майже не бувають).",
          "39. Я досить байдужий до того, що зі мною буде.",
          "40. Іноді, коли я себе недобре відчуваю я буваю дратівливим.",
          "41. Значну частину часу у мене таке відчуття, що я зробив щось не те або навіть щось погане.",
          "42. Деякі люди до того полюбляють командувати, що мені так і кортить робити все наперекір, навіть якщо я знаю, що вони мають рацію.",
          "43. Я часто вважаю себе зобов'язаним відстоювати те, що вважаю справедливим.",
          "44. Моя мова зараз така ж як завжди (ні швидше і ні повільніше, немає ні хрипоти, ні невиразності).",
          "45. Я вважаю, що моє сімейне життя таке ж добре, як у більшості моїх знайомих.",
          "46. Мене вкрай зачіпає, коли мене критикують або лають.",
          "47. Іноді у мене буває таке відчуття, що я просто повинен нанести ушкодження собі або кому-небудь іншому.",
          "48. Моя поведінка значною мірою визначається звичаями тих, хто мене оточує.",
          "49. В дитинстві у мене була така компанія, де всі прагнули стояти один за одного.",
          "50. Іноді мені так і кортить з ким-небудь затіяти бійку.",
          "51. Бувало, що я казав про речі, в яких не розбираюся.",
          "52. Зазвичай я засинаю спокійно і мене не турбують ніякі думки.",
          "53. Останні декілька років я відчуваю себе добре.", "54. У мене ніколи не було ні припадків, ні судом.",
          "55. Зараз моя вага постійна (я не худну і не повнішаю).", "56. Я вважаю, що мене часто карали нізащо.",
          "57. Я легко плачу.", "58. Я мало втомлююся.",
          "59. Я був би досить спокійний, якби у кого-небудь з моєї сім'ї були неприємності через порушення закону.",
          "60. З моїм розумом творитися щось недобре.",
          "61. Щоб приховати свою сором'язливість мені доводиться докладати великі зусилля.",
          "62. Напади запаморочення у мене бувають дуже рідко (або майже не бувають).",
          "63. Мене турбують сексуальні (статеві) питання.",
          "64. Мені важко підтримувати розмову з людьми, з якими я тільки що познайомився.",
          "65. Коли я намагаюся щось зробити, то часто помічаю, що у мене тремтять руки.",
          "66. Руки у мене такі ж спритні і моторні, як і раніше.",
          "67. Велику частину часу я відчуваю загальну слабкість.",
          "68. Іноді, коли я збентежений я сильно вкриваюся потом і мене це дратує.",
          "69. Буває, що я відкладаю на завтра те, що повинен зробити сьогодні.", "70. Думаю, що я людина приречена.",
          "71. Бували випадки, що мені було важке утриматися від того, щоб що-небудь не поцупити в кого-небудь або де-небудь, наприклад у магазині.",
          "72. Я зловживав спиртними напоями.", "73. Я часто про що-небудь турбуюся.",
          "74. Мені б хотілося бути членом декількох кружків або зборів.",
          "75. Я рідко задихаюся, і у мене не буває сильного серцебиття.",
          "76. Все своє життя я суворо дотримуюсь принципів, заснованих на почутті обов’язку.",
          "77. Траплялося, що я перешкоджав або поступав наперекір людям просто із принципу, а не тому, що справа була дійсно важливою.",
          "78. Якщо мені не загрожує штраф і машин поблизу немає, я можу перейти вулицю там, де бажаю, а не там де потрібно.",
          "79. Я завжди був незалежним і вільним від контролю з боку сім'ї.",
          "80. У мене бували періоди такої сильної стурбованості, що я навіть не міг всидіти на місці.",
          "81. Часто мої вчинки тлумачилися не вірно.",
          "82. Мої батьки і (або) інші члени моєї сім’ї прискіпуються до мене більше, ніж треба.",
          "83. Хтось керує моїми думками.", "84. Люди байдужі до того, що з тобою трапиться.",
          "85. Мені подобається бути в компанії, де всі жартують один над одним.",
          "86. В школі я засвоював матеріал повільніше, аніж інші.", "87. Я цілком впевнений у собі.",
          "88. Нікому не довіряти – найбезпечніше.",
          "89. Раз на тиждень або частіше я буваю дуже збудженим і схвильованим.",
          "90. Коли я знаходжуся в компанії, мені важко знайти відповідну тему для розмови.",
          "91. Мені легко примусити інших людей боятися мене, і іноді я це роблю ради забави.",
          "92. У грі я вважаю за краще вигравати.",
          "93. Безглуздо засуджувати людину, яка обдурила того, хто сам дозволяє себе обдурювати.",
          "94. Хтось намагається впливати на мої думки.", "95. Я щодня випиваю багато води.",
          "96. Щасливіше всього я буваю наодинці.",
          "97. Я обурююся кожного разу, коли дізнаюся, що злочинець з якої-небудь  причини залишився безкарним.",
          "98. У моєму житті був один або декілька випадків, коли я відчував, що хтось за допомогою гіпнозу примушує мене скоювати ті або інші вчинки.",
          "99. Я дуже рідко заговорюю з людьми першим.", "100. У мене ніколи не було зіткнень із законом.",
          "101. Мені приємно мати серед своїх знайомих значних людей, це як би додає мені вагу у власних очах.",
          "102. Іноді без жодної причини у мене раптом наступають періоди незвичайної веселості.",
          "103. Життя для мене майже завжди пов'язано з напругою.",
          "104. У школі мені було дуже важко виступати перед класом.",
          "105. Люди проявляють по відношенні до мене стільки співчуття і симпатії, наскільки я заслуговую.",
          "106. Я відмовляюся грати в деякі ігри, тому що це у мене погано виходить.",
          "107. Мені здається, що я знаходжу друзів з такою ж легкістю, як і інші.",
          "108. Мені неприємно, коли навколо мене є люди.", "109. Як правило, мені не везе.",
          "110. Мене легко збити з пантелику.", "111. Деякі з членів моєї сім'ї скоювали вчинки, які мене лякали.",
          "112. Іноді у мене бувають напади сміху або плачу, з якими я ніяк не можу справитися.",
          "113. Мені важко приступити до виконання нового завдання або розпочати нову справу.",
          "114. Якби люди не були налаштовані проти мене, я досягнув би у житті набагато більшого.",
          "115. Мені здається, що мене ніхто не розуміє.", "116. Серед моїх знайомих є люди, які мені не подобаються.",
          "117. Я легко втрачаю терпіння з людьми.", "118. Часто у новій обстановці я переживаю почуття тривоги.",
          "119. Часто мені хочеться померти.", "120. Іноді я такий збуджений, що мені важко заснути.",
          "121. Часто я переходжу на іншу сторону вулиці, щоб уникнути зустрічі з тим, кого я побачив.",
          "122. Бувало, що я кидав почату справу, оскільки боявся, що я не справлюся з нею.",
          "123. Майже щодня трапляється що-небудь, що лякає мене.",
          "124. Навіть серед людей я зазвичай відчуваю себе самотнім.",
          "125. Я переконаний, що існує лише одне єдине правильне розуміння значення життя.",
          "126. В гостях я частіше сиджу де-небудь осторонь або розмовляю з ким-небудь одним, ніж беру участь у загальних розвагах.",
          "127. Мені часто кажуть, що я запальний.", "128. Буває, що я з ким-небудь пліткую.",
          "129. Часто мені неприємно, коли я намагаюся застерегти кого-небудь від помилок, а мене розуміють неправильно.",
          "130. Я часто звертаюся до людей за порадою.",
          "131. Часто, навіть тоді, коли усе для мене складається добре, я відчуваю що мені усе байдуже.",
          "132. Мене досить важко вивести з себе.",
          "133. Коли я намагаюся вказати людям на їх помилки або допомогти вони часто розуміють мене неправильно.",
          "134. Зазвичай я спокійний, і мене нелегко вивести з душевної рівноваги.",
          "135. Я заслуговую суворого покарання за свою провину.",
          "136. Мені притаманно так сильно переживати свої розчарування, що я не можу примусити себе не думати про них.",
          "137. Часом мені здається, що я ні на що не здатний.",
          "138. Бувало, що під час обговорення деяких питань я, особливо не замислюючись, погоджувався з думкою інших.",
          "139. Мене дуже турбують різного роду нещастя.", "140. Мої переконання і погляди непохитні.",
          "141. Я вважаю, що можна не порушуючи закон спробувати знайти в ньому лазівку.",
          "142. Є люди, які мені настільки неприємні, що я в глибині душі радію, коли вони одержують прочухан за що-небудь.",
          "143. У мене бували періоди, коли через хвилювання я втрачав сон.",
          "144. Я відвідую різні суспільні заходи, тому що це дозволяє бувати мені серед людей.",
          "145. Можна пробачити людям порушення тих правил, які вони вважають нерозсудливими.",
          "146. У мене є погані звички, які є настільки сильними, що боротися з ними просто марно.",
          "147. Я охоче знайомлюся з новими людьми.", "148. Буває, що непристойний жарт у мене викликає сміх.",
          "149. Якщо справа йде у мене погано, то мені відразу хочеться все кинути.",
          "150. Я вважаю за краще діяти відповідно до  власних планів, а не слідувати вказівкам інших.",
          "151. Мені подобається, коли оточуючі знають мою точку зору.",
          "152. Якщо я поганої думки про людину або навіть зневажаю його, я мало прагну приховати це від нього.",
          "153. Я людина нервова і легко збудлива.", "154. Все у мене виходить погано, не так як треба.",
          "155. Майбутнє здається мені безнадійним.",
          "156. Люди досить легко можуть змінити мою думку, навіть якщо до цього вона здавалася мені остаточною.",
          "157. Кілька разів на тиждень у мене буває таке відчуття, що повинно трапитися щось жахливе.",
          "158. Значну частину часу я відчуваю себе втомленим.", "159. Я люблю бувати на вечорах і просто в компаніях.",
          "160. Я прагну відхилитися від конфліктів і скрутних положень.",
          "161. Мене дуже дратує те, що я забуваю, куди кладу речі.",
          "162. Пригодницькі розповіді мені подобаються більше, ніж розповіді про любов.",
          "163. Якщо я схочу зробити щось, але оточуючі вважають, що цього робити не варто, я можу легко відмовитися від своїх намірів.",
          "164. Безглуздо засуджувати людей, які прагнуть урвати від життя все, що можуть.",
          "165. Мені байдуже, що про мене думають інші.",
          "166. Я абсолютно не пристосований до військової служби і це мене дуже лякає.",
          "167. Я переконаний, що чоловіки повинні служити у Збройних Силах тільки за власним бажанням.",
          "168. Останнім часом у мене все частіше і частіше трапляються „промахи” і невдачі по службі.",
          "169. Найбільші труднощі для мене під час служби – це необхідність підкорятися командирам і начальникам.",
          "170. Тим правилами, які, на мій погляд, несправедливі, я завжди прагну протидіяти.",
          "171. Мені хотілося б випробувати себе серйозною і небезпечною справою.",
          "172. Мене довго не залишає відчуття образи, заподіяне товаришами.",
          "173. Жити за військовим розпорядком для мене просто нестерпно.",
          "174. Я сумніваюся, чи зможу я зі своїм здоров'ям витримати всі навантаження військової служби.",
          "175. Я заздрю тим, хто зміг ухилитися від військової служби.",
          "176. Я відчуваю все більше і більше розчарувань по відношенню до моєї військової спеціальності.",
          "177. Я часто розгублююся у складних і небезпечних ситуаціях.",
          "178. Мені хотілося б служити у ПДВ або частинах спецназу.",
          "179. Із службою у мене ніщо не виходить (не „клеїться”). Часто думаю: „не моя це справа”",
          "180. Коли мною хтось командує, це викликає у мене відчуття протесту.",
          "181. Мені завжди було важко пристосовуватися до нового колективу.",
          "182. Під час подальшої служби я був би не проти послужити там, де небезпечно і де ведуться бойові дії.",
          "183. Присяга на вірність Вітчизні у сучасних умовах втратила свою актуальність.",
          "184. Мені завжди було нелегко пристосовуватися до нових умов життя.",
          "185. У складних ситуаціях я не можу швидко приймати правильні рішення.",
          "186. Я упевнений, що в майбутньому не стану укладати або продовжувати контракт на продовження військової служби.",
          "187. У мене бувають періоди похмурої дратівливості, під час яких я „зриваю зло” на оточуючих.",
          "188. Я насилу витримую фізичні навантаження, пов’язані з моєю професійною діяльністю.",
          "189. Я достатньо спокійно відношуся до необхідності брати участь в тривалих і небезпечних відрядженнях.",
          "190. Навряд чи я схочу присвятити все своє життя військовій професії (залишитися на службу за контрактом, поступити у військове училище).",
          "191. „За компанію” з товаришами я можу прийняти неабияку кількість алкоголю (перевищити свою звичайну „норму”).",
          "192. У компаніях, де я часто буваю, друзі іноді палять „травичку”. Я їх за це не засуджую.",
          "193. Останнім часом, щоб не „зірватися”, я був вимушений приймати заспокійливі ліки.",
          "194. Мої батьки (родичі) часто виказували побоювання у зв'язку з моїми випивками.",
          "195. Немає нічого поганого, коли люди намагаються випробувати на собі незвичайні стани, приймаючи деякі речовини.",
          "196. У стані агресії я здатний багато на що.", "197. Я крутий і жорстокий з оточуючими.",
          "198. Якщо хтось заподіяв мені зло, я вважаю зобов'язаним відплатити йому тим же („око за око, зуб за зуб”).",
          "199. Можна погодитися з тим, що я не дуже-то схильний виконувати багато наказів, вважаючи їх безрозсудними.",
          "200. Я думаю, що будь-яке положення законів і військових статутів можна тлумачити двояко."]

sten_dost = ["ВИСОКА достовірність результатів обстеження.",
             "ДОСТАТНЯ достовірність результатів обстеження. Окремі ознаки соціальної бажаності.",
             "Результати обстеження НЕДОСТОВІРНІ. Формулювання висновку не уявляється можливим. Потрібне додаткове поглиблене обстеження. "]

sten_oap = [
    "1-Й РІВЕНЬ СТІЙКОСТІ ДО БОЙОВОГО СТРЕСУ. Високий рівень розвитку адаптаційних можливостей особистості. Повністю відповідає вимогам, що пред'являються до військовослужбовців в умовах бойової діяльності.",
    "2-Й РІВЕНЬ СТІЙКОСТІ ДО БОЙОВОГО СТРЕСУ. Достатній рівень розвитку адаптаційних можливостей особистості. В основному відповідає вимогам, що пред'являються до військовослужбовців в умовах бойової діяльності.",
    "3-Й РІВЕНЬ СТІЙКОСТІ ДО БОЙОВОГО СТРЕСУ. Задовільний рівень розвитку адаптаційних можливостей особистості. Мінімально відповідає вимогам, що пред'являються до військовослужбовців в умовах бойової діяльності.",
    "4-Й РІВЕНЬ СТІЙКОСТІ ДО БОЙОВОГО СТРЕСУ. Недостатній рівень розвитку адаптаційних можливостей особистості. Не відповідає вимогам, що пред'являються до військовослужбовців в умовах бойової діяльності. "]

sten_pr = [
    "Високий рівень нервово-психічної стійкості і поведінкової регуляції. Високий рівень працездатності, у тому числі і в умовах вираженого стресу. Висока толерантність до несприятливих психічних і фізичних навантажень.",
    "Достатньо високий рівень нервово-психічної стійкості і поведінкової регуляції. Достатньо високий рівень працездатності, у тому числі і в ускладнених умовах діяльності. Достатньо висока толерантність до психічних і фізичних навантажень. Достатньо висока стійкість до дії стрес-чинників.",
    "Достатній рівень нервово-психічної стійкості і поведінкової регуляції. Достатній рівень працездатності, у тому числі і в ускладнених умовах діяльності. Достатня толерантність до психічних і фізичних навантажень. Достатня стійкість до дії стрес-чинників.",
    "В цілому достатній рівень нервово-психічної стійкості і поведінкової регуляції. Стійкий рівень працездатності у звичних умовах життєдіяльності. При тривалій дії явних психічних навантажень можливо тимчасове погіршення якості діяльності.",
    "Дещо понижений рівень нервово-психічної стійкості і поведінкової регуляції. Нестабільний рівень працездатності, що особливо проявляється в ускладнених умовах діяльності. Адаптація до нових і незвичайних умов життєдіяльності ускладнена і може супроводжуватися тимчасовим погіршенням функціонального стану організму.",
    "Окремі ознаки нервово-психічної нестійкості і порушення поведінкової регуляції. Недостатня толерантність до психічних і фізичних навантажень. Адаптація до нових умов життєдіяльності, як правило, ускладнена і може супроводжуватися тривалим погіршенням функціонального стану організму і професійної працездатності. При надзвичайно високих психічних навантаженнях можливий зрив професійної діяльності.",
    "Виражені ознаки нервово-психічної нестійкості і порушення поведінкової регуляції. Низька толерантність до психічних і фізичних навантажень. Адаптація до нових умов життєдіяльності протікає хворобливо. Можливе тривале і виражене погіршення функціонального стану організму. Рівень професійної працездатності у даний період часу низький. При посиленні психічних навантажень достатньо вірогідний зрив професійної діяльності.",
    "Вкрай високий рівень нервово-психічної нестійкості. Ознаки граничних нервово-психічних розладів. Вкрай низька толерантність до психічних і фізичних навантажень. Адаптація до нових умов життєдіяльності протікає дуже хворобливо з тривалим і вираженим погіршенням функціонального стану організму. Працездатність у даний період часу різко знижена. Посилення психічних навантажень приводить до зриву професійної діяльності"]

sten_kp = [
    "Високий рівень комунікативних здібностей. Швидко адаптується у новому колективі. Легко встановлює контакти з оточуючими.У міжособистісному спілкуванні неконфліктний. Завжди адекватно оцінює свою роль і правильно будує міжперсональні взаємостосунки у колективі.",
    "Достатньо високий рівень комунікативних здібностей. Достатньо швидко адаптується у новому колективі. При встановленні міжособистісних контактів з оточуючими, як правило, не зазнає труднощів. У спілкуванні не конфліктний. У більшості випадків адекватно оцінює свою роль в колективі. На критику реагує адекватно. Достатня здатність до корекції поведінки.",
    "Достатній рівень комунікативних здібностей. Достатньо швидко адаптується у новому колективі. При встановленні міжособистісних контактів з оточуючими, як правило, не зазнає труднощів. У спілкуванні не конфліктний. У більшості випадків адекватно оцінює свою роль в колективі. На критику реагує адекватно. Достатня здатність до корекції поведінки.",
    "Рівень комунікативних здібностей середній. У цілому без особливих ускладнень адаптується до нового колективу. При встановленні міжособистісних контактів з оточуючими іноді може неправильно будувати стратегію своєї поведінки. Разом з тим, до критичних зауважень відноситься адекватно, здатний коригувати свою поведінку. У спілкуванні не конфліктний. Достатньо адекватно оцінює свою роль у колективі.",
    "Задовільний рівень комунікативних здібностей. На початковому етапі адаптації до нового колективу можуть виникати ускладнення. Не завжди правильно будує міжперсональні взаємостосунки, зважаючи на деяку неадекватність самооцінки. На критичні зауваження на свою адресу в основному реагує адекватно, хоча і дещо хворобливо. В цілому здатний до корекції своєї поведінки.",
    "Понижений рівень комунікативних здібностей. Наявність окремих ознак акцентуації характеру. На початковому етапі адаптації до нового колективу виникають значні ускладнення. Міжперсональні взаємостосунки (як по горизонталі, так і по вертикалі) часто будує неправильно. Хворобливо реагує на критику. Недостатньо розвинута здатність до корекції своєї поведінки.",
    "Рівень комунікативних здібностей низький. Наявність ознак акцентуації характеру. Початковий етап адаптації до нового колективу розтягнутий у часі і, як правило, протікає вельми хворобливо. Часто виникають ускладнення в побудові міжособистісних контактів з оточуючими, зважаючи на наявність неадекватної самооцінки. Схильність до підвищеної конфліктності. Хворобливо реагує на критику. Фіксований на образах, що заподіяні йому оточуючими. Недостатньо розвинута здатність до корекції поведінки.",
    "Вкрай низький рівень комунікативних здібностей. Наявність виражених ознак акцентуації характеру. Адаптація до нового колективу протікає тривало і украй хворобливо. Постійно випробовує утруднення в побудові міжособистісних контактів з оточуючими. Високий рівень конфліктності. Колективом, як правило, відкидаємо. Фіксований на образах, заподіяних оточуючими, унаслідок чого схилений до ірраціональних вчинків. Вкрай низька здатність до корекції поведінки."]

sten_mn = [
    "Дуже високий рівень соціалізації. Суворо орієнтований на загальноприйняті і соціально схвалювані норми поведінки. Суворо дотримується корпоративних вимог. У повсякденній діяльності групові інтереси ставить вище особистісних. Виражені альтруїстські якості.",
    "Високий рівень соціалізації. Суворо орієнтований на загальноприйняті і соціально ухвалені норми поведінки. Схильний дотримуватися корпоративних вимог. У повсякденній діяльності групові інтереси ставить вище особистісних.",
    "Достатньо високий рівень соціалізації. Орієнтований на дотримання загальноприйнятих і соціально ухвалених норм поведінки. Дотримується корпоративних вимог. У повсякденній життєдіяльності групові інтереси, як правило, переважають над особистісними інтересами.",
    "Достатній рівень соціалізації. У цілому орієнтований на дотримання загальноприйнятих і соціально ухвалених норм поведінки. У цілому дотримується корпоративних вимог. В повсякденній життєдіяльності групові інтереси, як правило, переважають над особистісними інтересами.",
    "В цілому достатній рівень соціалізації. Прагне дотримуватися загальноприйнятих і соціально ухвалених норм поведінки. У повсякденній життєдіяльності групові інтереси, як правило, переважають над особистісними інтересами.",
    "Задовільний рівень соціалізації. Не завжди орієнтований на дотримання загальноприйнятих і соціально ухвалених норми поведінки. У повсякденній життєдіяльності особистісні інтереси, як правило, переважають над груповими.",
    "Недостатній рівень соціалізації. В цілому не прагне дотримуватися загальноприйнятих норм поведінки і соціально ухвалених вимог. В повсякденній життєдіяльності особистісні інтереси переважають над груповими.",
    "Низький рівень соціалізації. Не прагне дотримуватися загальноприйнятих норм поведінки. В основному вважає за краще діяти згідно власних планів, не орієнтуючись на думку оточуючих. В повсякденній життєдіяльності переважають егоцентричні тенденції. Особистісні інтереси переважають над інтересами групи. Досягнення особистісних інтересів може здійснювати в обхід існуючих заборон і правил.",
    "Вкрай низький рівень соціалізації (значно відмінний від номінальних значень для даної вікової групи). Вважає за краще діяти згідно власних планів, не рахуючись з думкою оточуючих. Особистісні інтереси домінують над груповими. Для досягнення особистісних інтересів ігноруються загальноприйняті норми і правила поведінки."]

sten_vps = [
    "Високий рівень військово-професійної спрямованості. Виражене бажання продовжувати професійну діяльність, у тому числі і в особливих умовах.",
    "Достатній рівень військово-професійної спрямованості. Стійка орієнтація на продовження професійної діяльності, у тому числі і в особливих умовах.",
    "В цілому достатній рівень військово-професійної спрямованості. Орієнтований на продовження професійної діяльності, у тому числі і в особливих умовах.",
    "Недостатній рівень військово-професійної спрямованості. Не повною мірою задоволений своєю військовою професійною діяльністю і службовим призначенням. Орієнтація на продовження професійної діяльності сумнівна.",
    "Низький рівень військово-професійної спрямованості. Не задоволений своєю військовою професійною діяльністю і службовим призначенням."]

sten_dap = [
    "Відсутність  ознак девіантних (аддиктивної і делинквентної) форм поведінки. Відсутність ознак агресивної поведінки відносно оточуючих. Орієнтація на дотримання соціально ухвалених норм поведінки і раціональну побудову міжперсональних взаємостосунків з ровесниками і із старшими за віком.",
    "В цілому виражені ознаки девіантних (аддиктивної і делинквентної) форм поведінки відсутні. Відмічається наявність окремих ознак нераціональної побудови міжперсональних взаємостосунків з ровесниками і із старшими за віком. Іноді допускає порушення соціально ухвалених норм поведінки.",
    "Відзначено наявність деяких ознак девіантних (аддиктивної і делинквентної) форм поведінки. Наявність агресивних реакцій відносно оточуючих. Схильність до нераціональної побудови міжперсональних взаємостосунків з ровесниками і із старшими за віком. Схильний допускати порушення соціально ухвалених норм поведінки.",
    "Наявність виразних ознак девіантних (аддиктивної і делинквентної) форм поведінки. Наявність виражених агресивних реакцій відносно оточуючих. Як правило, міжперсональні взаємостосунки з ровесниками і із старшими за віком будує нераціонально. Не орієнтований на дотримання соціально ухвалених норм поведінки."]

sten_sz = ["Відсутність  ознак суїцидального ризику.",
           "В цілому виразних ознак суїцидальної схильності не виявлено. Наголошується наявність окремих ознак, що свідчать про певні труднощі в міжперсональних взаємостосунках з ровесниками і (або) із старшими по віку.",
           "Відзначена наявність окремих ознак суїцидальної схильності. За наявності затяжної військово-професійної адаптації або труднощів у міжперсональних взаємостосунках з ровесниками і із старшими за віком можуть виникнути думки суїцидальної спрямованості.",
           "Відзначена наявність виразних ознак суїцидальної схильності. За наявності затяжної військово-професійної адаптації або труднощів в міжперсональних взаємостосунках з ровесниками і із старшими по віку можуть виникнути думки про суїцидальний шантаж або закінчені суїцидальні дії."]


def check_root(username, upassword):  ## check mysql root user
    con = pymysql.connect(host='localhost', user='root', password='1111', db='user', charset='utf8mb4',
                          cursorclass=DictCursor)
    cur = con.cursor()
    cur.execute("SELECT upassword FROM user_root WHERE username='" + username + "'")
    result = cur.fetchall()
    # return result
    if upassword in str(result):
        # print("password correct")
        return True;
    else:
        # print("password incorrect")
        return False;


def check_admin(username, upassword):
    con = pymysql.connect(host='localhost', user='root', password='1111', db='user', charset='utf8mb4',
                          cursorclass=DictCursor)
    cur = con.cursor()
    cur.execute("SELECT upassword FROM user_admin WHERE username='" + username + "'")
    result = cur.fetchall()
    # return result
    if upassword in str(result):
        # print("password correct")
        return True;
    else:
        # print("password incorrect")
        return False;


@app.route('/', methods=['GET', 'POST'])
def main():
    session['log'] = False
    if request.method == 'POST':
        if request.form['form_id'] == 'one':
            return redirect('/auth')
        elif request.form['form_id'] == 'two':
            return redirect('/test')
    return render_template('index.html')


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        if request.form['form_id'] == 'info':
            session['log'] = True
            global sh
            global bd_result
            sh = []
            bd_result = []
            sh.append(request.form['surname'])
            sh.append(request.form['name'])
            sh.append(request.form['secondname'])
            sh.append(request.form['birthday'])
            sh.append(request.form['desc'])
            sh.append(request.form['select-css'])
            #####
            bd_result.append(request.form['surname'])
            bd_result.append(request.form['name'])
            bd_result.append(request.form['secondname'])
            bd_result.append(request.form['birthday'])
            bd_result.append(request.form['desc'])
            bd_result.append(request.form['select-css'])
            return redirect('/consent')
    return render_template('test.html')


@app.route('/consent', methods=['GET', 'POST'])
def consent():
    if 'log' in session:
        if request.method == 'POST':
            global timestart
            todaytime = datetime.datetime.today()
            timestart = str(todaytime.strftime("%H:%M:%S"))
            session['count'] = 0
            return redirect('/ask')
        return render_template('consent.html')
    else:
        return redirect('/')


@app.route('/ask', methods=['GET', 'POST'])
def ask1():
    if 'log' in session:
        if request.method == 'POST':
            if request.form['form_id'] == 'ТАК':
                # print(request.form['form_id'])
                # print(session.get('count'))
                # sh.append(str(session.get('count') + 1) + ". " + request.form['form_id'])
                sh.append(str(request.form['form_id']))  # print(sh)
            elif request.form['form_id'] == 'НІ':
                # print(request.form['form_id'])
                # print(session.get('count'))
                # sh.append(str(session.get('count') + 1) + ". " + request.form['form_id'])
                sh.append(str(request.form['form_id']))  # print(sh)

            if 'count' in session:
                if session.get('count') < 199:
                    session['count'] = session.get('count') + 1
                else:
                    global timefinish
                    todaytime = datetime.datetime.today()
                    timefinish = str(todaytime.strftime("%H:%M:%S"))
                    session['count'] = 0
                    session['log'] = False
                    insert_mysql(sh)

                    #### suda nada finish

                    return redirect('/')
            else:
                session['count'] = 0
        return render_template('ask/ask1.html', data_s=data_s[session.get('count')])
    else:
        return redirect('/')


@app.route('/bdanswer', methods=['GET', 'POST'])
def bdanswer():
    if 'admin' in session:
        if request.method == 'POST':
            if request.form["form_id"] == 'goback':
                return redirect("/action")
        items = getdb()
        return render_template('bd_answer.html', items=items)
    else:
        return redirect("/auth")


@app.route('/bdresult', methods=['GET', 'POST'])
def bdresult():
    if 'admin' in session:
        if request.method == 'POST':
            if request.form["form_id"] == 'goinfo':
                global id_u
                id_u = request.form["id"]
                return redirect("/admin_result")
            elif request.form["form_id"] == 'goback':
                return redirect("/action")
        items = getdb_2()
        return render_template('bd_result.html', items=items)
    else:
        return redirect("/auth")


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        hashpass = hashlib.sha256(request.form['pass'].encode())
        # print(hashpass.hexdigest())
        checklog = check_root(request.form['username'], hashpass.hexdigest())
        if checklog == True:
            session['admin'] = True
            return redirect("/action")
        else:
            session.pop('admin', None)
    return render_template('auth.html')


@app.route('/action', methods=['GET', 'POST'])
def action():
    if 'admin' in session:
        if request.method == "POST":
            if request.form["form_id"] == "two":
                return redirect("/bdresult")
            elif request.form["form_id"] == "one":
                return redirect("/admin")
            if request.form["form_id"] == "three":
                return redirect("/bdanswer")
            if request.form["form_id"] == "foo":
                session.pop('admin', None)
                # session['admin'] = False
                return redirect("/")
        return render_template("action.html")
    else:
        return redirect("/auth")


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'admin' in session:
        if request.method == "POST":
            if request.form["form_id"] == "one":
                hashpass = hashlib.sha256(request.form['pass'].encode())
                insert_user_root(request.form['login'], hashpass.hexdigest())
            elif request.form["form_id"] == "two":
                delete_user_root(request.form['id'])
            elif request.form["form_id"] == 'goback':
                return redirect("/action")

        items = get_login()
        return render_template("admin.html", items=items)
    else:
        return redirect("/auth")


@app.route('/admin_result', methods=['GET', 'POST'])
def admin_result():
    if 'admin' in session:
        try:
            get_info(id_u)
            return render_template("admin_result.html", items=result_info)
        except:
            return redirect("/bdresult")
    else:
        return redirect("/auth")



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", use_reloader=True)
