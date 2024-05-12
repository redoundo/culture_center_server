import firebase_admin
from typing import Sequence
from .db.selectdb import need_message_in_fmc_receivers
from .db.tablemodels import Users, Lectures
from firebase_admin import messaging

firebase_app = firebase_admin.initialize_app()


def send_fcm_message(new_user: Users = None):
    """
    fcm 알림을 받는 사용자가 있고 접수한 강좌 내역이 존재 함다면 해당 사용자에게 fcm 푸시를 보낸다.
    :return:
    """
    if new_user is None:
        message_receivers: dict[Users, Sequence[Lectures]] = need_message_in_fmc_receivers()
        receivers: list[Users] = list(message_receivers.keys())
    else:
        message_receivers: dict[Users, Sequence[Lectures]] = need_message_in_fmc_receivers(new_user=new_user)
        receivers: list[Users] = [new_user]

    if len(receivers) < 1:
        return
    for receiver in receivers:
        messages: list[messaging.Message] = message_template(receiver, message_receivers.get(receiver))
        if len(messages) > 1:
            response = messaging.send_each(messages=messages)
            print(f"fcm message are sent! {response.success_count}")
        else:
            messaging.send(message=messages[0])
            print(f"fcm message is sent!")
    return


def message_template(user: Users, lectures: Sequence[Lectures]) -> list[messaging.Message]:
    """
    message 내용 설정.
    :param user: 사용자 정보
    :param lectures: 사용자가 신청한 내용중 오늘 강의를 하는 강좌의 내용들.
    :return:
    """
    messages: list[messaging.Message] = []
    if len(lectures) > 1:
        for lecture in lectures:
            title: str = f"{user.nickname} 님! 오늘 {lecture.title} 에 가는 날이에요!"
            body: str = f"{lecture.lectureSupplies} 을 챙겨서 {lecture.branch} 에 가야 해요! 기억이 안난다면 {lecture.url} 을 보세요!"
            messages.append(
                messaging.Message(notification=messaging.Notification(title=title, body=body, image=lecture.src),
                                  token=user.fcmToken))
    else:
        title: str = f"{user.nickname} 님! 오늘 {lectures[0].title} 에 가는 날이에요!"
        body: str = f"{lectures[0].lectureSupplies} 을 챙겨서 {lectures[0].branch} 에 가야 해요! 기억이 안난다면 {lectures[0].url} 을 보세요!"
        messages.append(
            messaging.Message(notification=messaging.Notification(title=title, body=body, image=lectures[0].src),
                              token=user.fcmToken))
    return messages




