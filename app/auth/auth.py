from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Request
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest
from app.helpers.thermo_helpers import NestDataExtraction
from dotenv import load_dotenv
import os

import google_auth_oauthlib.flow
import requests, json

load_dotenv()

CLIENT_SECRET_FILE = os.getenv("CLIENT_SECRET_FILE")
REDIRECT_URI = os.getenv("REDIRECT_URI")
PROJECT_ID = os.getenv("PROJECT_ID")

app = FastAPI()


def auth_flow():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=[
            "https://www.googleapis.com/auth/sdm.service",
        ],
    )
    flow.redirect_uri = REDIRECT_URI
    return flow


@app.get("/auth/login")
def login():
    flow = auth_flow()
    authorization_url, _ = flow.authorization_url(
        access_type="offline", include_granted_scope="true", prompt="consent"
    )
    return RedirectResponse(authorization_url)


@app.get("/auth/callback")
def callback(request: Request):
    flow = auth_flow()
    flow.fetch_token(authorization_response=str(request.url))
    credentials = flow.credentials

    with open("tokens.json", "w") as f:
        json.dump(
            {
                "token": credentials.token,
                "refresh_token": credentials.refresh_token,
                "token_uri": credentials.token_uri,  # type: ignore
                "client_id": credentials.client_id,
                "client_secret": credentials.client_secret,
                "scopes": credentials.scopes,
            },
            f,
        )
        return {"status": "tokens saved"}


"""
Goal is to get certain data points from the thermostat
Data points needed: temperature, thermostat mode, thermostat high/low thresholds, ambient/current temperature
"""


@app.get("/nest/devices")
def get_data():
    creds = load_credentials()
    headers = {"Authorization": f"Bearer {creds.token}"}
    url = f"https://smartdevicemanagement.googleapis.com/v1/enterprises/{PROJECT_ID}/devices"
    response = requests.get(url, headers=headers)
    data = response.json()
    readings = []
    for device in data.get("devices"):
        readings.append(
            {
                "temperature": NestDataExtraction.get_temperature(device),
                "mode": NestDataExtraction.get_thermostat_temp_set_points(device),
                "status": NestDataExtraction.get_thermostat_hvac_status(device),
                "heater_threshold": NestDataExtraction.get_thermostat_mode(device),
            }
        )
    return readings


def load_credentials():
    with open("tokens.json", "r") as f:
        data = json.load(f)

    creds = Credentials(**data)

    if creds.expired and creds.refresh_token:
        creds.refresh(GoogleRequest())

        with open("tokens.json", "w") as f:
            json.dump(
                {
                    "token": creds.token,
                    "refresh_token": creds.refresh_token,
                    "token_uri": creds.token_uri,
                    "client_id": creds.client_id,
                    "client_secret": creds.client_secret,
                    "scopes": creds.scopes,
                },
                f,
            )
    return creds
