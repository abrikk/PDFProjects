import copy
import random

import pandas
from fpdf import FPDF


class PDF(FPDF):
    words = []
    speech_words = {}
    speech_counts = {}
    line = 0
    answers = []

    def create_test(self, words: list, n: int = 10, title: str = "Day"):
        self.words = [word for word in words if isinstance(word[1], str)]
        self.words = list(filter(self.has_opts, self.words))

        for word_data in self.words:
            num, word, part_of_speech, _, definition, *_ = word_data
            if part_of_speech not in self.speech_words:
                self.speech_words[part_of_speech] = []
            self.speech_words[part_of_speech].append(word_data)

        for group in self.split_list(self.words, n):
            self.add_page()
            self.set_title(title)

            for word in group:
                self.add_word(word)

        print(self.answers)
        self.add_answers(20)

    def set_title(self, title):
        title = title + " " + str(self.page_no())
        self.set_font("helvetica", "IB", 28)
        width = self.get_string_width(title) + 6
        self.set_x((210 - width) / 2)
        self.cell(width, 10, title, new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(4)

    def add_word(self, word_data: list):
        self.line += 1
        self.set_font(size=12)
        num, word, part_pf_speech, _, definition, *_ = word_data
        self.multi_cell(self.epw, txt=str(self.line) + ". " + definition)
        self.ln(2)
        self.add_options(word, part_pf_speech, word_data)

    def add_options(self, word: str, part_of_speech: str, word_data: list):
        all_speech_words = copy.deepcopy(self.speech_words[part_of_speech])
        all_speech_words.remove(word_data)
        all_possible_options = list(map(self.a_word, all_speech_words))
        possible_options = random.sample(all_possible_options, 3) + [word]
        random.shuffle(possible_options)

        self.answers.append(("A", "B", "C", "D")[possible_options.index(word)])

        a, b, c, d = possible_options
        col_width = pdf.epw / 2

        for left, right in self.split_list(list(zip(["A)", "B)", "C)", "D)"], [a, b, c, d])), 2):
            pdf.cell(col_width, txt=left[0] + " " + left[1], new_x="RIGHT", new_y="TOP")
            pdf.cell(col_width, txt=right[0] + " " + right[1], new_x="RIGHT", new_y="TOP")
            pdf.ln(5)

    def add_answers(self, n: int):
        self.add_page()
        col_width = pdf.epw / n
        line_height = pdf.font_size * 1.5
        for row in self.split_list(self.answers, n):
            for ans in row:
                pdf.multi_cell(col_width, line_height, ans, border=1, align="C",
                               new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
            pdf.ln(line_height)

    @staticmethod
    def split_list(my_list: list, n: int) -> list[list]:
        """
        Split a list into groups of a specified size.
        Any remaining elements that do not form a full group are ignored.

        Parameters:
        my_list (list[int]): The list to be split.
        n (int): The size of each group.

        Returns:
        list[list[int]]: A list of lists, where each inner list represents a group.
        """
        grouped_list = []
        for i in range(0, len(my_list), n):
            group = my_list[i:i + n]
            if len(group) == n:
                grouped_list.append(group)
        return grouped_list

    def has_opts(self, word: list) -> bool:
        part_of_speech = word[2]
        if part_of_speech not in self.speech_counts:
            self.speech_counts[part_of_speech] = 0
            for w in self.words:
                if w[2] == part_of_speech:
                    self.speech_counts[part_of_speech] += 1
        return self.speech_counts[part_of_speech] >= 4

    @staticmethod
    def contains_item(sublist):
        return isinstance(sublist[1], str)

    @staticmethod
    def a_word(my_list):
        return my_list[1]


pdf = PDF()
pdf.set_margin(3)
pdf.set_font("helvetica", "B", 14)

df = pandas.read_excel('voca.xlsx', sheet_name='Sheet1')
my_words = [list(row) for index, row in df.iterrows()]

pdf.create_test(my_words, 10)

pdf.output("word_test.pdf")
