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
                user_telegram_bot_id varchar, 
                user_email varchar,
                user_password varchar,
                user_hashed_password varchar,
                user_type int,
                min_heart_rate decimal DEFAULT NULL,
                max_heart_rate decimal DEFAULT NULL,
                min_body_temprature decimal DEFAULT NULL,
                max_body_temprature decimal DEFAULT NULL
            );
        """
        #user_type=0:admin 1:doctor 2:sick 3:device 4:disabled
        execute_query(query,max_retry=50)
    except Exception as ex:
        print("=========================================================================================")
        print(ex)
        print("Users creation failed")
        print(query)
    try:
        query = """
                    
            INSERT INTO users_table
                ( user_name,user_lastname,user_email,user_password,user_hashed_password,user_type,user_telegram_bot_id)
            SELECT  'admin','admin','admin@admin.com','123456','123456',0,''
            WHERE
                NOT EXISTS (
                    SELECT id FROM users_table WHERE user_email = 'admin@admin.com'
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

    try:
        query = """
        DO $$
        BEGIN
            -- Check if the foreign key constraint already exists
            IF NOT EXISTS (
                SELECT 1
                FROM information_schema.table_constraints
                WHERE constraint_type = 'FOREIGN KEY'
                  AND table_name = 'messagge_content'
                  AND constraint_name = 'fk_users_messages_sender'
            ) THEN
                -- Add the foreign key constraint
                ALTER TABLE messages_table
                ADD CONSTRAINT fk_users_messages_sender
                FOREIGN KEY (sender_id)
                REFERENCES users_table (id)
                ON DELETE CASCADE;
            END IF;
        
            -- Check if the foreign key constraint already exists
            IF NOT EXISTS (
                SELECT 1
                FROM information_schema.table_constraints
                WHERE constraint_type = 'FOREIGN KEY'
                  AND table_name = 'messagge_content'
                  AND constraint_name = 'fk_users_messages_reciever'
            ) THEN
                -- Add the foreign key constraint
                ALTER TABLE messages_table
                ADD CONSTRAINT fk_users_messages_reciever
                FOREIGN KEY (sender_id)
                REFERENCES users_table (id)
                ON DELETE CASCADE;
            END IF;
        END $$;
        """
        execute_query(query,max_retry=50)
    except Exception as ex:
        print("=========================================================================================")
        print(ex)
        print("Users creation failed")
        print(query)

    try:
        query = """
        ALTER TABLE users_table
        ADD CONSTRAINT users_table_id_unique UNIQUE (id);
        """
        execute_query(query, max_retry=50)
    except Exception as ex:
        print("=========================================================================================")
        print(ex)
        print("Users creation failed")
        print(query)