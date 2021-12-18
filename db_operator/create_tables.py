from db_operator.base_manager import PostgresBaseManager

postgres_manager = PostgresBaseManager()
cur = postgres_manager.conn.cursor()


def create_city_town_table():
    cur.execute(
        """
        CREATE TABLE City_Town (
            cityID varchar(10),
            cityName varchar(5),
            townID varchar(12) PRIMARY key,
            townName varchar(5)
        );
        """
    )
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")


def create_all_table():
    cur.execute(
        """
        CREATE TABLE Rain_Warning (
        stationNo varchar(12) PRIMARY key,
        townCode varchar(12),
        APIupdateTime int,
        DBupdateTime int,
        warningLevel smallint
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE Rain_Station (
        stationNo varchar(12) PRIMARY key,
        stationName varchar(10),
        latitude decimal(11,7),
        longitude decimal(11,7),
        DBupdateTime int
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE Water_Warning (
        stationNo varchar(12) PRIMARY key,
        townCode varchar(12),
        APIupdateTime int,
        DBupdateTime int,
        warningLevel smallint
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE Water_Station (
        stationNo varchar(12) PRIMARY key,
        stationName varchar(10),
        latitude decimal(11,7),
        longitude decimal(11,7),
        DBupdateTime int
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE Reservoir_Warning (
        stationNo varchar(12) PRIMARY key,
        townCode varchar(12),
        APIupdateTime int,
        DBupdateTime int,
        nextSpillTime int
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE Reservoir_Station (
        stationNo varchar(12) PRIMARY key,
        stationName varchar(10),
        latitude decimal(11,7),
        longitude decimal(11,7),
        DBupdateTime int
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE Reservoir_Affected (
        stationNo varchar(12) PRIMARY key,
        cityCode varchar(10),
        townCode varchar(12),
        DBupdateTime int
        );
        """
    )
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")
