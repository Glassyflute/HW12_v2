import json
from pprint import pprint as pp
from exceptions import DataWriteError
from json import JSONDecodeError


class PostsManager:
    """
    Класс для обработки постов. Загружает для чтения данные из json по ссылке
     (path), ищет посты по части слова, перезаписывает данные в json
    """
    def __init__(self, path):
        self.path = path

    def load_posts_from_json(self):
        """
        Загружает для чтения данные из json по ссылке (path)
        :return:
        """
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                posts_data = json.load(file)
            return posts_data
        except FileNotFoundError:
            print("Файл не найден")
        except JSONDecodeError:
            print("Ошибка в чтении файла json")

    def search_posts_by_substring(self, substring):
        """
        ищет посты по части слова
        :param substring:
        :return:
        """
        substring_lower = substring.lower()
        posts_selected = []

        posts_data = self.load_posts_from_json()
        for post in posts_data:
            search_text = post["content"].lower()
            if substring_lower in search_text:
                posts_selected.append(post)
        return posts_selected

    def overwrite_json_data(self, posts_data):
        """
        перезаписывает данные в json
        :param posts_data:
        :return:
        """
        try:
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(posts_data, file, ensure_ascii=False)
        except FileNotFoundError:
            print("Файл не найден")

    def add_post_to_json_list(self, new_post):
        """
        добавляет новый пост в файл json со списком постов в формате словарей
        :param new_post:
        :return:
        """
        posts_data = self.load_posts_from_json()
        try:
            posts_data.append(new_post)
            self.overwrite_json_data(posts_data)
        except DataWriteError:
            print("Данные не были перезаписаны в файл json")

