from typing import List
import requests
from urllib.parse import urljoin


class GroupInfo:
    def __init__(self, name, link, point) -> None:
        self.name = name
        self.point = point
        self.link = link

    @staticmethod
    def parse(j):
        return GroupInfo(j['name'], j['link'], j['point'])


class UserInfo:
    def __init__(self, id, point) -> None:
        self.id = id
        self.point = point

    @staticmethod
    def parse(j):
        return UserInfo(j['id'], j['point'])


class TaskSystem:
    def __init__(self, token: str) -> None:
        self.token = token
        if not self.__validate_token():
            raise ValueError("Token is invalid")

        self.__base_url = 'https://tsww.website/app/api/client{token}/'.format(
            token = self.token
        )

    def __validate_token(self) -> bool:
        parts = self.token.split(':')
        if parts.__len__() != 2:
            return False
        
        if not parts[0].__len__() > 5 or not parts[0].isdigit():
            return False

        if parts[1].__len__() != 36:
            return False

        return True

    def _send_request(self, end_point: str, params = {}):
        url = urljoin(
            self.__base_url, 
            end_point
        )
        result = requests.get(url, params= params)
        json_result = result.json()
        if result.status_code == 200:
            if json_result['ok']:
                return json_result['result']
            else:
                raise requests.ConnectionError(json_result['code'])
        else:
            raise requests.ConnectionError('Invalid status code') 

    def topGroups(self, offset:int = 0, limit:int = 10) -> List[GroupInfo]:
        json = self._send_request('topGroups', {'offset': offset, 'limit': limit})
        result = []
        for x in json:
            result.append(
                GroupInfo.parse(x)
            )

        return result

    def users_count(self):
        return self._send_request('usersCount')

    def is_user(self, user_id:int) -> bool:
        return self._send_request('isUser', {'userId': user_id})

    def get_user(self, user_id:int) -> List[GroupInfo]:
        return UserInfo.parse(self._send_request('getUser', {'userId': user_id}))

    def get_users(self, offset:int = 0, limit:int = 10) -> List[UserInfo]:
        json = self._send_request('getUsers', {'offset': offset, 'limit': limit})
        result = []
        for x in json:
            result.append(
                UserInfo.parse(x)
            )

        return result
