import json
import logging
from typing import Iterable
from time import sleep

import vk

from credentials import API_VERSION, ACCESS_TOKEN
from helping_func import merge_arrays, logging_all_class_methods

logging.basicConfig(filename="sample.log", level=logging.INFO)


@logging_all_class_methods
class VkTarget:
    def __init__(self, filename="data", access_token=ACCESS_TOKEN):
        self.__vk_session = vk.Session(access_token=access_token)
        self._api = vk.API(self.__vk_session)
        self.output_filename = filename
        self.timeout = 1

    def get_group_users(self, _group_id: int, **kwargs) -> list:
        first = self._api.groups.getMembers(group_id=_group_id, v=API_VERSION, **kwargs)
        data = first.get("items")
        count = first.get("count") // 1000
        for i in range(1, count + 1):
            data += self._api.groups.getMembers(group_id=_group_id, v=API_VERSION,
                                                offset=i * 1000, **kwargs).get(
                "items")
            sleep(self.timeout)
        data = merge_arrays(data)
        return data

    def save_data(self, data: list or dict, filename=None):
        if filename:
            self.output_filename = filename
        is_dict = isinstance(data, dict)
        if is_dict:
            file_extension = "json"
        else:
            file_extension = "txt"
        full_filename = ".".join((self.output_filename, file_extension))
        with open(full_filename, "w") as file:
            if is_dict:
                json.dump(data, file, indent=4)
            else:
                for item in data:
                    file.write("vk.com/id" + str(item) + "\n")

    def get_overlapping_people(self, *users_collection: list or tuple):
        """
        param: users_collection - many arrays with users
        returned value: users who is in all arrays
        """
        all_people_in_all_groups = list()

        for pack_of_users in users_collection:
            all_people_in_all_groups.append(pack_of_users)
        overlapping_people = list(set(merge_arrays(all_people_in_all_groups)))
        self.save_data(overlapping_people)
        return overlapping_people

    # TODO: add parametrs to query
    def search_groups(self, query, **kwargs):
        data = dict()
        result_of_search = self._api.groups.search(q=query, v=API_VERSION, count=1000,
                                                   **kwargs)
        data[query] = result_of_search.get("items")
        self.save_data(data)
        return data

    def get_user_followers(self, _user_id, _count=1000):
        first = self._api.users.getFollowers(user_id=_user_id, v=API_VERSION, count=_count)
        user_data = first.get("items")
        count = first.get("count") // 1000

        for i in range(1, count + 1):
            user_data += self._api.users.getFollowers(user_id=_user_id, v=API_VERSION,
                                                      offset=i * 1000, count=_count).get(
                "items")
            sleep(self.timeout)

        user_data = merge_arrays(user_data)
        return user_data

    def search_users(self, query, fields=None, **kwargs):
        data = list()
        result_of_search = self._api.users.search(q=query, v=API_VERSION, count=1000,
                                                  **kwargs)

        data.append(result_of_search.get("items"))

        count = result_of_search.get("count") // 1000

        for i in range(1, count + 1):
            data.append(self._api.users.search(q=query, v=API_VERSION, count=1000, offset=i * 1000,
                                               **kwargs))
            sleep(self.timeout)
        data = merge_arrays(data)
        return data

    def get_friend_of_user(self, _user_id: int, **kwargs) -> list:
        try:
            result = self._api.friends.get(user_id=_user_id, v=API_VERSION, **kwargs)
            result = result.get("items")
        except:
            print(f"Profile with {_user_id=} is private")
            result = None
        return result
    # TODO: Аналитика, Аудитория постов, Комментарии, Аудитория фотоальбомов, Активная аудитория, Поиск постов, Аудитория сообществ
    # Друзья аудитории, Поиск по Дню рождения
    #


if __name__ == '__main__':
    x = VkTarget()
    print(x.get_friend_of_user(324))
