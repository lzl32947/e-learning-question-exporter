from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple, Union, List


class QuestionType(Enum):
    SingleChoice = 1  # Multiple Choice Question
    MultipleChoice = 2  # Real Multiple Choice Question
    Judge = 3
    Calculation = 4  # Calculation Question
    Picture = 5  # Picture Question
    Fill = 6  # Fill in the blanks
    Unknown = -1


mappings = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I"}


class BaseQuestion(ABC):
    def __init__(self,
                 question_sequence: Tuple[int],
                 question_body: str,
                 question_chapter: str = "",
                 question_explanation=""):
        self.question_sequence = question_sequence
        self.question_body = question_body
        self.question_type = QuestionType.Unknown
        self.question_chapter = question_chapter
        self.question_explanation = question_explanation

    def get_chapter(self):
        return "{}/{}".format(self.question_sequence[0], self.question_sequence[1])

    @staticmethod
    def check_answer(answer: str):
        ans = []
        for i in range(ord("A"), ord("J")):
            if chr(i) in answer:
                ans.append(chr(i))
        return "".join(ans)

    @staticmethod
    def check_choice(choices: Union[Tuple[str], List[str]]):
        for i in range(len(choices)):
            if len(choices[i]) > 1 and choices[i].startswith("|"):
                choices[i] = choices[i][1:]

        while True:
            contains_flag = True
            for i in range(len(choices)):
                if choices[i] != "" and not choices[i].startswith(mappings[i]):
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


class SingleChoiceQuestion(BaseQuestion):
    def __init__(self,
                 question_sequence: Tuple[int],
                 question_body: str,
                 question_choices: Union[Tuple[str], List[str]],
                 question_answer: str,
                 question_chapter: str = "",
                 question_explanation=""):
        super(SingleChoiceQuestion, self).__init__(question_sequence, question_body,
                                                   question_chapter, question_explanation)
        self.question_type = QuestionType.SingleChoice
        self.question_choices = self.check_choice(question_choices)
        self.question_answer = self.check_answer(question_answer)


class MultipleChoiceQuestion(BaseQuestion):
    def __init__(self,
                 question_sequence: Tuple[int],
                 question_body: str,
                 question_choices: Union[Tuple[str], List[str]],
                 question_answer: str,
                 question_chapter: str = "",
                 question_explanation=""):
        super(MultipleChoiceQuestion, self).__init__(question_sequence, question_body,
                                                     question_chapter, question_explanation)
        self.question_type = QuestionType.MultipleChoice
        self.question_answer = self.check_answer(question_answer)
        self.question_choices = self.check_choice(question_choices)


class JudgeQuestion(BaseQuestion):
    def __init__(self,
                 question_sequence: Tuple[int],
                 question_body: str,
                 question_answer: bool,
                 question_chapter: str = "",
                 question_explanation=""):
        super(JudgeQuestion, self).__init__(question_sequence, question_body,
                                            question_chapter, question_explanation)
        self.question_type = QuestionType.Judge
        self.question_answer = question_answer


class CalculationQuestion(BaseQuestion):
    def __init__(self, question_sequence: Tuple[int], question_body: str,
                 question_answer: List[str],
                 question_chapter: str = "",
                 question_explanation: str = "",
                 question_related: str = ""):
        super().__init__(question_sequence, question_body, question_chapter, question_explanation)
        self.question_type = QuestionType.Calculation
        self.question_answer = question_answer
        self.question_chapter = question_chapter
        self.question_explanation = "解题：{}\n\n关联评价点：{}".format(question_explanation, question_related)
