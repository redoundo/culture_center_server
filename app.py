import requests
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from appserver.error.customerror import global_error_handler
from appserver.db.selectdb import *
from appserver.db.changedb import *
from appserver.sendfcmmessage import *
from utils.util import validate_string
from appserver.error.customerror import CustomException
from appserver.Jwt.jwtprovider import decode_jwt, encode_jwt
from apscheduler.schedulers.background import BackgroundScheduler
import hashlib
import os


os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
# 사용자 정의 에러가 raise 되면 global_error_handler 가 잡아서 해당 에러 내용을 response 에 넣는다.
flask_app = global_error_handler(Flask(__name__))
CORS(flask_app, origins=["http://localhost:3000"])

# 매일 아침 7시에 fcm message 를 보내는 scheduler.
# background_scheduler: BackgroundScheduler = BackgroundScheduler()
#
#
# @background_scheduler.scheduled_job(trigger="cron", hour=7)
# def send_message():
#     send_fcm_message()
#     print("fcm_message are sent!! current time is ")
#     return
#
#
# background_scheduler.start()
#
#
# @flask_app.teardown_appcontext
# def shutdown_scheduler():
#     """
#     flask app 이 끝나면 background scheduler 도 닫는다.
#     :return:
#     """
#     background_scheduler.shutdown()
#     return


@flask_app.route('/api/', methods=['GET'])
@flask_app.route('/api/lecture', methods=['GET'])
def find_all_lectures_by_search_options():
    """
    검색 조건 설정에 필요한 내용과 전달된 조건으로 찾은 강좌를 반환 한다.
    :return:
    """
    params = request.args
    token = request.headers.get("Authorization")
    print(params.get("categoryId"))
    lectures: list[dict] = (
        select_all_lectures_by_search_options(page=params.get("page"), category=params.get('categoryId'),
                                              centerType=params.get('type'), keyword=params.get('keyword'),
                                              target=params.get('targetId'))
    )
    if token != None:
        user_id = decode_jwt(token).get("userId")
        liked_applied: dict = {}
        liked_applied["liked"] = select_all_liked_lectures_by_user_id(user_id)
        liked_applied["applied"]=select_all_applied_lectures_by_user_id(user_id)
    else:
        liked_applied = None
    targets: list[dict] = select_all_targets()
    categories: list[dict] = select_all_categories()
    center_types: Sequence[str] = select_all_center_type()
    return jsonify({
        'lectures': lectures, 'targets': targets, 'categories': categories, 'type': center_types, "liked_applied": liked_applied
    })


@flask_app.route('/api/lecture/detail', methods=["GET"])
def find_lecture_by_lecture_id():
    """
    강좌 아이디로 강좌 내용을 찾아 반환.
    :return:
    """
    lecture_id = request.args.get('lectureId')

    if validate_string(lecture_id):
        lecture: Lectures = select_lecture_by_lecture_id(int(lecture_id))
        return jsonify({
            'lecture': lecture
        })

    return jsonify({'lecture': None})


@flask_app.route('/api/lecture/detail/liked', methods=["GET"])
@flask_app.route('/api/lecture/liked', methods=["GET"])
def set_liked_this_lecture_by_lecture_id():
    """
    강좌 저장.
    :return:
    """
    lecture_id = request.args.get('lectureId')
    token = request.headers.get("Authorization")

    if not validate_string(token):
        raise CustomException.NEED_LOGIN_EXCEPTION

    if validate_string(lecture_id):
        user_id = decode_jwt(token).get("userId")  # 문제가 있으면 예외가 발생해 진행되지 않음.
        insert_liked_by_user_id(lecture_id=int(lecture_id), user_id=int(user_id))
    return jsonify({'status': 200})


@flask_app.route("/api/lecture/detail/applied", methods=["GET"])
@flask_app.route('/api/lecture/applied', methods=["GET"])
def set_applied_this_lecture_by_lecture_id():
    """
    토큰이 없어도 아무런 alert 발생 하지 않고 있으면 해당 사용자 아이디로 지원한 강좌 저장
    :return:
    """
    lecture_id = request.args.get("lectureId")
    token = request.headers.get("Authorization")
    print(lecture_id)
    if not validate_string(token):
        return
    if not validate_string(lecture_id):
        return

    user_id = decode_jwt(token).get("userId")
    insert_applied_by_user_id(lecture_id=int(lecture_id), user_id=int(user_id))
    return jsonify({'status': 200})


