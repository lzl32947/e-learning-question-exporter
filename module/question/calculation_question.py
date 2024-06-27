import re
from typing import Union, Tuple, Optional, List

from .base import Question, QuestionType


class CalculationQuestion(Question):
    def __init__(self, question_sequence: Union[Tuple[int, ...], str], question_body: str, question_answer: str, question_explanation: str, question_related: str,
                 question_raw_catalog: str, question_raw_type: str):
        super().__init__(question_sequence, question_body, question_answer, question_explanation, question_related, question_raw_catalog, question_raw_type)
        self.question_type = QuestionType.Calculation

    @staticmethod
    def create(intermediate: str, s1: int, s2: int, catalog: str, ntype: str) -> List["CalculationQuestion"]:
        data_list = []
        regex = re.compile(f"^{s1}+\\.{s2}+\\.(\\d+)\\." + r"\s*第(\d+)题\s([\s\S]*?)正确答案：(.*?)[，,]\s+教师详解：([\s\S]*?)关联评价点的名称：(.*?)\s", re.M)

        p = regex.findall(intermediate)
        for item in p:
            seq = (s1, s2, int(item[0]))
            inner_seq = int(item[1])
            body = item[2]
            answer = item[3]
            explanation = item[4]
            related = item[5]

            question = CalculationQuestion(seq, body, answer, explanation, related, catalog, ntype)
            data_list.append(question)

        return data_list
