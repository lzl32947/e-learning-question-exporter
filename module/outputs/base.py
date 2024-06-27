import os.path
from abc import abstractmethod, ABC
from typing import List, Optional

import openpyxl
from docx import Document

from ..question import Question

from ..utils import get_store_path


class BaseOutput(ABC):
    def __init__(self, questions: List[Question], title: str, store_path: str, output_path: Optional[str] = None):
        self.questions = sorted(questions, key=lambda x: x.question_sequence)
        self.title = title
        self.output_path = output_path
        self.store_path = store_path

    @abstractmethod
    def output(self) -> Optional[str]:
        pass

    @staticmethod
    def get_sequence(question: Question):
        return ".".join(map(str, question.question_sequence))

    @staticmethod
    def get_chapter(question: Question):
        return "{}/{}".format(question.question_raw_catalog, question.question_raw_type)


class BaseOutputText(BaseOutput):
    def __init__(self, questions: List[Question], title: str, store_path: str, output_path: Optional[str] = None, formats: str = "txt"):
        super().__init__(questions, title, store_path, output_path)
        self.output_file = os.path.join(get_store_path(self.output_path), title + f".{formats}")
        self.output_content = ""

    def save(self):
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(self.output_content)

    @abstractmethod
    def output(self) -> Optional[str]:
        pass


class BaseOutputExcel(BaseOutput):
    def __init__(self, questions: List[Question], title: str, store_path: str, output_path: Optional[str] = None):
        super().__init__(questions, title, store_path, output_path)
        self.output_file = os.path.join(get_store_path(self.output_path), title + ".xlsx")
        self.bk = openpyxl.Workbook()

    def save(self):
        self.bk.save(self.output_file)

    @abstractmethod
    def output(self) -> Optional[str]:
        pass


class BaseOutputWord(BaseOutput):
    def __init__(self, questions: List[Question], title: str, store_path: str, output_path: Optional[str] = None):
        super().__init__(questions, title, store_path, output_path)
        self.output_file = os.path.join(get_store_path(self.output_path), title + ".docx")
        self.doc = Document()

    def save(self):
        self.doc.save(self.output_file)

    @abstractmethod
    def output(self) -> Optional[str]:
        pass
