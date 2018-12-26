import datetime

from sqlalchemy import Column, Date, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Record(Base):
    __tablename__ = 'records'

    category = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)
    url = Column(String)

    def __repr__(self):
        return "<Record(category='%s', date='%s', url='%s')>" % (
            self.category, self.date, self.url)


Base.metadata.create_all(engine)

if __name__ == "__main__":
    session = Session()
    print(session.query(Record).all())
    session.add(Record(category="test", date=datetime.date(
        2018, 12, 26), url="https://pastebin.com/raw/sXCVakjQ"))
    session.commit()
