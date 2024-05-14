import re

from tqdm import tqdm

from process.base_process import ProcessViaTika, ProcessViaFitz
from questions import *


class ProcessForSelection(ProcessViaFitz):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_regex(self):
        return re.compile(
            r"(\d+\.\d+\.\d+)\.\s+第(\d+)题([\s\S]+?)(?=A)(?:A\.)([\s\S]+?)(?=B)(?:B\.)([\s\S]+?)(?=[C正])((?:C\.)([\s\S]+?)(?=[D正]))*((?:D\.)([\s\S]+?)(?=[E正]))*((?:E\.)([\s\S]+?)(?=[F正]))*((?:F\.)([\s\S]+?)(?=[G正]))*((?:G\.)([\s\S]+?)(?=H正))*((?:H\.)([\s\S]+?)(?=I正))*((?:I\.)([\s\S]+?)(?=正))*正确答案：\s*([ABCDEFGHI]+)\s+关联评价点的名称：(.*?)\n",
            re.MULTILINE)

    def __call__(self, *args, **kwargs):

        data = self.raw_process()
        bar = tqdm(range(len(data)))
        bar.set_description("Processing Selection Questions")
        for index, (
                seq, seq_num, body, ans_a, ans_b, _, ans_c, _, ans_d, _, ans_e, _, ans_f, _, ans_g, _, ans_h, _, ans_i,
                correct_ans,
                related) in enumerate(data):
            bar.update(1)
            if not int(seq.split(".")[0]) in self.filters:
                continue
            large_chapter, mid_chapter, small_chapter = map(int, seq.split("."))
            body, ans_a, ans_b, ans_c, ans_d, ans_e, ans_f, ans_g, ans_h, ans_i = map(self.process_body,
                                                                                      [body, ans_a, ans_b, ans_c, ans_d,
                                                                                       ans_e, ans_f,
                                                                                       ans_g, ans_h, ans_i])
            q = None
            if large_chapter == 1:
                # 单选题
                if mid_chapter in self.level:
                    q = SingleChoiceQuestion((large_chapter, mid_chapter, small_chapter), body,
                                             [ans_a, ans_b, ans_c, ans_d, ans_e, ans_f, ans_g, ans_h, ans_i],
                                             correct_ans,
                                             question_explanation=related)
            elif large_chapter == 2:
                # 多选题
                if mid_chapter in self.level:
                    q = MultipleChoiceQuestion((large_chapter, mid_chapter, small_chapter), body,
                                               [ans_a, ans_b, ans_c, ans_d, ans_e, ans_f, ans_g, ans_h, ans_i],
                                               correct_ans,
                                               question_explanation=related)
            elif large_chapter == 3:
                # 判断题
                if mid_chapter in self.level:
                    correct_ans = True if correct_ans == "A" else False
                    q = JudgeQuestion((large_chapter, mid_chapter, small_chapter), body, correct_ans,
                                      question_explanation=related)
            elif large_chapter == 4:
                # 识图题
                if mid_chapter in self.level:
                    q = SingleChoiceQuestion((large_chapter, mid_chapter, small_chapter), body,
                                             [ans_a, ans_b, ans_c, ans_d, ans_e, ans_f, ans_g, ans_h, ans_i],
                                             correct_ans,
                                             question_explanation=related)
            else:
                raise RuntimeError("Error >> Unknown question type!")
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
