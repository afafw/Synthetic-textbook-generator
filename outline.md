1. Define the prompt:
   - Constraints or requirements for the generated text

2. Set the vocabulary:
   - Create a fixed vocabulary of diverse words related to the textbook topic

3. Generate the text:
   - Initialize the generated text as an empty string
   - Start with the prompt
   - For each iteration:
     - Put the zero-shot example at the very first place
     - Inject randomness into the prompt by including a random subset of words from the vocabulary
     - Generate new text using GPT-3.5 Turbo based on the modified prompt
     - Add the generated text to the overall generated text

5. Ensure diversity:
   - Use constraints on topics and target audience for each iteration of generating text
   - Specify different topics or target audiences to promote diversity


6. Output the generated synthetic textbook:
   - Save the generated text to a file or present it in a suitable format for further use

