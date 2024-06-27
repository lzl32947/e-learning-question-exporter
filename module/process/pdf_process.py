import os.path
from typing import Optional
import fitz
import hashlib

from ..utils import STORE_PATH

PLACEHOLDER = "<<<image{:04d}>>>"
PLACEHOLDER_RE = r"<<<image\d+>>>"
PLACEHOLDER_RE_TUPLE = r"<<<image(\d+)>>>"

TEXT_PATH = "text"
IMAGE_PATH = "image"


def cal_md5(file_path: str) -> Optional[str]:
    """
    Calculate the md5 hash value of the file
    Parameters
    ----------
    file_path : str
        The path of the file

    Returns the md5 hash value of the file
    -------

    """
    try:
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None


class PDFProcessor:
    def __init__(self):
        raise RuntimeError("Error >> This class is not allowed to be instantiated!")

    @staticmethod
    def read_in_raw_pdf(file_path: str, override: bool = False) -> Optional[str]:
        """
        Read in the raw pdf file and store the text and the images, returning the path to the storage directory
        Parameters
        ----------
        file_path : str
            The path of the pdf file
        override : bool
            Whether to override the existing storage directory

        Returns the storage path of the pdf file
        -------

        """
        try:
            md5 = cal_md5(file_path)
            if md5 is None:
                return None
            else:
                doc = fitz.open(file_path)

                storage_path = os.path.join(STORE_PATH, md5)
                if os.path.exists(storage_path) and not override:
                    return storage_path
                else:
                    os.makedirs(storage_path, exist_ok=True)
                    global_index = 0
                    contents = []
                    image_lists = []

                    for _ in enumerate(doc.pages()):
                        index: int = _[0]
                        page: fitz.Page = _[1]

                        text_bbox_raw_list = page.get_text("blocks")
                        # In format of the followings:
                        # (x0, y0, x1, y1, "lines in the block", block_no, block_type)
                        text_bbox_list = []
                        for item in text_bbox_raw_list:
                            content = item[4].strip()

                            # Filter out the unnecessary contents
                            if not (content.startswith("国网江苏省电力有限公司") or content.startswith("当前工种") or
                                    (content.startswith("第") and content.endswith("页")) or content == ""):
                                text_bbox_list.append(item)

                        # Extract the images
                        tuple_image = page.get_images(full=True)
                        image_bbox_list = []
                        # In format of the followings:
                        # (x0, y0, x1, y1)
                        for index, image in enumerate(tuple_image):
                            bbox_data = page.get_image_bbox(image)
                            # Filter out the invalid bbox data
                            if bbox_data.x0 > bbox_data.x1 or bbox_data.y0 > bbox_data.y1:
                                continue
                            else:
                                # Get the image
                                image_bbox_list.append((global_index, bbox_data))
                                xref = image[0]
                                base_image = doc.extract_image(xref)
                                image_bytes = base_image["image"]
                                image_ext = "png"
                                image_lists.append((global_index, image_bytes, image_ext))
                                global_index += 1

                        # Arrange the text and the images by the y0 coordinate
                        text_bbox_list.sort(key=lambda x: x[1])
                        image_bbox_list.sort(key=lambda x: x[1].y0)

                        #########################################################
                        # Prerequisite : There is only one image in one row
                        # This program relays on the y0 coordinate to arrange the text and the images,
                        # which indicates that if there are multiple images in one row, the program will not work properly
                        #########################################################

                        text_index = 0
                        image_index = 0

                        # Merge the text and the images
                        if len(image_bbox_list) == 0:
                            while text_index < len(text_bbox_list):
                                contents.append(text_bbox_list[text_index][4])
                                text_index += 1
                        else:
                            # Add the placeholder for the images
                            while text_index < len(text_bbox_list) and image_index < len(image_bbox_list):
                                if text_bbox_list[text_index][1] < image_bbox_list[image_index][1].y0:
                                    contents.append(text_bbox_list[text_index][4])
                                    text_index += 1
                                else:
                                    contents.append(PLACEHOLDER.format(image_bbox_list[image_index][0]))
                                    image_index += 1
                            if text_index < len(text_bbox_list):
                                while text_index < len(text_bbox_list):
                                    contents.append(text_bbox_list[text_index][4])
                                    text_index += 1
                            elif image_index < len(image_bbox_list):
                                while image_index < len(image_bbox_list):
                                    contents.append(PLACEHOLDER.format(image_bbox_list[image_index][0]))
                                    image_index += 1
                    contents = "\n".join(contents)

                    # Store the text and the images
                    os.makedirs(os.path.join(storage_path, TEXT_PATH), exist_ok=True)
                    with open(os.path.join(storage_path, TEXT_PATH,"text.txt"), "w", encoding="utf-8") as f:
                        f.write(contents)

                    os.makedirs(os.path.join(storage_path, IMAGE_PATH), exist_ok=True)
                    for index, image_bytes, image_ext in image_lists:
                        with open(os.path.join(storage_path, IMAGE_PATH, "{:04d}.{}".format(index, image_ext)), "wb") as f:
                            f.write(image_bytes)
                return storage_path
        except:
            return None
