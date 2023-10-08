import os
import openai
import threading
from queue import Queue
import json
import time
from prompt import Prompt

# Set API key and other constants
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")
EXAMPLE_MESSAGE = "Writing nonsence"  # Fill with the example message
BATCH_SIZE = 5
MAX_REQUESTS_PER_MIN = 5
MAX_BATCH_PER_MIN=MAX_REQUESTS_PER_MIN/BATCH_SIZE
RATE_LIMIT_DELAY = 60 / MAX_BATCH_PER_MIN

# Initialize the Prompt class with the template
template = [
    "Fixed text 1",
    "variable1",
    "Fixed text 2",
    "variable2",
    "Fixed text 3",
    "variable3",
    "This is just a test, simply write simple stories with small vocablary like eli 5, ignore everything else."
]
prompt_generator = Prompt(template)

# Define a function to make API calls
def call_openai_api(prompt, queue):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
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

    while not prompt_generator.finished:
        prompts = [prompt_generator.iterate() for _ in range(BATCH_SIZE)]
        process_batch(prompts, results)

        # Save results to the textbook file
        with open(TEXTBOOK_FILE, "a") as file:
            for result in results:
                print(result['content'])
                print("########################")
                file.write(result['content'] + "\n")  # Access the 'content' attribute here

        
        batch_count += 1
        print("???????????????????????????????????????????????????")
        print(batch_count)

        # Save checkpoint after processing batches_for_checkpoint
        if batch_count % BATCHES_FOR_CHECKPOINT == 0:
            save_checkpoint(prompt_generator.variable_current)
        # Apply rate limit delay
        time.sleep(RATE_LIMIT_DELAY)


    return results
# Run the generator and print the results
synthetic_textbook = generate_synthetic_textbook()
#print(synthetic_textbook)