sampletoken.json을 복사한 뒤 token.json으로 이름을 바꿔, 자신의 네이버 API client_id와 client_secret, 디스코드 봇의 토큰을 입력하여주시기 바랍니다.
# discordnews
2024년 2학기 자료구조 수행평가를 위해 제작하게 된 프로젝트입니다.
총 제작기간: 1시간 20분

![image](https://github.com/user-attachments/assets/9e024fb5-a545-449f-a910-bcf476cdaa33)

자료구조인 '트리'에서 영감을 받아 제작하게 된 해야할 일을 정리해주는 디스코드 봇입니다.

## 작동 원리
![image](https://github.com/user-attachments/assets/3f3ba45f-fc20-425b-bb24-762acc9621bb)

프로젝트와 할 일을 입력받는다.

![image](https://github.com/user-attachments/assets/3f3b1f59-8bf3-4754-a96e-39f3bcfcf651)

같은 프로젝트에 또다른 할 일을 추가할 수 있다.

![image](https://github.com/user-attachments/assets/b0130c36-a808-4125-aa4f-46666da72240)

또다른 프로젝트에 새로운 할 일을 추가할 수 있다.

![image](https://github.com/user-attachments/assets/127e58b8-c036-4737-a4f0-c791336bae80)

만약 한 프로젝트에 한 일이 전부 완료된 경우, 해당 프로젝트는 삭제된다.

## 주 사용 기술
- `discord.py`: 디스코드 봇을 만들기 위한 라이브러리
- `json`: json의 딕셔너리 구조를 응용한 트리 구조

Thanks to. 마셜 골드스미스 - 일 잘하는 당신이 성공을 못하는 20가지 비밀
