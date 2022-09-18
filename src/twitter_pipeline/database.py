from typing import Dict

from decouple import config
from sqlalchemy import MetaData, Table, Column, Integer, DateTime, JSON
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy_utils import database_exists, create_database

DB_USERNAME = config("db_username")
DB_PASSWORD = config("db_password")
DB_HOSTNAME = config("db_hostname")
DB_PORT = config("db_port")
DB_NAME = config("db_name")

SQLALCHEMY_DB_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}"

metadata_obj = MetaData()

raw_tweets = Table(
    "raw_tweets",
    metadata_obj,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("recorded_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column("data", JSON, nullable=False)
)

engine = create_engine(SQLALCHEMY_DB_URL)


def save_to_db(data: Dict) -> None:
    ins = raw_tweets.insert().values(data=data)
    conn = engine.connect()
    conn.execute(ins)
    conn.close()


def main() -> None:
    if not database_exists(engine.url):
        create_database(engine.url)

    print(f"{database_exists(engine.url)=}")

    metadata_obj.create_all(engine)


if __name__ == "__main__":
    main()
