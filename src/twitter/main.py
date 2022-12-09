import cleanser
from constants import EN_TWITTER_ID
from database import Session
from models import RawMetric
from user import User

if __name__ == "__main__":
    users = User(ids=EN_TWITTER_ID)
    users.save_to_db()

    session = Session()
    last_record = session.query(RawMetric).order_by(RawMetric.id.desc()).first()
    cleanser.save_to_db([last_record])

#  sudo crontab -u aowang -e\l
#  sudo service cron restart
