import PyPDF2

# กำหนดพาธไฟล์ PDF ต้นฉบับและไฟล์ที่จะแก้ไข
pdf_path = r"c:\xampp\htdocs\it_shop\test1\approve_wh3_081156.pdf"
output_pdf_path = r"c:\xampp\htdocs\it_shop\test1\filled_form.pdf"

# เปิดไฟล์ PDF
pdf_file = open(pdf_path, "rb")
pdf_reader = PyPDF2.PdfReader(pdf_file)
pdf_writer = PyPDF2.PdfWriter()

# คัดลอกหน้าทั้งหมดจากไฟล์เดิม
for page in pdf_reader.pages:
    pdf_writer.add_page(page)

# ดึงฟอร์มฟิลด์
fields = pdf_reader.get_form_text_fields()

if fields:
    # กรอกค่าทุกช่องตามชื่อฟิลด์
    filled_fields = {field_name: field_name for field_name in fields.keys()}
    pdf_writer.update_page_form_field_values(pdf_writer.pages[0], filled_fields)
    
    print("Filled Form Fields:")
    for field_name, value in filled_fields.items():
        print(f"{field_name}: {value}")
else:
    print("No form fields found.")

# บันทึกไฟล์ PDF ที่กรอกข้อมูลแล้ว
with open(output_pdf_path, "wb") as output_pdf:
    pdf_writer.write(output_pdf)

pdf_file.close()

print(f"Completed! The filled form is saved as: {output_pdf_path}")
