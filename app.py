import os
from flask import Flask, request
import requests
from loguru import logger
from src.models import Location, db

logger.add("logs/app.log", rotation="500 MB", level="INFO")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/")
def process_client_meta():
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    response = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={os.getenv("IPGEOLOCATION_API_KEY")}&ip={client_ip}')
    
    if response.status_code == 200:
        client_info = response.json()
        location = Location(
            ip=client_info.get('ip'),
            continent_code=client_info.get('continent_code'),
            continent_name=client_info.get('continent_name'),
            country_code2=client_info.get('country_code2'),
            country_code3=client_info.get('country_code3'),
            country_name=client_info.get('country_name'),
            city=client_info.get('city'),
            zipcode=client_info.get('zipcode'),
            latitude=client_info.get('latitude'),
            longitude=client_info.get('longitude'),
            isp=client_info.get('isp'),
        )
        
        try:
            db.session.add(location)
            db.session.commit()
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            db.session.rollback()
                
    else:
        logger.error(f"IPGeolocation API error: {response.status_code} - {response.text}")
            
    return "Thank you!", 200
