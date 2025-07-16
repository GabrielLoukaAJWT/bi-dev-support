import sys
import constants as cta

import oracledb 
import os
import platform


def test_oracle_instant_client():
    print("ARCH:", platform.architecture())
    print("FILES AT lib_dir:")
    for name in os.listdir(cta.LIB_DIR):
        print(name)


def connect_to_oracle(psw : str) -> bool :
    try:
        oracledb.init_oracle_client(lib_dir=cta.LIB_DIR)
        print("Initialized Oracle Instant Client.\n")
    except Exception as error:
        print("Error connecting: cx_Oracle.init_oracle_client()")
        print(error)

    try:    
        with oracledb.connect(user=cta.USERNAME, password=psw, dsn=cta.CONNECTION_STRING) as connection:
            with connection.cursor() as cursor:
                print("Valid credentials - connection successful.\n")
                return True, cta.DB_CONNEXION_SUCCESS
    except Exception as error:
        print("Invalid credentials - connexion denied.\n")
        return False, cta.DB_CONNEXION_ERROR
        


            # sql = "select woo.si_number, woo.entry_date from wo_operation woo where (woo.entry_date > SYSDATE - INTERVAL '1' MONTH)"
            # for r in cursor.execute(sql):
            #     print(r)