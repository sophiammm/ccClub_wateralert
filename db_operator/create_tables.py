from db_operator.base_manager import PostgresBaseManager


def create_city_town_table():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    cur.execute(
        """
        CREATE TABLE City_Town (
            cityCode varchar(10),
            cityName varchar(5),
            townCode varchar(12) PRIMARY key,
            townName varchar(5)
        );
        """
    )
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")


def create_water_related_table():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
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
        latitude decimal(11,7),
        longitude decimal(11,7)
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
        basinName varchar(8),
        latitude decimal(11,7),
        longitude decimal(11,7)
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
        nextSpillTime int,
        status varchar(15)
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE Reservoir_Station (
        stationNo varchar(12) PRIMARY key,
        stationName varchar(10)
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE Reservoir_AffectedArea (
        stationNo varchar(12),
        townCode varchar(12)
        );
        """
    )
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")


def create_user_table():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    cur.execute(
        """
        CREATE TABLE Usr (
            id SERIAL PRIMARY KEY NOT NULL,
            usrName varchar(20) NOT NULL,
            email varchar(50) UNIQUE NOT NULL ,
            password TEXT NOT NULL
        );
        """
    )
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")


def create_user_loc_table():
    postgres_manager = PostgresBaseManager()
    cur = postgres_manager.conn.cursor()
    cur.execute(
        """
        CREATE TABLE usrLocation (
            ownerID INTEGER PRIMARY KEY NOT NULL,
            latitude decimal(11,7),
            longitude decimal(11,7),
            FOREIGN KEY (ownerID) REFERENCES Usr (id)
        );
        """
    )
    postgres_manager.conn.commit()
    cur.close()
    postgres_manager.close_connection()
    print("Operation completed")
