import json
from http import HTTPStatus
import requests
from data.get_board_operations_data import *


class TestGetBoardOperations:

    def test_fetch_boards(self, base_url, create_boards, auth_header):
        fetch_response = requests.get(f"{base_url}/boards", headers=auth_header)
        assert fetch_response.status_code == HTTPStatus.OK
        json = fetch_response.json()
        assert len(multiple_boards) == len(json)
        for expected, actual in zip(multiple_boards, json):
            assert expected['title'] == actual['title']
            assert expected['description'] == actual['description']
            assert actual['id'] > 0

    def test_search_board(self, base_url, create_boards, auth_header):
        response = requests.get(f"{base_url}/boards?search={search_board}", headers=auth_header)
        json = response.json()
        assert response.status_code == HTTPStatus.OK
        assert json[0]['title'] == search_board

    def test_filter_by_created_date(self, base_url, auth_header, create_boards):
        board_index = int(len(create_boards) / 2)
        middle_board = create_boards[board_index]
        created_at = middle_board['createdAt']
        api_filter = {
            "createdAt": {
                "gt": created_at
            }
        }
        # json.dumps converts dictionary to json
        response = requests.get(f"{base_url}/boards/?filter={json.dumps(api_filter)}", headers=auth_header)
        json_response = response.json()
        assert response.status_code == HTTPStatus.OK

        # list slicing so that parmas.board will be obtained from middle index for comparision
        expected_board = multiple_boards[board_index + 1:len(multiple_boards):]
        for actual, expected in zip(json_response, expected_board):
            assert actual['title'] == expected['title']
            assert actual['description'] == expected['description']

    def test_sort_boards(self, create_boards, base_url, auth_header):
        sort_input = [
            {
                "description": "asc"
            }
        ]
        sort_response = requests.get(f"{base_url}/boards/?sort={json.dumps(sort_input)}",
                                     headers=auth_header)
        actual_result = sort_response.json()
        assert sort_response.status_code == HTTPStatus.OK
        for actual, expected in zip(actual_result, sort_by_description):
            assert actual['description'] == expected['description']

    def test_pagination(self, base_url, auth_header, create_boards):
        search_response = requests.get(f"{base_url}/boards/?skip={skip}&limit={limit}",
                                       headers=auth_header)
        json_response = search_response.json()
        assert search_response.status_code == HTTPStatus.OK
        expected_list = create_boards[skip: skip + limit:]
        for actual, expected in zip(expected_list, json_response):
            assert actual['title'] == expected['title']
            assert actual['description'] == expected['description']
