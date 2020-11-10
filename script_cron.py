#coding:utf-8
import connexion
import donnees_deliveroo
import donnees_just_eat
import donnees_oracle
import datetime
import antiCaptcha

"""script cron qui doit s'exécuter toutes les x minutes"""

req1="SELECT id_relation,id_structure,id_site,id_auth FROM relation;"
connexion.cursor.execute(req1)
all_id=connexion.cursor.fetchall()
if all_id !=[]:
    for ids in all_id:
        id_relation = ids[0]
        id_structure = ids[1]
        id_site = ids[2]
        id_auth = ids[3]
        r="SELECT directory FROM structure WHERE id_structure="+str(ids[1])+";"
        connexion.cursor.execute(r)
        dossier=connexion.cursor.fetchone()
        if int(id_site)==2:
            req2="SELECT login,password FROM authentification WHERE id_site={} AND id_structure={};".format(id_site,id_structure)
            connexion.cursor.execute(req2)
            identifiants=connexion.cursor.fetchall()
            donnees_deliveroo.account=identifiants[0][0]
            donnees_deliveroo.passphrase=identifiants[0][1]
            donnees_deliveroo.dossier=dossier
            dataDeliverooJSON=donnees_deliveroo.main()
            try:
                req3="UPDATE relation SET datajson='{}' WHERE id_structure={} AND id_site={};".format(dataDeliverooJSON,id_structure,id_site)
                connexion.cursor.execute(req3)
                connexion.mydb.commit()
            except:
                req="SELECT name FROM structure WHERE id_structure={};".format(id_structure)
                connexion.cursor.execute(req)
                structure_name=connexion.cursor.fetchone()
                print("["+datetime.datetime.today().isoformat(sep=" ",timespec="seconds")+"] les identifiants sont peut-être incorrects : site - Deliveroo  structure - "+structure_name[0])
                continue

        if int(id_site)==3:
            req2="SELECT login,company,password FROM authentification WHERE id_site={} AND id_structure={};".format(id_site,id_structure)
            connexion.cursor.execute(req2)
            identifiants=connexion.cursor.fetchall()
            donnees_oracle.account=identifiants[0][0]
            donnees_oracle.companyphrase=identifiants[0][1]
            donnees_oracle.passphrase=identifiants[0][2]
            donnees_oracle.dossier=dossier
            dataOracleJSON=donnees_oracle.main()
            try:
                req3="UPDATE relation SET datajson='{}' WHERE id_structure={} AND id_site={};".format(dataOracleJSON,id_structure,id_site)
                connexion.cursor.execute(req3)
                connexion.mydb.commit()
            except:
                req="SELECT name FROM structure WHERE id_structure={};".format(id_structure)
                connexion.cursor.execute(req)
                structure_name=connexion.cursor.fetchone()
                print("["+datetime.datetime.today().isoformat(sep=" ",timespec="seconds")+"] les identifiants sont peut-être incorrects : site - Oracle  structure - "+structure_name[0])
                continue
    print('['+datetime.datetime.today().isoformat(sep=" ",timespec="seconds")+'] database updated')
