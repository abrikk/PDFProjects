from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            self.set_font("helvetica", "B", 28)
            width = self.get_string_width(self.title) + 6
            self.set_x((210 - width) / 2)
            self.cell(width, 10, self.title, new_x="LMARGIN", new_y="NEXT", align="C")
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_word(self, word_info: list):
        self.set_font("helvetica", size=16)
        no, word, part_of_speech, lvl, defin, synon = word_info

        if isinstance(word, float):
            return

        if self.will_page_break(16):
            self.add_page()

        self.cell(txt=str(no) + ".")

        self.set_font(style="B")
        self.cell(txt=word.capitalize())

        self.set_font(style="")

        txt = "({part_of_speech}) {lvl}- {defin}. (synonyms: {synon})".format(
            part_of_speech=part_of_speech,
            lvl="(" + lvl + ") " if not isinstance(lvl, float) else "",
            defin=defin.encode("windows-1252").decode("latin-1"),
            synon=synon)

        self.write(txt=txt, print_sh=True)
        self.ln(12)
