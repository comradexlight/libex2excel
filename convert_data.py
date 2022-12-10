import xlsxwriter
from typing import List

from get_data import Book


def convert_data_to_table(data: List[Book], file_name: str) -> None:
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({"bold": True})
    worksheet.write(0, 0, "Автор", bold)
    worksheet.write(0, 1, "Название", bold)
    worksheet.write(0, 2, "Серия", bold)
    worksheet.write(0, 3, "Год издания", bold)
    worksheet.write(0, 4, "Издательство", bold)
    worksheet.write(0, 5, "Состояние", bold)
    for index, book in enumerate(data):
        worksheet.write(index + 1, 0, book.author)
        worksheet.write(index + 1, 1, book.title)
        worksheet.write(index + 1, 2, book.book_series)
        worksheet.write(index + 1, 3, book.year_of_publication)
        worksheet.write(index + 1, 4, book.publishing)
        worksheet.write(index + 1, 5, book.condition)
    print(f"File {file_name} created")
    workbook.close()
