import sys

my_klm_dict = {"k": 248.7, "p": 452.2, "h": 994.3, "m": 2657.6, "b": 100, "d": 0}
literature_klm_dict = {"k": 0, "p": 0, "h": 0, "m": 0, "b": 0, "d": 0}  # TODO insert values from literature

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