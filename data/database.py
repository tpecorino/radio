from sqlalchemy import create_engine, Column, String, Integer, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/db.sqlite"
TABLE_NAME = "stations"


class Station(Base):
    __tablename__ = TABLE_NAME

    id = Column("id", Integer, primary_key=True, autoincrement=True,
                nullable=False, unique=True)
    name = Column("name", String(25))
    url = Column("url", String(255))

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return f"Station" \
               f"(id={self.id!r}, " \
               f"name={self.name!r}, " \
               f"url={self.url!r}, "


def seed_database(db):
    station_1 = Station("Radio Italia", 'https://stream10.xdevel.com/audio1s977004-1749/stream/icecast.audio')
    station_2 = Station("WUNC", 'http://wunc-ice.streamguys1.com:80/wunc-128-mp3')
    station_3 = Station("KUT", 'http://kut.streamguys1.com/kut')
    db.add(station_1)
    db.add(station_2)
    db.add(station_3)
    db.commit()


def fetch_stations(db):
    return db.query(Station).all()


def fetch_entity_by_id(db, pk):
    return db.query(Station).filter(Station.id == pk).first()


def update_station(db, pk, updated_station):
    db.query(Station).filter(Station.id == pk).update(updated_station)
    db.commit()
    return updated_station


def save_station(db, station):
    station = Station(station["name"], station["url"])
    db.add(station)
    db.commit()
    return station


def delete_station(db, station_id):
    db.query(Station).filter(Station.id == station_id).delete()
    db.commit()


def get_database_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == "__main__":
    session = get_database_session()

    # table_exists = inspect(session).has_table(TABLE_NAME)
    stations = fetch_stations(session)
    print('stations', len(stations))
    if not stations:
        print('seed')
        seed_database(session)

    for Station in stations:
        print(f"Station: {Station.name}")
