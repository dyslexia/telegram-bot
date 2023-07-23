import os

from requests import get, post
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DUNE_API_KEY")
HEADER = {"x-dune-api-key": API_KEY}
BASE_URL = "https://api.dune.com/api/v1/"


def make_api_url(module, action, ID):
    url = BASE_URL + module + "/" + ID + "/" + action
    return url


def execute_query(query_id, engine="small"):
    url = make_api_url("query", "execute", query_id)
    params = {
        "performance": engine,
    }
    response = post(url, headers=HEADER, params=params)
    execution_id = response.json()['execution_id']
    return execution_id


def get_query_status(execution_id):
    url = make_api_url("execution", "status", execution_id)
    response = get(url, headers=HEADER)
    return response


def get_query_results(execution_id):
    url = make_api_url("execution", "results", execution_id)
    response = get(url, headers=HEADER)
    return response


def cancel_query_execution(execution_id):
    url = make_api_url("execution", "cancel", execution_id)
    response = get(url, headers=HEADER)
    return response
