import os
import openai
import threading
from queue import Queue
import json
import time
from prompt import Prompt
import pandas as pd
from fastparquet import ParquetFile, write
# Set API key and other constants
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
EXAMPLE_MESSAGE = """To begin, let us define singular and nonsingular matrices. A matrix is said to be singular if its
determinant is zero. On the other hand, a matrix is said to be nonsingular if its determinant is not
zero. Now, let's explore these concepts through examples.
Example 1: Consider the matrix A = np.array([[1, 2], [2, 4]]). We can check if this matrix is
singular or nonsingular using the determinant function. We can define a Python function, `is_singular(A)`, which returns true if the determinant of A is zero, and false otherwise.
import numpy as np
def is_singular(A):
    det = np.linalg.det(A)
    if det == 0:
        return True
    else:
        return False

A = np.array([[1, 2], [2, 4]])
print(is_singular(A)) # True
"""
BATCH_SIZE = 5
MAX_REQUESTS_PER_MIN = 5
MAX_BATCH_PER_MIN=MAX_REQUESTS_PER_MIN/BATCH_SIZE
RATE_LIMIT_DELAY = 60 / MAX_BATCH_PER_MIN

# Initialize the Prompt class with the template
template = [
    "Now you will act as a teacher preparing for text books",
    "\n",
    "The user will provide you with a basic example of a textbook that looks well, you text book may include several instances of text similar to this text book",
    "You do not need to respond anything else as you are very focued on preparing textbook and a expert in doing so.",
    "Remember to keep your textbook on topic, to illustrate with python code and not only words, the user only provides you with a example, and you should write as long as possible to fully make your student aware how it works. topic is:",
    "variable1",
    "\nYour text book does not include the example user provided, if you feel necessary using it, you should copy it"
]
prompt_generator = Prompt(template)

# Define a function to write data to a Parquet file
def write_to_parquet(data, file_name, max_file_size):
    # Convert data to a DataFrame
    df = pd.DataFrame({'content': [data]})  # Wrap the data in a list

    # Check if the file exists
    if os.path.exists(file_name):
        # Check the size of the current file
        file_size = os.path.getsize(file_name)

        # If the file size exceeds the maximum size, create a new file
        if file_size >= max_file_size:
            # Extract the base file name and extension
            base_name, extension = os.path.splitext(file_name)

            # Create a new file name
            file_name = f"{base_name}_1{extension}"
    else:
        # Create an empty Parquet file with the appropriate schema
        empty_df = pd.DataFrame(columns=['content'])
        write(file_name, empty_df)

    # Write the DataFrame to a Parquet file
    write(file_name, df, append=True)

    return file_name
# Define a function to make API calls
def call_openai_api(prompt, queue):
    #print(prompt)
    #print("###########")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": EXAMPLE_MESSAGE},
        ],
    )
    queue.put(completion.choices[0].message)

# Define a function to process a batch of prompts
def process_batch(prompts, results):
    threads = []
    queue = Queue()

    for prompt in prompts:
        thread = threading.Thread(target=call_openai_api, args=(prompt, queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    while not queue.empty():
        results.append(queue.get())

# Checkpoint and result file paths
CHECKPOINT_FILE = "result/checkpoint.json"
TEXTBOOK_FILE = "result/textbook.txt"
BATCHES_FOR_CHECKPOINT = 1

# Function to save checkpoint
def save_checkpoint(variable_current):
    with open(CHECKPOINT_FILE, "w") as file:
        json.dump({"variable_current": variable_current}, file)

# Function to load checkpoint
def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as file:
            data = json.load(file)
            return data["variable_current"]
    return None

# Modified main function to generate synthetic textbook
def generate_synthetic_textbook():
    results = []
    checkpoint_data = load_checkpoint()
    if checkpoint_data:
        prompt_generator.variable_current = checkpoint_data
    batch_count = 0
    max_file_size = 383 * 1024 * 1024  # Maximum file size in bytes
    parquet_file = "result/textbook.parquet"  # Initial Parquet file

    while not prompt_generator.finished:
        prompts = [prompt_generator.iterate() for _ in range(BATCH_SIZE)]
        
        # Filter out None prompts and stop if all prompts are None
        prompts = [prompt for prompt in prompts if prompt is not None]

        process_batch(prompts, results)

        # Save results to the Parquet file
        for result in results:
            parquet_file = write_to_parquet(result['content'], parquet_file, max_file_size)

        batch_count += 1
        #print the batch that is processing
        print(batch_count)

        # Save checkpoint after processing batches_for_checkpoint
        if batch_count % BATCHES_FOR_CHECKPOINT == 0:
            save_checkpoint(prompt_generator.variable_current)

        # Apply rate limit delay
        time.sleep(RATE_LIMIT_DELAY)
        results.clear()

    return results
# Run the generator and print the results
synthetic_textbook = generate_synthetic_textbook()
#print(synthetic_textbook)