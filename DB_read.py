from DB_basic import PostgresBaseManager


def getWarn(table):
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    try:
        cur.execute(
            f"SELECT * FROM {table}")
        # Retrieve all rows from the PostgreSQL table
        results = cur.fetchall()
        postgres_manager.conn.commit()
    except Exception as e:
        print("Read failed.")
        print(e)
    finally:
        cur.close()
        return results


if __name__ == "__main__":
    print(getWarn("Rain_Warning"))
