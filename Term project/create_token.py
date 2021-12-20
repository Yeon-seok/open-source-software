#카카오톡으로 메시지를 보내기 위해 카카오 API를 사용하기 위한 사용자 토큰을 발급 받는 코드
#중요 정보는 삭제

import requests

url = 'https://kauth.kakao.com/oauth/token'
rest_api_key =  '[rest_api_key]'
redirect_uri = 'https://example.com/oauth'
authorize_code = '[authorize_code]'

data = {
    'grant_type':'refresh_token',
    'client_id':rest_api_key,
    "refresh_token": "[refresh_token]"
    # 'redirect_uri':redirect_uri,
    # 'code': authorize_code,
    }

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)


import json
with open("kakao_code.json","w") as fp:
    json.dump(tokens, fp)

