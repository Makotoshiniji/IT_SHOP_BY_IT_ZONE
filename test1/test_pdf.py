import PyPDF2

# เปิดไฟล์ PDF
pdf_path = r"c:\xampp\htdocs\it_shop\test1\approve_wh3_081156.pdf"
pdf_file = open(pdf_path, "rb")
pdf_reader = PyPDF2.PdfReader(pdf_file)

# ดึงฟอร์มฟิลด์
fields = pdf_reader.get_form_text_fields()
if fields:
    for field_name, value in fields.items():
        print(f"Field Name: {field_name} | Default Value: {value}")
else:
    print("No form fields found.")

pdf_file.close()