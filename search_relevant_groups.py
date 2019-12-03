from time import sleep
import json
from typing import Iterable

import vk
from credentials import API_VERSION, ACCESS_TOKEN


def merge_arrays(array):
    result = list()
    for el in array:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            result.extend(merge_arrays(el))
        else:
            result.append(el)
    return result


class VkTarget:
    def __init__(self, filename="data", access_token=ACCESS_TOKEN):
        self.__vk_session = vk.Session(access_token=access_token)
        self._api = vk.API(self.__vk_session)
        self.output_filename = filename

    def get_members(self, _group_id: int, timeout: int = 1) -> list:
        first = self._api.groups.getMembers(group_id=_group_id, v=API_VERSION)
        data = first.get("items")
        count = first.get("count") // 1000
        for i in range(1, count + 1):
            data += self._api.groups.getMembers(group_id=_group_id, v=API_VERSION,
                                                offset=i * 1000).get(
                "items")
            sleep(timeout)
        data = merge_arrays(data)
        return data

    def save_data(self, data: list or dict):
        if isinstance(data, dict):
            file_extension = "json"
        else:
            file_extension = "txt"
        full_filename = ".".join((self.output_filename, file_extension))
        with open(full_filename, "w") as file:
            if isinstance(data, dict):
                json.dump(data, file, indent=4)
            else:
                for item in data:
                    file.write("vk.com/id" + str(item) + "\n")

    def get_overlapping_people(self, groups_id: list or tuple):
        all_people_in_all_groups = list()

        for group_id in groups_id:
            all_people_in_all_groups.append(self.get_members(group_id))
        overlapping_people = list(set(merge_arrays(all_people_in_all_groups)))
        self.save_data(overlapping_people)
        return overlapping_people

    # TODO: add parametrs to query
    def search_groups(self, query, country_id=None, city_id=None, sort=None):
        data = dict()
        result_of_search = self._api.groups.search(q=query, v=API_VERSION, count=1000, country_id=1)
        data[query] = result_of_search.get("items")
        self.save_data(data)
        return data


if __name__ == '__main__':
    x = VkTarget()
    x.search_groups("Овечка")
