# I know Chinese name is always a headache for all, but I have to say that the name of the class is a good way to distinguish the class.
import re
from typing import List

from excel_exporter.question.base import Question, QuestionType

matching_regex = re.compile(r"^[ABCDEFGHI]\.]", re.M)


class Question_AnGui(Question):
    def __init__(self, order: int, l1:str,l2:str, question_catalog: str, question_type: str,question: str,  options: str,answer: str,  source: str):
        super().__init__()
        self.order = order
        self.question = question
        self.l1 = l1
        self.l2 = l2
        self.question_catalog = question_catalog
        self.question_type = self.parse_type(question_type)
        self.options = self.parse_options(options)
        self.answer = answer
        self.source = source

    @staticmethod
    def parse_type(question_type: str) -> QuestionType:
        if question_type.startswith("单选"):
            return QuestionType.SingleChoice
        elif question_type.startswith("多选"):
            return QuestionType.MultipleChoice
        elif question_type.startswith("判断"):
            return QuestionType.Judge
        elif question_type.startswith("计算"):
            return QuestionType.Calculation
        elif question_type.startswith("识图"):
            return QuestionType.Picture
        elif question_type.startswith("简答"):
            return QuestionType.Answer
        else:
            return QuestionType.Unknown

    @staticmethod
    def parse_options(option: str) -> List[str]:
        items = option.strip().split("|")

        for index,item in enumerate(items):
            if len(item) < 2:
                continue
            items[index] = item[2:]

        return items

