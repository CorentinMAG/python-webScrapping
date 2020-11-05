#coding:utf-8
import connexion
import datetime
import antiCaptcha

"""script cron qui doit s'exécuter toutes les dimaches soir"""

req1="SELECT id_relation,id_structure,id_site,id_auth FROM relation;"
connexion.cursor.execute(req1)
all_id=connexion.cursor.fetchall()
if all_id !=[]:
    for ids in all_id:
        r="SELECT directory FROM structure WHERE id_structure="+str(ids[1])+";"
        connexion.cursor.execute(r)
        dossier=connexion.cursor.fetchone()
        if int(ids[2]==4):
            req2="SELECT login,company,password FROM authentification WHERE id_site="+str(ids[2])+" AND id_structure="+str(ids[1])+";"
            connexion.cursor.execute(req2)
            identifiants=connexion.cursor.fetchall()
            antiCaptcha.account=identifiants[0][0]
            antiCaptcha.pinCode=identifiants[0][1]
            antiCaptcha.passphrase=identifiants[0][2]
            antiCaptcha.dossier=dossier
            dataUberJSON=antiCaptcha.main()
            try:
                req3="UPDATE relation SET datajson='"+dataUberJSON+"' WHERE id_structure="+str(ids[1])+" AND id_site="+str(ids[2])+";"
                connexion.cursor.execute(req3)
                connexion.mydb.commit()
            except:
                req="SELECT name FROM structure WHERE id_structure="+str(ids[1])+";"
                connexion.cursor.execute(req)
                structure_name=connexion.cursor.fetchone()
                print("["+datetime.datetime.today().isoformat(sep=" ",timespec="seconds")+"] les identifiants sont peut-être incorrects : site - UBER  structure - "+structure_name[0])
                continue