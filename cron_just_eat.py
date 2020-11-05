#coding:utf-8
import connexion
import donnees_just_eat
import datetime

"""toutes les 2 semaines"""


req1="SELECT id_relation,id_structure,id_site,id_auth FROM relation;"
connexion.cursor.execute(req1)
all_id=connexion.cursor.fetchall()
if all_id !=[]:
    for ids in all_id:
        r="SELECT directory FROM structure WHERE id_structure="+str(ids[1])+";"
        connexion.cursor.execute(r)
        dossier=connexion.cursor.fetchone()
        if int(ids[2])==1:
            req2="SELECT login,password FROM authentification WHERE id_site="+str(ids[2])+" AND id_structure="+str(ids[1])+";"
            connexion.cursor.execute(req2)
            identifiants=connexion.cursor.fetchall()
            donnees_just_eat.account=identifiants[0][0]
            donnees_just_eat.passphrase=identifiants[0][1]
            donnees_just_eat.dossier=dossier
            dataJustEatJSON=donnees_just_eat.main()
            try:
                req3="UPDATE relation SET datajson='"+dataJustEatJSON+"' WHERE id_structure="+str(ids[1])+" AND id_site="+str(ids[2])+";"
                connexion.cursor.execute(req3)
                connexion.mydb.commit()
            except:
                req="SELECT name FROM structure WHERE id_structure="+str(ids[1])+";"
                connexion.cursor.execute(req)
                structure_name=connexion.cursor.fetchone()
                print("["+datetime.datetime.today().isoformat(sep=" ",timespec="seconds")+"] les identifiants sont peut-être incorrects : site - JustEat  structure - "+structure_name[0])
                continue