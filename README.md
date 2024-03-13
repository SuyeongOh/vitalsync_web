# vitalsync_web

## 사용 명령
  - `cd vitalsync_web`
  - `uvicorn server.vital.service.VitalService:vitalService --host 0.0.0.0 --port 1024 --reload`
  - `uvicorn server.vital.service.UserService:userService --host 0.0.0.0 --port 1025 --reload`

- android에서 baseurl 세팅 후 사용

## 주의사항
1. 사용 운영체제에서 방화벽 예외 사항으로 등록(1024 포트)
2. https주소가아닌 http 주소(SSL 인증서 및 키가 없음)
3. 해당 git에 push를 해도 좋고, 이것을 rppg-remotebiosensing에 merging 하여도 무방.

## 사용 라이브러리
  - fastapi
  - pydantic
  - uvicorn
  - typing
  - numpy
  - matplotlib
  - scipy