from prompt import Prompt

template = [
    "Fixed text 1",
    "THE STRING.variable1",
    "Fixed text 2",
    "THE STRING.variable2",
    "Fixed text 3"
]

prompt = Prompt(template)

print("Initialized prompt:")
print(prompt.template)
print(prompt.variable_places)
print(prompt.variable_current)
print(prompt.variable_maximum)
print()

print("Iterating prompt:")
while True:
    result = prompt.iterate()
    if result is None:
        break
    print(result)
