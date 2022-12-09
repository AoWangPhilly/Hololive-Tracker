from sqlalchemy import Integer, JSON, DateTime, func, Column, String, Numeric, UniqueConstraint

from database import Base, engine


class RawMetric(Base):
    __tablename__ = "raw_metrics"

    id = Column(Integer, primary_key=True, nullable=False)
    datetime = Column(DateTime, server_default=func.now())
    data = Column(JSON, nullable=False)


class CleansedMetric(Base):
    __tablename__ = "cleansed_metrics"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    twitter_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    description = Column(String, nullable=False)
    followers_count = Column(Integer, nullable=False)
    following_count = Column(Integer, nullable=False)
    listed_count = Column(Integer, nullable=False)
    tweet_count = Column(Integer, nullable=False)
    profile_image_url = Column(String, nullable=False)
    youtube_channel_id = Column(String, nullable=False)
    unix_id = Column(Numeric, nullable=False)

    __table_args__ = (UniqueConstraint("twitter_id", "unix_id", name="_idol_metric"),)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
