#발급 받은 토큰을 이용해 카카오 API로 나에게 메시지 보내기를 클래스로 구현

import requests
import json

with open("kakao_code.json","r") as fp:
    tokens = json.load(fp)

class send_message :
    def __init__(self, seat_number) :
        self.url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        self.headers = {
                        "Authorization" : "Bearer " + tokens["access_token"]
                        }
        self.data = {
                "template_object": json.dumps({
                "object_type":"text",
                "text":f"관리자님, 방역수칙을 위반한 사용자가 존재합니다. 조치를 취해주세요! 좌석 번호는 {seat_number}번 입니다.",
                "link":{
                    "web_url":"www.naver.com"
                    }
                    })
                    }
    def requests(self) :
        requests.post(self.url, headers=self.headers, data=self.data)


