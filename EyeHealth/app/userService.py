from fastapi import FastAPI, Depends, HTTPException
from fastapi_users import FastAPIUsers, models, schemas
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, BearerTransport
from sqlalchemy import Column, Integer, String, Enum, create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from passlib.context import CryptContext
import datetime
import jwt
from pydantic import EmailStr
import os

# ================= Инициализация =================
DATABASE_URL = "postgresql://postgres:password@localhost/userdb"
SECRET_KEY = "MY_SECRET_KEY"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

class PasswordConfigurator:
    password_for_hash = "ssh"
    password_helper: PasswordHelperProtocol

    def __init__(self, password_helper: Optional[PasswordHelperProtocol] = None):
        if password_helper is None:
            self.password_helper = PasswordHelper()
        else:
            self.password_helper = password_helper

    def hash(self, password_for_hash: str):
        hashed_password = self.password_helper.hash(self.password_for_hash)
        return hashed_password

password_configurator = PasswordConfigurator()
class UserService:
    def __init__(self, name=None, email=None, role=None):
        self.name = name
        self.email = email
        self.role = role

    def get_user_info(self):
        return {"name": self.name, "email": self.email, "role": self.role}


class UserServiceBuilder:
    def __init__(self):
        self._user = {}

    def set_name(self, name):
        self._user["name"] = name
        return self

    def set_email(self, email):
        self._user["email"] = email
        return self

    def set_role(self, role):
        self._user["role"] = role
        return self

    def build(self):
        return UserService(**self._user)


class UserServiceDirector:
    def __init__(self, builder):
        self.builder = builder

    def construct_admin(self, name, email):
        """Метод для создания пользователя с ролью Admin"""
        return self.builder.set_name(name).set_email(email).set_role("Admin").build()

    def construct_user(self, name, email):
        """Метод для создания обычного пользователя с ролью User"""
        return self.builder.set_name(name).set_email(email).set_role("User").build()

    def construct_guest(self, name, email):
        """Метод для создания гостевого пользователя"""
        return self.builder.set_name(name).set_email(email).set_role("Guest").build()




# ================= Модель пользователя =================
class RoleEnum(str, Enum):
    ADMIN = "Admin"
    DOCTOR = "Doctor"


class User(models.BaseUser, models.BaseOAuthAccount):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    password = Column(String, nullable=False)  # Хешированный пароль


Base.metadata.create_all(bind=engine)


# ================= Схемы Pydantic =================
class UserCreate(schemas.BaseUserCreate):
    name: str
    phone_number: str
    role: RoleEnum


class UserResponse(schemas.BaseUser):
    id: int
    name: str
    phone_number: str
    role: RoleEnum


class AuthRequest(schemas.BaseLogin):
    pass


# ================= Репозитории и сервисы =================

# FastAPI Users создаст всё для аутентификации, включая создание токенов
class UserRepository:
    def __init__(self, db: Session):
        self.db = db
         async def create(
        self,
        user_create: UserCreate,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> User:
        await self.validate_password(user_create.password, user_create)

        existing_user = self.find_by_email(user_create.email)
        if existing_user is not None:
            raise HTTPException(status_code=400, detail="User already exists")

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )

        password = user_dict.pop("password")
        user_dict["hashed_password"] = pwd_context.hash(password)

        created_user = User(**user_dict)
        self.save(created_user)

        return created_user

    def save(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def find_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()


# ================= FastAPI Users Authentication =================
def get_jwt_strategy():
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)


# ================= FastAPI Users настройки =================
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(),
    get_strategy=get_jwt_strategy
)

# FastAPI Users экземпляр
fastapi_users = FastAPIUsers(
    get_user_manager=UserRepository,
    auth_backends=[auth_backend],
    user_model=User,
    user_create_model=UserCreate,
    user_update_model=UserResponse
)


# ================= Маршруты FastAPI =================
@app.post("/register")
async def register(user_data: UserCreate, db: Session = Depends(SessionLocal)):
    repo = UserRepository(db)
    hashed_password = pwd_context.hash(user_data.password)
    new_user = User(
        name=user_data.name,
        phone_number=user_data.phone_number,
        email=user_data.email,
        role=user_data.role,
        password=hashed_password
    )
    repo.save(new_user)
    return {"message": "Пользователь зарегистрирован!"}


@app.post("/auth")
async def auth(auth_request: AuthRequest, db: Session = Depends(SessionLocal)):
    repo = UserRepository(db)
    user = repo.find_by_email(auth_request.email)
    if not user or not pwd_context.verify(auth_request.password, user.password):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    # Генерация токена вручную (если не использовать FastAPI Users для этого)
    token = jwt.encode({"sub": user.email, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)}, SECRET_KEY,
                       algorithm="HS256")
    return {"token": token}


# Добавление маршрутов для FastAPI Users
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_register_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])
