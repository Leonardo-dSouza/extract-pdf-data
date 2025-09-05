from extract import *
from pdf2txt import pdf_to_text_native


if __name__ == "__main__":
    texto = pdf_to_text_native("1.pdf")

    data_json = return_Datajson(texto)

    print(data_json)
    print(company_name(texto))