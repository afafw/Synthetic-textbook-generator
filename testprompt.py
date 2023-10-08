from prompt import Prompt
import time
template = [
    "Now you will act as a teacher preparing for text books",
    "\n",
    "The user will provide you with a basic example of a textbook that looks well, you text book may include several instances of text similar to this text book",
    "You do not need to respond anything else as you are very focued on preparing textbook and a expert in doing so.",
    "Remember to keep your textbook on topic, to illustrate with python code and not only words, the user only provides you with a example, and you should write as long as possible to fully make your student aware how it works. topic is:",
    "variable1",
    "\nYour text book does not include the example user provided, if you feel necessary using it, you should copy it"
]
prompt = Prompt(template)

print("Initialized prompt:")
print(prompt.template)
print(prompt.variable_places)
print(prompt.variable_current)
print(prompt.variable_maximum)
print()

print("Iterating prompt:")
#time.wait(30)
while True:
    result = prompt.iterate()
    if result is None:
        break
    print(result)
