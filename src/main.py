import src.twitter.cleanser as cleanser
from src.constants import EN_TWITTER_ID
from src.database import Session
from src.models import RawTwitterMetric
from src.twitter.user import User


def main() -> None:
    users = User(ids=EN_TWITTER_ID)
    users.save_to_db()
    session = Session()
    last_record = session.query(RawTwitterMetric).order_by(RawTwitterMetric.id.desc()).first()
    cleanser.save_to_db([last_record])


if __name__ == "__main__":
    main()

#  sudo crontab -u aowang -e\l
#  sudo service cron restart
