import json
import os
import time

import psycopg2


def database_connection(database_name='postgres'):
    if os.environ['environment'] == 'running':
        return psycopg2.connect(
            dbname=os.environ['RD_database_name'],
            user=os.environ['RD_user_name'],
            password=os.environ['RD_user_password'],
            host=os.environ['RD_host'],
            port=os.environ['RD_port_number'],
            connect_timeout=os.environ['RD_time_out']
        )
    else:
        return psycopg2.connect(
            dbname=database_name,
            user='postgres',
            password='ComeToSchool1367',
            host='127.0.0.1',
            port=5432,
            connect_timeout=30
        )


def fetch_list(db_quey):
    conn = database_connection()
    cur = conn.cursor()
    print(db_quey)
    cur.execute(db_quey)
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return rows


def execute_query(db_quey,max_retry=0):
    counter= max_retry
    while True:
        try:
            print("Running this query.")
            print(db_quey)
            conn = database_connection(database_name='postgres')
            cur = conn.cursor()
            cur.execute(db_quey)
            id_of_new_row = 0  #cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            print("Query executed successfully")
            print(db_quey)
            return id_of_new_row
        except Exception as e:
            if counter > 0:
                print("=============================================================")
                print("Query Excution failed :")
                print(str(e))
                counter -= 1
                time.sleep(5)
            else:
                raise


def create_database_query(db_quey):
    try:
        conn = database_connection(database_name='postgres')
        cur = conn.cursor()
        print("Running this query.")
        print(db_quey)
        cur.execute(db_quey)
        id_of_new_row = 0  #cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        print("Query executed successfully")
        print(db_quey)
        return id_of_new_row
    except:
        raise
