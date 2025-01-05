from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date, DateTime, Float, BigInteger
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from app import db

class Test(db.Model):
    __tablename__='test'
    id = Column(BigInteger, primary_key=True)
    test = Column(String)
    
    def __init__(self, test):
        self.test=test
        