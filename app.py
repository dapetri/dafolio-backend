import os
from flask import Flask, jsonify, request
import requests
from loguru import logger
from src.models import Location, db
from flask_cors import CORS

from src.utils import restrict_to_local_network

logger.add("logs/app.log", rotation="500 MB", level="INFO")

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def process_client_meta():
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    response = requests.get(
        f'https://api.ipgeolocation.io/ipgeo?apiKey={os.getenv("IPGEOLOCATION_API_KEY")}&ip={client_ip}'
    )

    if response.status_code == 200:
        client_info = response.json()
        location = Location(
            ip=client_info.get("ip"),
            continent_code=client_info.get("continent_code"),
            continent_name=client_info.get("continent_name"),
            country_code2=client_info.get("country_code2"),
            country_code3=client_info.get("country_code3"),
            country_name=client_info.get("country_name"),
            city=client_info.get("city"),
            zipcode=client_info.get("zipcode"),
            latitude=client_info.get("latitude"),
            longitude=client_info.get("longitude"),
            isp=client_info.get("isp"),
        )

        try:
            db.session.add(location)
            db.session.commit()
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            db.session.rollback()

    else:
        logger.error(
            f"IPGeolocation API error: {response.status_code} - {response.text}"
        )

    return "Thank you!", 200


@app.route("/locations", methods=["GET", "POST"])
def locations():
    if request.method == "GET":
        return get_locations()
    elif request.method == "POST":
        return add_location()


def get_locations():
    try:
        locations = Location.query.all()

        features = []
        for location in locations:
            if location.latitude and location.longitude:
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            float(location.longitude),
                            float(location.latitude),
                        ],
                    },
                }
                features.append(feature)

        geojson = {"type": "FeatureCollection", "features": features}

        return jsonify(geojson)

    except Exception as e:
        logger.error(f"Error getting locations: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


def add_location():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        location = Location(
            ip=data.get("ip"),
            continent_code=data.get("continent_code"),
            continent_name=data.get("continent_name"),
            country_code2=data.get("country_code2"),
            country_code3=data.get("country_code3"),
            country_name=data.get("country_name"),
            city=data.get("city"),
            zipcode=data.get("zipcode"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            isp=data.get("isp"),
        )

        db.session.add(location)
        db.session.commit()

        return jsonify({"message": "Location added successfully"}), 201

    except Exception as e:
        logger.error(f"Error adding location: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
