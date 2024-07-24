import os
from typing import Optional

from module.process.pdf_process import TEXT_PATH
import re


class AnalysisProcessor:

    def __init__(self):
        raise RuntimeError("Error >> This class is not allowed to be instantiated!")

    @staticmethod
    def read_in_intermediate_results(input_path: str) -> Optional[str]:
        """
        Read in the intermediate results of the pdf file
        Parameters
        ----------
        input_path : str
            The path towards the storage directory of given pdf file
                Should contain the `text` directory with the `text.txt` file

        Returns the intermediate results of the pdf file in string format or None if failed
        -------

        """
        try:
            text_path = os.path.join(input_path, TEXT_PATH, "text.txt")
            with open(text_path, "r", encoding="utf-8") as f:
                return f.read()
        except:
            return None

    @staticmethod
    def read_title(intermediate: str):
        """
        Read the title of the pdf file

        Parameters
        ----------
        intermediate : str
            The intermediate results of the pdf file in string format

        Returns the title of the pdf file or None if failed
        -------

        """
        try:
            regex = re.compile(r"^(.*)\s*(.*)\s*(\d+)年(\d+)月(\d+)日", re.M)
            p = regex.match(intermediate)
            if p:
                return p.group(1), p.group(2), int(p.group(3)), int(p.group(4)), int(p.group(5))
            return None
        except:
            return None

    @staticmethod
    def read_catalog(intermediate: str) -> Optional[set]:
        """
        Read the catalog of the pdf file

        Parameters
        ----------
        intermediate : str
            The intermediate results of the pdf file in string format

        Returns the catalog of the pdf file or None if failed
        -------

        """
        data_set = set()
        try:
            regex = re.compile(r"^(\d+)\.\s(.*)\s", re.M)
            p = regex.findall(intermediate[:500])
            for item in p:
                data_set.add((int(item[0]), item[1]))
            return data_set
        except:
            return None

    @staticmethod
    def read_context(intermediate: str) -> Optional[set[int,int, str, str]]:
        """
        Read the context menu of the pdf file
        Parameters
        ----------
        intermediate : str
            The intermediate results of the pdf file in string

        Returns the context menu of the pdf file or None if failed
        -------

        """
        data_set = set()
        try:
            types = AnalysisProcessor.read_types(intermediate)
            catalog = AnalysisProcessor.read_catalog(intermediate)
            if types is None or catalog is None:
                return None
            else:
                for catalog_index, catalog_text in catalog:
                    for s1, s2, ntype in list(filter(lambda x: x[0] == catalog_index, types)):
                        data_set.add((s1, s2, catalog_text, ntype))
                return data_set
        except:
            return None

    @staticmethod
    def read_types(intermediate: str) -> Optional[set]:
        data_set = set()
        try:
            regex = re.compile(r"^(\d+)\.(\d+)\.\s*([^\d\s]+)\s", re.M)
            p = regex.findall(intermediate)
            for item in p:
                data_set.add((int(item[0]), int(item[1]), item[2]))
            return data_set
        except:
            return None
