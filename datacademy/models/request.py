"""Module containing the verification request class."""

from pydantic import BaseModel

from .objects import ObjectModel
from .types import ANSWER_TYPES, OBJECT_TYPES


class VerificationRequest(BaseModel):
    """Model class for an answer."""

    module: str
    """Module indentifier."""

    question: str
    """Question identifier."""

    answer: ObjectModel
    """ObjectModel containing the answer."""

    @staticmethod
    def create(module: str, question: str, answer: ANSWER_TYPES) -> 'VerificationRequest':
        """Creat a new answer.

        Args:
            module (str): Module identifier.
            question (str): Question identifier.
            answer (obj_types): Given answer.

        Returns:
            AnswerRequest: Answer object.
        """
        return VerificationRequest(module=module, question=question, answer=ObjectModel.create(answer))

    def get(self) -> OBJECT_TYPES:
        """Get the given answer.

        Returns:
            Any: Given answer.
        """
        return self.answer.get()
