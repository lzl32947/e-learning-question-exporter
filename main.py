import os

from module import PDFProcessor, AnalysisProcessor

import sys

from module import QuestionFactory, KaoShiBaoExcel
from module.output import KaoShiBaoWord

sys.path.append(os.path.join(os.path.dirname(__file__)))
if __name__ == '__main__':
    pdf_processor = PDFProcessor.read_in_raw_pdf("input/电力电缆安装运维工（输电）-2024年05月17日机考题库.pdf", override=True)
    inter = AnalysisProcessor.read_in_intermediate_results(pdf_processor)
    context = AnalysisProcessor.read_context(inter)
    questions = []
    for s1, s2, catalog, ntype in context:
        if s2 == 1:
            questions.extend(QuestionFactory.create(inter, s1, s2, catalog, ntype))
    a = KaoShiBaoWord(questions, "电力电缆安装运维工（输电）", pdf_processor).output()

    print(a)
