from my_pdf import PDF

tasks = [
    "do physical exercises",
    "read a book (at least 10 pages)",
    "revise Voca-Doka",
    "add 10+ new words to learn",
    "play with brother",
    "do pull ups / push ups (min. 10)",
    "do math (min. 10 tasks)",
    "do speaking",
    "read an article",
    "watch movie/series in English",
    "do vocabulary tasks from a book"
]  # the tasks that should be done every day

pdf = PDF(orientation="L", tasks=tasks)

pdf.make_tracker()  # creating a page for default time
pdf.make_tracker(2, 2022)  # creating a page for February 2022
pdf.make_tracker(3, 2022)  # creating a page for March 2022
pdf.make_tracker(4, 2032)  # creating a page for April 2032

pdf.output("tada_list.pdf")
