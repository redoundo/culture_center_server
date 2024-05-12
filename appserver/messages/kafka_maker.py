from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
import dotenv
import os
import requests
import datetime
dotenv.load_dotenv()


class CustomKafkaProducer:

    producer: KafkaProducer
    topic: str

    def __init__(self, topic: str):
        producer = KafkaProducer(
            acks=0,  # 메시지 전송 완료에 대한 체크
            compression_type='gzip',  # 메시지 전달할 때 압축(None, gzip, snappy, lz4 등)
            bootstrap_servers=['localhost:9092'],  # 전달하고자 하는 카프카 브로커의 주소 리스트
            value_serializer=lambda x: x.encode('utf-8')  # 메시지의 값 직렬화
        )
        self.producer = producer
        self.topic = topic
        return

    def produce(self, message: str):
        self.producer.send(topic=self.topic, value=message)
        self.producer.flush()
        return


class CustomKafkaConsumer:
    consumer: KafkaConsumer
    topic: str

    def __init__(self, topic: str):
        consumer = KafkaConsumer(
            topic,  # 토픽명
            bootstrap_servers=['localhost:9092'],  # 카프카 브로커 주소 리스트
            auto_offset_reset='earliest',  # 오프셋 위치(earliest:가장 처음, latest: 가장 최근)
            enable_auto_commit=True,  # 오프셋 자동 커밋 여부
            group_id=f"{topic}-group",  # 컨슈머 그룹 식별자
            value_deserializer=lambda x: x.decode('utf-8'),  # 메시지의 값 역직렬화
            consumer_timeout_ms=1000  # 데이터를 기다리는 최대 시간
        )
        self.topic = topic
        self.consumer = consumer
        return

    def send(self):
        for message in self.consumer:
            print(message)
        return

