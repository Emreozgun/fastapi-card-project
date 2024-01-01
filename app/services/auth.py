import uuid as uuid_pkg
from datetime import datetime, timedelta
from fastapi import status
from typing import Optional
from jose import jwt
from sqlalchemy import select, delete
from app.backend.config import config
from app.const import (
    AUTH_TOKEN_ALGORITHM,
    AUTH_TOKEN_EXPIRE_MINUTES,
    AUTH_TOKEN_TYPE,
)
from app.exc import raise_with_log
from app.models.users import UserModel
from app.schemas.auth import (
    ReqRegisterSchema,
    ReqLoginSchema,
    TokenSchema,
)
from app.schemas.card import ReqCreateCardSchema
from app.services.base import BaseDataManager, BaseService
from beartype import beartype

from app.services.card import CardService, generate_card_no
from app.util.auth import HashingMixin


@beartype
class AuthService(BaseService):
    def create_user(self, data: ReqRegisterSchema) -> TokenSchema:
        user = AuthDataManager(self.session).create_user(data.email, data.password)
        access_token = self._create_access_token(user_uuid=user.id)
        card = CardService(self.session).create_card(data=ReqCreateCardSchema(label="", card_no=generate_card_no()))
        return TokenSchema(access_token=access_token, token_type=AUTH_TOKEN_TYPE)

    def login(self, login: ReqLoginSchema) -> TokenSchema:
        user = AuthDataManager(self.session).get_user_with_login(login.email, login.password)
        if user is None:
            raise_with_log(status.HTTP_400_BAD_REQUEST, "Invalid email or password")
        # TODO: card_status = 'ACTIVE'
        access_token = self._create_access_token(user_uuid=user.id)
        return TokenSchema(access_token=access_token, token_type=AUTH_TOKEN_TYPE)

    def _create_access_token(self, user_uuid: str) -> str:
        payload = {
            "user": user_uuid,
            "expires_at": self._expiration_time(),
        }
        return jwt.encode(payload, config.token_key, algorithm=AUTH_TOKEN_ALGORITHM)

    #
    # def logout(self, user: UserSessionSchema) -> None:
    #     AuthDataManager(self.session).update_user_session(
    #         user.user_uuid, user.session_uuid, "closed"
    #     )

    @staticmethod
    def _expiration_time() -> str:
        expires_at = datetime.utcnow() + timedelta(minutes=AUTH_TOKEN_EXPIRE_MINUTES)
        return expires_at.strftime("%Y-%m-%d %H:%M:%S")


@beartype
class AuthDataManager(BaseDataManager, HashingMixin):
    def create_user(self, email: str, password: str) -> UserModel:
        model = UserModel(
            uuid=uuid_pkg.uuid4().hex,
            email=email,
            hashed_password=self.bcrypt(password),
        )
        self.session.add(model)
        return model

    def get_user_with_login(self, email: str, password: str) -> Optional[UserModel]:
        model = self.get_one(select(UserModel).where(UserModel.email == email))
        if not isinstance(model, UserModel):
            return None
        if not self.verify(model.password, password):
            print("not verify", model.password, password)
            return None
        return model

    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        model = self.get_one(select(UserModel).where(UserModel.email == email))
        if not isinstance(model, UserModel):
            return None
        return model

    # TODO: dev env
    if True:
        def delete_all(self):
            self.session.execute(delete(UserModel))
            self.session.commit()