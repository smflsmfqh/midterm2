import os
import cv2
import pathlib
import requests
from datetime import datetime

class ChangeDetection:
    HOST = 'http://127.0.0.1:8000'
    username = 'haneullee'
    password = 'jk970901'
    token = ''
    title = ''
    text = ''

    def __init__(self, names):
        # 이전 결과를 저장하는 리스트 초기화
        self.result_prev = [0 for _ in range(len(names))]
        
        # 토큰을 요청하여 저장
        res = requests.post(
            f"{self.HOST}/api/token/",
            data={'username': self.username, 'password': self.password}
        )
        if res.status_code ==200: #로그인 성공
            self.token = res.json().get('access')
            if self.token is None:
                print("Token is None. Check the response: ", res.json())
        else: #로그인 실패
            print(f"Failed to obtain token. Status code: {res.status_code}, Response: {res.text}")
            raise ValueError("Failed to obtain JWT token")
        print("Token obtained: ", self.token)
        #res.raise_for_status()  # 요청에 실패하면 예외 발생
        #self.token = res.json().get('token')  # 토큰 저장
        #print(self.token)  # 토큰 출력
    
    def add(self, names, detected_current, save_dir, image):
        self.title = ''
        self.text = ''
        change_flag = 0  # 변화 감지 플래그
        i = 0

        # 객체 출현 변화 확인
        while i < len(self.result_prev):
            # 이전 상태가 '0'이고 현재 상태가 '1'일 때 변화를 감지
            if self.result_prev[i] == 0 and detected_current[i] == 1:
                change_flag = 1
                self.title = names[i]
                self.text += names[i] + ", "
            i += 1

        # 현재 객체 검출 상태를 이전 상태로 저장
        self.result_prev = detected_current[:]

        # 변화가 감지되면 서버에 이미지 전송
        if change_flag == 1:
            self.send(save_dir, image)

    def send(self, save_dir, image):
        # 현재 시각 정보 가져오기
        now = datetime.now()
        today = datetime.now()

        # 이미지 저장 경로 생성
        save_path = pathlib.Path(os.getcwd()) / save_dir / 'detected' / str(today.year) / str(today.month) / str(today.day)
        save_path.mkdir(parents=True, exist_ok=True)

        # 이미지 파일명 설정
        full_path = save_path / '{0}-{1}-{2}-{3}.jpg'.format(today.hour, today.minute, today.second, today.microsecond)

        # 이미지 리사이즈 및 저장
        dst = cv2.resize(image, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        cv2.imwrite(str(full_path), dst)

        # 인증 헤더 생성
        headers = {
            'Authorization': 'JWT ' + self.token,
            'Accept': 'application/json'
        }

        # POST 요청에 보낼 데이터 구성
        data = {
            'author': 1,
            'title': self.title,
            'text': self.text,
            'created_date': now.isoformat(),
            'published_date': now.isoformat()

        }
        print("Sending data:", data)  # 데이터 확인
        file = {'image': open(full_path, 'rb')}

        # 서버에 POST 요청 전송
        res = requests.post(f"{self.HOST}/api_root/Post/", data=data, files=file, headers=headers)
        print("Response status code:", res.status_code)
        print("Response content:", res.content) # 응답 출력

        # 파일 닫기
        file['image'].close()