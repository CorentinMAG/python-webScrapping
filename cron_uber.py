#coding:utf-8
import connexion
import datetime
import antiCaptcha

"""script cron qui doit s'exécuter toutes les dimanches soir"""

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
        if int(id_site==4):
            req2="SELECT login,company,password FROM authentification WHERE id_site={} AND id_structure={};".format(id_ste,id_structure)
            connexion.cursor.execute(req2)
            identifiants=connexion.cursor.fetchall()
            antiCaptcha.account=identifiants[0][0]
            antiCaptcha.pinCode=identifiants[0][1]
            antiCaptcha.passphrase=identifiants[0][2]
            antiCaptcha.dossier=dossier
            dataUberJSON=antiCaptcha.main()
            try:
                req3="UPDATE relation SET datajson='{}' WHERE id_structure={} AND id_site={};".format(dataUberJSON,id_structure,id_site)
                connexion.cursor.execute(req3)
                connexion.mydb.commit()
            except:
                req="SELECT name FROM structure WHERE id_structure={};".format(id_structure)
                connexion.cursor.execute(req)
                structure_name=connexion.cursor.fetchone()
                print("["+datetime.datetime.today().isoformat(sep=" ",timespec="seconds")+"] les identifiants sont peut-être incorrects : site - UBER  structure - "+structure_name[0])
                continue