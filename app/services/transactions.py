import uuid as uuid_pkg
from sqlalchemy import delete, func, text

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

        details = [
            CardTransactionsDetails(
                label=t.label,
                card_no=t.card_no,
                amount=t.amount,
                description=t.description,
            )
            for t in transactions
        ]

        return ResFilterCardTransactionsSchema(details=details)

    def get_card_stats(self, user: UserSchema = Depends(get_current_user)) -> ResCardStatsSchema:
        active_card_count, total_amount_spent_on_active_cards = TransactionDataManager(
            self.session).get_active_card_stats(user_id=user.id)

        passive_card_count, total_amount_spent_on_passive_cards = TransactionDataManager(
            self.session).get_passive_card_stats(user_id=user.id)

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

    # TODO: Add beartype for all function
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

        return 0 if active_card_count is None else active_card_count, 0.00 if total_amount_spent_on_active_cards is None else total_amount_spent_on_active_cards

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

        return 0 if passive_card_count is None else passive_card_count, 0.00 if total_amount_spent_on_passive_cards is None else total_amount_spent_on_passive_cards

    def filter_cards_transactions(self, user_id: str, filter_text: str):

        result = self.session.execute(
            text("""
            SELECT transactions.*, card.*
            FROM transactions
            JOIN card ON transactions.card_id = card.card_no
            WHERE card.user_id = :user_id
            AND (card.label LIKE '%' || :filter_text || '%' OR card.card_no LIKE '%' || :filter_text || '%');
            """
                 ),
            {"user_id": user_id, "filter_text": filter_text}
        )

        filtered_cards = result.fetchall()

        return filtered_cards

    # TODO: dev env
    if True:
        def delete_all(self):
            self.session.execute(delete(UserModel))
            self.session.commit()
