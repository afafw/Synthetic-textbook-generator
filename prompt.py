import os


class Prompt:
    """
    A class to generate text prompts based on a given template and a set of variable text files.
    Remember that it can not deal with a sequence of string that do not have a variable constraint.
    Attributes:
        template (list): A list of strings representing the template with variable text placeholders.
        variable_places (list): A list of indices in the template where variable text placeholders are found.
        variable_current (list): A list of current indices for each variable text placeholder.
        variable_maximum (list): A list of maximum indices for each variable text placeholder.
        variable_dic (list): A list of lists containing the variable texts read from the corresponding text files.
        finished (bool): A flag indicating if all possible combinations of variable texts have been exhausted.

    Methods:
        _is_variable_text(text): Checks if a given text is a variable text placeholder.
        iterate(): Generates the next prompt by iterating through the variable texts.
    """
    def __init__(self, template):
        self.template = template
        self.variable_places = []
        self.variable_current = []
        self.variable_maximum = []
        self.variable_dic = []
        self.finished = False

        for i, text in enumerate(template):
            if self._is_variable_text(text):
                self.variable_places.append(i)
                self.variable_current.append(0)

                variable_name = text
                variable_text_file = os.path.join('constraint', f'{variable_name}.txt')
                if not os.path.exists(variable_text_file):
                    raise Exception(f"Variable text file '{variable_text_file}' not found.")

                with open(variable_text_file, 'r') as file:
                    variable_text_lines = [line.strip() for line in file.readlines()]
                    self.variable_dic.append(variable_text_lines)
                    self.variable_maximum.append(len(variable_text_lines))

    @staticmethod
    def _is_variable_text(text):
        variable_name = text
        variable_text_file = os.path.join('constraint', f'{variable_name}.txt')
        return os.path.exists(variable_text_file) if variable_name else False

    def iterate(self):
        if self.finished:
            return None
        prompt_parts = []
        last_variable_index = self.variable_places[-1] if self.variable_places else None

        for i, text in enumerate(self.template):
            if i in self.variable_places:
                var_index = self.variable_places.index(i)
                prompt_parts.append(self.variable_dic[var_index][self.variable_current[var_index]])

                if i == last_variable_index:
                    j = len(self.variable_current) - 1
                    self.variable_current[j] += 1
                    while j >= 0 and self.variable_current[j] == self.variable_maximum[j]:
                        self.variable_current[j] = 0
                        if j > 0:
                            self.variable_current[j-1] += 1
                        j -= 1
                    if j < 0:
                        self.finished = True
            else:
                prompt_parts.append(text)

        return ' '.join(prompt_parts) if any(part is not None for part in prompt_parts) else None