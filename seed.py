#!/usr/bin/env python3

# Script goes here!
# from faker import Faker
# import random

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///hospital.db")
session = Session(engine, future = True)

