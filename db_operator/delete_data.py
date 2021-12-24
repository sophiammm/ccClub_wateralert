from db_operator.base_manager import PostgresBaseManager


def delete_user_location(user_id):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    sql = f"DELETE FROM usrLocation WHERE ownerID='{user_id}';"
    try:
        cur.execute(sql)
        postgres_manager.conn.commit()
    except Exception as e:
        print("Read failed.")
        print(e)
    finally:
        cur.close()
