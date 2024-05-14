import importlib
import json
import os.path

from base_output import OutputExcel2KaoShiBao, OutputWord2KaoShiBao

TARGET_CONFIG = "营销-核算账务收费员（初中高）"  # Change this to the config file you want to use

OUTPUT_TYPE = OutputWord2KaoShiBao  # Change this to the output type you want to use

if __name__ == '__main__':
    assert os.path.exists("config")

    if not os.path.exists("output"):
        os.mkdir("output")

    target_file = os.path.join("config", TARGET_CONFIG + ".json")

    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as fin:
            config_raw = json.load(fin)
            process = config_raw["process"]
    else:
        raise RuntimeError("Error >> Config not found!")

    outputs = OUTPUT_TYPE(config_raw["title"])

    for single_process in process:
        lib = importlib.import_module("process")
        if hasattr(lib, single_process["process"]):
            _ = getattr(lib, single_process["process"])
            target = _(**{"file": config_raw["file"], "filter": single_process["filter"],
                          "level": config_raw["level"]})
            target()
            outputs.append(target)
        else:
            raise RuntimeError(
                "Error >> Process not found! Please check whether it has been registered in __init__.py!")
    outputs.write()
