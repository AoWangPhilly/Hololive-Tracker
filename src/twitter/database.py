from decouple import config
from sqlalchemy import MetaData, create_engine
from sqlalchemy_utils import database_exists, create_database

DB_USERNAME = config("db_username")
DB_PASSWORD = config("db_password")
DB_HOSTNAME = config("db_hostname")
DB_PORT = config("db_port")
DB_NAME = config("db_name")

SQLALCHEMY_DB_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}"

metadata_obj = MetaData()

engine = create_engine(SQLALCHEMY_DB_URL)


def main() -> None:
    if not database_exists(engine.url):
        create_database(engine.url)

    print(f"{database_exists(engine.url)=}")

    metadata_obj.create_all(engine)


if __name__ == "__main__":
    main()
