import collections
import json
import os.path
import shutil
from abc import ABC, abstractmethod
from typing import Callable, Optional

import fitz
import tika
from tika import parser
import re


class BaseProcess(ABC):
    def __init__(self, **kwargs):
        if "file" in kwargs.keys():
            self.file = kwargs["file"]
        else:
            raise RuntimeError("Error >> Fail to load file!")
        if "filter" in kwargs.keys():
            self.filters = kwargs["filter"]
        else:
            raise RuntimeError("Error >> Fail to load filter!")
        if "level" in kwargs.keys():
            self.level = kwargs["level"]
        else:
            raise RuntimeError("Error >> Fail to load level!")
        self.length = 0

        self.question_dict = collections.defaultdict(list)
        self.question_size_dict = collections.defaultdict(int)

    @abstractmethod
    def raw_process(self):
        pass

    @abstractmethod
    def get_regex(self):
        pass


class ProcessViaFitz(BaseProcess, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def raw_process(self, extra_func: Optional[Callable] = None):
        doc = fitz.open(os.path.join(os.getcwd(), "input", self.file))

        if os.path.exists("temp"):
            shutil.rmtree("temp", ignore_errors=True)
        os.mkdir("temp")

        contents = []
        global_index = 0

        for _ in enumerate(doc.pages()):

            index: int = _[0]
            page: fitz.Page = _[1]

            text_bbox_raw_list = page.get_text("blocks")
            # (x0, y0, x1, y1, "lines in the block", block_no, block_type)
            text_bbox_list = []
            for item in text_bbox_raw_list:
                content = item[4].strip()
                if not (content.startswith("国网江苏省电力有限公司") or content.startswith("当前工种") or
                        (content.startswith("第") and content.endswith("页")) or content == ""):
                    text_bbox_list.append(item)

            tuple_image = page.get_images(full=True)
            image_bbox_list = []
            # (x0, y0, x1, y1)
            for index, image in enumerate(tuple_image):
                bbox_data = page.get_image_bbox(image)
                if bbox_data.x0 > bbox_data.x1 or bbox_data.y0 > bbox_data.y1:
                    continue
                else:
                    image_bbox_list.append((global_index, bbox_data))
                    xref = image[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = "png"
                    with open(f"temp/{global_index}.{image_ext}", "wb") as f:
                        f.write(image_bytes)
                    global_index += 1

            text_bbox_list.sort(key=lambda x: x[1])
            image_bbox_list.sort(key=lambda x: x[1].y0)

            text_index = 0
            image_index = 0

            if len(image_bbox_list) == 0:
                while text_index < len(text_bbox_list):
                    contents.append(text_bbox_list[text_index][4])
                    text_index += 1
            else:

                while text_index < len(text_bbox_list) and image_index < len(image_bbox_list):
                    if text_bbox_list[text_index][1] < image_bbox_list[image_index][1].y0:
                        contents.append(text_bbox_list[text_index][4])
                        text_index += 1
                    else:
                        contents.append("<<<image{:04d}>>>".format(image_bbox_list[image_index][0]))
                        image_index += 1
                if text_index < len(text_bbox_list):
                    while text_index < len(text_bbox_list):
                        contents.append(text_bbox_list[text_index][4])
                        text_index += 1
                elif image_index < len(image_bbox_list):
                    while image_index < len(image_bbox_list):
                        contents.append("<<<image{:04d}>>>".format(image_bbox_list[image_index][0]))
                        image_index += 1
        contents = "\n".join(contents)

        if extra_func is not None:
            contents = extra_func(contents)

        if not os.path.exists("../temp"):
            os.mkdir("../temp")
        with open(os.path.join(os.getcwd(), "temp", "raw_content.txt"), "w", encoding="utf-8") as fout:
            print("Info >> Raw files dump into 'temp/raw_content.txt'...")
            fout.write(str(contents))

        contents = self.get_regex().findall(contents)
        self.length = len(contents)

        return contents

    @staticmethod
    def process_body(data: str):
        data = data.strip().replace("\n\n", "")
        return data


class ProcessViaTika(BaseProcess, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        tika.initVM()
        self.split_regex_list = [re.compile(
            r"(国\s*网\s*江\s*苏\s*省\s*电\s*力\s*有\s*限\s*公\s*司)", re.MULTILINE),
            re.compile(r"当前工种:.*\s+工种定义:.*\s+", re.MULTILINE),
            re.compile(r"第\s*\d+\s*页\s+", re.MULTILINE)]

    def raw_process(self, extra_func: Optional[Callable] = None):
        print("Warning! Tika ONLY process the texts but no images")
        parsed = parser.from_file(os.path.join(os.getcwd(), "input", self.file))
        contents = parsed["content"]

        # Remove the arts fonts
        for repl in self.split_regex_list:
            contents = repl.sub("", contents)

        if extra_func is not None:
            contents = extra_func(contents)

        if not os.path.exists("../temp"):
            os.mkdir("../temp")
        with open(os.path.join(os.getcwd(), "temp", "raw_content.txt"), "w", encoding="utf-8") as fout:
            print("Info >> Raw files dump into 'temp/raw_content.txt'...")
            fout.write(str(contents))

        contents = self.get_regex().findall(contents)
        self.length = len(contents)

        return contents

    @staticmethod
    def process_body(data: str):
        data = data.strip().replace("\n\n", "")
        return data
