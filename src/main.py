import src.models as models
import src.twitter.cleanser as twitter_cleanser
import src.youtube.cleanser as youtube_cleanser
from src.constants import EN_TWITTER_ID, EN_YOUTUBE_CHANNEL_ID
from src.database import Session, engine, setup_db
from src.twitter.user import User
from src.youtube.channel import Channel


def main() -> None:
    setup_db()
    models.Base.metadata.create_all(engine)

    session = Session()

    users = User(ids=EN_TWITTER_ID)
    users.save_to_db(models.RawTwitterMetric)
    last_record = session.query(models.RawTwitterMetric).order_by(models.RawTwitterMetric.id.desc()).first()
    twitter_cleanser.save_to_db([last_record])

    channel = Channel(channel_id="")
    for channel_id in EN_YOUTUBE_CHANNEL_ID:
        channel.set_channel_id(channel_id=channel_id)
        channel.save_to_db(models.RawYouTubeMetric)
        last_record = session.query(models.RawYouTubeMetric).order_by(models.RawYouTubeMetric.id.desc()).first()
        youtube_cleanser.save_to_db(last_record)


if __name__ == "__main__":
    main()

#  sudo crontab -u aowang -e\l
#  sudo service cron restart
#  cd "/mnt/c/Users/Ao Wang/projects/Hololive-Tracker" && /home/aowang/.virtualenvs/Hololive-Tracker/bin/python3 -m src.main
