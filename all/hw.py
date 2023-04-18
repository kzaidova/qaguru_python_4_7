import requests
import csv
from zipfile import ZipFile, ZIP_DEFLATED
import os



url_sample_pdf = 'https://docs.pytest.org/_/downloads/en/latest/pdf/'
url_sample_xls = 'https://file-examples.com/index.php/sample-documents-download/sample-xls-download/'
response_pdf = requests.get(url_sample_pdf, allow_redirects=True)
response_xls = requests.get(url_sample_xls, allow_redirects=True)


def create_content():
    with open('resources/latest.pdf', 'wb') as f:
        f.write(response_pdf.content)

    with open('resources/XLSX_10', 'wb') as f:
        f.write(response_xls.content)

    with open('resources/test.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=";")
        csvwriter.writerow(["Name", "Last_Name", "DOB"])
        csvwriter.writerow(["Alex", "Alex", "21/08/2001"])
        csvwriter.writerow(["Kate", "Kate", "23/03/1997"])
        csvwriter.writerow(["A", "A", "15/09/1999"])



def archive_all_files():
    dirName = 'resources/'

    for folderName, subfolders, filenames in os.walk(dirName):
        with ZipFile('resources/Архив.zip', 'w', compression=ZIP_DEFLATED, compresslevel=5) as zipcreate:
            for filename in filenames:
                if filename == ".DS_Store":
                    # пропускаем системную папку macos
                    continue
                filePath = os.path.join(folderName, filename)
                zipcreate.write(filePath)

        print(zipcreate.namelist())



def read_and_check_row():
    with ZipFile('resources/Архив.zip') as myzip:
        with myzip.open('resources/latest.pdf', 'r') as myfile:
            row_count = sum(1 for row in myfile)
    with ZipFile('resources/Архив.zip') as myzip:
        with myzip.open('resources/latest.pdf', "r") as myfile:
            row_count_arc = sum(1 for row in myfile)
    assert row_count == row_count_arc, 'Кажется файл изменили!'

    with ZipFile('resources/Архив.zip') as myzip:
        with myzip.open('resources/XLSX_10', 'r') as myfile:
            row_count = sum(1 for row in myfile)
    with ZipFile('resources/Архив.zip') as myzip:
        with myzip.open('resources/XLSX_10', "r") as myfile:
            row_count_arc = sum(1 for row in myfile)
    assert row_count == row_count_arc, 'Кажется файл изменили!'

    with ZipFile('resources/Архив.zip') as myzip:
        with myzip.open('resources/test.csv', 'r') as myfile:
            row_count = sum(1 for row in myfile)
    with ZipFile('resources/Архив.zip') as myzip:
        with myzip.open('resources/test.csv', "r") as myfile:
            row_count_arc = sum(1 for row in myfile)
    assert row_count == row_count_arc, 'Кажется файл изменили!'


def read_and_check_size():
    pdf_file_size = os.path.getsize('resources/latest.pdf')
    xlsx_file_size = os.path.getsize('resources/XLSX_10')
    csv_file_size = os.path.getsize('resources/test.csv')

    with ZipFile('resources/Архив.zip') as myzip:
        sample_size_pdf_in_archive = myzip.getinfo('resources/latest.pdf').file_size
        sample_size_xlsx_in_archive = myzip.getinfo('resources/XLSX_10').file_size
        sample_size_csv_in_archive = myzip.getinfo('resources/test.csv').file_size


    assert sample_size_pdf_in_archive == pdf_file_size, 'Кажется файл изменили!'
    assert sample_size_xlsx_in_archive == xlsx_file_size, 'Кажется файл изменили!'
    assert sample_size_csv_in_archive == csv_file_size, 'Кажется файл изменили!'
