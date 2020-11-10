#coding:utf-8
import connexion
import donnees_just_eat
import datetime
import json

"""toutes les 2 semaines"""


req1="SELECT id_relation,id_structure,id_site,id_auth FROM relation;"
connexion.cursor.execute(req1)
all_id=connexion.cursor.fetchall()
if all_id !=[]:
    for ids in all_id:
        id_relation = ids[0]
        id_structure = ids[1]
        id_site = ids[2]
        id_auth = ids[3]
        r="SELECT directory FROM structure WHERE id_structure={};".format(id_structure)
        connexion.cursor.execute(r)
        dossier=connexion.cursor.fetchone()
        if int(id_site)==1:
            req2="SELECT login,password FROM authentification WHERE id_site={} AND id_structure={};".format(id_site,id_structure)
            connexion.cursor.execute(req2)
            identifiants=connexion.cursor.fetchall()
            donnees_just_eat.account=identifiants[0][0]
            donnees_just_eat.passphrase=identifiants[0][1]
            donnees_just_eat.dossier=dossier
            dataJustEatJSON=donnees_just_eat.main()
            try:
                req3="UPDATE relation SET datajson='{}' WHERE id_structure={} AND id_site={};".format(dataJustEatJSON,id_structure,id_site)
                connexion.cursor.execute(req3)
                connexion.mydb.commit()
            except:
                req="SELECT name FROM structure WHERE id_structure={};".format(id_structure)
                connexion.cursor.execute(req)
                structure_name=connexion.cursor.fetchone()
                print("["+datetime.datetime.today().isoformat(sep=" ",timespec="seconds")+"] les identifiants sont peut-être incorrects : site - JustEat  structure - "+structure_name[0])
                continue