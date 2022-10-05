# Numanguan - AI기반 관상 키워드, 운명의 단짝 매칭 서비스

## 1. 프로젝트 설명

### 프로젝트명
```
AI 기반 관상 키워드, 운명의 단짝 매칭 서비스
```
### 프로젝트 소개
```
사용자의 얼굴 이미지를 입력받아 닮은 연예인 얼굴과 관상 키워드를 출력합니다.

사용자의 생년월일 정보를 입력받아 사주팔자 정보를 통해 운명의 단짝의 성격과 외모를 출력합니다.
```
### 디렉토리 구조

```
fastapi-postgresql
┣── .github
┃   └─ workflows
│      └─ docker-image.yml
├── app
│   ├─ config.py
│   └─ main.py 
┣── sql_app
│   ├─ crud.py
│   ├─ database.py
│   ├─ models.py
│   └─ schemas.py
├── templates
│   ├─ index.html
│   └─ result.html
├── Dockerfile
├── poetry.lock
└── pyproject.toml
```
- `.github` - `workflows` : Github Actions 관련 디렉토리
    - `docker-image.yml` : 개발 서버 -> 운영서버 자동배포 ci/cd를 위한 yaml 파일

- `app` : main 기능 디렉토리
    - `config.py` : 환경변수 설정
    - `main.py` : main

- `sql_app` : 데이터베이스 관련 디렉토리(ORM)
    - `crud.py` : CRUD 작업
    - `database.py` : 데이터베이스 세션 연결 (SQLAlchemy)
    - `models.py` : 데이터베이스 테이블(컬럼, 속성) 생성 (SQLAlchemy model)
    - `schemas.py` : 데이터베이스 데이터 검증 (pydantic model)

- `templates` : html 템플릿 관련 디렉토리
    - `index.html` : 메인 화면 html 파일
    - `result.html` : 결과 화면 html 파일

<br>

- `Dockerfile` : 배포 이미지 작성

- `poetry.lock` : 의존성 잠금

- `pyproject.toml` : 설치 패키지 관리


## 2. 프로젝트 정보

### 기능별 사진



### 코드 설명


## 3. 프로젝트 결과

## 4. 외부리소스 정보
