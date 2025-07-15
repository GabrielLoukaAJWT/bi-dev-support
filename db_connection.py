import sys
import constants as cta

import oracledb 
import getpass
import os
import platform


def test_oracle_instant_client():
    print("ARCH:", platform.architecture())
    print("FILES AT lib_dir:")
    for name in os.listdir(cta.LIB_DIR):
        print(name)


def connect_to_oracle() -> None :
    try:
        oracledb.init_oracle_client(lib_dir=cta.LIB_DIR)
        print("Connection successful :)\n")
    except Exception as error:
        print("Error connecting: cx_Oracle.init_oracle_client()")
        print(error)
        sys.exit(1)

    passwordOcl = getpass.getpass(f"Enter password for {cta.USERNAME}@{cta.CONNECTION_STRING}: ")

    with oracledb.connect(user=cta.USERNAME, password=passwordOcl, dsn=cta.CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            sql = "select woo.si_number, woo.entry_date from wo_operation woo where (woo.entry_date > SYSDATE - INTERVAL '1' MONTH)"
            for r in cursor.execute(sql):
                print(r)