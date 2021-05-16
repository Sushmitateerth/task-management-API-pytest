import jwt
import pytest
import os
import psycopg2
import requests
from dotenv import load_dotenv
from data.get_board_operations_data import multiple_boards

load_dotenv()


@pytest.fixture(scope="module")
def base_url():
    return os.getenv("BASE_URL")


@pytest.fixture(scope="module")
def db_config():
    return {
        'user': os.getenv("USER"),
        'host': os.getenv("HOST"),
        'port': os.getenv("PORT"),
        'dbname': os.getenv("DBNAME"),
        'password': os.getenv("PASSWORD"),
    }


@pytest.fixture(scope="module")
def auth_header(base_url):
    user = {"username": "test3 user", "password": "Passw0rd!"}
    requests.post(f"{base_url}/auth/signup", json=user)
    response = requests.post(f"{base_url}/auth/signin", json=user)
    token = response.json()['token']
    header = {"Authorization": f"Bearer {token}"}

    return header


@pytest.fixture(scope="module")
def create_boards(base_url, auth_header, clear_boards):
    clear_boards()
    board_list = []
    for board in multiple_boards:
        response = requests.post(f"{base_url}/boards", json=board, headers=auth_header)
        json = response.json()
        board_list.append(json)
    return board_list


@pytest.fixture(scope="module")
def clear_users(db_config):
    def fn():
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM public."User"')

    return fn


@pytest.fixture(scope="module")
def clear_boards(db_config):
    def fn():
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                cur.execute('DELETE FROM public."Board"')

    return fn
