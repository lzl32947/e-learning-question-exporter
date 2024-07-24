from enum import Enum


class HeaderType(Enum):
    AnQuanZhunRu = ("序号", "题目名称", "单位名称", "题目类型", "难易程度", "选项", "答案", "题目来源")
    AnGui = ("序号", "一级纲要", "二级纲要", "题目分类", "题型", "题干", "选项", "答案", "题目依据", "试题分数", "试题编码", "备注", "说明")


INDEX_TYPE_MAPPINGS = {
    0: HeaderType.AnQuanZhunRu,
    1: HeaderType.AnGui,
}
