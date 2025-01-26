from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), nullable=False)
    continent_code = db.Column(db.String(2))
    continent_name = db.Column(db.String(50))
    country_code2 = db.Column(db.String(2))
    country_code3 = db.Column(db.String(3))
    country_name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    zipcode = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    isp = db.Column(db.String(100))


#     "ip": "151.68.50.144",
#     "continent_code": "EU",
#     "continent_name": "Europe",
#     "country_code2": "IT",
#     "country_code3": "ITA",
#     "country_name": "Italy",
#     "city": "Milano",
#     "zipcode": "20122",
#     "latitude": "45.46420",
#     "longitude": "9.18998",
#     "isp": "WIND TRE S.P.A.",