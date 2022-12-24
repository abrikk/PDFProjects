from fpdf import FPDF
import pandas as pd
import datetime


class PDF(FPDF):
    month: int = datetime.date.today().month  # default month
    year: int = datetime.date.today().year  # default year

    def __init__(self,
                 orientation="portrait",
                 unit="mm",
                 format="A4",
                 tasks=None,
                 txt_width=80,
                 line_height=10
                 ):
        super().__init__(orientation, unit, format)
        self.tasks = tasks or []  # daily tasks to do
        self.txt_width = txt_width  # width of the first column. default 80 mm
        self.line_height = line_height  # height of the line. default 10 mm

        self.set_margin(0)

    def add_columns(self, day_width, days_in_month):
        self.set_font("helvetica", "", 10)
        for d in range(1, days_in_month + 1):
            self.multi_cell(day_width, self.line_height, str(d), border=1, align="C",
                            new_x="RIGHT", new_y="TOP", max_line_height=self.font_size)
        self.ln()

    def add_rows(self, day_width, days_in_month):
        tasks = self.tasks + (20 - len(self.tasks)) * [""]

        self.set_font("helvetica", "B", 11)
        for i, task in enumerate(tasks, start=1):
            self.cell(self.txt_width, self.line_height, str(i) + ". " + task.capitalize(), 1)

            for d in range(1, days_in_month + 1):
                self.multi_cell(day_width, self.line_height, "", border=1, align="C",
                                new_x="RIGHT", new_y="TOP", max_line_height=self.font_size)
            self.ln()

    @staticmethod
    def days_in_month(month: int = month, year: int = year):
        return pd.Timestamp(year=year, month=month, day=1).daysinmonth

    @staticmethod
    def heading(month: int = month, year: int = year):
        current_month = datetime.date(year, month, 1).strftime("%B")
        return f"Daily tasks for {current_month} {year}"

    def make_tracker(self, month: int = month, year: int = year):
        """A function that creates a page of daily tasks for given month and year. Current month and year is used if
        no argument is given"""

        self.add_page()
        self.set_font("helvetica", "B", 15)
        self.cell(self.txt_width, self.line_height, self.heading(month, year), 1, align="C")

        days_in_month = self.days_in_month(month, year)  # the number of days in given month
        day_width = (297 - self.txt_width) / days_in_month  # width of one day column

        self.add_columns(day_width, days_in_month)
        self.add_rows(day_width, days_in_month)
