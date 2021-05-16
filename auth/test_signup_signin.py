import time
import pytest
import jwt
import requests
from http import HTTPStatus
from util.time import num_seconds
from data.signup_signin_data import negative_cases, positive_case, user_conflict_case


class TestSignupSignin:
    jwt_buffer = 1

    @pytest.mark.parametrize("operation, req, exp_status_code, exp_error_msg", negative_cases)
    def test_unsuccessful_signup_signin(self, clear_users, base_url, operation, req, exp_status_code, exp_error_msg):
        clear_users()

        response = requests.post(f"{base_url}/auth/{operation}", json=req)
        json = response.json()

        assert response.status_code == exp_status_code
        if isinstance(exp_error_msg, list):
            assert exp_error_msg == json['errors']

        else:
            assert exp_error_msg in json['errors']

    @pytest.mark.parametrize("req, exp_status_code, exp_error_msg", user_conflict_case)
    def test_signup_conflict(self, clear_users, base_url, req, exp_status_code, exp_error_msg):
        clear_users()

        response = requests.post(f"{base_url}/auth/signup", json=req)

        assert response.status_code == HTTPStatus.CREATED

        response = requests.post(f"{base_url}/auth/signup", json=req)
        json = response.json()

        assert response.status_code == exp_status_code
        assert exp_error_msg in json['errors']

    @pytest.mark.parametrize("req", positive_case)
    def test_successful_signup_signin(self, clear_users, base_url, req):
        clear_users()

        # Create a new user
        response = requests.post(f"{base_url}/auth/signup", json=req)
        json = response.json()

        # Verify successful signup
        assert response.status_code == HTTPStatus.CREATED
        assert json['id'] > 0
        assert json['username'] == req['username']
        created_user_id = json['id']

        # Signin with created user
        response = requests.post(f"{base_url}/auth/signin", json=req)
        json = response.json()

        # Verify successful signin & JWT payload
        assert response.status_code == HTTPStatus.OK
        jwt_payload = jwt.decode(json['token'], options={'verify_signature': False})
        assert jwt_payload['id'] == created_user_id
        assert jwt_payload['username'] == req['username']

        current_time = int(time.time())
        assert current_time >= jwt_payload['iat'] >= current_time - self.jwt_buffer
        expected_exp = jwt_payload['iat'] + num_seconds()
        assert jwt_payload['exp'] == expected_exp
