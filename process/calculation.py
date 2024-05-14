import re

from tqdm import tqdm

from process.base_process import ProcessViaTika, ProcessViaFitz
from questions import CalculationQuestion


class ProcessForCalculation(ProcessViaFitz):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_regex(self):
        return re.compile(
            r"(\d+\.\d+\.\d+)\.\s*第(\d+)题\s([\s\S]*?)正确答案：(.*?)[，,]\s+教师详解：([\s\S]*?)关联评价点的名称：(.*?)\s",
            re.MULTILINE)

    @staticmethod
    def split_calculation_body(body: str):
        return re.split(r"\d\. 计算题",body)[-1]

    def __call__(self, *args, **kwargs):
        data = self.raw_process(self.split_calculation_body)
        bar = tqdm(range(len(data)))
        bar.set_description("Processing Calculation Questions")
        for index, (seq, seq_num, body, ans, explain, related) in enumerate(data):
            bar.update(1)
            if not int(seq.split(".")[0]) in self.filters:
                continue
            large_chapter, mid_chapter, small_chapter = map(int, seq.split("."))
            body, explain, related = map(self.process_body,
                                         [body, explain, related])
            q = None
            if mid_chapter in self.level:
                q = CalculationQuestion((large_chapter, mid_chapter, small_chapter), body,
                                        ans,
                                        question_explanation=explain, question_related=related)

            if q is not None:
                self.question_dict[(large_chapter, mid_chapter)].append(q)
                self.question_size_dict[(large_chapter, mid_chapter)] = max(
                    self.question_size_dict[(large_chapter, mid_chapter)], small_chapter)
        bar.close()
        for key in self.question_dict.keys():
            if len(self.question_dict[key]) == self.question_size_dict[key]:
                print("Info >> Process Chapter {}-{} finished.".format(key[0], key[1]))
            else:
                ts = set([i for i in range(1, self.question_size_dict[key] + 1)]).difference(
                    set([q.question_sequence[-1] for q in self.question_dict[key]])
                )
                for item in ts:
                    print("Warning >> Chapter {}-{} missing question {}".format(key[0], key[1], item))
