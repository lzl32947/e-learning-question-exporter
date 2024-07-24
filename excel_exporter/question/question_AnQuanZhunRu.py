# I know Chinese name is always a headache for all, but I have to say that the name of the class is a good way to distinguish the class.
import re
from typing import List

from excel_exporter.question.base import Question, QuestionType

matching_regex = re.compile(r"^[ABCDEFGHI]\.]", re.M)


class Question_AnQuanZhunRu(Question):
    def __init__(self, order: int, question: str, company: str, question_type: str, easiness: str, options: str, answer: str, source: str):
        super().__init__()
        self.order = order
        self.question = question
        self.company = company
        self.question_type = self.parse_type(question_type)
        self.easiness = easiness
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
        else:
            return QuestionType.Unknown

    @staticmethod
    def parse_options(option: str) -> List[str]:
        items = option.strip().split("|")

        for index,item in enumerate(items):
            items[index] = item[2:]

        return items

