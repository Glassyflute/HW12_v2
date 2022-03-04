from flask import Blueprint, render_template, request
from functions import PostsManager
import logging
POST_PATH = "posts.json"

# создаем блюпринт и называем его
main_blueprint = Blueprint("main_blueprint", __name__, template_folder="templates")
logging.basicConfig(filename="basic.log", level=logging.INFO)


@main_blueprint.route("/")
def page_index():
    logging.info("Запрошена главная страница")
    return render_template("index.html")


# страница с результатами поиска по части слова, отображает список публикаций
@main_blueprint.route("/list")
def page_search():
    s = request.args.get("s")
    post_manager = PostsManager(POST_PATH)
    logging.info("Поиск выполняется")

    search_result = post_manager.search_posts_by_substring(s)

    if not search_result:
        return "Публикации по вашему выбору не найдено"

    return render_template("post_list.html", search_result=search_result, s=s)
