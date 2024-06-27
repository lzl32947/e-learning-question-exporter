from typing import Union, Callable, List

from ..question import SingleChoiceQuestion, MultipleChoiceQuestion, JudgeChoiceQuestion, PictureChoiceQuestion, CalculationQuestion, Question

QUESTION_TYPE_MAPPINGS = {
    "单选题": SingleChoiceQuestion,
    "多选题": MultipleChoiceQuestion,
    "判断题": JudgeChoiceQuestion,
    "计算题": CalculationQuestion,
    "识图题": PictureChoiceQuestion,
}


class QuestionFactory:
    def __init__(self):
        raise RuntimeError("Error >> This class is not allowed to be instantiated!")

    @staticmethod
    def create(intermediate: str, s1: int, s2: int, catalog: str, ntype: str) -> List[Question]:
        if catalog in QUESTION_TYPE_MAPPINGS.keys():
            catalog_callable = QUESTION_TYPE_MAPPINGS[catalog]
        else:
            raise ValueError("Error >> Unknown question type: {}".format(catalog))
        if not hasattr(catalog_callable, "create"):
            raise ValueError("Error >> The catalog must have the method 'match_text'!")
        questions = catalog_callable.create(intermediate, s1, s2, catalog, ntype)
        return questions
