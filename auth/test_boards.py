import pytest
import requests
from http import HTTPStatus
from data.boards_data import positive_case, negative_case
from util.time import to_epoch


class TestBoards:
    created_at_buffer = 1

    @pytest.mark.parametrize("req, exp_status_code, err_msg", negative_case)
    def test_create_invalid_board(self, base_url, req, exp_status_code, err_msg, auth_header):
        response = requests.post(f"{base_url}/boards", json=req, headers=auth_header)
        assert response.status_code == exp_status_code
        assert err_msg in response.json()['errors']

    @pytest.mark.parametrize("req, exp_status_code", positive_case)
    def test_create_delete_fetch_new_board(self, base_url, auth_header, req, exp_status_code, clear_boards):
        clear_boards()
        response = requests.post(f"{base_url}/boards", json=req, headers=auth_header)
        json = response.json()
        assert response.status_code == exp_status_code
        assert json['id'] > 0
        assert json['description'] is None
        assert json['title'] == req['title']
        assert to_epoch(json['createdAt']) - to_epoch(json['updatedAt']) <= self.created_at_buffer

        # fetch the created board
        search = requests.get(f"{base_url}/boards/{json['id']}", headers=auth_header)
        assert search.json()['id'] == json['id']
        assert search.status_code == HTTPStatus.OK
        id = response.json()['id']

        # delete the created board
        delete_response = requests.delete(f"{base_url}/boards/{id}", headers=auth_header)
        delete_response.status_code == HTTPStatus.OK

        # invalid fetch, as board is deleted previously
        fetch_response = requests.get(f"{base_url}/boards/{id}", headers=auth_header)
        assert fetch_response.status_code == HTTPStatus.NOT_FOUND
        assert 'board with id {} not found'.format(id) in fetch_response.json()['errors']
