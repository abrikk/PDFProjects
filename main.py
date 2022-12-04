import pandas

from my_pdf import PDF

pdf = PDF()
pdf.set_title("VOCA-DOKA")
pdf.set_left_margin(3)
pdf.set_right_margin(3)
pdf.add_page()
pdf.set_font("helvetica", "B", 16)
df = pandas.read_excel('voca.xlsx', sheet_name='Sheet1')

for row in df.iterrows():
    pdf.add_word(row[1].tolist())


pdf.output("voca-doka.pdf")

