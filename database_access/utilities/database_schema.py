from utilities.db_tools import execute_query


def tables_creation():
    query=""
    try:
        query = """
        CREATE TABLE IF NOT EXISTS service_catalog
            (
                id           bigint generated always as identity (minvalue 0),
                service_name varchar,
                service_value varchar,
                last_usage   timestamp default now(),
                last_state   char
            );
        """
        execute_query(query,max_retry=50)
    except Exception as ex:
        print("=========================================================================================")
        print(ex)
        print("configs creation failed")
        print(query)
    try:
        query = """
        CREATE TABLE IF NOT EXISTS users_table
            (
                id bigint generated always as identity (minvalue 0),
                user_name varchar,
                user_lastname varchar, 
                user_email varchar,
                user_password varchar,
                user_hashed_password varchar,
                user_type int
            );
        """
        #user_type=0:admin 1:doctor 2:sick 3:device 4:disabled
        execute_query(query,max_retry=50)
    except Exception as ex:
        print("=========================================================================================")
        print(ex)
        print("Users creation failed")
        print(query)
#Messaging Table
    try:
        query = """
        CREATE TABLE IF NOT EXISTS messages_table
            (
                id bigint generated always as identity (minvalue 0),
                sender_id bigint,
                reciever_id bigint,
                messagge_content varchar, 
                creation_date timestamp default now(),
                message_state int
            );
        """
                ##message_state:[0:sent,1:recieved,2:read,3:deleted,4:accepted,5:rejected,6:notification]
        execute_query(query,max_retry=50)
    except Exception as ex:
        print("=========================================================================================")
        print(ex)
        print("Messaging creation failed")
        print(query)

    try:
        query = """
        CREATE TABLE IF NOT EXISTS users_doctors_table
            (
                id bigint generated always as identity (minvalue 0),
                docter_user_id bigint,
                sick_user_id bigint
            );
        """
        execute_query(query,max_retry=50)
    except Exception as ex:
        print("=========================================================================================")
        print(ex)
        print("Users creation failed")
        print(query)