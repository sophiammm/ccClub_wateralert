from datetime import datetime


def dateToStamp(date: str) -> int:
    # format:yyyy-MM-dd HH:mm
    dt = datetime.fromisoformat(date)
    timestamp = int(dt.timestamp())
    print(timestamp)
    return timestamp


def stampToDate(stamp: int) -> str:
    dt = datetime.fromtimestamp(stamp)
    print(dt)
    return dt


if __name__ == "__main__":
    cur = datetime.now()
    dateToStamp(str(cur))
