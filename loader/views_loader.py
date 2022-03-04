from flask import Blueprint, render_template, request
from exceptions import PictureTypeError
from functions import PostsManager
import logging
POST_PATH = "posts.json"

# создаем блюпринт и называем его
loader_blueprint = Blueprint("loader_blueprint", __name__, template_folder="templates")
logging.basicConfig(filename="basic.log", level=logging.INFO)

# создаем вьюшки из блюпринт на разные страницы


# страница, куда можно прикреплять файл рисунка с текстовым полем
@loader_blueprint.route("/post")
def page_post_main():
    logging.info("Запрошена страница для добавления поста")
    return render_template("post_form.html")


# как выглядит страница нового поста после добавления самого поста
@loader_blueprint.route("/post", methods=["POST"])
def page_post_upload():
    logging.info("Данные поста вносятся пользователем")
    picture = request.files.get("picture")
    content = request.form.get("content")
    picture.save(f"./uploads/images/{picture.filename}")

    if not picture or not content:
        logging.exception("Ошибка загрузки: файл или картинка не загружены")
        return "Ошибка загрузки"
    # return f"Загружена картинка {picture.filename}, содержимое поста {content}"
    # `exception`    если    ошибка    при    загрузке    файла

    try:
        pic_full_name = picture.filename
        if pic_full_name.split(".")[-1] not in ["jpeg", "jpg", "png"]:
            raise PictureTypeError("Загруженный файл не имеет расширение jpeg, png")
    except PictureTypeError:
        logging.info("Загруженный файл не картинка")
        return "Загруженный файл не имеет расширение jpeg или png"

    picture_path = f"/uploads/images/{picture.filename}"

    new_post = {"pic": picture_path, "content": content}
    post_manager = PostsManager(POST_PATH)
    new_posts_list = post_manager.add_post_to_json_list(new_post)

    return render_template("post_uploaded.html",
                           content=content, picture_path=picture_path)
