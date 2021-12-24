from datetime import datetime


def date_to_stamp(date: str) -> int:
    # format:yyyy-MM-dd HH:mm
    dt = datetime.fromisoformat(date)
    timestamp = int(dt.timestamp())
    return timestamp


def stamp_to_date(stamp: int) -> datetime:
    dt = datetime.fromtimestamp(stamp)
    return dt


if __name__ == "__main__":
    cur = datetime.now()
    no = date_to_stamp(str(cur))
    print(stamp_to_date(no))
