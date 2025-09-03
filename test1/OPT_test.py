import random
import smtplib
from email.message import EmailMessage

# สร้าง OTP 6 หลัก
otp = "".join(str(random.randint(0, 9)) for _ in range(6))
print(otp)

# การตั้งค่า SMTP
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

from_mail = 'shopitzone57@gmail.com'
server.login(from_mail, 'qvkw uvun fodm ecui')
# to_mail = input("Enter your email: ")
to_mail = 'Tineningch@gmail.com'

# สร้างเนื้อหา Email
msg = EmailMessage()
msg['Subject'] = "Your OTP Verification Code"
msg['From'] = from_mail
msg['To'] = to_mail

# เนื้อหา HTML
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            padding: 20px;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        .otp {{
            font-size: 24px;
            font-weight: bold;
            color: #4caf50;
        }}
        .footer {{
            margin-top: 20px;
            font-size: 12px;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h2>Welcome to IT Zone Shop</h2>
        <p>Thank you for using our service. Please use the OTP below to verify your email address:</p>
        <p class="otp">{otp}</p>
        <p>This OTP is valid for the next 2 minutes. If you did not request this, please ignore this email.</p>
        <div class="footer">
            <p>© 2024 ShopItZone. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

# ใส่ HTML เนื้อหาเข้าไปใน Email
msg.add_alternative(html_content, subtype='html')

# ส่ง Email
server.send_message(msg)
print('Email sent')

# ตรวจสอบ OTP
input_otp = input("Enter the OTP: ")

if input_otp == otp:
    print('OTP Verified')
else:
    print('Invalid OTP')

server.quit()

