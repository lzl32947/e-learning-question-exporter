from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Union, Tuple, Callable


class QuestionType(Enum):
    SingleChoice = 1  # Multiple Choice Question
    MultipleChoice = 2  # Real Multiple Choice Question
    Judge = 3
    Calculation = 4  # Calculation Question
    Picture = 5  # Picture Question
    Unknown = -1


ORDER_MAPPINGS = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I"}


class Question(ABC):
    @staticmethod
    def _check_question_sequence(seq: Union[Tuple[int, ...], str]) -> Tuple[int, ...]:
        if isinstance(seq, str):
            try:
                return tuple(map(int, seq.split(".")))
            except:
                return (-1,)
        return seq

    @staticmethod
    def remove_separator(content: str) -> str:
        while True:
            if content.endswith("\r") or content.endswith("\n"):
                content = content[:-1]
            else:
                break
        return content

    def __init__(self, question_sequence: Union[Tuple[int, ...], str], question_body: str, question_answer: str, question_explanation: str, question_related: str,
                 question_raw_catalog: str, question_raw_type: str):
        self.question_sequence: Tuple[int, ...] = self._check_question_sequence(question_sequence)
        self.question_body: str = self.remove_separator(question_body)
        self.question_type: QuestionType = QuestionType.Unknown
        self.question_explanation: str = question_explanation
        self.question_related: str = question_related
        self.question_answer: str = question_answer
        self.question_raw_catalog: str = question_raw_catalog
        self.question_raw_type: str = question_raw_type
