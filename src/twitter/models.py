from sqlalchemy import Integer, JSON, DateTime, func, Column

from src.twitter.database import Base, engine


class RawMetric(Base):
    __tablename__ = "raw_metrics"

    id = Column(Integer, primary_key=True, nullable=False)
    datetime = Column(DateTime, server_default=func.now())
    data = Column(JSON, nullable=False)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
