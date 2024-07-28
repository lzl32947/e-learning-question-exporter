import traceback
from typing import List, Optional

from .base import BaseOutputExcel
from ..errors import CreateOutputError, OutputTypeError
from ..question import Question, QuestionType, Question_AnQuanZhunRu, Question_AnGui


class KaoShiBao:
    def __init__(self):
        pass




class KaoShiBaoExcel(BaseOutputExcel, KaoShiBao):
    def __init__(self, questions: List[Question], title: str, output_path: Optional[str] = None):
        BaseOutputExcel.__init__(self, questions, title, output_path)
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
            QuestionType.Answer: "简答题",
        }


    def write(self, q: Question, index: int):
        row = list()
        if isinstance(q,Question_AnQuanZhunRu):
            row.append(q.question)
            row.append(self.mappings[q.question_type])
            n = len(q.options)
            row.extend(q.options)
            for i in range(8-n):
                row.append("")
            row.append(q.answer)
            row.append(f"{q.order}.({q.company}): {q.source}")
            row.append("")
            row.append(q.easiness)
        elif isinstance(q,Question_AnGui):
            row.append(q.question)
            row.append(self.mappings[q.question_type])
            if q.question_type != QuestionType.Answer and q.question_type != QuestionType.Calculation:
                n = len(q.options)
                row.extend(q.options)
                for i in range(8-n):
                    row.append("")
            else:
                for i in range(8):
                    row.append("")
            row.append(q.answer)
            row.append(f"{q.order}.({q.l1}-{q.l2}-{q.question_catalog}) : {q.source}")
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
