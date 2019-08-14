from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime


Base = declarative_base()


class Crime_Event(Base): #parent
    __tablename__ = 'crime_events'
    id=Column(Integer,primary_key=True)
    complaint_num=Column(Integer)
    date_of_occurance=Column(String)
    time_of_occurance=Column(Text)
    crime_completed_y_n=Column(Text)
    jurisdiction_code=Column(Text)
    jurisdiction_desc=Column(Text)
    report_date=Column(String)
    level_of_offense=Column(Text)
    offense_descr=Column(Text)
    location_id = Column(Integer,ForeignKey('locations.id'))
    victim_id = Column(Integer,ForeignKey('victims.id'))
    suspect_id = Column(Integer,ForeignKey('suspects.id'))

    locations = relationship("Location",back_populates="crimes")
    victims = relationship("Victim",back_populates="crimes")
    suspects = relationship("Suspect",back_populates="crimes")

class Location(Base):
    __tablename__ = 'locations'
    id=Column(Integer,primary_key=True)
    latitude=Column(Float)
    longitude=Column(Float)
    precinct=Column(Integer)
    borough=Column(Text)

    crimes = relationship("Crime_Event",back_populates="locations")



class Victim(Base): #child
    __tablename__ = 'victims'
    id=Column(Integer,primary_key=True)
    age_group = Column(Text)
    race = Column(Text)
    gender = Column(Text)

    crimes = relationship("Crime_Event",back_populates="victims")


class Suspect(Base):
    __tablename__ = 'suspects'
    id=Column(Integer,primary_key=True)
    age_group = Column(Text)
    race = Column(Text)
    gender = Column(Text)

    crimes = relationship("Crime_Event",back_populates="suspects")


engine = create_engine('sqlite:///crime_data.db')
Base.metadata.create_all(engine)
