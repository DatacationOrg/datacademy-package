"""Module containing classes for the verification response."""

from pydantic import BaseModel

from .objects import ObjectModel
from .types import ANSWER_TYPES

DEFAULT_MESSAGE_CORRECT: str = "That's correct!"
"""Default message to show for correct answers."""

DEFAULT_MESSAGE_INCORRECT: str = "Unfortunately, that's not correct."
"""Default message to show for incorrect answers."""

DEFAULT_MESSAGE_HINTS: str = 'Here are some hints:'
"""Default message to show for hints."""

DEFAULT_MESSAGE_INFO: str = 'Here is some additional information:'
"""Default message to show for information."""


class VerificationMessage(BaseModel):
    """Model class for messages included in an verification response."""

    message: str
    """Message string."""

    obj: ObjectModel | None = None
    """Optional request object accompanying the message."""

    @staticmethod
    def create(message: str, obj: ANSWER_TYPES | None = None) -> 'VerificationMessage':
        """Create a new message.

        Args:
            message (str): Message string
            obj (obj_types | None, optional): Object accompanying the message. Defaults to None.

        Returns:
            Message: Message.
        """
        if obj is not None:
            return VerificationMessage(message=message, obj=ObjectModel.create(obj))
        return VerificationMessage(message=message)

    def get_object(self) -> ANSWER_TYPES | None:
        """Get the object.

        Returns:
            Any: Object accompanying the message, if any.
        """
        if self.obj is None:
            return None

        return self.obj.get()


class VerificationResponse(BaseModel):
    """Model class for a response to an answer."""

    correct: bool = True
    """Whether the answer was correct."""

    errors: list[VerificationMessage] = []
    """List of errors."""

    hints: list[VerificationMessage] = []
    """List of hints."""

    info: list[VerificationMessage] = []
    """List of information messages."""

    message_correct: str = DEFAULT_MESSAGE_CORRECT
    """Message to show for correct answers."""

    message_incorrect: str = DEFAULT_MESSAGE_INCORRECT
    """Message to show for INcorrect answers."""

    message_hints: str = DEFAULT_MESSAGE_HINTS
    """Message to show for hints."""

    message_info: str = DEFAULT_MESSAGE_INFO
    """Message to show for information."""

    def add_error(self, message: str, obj: ANSWER_TYPES | None = None) -> None:
        """Add an error. Will automatically set the answer to be incorrect.

        NOTE: Will not change correctness of answer.

        Args:
            message (str): Error message.
            obj (obj_types | None, optional): Object to accompany message. Defaults to None.
        """
        self.set_incorrect()
        self.errors.append(VerificationMessage.create(message, obj))

    def add_hint(self, message: str, obj: ANSWER_TYPES | None = None) -> None:
        """Add a hint.

        NOTE: Will not change correctness of answer.

        Args:
            message (str): Error message.
            obj (obj_types | None, optional): Object to accompany message. Defaults to None.
        """
        self.hints.append(VerificationMessage.create(message, obj))

    def add_info(self, message: str, obj: ANSWER_TYPES | None = None) -> None:
        """Add an information message.

        NOTE: Will not change correctness of answer.

        Args:
            message (str): Error message.
            obj (obj_types | None, optional): Object to accompany message. Defaults to None.
        """
        self.info.append(VerificationMessage.create(message, obj))

    def is_correct(self) -> bool:
        """Get whether this message is correct.

        Returns:
            bool: True if correct, False otherwise.
        """
        return self.correct

    def is_incorrect(self) -> bool:
        """Get whether this message is incorrect.

        Returns:
            bool: True if incorrect, False otherwise.
        """
        return not self.correct

    def set_correct(self, message: str | None = None) -> None:
        """Set this answer to be correct.

        Args:
            message (str | None, optional): Correct message to use instead of default. Defaults to None.
        """
        self.correct = True
        if message is not None:
            self.message_correct = message

    def set_incorrect(self, message: str | None = None) -> None:
        """Set this answer to be incorrect.

        Args:
            message (str | None, optional): Incorrect message to use instead of default. Defaults to None.
        """
        self.correct = False
        if message is not None:
            self.message_incorrect = message

    def set_hint_message(self, message: str) -> None:
        """Set the message for hints to use instead of default.

        Args:
            message (str): Message.
        """
        self.message_hints = message

    def set_info_message(self, message: str) -> None:
        """Set the message for additional information to use instead of default.

        Args:
            message (str): Message.
        """
        self.message_hints = message
