import random
from itertools import zip_longest

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

            for word1, word2 in self.split_list(group, 2):
                self.add_word(word1, word2)

        self.add_answers(15)

    def set_title(self, title):
        title = title + " " + str(self.page_no())
        self.set_font("helvetica", "IB", 28)
        width = self.get_string_width(title) + 6
        self.set_x((210 - width) / 2)
        self.cell(width, 10, title, new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(4)

    def add_word(self, word_data1: list, word_data2: list):
        self.set_font(size=12)
        num1, word1, part_pf_speech1, _, definition1, *_ = word_data1
        num2, word2, part_pf_speech2, _, definition2, *_ = word_data2
        col_width = self.epw / 2
        self.line += 1
        self.set_stretching(80)
        self.multi_cell(col_width, 10, txt=str(self.line) + ". " + definition1,
                        new_x="RIGHT", new_y="TOP", max_line_height=self.font_size * 1.5)
        self.line += 1
        self.multi_cell(col_width, 10, txt=str(self.line) + ". " + definition2,
                        max_line_height=self.font_size * 1.5)
        self.ln(4)

        self.add_options(word_data1, word_data2)

    def add_options(self, word_data1: list, word_data2: list):
        self.set_font(size=11)
        col_width = self.epw / 4

        def wrong_answers_for_word(word_data):
            all_speech_words = [w for w in self.speech_words[word_data[2]] if w != word_data]
            all_possible_options = list(map(self.a_word, all_speech_words))
            return random.sample(all_possible_options, 3)

        def possible_opts(word_data):
            word = word_data[1]

            wrong_answers = wrong_answers_for_word(word_data)
            possible_options = wrong_answers + [word]
            random.shuffle(possible_options)

            self.answers.append(("A", "B", "C", "D")[possible_options.index(word)])
            return possible_options

        ans_line1, ans_line2 = self.order_answers(possible_opts(word_data1), possible_opts(word_data2))

        for opt1, opt2 in ans_line1:
            self.multi_cell(col_width, txt="A) " + opt1, align="L", new_x="RIGHT", new_y="TOP")
            self.multi_cell(col_width, txt="B) " + opt2, align="L", new_x="RIGHT", new_y="TOP")
        else:
            self.ln(5)

        for opt1, opt2 in ans_line2:
            self.multi_cell(col_width, txt="C) " + opt1, align="L", new_x="RIGHT", new_y="TOP")
            self.multi_cell(col_width, txt="D) " + opt2, align="L", new_x="RIGHT", new_y="TOP")
        else:
            self.ln(5)

    def add_answers(self, n: int):
        self.set_margin(0)
        self.add_page()
        i = 0
        col_width = self.epw / n
        line_height = self.font_size * 1.5
        for row in self.split_list(self.answers, n, True):
            for ans in row:
                i += 1
                self.multi_cell(col_width, line_height, str(i) + ". " + ans, border=1, align="C",
                                new_x="RIGHT", new_y="TOP", max_line_height=self.font_size)
            self.ln(line_height)

    def has_opts(self, word: list) -> bool:
        part_of_speech = word[2]
        if part_of_speech not in self.speech_counts:
            self.speech_counts[part_of_speech] = 0
            for w in self.words:
                if w[2] == part_of_speech:
                    self.speech_counts[part_of_speech] += 1
        return self.speech_counts[part_of_speech] >= 4

    def order_answers(self, ans1: list, ans2: list):
        combined_list = list(zip(ans1, ans2))
        grouped_list = [list(g) for g in self.grouper(combined_list, 2)]
        result = [[[x for x, _ in sublist], [y for _, y in sublist]] for sublist in grouped_list]
        return result

    @staticmethod
    def split_list(my_list: list, n: int, all_items: bool = False) -> list[list]:
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
            if len(group) == n or all_items:
                grouped_list.append(group)

        return grouped_list

    @staticmethod
    def contains_item(sublist):
        return isinstance(sublist[1], str)

    @staticmethod
    def a_word(my_list):
        return my_list[1]

    @staticmethod
    def grouper(iterable, n, fillvalue=None):
        """Collect data into fixed-length chunks or blocks"""
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fillvalue)


pdf = PDF()
pdf.set_margin(3)
pdf.set_font("helvetica", "B", 14)

df = pandas.read_excel('voca.xlsx', sheet_name='Sheet1')
my_words = [list(row) for index, row in df.iterrows()]

pdf.create_test(my_words, 20)

pdf.output("word_test.pdf")
