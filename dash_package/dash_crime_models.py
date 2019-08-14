from sqlalchemy import Column, Integer, Text, Date
from dash_package import db


class Crime_Event(db.Model): #parent
    __tablename__ = 'crime_events'
    id=db.Column(db.Integer,primary_key=True)
    complaint_num=db.Column(db.Integer)
    date_of_occurance=db.Column(db.Date)
    time_of_occurance=db.Column(db.String)
    crime_completed_y_n=db.Column(db.Text)
    jurisdiction_code=db.Column(db.Text)
    jurisdiction_desc=db.Column(db.Text)
    report_date=db.Column(db.String)
    level_of_offense=db.Column(db.Text)
    offense_descr=db.Column(db.Text)
    location_id = db.Column(db.Integer,db.ForeignKey('locations.id'))
    victim_id = db.Column(db.Integer,db.ForeignKey('victims.id'))
    suspect_id = db.Column(db.Integer,db.ForeignKey('suspects.id'))

    locations = db.relationship("Location",back_populates="crimes")
    victims = db.relationship("Victim",back_populates="crimes")
    suspects = db.relationship("Suspect",back_populates="crimes")

class Location(db.Model):
    __tablename__ = 'locations'
    id=db.Column(db.Integer,primary_key=True)
    latitude=db.Column(db.Float)
    longitude=db.Column(db.Float)
    precinct=db.Column(db.Integer)
    borough=db.Column(db.Text)

    crimes = db.relationship("Crime_Event",back_populates="locations")


class Victim(db.Model): #child
    __tablename__ = 'victims'
    id=db.Column(db.Integer,primary_key=True)
    age_group = db.Column(db.Text)
    race = db.Column(db.Text)
    gender = db.Column(db.Text)

    crimes = db.relationship("Crime_Event",back_populates="victims")


class Suspect(db.Model):
    __tablename__ = 'suspects'
    id=db.Column(db.Integer,primary_key=True)
    age_group = db.Column(db.Text)
    race = db.Column(db.Text)
    gender = db.Column(db.Text)

    crimes = db.relationship("Crime_Event",back_populates="suspects")