@flask_app.route("/api/myPage/user", methods=['POST'])
def find_user_by_user_id():
    """
    jwt 토큰을 통해 사용자 아이디를 가져온 뒤, 해당 아이디로 저장된 내용들을 전부 가져온다.
    :return:
    """
    token = request.get_json()
    print(token)
    if not validate_string(token["Authorization"]):
        raise CustomException.NEED_LOGIN_EXCEPTION

    user_id = decode_jwt(token["Authorization"]).get("userId")
    if user_id is None:
        raise CustomException.INVALID_JWT_TOKEN_EXCEPTION

    result = select_users_info_by_user_id(int(user_id))
    if result is None:
        return jsonify({"user": None})

    return jsonify({"user": result})


@flask_app.route("/api/myPage/<applied_liked>/delete", methods=['GET'])
def my_page_delete_liked_or_applied_by_lecture_id(applied_liked: str):
    """
    저장 했거나 지원 했던 강좌 삭제
    :param applied_liked: applied | liked
    :return:
    """
    token = request.headers.get("Authorization")
    print(token)
    if not validate_string(token):
        raise CustomException.NEED_LOGIN_EXCEPTION
    user_id = decode_jwt(token).get("userId")
    if user_id is None:
        raise CustomException.INVALID_JWT_TOKEN_EXCEPTION
    lecture_id = request.args.get("lectureId")
    print(lecture_id)
    if not validate_string(lecture_id):
        raise CustomException.NO_REQUIRED_ARGUMENTS_EXCEPTION

    if applied_liked == "liked":
        delete_liked_by_lecture_id_user_id(lecture_id=int(lecture_id), user_id=int(user_id))
    else:
        delete_applied_by_lecture_id_user_id(lecture_id=int(lecture_id), user_id=int(user_id))
    return jsonify({"status": 200})


@flask_app.route('/api/myPage/edit', methods=['POST'])
def find_user_info_for_edit_info():
    """
    정보 변경을 위해 토큰에서 사용자 아이디를 받아온 뒤 사용자 정보를 가져온다.
    :return: 사용자 정보
    """
    token = request.get_json()
    print(token)
    if not validate_string(token["Authorization"]):
        raise CustomException.NEED_LOGIN_EXCEPTION
    user_id = decode_jwt(token["Authorization"]).get("userId")
    if user_id is None:
        raise CustomException.INVALID_JWT_TOKEN_EXCEPTION
    user: Users = select_user_by_user_id(int(user_id))
    return jsonify({"user": user})


@flask_app.route("/api/myPage/edit/update", methods=["PUT", "POST"])
def update_user_info():
    """
    사용자 정보 업데이트
    :return:
    """
    token = request.get_json()
    print(token)
    if not validate_string(token["Authorization"]):
        raise CustomException.NEED_LOGIN_EXCEPTION

    user_id = decode_jwt(token["Authorization"]).get("userId")
    if user_id is None:
        raise CustomException.INVALID_JWT_TOKEN_EXCEPTION

    changed_info = request.get_json()
    if changed_info["nickname"] is None:
        return
    update_user_by_user_id(int(user_id), changed_info["nickname"])
    return jsonify({"status": 200})


@flask_app.route("/api/myPage/withdraw", methods=["POST"])
def let_withdraw_user_by_user_id():
    """
    회원 탈퇴
    :return:
    """
    token = request.get_json()
    print(token)
    if not validate_string(token["Authorization"]):
        raise CustomException.NEED_LOGIN_EXCEPTION
    user_id = decode_jwt(token["Authorization"]).get("userId")
    if user_id is None:
        raise CustomException.INVALID_JWT_TOKEN_EXCEPTION
    withdraw_user_by_user_id(int(user_id))
    return jsonify({"status": 200})


@flask_app.route("/api/<sns>/login", methods=["POST"])
def sns_access_token(sns: str):
    query = request.get_json()
    print(query)

    if sns == "naver":
        publish_url: str = "https://nid.naver.com/oauth2.0/token"
        response = requests.get(publish_url + "?" + query["query"])
    else:
        publish_url: str = "https://oauth2.googleapis.com/token"
        response = requests.post(publish_url, query)

    res = response.json()
    print(res)
    return jsonify(res)

@flask_app.route("/api/naver/user_info", methods=["POST"])
def naver_get_user_info():
    url: str = "https://openapi.naver.com/v1/nid/me"
    naver_token = request.get_json()
    print(naver_token)
    response = requests.get(url=url, headers={"Authorization": "Bearer " + naver_token["Authorization"]})
    res = response.json()
    print(res)
    return jsonify(res)


