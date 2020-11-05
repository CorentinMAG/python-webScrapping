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
        r="SELECT directory FROM structure WHERE id_structure="+str(ids[1])+";"
        connexion.cursor.execute(r)
        dossier=connexion.cursor.fetchone()
        if int(ids[2])==2:
            req2="SELECT login,password FROM authentification WHERE id_site="+str(ids[2])+" AND id_structure="+str(ids[1])+";"
            connexion.cursor.execute(req2)
            identifiants=connexion.cursor.fetchall()
            donnees_deliveroo.account=identifiants[0][0]
            donnees_deliveroo.passphrase=identifiants[0][1]
            donnees_deliveroo.dossier=dossier
            dataDeliverooJSON=donnees_deliveroo.main()
            try:
                req3="UPDATE relation SET datajson='"+dataDeliverooJSON+"' WHERE id_structure="+str(ids[1])+" AND id_site="+str(ids[2])+";"
                connexion.cursor.execute(req3)
                connexion.mydb.commit()
            except:
                req="SELECT name FROM structure WHERE id_structure="+str(ids[1])+";"
                connexion.cursor.execute(req)
                structure_name=connexion.cursor.fetchone()
                print("["+datetime.datetime.today().isoformat(sep=" ",timespec="seconds")+"] les identifiants sont peut-être incorrects : site - Deliveroo  structure - "+structure_name[0])
                continue

        # if int(ids[2])==1:
        #     req2="SELECT login,password FROM authentification WHERE id_site="+str(ids[2])+" AND id_structure="+str(ids[1])+";"
        #     connexion.cursor.execute(req2)
        #     identifiants=connexion.cursor.fetchall()
        #     donnees_just_eat.account=identifiants[0][0]
        #     donnees_just_eat.passphrase=identifiants[0][1]
        #     donnees_just_eat.dossier=dossier
        #     dataJustEatJSON=donnees_just_eat.main()
        #     try:
        #         req3="UPDATE relation SET datajson='"+dataJustEatJSON+"' WHERE id_structure="+str(ids[1])+" AND id_site="+str(ids[2])+";"
        #         connexion.cursor.execute(req3)
        #         connexion.mydb.commit()
        #     except:
        #         req="SELECT name FROM structure WHERE id_structure="+str(ids[1])+";"
        #         connexion.cursor.execute(req)
        #         structure_name=connexion.cursor.fetchone()
        #         print("["+datetime.datetime.today().isoformat(sep=" ",timespec="seconds")+"] les identifiants sont peut-être incorrects : site - JustEat  structure - "+structure_name[0])
        #         continue

        if int(ids[2])==3:
            req2="SELECT login,company,password FROM authentification WHERE id_site="+str(ids[2])+" AND id_structure="+str(ids[1])+";"
            connexion.cursor.execute(req2)
            identifiants=connexion.cursor.fetchall()
            donnees_oracle.account=identifiants[0][0]
            donnees_oracle.companyphrase=identifiants[0][1]
            donnees_oracle.passphrase=identifiants[0][2]
            donnees_oracle.dossier=dossier
            dataOracleJSON=donnees_oracle.main()
            try:
                req3="UPDATE relation SET datajson='"+dataOracleJSON+"' WHERE id_structure="+str(ids[1])+" AND id_site="+str(ids[2])+";"
                connexion.cursor.execute(req3)
                connexion.mydb.commit()
            except:
                req="SELECT name FROM structure WHERE id_structure="+str(ids[1])+";"
                connexion.cursor.execute(req)
                structure_name=connexion.cursor.fetchone()
                print("["+datetime.datetime.today().isoformat(sep=" ",timespec="seconds")+"] les identifiants sont peut-être incorrects : site - Oracle  structure - "+structure_name[0])
                continue
        # if int(ids[2]==4):
        #     req2="SELECT login,company,password FROM authentification WHERE id_site="+str(ids[2])+" AND id_structure="+str(ids[1])+";"
        #     connexion.cursor.execute(req2)
        #     identifiants=connexion.cursor.fetchall()
        #     antiCaptcha.account=identifiants[0][0]
        #     antiCaptcha.pinCode=identifiants[0][1]
        #     antiCaptcha.passphrase=identifiants[0][2]
        #     antiCaptcha.dossier=dossier
        #     dataUberJSON=antiCaptcha.main()
        #     try:
        #         req3="UPDATE relation SET datajson='"+dataUberJSON+"' WHERE id_structure="+str(ids[1])+" AND id_site="+str(ids[2])+";"
        #         connexion.cursor.execute(req3)
        #         connexion.mydb.commit()
        #     except:
        #         req="SELECT name FROM structure WHERE id_structure="+str(ids[1])+";"
        #         connexion.cursor.execute(req)
        #         structure_name=connexion.cursor.fetchone()
        #         print("["+datetime.datetime.today().isoformat(sep=" ",timespec="seconds")+"] les identifiants sont peut-être incorrects : site - UBER  structure - "+structure_name[0])
        #         continue

    print('['+datetime.datetime.today().isoformat(sep=" ",timespec="seconds")+'] database updated')
