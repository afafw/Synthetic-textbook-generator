import os


class Prompt:
    def __init__(self, template):
        self.template = template
        self.variable_places = []
        self.variable_current = []
        self.variable_maximum = []
        self.variable_dic = []

        for i, text in enumerate(template):
            if self._is_variable_text(text):
                self.variable_places.append(i)
                self.variable_current.append(0)

                variable_name = text.split(".")[1]
                variable_text_file = f'constraint/{variable_name}.txt'
                if not os.path.exists(variable_text_file):
                    raise Exception(f"Variable text file '{variable_text_file}' not found.")

                with open(variable_text_file, 'r') as file:
                    variable_text_lines = [line.strip() for line in file.readlines()]
                    self.variable_dic.append(variable_text_lines)
                    self.variable_maximum.append(len(variable_text_lines))

    @staticmethod
    def _is_variable_text(text):
        variable_name = text.split(".")[1] if '.' in text else None
        variable_text_file = f'constraint/{variable_name}.txt' if variable_name else None
        return os.path.exists(variable_text_file) if variable_name else None

    def iterate(self):
        prompt_parts = []
        last_variable_index = self.variable_places[-1] if self.variable_places else None

        for i, text in enumerate(self.template):
            if i in self.variable_places:
                var_index = self.variable_places.index(i)
                prompt_parts.append(self.variable_dic[var_index][self.variable_current[var_index]])

                if i == last_variable_index:
                    for j in range(len(self.variable_places) - 1, -1, -1):
                        self.variable_current[j] += 1

                        if self.variable_current[j] < self.variable_maximum[j]:
                            break
                        else:
                            self.variable_current[j] = 0

                            if j == 0:
                                return None
            else:
                prompt_parts.append(text)

        return ' '.join(prompt_parts) if any(part is not None for part in prompt_parts) else None