import uuid as uuid_pkg
from fastapi import Depends
from typing import Optional, List, Type
from sqlalchemy import delete, update, func, desc
# from app.exc import raise_with_log
from app.models.card import CardModel
from app.models.users import UserModel
from app.schemas.auth import (
    UserSchema,
)
from app.schemas.base import ResMessageSchema
from app.schemas.card import ReqCreateCardSchema, ResCreateCardSchema, ReqDeleteCardSchema, \
    ReqUpdateCardSchema, ResFindAllCardSchema
from app.services.base import BaseDataManager, BaseService
from beartype import beartype
from typing import Union

from app.util.common import get_current_user
from app.util.card import generate_card_no


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_schema = OAuth2PasswordBearer(tokenUrl=AUTH_URL, auto_error=False)


@beartype
class CardService(BaseService):
    def create_card(self, data: ReqCreateCardSchema,
                    user: UserSchema = Depends(get_current_user)) -> ResCreateCardSchema:
        print(user.dict())
        if not data.card_no:
            excluded_card_nos = CardDataManager(self.session).find_all(user_id=user.id)
            generate_card_no(excluded_card_nos=excluded_card_nos)

        card = CardDataManager(self.session).create_card(label=data.label, card_no=data.card_no, user_id=user.id)
        return ResCreateCardSchema(card_no=card.card_no)

    def update_card(self, data: ReqUpdateCardSchema, user: UserSchema = Depends(get_current_user)) -> ResMessageSchema:
        card = CardDataManager(self.session).update_card(status=data.status, label=data.label, card_no=data.card_no,
                                                         user_id=user.id)

        if card.status == data.status:
            return ResMessageSchema(message=f"Card is updated", is_success=True)
        else:
            return ResMessageSchema(message=f"Card is not updated!", is_success=False)

    def delete_card(self, data: ReqDeleteCardSchema, user: UserSchema = Depends(get_current_user)) -> ResMessageSchema:
        card = CardDataManager(self.session).delete_card(card_no=data.card_no, user_id=user.id)
        if card:
            return ResMessageSchema(message=f"Card is deleted", is_success=True)
        else:
            return ResMessageSchema(message=f"Card is not deleted!", is_success=False)

    def find_all_cards(self, user: UserSchema = Depends(get_current_user)) -> ResFindAllCardSchema:
        cards = CardDataManager(self.session).find_all(user_id=user.id)

        cards_list = []
        for c in cards:
            cards_list.append(CardModel(label=c["label"], card_no=c["card_no"], amount=c["user_id"], description=c["status"]))

        return ResFindAllCardSchema(cards=cards_list)

    def validate_user_card_access(self, card_no: str, user: UserSchema = Depends(get_current_user)) -> bool:
        card = CardDataManager(self.session).validate_user_card_access(user_id=user.id, card_no=card_no)

        return True if card else False


@beartype
class CardDataManager(BaseDataManager):
    def create_card(self, label: str, card_no: str, user_id: str) -> CardModel:
        model = CardModel(
            id=uuid_pkg.uuid4().hex,
            label=label,
            card_no=card_no,
            user_id=user_id,
        )
        self.session.add(model)
        return model

    def validate_user_card_access(self, card_no: str, user_id: str) -> Optional[CardModel]:
        return self.session.query(CardModel).filter(
            CardModel.id == card_no,
            CardModel.user_id == user_id,
            CardModel.status != 'deleted'
        ).first()

    def get_card_count(self, user_id: str) -> int:
        return (
            self.session.query(func.count())
            .filter(CardModel.user_id == user_id, CardModel.status != 'deleted')
            .scalar()
        )

    def delete_card(self, card_no: str, user_id: str) -> Union[CardModel, None]:
        model = self.validate_user_card_access(card_no=card_no, user_id=user_id)

        if model:
            card_count = self.get_card_count(user_id=user_id)
            if card_count > 1:
                self.session.delete(model)
                self.session.commit()
                return model
            else:
                return None
        else:
            return None

    def update_card(self, card_no: str, user_id: str, label: str, status: str) -> Optional[CardModel]:

        stmt = update(CardModel).where(
            CardModel.card_no == card_no,
            CardModel.user_id == user_id,
            CardModel.status != 'deleted'
        )

        if label is not None:
            stmt = stmt.values(label=label)
        if status is not None:
            stmt = stmt.values(status=status)

        result = self.session.execute(stmt.returning(CardModel))
        updated_model = result.fetchone()

        self.session.commit()

        return updated_model

    def find_all(self, user_id: str) -> List[Type[CardModel]]:
        return self.session.query(CardModel).filter(
            CardModel.user_id == user_id, CardModel.status != 'deleted'
        ).order_by(desc(CardModel.date_modified)).all()

    # TODO: dev env
    if True:
        def delete_all(self):
            self.session.execute(delete(UserModel))
            self.session.commit()
