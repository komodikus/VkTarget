import json
import logging
import datetime
from time import sleep

import vk

from vktargetBackend.vktarg.vk_api.credentials import API_VERSION, ACCESS_TOKEN
from vktargetBackend.vktarg.vk_api.helping_func import merge_arrays, logging_all_class_methods

LOGS_PATH = "logs"
logging.basicConfig(filename="/".join((LOGS_PATH, f"{datetime.datetime.now()}sample.log")),
                    level=logging.INFO)


@logging_all_class_methods
class VkTarget:
    def __init__(self, filename="data", access_token=ACCESS_TOKEN):
        self.__vk_session = vk.Session(access_token=access_token)
        self._api = vk.API(self.__vk_session)
        self.output_filename = filename
        self.timeout = 1

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

    # GROUPS METHODS
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

    def search_groups(self, query, **kwargs):
        """

        """
        data = dict()
        result_of_search = self._api.groups.search(q=query, v=API_VERSION, count=1000,
                                                   **kwargs)
        data[query] = result_of_search.get("items")
        self.save_data(data)
        return data

    # USERS FOLOWERS SEARCH FRIENDS
    def get_user_followers(self, _user_id, _count=1000):
        first = self._api.users.getFollowers(user_id=_user_id, v=API_VERSION, count=_count)
        user_data = first.get("items")
        count = first.get("count") // 1000
        if not count:
            for i in range(1, count + 1):
                user_data += self._api.users.getFollowers(user_id=_user_id, v=API_VERSION,
                                                          offset=i * 1000, count=_count).get(
                    "items")
                sleep(self.timeout)

            user_data = merge_arrays(user_data)
        return user_data

    def search_users(self, query, fields=None, **kwargs):
        data = list()
        func = self._api.users.search

        result_of_search = func(q=query, v=API_VERSION, count=1000,
                                **kwargs)

        data.append(result_of_search.get("items"))

        count = result_of_search.get("count") // 1000
        if not count:
            for i in range(1, count + 1):
                data.append(func(q=query, v=API_VERSION, count=1000, offset=i * 1000,
                                 **kwargs))
                sleep(self.timeout)
            data = merge_arrays(data)
        return data

    def get_friend_of_user(self, _user_id: int, **kwargs) -> list:
        result = self._api.friends.get(user_id=_user_id, v=API_VERSION, **kwargs)
        result = result.get("items")
        return result

    # WALLS POST COMMENTS LIKES REPOSTS ACTIVITY
    def get_wall_posts(self, _owner_id, **kwargs):
        result = self._api.wall.get(owner_id=_owner_id, v=API_VERSION, **kwargs)
        result = result.get("items")
        return result

    def get_wall_comments(self, _owner_id, _post_id, **kwargs):
        """
        if we wont see group comments
        we need use id with minus
        -id
        """
        result = self._api.wall.getComments(owner_id=_owner_id, post_id=_post_id, v=API_VERSION,
                                            count=50, sort="desk", **kwargs)
        result = result.get("items")
        return result

    def get_post_reposts(self, _owner_id, _post_id, **kwargs):
        first = self._api.wall.getReposts(owner_id=_owner_id, post_id=_post_id, v=API_VERSION,
                                          count=1000, **kwargs)
        post_reposts = first.get("items")

        count = first.get("count") // 1000
        if not count:
            for i in range(1, count + 1):
                post_reposts += self._api.wall.getReposts(owner_id=_owner_id, post_id=_post_id,
                                                          v=API_VERSION, offset=i * 1000,
                                                          **kwargs)
                sleep(self.timeout)
            post_reposts = merge_arrays(post_reposts)
        return post_reposts

    def get_users_birthday_dates(self, _users_ids, days_to_bday=None):
        """
        Если передаем без параметра days_to_bday то получаем словарь пользователей ид:дата др
        Если с параметром то передает словарь пользователей у которых до др меньше days_to_bday
        """
        response = self._api.users.get(user_ids=_users_ids, v=API_VERSION, fields="bdate")
        result = {user.get("id"): user.get("bdate") for user in response}

        if days_to_bday:
            bdates_results = dict()
            today = datetime.date.today()
            for user in result.items():
                bday_date = user[1].split(".")
                b_day, b_month = map(int, bday_date)
                user_bday_date = datetime.date(today.year, b_month, b_day)
                if (user_bday_date - today).days <= days_to_bday and b_month == today.month:
                    bdates_results["id"] = user[0]
                    bdates_results["bdate"] = user[1]
            return bdates_results
        return result
    # TODO: Аналитика, Аудитория постов, Комментарии, Аудитория фотоальбомов, Активная аудитория, Поиск постов


if __name__ == '__main__':
    x = VkTarget()
    print(x.search_users("Pasha"))
    print(x.get_users_birthday_dates(_users_ids=(80748910, 11), days_to_bday=30))
