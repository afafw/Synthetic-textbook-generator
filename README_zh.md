# 生成合成教材

该程序根据给定的模板和一组可变文本文件生成合成教材。该程序使用 OpenAI API 生成教材的内容。

此 repo 受到 tinystories 的启发,期望提供一个简单脚本来实现简单合成教科书。

如果有任何人有比较好的模板和约束并期望开源生成结果的话可以在issue中提出，我将在力所能及的范围内代为生成。需要提供/constraint/*.txt 以及template

## 如何使用

### 第 1 步：设置您的环境

首先，您需要设置您的环境。此程序需要 Python 和几个库，包括 `os`、`openai`、`threading`、`Queue`、`json`、`time`、`pandas` 和 `fastparquet`。您可以使用 pip 安装这些库：

```python
pip install openai pandas fastparquet
```

```python
pip install -r requirements.txt
```

您还需要将 OpenAI API 密钥和基本 URL 设置为环境变量：

```bash
export OPENAI_API_KEY="your_api_key_here"
export OPENAI_API_BASE="https://api.openai.com"
```
你还需要创建对应存储变量或者结果的文件夹
```bash
mkdir constraint
mkdir result
```
### 第 2 步：准备您的模板和可变文本文件

该程序使用模板生成合成教材。模板是一个字符串列表，其中每个字符串要么是教材的固定部分，要么是可变文本的占位符。可变文本从名为 'constraint' 的目录中的文本文件中读取。每个可变文本文件应以占位符文本和 '.txt' 扩展名命名。

以下是一个模板示例：

```python
template = [
    "Now you will act as a teacher preparing for text books",
    "\n",
    "The user will provide you with a basic example of a textbook that looks well, you text book may include several instances of text similar to this text book",
    "You do not need to respond anything else as you are very focued on preparing textbook and a expert in doing so.",
    "Remember to keep your textbook on topic, to illustrate with python code and not only words, the user only provides you with a example, and you should write as long as possible to fully make your student aware how it works. topic is:",
    "variable1",
    "\nYour text book does not include the example user provided, if you feel necessary using it, you should copy it"
]
```

在此示例中，'variable1' 是可变文本的占位符。程序将在 'constraint' 目录中查找名为 'variable1.txt' 的文件，并用此文件中的文本行替换 'variable1'。

### 第 3 步：运行程序

要运行程序，您需要使用模板初始化 `Prompt` 类并调用 `generate_synthetic_textbook` 函数：

```python
prompt_generator = Prompt(template)
synthetic_textbook = generate_synthetic_textbook()
```
或者修改 `generator.py`，然后简单地运行：

```bash
python generator.py
```

`generate_synthetic_textbook` 函数生成合成教材并将其保存到 'result' 目录中名为 'textbook.parquet' 的 Parquet 文件中。在处理一定数量的批次后，该函数还将检查点保存到名为 'checkpoint.json' 的 JSON 文件中。检查点包含可变文本占位符的当前索引，如果生成过程中断，可以用于恢复生成过程。

该函数应用速率限制延迟，以避免超过每分钟 API 请求的最大数量。根据批量大小和每分钟最大请求数计算延迟：

```python
RATE_LIMIT_DELAY = 60 / MAX_BATCH_PER_MIN
```

该函数在每个批次后清除结果以节省内存。

### 第 4 步：检查结果

程序运行完成后，您可以在 'textbook.parquet' 文件中检查合成教材。您还可以检查 'checkpoint.json' 文件以查看可变文本占位符的最终索引。

### 关于示例
如果你想直接运行程序查看生成示例教材的过程，请删除result/*并将constraint/variable1.txt.example改回variable1.txt。不要忘记安装所需的包和设置环境变量。

然后运行以下命令：
```bash
python generator.py
```