# class CustomKafkaConsumer:
#
#     consumer: KafkaConsumer
#     topic: str
#
#     kakaoTalkUrl: str = os.getenv("KAKAO_TALK_URL")
#     refreshTokenUrl: str = os.getenv("KAKAO_TOKEN_REFRESH_URL")
#     clientId: str = os.getenv("KAKAO_REST_API_KEY")
#     authorityUrl: str = os.getenv("MY_KAKAO_TALK_ALLOW_AUTHORITY")
#     redirectUri: str = os.getenv("KAKAO_REDIRECT_URI")
#     sendFailMessagePath: str = os.getenv("SENT_FAILED_MESSAGE_PATH")
#     authCode: str = os.getenv("KAKAO_AUTHORITY_CODE")
#
#     accessToken: str
#     refreshToken: str
#
#     def __init__(self, topic: str):
#         self._reissue_tokens()
#
#         consumer = KafkaConsumer(
#             topic,  # 토픽명
#             bootstrap_servers=['localhost:9092'],  # 카프카 브로커 주소 리스트
#             auto_offset_reset='earliest',  # 오프셋 위치(earliest:가장 처음, latest: 가장 최근)
#             enable_auto_commit=True,  # 오프셋 자동 커밋 여부
#             group_id=f"{topic}-group",  # 컨슈머 그룹 식별자
#             value_deserializer=lambda x: x.decode('utf-8'),  # 메시지의 값 역직렬화
#             consumer_timeout_ms=1000  # 데이터를 기다리는 최대 시간
#         )
#         self.topic = topic
#         self.consumer = consumer
#         return
#
#     def consume(self):
#         for message in self.consumer:
#             self._message_request(message)
#         return
#
#     def _token_request_template(self, position: str, **kwargs):
#         """
#         access_token 과 refresh_token 을 다시 발급 받아야 할 때 사용. code 는 rest api 가 아니기 때문에 내가 직접 넣어줘야 함.
#         :param kwargs: 추가적으로 설정할 내용
#         :return: response.json() | None
#         """
#         data: dict = {
#             "grant_type": "authorization_code",
#             "client_id": self.clientId
#         }
#         if kwargs is not None:
#             data.update(kwargs)
#         response = requests.post(self.refreshTokenUrl, data=data)
#         if response.status_code != 200:
#             self._send_fail(position=position, response=response.json(), data=data)  # 실패 하면 실패한 내용을 json 에 저장.
#             return None
#         return response.json()
#
#     def _send_fail(self, position: str, **kwargs):
#         """
#         메세지 를 보내는 데 실패했을 경우, 관련 내용을 넣어 send failed.json 에 저장한다.
#         :param position: 실패한 위치
#         :param kwargs: 당시 내용
#         :return:
#         """
#         reason: dict = {
#             "position": position,
#             "failed_time": str(datetime.datetime.now())
#         }
#         if kwargs is not None:
#             reason.update(kwargs)
#         with open(self.sendFailMessagePath, "a", encoding="utf-8-sig") as J:
#             json.dump(reason, J, indent=4, ensure_ascii=False)
#         return
#
#     def _reissue_tokens(self):
#         """
#         access token 과 refresh token 을 가져 온다.
#         만일 token 들을 가져오는 데 필요한 code 가 유효 하지 않다면 -1 을 put 한다.
#         :return:
#         """
#         tokens: dict = self._token_request_template(redirect_uri=self.redirectUri, code=self.authCode,
#                                                     position="reissue_token")
#         if tokens is not None:
#             if "access_token" in list(tokens.keys()):
#                 self.accessToken = tokens['access_token']
#                 self.refreshToken = tokens['refresh_token']
#         else:
#             tried_agin = self._token_request_template(redirect_uri=self.redirectUri, code=self.authCode,
#                                                       position="reissue_token_tried_agin")
#             if tried_agin is None:
#                 print(f"access token 을 받아 오는 것에 실패 했습니다. code 값은 {self.authCode} 이며 응답 내용은 이렇습니다. {tokens}")
#         return
#
#     def _reissue_access_token(self):
#         """
#         refresh token 이 존재 한다고 가정. refresh token 울 이용해 access_token 을 가져 온다.
#         refresh token 이 유효하지 않다면 에러.
#         :return:
#         """
#         response: dict = self._token_request_template(refresh_token=self.refreshToken, position="reissue_access_token")
#         if response is None:  # 만약 refresh token 으로 access token 을 가져오지 못한다면 한번만 더 해본다.
#             tried_agin = self._token_request_template(refresh_token=self.refreshToken,
#                                                       position="reissue_access_token_tried_agin")
#             if tried_agin is None:
#                 return
#             else:
#                 response = tried_agin
#
#         listed: list = list(response.keys())
#         if "access_token" not in listed:
#             print(f"can't get access token response are {response}")
#             return
#
#         self.accessToken = response.get("access_token")
#         if "refresh_token" in listed:
#             self.refreshToken = response.get("refresh_token")
#         return
#
#     def _talk_message_request(self, text: str, position: str, **kwargs):
#         """
#         카카오 톡으로 메세지를 전한다.
#         :param text: 알림 내용
#         :param kwargs: 추가적으로 설정할 내용
#         :return: dict = response.json() | None
#         """
#         if self.refreshToken is None:
#             self._reissue_tokens()
#
#         if self.accessToken is None:
#             self._reissue_access_token()
#
#         header: dict = {
#             "Authorization": f"Bearer {self.accessToken}"
#         }
#         body: dict = {
#             "object_type": "text",
#             "text": text,
#             "link": {
#                 "web_url": self.authorityUrl
#             }
#         }
#         if kwargs is not None:
#             body.update(kwargs)
#         template: dict = {"template_object": json.dumps(body, ensure_ascii=False)}
#
#         response = requests.post(self.kakaoTalkUrl, headers=header, data=template)
#         if response.status_code != 200:
#             self._send_fail(position=position, header=header, template=template, response=response.json())
#             return None
#         return response.json()
#
#     def _message_request(self, text: str):
#         """
#         카톡 메세지를 보낸다. 최대 2번 실행 한다.
#         TODO: 2번 이상 실패 하면 token 에 문제가 있다는 의미이다. 그 뒤에도 계속 실패할 텐데 이에 대한 대책이 존재하지 않는다.
#         :param text: 메시지 내용
#         :return:
#         """
#         print(text)
#         response = self._talk_message_request(text=text, position="message_request")
#         if response is None:
#             self._reissue_access_token()
#             tried_agin = self._talk_message_request(text=text, position="message_request_tried_agin")
#             if tried_agin is None:
#                 return
#         else:
#             pass
#         return

