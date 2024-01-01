import uuid as uuid_pkg
from sqlalchemy import delete, func

from app.exc import raise_with_log
# from app.exc import raise_with_log
from app.models.card import CardModel
from app.models.transactions import TransactionsModel
from app.models.users import UserModel
from app.schemas.auth import (
    UserSchema,
)
from fastapi import Depends, status
from app.schemas.transactions import (ResCardStatsSchema, ReqCreateTransactionSchema, ResCreateTransactionSchema,
                                      ResFilterCardTransactionsSchema, CardTransactionsDetails)
from typing import Union

from app.services.base import BaseDataManager, BaseService
from beartype import beartype

from app.services.card import CardService
from app.util.common import get_current_user


@beartype
class TransactionService(BaseService):

    def create(self, data: ReqCreateTransactionSchema,
               user: UserSchema = Depends(get_current_user)) -> ResCreateTransactionSchema:

        is_valid_user = CardService(self.session).validate_user_card_access(user=user, card_no=data.card_id)

        if not is_valid_user:
            raise_with_log(status.HTTP_400_BAD_REQUEST, "Unauthorized user/Card not found!")

        transaction = TransactionDataManager(self.session).create(amount=data.amount, description=data.description,
                                                                  card_id=data.card_id)
        return ResCreateTransactionSchema(t_id=transaction.id)

    def filtered_card_transactions(self, text: Union[str, None],
                                   user: UserSchema = Depends(get_current_user)) -> ResFilterCardTransactionsSchema:

        transactions = TransactionDataManager(self.session).filter_cards_transactions(user_id=user.id,
                                                                                      filter_text=text)

        details = []

        if len(transactions) > 0:
            for t in transactions:
                details.append(CardTransactionsDetails(label=t["label"], card_no=t["card_no"], amount=t["amount"],
                                                       description=t["description"]))

        return ResFilterCardTransactionsSchema(details=details)

    def get_card_stats(self, user: UserSchema = Depends(get_current_user)) -> ResCardStatsSchema:
        active_card_count, total_amount_spent_on_active_cards = TransactionDataManager(
            self.session).get_active_card_stats(user_id=user.user_uuid)

        passive_card_count, total_amount_spent_on_passive_cards = TransactionDataManager(
            self.session).get_active_card_stats(user_id=user.user_uuid)

        return ResCardStatsSchema(active_card_count=active_card_count, passive_card_count=passive_card_count,
                                  total_amount_spent_on_passive_cards=total_amount_spent_on_passive_cards,
                                  total_amount_spent_on_active_cards=total_amount_spent_on_active_cards)


@beartype
class TransactionDataManager(BaseDataManager):
    def create(self, amount: float, description: str, card_id: str) -> TransactionsModel:
        # TODO: Auto-generated yapilabilir.
        model = TransactionsModel(
            id=uuid_pkg.uuid4().hex,
            amount=amount,
            description=description,
            card_id=card_id
        )
        self.session.add(model)
        return model

    def get_active_card_stats(self, user_id: str):
        active_card_count = (
            self.session.query(func.count())
            .filter(CardModel.user_id == user_id, CardModel.status == 'active')
            .scalar()
        )

        total_amount_spent_on_active_cards = (
            self.session.query(func.sum(TransactionsModel.amount))
            .join(CardModel, TransactionsModel.card_id == CardModel.card_no)
            .filter(CardModel.user_id == user_id, CardModel.status == 'active')
            .scalar()
        )

        return active_card_count, total_amount_spent_on_active_cards

    def get_passive_card_stats(self, user_id: str):
        passive_card_count = (
            self.session.query(func.count())
            .filter(CardModel.user_id == user_id, CardModel.status == 'passive')
            .scalar()
        )

        total_amount_spent_on_passive_cards = (
            self.session.query(func.sum(TransactionsModel.amount))
            .join(CardModel, TransactionsModel.card_id == CardModel.card_no)
            .filter(CardModel.user_id == user_id, CardModel.status == 'passive')
            .scalar()
        )

        return passive_card_count, total_amount_spent_on_passive_cards

    def filter_cards_transactions(self, user_id: str, filter_text: str):
        filtered_cards = (
            self.session.query(TransactionsModel)
            .join(CardModel, TransactionsModel.card_id == CardModel.card_no)
            .filter(
                CardModel.user_id == user_id,
                (CardModel.label.ilike(f"%{filter_text}%") | CardModel.card_no.ilike(f"%{filter_text}%"))
            )
            .all()
        )

        return filtered_cards

    # TODO: dev env
    if True:
        def delete_all(self):
            self.session.execute(delete(UserModel))
            self.session.commit()
