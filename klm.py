import sys

# Values of the KLM operators from the literature:
# Kieras, D. (2001). Using the keystroke-level model to estimate execution times. University of Michigan, 555.
# Card, S. K., Moran, T. P., & Newell, A. (1980). The keystroke-level model for user performance time with interactive systems. Communications of the ACM, 23(7), 396-410.
# Used Keystroke-time for average skilled typist.
my_klm_dict = {"k": 248.7, "p": 452.2, "h": 994.3, "m": 2657.6, "b": 100, "d": 0}
literature_klm_dict = {"k": 200, "p": 1100, "h": 400, "m": 1200, "b": 100, "d": 0}

operators = "kphmbd"
numbers = "1234567890"


class KLMPredictor:
    lines = ""

    def __init__(self):
        super().__init__()
        self.parse_file()

    def parse_file(self):
        if len(sys.argv) < 2:
            sys.stderr.write("Please pass a .txt file with KLM operators as argument!")
            sys.exit()

        filepath = sys.argv[1]
        try:
            with open(filepath) as f:
                self.lines = f.readlines()
        except FileNotFoundError:
            sys.stderr.write("File not found! Please check your arguments!")
            sys.exit()

    def predict(self):
        predicted_time_our_model = 0
        predicted_time_literature_model = 0
        current_number_modifiers = []
        for line in self.lines:
            line = line.lower()
            for char in line:

                # once a comment starts, the rest of the line can be ignored
                if char == "#":
                    break

                # skip spaces
                if char == " ":
                    continue

                # check for numeric modifiers
                if char in numbers:
                    current_number_modifiers.append(char)

                # finally, check for operators
                elif char in operators:
                    multiplier = self.get_multiplier(current_number_modifiers)
                    predicted_time_our_model += multiplier * my_klm_dict.get(char)
                    predicted_time_our_model += multiplier * literature_klm_dict.get(char)
                    current_number_modifiers.clear()

        print("Predicted time (our model): " + str(predicted_time_our_model) + " ms")
        print("Predicted time (literature  model): " + str(predicted_time_literature_model) + " ms")

    def get_multiplier(self, number_list):
        """
        Returns numeric modifiers from the string as int
        """
        number_as_string = ""
        for number in number_list:
            number_as_string += str(number)

        return int(number_as_string) if number_as_string != "" else 1


if __name__ == "__main__":
    predictor = KLMPredictor()
    predictor.predict()
