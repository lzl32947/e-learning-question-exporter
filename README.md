# E学堂技能等级导出工具

本项目包含解析技能等级赛题库`PDF`文件的脚本。

[English Ver. Document](README.EN.md)

## 依赖

请使用下列命令安装依赖：

```bash
python -m pip install -r requirements.txt
```

## 使用

### 修改`main.py`

* 修改`main.py`中的`TARGET_CONFIG`项为`config`文件夹下的配置文件名（请不要带上`.json`后缀）
* 修改`main.py`中的`OUTPUT_TYPE`项为导出文件的方法，目前支持`OutputExcel2KaoShiBao`和`OutputWord2KaoShiBao`
  两种方法，分别对应`考试宝`软件的两种题目导入模板。

### 运行

运行`main.py`即可。

```bash
python main.py
```

导出的文件将会保存在`output`文件夹下，并以`config`文件中的`title`项命名。

## 配置项

### 创建配置文件
关于配置文件的创建，请参考`config`文件夹下的[说明](config/README.md)。

### 代码配置
#### PDF解析

`PDF`文件的解析共有两种类库:
* `pymupdf`（`fitz`）：更全面的解析，支持解析图片，适合没有图片的文件
* `tika`：基于`Java`的解析，仅支持解析文字

二者分别对应`ProcessViaTika`类及`ProcessViaFitz`类，您可以在`process/base_process.py`中找到两类的实现。

默认情况下使用`ProcessViaFitz`类以支持图片解析。

#### 导出

导出的文件类型有两种：

* `OutputExcel2KaoShiBao`：导出为`考试宝`软件的`Excel`模板，解析准确但是不支持图片
* `OutputWord2KaoShiBao`：导出为`考试宝`软件的`Word`模板，由于`Word`的排版问题，解析可能不准确并需要再上传题库时手动调整，但支持图片的上传

请按需选择，并在`main.py`中修改`OUTPUT_TYPE`项以切换。

## 已知问题
1. 导出的`Word`模板在选项仅有图片时在上传题库过程中会出现解析错误，类似于:
  ![known_issue_1.png](doc/image/known_issue_1.png)
  此时，需要在题库导入页面中手动将图像文件复制到对应选项框中。
2. 由于`考试宝`软件对`Word`模板的解析问题，导出的`Word`模板在上传题库过程中可能会出现解析错误，常见选项错位等问题，此时需要手动调整。
  例如：
  ```html
    1. 以下关于装置的说法，正确的是（ ）
    A. 会产生10A的交流电
    B. 会产生100A的交流电
    C. 会产生1000A的交流电
  ```
  此时，再导入`考试宝`时，由于其对`Word`模板的会解析题目中的`A`、`B`、`C`等字母，导致选项错位，如无人工介入会变成：
  ```html
    1. 以下关于装置的说法，正确的是（ ）
    A. 会产生10
    B. 的交流电
    C. 会产生100
    D. 的交流电
    E. 会产生1000
    F. 的交流电
  ```
  这种情况是由于该软件平台造成的，目前无法自动解决，需要手动调整。
  
## 其他

欢迎PR并提出建议，也欢迎提出各类`Issue`。
