import datetime
import json

import requests
import dotenv
import os
from queue import Queue
dotenv.load_dotenv()


class DiscordMessenger:

    webhookUrl: str = os.getenv("DISCORD_WEBHOOK_URL")
    messageQueue: Queue

    def __init__(self, message_queue: Queue):
        """
        discord 알림 전달 해주는 messanger
        :param message_queue: message 가 담긴 queue
        """
        self.messageQueue = message_queue
        return

    def send_message(self):
        """
        message queue 에 있는 메세지 내용을 discord webhook url 로 보낸다.
        :return:
        """
        while True:
            data = self.messageQueue.get()
            if data is None:
                break
            else:
                self._message_template(data)
        return

    def _message_template(self, text: str):
        """
        메세지를 template 를 설정 한다. 알림 전송에 실패 하면 sendfailed.json 에 저장 한다.
        :param text: 전송할 message 내용
        :return:
        """
        template: dict = {
            "content": text + "\n" + datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        }
        response = requests.post(self.webhookUrl, template)

        if response.status_code > 299:  # 문제가 발생 하면
            template["content"] = response.json() + "\n" + text
            template["error_time"] = datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
            with open("sendfailed.json", "a") as j:
                json.dump(template, j)
        return

