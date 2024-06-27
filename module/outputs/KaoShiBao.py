import os.path
import re
import traceback
from typing import List, Optional

from .base import BaseOutputExcel, BaseOutputWord
from ..process import PLACEHOLDER_RE, PLACEHOLDER_RE_TUPLE, IMAGE_PATH
from ..question import Question, QuestionType, SingleChoiceQuestion, MultipleChoiceQuestion, JudgeChoiceQuestion, CalculationQuestion, PictureChoiceQuestion


class KaoShiBao:
    def __init__(self):
        pass


class KaoShiBaoWord(BaseOutputWord, KaoShiBao):

    def __init__(self, questions: List[Question], title: str, store_path: str, output_path: Optional[str] = None):
        BaseOutputWord.__init__(self, questions, title, store_path, output_path)
        KaoShiBao.__init__(self)
        self.mappings = {
            QuestionType.SingleChoice: "单选题",
            QuestionType.MultipleChoice: "多选题",
            QuestionType.Judge: "判断题",
            QuestionType.Calculation: "问答题",
            QuestionType.Picture: "单选题",
        }

    def create_explanation(self, q: Question) -> str:
        if isinstance(q, CalculationQuestion):
            return f"原题目({self.get_sequence(q)})  解题方法为({q.question_explanation}) 关联评价点为({q.question_related})"
        elif isinstance(q, SingleChoiceQuestion) or isinstance(q, MultipleChoiceQuestion) or isinstance(q, PictureChoiceQuestion) or isinstance(q, JudgeChoiceQuestion):
            return f"原题目({self.get_sequence(q)})  关联评价点({q.question_related})"
        return ""

    def write_paragraph(self, content: str):
        body = re.split("(" + PLACEHOLDER_RE + ")", content)
        for i in body:
            p = re.match(PLACEHOLDER_RE_TUPLE, i)
            if p:
                image_id = p.group(1)
                self.doc.add_picture(os.path.join(self.store_path, IMAGE_PATH, f"{image_id}.png"))
            else:
                self.doc.add_paragraph(i)

    def write(self, q: Question, index: int):
        # self.write_paragraph(self.mappings[q.question_type])
        self.write_paragraph(f"{index}、{q.question_body}")
        if isinstance(q, SingleChoiceQuestion) or isinstance(q, MultipleChoiceQuestion) or isinstance(q, PictureChoiceQuestion) or isinstance(q, JudgeChoiceQuestion):
            for i in range(8):
                if i > len(q.question_selections) - 1:
                    break
                self.write_paragraph(f"{chr(65 + i)}、{q.question_selections[i]}")
        self.write_paragraph(f"答案：{q.question_answer}")
        self.write_paragraph(f"解析：{self.create_explanation(q)}")
        self.write_paragraph(f"章节：{self.get_chapter(q)}")
        self.doc.add_paragraph("\n")

    def output(self) -> Optional[str]:
        try:
            for index, q in enumerate(self.questions):
                if q.question_type in self.mappings.keys():
                    self.write(q, index + 1)
            self.save()
            return self.output_file
        except Exception as e:
            traceback.print_exc()
            return None


class KaoShiBaoExcel(BaseOutputExcel, KaoShiBao):
    def __init__(self, questions: List[Question], title: str, store_path: str, output_path: Optional[str] = None):
        BaseOutputExcel.__init__(self, questions, title, store_path, output_path)
        KaoShiBao.__init__(self)
        self.title = ("题干（必填）", "题型 （必填）", "选项 A", "选项 B", "选项 C", "选项 D",
                      "选项E(勿删)", "选项F(勿删)", "选项G(勿删)", "选项H(勿删)", "正确答案（必填）", "解析（勿删）",
                      "章节（勿删）", "难度")
        self.mappings = {
            QuestionType.SingleChoice: "单选题",
            QuestionType.MultipleChoice: "多选题",
            QuestionType.Judge: "判断题",
            QuestionType.Calculation: "简答题",
            QuestionType.Picture: "单选题",
        }

    def create_explanation(self, q: Question) -> str:
        if isinstance(q, CalculationQuestion):
            return f"原题目: {self.get_sequence(q)}\n解题: {q.question_explanation}\n关联评价点: {q.question_related}"
        elif isinstance(q, SingleChoiceQuestion) or isinstance(q, MultipleChoiceQuestion) or isinstance(q, PictureChoiceQuestion) or isinstance(q, JudgeChoiceQuestion):
            return f"原题目: {self.get_sequence(q)}\n关联评价点: {q.question_related}"
        return ""

    def write(self, q: Question, index: int):
        row = list()
        row.append(q.question_body)
        row.append(self.mappings[q.question_type])

        if isinstance(q, SingleChoiceQuestion) or isinstance(q, MultipleChoiceQuestion) or isinstance(q, PictureChoiceQuestion) or isinstance(q, JudgeChoiceQuestion):
            for index in range(8):
                row.append(q.question_selections[index] if index < len(q.question_selections) else "")
            correct_ans = "".join([i for i in q.question_answer if i in ["A", "B", "C", "D", "E", "F", "G", "H"]])
            row.append(correct_ans)
        elif isinstance(q, CalculationQuestion):
            row.extend(["" for _ in range(8)])
            row.append(q.question_answer)
        row.append(self.create_explanation(q))
        row.append(self.get_chapter(q))
        # Remove all images since Excel cannot display them
        row = ["".join(re.split(PLACEHOLDER_RE, i)) for i in row]
        self.bk.active.append(row)

    def output(self) -> Optional[str]:
        try:
            self.bk.active.append(self.title)
            for index, q in enumerate(self.questions):
                if q.question_type in self.mappings.keys():
                    self.write(q, index + 1)
            self.save()
            return self.output_file
        except Exception as e:
            traceback.print_exc()
            return None
