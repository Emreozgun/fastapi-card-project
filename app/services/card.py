import uuid as uuid_pkg
from fastapi import Depends
from typing import Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import update, func, desc, and_, or_
# from app.exc import raise_with_log
from app.models.card import CardModel
from app.models.users import UserModel
from app.schemas.auth import (
    UserSchema,
)
from app.schemas.base import ResMessageSchema
from app.schemas.card import ReqCreateCardSchema, ResCreateCardSchema, ReqDeleteCardSchema, \
    ReqUpdateCardSchema, ResFindAllCardSchema, CardSchema
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
        if not data.card_no:
            excluded_card_nos = CardDataManager(self.session).find_all(user_id=user.id)
            data.card_no = generate_card_no(excluded_card_nos=excluded_card_nos)
        card = CardDataManager(self.session).create_card(label=data.label, card_no=data.card_no, user_id=user.id)
        return ResCreateCardSchema(card_no=card.card_no)

    def update_card(self, data: ReqUpdateCardSchema, user: UserSchema = Depends(get_current_user)) -> ResMessageSchema:
        print("dStatus: ", data.status)
        card = CardDataManager(self.session).update_card(status=data.status, label=data.label, card_no=data.card_no,
                                                         user_id=user.id)
        if card:
            return ResMessageSchema(message=f"Card is updated", is_success=True)
        else:
            return ResMessageSchema(message=f"Card is not updated!", is_success=False)

    def delete_card(self, data: ReqDeleteCardSchema, user: UserSchema = Depends(get_current_user)) -> ResMessageSchema:
        card = CardDataManager(self.session).update_card(status='deleted', card_no=data.card_no, user_id=user.id)
        if card:
            return ResMessageSchema(message=f"Card is deleted", is_success=True)
        else:
            return ResMessageSchema(message=f"Card is not deleted!", is_success=False)

    def find_all_cards(self, user: UserSchema = Depends(get_current_user)) -> ResFindAllCardSchema:
        cards = CardDataManager(self.session).find_all(user_id=user.id)

        cards_list = []
        for c in cards:
            c_json = jsonable_encoder(c)
            cards_list.append(CardSchema(**c_json))

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
        x = self.session.query(CardModel).filter(
            CardModel.card_no == card_no,
            CardModel.user_id == user_id,
            CardModel.status != 'deleted'
        ).first()
        return x

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

    def update_card(self, card_no: str, user_id: str, label: Optional[str] = None, status: Optional[str] = None) -> Optional[CardModel]:
        # TODO: merge with transaction part. Same functions.
        active_cards = (
            self.session.query(CardModel.card_no)
            .filter(
                CardModel.user_id == user_id,
                CardModel.status == 'active'
            )
            .all()
        )

        if len(active_cards) > 1 or card_no not in [card[0] for card in active_cards]:
            stmt = update(CardModel).where(
                    CardModel.card_no == card_no,
                    CardModel.user_id == user_id,
                    CardModel.status != 'deleted'
            )

            if label is not None:
                stmt = stmt.values(label=label)
            if status is not None:
                print("status: ", status)
                stmt = stmt.values(status=status)

            result = self.session.execute(stmt)

            updated_rows = result.rowcount

            if updated_rows > 0:
                updated_model = self.session.query(CardModel).filter(
                    CardModel.card_no == card_no,
                    CardModel.user_id == user_id
                ).first()
                return updated_model

        return None

    def find_all(self, user_id: str) -> List[CardModel]:
        res = self.session.query(CardModel).filter(
            CardModel.user_id == user_id, CardModel.status != 'deleted'
        ).order_by(desc(CardModel.date_modified)).all()
        return res