@flask_app.route("/api/signin/<sns>/publish_jwt", methods=["POST"])
def sign_in_publish_jwt(sns: str):
    user_info = request.get_json()
    print(user_info)
    print(sns)
    if user_info["email"] is None or user_info["id"] is None:
        raise CustomException.FAILED_AUTHORIZED_EXCEPTION

    exist: int = check_user_already_exists(user_info["email"])
    if exist > 0:
        user: Users = select_user_by_email(user_info["email"])
        print(user.userId)
        print(encode_jwt(user.userId))
        return jsonify({"status": 200, "Authentication": encode_jwt(user.userId)})

    if sns == "CultureCenter":
        now: datetime = datetime.now()
        provider_id: str = (sns.upper() + "_" + str(now.year) + str(now.month) + str(now.day) + "_"
                            + str(today_sign_in_user_mount() + 1))

        if user_info["nickname"] is None:
            nickname: str = provider_id
        else:
            nickname: str = user_info["nickname"]

        encrypt = hashlib.sha256()
        encrypt.update(user_info["password"].encode('utf-8'))
        sign_in_user(user_info["email"], encrypt.hexdigest(), nickname, sns, provider_id)

    else:
        provider_id: str = sns.upper() + "_" + user_info["id"]
        nickname: str = user_info["email"]

        print(nickname)
        sign_in_user(user_info["email"], provider_id, nickname, sns, provider_id)

    new_user: Users = select_user_by_email(user_info["email"])
    print(new_user.userId)
    return jsonify({"status": 200, "Authentication": encode_jwt(new_user.userId)})


@flask_app.route("/api/login/<sns>/publish_jwt", methods=["POST"])
def login_publish_jwt(sns: str):
    user_info = request.get_json()
    if user_info["email"] is None or user_info["id"] is None:
        raise CustomException.FAILED_AUTHORIZED_EXCEPTION

    user: Users = select_user_by_email(user_info["email"])
    if user is None:
        return jsonify({"status": 404, "data": user_info})

    if sns == "CultureCenters":
        encrypt = hashlib.sha256()
        encrypt.update(user_info["password"].encode('utf-8'))
        if user.password != encrypt.hexdigest():
            return jsonify({"status": 401})

    jwt_token: str = encode_jwt(user.userId)
    return jsonify({"status": 200, "Authentication": jwt_token})


@flask_app.route("/api/auth/isValid", methods=["POST"])
def is_logged_in():
    token = request.get_json()
    decoded = decode_jwt(token["token"])
    print(decoded)
    user: Users = select_user_by_user_id(decoded["userId"])
    if user.userId != None:
        return jsonify({"status": 200, "userId": user.userId})
    else:
        return jsonify({"status": 400, "userId": -1})

@flask_app.route("/api/signin/check_nickname_is_unique", methods=["POST"])
def nickname_uniqueness():
    """
    닉네입 사용 가능 여부 확인
    :return:
    """
    need_check = request.get_json()
    if need_check["nickname"] is None:
        raise CustomException.NO_REQUIRED_ARGUMENTS_EXCEPTION

    exist: int = check_user_nickname_is_unique(need_check["nickname"])
    if exist > 0:
        return jsonify({"status": 226, "canUse": False})
    return jsonify({"status": 200, "canUse": True})


@flask_app.route("/api/register_fcm_receiver", methods=["POST"])
def registering_fcm_receiver():
    token = request.headers.get("Authorization")
    if not validate_string(token):
        raise CustomException.NEED_LOGIN_EXCEPTION

    user_id = decode_jwt(token).get("userId")
    if user_id is None:
        raise CustomException.INVALID_JWT_TOKEN_EXCEPTION

    registered_token = request.get_json()
    if registered_token["vapidToken"] is None:
        return jsonify({"status": 400, "registered": False})  # register token 이 없으면 저장할 수 없으므로, 에러 반환.

    register_fcm_receiver(user_id, registered_token["vapidToken"])
    return jsonify({"status": 200, "registered": True})


@flask_app.route("/api/new_data_json", methods=["GET"])
def download_new_data():
    file_path: str = "/flask-server/sample/train_sample.json"
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_file(path_or_file=file_path, as_attachment=True, download_name="train_sample.json")
    else:
        return jsonify({"status": 404, "message": "no such file."})

if __name__ == "__main__":
    print("how are you??")
    flask_app.run(port=8079)
