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

_required = ["CLIENT_SECRET_FILE", "REDIRECT_URI", "PROJECT_ID"]
_missing = [k for k in _required if not os.getenv(k)]
if _missing:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(_missing)}")

CLIENT_SECRET_FILE = os.getenv("CLIENT_SECRET_FILE", "").strip()
REDIRECT_URI = os.getenv("REDIRECT_URI", "").strip()
PROJECT_ID = os.getenv("PROJECT_ID", "").strip()

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
    try:
        flow.fetch_token(authorization_response=str(request.url))
    except Exception as e:
        return {"error": f"Failed to fetch token: {e}"}

    credentials = flow.credentials

    try:
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
    except OSError as e:
        return {"error": f"Failed to save tokens: {e}"}

    return {"status": "tokens saved"}


"""
Goal is to get certain data points from the thermostat
Data points needed: temperature, thermostat mode, thermostat high/low thresholds, ambient/current temperature
"""


def fetch_devices():
    creds = load_credentials()
    headers = {"Authorization": f"Bearer {creds.token}"}
    url = f"https://smartdevicemanagement.googleapis.com/v1/enterprises/{PROJECT_ID}/devices"
    response = requests.get(url, headers=headers)
    if not response.ok:
        raise RuntimeError(f"SDM API error {response.status_code}: {response.text}")

    data = response.json()
    readings = []
    for device in data.get("devices", []):
        readings.append(
            {
                "current_temperature": NestDataExtraction.get_temperature(device),
                "set_point_heat": NestDataExtraction.get_thermostat_temp_set_points_heat(
                    device
                ),
                "set_point_cool": NestDataExtraction.get_thermostat_temp_set_points_cool(
                    device
                ),
                "status": NestDataExtraction.get_thermostat_hvac_status(device),
                "mode": NestDataExtraction.get_thermostat_mode(device),
            }
        )
    return readings


@app.get("/nest/devices")
def get_data():
    try:
        return fetch_devices()
    except RuntimeError as e:
        return {"error": str(e)}


def load_credentials():
    try:
        with open("tokens.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise RuntimeError("tokens.json not found — complete OAuth flow at /auth/login first")
    except (OSError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Failed to read tokens.json: {e}")

    creds = Credentials(**data)

    if creds.expired and creds.refresh_token:
        try:
            creds.refresh(GoogleRequest())
        except Exception as e:
            raise RuntimeError(f"Failed to refresh credentials: {e}")

        try:
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
        except OSError as e:
            raise RuntimeError(f"Failed to save refreshed tokens: {e}")

    return creds
