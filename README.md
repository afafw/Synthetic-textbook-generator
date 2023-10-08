# Synthetic Textbook Generator
[English](README.md) | [中文](README_zh.md)

This program is designed to generate synthetic textbooks based on a given template and a set of variable text files. The program uses the OpenAI API to generate the content of the textbook.

This repo is a simple scipt that might be able to reproduce synthetic textbook like phi or tinystories

If anyone has a better template and constraints and expects to open-source the generated results, they can propose it in the issue, and I will generate it on their behalf if I had the time(and sufficient quota). You need to provide /constraint/*.txt and template.

## How to Use

### Step 1: Set Up Your Environment

First, you need to set up your environment. This program requires Python and several libraries, including `os`, `openai`, `threading`, `Queue`, `json`, `time`, `pandas`, and `fastparquet`. You can install these libraries using pip:

```python
pip install openai pandas fastparquet
```

```python
pip install -r requirements.txt
```

You also need to set your OpenAI API key and base URL as environment variables:

```bash
export OPENAI_API_KEY="your_api_key_here"
export OPENAI_API_BASE="https://api.openai.com"
```
You also need to create folder for saving results and constraints:
```bash
mkdir constraint
mkdir result
```

### Step 2: Prepare Your Template and Variable Text Files

The program uses a template to generate the synthetic textbook. The template is a list of strings, where each string is either a fixed part of the textbook or a placeholder for variable text. The variable text is read from text files located in a directory named 'constraint'. Each variable text file should be named with the placeholder text and the '.txt' extension.

Here is an example of a template:

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

In this example, 'variable1' is a placeholder for variable text. The program will look for a file named 'variable1.txt' in the 'constraint' directory and replace 'variable1' with the lines of text in this file.

### Step 3: Run the Program

To run the program, you need to initialize the `Prompt` class with your template and call the `generate_synthetic_textbook` function:

```python
prompt_generator = Prompt(template)
synthetic_textbook = generate_synthetic_textbook()
```
Or modify the `generator.py` and simply run:

```bash
python generator.py
```

The `generate_synthetic_textbook` function generates the synthetic textbook and saves it to a Parquet file named 'textbook.parquet' in the 'result' directory. The function also saves a checkpoint to a JSON file named 'checkpoint.json' in the 'result' directory after processing a certain number of batches. The checkpoint contains the current indices of the variable text placeholders and can be used to resume the generation process if it is interrupted.

The function applies a rate limit delay to avoid exceeding the maximum number of API requests per minute. The delay is calculated based on the batch size and the maximum number of requests per minute:

```python
RATE_LIMIT_DELAY = 60 / MAX_BATCH_PER_MIN
```

The function clears the results after each batch to save memory.

### Step 4: Check the Results

After the program finishes running, you can check the synthetic textbook in the 'textbook.parquet' file. You can also check the 'checkpoint.json' file to see the final indices of the variable text placeholders.



### About example
If you want to directly run the program to view the process about how the resulting example textbook is generated. Delete result/* and rename constraint/variable1.txt.example back to variable1.txt
Do not forgot to setup requirement packages and environment variables.

Than
```bash
python generator.py
```