import easygui
import PyPDF2
import os
from pathlib import Path


def main():
    for i in range(0, 3):
        i = i + 1
        if i == 1:
            print(i, " :Merge Several pdf documents")
        if i == 2:
            print(i, " :Extract a page from a document")
        if i == 3:
            print(i, " :Add a watermark to a document")
    user_operations = int(input("What PDF operation do you want : "))
    if user_operations == 1:
        merge_documents()
    elif user_operations == 2:
        extract_page()
    elif user_operations == 3:
        add_watermark()
    else:
        print("Please restart the program and select from the range above.")


def merge_documents():
    print(" \n Please put the documents you want to merge in an empty folder \n")
    try:
        documents_location = os.path.abspath(input(" \n Enter the path: "))
        all_files = os.listdir(documents_location)
        pdffiles = []
        for file in all_files:
            if file.endswith(".pdf"):
                pdffiles.append(os.path.join(documents_location, file))
        if len(pdffiles) == 0:
            print(f"There are no pdf files in the folder {os.path.basename(documents_location)}")
        else:
            print(f"There are {len(pdffiles)} pdf files in the folder {os.path.basename(documents_location)}")
            pdffiles.sort()
        document_name = os.path.join(documents_location, "merged.pdf")
        if os.path.exists(document_name):
            os.remove(document_name)
        new_document = PyPDF2.PdfMerger()
        for file in pdffiles:
            with open(file, "rb") as f:
                new_document.append(f)
        with open(document_name, "wb") as f:
            new_document.write(f)
        new_document.close()
        print(f"The PDF files have been merged and saved as {document_name}")

    except Exception as e:
        print("An error occurred: ", str(e))


def extract_page():
    file_path = os.path.abspath(input("Enter the file location: "))
    with open(file_path, "rb") as f:
        pdf = PyPDF2.PdfReader(f)
        print("\n The selected PDF has ", len(pdf.pages), " pages")
        page_number = int(input("Which page do you want to extract "))
        if page_number > len(pdf.pages):
            print("Page number is out of range")
            return

        output = PyPDF2.PdfWriter()
        output.add_page(pdf.pages[page_number - 1])
        new_file = file_path.replace(".pdf", f"_page{page_number}.pdf")
        with open(new_file, "wb") as f:
            output.write(f)
    print("Page extracted successfully, new file saved as", new_file)


def add_watermark():
    file_path = os.path.abspath(input("Enter the file location: "))
    watermark_path = os.path.abspath(input("Watermark file location: "))

    with open(file_path, "rb") as f:
        pdf = PyPDF2.PdfReader(f)
        with open(watermark_path, "rb") as w:
            watermark = PyPDF2.PdfReader(w).pages[0]

            output = PyPDF2.PdfWriter()
            for i in range(len(pdf.pages)):
                page = pdf.pages[i]
                page.rotate(45)
                page.merge_page(watermark)
                output.add_page(page)
            new_file = file_path.replace(".pdf", "_with_watermark.pdf")
    with open(new_file, "wb") as f:
        output.write(f)
    print("Watermark added successfully, new file saved as", new_file)


if __name__ == '__main__':
    main()
