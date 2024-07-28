import traceback
from typing import List, Optional

from .base import BaseOutputText, BaseOutputExcel
from ..errors import CreateOutputError, OutputTypeError
from ..question import Question, QuestionType, Question_AnQuanZhunRu, Question_AnGui


class XiaoBao:
    def __init__(self):
        pass




class XiaoBaoExcel(BaseOutputExcel, XiaoBao):
    def __init__(self, questions: List[Question], title: str, output_path: Optional[str] = None):
        BaseOutputExcel.__init__(self, questions, title, output_path)
        XiaoBao.__init__(self)
        self.title = ("题干（必填）", "答案", "选项 A", "选项 B", "选项 C", "选项 D","选项 E", "选项 F", "选项 G", "选项 H")
        self.mappings = {
            QuestionType.SingleChoice: "单选题",
            QuestionType.MultipleChoice: "多选题",
            QuestionType.Judge: "判断题",
            QuestionType.Calculation: "简答题",
            QuestionType.Picture: "单选题",
            QuestionType.Answer: "简答题",
        }


    def write(self, q: Question, index: int):
        row = list()
        if isinstance(q,Question_AnQuanZhunRu):
            if q.question_type == QuestionType.SingleChoice or q.question_type == QuestionType.MultipleChoice or q.question_type == QuestionType.Judge:
                row.append(q.question)
                row.append(q.answer)
                n = len(q.options)
                row.extend(q.options)
                for i in range(8-n):
                    row.append("")
        elif isinstance(q,Question_AnGui):
            if q.question_type == QuestionType.SingleChoice or q.question_type == QuestionType.MultipleChoice or q.question_type == QuestionType.Judge:
                row.append(q.question)
                row.append(q.answer)
                n = len(q.options)
                row.extend(q.options)
                for i in range(8 - n):
                    row.append("")
        else:
            raise OutputTypeError(f"The question type is not supported!, get {type(q)}!")
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
            raise CreateOutputError(traceback.format_exc())
