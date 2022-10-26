# Numanguan - AI기반 관상 키워드, 운명의 단짝 매칭 서비스

## 1. 프로젝트 설명

### 프로젝트명

AI 기반 관상 키워드, 운명의 단짝 매칭 서비스

### 프로젝트 소개

사용자의 얼굴 이미지를 입력받아 닮은 연예인 얼굴과 관상 키워드를 출력합니다.

사용자의 생년월일 정보를 입력받아 사주팔자 정보를 통해 운명의 단짝의 성격과 외모를 출력합니다.

### 디렉토리 구조

```
fastapi-postgresql
├── .github
│   └─ workflows
│      └─ docker-image.yml
├── app
│   ├─ config.py
│   └─ main.py 
├── sql_app
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

- `app` : main 기능 디렉토리

- `images` : favicon 이미지

- `sql_app` : 데이터베이스 관련 디렉토리(ORM)

- `templates` : html 템플릿 관련 디렉토리


### 인프라 아키텍처
<img src="https://user-images.githubusercontent.com/58734611/197971132-6a7dce78-352f-4f6a-a3da-d2934d33e4ae.png">

### 어플리케이션 아키텍처
<img src="https://user-images.githubusercontent.com/58734611/197971034-a090c936-467d-49be-b6e8-d5f69bc0c8b8.png">

## 2. 프로젝트 결과물

### 기능별 사진

<img src="https://user-images.githubusercontent.com/58734611/194035548-a1c856b1-e6c6-4b76-80db-13b633ff3c54.png">
<p>메인 화면 - 사용자 입력 받는 화면</p>

<img src="https://user-images.githubusercontent.com/58734611/194035632-deef9a2c-2c93-4c3f-9661-92669430f958.png">
<p>결과 화면1 - 관상 정보와 키워드 정보 출력 화면</p>

<img src="https://user-images.githubusercontent.com/58734611/194035672-22472096-3437-40ec-98ff-b9a2c91ec1a0.png">
<p>결과화면2 - 운명의 단짝 성격, 외모 정보 출력 화면</p>

### 코드 설명

#### App

```python
@app.get("/", response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

```python
@app.post("/result/")
def create_user(request: Request, image: UploadFile = File() , name: str = Form(), gender: str = Form(), year: str = Form(), month: str=Form(), day: str=Form(),keyword: str=Form(), db: Session= Depends(get_db)):

    ...
    
    return templates.TemplateResponse("result.html", {"request":request,"name":user.name, "image":my_image, "other_image":other_image, "keyword": keyword ,"look":saju.look, "personality":saju.personality})
```
> HTTP Method(GET, POST)를 통해 html파일과 요청받은 정보를 DB에서 읽어 응답

#### DB

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    gender = Column(String,  index=True)
    year = Column(Integer,  index=True)
    month = Column(Integer,  index=True)
    day = Column(Integer,  index=True)
```
```python
class Saju(Base):
    __tablename__ = "saju"

    owner_id = Column(Integer, ForeignKey("users.id"))
    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String, index=True)
    year = Column(Integer, index=True)
    month = Column(Integer, index=True)
    day = Column(Integer,  index=True)
    look = Column(String(512), index=True)
    personality = Column(String(512), index=True)
```

> 사용자 정보와 사주팔자 정보 테이블 생성

```python
SQLALCHEMY_DATABASE_URL = "postgresql://..."

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

> DB 엔진 연결

```python
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, gender=user.gender, year=user.year, month=user.month, day=user.day)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

```python
def get_saju(db: Session, gender: str, year: int, month: int, day: int):
    return db.query(models.Saju).filter(models.Saju.gender == gender
    , models.Saju.year == year, models.Saju.month == month
    , models.Saju.day == day).first()
```
> 사용자 정보 저장 및 사주팔자 정보 읽기
