from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Union, Tuple, Callable


class QuestionType(Enum):
    SingleChoice = 1  # Multiple Choice Question
    MultipleChoice = 2  # Real Multiple Choice Question
    Judge = 3
    Calculation = 4  # Calculation Question
    Picture = 5  # Picture Question
    Answer = 6  # Answer
    Unknown = -1


ORDER_MAPPINGS = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I"}


class Question(ABC):
    def __init__(self):
        self.name = "Unknown"
        self.question_type = QuestionType.Unknown
