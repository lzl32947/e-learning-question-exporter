# Configuration Folder

This folder stores all the configuration files for the export items. The format of the configuration files is `json`.

Please note that the configuration files here are not the latest, which means you might not be able to use them directly. In this case, you can recreate the configuration files by following the steps below.

## Creating Configuration Files

You need to follow these steps to create a configuration file:

1. Create a new `json` file with the name of your export item, for example, `example.json`.
2. Fill in the configuration information in the file as needed. An example configuration format is as follows. (Please note: `json` format does not support comments, so please delete any comment items starting with `//` before saving the configuration file)
    ```json
    {
      "process": [  // Processing steps
        {
          "process": "ProcessForSelection", // Call ProcessForSelection to handle multiple choice and true/false questions
          "filter": [  // Filters; in this file, chapters 1, 2, 3, and 4 are multiple choice and true/false questions
            1,
            2,
            3,
            4
          ]
        },
        {
          "process": "ProcessForCalculation", // Call ProcessForCalculation to handle calculation questions
          "filter": [ // Filters; in this file, chapter 5 is calculation questions
            5
          ]
        }
      ],
      "file": "继电保护员（220kV及以下）-2024年02月27日机考题库.pdf",  // File name; the file should be located in the `input` folder
      "type": "二次", // File type; this field is used to distinguish topics under different major categories
      "title": "继电保护员（220kV及以下）（初中高）", // Title of the export item
      "level": [ // Levels of the export item; generally, 1 is for primary workers, 2 for intermediate workers, 3 for advanced workers, 4 for technicians, and so on. However, some majors may have intermediate workers starting at level 1, so please pay attention when creating the configuration file.
        1,
        2,
        3
      ]
    }
    ```