import re
from typing import Union, Tuple, List, Optional

from .base import Question, QuestionType, ORDER_MAPPINGS


class MultipleChoiceQuestion(Question):

    @staticmethod
    def filter_choices(choices: List[str]) -> List[str]:
        # Filter out empty choices
        choices = [i.strip() for i in choices if i != ""]
        choices = [MultipleChoiceQuestion.remove_separator(i) for i in choices if i != ""]

        # Filter out the choices that starts with "|" that are mistakenly added
        for i in range(len(choices)):
            if len(choices[i]) > 1 and choices[i].startswith("|"):
                choices[i] = choices[i][1:]

        # Filter out the choices that are starts with the sequential orders, e.g. A. XXX, B. XXX, C. XXX
        while True:
            contains_flag = True
            for i in range(len(choices)):
                if choices[i] != "" and not choices[i].startswith(ORDER_MAPPINGS[i]):
                    contains_flag = False
                    break
            if contains_flag:
                # There is something to be removed!
                if len(choices[0]) >= 2:
                    char = choices[0][1]
                    if char in [".", "、", "-", "_"]:
                        # Yes, we check
                        remove_flag = True
                        for i in range(1, len(choices)):
                            if choices[i] != "" and char != choices[i][1]:
                                remove_flag = False
                                break
                        if remove_flag:
                            # REMOVE NOW!
                            for i in range(len(choices)):
                                if choices[i] != "":
                                    choices[i] = choices[i][2:].strip()
                    else:
                        break
                else:
                    break
            else:
                break

        return choices

    def __init__(self, question_sequence: Union[Tuple[int, ...], str], question_body: str, question_selections: List[str], question_answer: str, question_explanation: str,
                 question_related: str, question_raw_catalog: str, question_raw_type: str):
        super().__init__(question_sequence, question_body, question_answer, question_explanation, question_related, question_raw_catalog, question_raw_type)
        self.question_selections = self.filter_choices(question_selections)
        self.question_type = QuestionType.MultipleChoice

    @staticmethod
    def call_regex(intermediate: str, s1: int, s2: int) -> Tuple[Tuple[int, ...], int, str, List[str], str, str]:
        regex = re.compile(
            f"^{s1}\\.{s2}\\.(\\d+)\\." + r"\s+第(\d+)题([\s\S]+?)(?=A)(?:A\.)([\s\S]+?)(?=B)(?:B\.)([\s\S]+?)(?=[C正])((?:C\.)([\s\S]+?)(?=[D正]))*((?:D\.)([\s\S]+?)(?=[E正]))*((?:E\.)([\s\S]+?)(?=[F正]))*((?:F\.)([\s\S]+?)(?=[G正]))*((?:G\.)([\s\S]+?)(?=H正))*((?:H\.)([\s\S]+?)(?=I正))*((?:I\.)([\s\S]+?)(?=正))*正确答案：\s*([ABCDEFGHI]+)\s+关联评价点的名称：(.*?)\n",
            re.MULTILINE)
        p = regex.findall(intermediate)
        for item in p:
            seq = (s1, s2, int(item[0]))
            inner_seq = int(item[1])
            body = item[2]
            ans_a = item[3]
            ans_b = item[4]
            ans_c = item[6]
            ans_d = item[8]
            ans_e = item[10]
            ans_f = item[12]
            ans_g = item[14]
            ans_h = item[16]
            ans_i = item[18]
            correct_ans = item[19]
            related = item[20]
            yield seq, inner_seq, body, [ans_a, ans_b, ans_c, ans_d, ans_e, ans_f, ans_g, ans_h, ans_i], correct_ans, related

    @staticmethod
    def create(intermediate: str, s1: int, s2: int, catalog: str, ntype: str) -> List["MultipleChoiceQuestion"]:
        data_list = []
        for item in MultipleChoiceQuestion.call_regex(intermediate, s1, s2):
            seq, inner_seq, body, selections, correct_ans, related = item
            data_list.append(MultipleChoiceQuestion(seq, body, selections, correct_ans, "", related, catalog, ntype))
        return data_list


class PictureChoiceQuestion(MultipleChoiceQuestion):
    def __init__(self, question_sequence: Union[Tuple[int, ...], str], question_body: str, question_selections: List[str], question_answer: str, question_explanation: str,
                 question_related: str, question_raw_catalog: str, question_raw_type: str):
        super().__init__(question_sequence, question_body, question_selections, question_answer, question_explanation, question_related, question_raw_catalog, question_raw_type)
        self.question_type = QuestionType.Picture

    @staticmethod
    def create(intermediate: str, s1: int, s2: int, catalog: str, ntype: str) -> List["PictureChoiceQuestion"]:
        data_list = []
        for item in PictureChoiceQuestion.call_regex(intermediate, s1, s2):
            seq, inner_seq, body, selections, correct_ans, related = item
            data_list.append(PictureChoiceQuestion(seq, body, selections, correct_ans, "", related, catalog, ntype))
        return data_list


class SingleChoiceQuestion(MultipleChoiceQuestion):
    def __init__(self, question_sequence: Union[Tuple[int, ...], str], question_body: str, question_selections: List[str], question_answer: str, question_explanation: str,
                 question_related: str, question_raw_catalog: str, question_raw_type: str):
        super().__init__(question_sequence, question_body, question_selections, question_answer, question_explanation, question_related, question_raw_catalog, question_raw_type)
        self.question_type = QuestionType.SingleChoice

    @staticmethod
    def create(intermediate: str, s1: int, s2: int, catalog: str, ntype: str) -> List["SingleChoiceQuestion"]:
        data_list = []
        for item in SingleChoiceQuestion.call_regex(intermediate, s1, s2):
            seq, inner_seq, body, selections, correct_ans, related = item
            data_list.append(SingleChoiceQuestion(seq, body, selections, correct_ans, "", related, catalog, ntype))
        return data_list


class JudgeChoiceQuestion(SingleChoiceQuestion):
    def __init__(self, question_sequence: Union[Tuple[int, ...], str], question_body: str, question_selections: List[str], question_answer: str, question_explanation: str,
                 question_related: str, question_raw_catalog: str, question_raw_type: str):
        super().__init__(question_sequence, question_body, question_selections, question_answer, question_explanation, question_related, question_raw_catalog, question_raw_type)
        self.question_type = QuestionType.Judge

    @staticmethod
    def create(intermediate: str, s1: int, s2: int, catalog: str, ntype: str) -> List["JudgeChoiceQuestion"]:
        data_list = []
        for item in JudgeChoiceQuestion.call_regex(intermediate, s1, s2):
            seq, inner_seq, body, selections, correct_ans, related = item
            data_list.append(JudgeChoiceQuestion(seq, body, selections, correct_ans, "", related, catalog, ntype))
        return data_list
