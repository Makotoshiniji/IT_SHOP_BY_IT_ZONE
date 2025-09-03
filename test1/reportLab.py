import os
import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor
from datetime import datetime  # เพิ่มโมดูลสำหรับวันที่และเวลา





month = 12
saled_total = 0

# ฟังก์ชันดึงข้อมูลจากฐานข้อมูล
def get_product_data():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='db_itshop'
        )
        cursor = connection.cursor(dictionary=True)
        query = "SELECT product_code, product_name, price, stock FROM products"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()


def get_saled_quantity(product_code):
    month = 12  # กำหนดเดือนที่ต้องการ
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='db_itshop'
        )
        cursor = connection.cursor()
        # เพิ่มเงื่อนไขให้เลือกเฉพาะเดือนจาก order_date
        query = """
        SELECT SUM(quantity) AS total_saled 
        FROM order_detail 
        WHERE product_code = %s 
        AND MONTH(order_date) = %s
        """
        cursor.execute(query, (product_code, month))
        result = cursor.fetchone()
        return result[0] if result[0] else 0  # คืนค่าจำนวนรวม
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return 0
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()


# ฟังก์ชันตัดข้อความหากยาวเกิน 10 ตัวอักษร
def truncate_text(text, max_length=10):
    return text[:max_length] + "..." if len(text) > max_length else text


# ฟังก์ชันจัดรูปแบบราคา
def format_price(price):
    return f"฿{price:,.2f}"  # ขึ้นต้นด้วย ฿ และใส่ , คั่นหลักพัน พร้อมทศนิยม 2 ตำแหน่ง


def get_month_name(month):
    thai_months = [
        "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
        "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
    ]
    return thai_months[month - 1] if 1 <= month <= 12 else "ไม่ทราบเดือน"


# ลงทะเบียนฟอนต์ภาษาไทย
font_path = "fonts/Kanit/Kanit-ExtraLight.ttf"
if not os.path.exists(font_path):
    raise FileNotFoundError(f"ไม่พบไฟล์ฟอนต์ที่: {font_path}")

pdfmetrics.registerFont(TTFont('THSarabun', font_path))

# สไตล์ฟอนต์
styles = getSampleStyleSheet()
thai_style_left = ParagraphStyle(name='ThaiStyleLeft', fontName='THSarabun', fontSize=14, alignment=0)
thai_style_right = ParagraphStyle(name='ThaiStyleRight', fontName='THSarabun', fontSize=14, alignment=2)

# สร้างไฟล์ PDF
pdf_file = "product_report.pdf"
pdf = SimpleDocTemplate(
    pdf_file, 
    pagesize=letter,
    topMargin=20,  # ลดระยะห่างด้านบนให้ชิดมากขึ้น
    leftMargin=50,
    rightMargin=50,
    bottomMargin=30
)

month_name = get_month_name(month)

# หัวกระดาษ
# เพิ่มหัวข้อใหญ่ตรงกลางด้านบน
heading_center = Paragraph(
    f"รายงานผลประกอบการประจำเดือน {month_name}<br/>ของร้าน IT ZONE Shop",
    ParagraphStyle(
        name='CenterHeading',
        fontName='THSarabun',
        fontSize=16,            # ขนาดฟอนต์ใหญ่ขึ้น
        alignment=1,            # จัดกึ่งกลาง (CENTER)
        leading=24,             # ระยะห่างระหว่างบรรทัด
        spaceAfter=6,           # ระยะห่างจากข้อความด้านล่าง
        spaceBefore=0           # ลดช่องว่างด้านบน
    )
)

# สไตล์สำหรับ heading_left (เพิ่มระยะห่างระหว่างบรรทัด)
thai_style_left = ParagraphStyle(
    name='ThaiStyleLeft',
    fontName='THSarabun',
    fontSize=12,      # ขนาดตัวอักษร
    alignment=0,      # ชิดซ้าย
    leading=18,       # ระยะห่างระหว่างบรรทัด
    spaceBefore=0,    # ชิดขอบบน
    spaceAfter=0
)

# สไตล์สำหรับ heading_right (ชิดขอบบนขวา)
thai_style_right = ParagraphStyle(
    name='ThaiStyleRight',
    fontName='THSarabun',
    fontSize=12,
    alignment=2,      # ชิดขวา
    leading=14,       # ระยะห่างบรรทัดปกติ
    spaceBefore=0,    # ชิดขอบบน
    spaceAfter=0,
    rightMargin=200
)

# ดึงข้อมูลจากฐานข้อมูล
product_data = get_product_data()

# สร้างข้อมูลในตาราง
data = [["PRODUCT_CODE", "PRODUCT_NAME", "PRICE", "SALED_QUANTITY", "STOCK", "TOTAL"]]  # หัวตาราง
for product in product_data:
    truncated_name = truncate_text(product['product_name'])
    formatted_price = format_price(product['price'])
    saled_quantity = get_saled_quantity(product['product_code'])  # รวมจำนวนขาย
    total = product['price'] * saled_quantity  # คำนวณราคารวมเป็นตัวเลข
    saled_total += total  # รวมผลลัพธ์เข้ากับ saled_total
    formatted_total = format_price(total)  # แปลงเป็นรูปแบบราคา
    
    # เพิ่มข้อมูลเข้าไปในตาราง
    data.append([
        product['product_code'],
        truncated_name,
        formatted_price,
        saled_quantity,
        product['stock'],
        formatted_total
    ])


# แปลง SALED TOTAL ให้อยู่ในรูปแบบราคาหลังจากการคำนวณเสร็จ
formatted_saled_total = format_price(saled_total)

# สร้างวันที่ปัจจุบันในรูปแบบที่ต้องการ
current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # รูปแบบ: ปี-เดือน-วัน ชั่วโมง:นาที:วินาที

# สร้าง heading ขวาด้วย SALED TOTAL ที่คำนวณได้
heading_left = Paragraph(f"STORE: Online store<br/>ผู้พิมพ์: admin<br/>PRINT DATE: {current_date}", thai_style_left)
heading_right = Paragraph(f"SALED TOTAL: {formatted_saled_total}", thai_style_right)


header_data = [[heading_left, heading_right]]
header_table = Table(header_data, colWidths=[300, 300])
header_table.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # จัดชิดบน
    ('LEFTPADDING', (0, 0), (0, -1), 40),  # ไม่มี padding ซ้ายในคอลัมน์แรก
    ('RIGHTPADDING', (1, 0), (1, -1), 40),  # เพิ่ม padding ขวาคอลัมน์ที่สอง
    ('FONTNAME', (0, 0), (-1, -1), 'THSarabun'),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
]))



# สร้างตาราง ('BOTTOMPADDING', (start_col, start_row), (end_col, end_row), padding_value)
table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#DAE9F7')),  # สีหัวตาราง
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # จัดข้อความตรงกลาง
    ('ALIGN', (2, 1), (2, -1), 'RIGHT'),  # ราคาชิดขวา
    ('ALIGN', (0, 1), (1, -1), 'LEFT'),  # ราคาชิดขวา
    ('ALIGN', (3, 1), (3, -1), 'CENTER'),
    ('ALIGN', (5, 1), (5, -1), 'RIGHT'),  # ราคารวมชิดขวา
    ('FONTNAME', (0, 0), (-1, -1), 'THSarabun'),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE', (0, 0), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
]))

# เพิ่มองค์ประกอบทั้งหมดลงใน PDF
elements = [heading_center, header_table]
elements.append(table)

# สร้าง PDF
pdf.build(elements)

print(f"PDF report created: {pdf_file}")


print("Current Working Directory:", os.getcwd())