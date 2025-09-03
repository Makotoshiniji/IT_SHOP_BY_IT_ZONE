import sys, time, os, shutil
import mysql
import mysql.connector
import pymysql
import random
import smtplib
from email.message import EmailMessage
from db import create_connection, get_phone_products, get_notebook_products, get_comset_products, get_data_cart_items, get_user_id, get_product_name, get_product_price, get_headphone_products, update_quantity_in_database
from PyQt6 import QtWidgets, QtGui, QtCore 
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from decimal import Decimal


from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor
from datetime import datetime  # เพิ่มโมดูลสำหรับวันที่และเวลา




# เก็บข้อมูลบัญชีผู้ใช้ #
# user_data = {}
global logged_in_user  # เก็บชื่อผู้ใช้ที่เข้าสู่ระบบ #
logged_in_user = None

# ===================================HOME PAGE ==================================================#
class Homepage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('หน้าหลัก')
        self.setStyleSheet('background-color: #ffffff; border-radius: 15px;')
        self.showMaximized()
        self.setWindowIcon(QIcon('image/IT ZONE LOGO.png'))


        # สร้าง container แนวตั้งมาเป็น layout หลัก
        Main_Layout = QtWidgets.QVBoxLayout()  # สร้าง instance ของ QVBoxLayout
        self.setLayout(Main_Layout)  
        Main_Layout.setContentsMargins(0, 0, 0, 0)



# ========================= MENU TOP BAR PART ========================= #

        # สร้าง MenuBar_Widget และเพิ่ม title
        self.MenuBar_Widget = QWidget()
        self.MenuBar_Area = QHBoxLayout(self.MenuBar_Widget)
        self.MenuBar_Widget.setFixedHeight(100)  # ความสูงเมนูด้านบน
        self.MenuBar_Widget.setStyleSheet('background-color: #295CA5; border-radius: 0px;')

# ============================================ ITZONE ICON ซ้ายบน ============================================ #    

        icon_ITZONE_label = QLabel(self)
        icon_pixmap = QPixmap("assets/image/ITZONEEDIT W.png")  # ระบุที่อยู่ของไฟล์ไอคอน
        icon_pixmap = icon_pixmap.scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_ITZONE_label.setPixmap(icon_pixmap)

        IT_ZONE_TOP_TITLE = QWidget()
        IT_ZONE_TOP_TITLE.setLayout(QHBoxLayout())
        IT_ZONE_TOP_TITLE.layout().addWidget(icon_ITZONE_label)

        self.MenuBar_Area.addWidget(IT_ZONE_TOP_TITLE)

# ============================================ SEARCHBAR ด้านบน ============================================ #        
        # เพิ่มแถบค้นหา
        search_bar_container = QWidget()
        search_bar_layout = QHBoxLayout(search_bar_container)
        search_bar_layout.setContentsMargins(0, 0, 0, 0)

        # สร้าง QLineEdit สำหรับแถบค้นหา
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("ค้นหาสินค้า...")
        search_bar.setFixedHeight(30)
        search_bar.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;  /* กำหนดสีของข้อความที่พิมพ์ลงไปในช่องค้นหา */
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
                padding-left: 10px;
                font-size: 14px;
                font-family: 'PK Nakhon Pathom Demo';
            }
            QLineEdit::placeholder { 
                color: gray;  /* เปลี่ยนเป็นสีที่คุณต้องการ */
                font-family: 'PK Nakhon Pathom Demo';
            }
        """)

        # สร้าง QLabel สำหรับไอคอนแว่นขยาย
        search_icon = QLabel()
        icon_pixmap = QPixmap("assets/image/magnifying glass icon.png").scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        search_icon.setPixmap(icon_pixmap)
        search_icon.setStyleSheet("""
            background-color: #295CA5;
            border-top-right-radius: 15px;
            border-bottom-right-radius: 15px;
            padding: 5px;
        """)

        # ใส่ search_bar และ search_icon ลงใน layout ของ search_bar_container
        search_bar_layout.addWidget(search_bar)
        search_bar_layout.addWidget(search_icon)

        # เพิ่ม search_bar_container ลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(search_bar_container)

# ============================================ ABOUT US ปุ่ม ============================================ #

        # สร้างปุ่มสำหรับรถเข็นสินค้า
        contact_button = QPushButton("   About us")
        contact_button.setIcon(QIcon("assets/image/contact icon.png"))  # ระบุ path ไปยังไอคอนรถเข็น
        contact_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        contact_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม
        contact_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)
        contact_button.clicked.connect(self.go_to_contactus)
        # ตั้งค่าฟอนต์
        contact_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        contact_button.setFont(contact_button_font)

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(contact_button)

# ============================================ รถเข็นสินค้า ============================================ #

        # สร้างปุ่มสำหรับรถเข็นสินค้า
        cart_button = QPushButton("   รถเข็นสินค้า")
        cart_button.setIcon(QIcon("assets/image/cart icon.png"))  # ระบุ path ไปยังไอคอนรถเข็น
        cart_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        cart_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม
        cart_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)
        if logged_in_user == None:
            cart_button.clicked.connect(
                lambda: self.show_message("ยังไม่ล็อคอิน", "กรุณาล็อคอินเข้าสู่ระบบก่อน!", QtWidgets.QMessageBox.Icon.Warning)
            )
        else:
            cart_button.clicked.connect(self.go_to_cart)
        # ตั้งค่าฟอนต์
        cart_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        cart_button.setFont(cart_button_font)
        # cart_button.clicked.connect()

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(cart_button)

# ============================================ เข้าสู่ระบบ ============================================ #

        # # ใช้ global เพื่อตรวจสอบข้อมูลผู้ใช้งาน

        # ตรวจสอบว่ามีผู้ใช้งานล็อกอินหรือไม่
        if logged_in_user:
            # ถ้ามีผู้ใช้งานล็อกอิน แสดงชื่อผู้ใช้งานในปุ่ม
            user_button = QPushButton(f"   {logged_in_user}")
        else:
            # ถ้าไม่มีผู้ใช้งาน แสดงปุ่มเข้าสู่ระบบ
            user_button = QPushButton("   เข้าสู่ระบบ")

        # ตั้งค่าไอคอน
        user_button.setIcon(QIcon("assets/image/user icon.png"))  # ระบุ path ไปยังไอคอน
        user_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        user_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม

        # ตั้งค่า StyleSheet
        user_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)

        # ตั้งค่าฟอนต์
        user_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        user_button.setFont(user_button_font)
        user_button.clicked.connect(self.go_to_login)

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(user_button)

        # เพิ่ม MenuBar_Widget ลงใน Main_Layout
        Main_Layout.addWidget(self.MenuBar_Widget)


# ================================================================= 

#                         - CONTENT PART -

# ================================================================= 

        # สร้าง Container ของ MainContent ไว้เพื่อใส่เนื้อหา
        self.MainContent_Widget = QWidget()
        self.MainContent_Area = QHBoxLayout(self.MainContent_Widget)
        Main_Layout.addWidget(self.MainContent_Widget)
        self.MainContent_Widget.setContentsMargins(0, 0, 0, 0)
        self.MainContent_Area.setContentsMargins(0, 0, 0, 0)
        self.MainContent_Area.setAlignment(Qt.AlignmentFlag.AlignLeft)
# ========================= เมนูด้านแถบซ้าย ========================= #

        # สร้าง SideBar Menu เพื่อเพิ่มเมนู
        self.SideBar_Widget = QWidget()
        self.SideBar_Area = QVBoxLayout(self.SideBar_Widget)
        self.SideBar_Widget.setFixedWidth(80)  # กำหนดความกว้างของแถบด้านซ้าย
        self.SideBar_Widget.setStyleSheet('background-color: #295CA5; border-radius: 0px;')
        self.SideBar_Area.setContentsMargins(0, 0, 0, 0)

# ============================================ COMSET Button ============================================ #

        self.COMSET_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.COMSET_ICON.setIcon(QIcon("assets/image/COMSET icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.COMSET_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.COMSET_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.COMSET_ICON.clicked.connect(self.go_to_comset)
        self.SideBar_Area.addWidget(self.COMSET_ICON)

# ============================================ NOTEBOOK Button ============================================ #

        self.NOTEBOOK_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.NOTEBOOK_ICON.setIcon(QIcon("assets/image/NOTEBOOK icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.NOTEBOOK_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.NOTEBOOK_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.NOTEBOOK_ICON.clicked.connect(self.go_to_notebook)
        self.SideBar_Area.addWidget(self.NOTEBOOK_ICON)

# ============================================ PHONE Button ============================================ #

        self.PHONE_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.PHONE_ICON.setIcon(QIcon("assets/image/PHONE icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.PHONE_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.PHONE_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.PHONE_ICON.clicked.connect(self.go_to_phone)
        self.SideBar_Area.addWidget(self.PHONE_ICON)

# ============================================ HEADPHONE Button ============================================ #

        self.HEADPHONE_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.HEADPHONE_ICON.setIcon(QIcon("assets/image/HEADPHONE icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.HEADPHONE_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.HEADPHONE_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.HEADPHONE_ICON.clicked.connect(self.go_to_headphone)
        self.SideBar_Area.addWidget(self.HEADPHONE_ICON)

# ============================================ EXIT Button ============================================ #

        self.EXIT_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.EXIT_ICON.setIcon(QIcon("assets/image/EXIT icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.EXIT_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.EXIT_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.EXIT_ICON.clicked.connect(self.go_to_login)

        self.SideBar_Area.addWidget(self.EXIT_ICON) 
        self.EXIT_ICON.setContentsMargins(0, 0, 0, 0)       

        self.MainContent_Area.addWidget(self.SideBar_Widget)


# ========================= ส่วนของคอนเท้นหลักและscollเลื่อนหน้า ========================= #
        products = [
            "image/BIGSALE.png",
            "image/MEGASALE.png",
            "image/PAYDAY.png",
        ]

        # Scoll เลื่อน
        self.content_area = QtWidgets.QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setContentsMargins(0, 0, 0, 0)
        

        # Content widget
        self.content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_widget)
        self.content_widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.content_area.setWidget(self.content_widget)
        self.content_widget.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        
        # กำหนดระยะห่างระหว่าง widgets ใน layout
        self.content_layout.setSpacing(20)  # กำหนดระยะห่างระหว่าง QLabel เป็น 20 พิกเซล
        self.content_layout.setContentsMargins(70, 10, 10, 10)  # กำหนดระยะห่างของขอบ layout

        for product in products:
            label = QtWidgets.QLabel()  # สร้าง QLabel
            pixmap = QtGui.QPixmap(product)  # โหลดรูปภาพ
            label.setPixmap(pixmap)  # ตั้งค่า QPixmap ให้กับ QLabel
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # จัดตำแหน่งให้ตรงกลาง
            label.setScaledContents(True)  # ทำให้ภาพปรับขนาดตาม QLabel
            label.setFixedSize(1300, 300)  # กำหนดขนาดของ QLabel
            self.content_layout.addWidget(label)  # เพิ่ม QLabel ลงใน layout

            self.MainContent_Area.addWidget(self.content_area)  # ใช้ชื่อที่ถูกต้อง
            self.content_area.setStyleSheet("""
        QScrollBar:vertical {
            background: #e0e0e0;
            width: 10px;
            margin: 22px 0 22px 0;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical {
            background: #a0a0a0;
            border-radius: 5px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
        }
    """)




    #================= ฟังค์ชั่นไปหน้า LOGIN ================#
    
    def go_to_login(self):
        global logged_in_user
        logged_in_user = None  # รีเซ็ตค่า logged_in_user
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า CART ========================#

    def go_to_cart(self):
        self.cart_window = CartWindow()
        self.cart_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า Comset ========================#

    def go_to_comset(self):
        self.comset_window = ComsetWindow()
        self.comset_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า Notebook ========================#

    def go_to_notebook(self):
        self.notebook_window = NotebookWindow()
        self.notebook_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า phone ========================#

    def go_to_phone(self):
        self.phone_window = PhoneWindow()
        self.phone_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า headphone ========================#

    def go_to_headphone(self):
        self.headphone_window = HeadphoneWindow()
        self.headphone_window.show()
        self.close()
    
    #================= ฟังค์ชั่นไปหน้า contact ========================#

    def go_to_contactus(self):
        self.contactus_window = ContactusWindow()
        self.contactus_window.show()
        self.close()
    
    #================= ฟังค์ชั่นไปหน้า HOMEPAGE ================#
    
    # def go_to_home(self):
    #     self.home_page = CartWindow()  # สร้างหน้าแรก
    #     self.home_page.show()  # แสดงหน้าแรก
    #     self.home_page.showMaximized()
    #     self.close()

# =================================== Message แจ้งเตือน =====================================================

    def show_message(self, title, message, icon):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))
        msg_box.exec()



# =================================== CONTACT US PAGE ==================================================#
class ContactusWindow(QtWidgets.QWidget): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle('หน้าหลัก')
        self.setStyleSheet('background-color: #ffffff; border-radius: 15px;')
        self.showMaximized()  # แสดงผลแบบเต็มจอ
        self.setWindowIcon(QtGui.QIcon('image/IT ZONE LOGO.png'))

        # ตั้งค่า Layout หลัก
        main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(main_layout)

        # เพิ่มปุ่ม Home ในตำแหน่งซ้ายบน
        self.home_button = QtWidgets.QPushButton('Home', self)
        self.home_button.setFixedSize(100, 40)
        self.home_button.setStyleSheet('''
            QPushButton {
                background-color: #FFC70A;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 14px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #E4B210;
            }
        ''')
        self.home_button.clicked.connect(self.go_to_home)

        # สร้าง Layout สำหรับวางปุ่ม Home
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.home_button, alignment=QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        top_layout.setContentsMargins(10, 10, 10, 10)

        # เพิ่ม Layout ของปุ่ม Home เข้าไปใน Layout หลัก
        main_layout.addLayout(top_layout)

    def paintEvent(self, event):
        """ใช้ QPainter วาดรูปภาพพื้นหลัง"""
        painter = QtGui.QPainter(self)

        image_path = "assets/image/ITZONE CONTACT.png"
        if not os.path.exists(image_path):
            print(f"Image file not found: {image_path}")
            return  # หยุดการวาดถ้าหากไม่พบไฟล์

        # โหลดภาพที่ต้องการใช้เป็นพื้นหลัง
        pixmap = QtGui.QPixmap(image_path)

        # ขยายรูปให้พอดีกับขนาดหน้าต่าง
        painter.drawPixmap(self.rect(), pixmap)

        # เรียกใช้งานการวาดปกติของ QWidget
        super().paintEvent(event)

    def go_to_home(self):
        self.home_page = Homepage()  # สร้างหน้าแรก
        self.home_page.show()  # แสดงหน้าแรก
        self.close()  # ปิดหน้าต่างล็อกอิน




# ===================================CART WINDOW ==================================================#

class CartWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        global user_id
        self.user_id = user_id
        self.setWindowTitle('รถเข็น')
        self.setStyleSheet('background-color: #ffffff; border-radius: 15px;')
        self.showMaximized()
        self.setWindowIcon(QIcon('image/IT ZONE LOGO.png'))


        # สร้าง container แนวตั้งมาเป็น layout หลัก
        Main_Layout = QtWidgets.QVBoxLayout()  # สร้าง instance ของ QVBoxLayout
        self.setLayout(Main_Layout)  
        Main_Layout.setContentsMargins(0, 0, 0, 0)
        

# ========================= MENU TOP BAR PART ========================= #

        # สร้าง MenuBar_Widget และเพิ่ม title
        self.MenuBar_Widget = QWidget()
        self.MenuBar_Area = QHBoxLayout(self.MenuBar_Widget)
        self.MenuBar_Widget.setFixedHeight(100)  # ความสูงเมนูด้านบน
        self.MenuBar_Widget.setStyleSheet('background-color: #295CA5; border-radius: 0px;')

# ============================================ ITZONE ICON ซ้ายบน ============================================ #    

        icon_ITZONE_label = QLabel(self)
        icon_pixmap = QPixmap("assets/image/ITZONEEDIT W.png")  # ระบุที่อยู่ของไฟล์ไอคอน
        icon_pixmap = icon_pixmap.scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_ITZONE_label.setPixmap(icon_pixmap)

        IT_ZONE_TOP_TITLE = QWidget()
        IT_ZONE_TOP_TITLE.setLayout(QHBoxLayout())
        IT_ZONE_TOP_TITLE.layout().addWidget(icon_ITZONE_label)

        self.MenuBar_Area.addWidget(IT_ZONE_TOP_TITLE)

# ============================================ SEARCHBAR ด้านบน ============================================ #        
        # เพิ่มแถบค้นหา
        search_bar_container = QWidget()
        search_bar_layout = QHBoxLayout(search_bar_container)
        search_bar_layout.setContentsMargins(0, 0, 0, 0)

        # สร้าง QLineEdit สำหรับแถบค้นหา
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("ค้นหาสินค้า...")
        search_bar.setFixedHeight(30)
        search_bar.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;  /* กำหนดสีของข้อความที่พิมพ์ลงไปในช่องค้นหา */
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
                padding-left: 10px;
                font-size: 14px;
                font-family: 'PK Nakhon Pathom Demo';
            }
            QLineEdit::placeholder { 
                color: gray;  /* เปลี่ยนเป็นสีที่คุณต้องการ */
                font-family: 'PK Nakhon Pathom Demo';
            }
        """)

        # สร้าง QLabel สำหรับไอคอนแว่นขยาย
        search_icon = QLabel()
        icon_pixmap = QPixmap("assets/image/magnifying glass icon.png").scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        search_icon.setPixmap(icon_pixmap)
        search_icon.setStyleSheet("""
            background-color: #295CA5;
            border-top-right-radius: 15px;
            border-bottom-right-radius: 15px;
            padding: 5px;
        """)

        # ใส่ search_bar และ search_icon ลงใน layout ของ search_bar_container
        search_bar_layout.addWidget(search_bar)
        search_bar_layout.addWidget(search_icon)

        # เพิ่ม search_bar_container ลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(search_bar_container)

# ============================================ ABOUT US ปุ่ม ============================================ #

        # สร้างปุ่มสำหรับรถเข็นสินค้า
        contact_button = QPushButton("   About us")
        contact_button.setIcon(QIcon("assets/image/contact icon.png"))  # ระบุ path ไปยังไอคอนรถเข็น
        contact_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        contact_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม
        contact_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)
        contact_button.clicked.connect(self.go_to_contactus)
        # ตั้งค่าฟอนต์
        contact_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        contact_button.setFont(contact_button_font)

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(contact_button)

# ============================================ รถเข็นสินค้า ============================================ #

        # สร้างปุ่มสำหรับรถเข็นสินค้า
        cart_button = QPushButton("   รถเข็นสินค้า")
        cart_button.setIcon(QIcon("assets/image/cart icon.png"))  # ระบุ path ไปยังไอคอนรถเข็น
        cart_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        cart_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม
        cart_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)
        if logged_in_user == None:
            cart_button.clicked.connect(
                lambda: self.show_message("ยังไม่ล็อคอิน", "กรุณาล็อคอินเข้าสู่ระบบก่อน!", QtWidgets.QMessageBox.Icon.Warning)
            )
        else:
            cart_button.clicked.connect(self.go_to_cart)
        # ตั้งค่าฟอนต์
        cart_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        cart_button.setFont(cart_button_font)
        # cart_button.clicked.connect()

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(cart_button)

# ============================================ เข้าสู่ระบบ ============================================ #

        # # ใช้ global เพื่อตรวจสอบข้อมูลผู้ใช้งาน
        # global logged_in_user

        # ตรวจสอบว่ามีผู้ใช้งานล็อกอินหรือไม่
        if logged_in_user:
            # ถ้ามีผู้ใช้งานล็อกอิน แสดงชื่อผู้ใช้งานในปุ่ม
            user_button = QPushButton(f"   {logged_in_user}")
        else:
            # ถ้าไม่มีผู้ใช้งาน แสดงปุ่มเข้าสู่ระบบ
            user_button = QPushButton("   เข้าสู่ระบบ")

        # ตั้งค่าไอคอน
        user_button.setIcon(QIcon("assets/image/user icon.png"))  # ระบุ path ไปยังไอคอน
        user_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        user_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม

        # ตั้งค่า StyleSheet
        user_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)

        # ตั้งค่าฟอนต์
        user_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        user_button.setFont(user_button_font)
        user_button.clicked.connect(self.go_to_login)

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(user_button)

        # เพิ่ม MenuBar_Widget ลงใน Main_Layout
        Main_Layout.addWidget(self.MenuBar_Widget)

# ================================================================= 

#                         - CONTENT PART -

# ================================================================= 

        # สร้าง Container ของ MainContent ไว้เพื่อใส่เนื้อหา
        self.MainContent_Widget = QWidget()
        self.MainContent_Area = QHBoxLayout(self.MainContent_Widget)
        Main_Layout.addWidget(self.MainContent_Widget)
        self.MainContent_Widget.setContentsMargins(0, 0, 0, 0)
        self.MainContent_Area.setContentsMargins(0, 0, 0, 0)
        self.MainContent_Area.setAlignment(Qt.AlignmentFlag.AlignLeft)
# ========================= เมนูด้านแถบซ้าย ========================= #

        # สร้าง SideBar Menu เพื่อเพิ่มเมนู
        self.SideBar_Widget = QWidget()
        self.SideBar_Area = QVBoxLayout(self.SideBar_Widget)
        self.SideBar_Widget.setFixedWidth(80)  # กำหนดความกว้างของแถบด้านซ้าย
        self.SideBar_Widget.setStyleSheet('background-color: #295CA5; border-radius: 0px;')
        self.SideBar_Area.setContentsMargins(0, 0, 0, 0)

# ============================================ COMSET Button ============================================ #

        self.COMSET_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.COMSET_ICON.setIcon(QIcon("assets/image/COMSET icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.COMSET_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.COMSET_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.COMSET_ICON.clicked.connect(self.go_to_comset)
        self.SideBar_Area.addWidget(self.COMSET_ICON)

# ============================================ NOTEBOOK Button ============================================ #

        self.NOTEBOOK_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.NOTEBOOK_ICON.setIcon(QIcon("assets/image/NOTEBOOK icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.NOTEBOOK_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.NOTEBOOK_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.NOTEBOOK_ICON.clicked.connect(self.go_to_notebook)
        self.SideBar_Area.addWidget(self.NOTEBOOK_ICON)

# ============================================ PHONE Button ============================================ #

        self.PHONE_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.PHONE_ICON.setIcon(QIcon("assets/image/PHONE icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.PHONE_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.PHONE_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.PHONE_ICON.clicked.connect(self.go_to_phone)
        self.SideBar_Area.addWidget(self.PHONE_ICON)

# ============================================ HEADPHONE Button ============================================ #

        self.HEADPHONE_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.HEADPHONE_ICON.setIcon(QIcon("assets/image/HEADPHONE icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.HEADPHONE_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.HEADPHONE_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.HEADPHONE_ICON.clicked.connect(self.go_to_headphone)
        self.SideBar_Area.addWidget(self.HEADPHONE_ICON)

# ============================================ EXIT Button ============================================ #

        self.EXIT_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.EXIT_ICON.setIcon(QIcon("assets/image/EXIT icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.EXIT_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.EXIT_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.EXIT_ICON.clicked.connect(self.go_to_login)

        self.SideBar_Area.addWidget(self.EXIT_ICON) 
        self.EXIT_ICON.setContentsMargins(0, 0, 0, 0)       

        self.MainContent_Area.addWidget(self.SideBar_Widget)


# ========================= สร้าง QScrollArea ========================= #
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)

# ========================= สร้าง content widget ========================= # ใช้แบ่งโซนรายการสินค้า กับโซนรวมราคาสินค้า
        self.content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QHBoxLayout(self.content_widget)
        self.content_widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.scroll_area.setWidget(self.content_widget)  # ใช้ content_widget
        self.content_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)  # ตั้งค่าการจัดตำแหน่งให้ที่ด้านบน
        self.content_widget.setContentsMargins(0, 0, 0, 0)  # ไม่มีขอบ
        self.content_layout.setContentsMargins(0, 0, 0, 0)  # ไม่มีขอบ

# ========================= สร้าง product_selected_widget ========================= # สำหรับใช้เป็นพื้นที่ในการโชว์แถบรายการสินค้าในตะกร้า
        self.product_selected_widget = QtWidgets.QWidget()
        self.product_selected_layout = QtWidgets.QVBoxLayout(self.product_selected_widget)
        self.product_selected_widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.content_layout.addWidget(self.product_selected_widget)  # เพิ่ม self.product_selected_widget ใน content_layout
        self.product_selected_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.product_selected_widget.setContentsMargins(0, 0, 0, 0)
        self.product_selected_layout.setContentsMargins(0, 0, 0, 0) # กำหนดระยะห่างระหว่าง widgets ใน layout
        self.product_selected_layout.setSpacing(20)  # กำหนดระยะห่างระหว่าง QLabel เป็น 20 พิกเซล
        self.product_selected_layout.setContentsMargins(70, 10, 10, 10)  # กำหนดระยะห่างของขอบ layout


# สร้าง Cart_Title ที่จะแสดงจำนวนสินค้าตะกร้า
        self.Cart_Title = QLabel(f'ตะกร้าสินค้า (0)')
        self.product_selected_layout.addWidget(self.Cart_Title)
    # ตั้งค่ารูปแบบการแสดงผลของ Cart_Title
        self.Cart_Title.setStyleSheet("""
        QLabel {
            font-size: 20px;
            color: black;
            font-weight: 400;
        }
        """)
    # เรียกใช้ฟังก์ชันเพื่ออัปเดตจำนวนสินค้าในตะกร้า
        self.update_cart_count()


# ========================= สร้าง Wrapper Widget สำหรับ Product Summary ========================= #
        self.wrapper_widget = QtWidgets.QWidget()
        self.wrapper_layout = QtWidgets.QVBoxLayout(self.wrapper_widget)
        self.wrapper_layout.setContentsMargins(0, 40, 0, 0)  # กำหนด margins (Left, Top, Right, Bottom)
        self.content_layout.addWidget(self.wrapper_widget, alignment=QtCore.Qt.AlignmentFlag.AlignTop)

    # เรียกฟังก์ชันที่ใช้ในการสร้าง UI ส่วนต่างๆ
        self.setup_product_summary()
        self.setup_discount_code()
        self.setup_total_amount()
        self.setup_discount()
        self.setup_net_amount()
        self.setup_order_button()

    def update_cart_count(self):
        try:
            # ดึงข้อมูลสินค้าจากตะกร้า
            data_cart_items = get_data_cart_items(self.user_id)
            
            # อัปเดตจำนวนสินค้าตะกร้า
            j = len(data_cart_items)

            # อัปเดต Cart_Title
            if self.Cart_Title is not None and self.Cart_Title.parent() is not None:
                self.Cart_Title.setText(f'ตะกร้าสินค้า ({j})')

            # รีเฟรช layout โดยการลบ widget เก่าทิ้ง
            for i in reversed(range(self.product_selected_layout.count())):
                widget = self.product_selected_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()  # ลบ widget เก่าทิ้ง

            # เพิ่ม widget ใหม่จากข้อมูลสินค้าในตะกร้า
            for item_data in data_cart_items:
                product_widget = Cart_ProductWidget(item_data, self)  # ส่ง self (CartWindow) ให้กับ Cart_ProductWidget
                self.product_selected_layout.addWidget(product_widget)

        except Exception as e:
            print(f"Error: {e}")


    # def set_user_id(self, user_id):
    #     self.user_id = user_id  # กำหนด user_id เพื่อใช้ในฟังก์ชันต่างๆ ที่ต้องการ


    def setup_product_summary(self):
        """สร้างแถบรวมราคาสินค้า"""
        self.product_summary_widget = QtWidgets.QWidget()
        self.product_summary_layout = QtWidgets.QVBoxLayout(self.product_summary_widget)
        self.product_summary_widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.product_summary_widget.setMaximumHeight(400)
        self.product_summary_widget.setMinimumHeight(100)
        self.product_summary_layout.setContentsMargins(20, 20, 20, 20)

        self.product_summary_widget.setStyleSheet("""
        QWidget {
            background-color: #F8F8F8;
        }
        """)
        self.wrapper_layout.addWidget(self.product_summary_widget)


    def setup_discount_code(self):
        """สร้างแถบกรอกโค้ดส่วนลด"""
        self.discount_widget = QtWidgets.QWidget()
        self.discount_layout = QtWidgets.QHBoxLayout(self.discount_widget)
        self.discount_widget.setFixedHeight(65)
        self.discount_layout.setContentsMargins(0, 0, 0, 10)
        self.discount_layout.setSpacing(10)
        self.discount_widget.setStyleSheet("""
        QWidget {
            border-bottom: 1px solid #d2d2d2;
            border-radius: 0px;
        }
        """)

        self.discount_code_input = QtWidgets.QLineEdit()
        self.discount_code_input.setFixedSize(260, 45)
        self.discount_code_input.setPlaceholderText("กรอกคูปองส่วนลด")
        self.discount_code_input.setStyleSheet("""
        QLineEdit {
            border-bottom: 2px solid #d2d2d2;
            border-radius: 0px;
            padding: 0px;
            color: #333;
            text-align: left;  
        }
        QLineEdit:focus {
            border-bottom: 2px solid #6699CC;
        }
        QLineEdit::placeholder {
            color: #aaa;
            font-style: italic;
        }
        """)
        self.discount_layout.addWidget(self.discount_code_input)

        self.apply_discount_button = QtWidgets.QPushButton("ใช้งาน")
        self.apply_discount_button.setFixedSize(80, 45)
        self.apply_discount_button.setStyleSheet("""
        QPushButton {
            background-color: #6699CC;
            color: white;
            font-size: 14px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #557a99;
        }
        QPushButton:pressed {
            background-color: #466080;
        }
        """)
        self.discount_layout.addWidget(self.apply_discount_button)
        self.product_summary_layout.addWidget(self.discount_widget, alignment=QtCore.Qt.AlignmentFlag.AlignTop)

        # เชื่อมต่อปุ่ม "ใช้งาน" กับฟังก์ชัน apply_discount
        self.apply_discount_button.clicked.connect(self.apply_discount)


    def apply_discount(self):
        """ตรวจสอบโค้ดส่วนลดและอัปเดตราคา"""
        discount_code = self.discount_code_input.text().strip() #ดึงค่าข้อความจากช่องป้อนรหัสส่วนลดและลบช่องว่างด้านหน้าและด้านหลังข้อความ
        if discount_code == "ITSHOP3000":
            discount_value = 3000
            self.discount_amount_label.setText(f"฿{discount_value:,}")
        else:
            QtWidgets.QMessageBox.warning(self, "ข้อผิดพลาด", "คูปองส่วนลดไม่ถูกต้อง!")

        # อัปเดตยอดรวมสุทธิหลังจากตรวจสอบส่วนลด
        self.update_net_amount()


    def get_cart_items_total_price(self, user_id):
        """เชื่อมต่อกับฐานข้อมูลและคำนวณยอดรวมสินค้า"""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='db_itshop'
            )
            cursor = connection.cursor()
            cursor.execute("""
                SELECT 
                    products.price, 
                    cart_items.quantity
                FROM 
                    cart_items
                JOIN 
                    products 
                ON 
                    cart_items.product_code = products.product_code
                WHERE 
                    cart_items.user_id = %s
            """, (user_id,))
            items = cursor.fetchall()
            cursor.close()
            connection.close()

            #ใช้ for loop เพื่อวนซ้ำในแต่ละ (price, quantity) ของ items
            return sum(price * quantity for price, quantity in items) 
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return 0


    def setup_total_amount(self):
        """อัปเดตราคาสินค้าในช่องยอดรวม"""
        try:
            # คำนวณราคายอดรวมใหม่
            total_price = self.get_cart_items_total_price(self.user_id)
            total_amount = f"฿{total_price:,.2f}"

            # ตรวจสอบว่าช่องยอดรวมมีอยู่แล้วหรือไม่
            if hasattr(self, "total_amount_label"):
                self.total_amount_label.setText(total_amount)
            else:
                total_amount_layout = QtWidgets.QHBoxLayout()   # สร้าง Layout แนวนอนสำหรับแสดงยอดรวม
                total_text_label = QtWidgets.QLabel("ยอดรวม")   # สร้าง QLabel เพื่อแสดงข้อความ "ยอดรวม"
                self.total_amount_label = QtWidgets.QLabel(total_amount)   # สร้าง QLabel สำหรับแสดงยอดรวม

                total_text_label.setStyleSheet("QLabel {color: black;}")   # ตั้งค่ารูปแบบของ QLabel "ยอดรวม" ด้วย CSS (เปลี่ยนสีข้อความเป็นสีดำ)
                self.total_amount_label.setStyleSheet("QLabel {color: black;}")   # ตั้งค่ารูปแบบของ QLabel ที่แสดงยอดรวมด้วย CSS (เปลี่ยนสีข้อความเป็นสีดำ)

                total_amount_layout.addWidget(total_text_label)# เพิ่ม QLabel "ยอดรวม" ลงใน Layout
                total_amount_layout.addStretch()   # เพิ่มพื้นที่ว่างเพื่อดัน QLabel ยอดรวมไปทางขวา
                total_amount_layout.addWidget(self.total_amount_label)   # เพิ่ม QLabel ที่แสดงยอดรวมลงใน Layout

                self.product_summary_layout.addSpacing(5)   # เพิ่มระยะห่างใน Layout สรุปรายการสินค้า (แนวตั้ง) ระหว่างส่วนอื่นกับส่วนยอดรวม
                self.product_summary_layout.addLayout(total_amount_layout)   # เพิ่ม Layout "total_amount_layout" เข้าไปใน Layout สรุปรายการสินค้า

            # อัปเดตยอดรวมสุทธิ
            self.update_net_amount()

        except Exception as e:
            print(f"Error: {e}")


    def setup_discount(self):
        """สร้างช่องส่วนลด"""
        discount_layout = QtWidgets.QHBoxLayout()
        discount_text_label = QtWidgets.QLabel("ส่วนลด")
        discount_text_label.setStyleSheet("QLabel {color: black;}")

        self.discount_amount_label = QtWidgets.QLabel("฿0")  # บันทึก QLabel นี้ใน self
        self.discount_amount_label.setStyleSheet("QLabel {color: black;}")

        discount_layout.addWidget(discount_text_label)
        discount_layout.addStretch()
        discount_layout.addWidget(self.discount_amount_label)

        self.product_summary_layout.addSpacing(5)
        self.product_summary_layout.addLayout(discount_layout)


    def setup_net_amount(self):
        """สร้างช่องยอดรวมสุทธิ"""
        try:
            # ดึงยอดรวมจากสินค้าที่อยู่ในตะกร้า
            total_price = self.get_cart_items_total_price(self.user_id)
            net_amount = f"฿{total_price:,.2f}"  # ตั้งค่าเริ่มต้นให้เท่ากับยอดรวม

            # สร้างเลย์เอาต์และ QLabel สำหรับยอดรวมสุทธิ
            net_amount_layout = QtWidgets.QHBoxLayout()
            net_amount_text_label = QtWidgets.QLabel("ยอดรวมสุทธิ")
            net_amount_text_label.setStyleSheet("QLabel {color: black;}")

            self.net_amount_label = QtWidgets.QLabel(net_amount)  # ตั้งค่า QLabel ด้วยยอดรวมเริ่มต้น
            self.net_amount_label.setStyleSheet("QLabel {color: black;}")

            net_amount_layout.addWidget(net_amount_text_label)
            net_amount_layout.addStretch()
            net_amount_layout.addWidget(self.net_amount_label)

            self.product_summary_layout.addSpacing(10)
            self.product_summary_layout.addLayout(net_amount_layout)

        except Exception as e:
            print(f"Error in setup_net_amount: {e}")


    def update_net_amount(self):
        """อัปเดตยอดรวมสุทธิโดยใช้ยอดรวมและส่วนลด"""
        try:
            # ดึงราคายอดรวมจากตะกร้าและแปลงเป็น Decimal
            total_price = Decimal(self.get_cart_items_total_price(self.user_id))

            # ดึงส่วนลดจาก label และแปลงเป็น Decimal
            discount_text = self.discount_amount_label.text().replace("฿", "").replace(",", "")
            discount_amount = Decimal(discount_text) if discount_text else Decimal(0)

            # คำนวณยอดรวมสุทธิ
            net_amount = total_price - discount_amount
            self.net_amount_label.setText(f"฿{net_amount:,.2f}")

        except Exception as e:
            print(f"Error: {e}")


    def open_bill_window(self):
        """เปิดหน้าต่างบิลและส่งข้อมูลยอดรวม"""
        try:
            # คำนวณยอดรวมสินค้า
            total_price = Decimal(self.get_cart_items_total_price(self.user_id))
            print(f"Total Price: {total_price}")

            # ดึงข้อมูลส่วนลดจาก QLabel
            discount_text = self.discount_amount_label.text().replace("฿", "").replace(",", "")
            discount_amount = Decimal(discount_text) if discount_text else Decimal(0)

            # คำนวณยอดรวมสุทธิ
            net_amount = total_price - discount_amount

            # ส่งข้อมูลไปยังหน้าต่างบิล
            self.bill_window = BillWindow(
                order_id=self.current_order_id, 
                total_price=float(total_price), 
                discount=float(discount_amount), 
                net_amount=float(net_amount)
            )
            self.bill_window.show()
        except Exception as e:
            print(f"Error in opening BillWindow: {e}")


    def setup_order_button(self):
        """สร้างปุ่มซื้อ"""
        order_button = QtWidgets.QPushButton("ดำเนินการสั่งซื้อ")
        order_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        order_button.setFixedSize(360, 60)
        order_button.setStyleSheet("""
        QPushButton {
            background-color: #6699CC;
            color: white;
            font-size: 18px;
            font-weight: 750;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: #557a99;
        }
        QPushButton:pressed {
            background-color: #466080;
        }
        """)

        # เชื่อมโยงปุ่มกับฟังก์ชัน go_to_confirm_order
        order_button.clicked.connect(self.go_to_confirm_order)

        # เพิ่มปุ่มไปใน layout
        self.product_summary_layout.addSpacing(15)
        self.product_summary_layout.addWidget(order_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

# ========================= ส่วนเพื่ม Qscoll ลงใน MainContent ========================= #

        # เพิ่ม QScrollArea ลงใน MainContent_Area
        self.MainContent_Area.addWidget(self.scroll_area)  # ใช้ชื่อที่ถูกต้อง
        self.scroll_area.setStyleSheet("""
    QScrollBar:vertical {
        background: #e0e0e0;
        width: 10px;
        margin: 22px 0 22px 0;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical {
        background: #a0a0a0;
        border-radius: 5px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background: none;
    }
""")

    #================= ฟังค์ชั่นไปหน้า CONFIRM ORDER ================#

    def go_to_confirm_order(self):
        """เมื่อกดปุ่ม 'ดำเนินการสั่งซื้อ'"""
        self.setup_net_amount()
        # ดึงค่าจาก net_amount_label ที่แสดงยอดรวมสุทธิ
        # ดึงค่าข้อความจาก QLabel "net_amount_label" ซึ่งแสดงยอดสุทธิ แล้วลบสัญลักษณ์ "฿" และเครื่องหมายคอมมา (,) ออก
        total_amount = self.net_amount_label.text().replace("฿", "").replace(",", "")
        # แปลงเป็นตัวเลข แปลงค่า `total_amount` เป็นชนิดข้อมูล Decimal หาก `total_amount` มีค่า
        total_amount = Decimal(total_amount) if total_amount else Decimal(0)
        # เปิดหน้าต่าง ConfirmOrderWindow และส่งข้อมูล user_id และ total_amount
        self.confirm_order_window = ConfirmOrderWindow(self.user_id, total_amount)
        self.confirm_order_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า LOGIN ================#

    def go_to_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า CART ========================#

    def go_to_cart(self):
        self.cart_window = CartWindow()
        self.cart_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า Comset ========================#

    def go_to_comset(self):
        self.comset_window = ComsetWindow()
        self.comset_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า Notebook ========================#

    def go_to_notebook(self):
        self.notebook_window = NotebookWindow()
        self.notebook_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า phone ========================#

    def go_to_phone(self):
        self.phone_window = PhoneWindow()
        self.phone_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า headphone ========================#

    def go_to_headphone(self):
        self.headphone_window = HeadphoneWindow()
        self.headphone_window.show()
        self.close()

    def go_to_contactus(self):
        self.contactus_window = ContactusWindow()
        self.contactus_window.show()
        self.close()
    
    #================= ฟังค์ชั่นไปหน้า HOMEPAGE ================#
    
    # def go_to_home(self):
    #     self.home_page = CartWindow()  # สร้างหน้าแรก
    #     self.home_page.show()  # แสดงหน้าแรก
    #     self.home_page.showMaximized()
    #     self.close()

    # def update_cart(self):
    #     # ดึงข้อมูลสินค้าในตะกร้าปัจจุบัน
    #     data_cart_items = get_data_cart_items(self.user_id)
    #     current_ids = {item['id'] for item in data_cart_items}

    #     # ลบ widget ของสินค้าที่ไม่มีในตะกร้าแล้ว
    #     for item_id in list(self.cart_widgets.keys()):
    #         if item_id not in current_ids:
    #             widget = self.cart_widgets.pop(item_id)
    #             self.product_selected_layout.removeWidget(widget)
    #             widget.deleteLater()

    #     # เพิ่มหรืออัปเดตรายการที่มีอยู่
    #     for item in data_cart_items:
    #         item_id = item['id']
    #         if item_id in self.cart_widgets:
    #             # อัปเดต widget ที่มีอยู่
    #             self.cart_widgets[item_id].update_item(item)
    #         else:
    #             # สร้าง widget ใหม่สำหรับสินค้า
    #             new_widget = Cart_ProductWidget(item, self)
    #             self.cart_widgets[item_id] = new_widget
    #             self.product_selected_layout.addWidget(new_widget)

        # อัปเดตจำนวนสินค้าในตะกร้า
        self.update_cart_count()


class Cart_ProductWidget(QtWidgets.QWidget):
    def __init__(self, item_data, cart_window, parent=None):
        super().__init__(parent)
        self.cart_window = cart_window  # เก็บอ้างอิงถึง CartWindow
        global user_id
        self.user_id = user_id
        # print(self.user_id)

        # ข้อมูลสินค้า
        self.product_code = item_data['product_code']
        self.quantity = item_data['quantity']

        # ส่วนอื่นๆ ของ Cart_ProductWidget
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        # รูปสินค้า
        image_label = QtWidgets.QLabel()
        pixmap_path = f'assets/product_image/{self.product_code}_pic.png'
        pixmap = QtGui.QPixmap(pixmap_path)
        if pixmap.isNull():
            pixmap = QtGui.QPixmap('assets/product_image/default.png')  # ใช้รูป default หากไม่พบรูป
        pixmap = pixmap.scaled(85, 85)
        image_label.setPixmap(pixmap)
        self.layout.addWidget(image_label)

        # ชื่อสินค้า
        product_name = get_product_name(self.product_code) or "ไม่พบชื่อสินค้า"
        label_name = QtWidgets.QLabel(product_name)
        label_name.setWordWrap(True)
        label_name.setStyleSheet("color: black; font-size: 16px;")
        label_name.setFixedWidth(400)
        self.layout.addWidget(label_name)

        # ราคาสินค้า
        product_price = get_product_price(self.product_code) or 0.00
        price_label = QtWidgets.QLabel(f"฿{float(product_price):,.2f}")
        price_label.setStyleSheet("color: #F1574F; font-size: 16px;")
        self.layout.addWidget(price_label, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        # ปุ่มเพิ่ม/ลดจำนวนสินค้า
        quantity_layout = QtWidgets.QHBoxLayout()
        decrease_button = QtWidgets.QPushButton("-")
        decrease_button.setFixedSize(40, 30)
        self.quantity_label = QtWidgets.QLabel(str(self.quantity))
        self.quantity_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.quantity_label.setFixedSize(50, 30)
        increase_button = QtWidgets.QPushButton("+")
        increase_button.setFixedSize(40, 30)
        quantity_layout.addWidget(decrease_button)
        quantity_layout.addWidget(self.quantity_label)
        quantity_layout.addWidget(increase_button)
        self.layout.addLayout(quantity_layout)

        # ฟังก์ชันเพิ่ม/ลดจำนวนสินค้า
        # เชื่อมต่อปุ่ม decrease_button กับฟังก์ชัน change_quantity โดยส่งค่า -1
        decrease_button.clicked.connect(lambda: self.change_quantity(-1))
        # เชื่อมต่อปุ่ม increase_button กับฟังก์ชัน change_quantity โดยส่งค่า 1
        increase_button.clicked.connect(lambda: self.change_quantity(1))

        # ปุ่มถังขยะ
        trash_button = QtWidgets.QPushButton()
        trash_button.setFixedSize(30, 30)
        trash_button.setIcon(QtGui.QIcon('assets/image/trash_icon.png'))
        trash_button.setIconSize(QtCore.QSize(20, 20))
        trash_button.clicked.connect(self.confirm_remove_item)
        self.layout.addWidget(trash_button)

    def change_quantity(self, amount):
        new_quantity = self.quantity + amount
        if new_quantity >= 1:
            self.quantity = new_quantity
            self.quantity_label.setText(str(self.quantity))
            update_quantity_in_database(self.product_code, self.quantity)
            self.cart_window.setup_total_amount()  # เรียกใช้งาน setup_total_amount หลังจากอัปเดตเสร็จแล้ว

    def confirm_remove_item(self):
        reply = QtWidgets.QMessageBox.question(
            self,
            "ลบสินค้า",
            f"คุณต้องการลบสินค้ารหัส {self.product_code} ออกจากตะกร้าหรือไม่?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            self.remove_product_from_cart()

    def remove_product_from_cart(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='db_itshop'
            )
            cursor = connection.cursor()

            # ลบสินค้าจากตารางตะกร้า
            query = "DELETE FROM cart_items WHERE product_code = %s AND user_id = %s"
            cursor.execute(query, (self.product_code, self.user_id))

            # บันทึกการเปลี่ยนแปลง
            connection.commit()
            print(f"Product {self.product_code} removed successfully from the database.")
        except mysql.connector.Error as e:
            print(f"An error occurred: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        # อัปเดตจำนวนสินค้าหลังจากลบ
        self.cart_window.update_cart_count()
        self.cart_window.setup_total_amount()  # เรียกใช้งาน setup_total_amount หลังจากอัปเดตเสร็จแล้ว
        self.setParent(None)  # ลบ widget ออกจาก layout





# =================================== Message แจ้งเตือน =====================================================

    def show_message(self, title, message, icon):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))
        msg_box.exec()

# =================================== CONFIRM ORDER WINDOWN ===================================================== 

class ConfirmOrderWindow(QtWidgets.QWidget):
    def __init__(self, user_id, total_amount):
        super().__init__()
        self.user_id = user_id  # user_id ที่รับมา
        self.total_amount = total_amount  # total_amount ที่รับมา
        self.setWindowTitle("Confirm Order")
        self.setStyleSheet("background-color: #ffffff; border-radius: 15px;")
        self.setGeometry(360, 110, 700, 650)
        self.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))

        # Layout หลัก
        main_layout = QtWidgets.QVBoxLayout()

        # สร้าง Layout สำหรับ top bar
        top_bar_layout = QtWidgets.QHBoxLayout()

        # ปุ่ม "กลับ"
        self.back_button = QtWidgets.QPushButton("←")
        self.back_button.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 12))
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #ff6666; 
                color: #ffffff; 
                border-radius: 10px; 
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #ff3333;
            }
        """)
        self.back_button.clicked.connect(self.go_to_home)

        # เพิ่มปุ่ม "กลับ" ลงใน top_bar_layout
        top_bar_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        
        # เพิ่ม top_bar_layout ใน main_layout
        main_layout.addLayout(top_bar_layout)

        # หัวข้อ "ยืนยันการสั่งซื้อ"
        title_label = QtWidgets.QLabel("ยืนยันการสั่งซื้อ")
        title_label.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 24, QtGui.QFont.Weight.Bold))
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #000000;")
        main_layout.addWidget(title_label)

        # ฟอร์มสำหรับกรอกที่อยู่ในการจัดส่ง
        form_layout = QtWidgets.QFormLayout()
        form_layout.setContentsMargins(50, 20, 50, 20)

        # ช่องกรอกที่อยู่
        self.address_input = QtWidgets.QLineEdit()
        self.address_input.setPlaceholderText("กรอกที่อยู่ในการจัดส่ง")
        self.address_input.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 14))
        self.address_input.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; 
                color: #2d3b4f; 
                border: 1px solid #d3d3d3;  
                border-radius: 10px; 
                padding: 10px;
            }
            QLineEdit:hover {
                background-color: #dcdcdc;  
            }
        """)
        form_layout.addRow("ที่อยู่ในการจัดส่ง", self.address_input)

        main_layout.addLayout(form_layout)

        # ปุ่มยืนยันการสั่งซื้อ
        self.confirm_button = QtWidgets.QPushButton("ยืนยันการสั่งซื้อ")
        self.confirm_button.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 14))
        self.confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #1F232D; 
                color: #ffffff; 
                border-radius: 20px; 
                padding: 10px; 
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background-color: #2A2E38;  
            }
        """)
        self.confirm_button.clicked.connect(self.confirm_order)
        main_layout.addWidget(self.confirm_button)

        # ตั้งค่า layout หลัก
        self.setLayout(main_layout)

    def confirm_order(self):
        """บันทึกคำสั่งซื้อและที่อยู่ลงในฐานข้อมูล"""
        address = self.address_input.text().strip()
        if not address:
            self.show_message("ข้อผิดพลาด", "กรุณากรอกที่อยู่ในการจัดส่ง", QtWidgets.QMessageBox.Icon.Critical)
            return

        try:
            # เชื่อมต่อฐานข้อมูล MySQL
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='db_itshop'
            )
            cursor = connection.cursor()

            # สร้างคำสั่ง SQL สำหรับการบันทึกข้อมูลคำสั่งซื้อ
            query = """
                INSERT INTO orders (user_id, address, total_amount)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (self.user_id, address, self.total_amount))

            # ยืนยันการบันทึกข้อมูลคำสั่งซื้อ
            connection.commit()

            # ดึง order_id ที่เพิ่งถูกสร้าง
            order_id = cursor.lastrowid

            # ตอนนี้บันทึกข้อมูลในตาราง order_detail
            cart_items = self.get_cart_items(self.user_id)

            order_detail_query = """
                INSERT INTO order_detail (order_id, product_code, quantity, unit_price)
                VALUES (%s, %s, %s, %s)
            """
            for item in cart_items:
                product_code, quantity, unit_price = item
                cursor.execute(order_detail_query, (order_id, product_code, quantity, unit_price))

            connection.commit()

            cursor.close()
            connection.close()

            # แสดงข้อความยืนยันการสั่งซื้อ
            self.show_message("ยืนยันการสั่งซื้อ", "คำสั่งซื้อของคุณได้รับการยืนยันแล้ว", QtWidgets.QMessageBox.Icon.Information)

            # หลังจากแสดงข้อความยืนยันแล้ว ให้เปิดหน้าต่างบิล
            # เพิ่มการใช้ QTimer เพื่อรอปิด message box ก่อนที่จะเปิดหน้าต่างบิล
            QtCore.QTimer.singleShot(1000, lambda: self.show_bill_window(order_id))  # รอ 1 วินาทีแล้วเปิดหน้าต่างบิล

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.show_message("ข้อผิดพลาด", "เกิดข้อผิดพลาดในการบันทึกคำสั่งซื้อ", QtWidgets.QMessageBox.Icon.Critical)


    def get_cart_items(self, user_id):
        """ดึงข้อมูลสินค้าจากตะกร้าของผู้ใช้"""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='db_itshop'
            )
            cursor = connection.cursor()
            cursor.execute("""
                SELECT 
                    products.product_code, 
                    cart_items.quantity, 
                    products.price AS unit_price
                FROM 
                    cart_items
                JOIN 
                    products 
                ON 
                    cart_items.product_code = products.product_code
                WHERE 
                    cart_items.user_id = %s
            """, (user_id,))
            items = cursor.fetchall()
            cursor.close()
            connection.close()
            return items
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []


    def show_message(self, title, message, icon):
        """แสดงข้อความแจ้งเตือน"""
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))
        msg_box.exec()


    def show_bill_window(self, order_id):
        try:
            self.bill_window = BillWindow(order_id)  # สร้างหน้าต่างบิลโดยส่ง order_id
            self.bill_window.show()  # แสดงหน้าต่างบิล
            self.close()

        except Exception as e:
            print(f"Error opening BillWindow: {e}")
            self.show_message("ข้อผิดพลาด", "ไม่สามารถเปิดหน้าต่างบิลได้", QtWidgets.QMessageBox.Icon.Critical)


    def go_to_home(self):
        self.home_page = Homepage()  # สร้างหน้าแรก
        self.home_page.show()  # แสดงหน้าแรก
        self.close()  # ปิดหน้าต่างล็อกอิน



class BillWindow(QtWidgets.QWidget):
    def __init__(self, order_id, total_price=0, discount=0, net_amount=0):
        super().__init__()
        self.order_id = order_id
        self.total_price = total_price
        self.discount = discount
        self.net_amount = net_amount
        self.setup_ui()


        self.setWindowTitle("BILL")
        self.setGeometry(360, 110, 700, 600)
        self.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))

    def truncate_text(self, text, max_length):
        """ตัดข้อความให้มีความยาวไม่เกิน max_length และเพิ่ม '...' ถ้าจำเป็น"""
        if len(text) > max_length:
            return text[:max_length] + "..."
        return text
    
    def format_price(self, price):
        """ฟอร์แมตราคาสินค้าให้อยู่ในรูปแบบที่เหมาะสม"""
        return f"฿{price:,.2f}"

    def setup_ui(self):
        """สร้าง UI ของหน้าบิล"""
        try:
            print("Setting up BillWindow UI...")  # เพิ่มการดีบัก
            layout = QtWidgets.QVBoxLayout(self)

            # ส่วนหัวบิล (ชื่อร้านและวันที่)
            header_layout = QtWidgets.QVBoxLayout()
            shop_name_label = QtWidgets.QLabel("ร้าน IT ZONE")
            shop_name_label.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Weight.Bold))
            shop_name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            shop_name_label.setStyleSheet("color: #000000;")

            date_label = QtWidgets.QLabel(f"วันที่: {QtCore.QDate.currentDate().toString('yyyy-MM-dd')}")
            date_label.setFont(QtGui.QFont("Arial", 12))
            date_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            date_label.setStyleSheet("color: #333333;")

            header_layout.addWidget(shop_name_label)
            header_layout.addWidget(date_label)
            layout.addLayout(header_layout)

            # ส่วนตารางแสดงบิล
            self.table = QtWidgets.QTableWidget(self)
            self.table.setRowCount(0)
            self.table.setColumnCount(3)  # เปลี่ยนเป็น 3 คอลัมน์ (ชื่อสินค้า, จำนวน, รวมราคา)
            self.table.setHorizontalHeaderLabels(["ชื่อสินค้า", "จำนวน", "รวมราคา"])

            # ปรับขนาดคอลัมน์
            self.table.setColumnWidth(0, 350)  # กำหนดให้คอลัมน์ "ชื่อสินค้า" กว้างสุด
            self.table.setColumnWidth(1, 100)  # กำหนดขนาดคอลัมน์ "จำนวน"
            self.table.setColumnWidth(2, 150)  # กำหนดขนาดคอลัมน์ "รวมราคา"

            # ปรับสไตล์ตาราง
            self.table.setStyleSheet("""
                QTableWidget {
                    border: 1px solid #d3d3d3;
                    font-size: 14px;
                    padding: 5px;
                }
                QTableWidget::item {
                    padding: 10px;
                }
                QTableWidget::horizontalHeader {
                    background-color: #f4f4f4;
                    font-weight: bold;
                }
                QHeaderView::section {
                    background-color: #f4f4f4;
                    border: none;
                }
            """)

            # ทำให้ตัวเลขในคอลัมน์ "จำนวน" อยู่ตรงกลาง
            for i in range(self.table.rowCount()):
                self.table.item(i, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
            layout.addWidget(self.table)

            # ส่วนสำหรับยอดรวม
            total_layout = QtWidgets.QHBoxLayout()
            total_label = QtWidgets.QLabel("ยอดรวม: ")
            total_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Weight.Bold))
            total_label.setStyleSheet("color: #000000;")
            
            self.total_amount_label = QtWidgets.QLabel("฿0.00")
            self.total_amount_label.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Weight.Bold))
            self.total_amount_label.setStyleSheet("color: #e60000;")

            total_layout.addWidget(total_label)
            total_layout.addWidget(self.total_amount_label, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
            layout.addLayout(total_layout)

            # ปุ่มปิด
            close_button = QtWidgets.QPushButton("ปิด")
            close_button.setFont(QtGui.QFont("Arial", 14))
            close_button.setStyleSheet("""
                QPushButton {
                    background-color: #ff6666;
                    color: #ffffff;
                    border-radius: 10px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #ff3333;
                }
            """)
            close_button.clicked.connect(self.close)
            layout.addWidget(close_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

            # ปุ่มกลับไปหน้าหลัก
            back_button = QtWidgets.QPushButton("กลับไปหน้าหลัก")
            back_button.setFont(QtGui.QFont("Arial", 14))
            back_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: #ffffff;
                    border-radius: 10px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            back_button.clicked.connect(self.go_to_home)  # เชื่อมต่อกับฟังก์ชัน go_to_main_window
            layout.addWidget(back_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

            # ปุ่มพิมพ์ PDF
            print_pdf_button = QtWidgets.QPushButton("พิมพ์ใบเสร็จ")
            print_pdf_button.setFont(QtGui.QFont("Arial", 14))
            print_pdf_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: #ffffff;
                    border-radius: 10px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            print_pdf_button.clicked.connect(self.print_receipt_to_pdf)
            layout.addWidget(print_pdf_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

            # แทรกรูป QR Code ที่นี่
            self.qr_code_label = QtWidgets.QLabel(self)
            qr_code_pixmap = QtGui.QPixmap("assets/image/QR.jpg")  # กำหนดที่อยู่ของ QR Code
            self.qr_code_label.setPixmap(qr_code_pixmap.scaled(100, 100, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            self.qr_code_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(self.qr_code_label)

            # โหลดรายละเอียดบิล
            self.load_bill_details()

        except Exception as e:
            print(f"Error in setting up UI: {e}")
            QtWidgets.QMessageBox.warning(self, "ข้อผิดพลาด", "ไม่สามารถตั้งค่า UI ของบิลได้")

    def load_bill_details(self):
        """ดึงข้อมูลรายละเอียดสินค้าจากฐานข้อมูลและแสดงในตาราง"""
        try:
            print(f"Loading bill details for order_id: {self.order_id}")  # เพิ่มการดีบัก
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='db_itshop'
            )
            cursor = connection.cursor()

            cursor.execute("""
                SELECT 
                    p.product_name, 
                    od.quantity, 
                    (od.quantity * p.price) AS total_price
                FROM 
                    order_detail od
                JOIN 
                    products p ON od.product_code = p.product_code
                WHERE 
                    od.order_id = %s
            """, (self.order_id,))
            rows = cursor.fetchall()
            print(f"Fetched rows: {rows}")  # เพิ่มการดีบัก

            self.table.setRowCount(len(rows))
            total_price = self.net_amount
            for i, row in enumerate(rows):
                print(f"Adding row {i}: {row}")  # เพิ่มการดีบัก
                self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(row[0]))  # ชื่อสินค้า
                self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(row[1])))  # จำนวน
                self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(f"฿{row[2]:,.2f}"))  # รวมราคา
                total_price += row[2]  # คำนวณยอดรวม

            # แสดงยอดรวม
            self.total_amount_label.setText(f"฿{total_price:,.2f}")

            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            QtWidgets.QMessageBox.warning(self, "ข้อผิดพลาด", "ไม่สามารถดึงข้อมูลบิลได้")
        except Exception as e:
            print(f"Unexpected error: {e}")
            QtWidgets.QMessageBox.warning(self, "ข้อผิดพลาด", "ไม่สามารถดึงข้อมูลบิลได้")

        # แสดงยอดรวม
        self.total_price = total_price  # กำหนดให้ self.total_price เป็นยอดรวมที่คำนวณได้
        self.total_amount_label.setText(f"฿{self.total_price:,.2f}")


    def print_receipt_to_pdf(self):
        """พิมพ์ใบเสร็จเป็น PDF โดยใช้ข้อมูลจากตาราง"""
        dialog = QtWidgets.QFileDialog(self)
        file_path, _ = dialog.getSaveFileName(self, "บันทึกเป็น PDF", "", "PDF Files (*.pdf)")
        if file_path:
            try:
                # Setup for PDF creation
                font_path = "fonts/Kanit/Kanit-ExtraLight.ttf"
                if not os.path.exists(font_path):
                    raise FileNotFoundError(f"ไม่พบไฟล์ฟอนต์ที่: {font_path}")
                pdfmetrics.registerFont(TTFont('THSarabun', font_path))

                styles = getSampleStyleSheet()
                thai_style_left = ParagraphStyle(
                    name='ThaiStyleLeft',
                    fontName='THSarabun',
                    fontSize=14,
                    alignment=0,
                    leading=18,
                    spaceBefore=0,
                    spaceAfter=0
                )
                thai_style_right = ParagraphStyle(
                    name='ThaiStyleRight',
                    fontName='THSarabun',
                    fontSize=14,
                    alignment=2,
                    leading=14,
                    spaceBefore=0,
                    spaceAfter=0
                )

                pdf = SimpleDocTemplate(
                    file_path, 
                    pagesize=letter,
                    topMargin=20, 
                    leftMargin=50,
                    rightMargin=50,
                    bottomMargin=30
                )

                heading_center = Paragraph(
                    f"ใบเสร็จจากร้าน IT ZONE",
                    ParagraphStyle(
                        name='CenterHeading',
                        fontName='THSarabun',
                        fontSize=16,
                        alignment=1,
                        leading=24,
                        spaceAfter=6
                    )
                )

                # Get data from the table
                data = [["PRODUCT_NAME", "QUANTITY", "TOTAL"]]
                for row in range(self.table.rowCount()):
                    product_name = self.table.item(row, 0).text()
                    quantity = self.table.item(row, 1).text()
                    total_price = self.table.item(row, 2).text()

                    # Truncate the product name if it's too long
                    truncated_name = self.truncate_text(product_name, 40)

                    data.append([truncated_name, quantity, total_price])

                user_name = logged_in_user

                # Add total amount
                formatted_total = self.format_price(self.total_price)  # ใช้ self.total_price ที่ได้จากการคำนวณ
                footer = Paragraph(f"ยอดรวมทั้งหมด: {formatted_total}", thai_style_right)

                # Header section (store information)
                current_date = QtCore.QDate.currentDate().toString('yyyy-MM-dd')
                heading_left = Paragraph(f"ร้าน: IT ZONE Shop<br/>วันที่: {current_date}<br/>ผู้ใช้: {user_name}", thai_style_left)

                # Create tables
                header_data = [[heading_left, footer]]
                header_table = Table(header_data, colWidths=[300, 300])
                header_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('FONTNAME', (0, 0), (-1, -1), 'THSarabun'), ('FONTSIZE', (0, 0), (-1, -1), 12)]))

                table = Table(data)
                table.setStyle(TableStyle([ 
                    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#DAE9F7')), 
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'), 
                    ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
                    ('ALIGN', (0, 1), (1, -1), 'LEFT'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTNAME', (0, 0), (-1, -1), 'THSarabun'),
                    ('FONTSIZE', (0, 0), (-1, -1), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ]))

                elements = [heading_center, header_table, table]
                pdf.build(elements)

                QtWidgets.QMessageBox.information(self, "สำเร็จ", "บันทึกใบเสร็จเป็น PDF เรียบร้อย")
            
            except Exception as e:
                print(f"Error while printing to PDF: {e}")
                QtWidgets.QMessageBox.warning(self, "ข้อผิดพลาด", "เกิดข้อผิดพลาดขณะพิมพ์ใบเสร็จเป็น PDF")

    def go_to_home(self):
        self.home_page = Homepage()  # สร้างหน้าแรก
        self.home_page.show()  # แสดงหน้าแรก
        self.close()  # ปิดหน้าต่างล็อกอิน



class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setStyleSheet("background-color: #ffffff; border-radius: 15px;")
        self.setGeometry(360, 110, 700, 650)
        self.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))

        # Layout หลัก
        main_layout = QtWidgets.QVBoxLayout()

        # สร้าง Layout สำหรับ top bar
        top_bar_layout = QtWidgets.QHBoxLayout()

        # ปุ่ม "กลับ"
        self.back_button = QtWidgets.QPushButton("←")
        self.back_button.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 12))
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #ff6666; 
                color: #ffffff; 
                border-radius: 10px; 
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #ff3333;
            }
        """)
        self.back_button.clicked.connect(self.go_to_home)

        # เพิ่มปุ่ม "กลับ" ลงใน top_bar_layout
        top_bar_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        
        # เพิ่ม top_bar_layout ใน main_layout
        main_layout.addLayout(top_bar_layout)

        # สร้าง QLabel สำหรับแสดงภาพและพื้นหลังไล่สี #
        logo_frame = QtWidgets.QFrame(self)
        logo_frame.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #3a7bd5, stop:1 #00d2ff
                );  /* ไล่สีจากน้ำเงินเข้มไปอ่อน */
                border-radius: 10px;
                padding: 3px;
            }
        """)
        logo_layout = QtWidgets.QVBoxLayout(logo_frame)

        # สร้าง QLabel สำหรับแสดงภาพ #
        self.image_label = QtWidgets.QLabel(self)
        
        # โหลดภาพด้วย QPixmap #
        pixmap = QtGui.QPixmap("image/IT TOP.png")
        if not pixmap.isNull():  # ตรวจสอบว่าภาพโหลดสำเร็จหรือไม่
            # สร้าง QGraphicsEffect เพื่อเพิ่มเงา #
            shadow = QtWidgets.QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setXOffset(0)
            shadow.setYOffset(0)
            shadow.setColor(QtGui.QColor(0, 0, 0, 120))  # สีเงาเป็นสีดำโปร่งใสเล็กน้อย

            # ตั้งค่าเงาสำหรับ QLabel #
            self.image_label.setGraphicsEffect(shadow)
            self.image_label.setPixmap(
                pixmap.scaled(250, 125,  # ปรับขนาดภาพให้ใหญ่ขึ้น
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation
                    )
                )  # ปรับขนาดภาพตามต้องการ
            logo_layout.addWidget(self.image_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)  # จัดกึ่งกลางภาพใน layout
        
        main_layout.addWidget(logo_frame, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # เพิ่มหัวข้อ "เข้าสู่ระบบ"
        title_label = QtWidgets.QLabel("ยินดีต้อนรับสู่ ไอทีโซน")
        title_label.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 16, QtGui.QFont.Weight.Bold))
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #000000;")
        main_layout.addWidget(title_label)

        title_label = QtWidgets.QLabel("เข้าสู่ระบบ")
        title_label.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 24, QtGui.QFont.Weight.Bold))
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #000000;")
        main_layout.addWidget(title_label)

        # Layout สำหรับแบบฟอร์มล็อกอิน
        form_layout = QtWidgets.QFormLayout()
        form_layout.setContentsMargins(50, 20, 50, 20)

        # ช่องกรอกชื่อผู้ใช้ #
        username_icon = QtWidgets.QLabel()
        username_icon.setPixmap(QtGui.QPixmap("image/user icon black.png").scaled(20, 20, QtCore.Qt.AspectRatioMode.KeepAspectRatio))  # ปรับขนาดไอคอน
        username_icon.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 14))
        self.username = QtWidgets.QLineEdit()
        self.username.setPlaceholderText("ชื่อผู้ใช้")
        self.username.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 14))
        self.username.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; 
                color: #2d3b4f; 
                border: 1px solid #d3d3d3;  /* เส้นกรอบสีเทา */
                border-radius: 10px; 
                padding: 10px;
            }
            QLineEdit:hover {
                background-color: #dcdcdc;  /* สีเมื่อเมาส์ชี้อยู่ */
            }
        """)
        username_layout = QtWidgets.QHBoxLayout()
        username_layout.addWidget(username_icon)
        username_layout.addWidget(self.username)

        # ช่องกรอกรหัสผ่าน #
        password_icon = QtWidgets.QLabel()
        password_icon.setPixmap(QtGui.QPixmap("image/password icon black.png").scaled(20, 20, QtCore.Qt.AspectRatioMode.KeepAspectRatio))  # ปรับขนาดไอคอน
        password_icon.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 14))
        self.password = QtWidgets.QLineEdit()
        self.password.setPlaceholderText("รหัสผ่าน")
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 14))
        self.password.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; 
                color: #2d3b4f; 
                border: 1px solid #d3d3d3;  /* เส้นกรอบสีเทา */
                border-radius: 10px; 
                padding: 10px;
            }
            QLineEdit:hover {
                background-color: #dcdcdc;  /* สีเมื่อเมาส์ชี้อยู่ */
            }
        """)
        password_layout = QtWidgets.QHBoxLayout()
        password_layout.addWidget(password_icon)
        password_layout.addWidget(self.password)

        form_layout.addRow(username_layout)
        form_layout.addRow(password_layout)

        # เพิ่มข้อความ "Forgot your password?" ใต้ช่องกรอกรหัสผ่าน
        forgot_password_label = QtWidgets.QLabel('<a href="forgot_password">Forgot your password?</a>')
        forgot_password_label.setOpenExternalLinks(False)  # ปิดการเปิดลิงก์อัตโนมัติ
        forgot_password_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)  # ตั้งตำแหน่งข้อความให้ชิดซ้าย
        forgot_password_label.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 12))
        forgot_password_label.setStyleSheet("color: #007bff;")  # เปลี่ยนสีข้อความเป็นสีน้ำเงิน

        # เพิ่ม margin ด้านซ้าย
        forgot_password_layout = QtWidgets.QHBoxLayout()
        forgot_password_layout.addWidget(forgot_password_label)
        forgot_password_layout.setContentsMargins(30, 0, 0, 0)  # เพิ่ม margin ด้านซ้าย

        # เชื่อมต่อ signal เมื่อคลิกที่ลิงก์
        forgot_password_label.linkActivated.connect(self.go_to_InputUnameOrEmail)

        # เพิ่ม forgot_password_layout ลงใน form_layout
        form_layout.addRow(forgot_password_layout)

        # เพิ่ม form_layout ใน main_layout
        main_layout.addLayout(form_layout)

        # ปุ่มเข้าสู่ระบบ
        self.login_button = QtWidgets.QPushButton("เข้าสู่ระบบ")
        self.login_button.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 14))
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #1F232D; 
                color: #ffffff; 
                border-radius: 20px; 
                padding: 10px; 
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background-color: #2A2E38;  
            }
        """)
        self.login_button.clicked.connect(self.login)
        main_layout.addWidget(self.login_button)


        # ปุ่มลงทะเบียน
        self.register_button = QtWidgets.QPushButton("ลงทะเบียน")
        self.register_button.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 14))
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #4195CC; 
                color: #ffffff; 
                border-radius: 20px; 
                padding: 10px; 
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background-color: #3178a1;  
            }
        """)
        self.register_button.clicked.connect(self.go_to_register)
        main_layout.addWidget(self.register_button)

        # ตั้งค่า layout หลัก
        self.setLayout(main_layout)


    def go_to_home(self):
        self.home_page = Homepage()  # สร้างหน้าแรก
        self.home_page.show()  # แสดงหน้าแรก
        self.close()  # ปิดหน้าต่างล็อกอิน

    def go_to_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

    def go_to_admin_editpage(self):
        self.admin_editpage_window = Admin_Editpage()
        self.admin_editpage_window.show()
        self.close()


    def go_to_InputUnameOrEmail(self):
        self.InputUnameOrEmail_window = InputUnameOrEmailWindow()
        self.InputUnameOrEmail_window.show()
        self.close()



    def login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()

        # ตรวจสอบว่าช่องชื่อผู้ใช้และรหัสผ่านไม่ว่างเปล่า
        if not username or not password:
            self.show_message("ข้อมูลไม่ครบ", "กรุณากรอกชื่อผู้ใช้และรหัสผ่าน!", QtWidgets.QMessageBox.Icon.Warning)
            return  # หยุดการทำงานหากข้อมูลไม่ครบ

        # เชื่อมต่อฐานข้อมูลและตรวจสอบข้อมูล
        connection = create_connection()  # เชื่อมต่อฐานข้อมูลจาก db.py
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT password, role FROM user_register WHERE uname = %s", (username,))
                result = cursor.fetchone()

                # เปรียบเทียบรหัสผ่าน
                if result and result[0] == password:
                    global logged_in_user  # ใช้ตัวแปร global
                    logged_in_user = username  # อัปเดตชื่อผู้ใช้ที่ล็อคอิน

                    # ดึงข้อมูล user id
                    global user_id
                    user_id = get_user_id(logged_in_user)

                    self.show_message("สำเร็จ", f"เข้าสู่ระบบสำเร็จ! User Name: {logged_in_user}", QtWidgets.QMessageBox.Icon.Information)

                    # ตรวจสอบว่าเป็น user หรือ admin
                    if result[1] == 'admin':
                        print('admin')
                        # self.go_to_home()
                        self.go_to_admin_editpage()  # ไปยังหน้าจัดการสินค้า
                    else:
                        self.go_to_home()  # ไปยังหน้าแรก
                else:
                    self.show_message("ผิดพลาด", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง!", QtWidgets.QMessageBox.Icon.Warning)

            except mysql.connector.Error as err:
                self.show_message("Error", f"Error: {err}", QtWidgets.QMessageBox.Icon.Critical)
            finally:
                cursor.close()
                connection.close()
        else:
            self.show_message("Error", "Connection failed!", QtWidgets.QMessageBox.Icon.Critical)

# =================================== Message แจ้งเตือน =====================================================

    def show_message(self, title, message, icon):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))
        msg_box.exec()


# =================================== Input Username or email WINDOWN =====================================================

class InputUnameOrEmailWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OTP Verification")
        self.setStyleSheet("background-color: #ffffff; border-radius: 15px;")
        self.setGeometry(420, 100, 700, 650)
        self.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))

        # Layout หลัก
        main_layout = QtWidgets.QVBoxLayout()

        # Layout สำหรับ top bar (ปุ่ม "กลับ")
        top_bar_layout = QtWidgets.QHBoxLayout()
        self.back_button = QtWidgets.QPushButton("← กลับ")
        self.back_button.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 12))
        self.back_button.setStyleSheet("""
            QPushButton { 
                background-color: #ff6666; 
                color: #ffffff; 
                border-radius: 10px; 
                padding: 5px; 
            }
            QPushButton:hover { 
                background-color: #ff3333; 
            }
        """)
        self.back_button.clicked.connect(self.go_to_login)
        top_bar_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        top_bar_layout.addStretch()  
        main_layout.addLayout(top_bar_layout)

        # Layout สำหรับหัวข้อ
        title_label = QtWidgets.QLabel("กรอก Username หรือ Email")
        title_label.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 18, QtGui.QFont.Weight.Bold))
        title_label.setStyleSheet("color: #000000;")
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # ช่องสำหรับกรอกข้อความ
        self.input_field = QtWidgets.QLineEdit()
        self.input_field.setPlaceholderText("กรอก Username หรือ Email")
        self.input_field.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 16))
        self.input_field.setFixedSize(500, 50)
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #f2f2f2;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        main_layout.addWidget(self.input_field, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # ปุ่มยืนยัน OTP
        self.verify_button = QtWidgets.QPushButton("SUBMIT")
        self.verify_button.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 18, QtGui.QFont.Weight.Bold))
        self.verify_button.setFixedSize(350, 70)
        self.verify_button.setStyleSheet("""
            QPushButton {
                background-color: #4195CC; 
                color: #ffffff; 
                border-radius: 13px; 
                padding: 10px; 
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #3178a1;
            }
        """)
        self.verify_button.clicked.connect(self.check_user_input)
        main_layout.addWidget(self.verify_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

    def check_user_input(self):
        user_input = self.input_field.text().strip()

        # ตรวจสอบว่า input ว่างหรือไม่
        if not user_input:
            self.show_message("Error", "กรุณากรอกข้อมูล", QtWidgets.QMessageBox.Icon.Warning)
            return

        try:
            # เชื่อมต่อฐานข้อมูล
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='db_itshop'
            )

            with connection.cursor(dictionary=True) as cursor:
                if user_input.endswith(".com"):
                    # ตรวจสอบกับ email
                    query = "SELECT user_id, email FROM user_register WHERE email = %s"
                else:
                    # ตรวจสอบกับ uname
                    query = "SELECT user_id, uname FROM user_register WHERE uname = %s"

                cursor.execute(query, (user_input,))
                result = cursor.fetchone()

                if result:
                    if 'user_id' in result:
                        user_id = result["user_id"]
                        self.show_message("Success", f"พบข้อมูล User ID: {user_id}", QtWidgets.QMessageBox.Icon.Information)
                        self.go_to_OTPWindow(user_id)
                    else:
                        self.show_message("Error", "ไม่พบข้อมูลที่ตรงกับที่คุณกรอก", QtWidgets.QMessageBox.Icon.Warning)
                else:
                    self.show_message("Not Found", "ไม่พบข้อมูลที่ตรงกับที่คุณกรอก", QtWidgets.QMessageBox.Icon.Warning)

        except pymysql.MySQLError as e:
            self.show_message("Database Error", f"เกิดข้อผิดพลาด: {str(e)}", QtWidgets.QMessageBox.Icon.Critical)

        finally:
            if 'connection' in locals() and connection:
                connection.close()

    def go_to_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def go_to_OTPWindow(self, user_id):
        self.OTP_window = OTPWindow(user_id)
        self.OTP_window.show()
        self.close()

    def show_message(self, title, message, icon):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))
        msg_box.exec()




# =================================== OTP WINDOWN =====================================================

class OTPWindow(QtWidgets.QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle("OTP Verification")
        self.setStyleSheet("background-color: #ffffff; border-radius: 15px;")
        self.setGeometry(420, 100, 700, 650)
        self.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))
        self.user_id = user_id
        self.user_email = self.get_user_email()
        self.user_otp = self.OTP_Generate()
        # print (self.user_id)
        # print (self.user_email)


        # กำหนดเวลาสำหรับการนับถอยหลัง (2 นาที = 120 วินาที)
        self.remaining_time = 180

        # Layout หลัก
        main_layout = QtWidgets.QVBoxLayout()

        # Layout สำหรับ top bar (ปุ่ม "กลับ")
        top_bar_layout = QtWidgets.QHBoxLayout()
        self.back_button = QtWidgets.QPushButton("← กลับ")
        self.back_button.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 12))
        self.back_button.setStyleSheet("""
            QPushButton { 
                background-color: #ff6666; 
                color: #ffffff; 
                border-radius: 10px; 
                padding: 5px; 
            }
            QPushButton:hover { 
                background-color: #ff3333; 
            }
        """)
        self.back_button.clicked.connect(self.go_to_login)
        top_bar_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        top_bar_layout.addStretch()  # ดันปุ่มไปซ้ายสุด
        main_layout.addLayout(top_bar_layout)

        # Layout สำหรับหัวข้อ
        title_label = QtWidgets.QLabel("ยืนยันรหัส OTP")
        title_label.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 18, QtGui.QFont.Weight.Bold))
        title_label.setStyleSheet("color: #000000;")
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Layout สำหรับหัวข้อ
        title_label = QtWidgets.QLabel(f'Enter OTP sent to your email {self.user_email}')
        title_label.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 18, QtGui.QFont.Weight.Bold))
        title_label.setStyleSheet("color: #000000;")
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Layout สำหรับช่องกรอก OTP
        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        otp_layout = QtWidgets.QHBoxLayout()
        otp_layout.setContentsMargins(30, 0, 30, 0)
        otp_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        otp_layout.setSpacing(20)  # เพิ่มระยะห่างระหว่างช่องกรอก OTP 10px

        # เพิ่ม SpacerItem ที่ข้างซ้ายและขวาของ otp_layout
        otp_layout.addSpacerItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))

        self.otp_inputs = []

        for i in range(6):
            otp_input = QtWidgets.QLineEdit()
            otp_input.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 18))
            otp_input.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            otp_input.setMaxLength(1)
            otp_input.setValidator(QtGui.QIntValidator(0, 9))
            otp_input.setFixedSize(50, 70)
            otp_input.setStyleSheet("""
                QLineEdit {
                    background-color: #ffffff; 
                    color: #2d3b4f; 
                    border: 1px solid #d3d3d3; 
                    border-radius: 5px; 
                    padding: 0px;
                }
            """)
            otp_input.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
            otp_input.textChanged.connect(lambda _, idx=i: self.focus_next_input(idx))
            otp_layout.addWidget(otp_input)
            self.otp_inputs.append(otp_input)

        # เพิ่ม SpacerItem เพื่อให้ otp_layout อยู่กลาง
        otp_layout.addSpacerItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum))

        content_layout.addLayout(otp_layout)

        # Layout สำหรับ Time Remaining และ Resend Label
        otp_bottom_layout = QtWidgets.QHBoxLayout()

        # Time Remaining Label
        self.timer_label = QtWidgets.QLabel("Time Remaining 03:00 s")
        self.timer_label.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 12))
        self.timer_label.setStyleSheet("color: #555555; padding-left: 60px;")

        # สร้าง QTimer เพื่ออัปเดตเวลา
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # อัปเดตทุก 1000ms (1 วินาที)

        # Resend OTP Label
        self.resend_label = QtWidgets.QLabel('<a href="#">Resend OTP</a>')
        self.resend_label.setOpenExternalLinks(False)
        self.resend_label.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 12))
        self.resend_label.setStyleSheet("color: #E28F00; padding-left: 20px;")
        self.resend_label.linkActivated.connect(self.resend_otp)

        # จัดข้อความทั้งสองให้อยู่ตรงกลาง
        otp_bottom_layout.addWidget(self.timer_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        otp_bottom_layout.addWidget(self.resend_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # เพิ่ม otp_bottom_layout ลงใน content_layout
        content_layout.addLayout(otp_bottom_layout)

        main_layout.addLayout(content_layout)

        # ปุ่มยืนยัน OTP
        self.verify_button = QtWidgets.QPushButton("SUBMIT")
        self.verify_button.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 18, QtGui.QFont.Weight.Bold))
        self.verify_button.setFixedSize(350, 70)
        self.verify_button.setStyleSheet("""
            QPushButton {
                background-color: #4195CC; 
                color: #ffffff; 
                border-radius: 13px; 
                padding: 10px; 
                margin-top: 20px;
                
            }
            QPushButton:hover {
                background-color: #3178a1;
            }
        """)
        self.verify_button.clicked.connect(self.OTP_Verify)
        main_layout.addWidget(self.verify_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)
        



    def focus_next_input(self, idx):
        """เปลี่ยนโฟกัสไปที่ช่องถัดไปเมื่อกรอกตัวเลขเสร็จ"""
        if idx < len(self.otp_inputs) - 1 and self.otp_inputs[idx].text():
            self.otp_inputs[idx + 1].setFocus()


    #อัปเดตข้อความใน timer_label และลดเวลาที่เหลือ
    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.timer_label.setText(f"Time Remaining {minutes:02}:{seconds:02} s")
        else:
            self.timer.stop()
            self.timer_label.setText("Time's up!")
            self.handle_timeout()


    # ฟังก์ชันเมื่อเวลาหมด
    def handle_timeout(self):
        QtWidgets.QMessageBox.warning(self, "Time's Up", "OTP verification time has expired.")

    def get_user_email(self):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='db_itshop'
        )
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT email FROM user_register WHERE user_id = %s"
            cursor.execute(query, (self.user_id,))  # ใช้ self.user_id แทน user_id ตรงๆ
            result = cursor.fetchone()

            if result:
                return result['email']  # คืนค่า email
            return None  # กรณีไม่พบข้อมูล
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return None
        finally:
            cursor.close()
            connection.close()


    def OTP_Generate(self):
        # ตรวจสอบว่า self.user_email เป็น None หรือไม่
        if not self.user_email:
            self.show_message("Error", "Email not found or invalid.", QtWidgets.QMessageBox.Icon.Warning)
            return None  # หยุดการทำงานหากอีเมลไม่ถูกต้อง

        otp = "".join(str(random.randint(0, 9)) for _ in range(6))

        # การตั้งค่า SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        from_mail = 'shopitzone57@gmail.com'
        server.login(from_mail, 'qvkw uvun fodm ecui')
        to_mail = self.user_email  # ใช้อีเมลที่ดึงจากฐานข้อมูล

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
                <p>This OTP is valid for the next 3 minutes. If you did not request this, please ignore this email.</p>
                <div class="footer">
                    <p>© 2024 IT Zone Shop. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        # ใส่ HTML เนื้อหาเข้าไปใน Email
        msg.add_alternative(html_content, subtype='html')

        # ส่ง Email
        try:
            server.send_message(msg)
            print('Email sent')
        except Exception as e:
            print(f"Error sending email: {e}")
        finally:
            server.quit()

        return otp
    

    def OTP_Verify(self):
        # ดึงค่าที่ผู้ใช้กรอกจากแต่ละช่องใน self.otp_inputs
        otp_input = ''.join([otp_input.text() for otp_input in self.otp_inputs])

        # ตรวจสอบว่า OTP ที่กรอกตรงกับ OTP ที่ถูกสร้าง
        if otp_input == self.user_otp:
            # OTP ถูกต้อง
            self.show_message("Success", "OTP verified successfully!", QtWidgets.QMessageBox.Icon.Information)
            self.go_to_reset_password(self.user_id)
        else:
            # OTP ไม่ถูกต้อง
            self.show_message("Error", "Invalid OTP. Please try again.", QtWidgets.QMessageBox.Icon.Warning)


    def resend_otp(self):
        # สร้าง OTP ใหม่
        new_otp = self.OTP_Generate()

        if new_otp:
            # รีเซ็ตเวลานับถอยหลัง (ตั้งใหม่ที่ 180 วินาที)
            self.remaining_time = 180
            self.timer.start(1000)

            # อัปเดต self.user_otp ให้เป็น OTP ใหม่
            self.user_otp = new_otp

            # แสดงข้อความว่า OTP ใหม่ถูกส่งแล้ว
            self.show_message("OTP Sent", "A new OTP has been sent to your email.", QtWidgets.QMessageBox.Icon.Information)

            # อัปเดตข้อความใน timer_label เพื่อแสดงเวลาใหม่
            self.timer_label.setText("Time Remaining 03:00 s")

            # รีเซ็ตช่องกรอก OTP
            for otp_input in self.otp_inputs:
                otp_input.clear()
        else:
            # หากไม่สามารถสร้าง OTP ได้ ให้แสดงข้อความผิดพลาด
            self.show_message("Error", "Failed to generate a new OTP. Please try again.", QtWidgets.QMessageBox.Icon.Warning)


    def go_to_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


    def go_to_reset_password(self, user_id):
        self.reset_password_window = ResetPasswordWindow(user_id)
        self.reset_password_window.show()
        self.close()


    def show_message(self, title, message, icon):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))
        msg_box.exec()




# =================================== RESET PASSWORD WINDOWN =====================================================

class ResetPasswordWindow(QtWidgets.QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle("Reset Password")
        self.setStyleSheet("background-color: #ffffff; border-radius: 15px;")
        self.setGeometry(420, 100, 700, 650)
        self.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))
        self.user_id = user_id

        # Layout หลัก
        main_layout = QtWidgets.QVBoxLayout()

        # Layout สำหรับ top bar (ปุ่ม "กลับ")
        top_bar_layout = QtWidgets.QHBoxLayout()
        self.back_button = QtWidgets.QPushButton("← กลับ")
        self.back_button.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 12))
        self.back_button.setStyleSheet("""
            QPushButton { 
                background-color: #ff6666; 
                color: #ffffff; 
                border-radius: 10px; 
                padding: 5px; 
            }
            QPushButton:hover { 
                background-color: #ff3333; 
            }
        """)
        self.back_button.clicked.connect(self.go_to_login)
        top_bar_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        top_bar_layout.addStretch()
        main_layout.addLayout(top_bar_layout)

        # Layout สำหรับหัวข้อ
        title_label = QtWidgets.QLabel("Reset Password")
        title_label.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 18, QtGui.QFont.Weight.Bold))
        title_label.setStyleSheet("color: #000000;")
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # ช่องสำหรับกรอก Password ใหม่
        self.new_password_field = QtWidgets.QLineEdit()
        self.new_password_field.setPlaceholderText("กรอก Password ใหม่")
        self.new_password_field.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 16))
        self.new_password_field.setFixedSize(500, 50)
        self.new_password_field.setStyleSheet("""
            QLineEdit {
                background-color: #f2f2f2;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        self.new_password_field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)  # ทำให้แสดงเป็นจุด
        main_layout.addWidget(self.new_password_field, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # ช่องยืนยันรหัสผ่าน
        self.confirm_password_field = QtWidgets.QLineEdit()
        self.confirm_password_field.setPlaceholderText("ยืนยัน Password อีกครั้ง")
        self.confirm_password_field.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 16))
        self.confirm_password_field.setFixedSize(500, 50)
        self.confirm_password_field.setStyleSheet("""
            QLineEdit {
                background-color: #f2f2f2;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        # สำหรับการตั้งค่า EchoMode เป็นรหัสผ่าน
        self.confirm_password_field.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        main_layout.addWidget(self.confirm_password_field, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # ปุ่มยืนยัน
        self.verify_button = QtWidgets.QPushButton("SUBMIT")
        self.verify_button.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 18, QtGui.QFont.Weight.Bold))
        self.verify_button.setFixedSize(350, 70)
        self.verify_button.setStyleSheet("""
            QPushButton {
                background-color: #4195CC; 
                color: #ffffff; 
                border-radius: 13px; 
                padding: 10px; 
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #3178a1;
            }
        """)
        self.verify_button.clicked.connect(self.update_new_password)
        main_layout.addWidget(self.verify_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)


    def go_to_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


    def update_new_password(self):
        # ดึงค่าจาก input_field (รหัสผ่านใหม่และการยืนยันรหัสผ่าน)
        new_password = self.new_password_field.text().strip()
        confirm_password = self.confirm_password_field.text().strip()

        # ตรวจสอบความถูกต้องของรหัสผ่าน
        if new_password != confirm_password:
            self.show_message("Error", "รหัสผ่านไม่ตรงกัน กรุณากรอกใหม่", QtWidgets.QMessageBox.Icon.Warning)
            return
        
        if not new_password:
            self.show_message("Error", "กรุณากรอกรหัสผ่านใหม่", QtWidgets.QMessageBox.Icon.Warning)
            return

        try:
            # เชื่อมต่อกับฐานข้อมูล
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='db_itshop'
            )

            # สร้างคำสั่ง SQL เพื่ออัพเดตข้อมูลรหัสผ่าน
            query = "UPDATE user_register SET password = %s WHERE user_id = %s"

            # ทำการ execute คำสั่ง
            with connection.cursor() as cursor:
                cursor.execute(query, (new_password, self.user_id))
                connection.commit()

            # แสดงข้อความเมื่อทำการอัพเดตสำเร็จ
            self.show_message("Success", "รหัสผ่านถูกอัพเดตเรียบร้อยแล้ว", QtWidgets.QMessageBox.Icon.Information)
            self.go_to_login()  # หลังจากอัพเดตเสร็จ ไปที่หน้าล็อกอิน

        except mysql.connector.Error as e:
            self.show_message("Database Error", f"เกิดข้อผิดพลาด: {str(e)}", QtWidgets.QMessageBox.Icon.Critical)

        finally:
            if 'connection' in locals() and connection:
                connection.close()


    def show_message(self, title, message, icon):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))
        msg_box.exec()




# =================================== REGISTER WINDOWN =====================================================

class RegisterWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setStyleSheet("background-color: #ffffff; border-radius: 15px;")
        self.setGeometry(360, 110, 700, 650)
        layout = QtWidgets.QVBoxLayout()
        self.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))

        # Back Button #
        self.back_button = QtWidgets.QPushButton("←")
        self.back_button.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 12))
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #ff6666; 
                color: #ffffff; 
                border-radius: 10px; 
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #ff3333;
            }
        """)
        self.back_button.clicked.connect(self.go_to_login)
        layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        # Title Label #
        title_label = QtWidgets.QLabel("ลงทะเบียน")
        title_label.setFont(QtGui.QFont("PK Nakhon Pathom Pathom Demo", 24, QtGui.QFont.Weight.Bold))
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #000000; background: transparent;")  # ตั้งค่าพื้นหลังโปร่งใส
        layout.addWidget(title_label)     

        # Form Layout #
        form_layout = QtWidgets.QFormLayout()
        form_layout.setContentsMargins(50, 20, 50, 20)

        # Username  #
        username_icon = QtWidgets.QLabel()
        username_icon.setPixmap(QtGui.QPixmap("image/user icon black.png").scaled(20, 20, QtCore.Qt.AspectRatioMode.KeepAspectRatio))  # ปรับขนาดไอคอน
        username_icon.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 14))
        username_icon.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)  # ทำให้ QLabel ไม่รับการคลิก
        username_icon.setStyleSheet("background: transparent;")  # ตั้งค่าพื้นหลังโปร่งใส
        self.username = QtWidgets.QLineEdit()
        self.username.setPlaceholderText("ชื่อผู้ใช้")
        self.username.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 14))
        self.username.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; 
                color: #2d3b4f; 
                border: 1px solid #d3d3d3;  /* เส้นกรอบสีเทา */
                border-radius: 10px; 
                padding: 10px;
            }
            QLineEdit:hover {
                background-color: #dcdcdc;  /* สีเมื่อเมาส์ชี้อยู่ */
            }
        """)
        self.username.textChanged.connect(self.check_username_format)  # เชื่อมต่อ signal เพื่อตรวจสอบการเปลี่ยนแปลงของข้อความ
        self.username.textChanged.connect(self.check_username_format2)
        # Error Label for Username #
        self.username_error_label = QtWidgets.QLabel("")
        self.username_error_label.setStyleSheet("color: red;")
        self.username_error_label.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 10))

        layout.addWidget(self.username)
        layout.addWidget(self.username_error_label)  # เพิ่ม label สำหรับแสดงข้อความเตือน
        self.setLayout(layout)
        username_layout = QtWidgets.QHBoxLayout()
        username_layout.addWidget(username_icon)
        username_layout.addWidget(self.username)
        form_layout.addRow(username_layout)
        form_layout.addRow(self.username_error_label)


        # Password  #
        password_icon = QtWidgets.QLabel()
        password_icon.setPixmap(QtGui.QPixmap("image/password icon black.png").scaled(20, 20, QtCore.Qt.AspectRatioMode.KeepAspectRatio))  # ปรับขนาดไอคอน
        password_icon.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 14))
        password_icon.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)  # ทำให้ QLabel ไม่รับการคลิก
        password_icon.setStyleSheet("background: transparent;")  # ตั้งค่าพื้นหลังโปร่งใส
        self.password = QtWidgets.QLineEdit()
        self.password.setPlaceholderText("รหัสผ่าน")
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 14))
        self.password.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; 
                color: #2d3b4f; 
                border: 1px solid #d3d3d3;  /* เส้นกรอบสีเทา */
                border-radius: 10px; 
                padding: 10px;
            }
            QLineEdit:hover {
                background-color: #dcdcdc;  /* สีเมื่อเมาส์ชี้อยู่ */
            }
        """)

        # QLabel สำหรับแสดงข้อความแจ้งเตือน
        self.password_error_label = QtWidgets.QLabel("")
        self.password_error_label.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 12))
        self.password_error_label.setStyleSheet("color: red;")  # ข้อความสีแดง

        # เพิ่มการตรวจสอบความยาวรหัสผ่าน
        self.password.textChanged.connect(self.validate_password)

        password_layout = QtWidgets.QHBoxLayout()
        password_layout.addWidget(password_icon)
        password_layout.addWidget(self.password)
        
        form_layout.addRow(password_layout)
        form_layout.addRow(self.password_error_label) 

        # Phone Number  #
        phone_icon = QtWidgets.QLabel()
        phone_icon.setPixmap(QtGui.QPixmap("image/phone icon black.png").scaled(20, 20, QtCore.Qt.AspectRatioMode.KeepAspectRatio))  # ปรับขนาดไอคอน
        phone_icon.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 14))
        phone_icon.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)  # ทำให้ QLabel ไม่รับการคลิก
        phone_icon.setStyleSheet("background: transparent;")  # ตั้งค่าพื้นหลังโปร่งใส
        self.phone_number = QtWidgets.QLineEdit()
        self.phone_number.setPlaceholderText("เบอร์โทร")
        self.phone_number.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 14))
        self.phone_number.setMaxLength(12)  # จำกัดความยาวเบอร์โทร
        self.phone_number.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; 
                color: #2d3b4f; 
                border: 1px solid #d3d3d3;  /* เส้นกรอบสีเทา */
                border-radius: 10px; 
                padding: 10px;
            }
            QLineEdit:hover {
                background-color: #dcdcdc;  /* สีเมื่อเมาส์ชี้อยู่ */
            }
        """)
        self.phone_number.textChanged.connect(self.validate_phone_number)  # เชื่อมต่อ signal เพื่อตรวจสอบเบอร์โทร

        # Error Label for Phone Number
        self.phone_error_label = QtWidgets.QLabel("")
        self.phone_error_label.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 10))
        self.phone_error_label.setStyleSheet("color: red;")

        phone_layout = QtWidgets.QHBoxLayout()
        phone_layout.addWidget(phone_icon)
        phone_layout.addWidget(self.phone_number)
        form_layout.addRow(phone_layout)
        form_layout.addRow(self.phone_error_label)  # เพิ่มข้อความแจ้งเตือน

        # Email  #
        email_icon = QtWidgets.QLabel()
        email_icon.setPixmap(QtGui.QPixmap("image/email icon black.png").scaled(20, 20, QtCore.Qt.AspectRatioMode.KeepAspectRatio))  # ปรับขนาดไอคอน
        email_icon.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 14))
        email_icon.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)  # ทำให้ QLabel ไม่รับการคลิก
        email_icon.setStyleSheet("background: transparent;")  # ตั้งค่าพื้นหลังโปร่งใส
        self.email = QtWidgets.QLineEdit()
        self.email.setPlaceholderText("อีเมล")
        self.email.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 14))
        self.email.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff; 
                color: #2d3b4f; 
                border: 1px solid #d3d3d3;  /* เส้นกรอบสีเทา */
                border-radius: 10px; 
                padding: 10px;
            }
            QLineEdit:hover {
                background-color: #dcdcdc;  /* สีเมื่อเมาส์ชี้อยู่ */
            }
        """)
        email_layout = QtWidgets.QHBoxLayout()
        email_layout.addWidget(email_icon)
        email_layout.addWidget(self.email)
        form_layout.addRow(email_layout)

        layout.addLayout(form_layout)
        self.setLayout(layout)



        # ปุ่มลงทะเบียน #
        self.register_button = QtWidgets.QPushButton("ลงทะเบียน")
        self.register_button.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 14))
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #4195CC; 
                color: #ffffff; 
                border-radius: 20px; 
                padding: 10px; 
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background-color: #3178a1;  /* สีเมื่อเมาส์ชี้อยู่ */
            }
        """)
        self.register_button.clicked.connect(self.submit_form)
        layout.addWidget(self.register_button)
        self.setLayout(layout)

    def submit_form(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        phone_number = self.phone_number.text().strip()
        email = self.email.text().strip()

        # ตรวจสอบว่าช่องทั้งหมดไม่ว่างเปล่า
        if not username or not password or not phone_number or not email:
            self.show_message("ข้อมูลไม่ครบ", "กรุณากรอกข้อมูลในทุกช่อง!", QtWidgets.QMessageBox.Icon.Warning)
            return

        # เรียกใช้ add_applicant เพื่อเพิ่มข้อมูลในฐานข้อมูล
        self.add_applicant(username, password, phone_number, email)
        self.go_to_login()

    def check_username_format2(self):
        """ตรวจสอบเงื่อนไขชื่อผู้ใช้"""
        username_text = self.username.text()
        if len(username_text) < 4:  # ตรวจสอบความยาวอย่างน้อย 4 ตัวอักษร
            self.username_error_label.setText("ตัวแรกต้องเป็นตัวพิมพ์ใหญ่และต้องมีอย่างน้อย 4 ตัวอักษร")
            self.username_error_label.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 12))
        elif " " in username_text:  # ตรวจสอบห้ามมีช่องว่าง
            self.username_error_label.setText("ชื่อผู้ใช้ห้ามมีช่องว่าง")
        else:
            self.username_error_label.setText("")  # ล้างข้อความเตือนหากชื่อผู้ใช้ผ่านเงื่อนไข

    def check_username_format(self):
        text = self.username.text()
        # ตรวจสอบว่าตัวอักษรแรกเป็นตัวพิมพ์ใหญ่หรือไม่
        if text and not text[0].isupper():
            self.username.setToolTip("ตัวอักษรแรกต้องเป็นตัวพิมพ์ใหญ่เท่านั้น")  # แสดงข้อความแจ้งเตือนเมื่อไม่เป็นตัวพิมพ์ใหญ่
            self.username.setStyleSheet("""
                QLineEdit {
                    background-color: #ffffff; 
                    color: #ff0000;  /* ข้อความสีแดงเมื่อผิดพลาด */
                    border: 1px solid #d3d3d3;
                    border-radius: 10px; 
                    padding: 10px;
                }
            """)
        else:
            self.username.setToolTip("")  # ล้างข้อความเตือนเมื่อข้อมูลถูกต้อง
            self.username.setStyleSheet("""
                QLineEdit {
                    background-color: #ffffff; 
                    color: #2d3b4f;  /* กลับไปเป็นสีปกติ */
                    border: 1px solid #d3d3d3;
                    border-radius: 10px; 
                    padding: 10px;
                }
            """)

    def add_applicant(self, username, password, phone_number, email):
        role = "user"
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                sql = "INSERT INTO user_register (uname, password, phone_number, email, role) VALUES (%s, %s, %s, %s, %s)"
                values = (username, password, phone_number, email, role)
                
                cursor.execute(sql, values)
                connection.commit()
                self.show_message("สำเร็จ", f"Applicant '{username}' added successfully.", QtWidgets.QMessageBox.Icon.Information)
            except mysql.connector.Error as err:
                self.show_message("Error", f"Error: {err}", QtWidgets.QMessageBox.Icon.Critical)
            finally:
                cursor.close()
                connection.close()
        else:
            self.show_message("Error", "Connection failed!", QtWidgets.QMessageBox.Icon.Critical)

    def validate_password(self):
        """ตรวจสอบความยาวของรหัสผ่าน"""
        password_text = self.password.text()
        if len(password_text) < 6:
            self.password_error_label.setText("รหัสต้องมีอย่างน้อย 6 ตัวอักษร")
        else:
            self.password_error_label.setText("") 

    def validate_phone_number(self):
        """ตรวจสอบว่าเบอร์โทรไม่มีขีดกลาง -"""
        phone_text = self.phone_number.text()
        if "-" in phone_text:
            self.phone_error_label.setText("ไม่ต้องมี '-'")
            self.phone_error_label.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 12))
        else:
            self.phone_error_label.setText("")  # ล้างข้อความแจ้งเตือนหากไม่มีขีดกลาง 

    def show_message(self, title, message, icon):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))
        msg_box.exec()

    def go_to_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
    
# =================================== แชท-ติดต่อ =====================================================

class ContactWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ติดต่อเรา - แชท")
        self.setStyleSheet("background-color: #ffffff; border-radius: 15px;")
        self.setGeometry(400, 200, 600, 500)
        self.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))
        layout = QtWidgets.QVBoxLayout()

        # หัวข้อสำหรับหน้าต่างแชท
        title_label = QtWidgets.QLabel("แชทกับเรา")
        title_label.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 24, QtGui.QFont.Weight.Bold))     
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2d3b4f; padding-bottom: 10px;")
        layout.addWidget(title_label)

        # พื้นที่แสดงแชท (อ่านอย่างเดียว)
        self.chat_display = QtWidgets.QTextEdit()
        self.chat_display.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 12))
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background-color: #f0f0f0; color: #2d3b4f; border-radius: 10px; padding: 10px;")
        layout.addWidget(self.chat_display, stretch=2)

        # ช่องกรอกข้อความของผู้ใช้
        self.message_input = QtWidgets.QLineEdit()
        self.message_input.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 12))
        self.message_input.setPlaceholderText("พิมพ์ข้อความของคุณ...")
        self.message_input.setStyleSheet("background-color: #ffffff; color: #2d3b4f; border-radius: 10px; padding: 10px;")
        layout.addWidget(self.message_input)

        # ปุ่มส่งข้อความ
        send_button = QtWidgets.QPushButton("ส่ง")
        send_button.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 12))
        send_button.setStyleSheet("""
            QPushButton {
                background-color: #4195CC; 
                color: #ffffff; 
                border-radius: 10px; 
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3178a1;
            }
        """)
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        # ปุ่มปิดที่ด้านล่าง
        close_button = QtWidgets.QPushButton("ปิด")
        close_button.setFont(QtGui.QFont("PK Nakhon Pathom Demo", 12))
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #ff6666; 
                color: #ffffff; 
                border-radius: 10px; 
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #ff3333;
            }
        """)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def send_message(self):
        user_message = self.message_input.text()
        if user_message:
            # แสดงข้อความของผู้ใช้ในพื้นที่แชท
            self.chat_display.append(f"<b>คุณ:</b> {user_message}")
            
            # ตัวอย่างการตอบกลับจากผู้ช่วย (สามารถเปลี่ยนเป็นลอจิกจริงได้)
            bot_response = "ขอบคุณที่ติดต่อเรา! เราจะติดต่อกลับโดยเร็วที่สุด"
            self.chat_display.append(f"<b>แอดมิน:</b> {bot_response}")
            
            # ล้างช่องกรอกข้อความ
            self.message_input.clear()

# ===================================COMSET PAGE ==================================================#

class ComsetWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Comset_page')
        self.setStyleSheet('background-color: #ffffff; border-radius: 15px;')
        self.showMaximized()
        self.setWindowIcon(QIcon('image/IT ZONE LOGO.png'))


        # สร้าง container แนวตั้งมาเป็น layout หลัก
        Main_Layout = QtWidgets.QVBoxLayout()  # สร้าง instance ของ QVBoxLayout
        self.setLayout(Main_Layout)  
        Main_Layout.setContentsMargins(0, 0, 0, 0)
        


# ========================= MENU TOP BAR PART ========================= #

        # สร้าง MenuBar_Widget และเพิ่ม title
        self.MenuBar_Widget = QWidget()
        self.MenuBar_Area = QHBoxLayout(self.MenuBar_Widget)
        self.MenuBar_Widget.setFixedHeight(100)  # ความสูงเมนูด้านบน
        self.MenuBar_Widget.setStyleSheet('background-color: #295CA5; border-radius: 0px;')

# ============================================ ITZONE ICON ซ้ายบน ============================================ #    

        icon_ITZONE_label = QLabel(self)
        icon_pixmap = QPixmap("assets/image/ITZONEEDIT W.png")  # ระบุที่อยู่ของไฟล์ไอคอน
        icon_pixmap = icon_pixmap.scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_ITZONE_label.setPixmap(icon_pixmap)

        IT_ZONE_TOP_TITLE = QWidget()
        IT_ZONE_TOP_TITLE.setLayout(QHBoxLayout())
        IT_ZONE_TOP_TITLE.layout().addWidget(icon_ITZONE_label)

        self.MenuBar_Area.addWidget(IT_ZONE_TOP_TITLE)

# ============================================ SEARCHBAR ด้านบน ============================================ #        
        # เพิ่มแถบค้นหา
        search_bar_container = QWidget()
        search_bar_layout = QHBoxLayout(search_bar_container)
        search_bar_layout.setContentsMargins(0, 0, 0, 0)

        # สร้าง QLineEdit สำหรับแถบค้นหา
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("ค้นหาสินค้า...")
        search_bar.setFixedHeight(30)
        search_bar.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;  /* กำหนดสีของข้อความที่พิมพ์ลงไปในช่องค้นหา */
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
                padding-left: 10px;
                font-size: 14px;
                font-family: 'PK Nakhon Pathom Demo';
            }
            QLineEdit::placeholder { 
                color: gray;  /* เปลี่ยนเป็นสีที่คุณต้องการ */
                font-family: 'PK Nakhon Pathom Demo';
            }
        """)

        # สร้าง QLabel สำหรับไอคอนแว่นขยาย
        search_icon = QLabel()
        icon_pixmap = QPixmap("assets/image/magnifying glass icon.png").scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        search_icon.setPixmap(icon_pixmap)
        search_icon.setStyleSheet("""
            background-color: #295CA5;
            border-top-right-radius: 15px;
            border-bottom-right-radius: 15px;
            padding: 5px;
        """)

        # ใส่ search_bar และ search_icon ลงใน layout ของ search_bar_container
        search_bar_layout.addWidget(search_bar)
        search_bar_layout.addWidget(search_icon)

        # เพิ่ม search_bar_container ลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(search_bar_container)
        

# ============================================ ABOUT US ปุ่ม ============================================ #

        # สร้างปุ่มสำหรับรถเข็นสินค้า
        contact_button = QPushButton("   About us")
        contact_button.setIcon(QIcon("assets/image/contact icon.png"))  # ระบุ path ไปยังไอคอนรถเข็น
        contact_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        contact_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม
        contact_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)
        contact_button.clicked.connect(self.go_to_contactus)
        # ตั้งค่าฟอนต์
        contact_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        contact_button.setFont(contact_button_font)

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(contact_button)



# ============================================ รถเข็นสินค้า ============================================ #

        # สร้างปุ่มสำหรับรถเข็นสินค้า
        cart_button = QPushButton("   รถเข็นสินค้า")
        cart_button.setIcon(QIcon("assets/image/cart icon.png"))  # ระบุ path ไปยังไอคอนรถเข็น
        cart_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        cart_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม
        cart_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)
        if logged_in_user == None:
            cart_button.clicked.connect(
                lambda: self.show_message("ยังไม่ล็อคอิน", "กรุณาล็อคอินเข้าสู่ระบบก่อน!", QtWidgets.QMessageBox.Icon.Warning)
            )
        else:
            cart_button.clicked.connect(self.go_to_cart)
        # ตั้งค่าฟอนต์
        cart_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        cart_button.setFont(cart_button_font)
        # cart_button.clicked.connect()

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(cart_button)

# ============================================ เข้าสู่ระบบ ============================================ #

        # # ใช้ global เพื่อตรวจสอบข้อมูลผู้ใช้งาน
        # global logged_in_user

        # ตรวจสอบว่ามีผู้ใช้งานล็อกอินหรือไม่
        if logged_in_user:
            # ถ้ามีผู้ใช้งานล็อกอิน แสดงชื่อผู้ใช้งานในปุ่ม
            user_button = QPushButton(f"   {logged_in_user}")
        else:
            # ถ้าไม่มีผู้ใช้งาน แสดงปุ่มเข้าสู่ระบบ
            user_button = QPushButton("   เข้าสู่ระบบ")

        # ตั้งค่าไอคอน
        user_button.setIcon(QIcon("assets/image/user icon.png"))  # ระบุ path ไปยังไอคอน
        user_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        user_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม

        # ตั้งค่า StyleSheet
        user_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)

        # ตั้งค่าฟอนต์
        user_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        user_button.setFont(user_button_font)
        user_button.clicked.connect(self.go_to_login)

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(user_button)

        # เพิ่ม MenuBar_Widget ลงใน Main_Layout
        Main_Layout.addWidget(self.MenuBar_Widget)
        

# ================================================================= 

#                         - CONTENT PART -

# ================================================================= 

        # สร้าง Container ของ MainContent ไว้เพื่อใส่เนื้อหา
        self.MainContent_Widget = QWidget()
        self.MainContent_Area = QHBoxLayout(self.MainContent_Widget)
        Main_Layout.addWidget(self.MainContent_Widget)
        self.MainContent_Widget.setContentsMargins(0, 0, 0, 0)
        self.MainContent_Area.setContentsMargins(0, 0, 0, 0)
        self.MainContent_Area.setAlignment(Qt.AlignmentFlag.AlignLeft)
# ========================= เมนูด้านแถบซ้าย ========================= #

        # สร้าง SideBar Menu เพื่อเพิ่มเมนู
        self.SideBar_Widget = QWidget()
        self.SideBar_Area = QVBoxLayout(self.SideBar_Widget)
        self.SideBar_Widget.setFixedWidth(80)  # กำหนดความกว้างของแถบด้านซ้าย
        self.SideBar_Widget.setStyleSheet('background-color: #295CA5; border-radius: 0px;')
        self.SideBar_Area.setContentsMargins(0, 0, 0, 0)

# ============================================ COMSET Button ============================================ #

        self.COMSET_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.COMSET_ICON.setIcon(QIcon("assets/image/COMSET icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.COMSET_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.COMSET_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.COMSET_ICON.clicked.connect(self.go_to_comset)
        self.SideBar_Area.addWidget(self.COMSET_ICON)

# ============================================ NOTEBOOK Button ============================================ #

        self.NOTEBOOK_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.NOTEBOOK_ICON.setIcon(QIcon("assets/image/NOTEBOOK icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.NOTEBOOK_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.NOTEBOOK_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.NOTEBOOK_ICON.clicked.connect(self.go_to_notebook)
        self.SideBar_Area.addWidget(self.NOTEBOOK_ICON)

# ============================================ PHONE Button ============================================ #

        self.PHONE_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.PHONE_ICON.setIcon(QIcon("assets/image/PHONE icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.PHONE_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.PHONE_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.PHONE_ICON.clicked.connect(self.go_to_phone)
        self.SideBar_Area.addWidget(self.PHONE_ICON)

# ============================================ HEADPHONE Button ============================================ #

        self.HEADPHONE_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.HEADPHONE_ICON.setIcon(QIcon("assets/image/HEADPHONE icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.HEADPHONE_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.HEADPHONE_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.HEADPHONE_ICON.clicked.connect(self.go_to_headphone)
        self.SideBar_Area.addWidget(self.HEADPHONE_ICON)

# ============================================ EXIT Button ============================================ #

        self.EXIT_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.EXIT_ICON.setIcon(QIcon("assets/image/EXIT icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.EXIT_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.EXIT_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.EXIT_ICON.clicked.connect(self.go_to_login)

        self.SideBar_Area.addWidget(self.EXIT_ICON) 
        self.EXIT_ICON.setContentsMargins(0, 0, 0, 0)       

        self.MainContent_Area.addWidget(self.SideBar_Widget)

    # ========================= สร้าง หน้าแสดงรายการสินค้า ============================= #

        # Scroll Area
        self.content_area = QtWidgets.QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setContentsMargins(0, 0, 0, 0)

        # Content widget
        self.content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QGridLayout(self.content_widget)  # เปลี่ยนเป็น QGridLayout
        self.content_widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.content_area.setWidget(self.content_widget)
        self.content_widget.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(20)
        self.content_layout.setContentsMargins(10, 10, 10, 10)


        # กำหนดจำนวนคอลัมน์ที่ต้องการในกริด
        self.columns = 4
        self.display_products()

    def display_products(self):
        # ดึงข้อมูลสินค้า
        products = get_comset_products()

        # กำหนดค่าตัวแปรแถวและคอลัมน์สำหรับการแสดงสินค้า
        row = 0
        col = 0

        # Loop for adding product widgets
        for product in products:
            # Widget สำหรับแสดงผลสินค้าแต่ละรายการ
            product_widget = QtWidgets.QWidget()
            product_layout = QtWidgets.QVBoxLayout(product_widget)
            product_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # รูปภาพสินค้า
            label_image = QtWidgets.QLabel()
            image_path = f"assets/product_image/{product['product_code']}_pic.png"
            pixmap = QtGui.QPixmap(image_path)
            label_image.setPixmap(pixmap)
            label_image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_image.setScaledContents(True)
            label_image.setFixedSize(250, 250)
            product_layout.addWidget(label_image, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

            # ชื่อสินค้า
            label_name = QtWidgets.QLabel()
            label_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_name.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
            label_name.setWordWrap(True)  # ให้ขึ้นบรรทัดใหม่อัตโนมัติ
            label_name.setFixedWidth(200)  # กำหนดความกว้างสูงสุด
            label_name.setFixedHeight(50)  # ความสูงสูงสุดให้พอดี 2 บรรทัด

            # ใช้ QFontMetrics เพื่อตัดข้อความ แล้วแสดง ... แทน
            font_metrics = QtGui.QFontMetrics(label_name.font())
            # ให้ข้อความอยู่ในกรอบที่กำหนดและตัดออกเมื่อเกิน
            elided_text = font_metrics.elidedText(product["product_name"], QtCore.Qt.TextElideMode.ElideRight, 200)
            label_name.setText(elided_text)

            # จัดให้อยู่ตรงกลางทั้งแนวตั้งและแนวนอน
            product_layout.addWidget(label_name, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

            # ราคาสินค้า
            label_price = QtWidgets.QLabel(f"฿{product['price']:,}")
            label_price.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_price.setStyleSheet("""
                font-size: 18px;
                color: #007BFF;
                font-weight: bold;
                background-color: #e6f0ff;
                padding: 5px;
            """)
            product_layout.addWidget(label_price)

            # สร้างปุ่มเพิ่มสินค้า
            add_to_cart_button = QtWidgets.QPushButton("เพิ่มลงรถเข็น")
            add_to_cart_button.setStyleSheet("""
                QPushButton {
                    background-color: #007BFF;
                    color: white;
                    border-radius: 5px;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
                QPushButton:pressed {
                    background-color: #004085;
                }
            """)

            # เชื่อมปุ่มกับฟังก์ชันเพิ่มสินค้าในฐานข้อมูล
            add_to_cart_button.clicked.connect(lambda _, code=product['product_code']: self.add_to_cart_db(code))

            # เพิ่มปุ่มลงใน layout
            product_layout.addWidget(add_to_cart_button)

            # เพิ่ม product widget ลงใน layout ของกริด
            self.content_layout.addWidget(product_widget, row, col)

            # Update row and column for grid layout
            col += 1
            if col >= self.columns:
                col = 0
                row += 2

            # สร้างเส้นแบ่งแนวนอนหลังจากทุกๆ แถว
            if col == 0:
                separator = QtWidgets.QFrame()
                separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
                separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
                separator.setStyleSheet("color: #D3D3D3;")  # สีเทาอ่อน
                self.content_layout.addWidget(separator, row, 0, 1, self.columns)
                row += 1  # เพิ่ม row หลังจากเพิ่มเส้นแบ่ง

        # Add scroll area to main layout
        self.MainContent_Area.addWidget(self.content_area)
        self.content_area.setStyleSheet("""
            QScrollBar:vertical {
                background: #e0e0e0;
                width: 10px;
                margin: 22px 0 22px 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #a0a0a0;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
        """)



    #================= ฟังค์ชั่นไปหน้า LOGIN ================#
    
    def go_to_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า CART ========================#

    def go_to_cart(self):
        self.cart_window = CartWindow()
        self.cart_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า Comset ========================#

    def go_to_comset(self):
        self.comset_window = ComsetWindow()
        self.comset_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า Notebook ========================#

    def go_to_notebook(self):
        self.notebook_window = NotebookWindow()
        self.notebook_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า phone ========================#

    def go_to_phone(self):
        self.phone_window = PhoneWindow()
        self.phone_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า headphone ========================#

    def go_to_headphone(self):
        self.headphone_window = HeadphoneWindow()
        self.headphone_window.show()
        self.close()


    def go_to_contactus(self):
        self.contactus_window = ContactusWindow()
        self.contactus_window.show()
        self.close()
    
    #================= ฟังค์ชั่นไปหน้า HOMEPAGE ================#
    
    # def go_to_home(self):
    #     self.home_page = CartWindow()  # สร้างหน้าแรก
    #     self.home_page.show()  # แสดงหน้าแรก
    #     self.home_page.showMaximized()
    #     self.close()

    #================= ฟังค์ชั่นไปหน้า HOMEPAGE ================#

    def show_message(self, title, message, icon):
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    #================= ฟังค์ชั่นเพิ่มสินค้าเข้าฐานข้อมูล ================#

    def add_to_cart_db(self, product_code, quantity=1):
        # ตรวจสอบว่าได้ล็อคอินหรือยัง
        if not logged_in_user:
            self.show_message("Error", "กรุณาล็อคอินก่อนเพิ่มสินค้าลงในตะกร้า!", QtWidgets.QMessageBox.Icon.Warning)
            return

        # ดึง user_id จากฐานข้อมูลหรือใช้ค่าที่กำหนด
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # ค้นหาค่า user_id จากชื่อผู้ใช้ (logged_in_user)
                cursor.execute("SELECT user_id FROM user_register WHERE uname = %s", (logged_in_user,))
                result = cursor.fetchone()
                
                if result:
                    user_id = result[0]  # ดึง user_id
                    
                    # เช็คว่าในตะกร้ามีสินค้านี้แล้วหรือไม่ (อาจใช้ user_id และ product_code)
                    cursor.execute("""SELECT quantity FROM cart_items WHERE user_id = %s AND product_code = %s""", (user_id, product_code))
                    existing_item = cursor.fetchone()

                    if existing_item:
                        # ถ้ามีสินค้านี้แล้ว, เพิ่ม quantity เข้าไป
                        new_quantity = existing_item[0] + quantity
                        cursor.execute("""
                            UPDATE cart_items SET quantity = %s WHERE user_id = %s AND product_code = %s
                        """, (new_quantity, user_id, product_code))
                    else:
                        # ถ้ายังไม่มี, เพิ่มสินค้าใหม่ลงในตะกร้า
                        cursor.execute("""INSERT INTO cart_items (user_id, product_code, quantity) VALUES (%s, %s, %s)""", (user_id, product_code, quantity))

                    connection.commit()
                    # self.show_message("สำเร็จ", "สินค้าได้ถูกเพิ่มลงในตะกร้าแล้ว!", QtWidgets.QMessageBox.Icon.Information)
                else:
                    self.show_message("ข้อผิดพลาด", "ไม่พบผู้ใช้ในระบบ!", QtWidgets.QMessageBox.Icon.Warning)
            
            except mysql.connector.Error as e:
                self.show_message("ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {e}", QtWidgets.QMessageBox.Icon.Critical)
            finally:
                cursor.close()
                connection.close()

# =================================== NOTEBOOK PAGE ==================================================#

class NotebookWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Notebook_page')
        self.setStyleSheet('background-color: #ffffff; border-radius: 15px;')
        self.showMaximized()
        self.setWindowIcon(QIcon('image/IT ZONE LOGO.png'))


        # สร้าง container แนวตั้งมาเป็น layout หลัก
        Main_Layout = QtWidgets.QVBoxLayout()  # สร้าง instance ของ QVBoxLayout
        self.setLayout(Main_Layout)  
        Main_Layout.setContentsMargins(0, 0, 0, 0)
        


# ========================= MENU TOP BAR PART ========================= #

        # สร้าง MenuBar_Widget และเพิ่ม title
        self.MenuBar_Widget = QWidget()
        self.MenuBar_Area = QHBoxLayout(self.MenuBar_Widget)
        self.MenuBar_Widget.setFixedHeight(100)  # ความสูงเมนูด้านบน
        self.MenuBar_Widget.setStyleSheet('background-color: #295CA5; border-radius: 0px;')

# ============================================ ITZONE ICON ซ้ายบน ============================================ #    

        icon_ITZONE_label = QLabel(self)
        icon_pixmap = QPixmap("assets/image/ITZONEEDIT W.png")  # ระบุที่อยู่ของไฟล์ไอคอน
        icon_pixmap = icon_pixmap.scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_ITZONE_label.setPixmap(icon_pixmap)

        IT_ZONE_TOP_TITLE = QWidget()
        IT_ZONE_TOP_TITLE.setLayout(QHBoxLayout())
        IT_ZONE_TOP_TITLE.layout().addWidget(icon_ITZONE_label)

        self.MenuBar_Area.addWidget(IT_ZONE_TOP_TITLE)

# ============================================ SEARCHBAR ด้านบน ============================================ #        
        # เพิ่มแถบค้นหา
        search_bar_container = QWidget()
        search_bar_layout = QHBoxLayout(search_bar_container)
        search_bar_layout.setContentsMargins(0, 0, 0, 0)

        # สร้าง QLineEdit สำหรับแถบค้นหา
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("ค้นหาสินค้า...")
        search_bar.setFixedHeight(30)
        search_bar.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;  /* กำหนดสีของข้อความที่พิมพ์ลงไปในช่องค้นหา */
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
                padding-left: 10px;
                font-size: 14px;
                font-family: 'PK Nakhon Pathom Demo';
            }
            QLineEdit::placeholder { 
                color: gray;  /* เปลี่ยนเป็นสีที่คุณต้องการ */
                font-family: 'PK Nakhon Pathom Demo';
            }
        """)

        # สร้าง QLabel สำหรับไอคอนแว่นขยาย
        search_icon = QLabel()
        icon_pixmap = QPixmap("assets/image/magnifying glass icon.png").scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        search_icon.setPixmap(icon_pixmap)
        search_icon.setStyleSheet("""
            background-color: #295CA5;
            border-top-right-radius: 15px;
            border-bottom-right-radius: 15px;
            padding: 5px;
        """)

        # ใส่ search_bar และ search_icon ลงใน layout ของ search_bar_container
        search_bar_layout.addWidget(search_bar)
        search_bar_layout.addWidget(search_icon)

        # เพิ่ม search_bar_container ลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(search_bar_container)

# ============================================ ABOUT US ปุ่ม ============================================ #

        # สร้างปุ่มสำหรับรถเข็นสินค้า
        contact_button = QPushButton("   About us")
        contact_button.setIcon(QIcon("assets/image/contact icon.png"))  # ระบุ path ไปยังไอคอนรถเข็น
        contact_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        contact_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม
        contact_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)
        contact_button.clicked.connect(self.go_to_contactus)
        # ตั้งค่าฟอนต์
        contact_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        contact_button.setFont(contact_button_font)

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(contact_button)

# ============================================ รถเข็นสินค้า ============================================ #

        # สร้างปุ่มสำหรับรถเข็นสินค้า
        cart_button = QPushButton("   รถเข็นสินค้า")
        cart_button.setIcon(QIcon("assets/image/cart icon.png"))  # ระบุ path ไปยังไอคอนรถเข็น
        cart_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        cart_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม
        cart_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)
        if logged_in_user == None:
            cart_button.clicked.connect(
                lambda: self.show_message("ยังไม่ล็อคอิน", "กรุณาล็อคอินเข้าสู่ระบบก่อน!", QtWidgets.QMessageBox.Icon.Warning)
            )
        else:
            cart_button.clicked.connect(self.go_to_cart)
        # ตั้งค่าฟอนต์
        cart_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        cart_button.setFont(cart_button_font)
        # cart_button.clicked.connect()

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(cart_button)

# ============================================ เข้าสู่ระบบ ============================================ #

        # # ใช้ global เพื่อตรวจสอบข้อมูลผู้ใช้งาน
        # global logged_in_user

        # ตรวจสอบว่ามีผู้ใช้งานล็อกอินหรือไม่
        if logged_in_user:
            # ถ้ามีผู้ใช้งานล็อกอิน แสดงชื่อผู้ใช้งานในปุ่ม
            user_button = QPushButton(f"   {logged_in_user}")
        else:
            # ถ้าไม่มีผู้ใช้งาน แสดงปุ่มเข้าสู่ระบบ
            user_button = QPushButton("   เข้าสู่ระบบ")

        # ตั้งค่าไอคอน
        user_button.setIcon(QIcon("assets/image/user icon.png"))  # ระบุ path ไปยังไอคอน
        user_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        user_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม

        # ตั้งค่า StyleSheet
        user_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)

        # ตั้งค่าฟอนต์
        user_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        user_button.setFont(user_button_font)
        user_button.clicked.connect(self.go_to_login)

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(user_button)

        # เพิ่ม MenuBar_Widget ลงใน Main_Layout
        Main_Layout.addWidget(self.MenuBar_Widget)


# ================================================================= 

#                         - CONTENT PART -

# ================================================================= 

        # สร้าง Container ของ MainContent ไว้เพื่อใส่เนื้อหา
        self.MainContent_Widget = QWidget()
        self.MainContent_Area = QHBoxLayout(self.MainContent_Widget)
        Main_Layout.addWidget(self.MainContent_Widget)
        self.MainContent_Widget.setContentsMargins(0, 0, 0, 0)
        self.MainContent_Area.setContentsMargins(0, 0, 0, 0)
        self.MainContent_Area.setAlignment(Qt.AlignmentFlag.AlignLeft)
# ========================= เมนูด้านแถบซ้าย ========================= #

        # สร้าง SideBar Menu เพื่อเพิ่มเมนู
        self.SideBar_Widget = QWidget()
        self.SideBar_Area = QVBoxLayout(self.SideBar_Widget)
        self.SideBar_Widget.setFixedWidth(80)  # กำหนดความกว้างของแถบด้านซ้าย
        self.SideBar_Widget.setStyleSheet('background-color: #295CA5; border-radius: 0px;')
        self.SideBar_Area.setContentsMargins(0, 0, 0, 0)

# ============================================ COMSET Button ============================================ #

        self.COMSET_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.COMSET_ICON.setIcon(QIcon("assets/image/COMSET icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.COMSET_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.COMSET_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.COMSET_ICON.clicked.connect(self.go_to_comset)
        self.SideBar_Area.addWidget(self.COMSET_ICON)

# ============================================ NOTEBOOK Button ============================================ #

        self.NOTEBOOK_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.NOTEBOOK_ICON.setIcon(QIcon("assets/image/NOTEBOOK icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.NOTEBOOK_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.NOTEBOOK_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.NOTEBOOK_ICON.clicked.connect(self.go_to_notebook)
        self.SideBar_Area.addWidget(self.NOTEBOOK_ICON)

# ============================================ PHONE Button ============================================ #

        self.PHONE_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.PHONE_ICON.setIcon(QIcon("assets/image/PHONE icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.PHONE_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.PHONE_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.PHONE_ICON.clicked.connect(self.go_to_phone)
        self.SideBar_Area.addWidget(self.PHONE_ICON)

# ============================================ HEADPHONE Button ============================================ #

        self.HEADPHONE_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.HEADPHONE_ICON.setIcon(QIcon("assets/image/HEADPHONE icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.HEADPHONE_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.HEADPHONE_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.HEADPHONE_ICON.clicked.connect(self.go_to_headphone)
        self.SideBar_Area.addWidget(self.HEADPHONE_ICON)

# ============================================ EXIT Button ============================================ #

        self.EXIT_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.EXIT_ICON.setIcon(QIcon("assets/image/EXIT icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.EXIT_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.EXIT_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.EXIT_ICON.clicked.connect(self.go_to_login)

        self.SideBar_Area.addWidget(self.EXIT_ICON) 
        self.EXIT_ICON.setContentsMargins(0, 0, 0, 0)       

        self.MainContent_Area.addWidget(self.SideBar_Widget)

# ========================= สร้าง หน้าแสดงรายการสินค้า ============================= #

        # Scroll Area
        self.content_area = QtWidgets.QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setContentsMargins(0, 0, 0, 0)

        # Content widget
        self.content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QGridLayout(self.content_widget)  # เปลี่ยนเป็น QGridLayout
        self.content_widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.content_area.setWidget(self.content_widget)
        self.content_widget.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(20)
        self.content_layout.setContentsMargins(10, 10, 10, 10)

        # กำหนดจำนวนคอลัมน์ที่ต้องการในกริด
        self.columns = 4
        self.display_products()

    def display_products(self):
        # ดึงข้อมูลสินค้า
        products = get_notebook_products()

        # กำหนดค่าตัวแปรแถวและคอลัมน์สำหรับการแสดงสินค้า
        row = 0
        col = 0

        # Loop for adding product widgets
        for product in products:
            # Widget สำหรับแสดงผลสินค้าแต่ละรายการ
            product_widget = QtWidgets.QWidget()
            product_layout = QtWidgets.QVBoxLayout(product_widget)
            product_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # รูปภาพสินค้า
            label_image = QtWidgets.QLabel()
            image_path = f"assets/product_image/{product['product_code']}_pic.png"
            pixmap = QtGui.QPixmap(image_path)
            label_image.setPixmap(pixmap)
            label_image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_image.setScaledContents(True)
            label_image.setFixedSize(250, 250)
            product_layout.addWidget(label_image, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

            # ชื่อสินค้า
            label_name = QtWidgets.QLabel()
            label_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_name.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
            label_name.setWordWrap(True)  # ให้ขึ้นบรรทัดใหม่อัตโนมัติ
            label_name.setFixedWidth(200)  # กำหนดความกว้างสูงสุด
            label_name.setFixedHeight(50)  # ความสูงสูงสุดให้พอดี 2 บรรทัด

            # ใช้ QFontMetrics เพื่อตัดข้อความ แล้วแสดง ... แทน
            font_metrics = QtGui.QFontMetrics(label_name.font())
            # ให้ข้อความอยู่ในกรอบที่กำหนดและตัดออกเมื่อเกิน
            elided_text = font_metrics.elidedText(product["product_name"], QtCore.Qt.TextElideMode.ElideRight, 200)
            label_name.setText(elided_text)

            # จัดให้อยู่ตรงกลางทั้งแนวตั้งและแนวนอน
            product_layout.addWidget(label_name, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

            # ราคาสินค้า
            label_price = QtWidgets.QLabel(f"฿{product['price']:,}")
            label_price.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_price.setStyleSheet("""
                font-size: 18px;
                color: #007BFF;
                font-weight: bold;
                background-color: #e6f0ff;
                padding: 5px;
            """)
            product_layout.addWidget(label_price)

            # สร้างปุ่มเพิ่มสินค้า
            add_to_cart_button = QtWidgets.QPushButton("เพิ่มลงรถเข็น")
            add_to_cart_button.setStyleSheet("""
                QPushButton {
                    background-color: #007BFF;
                    color: white;
                    border-radius: 5px;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
                QPushButton:pressed {
                    background-color: #004085;
                }
            """)

            # เชื่อมปุ่มกับฟังก์ชันเพิ่มสินค้าในฐานข้อมูล
            add_to_cart_button.clicked.connect(lambda _, code=product['product_code']: self.add_to_cart_db(code))

            # เพิ่มปุ่มลงใน layout
            product_layout.addWidget(add_to_cart_button)

            # เพิ่ม product widget ลงใน layout ของกริด
            self.content_layout.addWidget(product_widget, row, col)

            # Update row and column for grid layout
            col += 1
            if col >= self.columns:
                col = 0
                row += 2

            # สร้างเส้นแบ่งแนวนอนหลังจากทุกๆ แถว
            if col == 0:
                separator = QtWidgets.QFrame()
                separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
                separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
                separator.setStyleSheet("color: #D3D3D3;")  # สีเทาอ่อน
                self.content_layout.addWidget(separator, row, 0, 1, self.columns)
                row += 1  # เพิ่ม row หลังจากเพิ่มเส้นแบ่ง

        # Add scroll area to main layout
        self.MainContent_Area.addWidget(self.content_area)
        self.content_area.setStyleSheet("""
            QScrollBar:vertical {
                background: #e0e0e0;
                width: 10px;
                margin: 22px 0 22px 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #a0a0a0;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
        """)



    #================= ฟังค์ชั่นไปหน้า LOGIN ================#
    
    def go_to_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า CART ========================#

    def go_to_cart(self):
        self.cart_window = CartWindow()
        self.cart_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า Comset ========================#

    def go_to_comset(self):
        self.comset_window = ComsetWindow()
        self.comset_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า Notebook ========================#

    def go_to_notebook(self):
        self.notebook_window = NotebookWindow()
        self.notebook_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า phone ========================#

    def go_to_phone(self):
        self.phone_window = PhoneWindow()
        self.phone_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า headphone ========================#

    def go_to_headphone(self):
        self.headphone_window = HeadphoneWindow()
        self.headphone_window.show()
        self.close()

    def go_to_contactus(self):
        self.contactus_window = ContactusWindow()
        self.contactus_window.show()
        self.close()
    
    #================= ฟังค์ชั่นไปหน้า HOMEPAGE ================#
    
    # def go_to_home(self):
    #     self.home_page = CartWindow()  # สร้างหน้าแรก
    #     self.home_page.show()  # แสดงหน้าแรก
    #     self.home_page.showMaximized()
    #     self.close()

# =================================== Message แจ้งเตือน =====================================================

    def show_message(self, title, message, icon):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))
        msg_box.exec()

        #================= ฟังค์ชั่นเพิ่มสินค้าเข้าฐานข้อมูล ================#

    def add_to_cart_db(self, product_code, quantity=1):
        # ตรวจสอบว่าได้ล็อคอินหรือยัง
        if not logged_in_user:
            self.show_message("Error", "กรุณาล็อคอินก่อนเพิ่มสินค้าลงในตะกร้า!", QtWidgets.QMessageBox.Icon.Warning)
            return

        # ดึง user_id จากฐานข้อมูลหรือใช้ค่าที่กำหนด
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # ค้นหาค่า user_id จากชื่อผู้ใช้ (logged_in_user)
                cursor.execute("SELECT user_id FROM user_register WHERE uname = %s", (logged_in_user,))
                result = cursor.fetchone()
                
                if result:
                    user_id = result[0]  # ดึง user_id
                    
                    # เช็คว่าในตะกร้ามีสินค้านี้แล้วหรือไม่ (อาจใช้ user_id และ product_code)
                    cursor.execute("""SELECT quantity FROM cart_items WHERE user_id = %s AND product_code = %s""", (user_id, product_code))
                    existing_item = cursor.fetchone()

                    if existing_item:
                        # ถ้ามีสินค้านี้แล้ว, เพิ่ม quantity เข้าไป
                        new_quantity = existing_item[0] + quantity
                        cursor.execute("""
                            UPDATE cart_items SET quantity = %s WHERE user_id = %s AND product_code = %s
                        """, (new_quantity, user_id, product_code))
                    else:
                        # ถ้ายังไม่มี, เพิ่มสินค้าใหม่ลงในตะกร้า
                        cursor.execute("""INSERT INTO cart_items (user_id, product_code, quantity) VALUES (%s, %s, %s)""", (user_id, product_code, quantity))

                    connection.commit()
                    # self.show_message("สำเร็จ", "สินค้าได้ถูกเพิ่มลงในตะกร้าแล้ว!", QtWidgets.QMessageBox.Icon.Information)
                else:
                    self.show_message("ข้อผิดพลาด", "ไม่พบผู้ใช้ในระบบ!", QtWidgets.QMessageBox.Icon.Warning)
            
            except mysql.connector.Error as e:
                self.show_message("ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {e}", QtWidgets.QMessageBox.Icon.Critical)
            finally:
                cursor.close()
                connection.close()

# ===================================PHONE PAGE ==================================================#

class PhoneWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Phone_page')
        self.setStyleSheet('background-color: #ffffff; border-radius: 15px;')
        self.showMaximized()
        self.setWindowIcon(QIcon('image/IT ZONE LOGO.png'))



        # สร้าง container แนวตั้งมาเป็น layout หลัก
        Main_Layout = QtWidgets.QVBoxLayout()  # สร้าง instance ของ QVBoxLayout
        self.setLayout(Main_Layout)  
        Main_Layout.setContentsMargins(0, 0, 0, 0)



# ========================= MENU TOP BAR PART ========================= #

        # สร้าง MenuBar_Widget และเพิ่ม title
        self.MenuBar_Widget = QWidget()
        self.MenuBar_Area = QHBoxLayout(self.MenuBar_Widget)
        self.MenuBar_Widget.setFixedHeight(100)  # ความสูงเมนูด้านบน
        self.MenuBar_Widget.setStyleSheet('background-color: #295CA5; border-radius: 0px;')

# ============================================ ITZONE ICON ซ้ายบน ============================================ #    

        icon_ITZONE_label = QLabel(self)
        icon_pixmap = QPixmap("assets/image/ITZONEEDIT W.png")  # ระบุที่อยู่ของไฟล์ไอคอน
        icon_pixmap = icon_pixmap.scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_ITZONE_label.setPixmap(icon_pixmap)

        IT_ZONE_TOP_TITLE = QWidget()
        IT_ZONE_TOP_TITLE.setLayout(QHBoxLayout())
        IT_ZONE_TOP_TITLE.layout().addWidget(icon_ITZONE_label)

        self.MenuBar_Area.addWidget(IT_ZONE_TOP_TITLE)

# ============================================ SEARCHBAR ด้านบน ============================================ #        
        # เพิ่มแถบค้นหา
        search_bar_container = QWidget()
        search_bar_layout = QHBoxLayout(search_bar_container)
        search_bar_layout.setContentsMargins(0, 0, 0, 0)

        # สร้าง QLineEdit สำหรับแถบค้นหา
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("ค้นหาสินค้า...")
        search_bar.setFixedHeight(30)
        search_bar.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;  /* กำหนดสีของข้อความที่พิมพ์ลงไปในช่องค้นหา */
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
                padding-left: 10px;
                font-size: 14px;
                font-family: 'PK Nakhon Pathom Demo';
            }
            QLineEdit::placeholder { 
                color: gray;  /* เปลี่ยนเป็นสีที่คุณต้องการ */
                font-family: 'PK Nakhon Pathom Demo';
            }
        """)

        # สร้าง QLabel สำหรับไอคอนแว่นขยาย
        search_icon = QLabel()
        icon_pixmap = QPixmap("assets/image/magnifying glass icon.png").scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        search_icon.setPixmap(icon_pixmap)
        search_icon.setStyleSheet("""
            background-color: #295CA5;
            border-top-right-radius: 15px;
            border-bottom-right-radius: 15px;
            padding: 5px;
        """)

        # ใส่ search_bar และ search_icon ลงใน layout ของ search_bar_container
        search_bar_layout.addWidget(search_bar)
        search_bar_layout.addWidget(search_icon)

        # เพิ่ม search_bar_container ลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(search_bar_container)

# ============================================ ABOUT US ปุ่ม ============================================ #

        # สร้างปุ่มสำหรับรถเข็นสินค้า
        contact_button = QPushButton("   About us")
        contact_button.setIcon(QIcon("assets/image/contact icon.png"))  # ระบุ path ไปยังไอคอนรถเข็น
        contact_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        contact_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม
        contact_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)
        contact_button.clicked.connect(self.go_to_contactus)
        # ตั้งค่าฟอนต์
        contact_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        contact_button.setFont(contact_button_font)

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(contact_button)

# ============================================ รถเข็นสินค้า ============================================ #

        # สร้างปุ่มสำหรับรถเข็นสินค้า
        cart_button = QPushButton("   รถเข็นสินค้า")
        cart_button.setIcon(QIcon("assets/image/cart icon.png"))  # ระบุ path ไปยังไอคอนรถเข็น
        cart_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        cart_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม
        cart_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)
        if logged_in_user == None:
            cart_button.clicked.connect(
                lambda: self.show_message("ยังไม่ล็อคอิน", "กรุณาล็อคอินเข้าสู่ระบบก่อน!", QtWidgets.QMessageBox.Icon.Warning)
            )
        else:
            cart_button.clicked.connect(self.go_to_cart)
        # ตั้งค่าฟอนต์
        cart_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        cart_button.setFont(cart_button_font)
        # cart_button.clicked.connect()

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(cart_button)

# ============================================ เข้าสู่ระบบ ============================================ #

        # # ใช้ global เพื่อตรวจสอบข้อมูลผู้ใช้งาน
        # global logged_in_user

        # ตรวจสอบว่ามีผู้ใช้งานล็อกอินหรือไม่
        if logged_in_user:
            # ถ้ามีผู้ใช้งานล็อกอิน แสดงชื่อผู้ใช้งานในปุ่ม
            user_button = QPushButton(f"   {logged_in_user}")
        else:
            # ถ้าไม่มีผู้ใช้งาน แสดงปุ่มเข้าสู่ระบบ
            user_button = QPushButton("   เข้าสู่ระบบ")

        # ตั้งค่าไอคอน
        user_button.setIcon(QIcon("assets/image/user icon.png"))  # ระบุ path ไปยังไอคอน
        user_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        user_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม

        # ตั้งค่า StyleSheet
        user_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)

        # ตั้งค่าฟอนต์
        user_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        user_button.setFont(user_button_font)
        user_button.clicked.connect(self.go_to_login)

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(user_button)

        # เพิ่ม MenuBar_Widget ลงใน Main_Layout
        Main_Layout.addWidget(self.MenuBar_Widget)
        

# ================================================================= 

#                         - CONTENT PART -

# ================================================================= 

        # สร้าง Container ของ MainContent ไว้เพื่อใส่เนื้อหา
        self.MainContent_Widget = QWidget()
        self.MainContent_Area = QHBoxLayout(self.MainContent_Widget)
        Main_Layout.addWidget(self.MainContent_Widget)
        self.MainContent_Widget.setContentsMargins(0, 0, 0, 0)
        self.MainContent_Area.setContentsMargins(0, 0, 0, 0)
        self.MainContent_Area.setAlignment(Qt.AlignmentFlag.AlignLeft)
# ========================= เมนูด้านแถบซ้าย ========================= #

        # สร้าง SideBar Menu เพื่อเพิ่มเมนู
        self.SideBar_Widget = QWidget()
        self.SideBar_Area = QVBoxLayout(self.SideBar_Widget)
        self.SideBar_Widget.setFixedWidth(80)  # กำหนดความกว้างของแถบด้านซ้าย
        self.SideBar_Widget.setStyleSheet('background-color: #295CA5; border-radius: 0px;')
        self.SideBar_Area.setContentsMargins(0, 0, 0, 0)

# ============================================ COMSET Button ============================================ #

        self.COMSET_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.COMSET_ICON.setIcon(QIcon("assets/image/COMSET icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.COMSET_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.COMSET_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.COMSET_ICON.clicked.connect(self.go_to_comset)
        self.SideBar_Area.addWidget(self.COMSET_ICON)

# ============================================ NOTEBOOK Button ============================================ #

        self.NOTEBOOK_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.NOTEBOOK_ICON.setIcon(QIcon("assets/image/NOTEBOOK icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.NOTEBOOK_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.NOTEBOOK_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.NOTEBOOK_ICON.clicked.connect(self.go_to_notebook)
        self.SideBar_Area.addWidget(self.NOTEBOOK_ICON)

# ============================================ PHONE Button ============================================ #

        self.PHONE_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.PHONE_ICON.setIcon(QIcon("assets/image/PHONE icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.PHONE_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.PHONE_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.PHONE_ICON.clicked.connect(self.go_to_phone)
        self.SideBar_Area.addWidget(self.PHONE_ICON)

# ============================================ HEADPHONE Button ============================================ #

        self.HEADPHONE_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.HEADPHONE_ICON.setIcon(QIcon("assets/image/HEADPHONE icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.HEADPHONE_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.HEADPHONE_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.HEADPHONE_ICON.clicked.connect(self.go_to_headphone)
        self.SideBar_Area.addWidget(self.HEADPHONE_ICON)

# ============================================ EXIT Button ============================================ #

        self.EXIT_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.EXIT_ICON.setIcon(QIcon("assets/image/EXIT icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.EXIT_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.EXIT_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.EXIT_ICON.clicked.connect(self.go_to_login)

        self.SideBar_Area.addWidget(self.EXIT_ICON) 
        self.EXIT_ICON.setContentsMargins(0, 0, 0, 0)       

        self.MainContent_Area.addWidget(self.SideBar_Widget)

    # ========================= สร้าง หน้าแสดงรายการสินค้า ============================= #

        # Scroll Area
        self.content_area = QtWidgets.QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setContentsMargins(0, 0, 0, 0)

        # Content widget
        self.content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QGridLayout(self.content_widget)  # เปลี่ยนเป็น QGridLayout
        self.content_widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.content_area.setWidget(self.content_widget)
        self.content_widget.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(20)
        self.content_layout.setContentsMargins(10, 10, 10, 10)


        # กำหนดจำนวนคอลัมน์ที่ต้องการในกริด
        self.columns = 4
        self.display_products()

    def display_products(self):
        # ดึงข้อมูลสินค้า
        products = get_phone_products()

        # กำหนดค่าตัวแปรแถวและคอลัมน์สำหรับการแสดงสินค้า
        row = 0
        col = 0

        # Loop for adding product widgets
        for product in products:
            # Widget สำหรับแสดงผลสินค้าแต่ละรายการ
            product_widget = QtWidgets.QWidget()
            product_layout = QtWidgets.QVBoxLayout(product_widget)
            product_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # รูปภาพสินค้า
            label_image = QtWidgets.QLabel()
            image_path = f"assets/product_image/{product['product_code']}_pic.png"
            pixmap = QtGui.QPixmap(image_path)
            label_image.setPixmap(pixmap)
            label_image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_image.setScaledContents(True)
            label_image.setFixedSize(250, 250)
            product_layout.addWidget(label_image, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

            # ชื่อสินค้า
            label_name = QtWidgets.QLabel()
            label_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_name.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
            label_name.setWordWrap(True)  # ให้ขึ้นบรรทัดใหม่อัตโนมัติ
            label_name.setFixedWidth(200)  # กำหนดความกว้างสูงสุด
            label_name.setFixedHeight(50)  # ความสูงสูงสุดให้พอดี 2 บรรทัด

            # ใช้ QFontMetrics เพื่อตัดข้อความ แล้วแสดง ... แทน
            font_metrics = QtGui.QFontMetrics(label_name.font())
            # ให้ข้อความอยู่ในกรอบที่กำหนดและตัดออกเมื่อเกิน
            elided_text = font_metrics.elidedText(product["product_name"], QtCore.Qt.TextElideMode.ElideRight, 200)
            label_name.setText(elided_text)

            # จัดให้อยู่ตรงกลางทั้งแนวตั้งและแนวนอน
            product_layout.addWidget(label_name, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

            # ราคาสินค้า
            label_price = QtWidgets.QLabel(f"฿{product['price']:,}")
            label_price.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_price.setStyleSheet("""
                font-size: 18px;
                color: #007BFF;
                font-weight: bold;
                background-color: #e6f0ff;
                padding: 5px;
            """)
            product_layout.addWidget(label_price)

            # สร้างปุ่มเพิ่มสินค้า
            add_to_cart_button = QtWidgets.QPushButton("เพิ่มลงรถเข็น")
            add_to_cart_button.setStyleSheet("""
                QPushButton {
                    background-color: #007BFF;
                    color: white;
                    border-radius: 5px;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
                QPushButton:pressed {
                    background-color: #004085;
                }
            """)

            # เชื่อมปุ่มกับฟังก์ชันเพิ่มสินค้าในฐานข้อมูล
            add_to_cart_button.clicked.connect(lambda _, code=product['product_code']: self.add_to_cart_db(code))

            # เพิ่มปุ่มลงใน layout
            product_layout.addWidget(add_to_cart_button)

            # เพิ่ม product widget ลงใน layout ของกริด
            self.content_layout.addWidget(product_widget, row, col)

            # Update row and column for grid layout
            col += 1
            if col >= self.columns:
                col = 0
                row += 2

            # สร้างเส้นแบ่งแนวนอนหลังจากทุกๆ แถว
            if col == 0:
                separator = QtWidgets.QFrame()
                separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
                separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
                separator.setStyleSheet("color: #D3D3D3;")  # สีเทาอ่อน
                self.content_layout.addWidget(separator, row, 0, 1, self.columns)
                row += 1  # เพิ่ม row หลังจากเพิ่มเส้นแบ่ง

        # Add scroll area to main layout
        self.MainContent_Area.addWidget(self.content_area)
        self.content_area.setStyleSheet("""
            QScrollBar:vertical {
                background: #e0e0e0;
                width: 10px;
                margin: 22px 0 22px 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #a0a0a0;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
        """)


    #================= ฟังค์ชั่นไปหน้า LOGIN ================#
    
    def go_to_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า CART ========================#

    def go_to_cart(self):
        self.cart_window = CartWindow()
        self.cart_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า Comset ========================#

    def go_to_comset(self):
        self.comset_window = ComsetWindow()
        self.comset_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า Notebook ========================#

    def go_to_notebook(self):
        self.notebook_window = NotebookWindow()
        self.notebook_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า phone ========================#

    def go_to_phone(self):
        self.phone_window = PhoneWindow()
        self.phone_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า headphone ========================#

    def go_to_headphone(self):
        self.headphone_window = HeadphoneWindow()
        self.headphone_window.show()
        self.close()

    def go_to_contactus(self):
        self.contactus_window = ContactusWindow()
        self.contactus_window.show()
        self.close()
    
    #================= ฟังค์ชั่นไปหน้า HOMEPAGE ================#
    
    # def go_to_home(self):
    #     self.home_page = CartWindow()  # สร้างหน้าแรก
    #     self.home_page.show()  # แสดงหน้าแรก
    #     self.home_page.showMaximized()
    #     self.close()

    #================= ฟังค์ชั่นเพิ่มสินค้าเข้าฐานข้อมูล ================#

    def add_to_cart_db(self, product_code, quantity=1):
        # ตรวจสอบว่าได้ล็อคอินหรือยัง
        if not logged_in_user:
            self.show_message("Error", "กรุณาล็อคอินก่อนเพิ่มสินค้าลงในตะกร้า!", QtWidgets.QMessageBox.Icon.Warning)
            return

        # ดึง user_id จากฐานข้อมูลหรือใช้ค่าที่กำหนด
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # ค้นหาค่า user_id จากชื่อผู้ใช้ (logged_in_user)
                cursor.execute("SELECT user_id FROM user_register WHERE uname = %s", (logged_in_user,))
                result = cursor.fetchone()
                
                if result:
                    user_id = result[0]  # ดึง user_id
                    
                    # เช็คว่าในตะกร้ามีสินค้านี้แล้วหรือไม่ (อาจใช้ user_id และ product_code)
                    cursor.execute("""SELECT quantity FROM cart_items WHERE user_id = %s AND product_code = %s""", (user_id, product_code))
                    existing_item = cursor.fetchone()

                    if existing_item:
                        # ถ้ามีสินค้านี้แล้ว, เพิ่ม quantity เข้าไป
                        new_quantity = existing_item[0] + quantity
                        cursor.execute("""
                            UPDATE cart_items SET quantity = %s WHERE user_id = %s AND product_code = %s
                        """, (new_quantity, user_id, product_code))
                    else:
                        # ถ้ายังไม่มี, เพิ่มสินค้าใหม่ลงในตะกร้า
                        cursor.execute("""INSERT INTO cart_items (user_id, product_code, quantity) VALUES (%s, %s, %s)""", (user_id, product_code, quantity))

                    connection.commit()
                    # self.show_message("สำเร็จ", "สินค้าได้ถูกเพิ่มลงในตะกร้าแล้ว!", QtWidgets.QMessageBox.Icon.Information)
                else:
                    self.show_message("ข้อผิดพลาด", "ไม่พบผู้ใช้ในระบบ!", QtWidgets.QMessageBox.Icon.Warning)
            
            except mysql.connector.Error as e:
                self.show_message("ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {e}", QtWidgets.QMessageBox.Icon.Critical)
            finally:
                cursor.close()
                connection.close()

# =================================== Message แจ้งเตือน =====================================================

    def show_message(self, title, message, icon):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))
        msg_box.exec()

# ===================================HEADPHONE PAGE ==================================================#

class HeadphoneWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Headphone_page')
        self.setStyleSheet('background-color: #ffffff; border-radius: 15px;')
        self.showMaximized()
        self.setWindowIcon(QIcon('image/IT ZONE LOGO.png'))


        # สร้าง container แนวตั้งมาเป็น layout หลัก
        Main_Layout = QtWidgets.QVBoxLayout()  # สร้าง instance ของ QVBoxLayout
        self.setLayout(Main_Layout)  
        Main_Layout.setContentsMargins(0, 0, 0, 0)
        


# ========================= MENU TOP BAR PART ========================= #

        # สร้าง MenuBar_Widget และเพิ่ม title
        self.MenuBar_Widget = QWidget()
        self.MenuBar_Area = QHBoxLayout(self.MenuBar_Widget)
        self.MenuBar_Widget.setFixedHeight(100)  # ความสูงเมนูด้านบน
        self.MenuBar_Widget.setStyleSheet('background-color: #295CA5; border-radius: 0px;')

# ============================================ ITZONE ICON ซ้ายบน ============================================ #    

        icon_ITZONE_label = QLabel(self)
        icon_pixmap = QPixmap("assets/image/ITZONEEDIT W.png")  # ระบุที่อยู่ของไฟล์ไอคอน
        icon_pixmap = icon_pixmap.scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_ITZONE_label.setPixmap(icon_pixmap)

        IT_ZONE_TOP_TITLE = QWidget()
        IT_ZONE_TOP_TITLE.setLayout(QHBoxLayout())
        IT_ZONE_TOP_TITLE.layout().addWidget(icon_ITZONE_label)

        self.MenuBar_Area.addWidget(IT_ZONE_TOP_TITLE)

# ============================================ SEARCHBAR ด้านบน ============================================ #        
        # เพิ่มแถบค้นหา
        search_bar_container = QWidget()
        search_bar_layout = QHBoxLayout(search_bar_container)
        search_bar_layout.setContentsMargins(0, 0, 0, 0)

        # สร้าง QLineEdit สำหรับแถบค้นหา
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("ค้นหาสินค้า...")
        search_bar.setFixedHeight(30)
        search_bar.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;  /* กำหนดสีของข้อความที่พิมพ์ลงไปในช่องค้นหา */
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
                padding-left: 10px;
                font-size: 14px;
                font-family: 'PK Nakhon Pathom Demo';
            }
            QLineEdit::placeholder { 
                color: gray;  /* เปลี่ยนเป็นสีที่คุณต้องการ */
                font-family: 'PK Nakhon Pathom Demo';
            }
        """)

        # สร้าง QLabel สำหรับไอคอนแว่นขยาย
        search_icon = QLabel()
        icon_pixmap = QPixmap("assets/image/magnifying glass icon.png").scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        search_icon.setPixmap(icon_pixmap)
        search_icon.setStyleSheet("""
            background-color: #295CA5;
            border-top-right-radius: 15px;
            border-bottom-right-radius: 15px;
            padding: 5px;
        """)

        # ใส่ search_bar และ search_icon ลงใน layout ของ search_bar_container
        search_bar_layout.addWidget(search_bar)
        search_bar_layout.addWidget(search_icon)

        # เพิ่ม search_bar_container ลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(search_bar_container)

# ============================================ ABOUT US ปุ่ม ============================================ #

        # สร้างปุ่มสำหรับรถเข็นสินค้า
        contact_button = QPushButton("   About us")
        contact_button.setIcon(QIcon("assets/image/contact icon.png"))  # ระบุ path ไปยังไอคอนรถเข็น
        contact_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        contact_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม
        contact_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)
        contact_button.clicked.connect(self.go_to_contactus)
        # ตั้งค่าฟอนต์
        contact_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        contact_button.setFont(contact_button_font)

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(contact_button)

# ============================================ รถเข็นสินค้า ============================================ #

        # สร้างปุ่มสำหรับรถเข็นสินค้า
        cart_button = QPushButton("   รถเข็นสินค้า")
        cart_button.setIcon(QIcon("assets/image/cart icon.png"))  # ระบุ path ไปยังไอคอนรถเข็น
        cart_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        cart_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม
        cart_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)
        if logged_in_user == None:
            cart_button.clicked.connect(
                lambda: self.show_message("ยังไม่ล็อคอิน", "กรุณาล็อคอินเข้าสู่ระบบก่อน!", QtWidgets.QMessageBox.Icon.Warning)
            )
        else:
            cart_button.clicked.connect(self.go_to_cart)
        # ตั้งค่าฟอนต์
        cart_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        cart_button.setFont(cart_button_font)
        # cart_button.clicked.connect()

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(cart_button)

# ============================================ เข้าสู่ระบบ ============================================ #

        # # ใช้ global เพื่อตรวจสอบข้อมูลผู้ใช้งาน
        # global logged_in_user

        # ตรวจสอบว่ามีผู้ใช้งานล็อกอินหรือไม่
        if logged_in_user:
            # ถ้ามีผู้ใช้งานล็อกอิน แสดงชื่อผู้ใช้งานในปุ่ม
            user_button = QPushButton(f"   {logged_in_user}")
        else:
            # ถ้าไม่มีผู้ใช้งาน แสดงปุ่มเข้าสู่ระบบ
            user_button = QPushButton("   เข้าสู่ระบบ")

        # ตั้งค่าไอคอน
        user_button.setIcon(QIcon("assets/image/user icon.png"))  # ระบุ path ไปยังไอคอน
        user_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        user_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม

        # ตั้งค่า StyleSheet
        user_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)

        # ตั้งค่าฟอนต์
        user_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        user_button.setFont(user_button_font)
        user_button.clicked.connect(self.go_to_login)

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(user_button)

        # เพิ่ม MenuBar_Widget ลงใน Main_Layout
        Main_Layout.addWidget(self.MenuBar_Widget)
        

# ================================================================= 

#                         - CONTENT PART -

# ================================================================= 

        # สร้าง Container ของ MainContent ไว้เพื่อใส่เนื้อหา
        self.MainContent_Widget = QWidget()
        self.MainContent_Area = QHBoxLayout(self.MainContent_Widget)
        Main_Layout.addWidget(self.MainContent_Widget)
        self.MainContent_Widget.setContentsMargins(0, 0, 0, 0)
        self.MainContent_Area.setContentsMargins(0, 0, 0, 0)
        self.MainContent_Area.setAlignment(Qt.AlignmentFlag.AlignLeft)
# ========================= เมนูด้านแถบซ้าย ========================= #

        # สร้าง SideBar Menu เพื่อเพิ่มเมนู
        self.SideBar_Widget = QWidget()
        self.SideBar_Area = QVBoxLayout(self.SideBar_Widget)
        self.SideBar_Widget.setFixedWidth(80)  # กำหนดความกว้างของแถบด้านซ้าย
        self.SideBar_Widget.setStyleSheet('background-color: #295CA5; border-radius: 0px;')
        self.SideBar_Area.setContentsMargins(0, 0, 0, 0)

# ============================================ COMSET Button ============================================ #

        self.COMSET_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.COMSET_ICON.setIcon(QIcon("assets/image/COMSET icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.COMSET_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.COMSET_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.COMSET_ICON.clicked.connect(self.go_to_comset)
        self.SideBar_Area.addWidget(self.COMSET_ICON)

# ============================================ NOTEBOOK Button ============================================ #

        self.NOTEBOOK_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.NOTEBOOK_ICON.setIcon(QIcon("assets/image/NOTEBOOK icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.NOTEBOOK_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.NOTEBOOK_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.NOTEBOOK_ICON.clicked.connect(self.go_to_notebook)
        self.SideBar_Area.addWidget(self.NOTEBOOK_ICON)

# ============================================ PHONE Button ============================================ #

        self.PHONE_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.PHONE_ICON.setIcon(QIcon("assets/image/PHONE icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.PHONE_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.PHONE_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.PHONE_ICON.clicked.connect(self.go_to_phone)
        self.SideBar_Area.addWidget(self.PHONE_ICON)

# ============================================ HEADPHONE Button ============================================ #

        self.HEADPHONE_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.HEADPHONE_ICON.setIcon(QIcon("assets/image/HEADPHONE icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.HEADPHONE_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.HEADPHONE_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.HEADPHONE_ICON.clicked.connect(self.go_to_headphone)
        self.SideBar_Area.addWidget(self.HEADPHONE_ICON)

# ============================================ EXIT Button ============================================ #

        self.EXIT_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.EXIT_ICON.setIcon(QIcon("assets/image/EXIT icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.EXIT_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.EXIT_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.EXIT_ICON.clicked.connect(self.go_to_login)

        self.SideBar_Area.addWidget(self.EXIT_ICON) 
        self.EXIT_ICON.setContentsMargins(0, 0, 0, 0)       

        self.MainContent_Area.addWidget(self.SideBar_Widget)

    # ========================= สร้าง หน้าแสดงรายการสินค้า ============================= #

        # Scroll Area
        self.content_area = QtWidgets.QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setContentsMargins(0, 0, 0, 0)

        # Content widget
        self.content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QGridLayout(self.content_widget)  # เปลี่ยนเป็น QGridLayout
        self.content_widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.content_area.setWidget(self.content_widget)
        self.content_widget.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(20)
        self.content_layout.setContentsMargins(10, 10, 10, 10)

        # กำหนดจำนวนคอลัมน์ที่ต้องการในกริด
        self.columns = 4
        self.display_products()

    def display_products(self):
        # ดึงข้อมูลสินค้า
        products = get_headphone_products()

        # กำหนดค่าตัวแปรแถวและคอลัมน์สำหรับการแสดงสินค้า
        row = 0
        col = 0

        # Loop for adding product widgets
        for product in products:
            # Widget สำหรับแสดงผลสินค้าแต่ละรายการ
            product_widget = QtWidgets.QWidget()
            product_layout = QtWidgets.QVBoxLayout(product_widget)
            product_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # รูปภาพสินค้า
            label_image = QtWidgets.QLabel()
            image_path = f"assets/product_image/{product['product_code']}_pic.png"
            pixmap = QtGui.QPixmap(image_path)
            label_image.setPixmap(pixmap)
            label_image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_image.setScaledContents(True)
            label_image.setFixedSize(250, 250)
            product_layout.addWidget(label_image, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

            # ชื่อสินค้า
            label_name = QtWidgets.QLabel()
            label_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_name.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
            label_name.setWordWrap(True)  # ให้ขึ้นบรรทัดใหม่อัตโนมัติ
            label_name.setFixedWidth(200)  # กำหนดความกว้างสูงสุด
            label_name.setFixedHeight(50)  # ความสูงสูงสุดให้พอดี 2 บรรทัด

            # ใช้ QFontMetrics เพื่อตัดข้อความ แล้วแสดง ... แทน
            font_metrics = QtGui.QFontMetrics(label_name.font())
            # ให้ข้อความอยู่ในกรอบที่กำหนดและตัดออกเมื่อเกิน
            elided_text = font_metrics.elidedText(product["product_name"], QtCore.Qt.TextElideMode.ElideRight, 200)
            label_name.setText(elided_text)

            # จัดให้อยู่ตรงกลางทั้งแนวตั้งและแนวนอน
            product_layout.addWidget(label_name, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

            # ราคาสินค้า
            label_price = QtWidgets.QLabel(f"฿{product['price']:,}")
            label_price.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_price.setStyleSheet("""
                font-size: 18px;
                color: #007BFF;
                font-weight: bold;
                background-color: #e6f0ff;
                padding: 5px;
            """)
            product_layout.addWidget(label_price)

            # สร้างปุ่มเพิ่มสินค้า
            add_to_cart_button = QtWidgets.QPushButton("เพิ่มลงรถเข็น")
            add_to_cart_button.setStyleSheet("""
                QPushButton {
                    background-color: #007BFF;
                    color: white;
                    border-radius: 5px;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
                QPushButton:pressed {
                    background-color: #004085;
                }
            """)

            # เชื่อมปุ่มกับฟังก์ชันเพิ่มสินค้าในฐานข้อมูล
            add_to_cart_button.clicked.connect(lambda _, code=product['product_code']: self.add_to_cart_db(code))

            # เพิ่มปุ่มลงใน layout
            product_layout.addWidget(add_to_cart_button)

            # เพิ่ม product widget ลงใน layout ของกริด
            self.content_layout.addWidget(product_widget, row, col)

            # Update row and column for grid layout
            col += 1
            if col >= self.columns:
                col = 0
                row += 2

            # สร้างเส้นแบ่งแนวนอนหลังจากทุกๆ แถว
            if col == 0:
                separator = QtWidgets.QFrame()
                separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
                separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
                separator.setStyleSheet("color: #D3D3D3;")  # สีเทาอ่อน
                self.content_layout.addWidget(separator, row, 0, 1, self.columns)
                row += 1  # เพิ่ม row หลังจากเพิ่มเส้นแบ่ง

        # Add scroll area to main layout
        self.MainContent_Area.addWidget(self.content_area)
        self.content_area.setStyleSheet("""
            QScrollBar:vertical {
                background: #e0e0e0;
                width: 10px;
                margin: 22px 0 22px 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #a0a0a0;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
        """)



    #================= ฟังค์ชั่นไปหน้า LOGIN ================#
    
    def go_to_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า CART ========================#

    def go_to_cart(self):
        self.cart_window = CartWindow()
        self.cart_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า Comset ========================#

    def go_to_comset(self):
        self.comset_window = ComsetWindow()
        self.comset_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า Notebook ========================#

    def go_to_notebook(self):
        self.notebook_window = NotebookWindow()
        self.notebook_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า phone ========================#

    def go_to_phone(self):
        self.phone_window = PhoneWindow()
        self.phone_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า headphone ========================#

    def go_to_headphone(self):
        self.headphone_window = HeadphoneWindow()
        self.headphone_window.show()
        self.close()

    def go_to_contactus(self):
        self.contactus_window = ContactusWindow()
        self.contactus_window.show()
        self.close()
    
    #================= ฟังค์ชั่นไปหน้า HOMEPAGE ================#
    
    # def go_to_home(self):
    #     self.home_page = CartWindow()  # สร้างหน้าแรก
    #     self.home_page.show()  # แสดงหน้าแรก
    #     self.home_page.showMaximized()
    #     self.close()

    #================= ฟังค์ชั่นเพิ่มสินค้าเข้าฐานข้อมูล ================#

    def add_to_cart_db(self, product_code, quantity=1):
        # ตรวจสอบว่าได้ล็อคอินหรือยัง
        if not logged_in_user:
            self.show_message("Error", "กรุณาล็อคอินก่อนเพิ่มสินค้าลงในตะกร้า!", QtWidgets.QMessageBox.Icon.Warning)
            return

        # ดึง user_id จากฐานข้อมูลหรือใช้ค่าที่กำหนด
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # ค้นหาค่า user_id จากชื่อผู้ใช้ (logged_in_user)
                cursor.execute("SELECT user_id FROM user_register WHERE uname = %s", (logged_in_user,))
                result = cursor.fetchone()
                
                if result:
                    user_id = result[0]  # ดึง user_id
                    
                    # เช็คว่าในตะกร้ามีสินค้านี้แล้วหรือไม่ (อาจใช้ user_id และ product_code)
                    cursor.execute("""SELECT quantity FROM cart_items WHERE user_id = %s AND product_code = %s""", (user_id, product_code))
                    existing_item = cursor.fetchone()

                    if existing_item:
                        # ถ้ามีสินค้านี้แล้ว, เพิ่ม quantity เข้าไป
                        new_quantity = existing_item[0] + quantity
                        cursor.execute("""
                            UPDATE cart_items SET quantity = %s WHERE user_id = %s AND product_code = %s
                        """, (new_quantity, user_id, product_code))
                    else:
                        # ถ้ายังไม่มี, เพิ่มสินค้าใหม่ลงในตะกร้า
                        cursor.execute("""INSERT INTO cart_items (user_id, product_code, quantity) VALUES (%s, %s, %s)""", (user_id, product_code, quantity))

                    connection.commit()
                    # self.show_message("สำเร็จ", "สินค้าได้ถูกเพิ่มลงในตะกร้าแล้ว!", QtWidgets.QMessageBox.Icon.Information)
                else:
                    self.show_message("ข้อผิดพลาด", "ไม่พบผู้ใช้ในระบบ!", QtWidgets.QMessageBox.Icon.Warning)
            
            except mysql.connector.Error as e:
                self.show_message("ข้อผิดพลาด", f"เกิดข้อผิดพลาด: {e}", QtWidgets.QMessageBox.Icon.Critical)
            finally:
                cursor.close()
                connection.close()

# =================================== Message แจ้งเตือน =====================================================

    def show_message(self, title, message, icon):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))
        msg_box.exec()



# =================================== ADMIN HOME PAGE ==================================================#
class Admin_Editpage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Admin Edit Page')
        self.setStyleSheet('background-color: #ffffff; border-radius: 15px;')
        self.showMaximized()
        self.setWindowIcon(QIcon('image/IT ZONE LOGO.png'))


        # สร้าง container แนวตั้งมาเป็น layout หลัก
        Main_Layout = QtWidgets.QVBoxLayout()  # สร้าง instance ของ QVBoxLayout
        self.setLayout(Main_Layout)  
        Main_Layout.setContentsMargins(0, 0, 0, 0)



# ========================= MENU TOP BAR PART ========================= #

        # สร้าง MenuBar_Widget และเพิ่ม title
        self.MenuBar_Widget = QWidget()
        self.MenuBar_Area = QHBoxLayout(self.MenuBar_Widget)
        self.MenuBar_Widget.setFixedHeight(100)  # ความสูงเมนูด้านบน
        self.MenuBar_Widget.setStyleSheet('background-color: #295CA5; border-radius: 0px;')

# ============================================ ITZONE ICON ซ้ายบน ============================================ #    

        icon_ITZONE_label = QLabel(self)
        icon_pixmap = QPixmap("assets/image/ITZONEEDIT W.png")  # ระบุที่อยู่ของไฟล์ไอคอน
        icon_pixmap = icon_pixmap.scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_ITZONE_label.setPixmap(icon_pixmap)

        IT_ZONE_TOP_TITLE = QWidget()
        IT_ZONE_TOP_TITLE.setLayout(QHBoxLayout())
        IT_ZONE_TOP_TITLE.layout().addWidget(icon_ITZONE_label)

        self.MenuBar_Area.addWidget(IT_ZONE_TOP_TITLE)

# ============================================ SEARCHBAR ด้านบน ============================================ #        
        # เพิ่มแถบค้นหา
        search_bar_container = QWidget()
        search_bar_layout = QHBoxLayout(search_bar_container)
        search_bar_layout.setContentsMargins(0, 0, 0, 0)

        # สร้าง QLineEdit สำหรับแถบค้นหา
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("ค้นหาสินค้า...")
        search_bar.setFixedHeight(30)
        search_bar.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;  /* กำหนดสีของข้อความที่พิมพ์ลงไปในช่องค้นหา */
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
                padding-left: 10px;
                font-size: 14px;
                font-family: 'PK Nakhon Pathom Demo';
            }
            QLineEdit::placeholder { 
                color: gray;  /* เปลี่ยนเป็นสีที่คุณต้องการ */
                font-family: 'PK Nakhon Pathom Demo';
            }
        """)

        # สร้าง QLabel สำหรับไอคอนแว่นขยาย
        search_icon = QLabel()
        icon_pixmap = QPixmap("assets/image/magnifying glass icon.png").scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        search_icon.setPixmap(icon_pixmap)
        search_icon.setStyleSheet("""
            background-color: #295CA5;
            border-top-right-radius: 15px;
            border-bottom-right-radius: 15px;
            padding: 5px;
        """)

        # ใส่ search_bar และ search_icon ลงใน layout ของ search_bar_container
        search_bar_layout.addWidget(search_bar)
        search_bar_layout.addWidget(search_icon)

        # เพิ่ม search_bar_container ลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(search_bar_container)



# ============================================ รถเข็นสินค้า ============================================ #

        # # สร้างปุ่มสำหรับรถเข็นสินค้า
        # cart_button = QPushButton("   รถเข็นสินค้า")
        # cart_button.setIcon(QIcon("assets/image/cart icon.png"))  # ระบุ path ไปยังไอคอนรถเข็น
        # cart_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        # cart_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม
        # cart_button.setStyleSheet("""
        #     QPushButton {
        #         background-color: #295CA5;
        #         color: white;
        #         border-radius: 10px;
        #         padding: 5px 10px;
        #         padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
        #     }
        #     QPushButton:hover {
        #         background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
        #     }
        # """)
        # if logged_in_user == None:
        #     cart_button.clicked.connect(
        #         lambda: self.show_message("ยังไม่ล็อคอิน", "กรุณาล็อคอินเข้าสู่ระบบก่อน!", QtWidgets.QMessageBox.Icon.Warning)
        #     )
        # else:
        #     cart_button.clicked.connect(self.go_to_cart)
        # # ตั้งค่าฟอนต์
        # cart_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        # cart_button.setFont(cart_button_font)
        # # cart_button.clicked.connect()

        # # เพิ่มปุ่มลงใน MenuBar_Area
        # self.MenuBar_Area.addWidget(cart_button)

# ============================================ เข้าสู่ระบบ ============================================ #

        # # ใช้ global เพื่อตรวจสอบข้อมูลผู้ใช้งาน

        # ตรวจสอบว่ามีผู้ใช้งานล็อกอินหรือไม่
        if logged_in_user:
            # ถ้ามีผู้ใช้งานล็อกอิน แสดงชื่อผู้ใช้งานในปุ่ม
            user_button = QPushButton(f"   {logged_in_user}")
        else:
            # ถ้าไม่มีผู้ใช้งาน แสดงปุ่มเข้าสู่ระบบ
            user_button = QPushButton("   เข้าสู่ระบบ")

        # ตั้งค่าไอคอน
        user_button.setIcon(QIcon("assets/image/user icon.png"))  # ระบุ path ไปยังไอคอน
        user_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        user_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม

        # ตั้งค่า StyleSheet
        user_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)

        # ตั้งค่าฟอนต์
        user_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        user_button.setFont(user_button_font)
        user_button.clicked.connect(self.go_to_login)

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(user_button)

        # เพิ่ม MenuBar_Widget ลงใน Main_Layout
        Main_Layout.addWidget(self.MenuBar_Widget)


# ================================================================= 

#                         - CONTENT PART -

# ================================================================= 

        # สร้าง Container ของ MainContent ไว้เพื่อใส่เนื้อหา
        self.MainContent_Widget = QWidget()
        self.MainContent_Area = QHBoxLayout(self.MainContent_Widget)
        Main_Layout.addWidget(self.MainContent_Widget)
        self.MainContent_Widget.setContentsMargins(0, 0, 0, 0)
        self.MainContent_Area.setContentsMargins(0, 0, 0, 0)
        self.MainContent_Area.setAlignment(Qt.AlignmentFlag.AlignLeft)
# ========================= เมนูด้านแถบซ้าย ========================= #

        # สร้าง SideBar Menu เพื่อเพิ่มเมนู
        self.SideBar_Widget = QWidget()
        self.SideBar_Area = QVBoxLayout(self.SideBar_Widget)
        self.SideBar_Widget.setFixedWidth(80)  # กำหนดความกว้างของแถบด้านซ้าย
        self.SideBar_Widget.setStyleSheet('background-color: #295CA5; border-radius: 0px;')
        self.SideBar_Area.setContentsMargins(0, 0, 0, 0)

# ============================================ EDIT PRODUCT Button ============================================ #

        self.Addmin_edite_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.Addmin_edite_ICON.setIcon(QIcon("assets/image/edit_product icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.Addmin_edite_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.Addmin_edite_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.Addmin_edite_ICON.clicked.connect(self.go_to_admin_editpage)
        self.SideBar_Area.addWidget(self.Addmin_edite_ICON)

# ============================================ ADD NEW PRODUCT Button ============================================ #

        self.NOTEBOOK_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.NOTEBOOK_ICON.setIcon(QIcon("assets/image/add_product icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.NOTEBOOK_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.NOTEBOOK_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.NOTEBOOK_ICON.clicked.connect(self.go_to_add_new_product)
        self.SideBar_Area.addWidget(self.NOTEBOOK_ICON)

# ============================================ REPORT Button ============================================ #

        self.REPORT_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.REPORT_ICON.setIcon(QIcon("assets/image/report icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.REPORT_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.REPORT_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.REPORT_ICON.clicked.connect(self.go_to_report)
        self.SideBar_Area.addWidget(self.REPORT_ICON)

# ============================================ EXIT Button ============================================ #

        self.EXIT_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.EXIT_ICON.setIcon(QIcon("assets/image/EXIT icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.EXIT_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.EXIT_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.EXIT_ICON.clicked.connect(self.go_to_login)

        self.SideBar_Area.addWidget(self.EXIT_ICON) 
        self.EXIT_ICON.setContentsMargins(0, 0, 0, 0)       

        self.MainContent_Area.addWidget(self.SideBar_Widget)


    # ========================= สร้าง หน้าแสดงรายการสินค้า ============================= #

        # Scroll Area
        self.content_area = QtWidgets.QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setContentsMargins(0, 0, 0, 0)

        # Content widget
        self.content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QGridLayout(self.content_widget)  # เปลี่ยนเป็น QGridLayout
        self.content_widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.content_area.setWidget(self.content_widget)
        self.content_widget.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(20)
        self.content_layout.setContentsMargins(10, 10, 10, 10)


        # กำหนดจำนวนคอลัมน์ที่ต้องการในกริด
        self.columns = 4
        self.display_products()

    def get_all_products(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='db_itshop'
            )
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT product_code, product_name, price FROM products
            """
            cursor.execute(query)
            products = cursor.fetchall()
            cursor.close()
            connection.close()
            return products
        except mysql.connector.Error as e:
            print(f"Error connecting to database: {e}")
            return []


    def display_products(self):
        # ดึงข้อมูลสินค้า
        products = self.get_all_products()

        row = 0
        col = 0
        for product in products:
            product_widget = QtWidgets.QWidget()
            product_layout = QtWidgets.QVBoxLayout(product_widget)
            product_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # รูปภาพสินค้า
            label_image = QtWidgets.QLabel()
            image_path = f"assets/product_image/{product['product_code']}_pic.png"
            pixmap = QtGui.QPixmap(image_path)
            if not pixmap.isNull():
                label_image.setPixmap(pixmap)
            else:
                print(f"Image not found for {image_path}")
            label_image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_image.setScaledContents(True)
            label_image.setFixedSize(250, 250)
            product_layout.addWidget(label_image, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

            # ชื่อสินค้า
            label_name = QtWidgets.QLabel()
            label_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_name.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
            label_name.setWordWrap(True)
            label_name.setFixedWidth(200)
            label_name.setFixedHeight(50)
            font_metrics = QtGui.QFontMetrics(label_name.font())
            elided_text = font_metrics.elidedText(product["product_name"], QtCore.Qt.TextElideMode.ElideRight, 200)
            label_name.setText(elided_text)
            product_layout.addWidget(label_name, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

            # ราคาสินค้า
            label_price = QtWidgets.QLabel(f"฿{product['price']:,}")
            label_price.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            label_price.setStyleSheet("""
                font-size: 18px;
                color: #007BFF;
                font-weight: bold;
                background-color: #e6f0ff;
                padding: 5px;
            """)
            product_layout.addWidget(label_price)

            # ปุ่มแก้ไขสินค้า
            add_to_cart_button = QtWidgets.QPushButton("แก้ไขสินค้า")
            add_to_cart_button.setStyleSheet("""
                QPushButton {
                    background-color: #007BFF;
                    color: white;
                    border-radius: 5px;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
                QPushButton:pressed {
                    background-color: #004085;
                }
            """)
            add_to_cart_button.clicked.connect(lambda _, code=product['product_code']: self.go_to_edit_product(code))
            product_layout.addWidget(add_to_cart_button)

            # เพิ่ม widget ลงใน grid layout
            self.content_layout.addWidget(product_widget, row, col)
            col += 1
            if col >= self.columns:
                col = 0
                row += 2

            # เส้นแบ่งหลังแถว
            if col == 0:
                separator = QtWidgets.QFrame()
                separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)
                separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
                separator.setStyleSheet("color: #D3D3D3;")
                self.content_layout.addWidget(separator, row, 0, 1, self.columns)
                row += 1

        self.MainContent_Area.addWidget(self.content_area)


    #================= ฟังค์ชั่นไปหน้า LOGIN ================#
    
    def go_to_login(self):
        global logged_in_user
        logged_in_user = None  # รีเซ็ตค่า logged_in_user
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


    #================= ฟังค์ชั่นไปหน้า Comset ========================#

    def go_to_admin_editpage(self):
        self.admin_editpage_window = Admin_Editpage()
        self.admin_editpage_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า Notebook ========================#

    def go_to_add_new_product(self):
        self.add_new_product_window = AddNewProductWindow()
        self.add_new_product_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า edit product ========================#

    def go_to_edit_product(self, product_code):
        self.edit_product_window = EditProductWindow(product_code)
        self.edit_product_window.show()

    #================= ฟังค์ชั่นไปหน้า edit product ========================#

    def go_to_report(self):
        self.edit_product_window = AdminReportWindow()
        self.edit_product_window.show()
        self.close()

# =================================== Message แจ้งเตือน =====================================================

    def show_message(self, title, message, icon):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))
        msg_box.exec()



# =================================== EDIT PRODUCT PAGE ==================================================#
class EditProductWindow(QtWidgets.QWidget):
    def __init__(self, product_code):
        super().__init__()
        self.setWindowTitle("Edit Product")
        self.showMaximized()
        self.setWindowIcon(QIcon('image/IT ZONE LOGO.png'))

        self.product_code = product_code
        self.init_ui()
        self.load_product_details()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Header
        label_header = QtWidgets.QLabel(f"Edit Product: {self.product_code}")
        label_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label_header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 20px;
        """)
        layout.addWidget(label_header)

        # Product Image
        image_layout = QtWidgets.QHBoxLayout()  # ใช้ QHBoxLayout สำหรับจัดตำแหน่งรูปภาพในแนวนอน
        self.product_image_label = QtWidgets.QLabel()
        self.update_product_image()  # Call this method to display the image when initializing
        self.product_image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Align image to center within QLabel
        image_layout.addStretch()  # เพิ่มพื้นที่ว่างด้านซ้าย
        image_layout.addWidget(self.product_image_label)  # ใส่ QLabel สำหรับแสดงรูปภาพ
        image_layout.addStretch()  # เพิ่มพื้นที่ว่างด้านขวา
        layout.addLayout(image_layout)  # เพิ่ม layout นี้ใน layout หลัก

        # ปุ่มเลือกภาพ
        upload_image_button = QtWidgets.QPushButton("Upload New Image")
        upload_image_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;  /* สีพื้นหลัง */
                color: white;  /* สีข้อความ */
                border-radius: 5px;  /* มุมโค้งมน */
                font-size: 16px;  /* ขนาดตัวอักษร */
                padding: 10px 20px;  /* ขนาดระยะห่างภายใน */
                border: none;  /* ไม่ให้มีขอบ */
            }
            QPushButton:hover {
                background-color: #0056b3;  /* สีพื้นหลังเมื่อ hover */
            }
            QPushButton:pressed {
                background-color: #003d80;  /* สีพื้นหลังเมื่อกด */
            }
            QPushButton:disabled {
                background-color: #cccccc;  /* สีพื้นหลังเมื่อปุ่มถูกปิดการใช้งาน */
                color: #666666;  /* สีข้อความเมื่อปุ่มถูกปิดการใช้งาน */
            }
        """)
        upload_image_button.clicked.connect(self.upload_image)
        layout.addWidget(upload_image_button)

        # ชื่อสินค้า
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Enter product name")
        self.name_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        layout.addWidget(QtWidgets.QLabel("Product Name:"))
        layout.addWidget(self.name_input)

        # ราคาสินค้า
        self.price_input = QtWidgets.QLineEdit()
        self.price_input.setPlaceholderText("Enter product price")
        self.price_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        layout.addWidget(QtWidgets.QLabel("Product Price:"))
        layout.addWidget(self.price_input)

        # คำอธิบายสินค้า
        self.description_input = QtWidgets.QTextEdit()
        self.description_input.setPlaceholderText("Enter product description")
        self.description_input.setStyleSheet("""
            QTextEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            QTextEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        self.description_input.setMinimumHeight(300)
        layout.addWidget(QtWidgets.QLabel("Product Description:"))
        layout.addWidget(self.description_input)

        # สต็อกสินค้า
        self.stock_input = QtWidgets.QLineEdit()
        self.stock_input.setPlaceholderText("Enter product stock")
        self.stock_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        layout.addWidget(QtWidgets.QLabel("Product Stock:"))
        layout.addWidget(self.stock_input)

        # ปุ่มบันทึก
        save_button = QtWidgets.QPushButton("Save Changes")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                font-size: 16px;
                padding: 10px 20px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
            QPushButton:disabled {
                background-color: #b0bec5;
                color: #607d8b;
            }
        """)
        save_button.clicked.connect(self.save_product)
        layout.addWidget(save_button)

        # Create a QWidget to hold all the layout content
        content_widget = QtWidgets.QWidget()
        content_widget.setLayout(layout)

        # Create the scroll area
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)

        # Set the scroll area as the main layout of the window
        final_layout = QtWidgets.QVBoxLayout(self)
        final_layout.addWidget(scroll_area)

        self.setLayout(final_layout)

    def update_product_image(self):
        """Update the displayed product image"""
        image_path = f"assets/product_image/{self.product_code}_pic.png"
        if os.path.exists(image_path):
            pixmap = QtGui.QPixmap(image_path)
            self.product_image_label.setPixmap(pixmap)
            self.product_image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.product_image_label.setScaledContents(True)
            self.product_image_label.setFixedSize(250, 250)
        else:
            self.product_image_label.setText("Image not available")
            self.product_image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def upload_image(self):
        """Open a file dialog to upload a new product image"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select Product Image",
            "",
            "Images (*.png *.jpg *.bmp *.jpeg);;All Files (*)"
        )
        if file_path:
            # Define the path where the image will be saved
            destination_path = f"assets/product_image/{self.product_code}_pic.png"
            try:
                # Move the file to the desired directory
                shutil.copy(file_path, destination_path)  # Use shutil.copy to avoid issues with rename
                self.update_product_image()  # Update the displayed image
                QtWidgets.QMessageBox.information(self, "Success", "Image uploaded successfully!")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to upload image: {e}")

    def load_product_details(self):
        """Load product details from the database"""
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='db_itshop'
        )
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT product_name, price, description, stock 
            FROM products 
            WHERE product_code = %s
        """
        cursor.execute(query, (self.product_code,))
        product = cursor.fetchone()
        if product:
            self.name_input.setText(product["product_name"])
            self.price_input.setText(str(product["price"]))
            self.description_input.setPlainText(product["description"])
            self.stock_input.setText(str(product["stock"]))
        cursor.close()
        connection.close()

    def save_product(self):
        """Save product details to the database"""
        new_name = self.name_input.text()
        new_price = self.price_input.text()
        new_description = self.description_input.toPlainText()
        new_stock = self.stock_input.text()
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='db_itshop'
            )
            cursor = connection.cursor()
            query = """
                UPDATE products
                SET product_name = %s, price = %s, description = %s, stock = %s
                WHERE product_code = %s
            """
            cursor.execute(query, (new_name, new_price, new_description, new_stock, self.product_code))
            connection.commit()
            cursor.close()
            connection.close()
            QtWidgets.QMessageBox.information(self, "Success", "Product updated successfully!")
            self.close()
        except mysql.connector.Error as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to update product: {e}")


# =================================== ADD NEW PRODUCT PAGE ==================================================#
class AddNewProductWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Product")
        self.showMaximized()
        self.setWindowIcon(QIcon('image/IT ZONE LOGO.png'))

        self.product_code = None  # จะไม่มี product_code สำหรับการเพิ่มสินค้าใหม่
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Create Back Button
        back_button = QPushButton("←")
        back_button.setFixedSize(80, 40)
        back_button.setStyleSheet("""
            QPushButton {
                background-color:rgb(9, 66, 172);
                color: white;
                font-size: 16px;
                padding: 5px 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color:rgb(14, 89, 229);
            }
            QPushButton:pressed {
                background-color:rgb(14, 89, 229);
            }
        """)
        back_button.clicked.connect(self.go_to_admin_editpage)

        # Add the Back Button to the header layout
        layout.addWidget(back_button)
        layout.addStretch()

        # Header
        label_header = QtWidgets.QLabel("Add New Product")
        label_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label_header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 20px;
        """)
        layout.addWidget(label_header)

        # ชื่อสินค้า
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Enter product name")
        self.name_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        layout.addWidget(QtWidgets.QLabel("Product Name:"))
        layout.addWidget(self.name_input)

        # ราคาสินค้า
        self.price_input = QtWidgets.QLineEdit()
        self.price_input.setPlaceholderText("Enter product price")
        self.price_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        layout.addWidget(QtWidgets.QLabel("Product Price:"))
        layout.addWidget(self.price_input)

        # คำอธิบายสินค้า
        self.description_input = QtWidgets.QTextEdit()
        self.description_input.setPlaceholderText("Enter product description")
        self.description_input.setStyleSheet("""
            QTextEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            QTextEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        self.description_input.setMinimumHeight(300)
        layout.addWidget(QtWidgets.QLabel("Product Description:"))
        layout.addWidget(self.description_input)

        # สต็อกสินค้า
        self.stock_input = QtWidgets.QLineEdit()
        self.stock_input.setPlaceholderText("Enter product stock")
        self.stock_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        layout.addWidget(QtWidgets.QLabel("Product Stock:"))
        layout.addWidget(self.stock_input)


        # เลือกประเภทสินค้า (Dropdown)
        self.product_type_combo = QtWidgets.QComboBox()
        self.product_type_combo.addItem("เลือกประเภทสินค้า")
        self.product_type_combo.addItem("คอมเซ็ท (CS)")
        self.product_type_combo.addItem("หูฟัง (HP)")
        self.product_type_combo.addItem("โน๊ตบุ๊ค (NB)")
        self.product_type_combo.addItem("โทรศัพท์ (PH)")
        self.product_type_combo.setStyleSheet("""
            QComboBox {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            QComboBox:focus {
                border: 1px solid #4CAF50;
            }
            QComboBox QAbstractItemView {
                font-size: 16px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
        """)
        layout.addWidget(QtWidgets.QLabel("ประเภทสินค้า:"))
        layout.addWidget(self.product_type_combo)

        # ตัวย่อแบรนด์
        self.brand_input = QtWidgets.QLineEdit()
        self.brand_input.setPlaceholderText("กรอกตัวย่อแบรนด์ (2 ตัวอักษร)")

        # ตั้งค่า QValidator สำหรับให้กรอกแค่ 2 ตัวอักษร
        self.brand_input.setMaxLength(2)

        # การตั้งค่าให้แปลงตัวอักษรเป็นตัวใหญ่ทุกครั้งที่พิมพ์
        self.brand_input.textChanged.connect(self.convert_to_uppercase)

        # ตั้งค่ารูปแบบสไตล์
        self.brand_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        
        # เพิ่ม QLabel และ QLineEdit เข้าไปใน layout
        layout.addWidget(QtWidgets.QLabel("ตัวย่อแบรนด์:"))
        layout.addWidget(self.brand_input)

        self.setLayout(layout)

        # ปุ่มบันทึก
        save_button = QtWidgets.QPushButton("Save New Product")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                font-size: 16px;
                padding: 10px 20px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
            QPushButton:disabled {
                background-color: #b0bec5;
                color: #607d8b;
            }
        """)
        save_button.clicked.connect(self.save_product)
        layout.addWidget(save_button)

        # สร้าง QWidget เพื่อเก็บเนื้อหาเค้าโครงทั้งหมด
        content_widget = QtWidgets.QWidget()
        content_widget.setLayout(layout)

        # สร้าง scroll area
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)

        # ตั้งค่าพื้นที่เลื่อนเป็นเค้าโครงหลักของหน้าต่าง
        final_layout = QtWidgets.QVBoxLayout(self)
        final_layout.addWidget(scroll_area)

        self.setLayout(final_layout)


    def go_to_admin_editpage(self):
        self.admin_editpage_window = Admin_Editpage()
        self.admin_editpage_window.show()
        self.close()


    def convert_to_uppercase(self):
        text = self.brand_input.text().upper()  # แปลงข้อความเป็นตัวใหญ่
        self.brand_input.setText(text)  # กำหนดค่าใหม่ให้กับ QLineEdit


    def save_product(self):
        new_name = self.name_input.text()
        new_price = self.price_input.text()
        new_description = self.description_input.toPlainText()
        new_stock = self.stock_input.text()

        product_type_full = self.product_type_combo.currentText()
        brand_full = self.brand_input.text()

        product_type = product_type_full.split('(')[-1].split(')')[0]
        brand = brand_full.split('(')[-1].split(')')[0]

        new_product_code = self.generate_product_code(product_type, brand)

        if new_product_code is None:
            return

        self.new_product_code = new_product_code

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='db_itshop'
            )
            cursor = connection.cursor()
            query = """
                INSERT INTO products (product_code, product_name, price, description, stock)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (new_product_code, new_name, new_price, new_description, new_stock))
            connection.commit()
            cursor.close()
            connection.close()

            QtWidgets.QMessageBox.information(self, "Success", "Product added successfully!")
            
            # เปิดหน้าต่างสำหรับอัปโหลดรูปภาพหลังจากบันทึกเสร็จ
            self.upload_window = UploadImageWindow(self.new_product_code)
            self.upload_window.show()

        except mysql.connector.Error as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to add product: {e}")



    # ฟังก์ชันคำนวนและรันตัวเลข product code
    def generate_product_code(self, product_type, brand):
        try:
            # เชื่อมต่อฐานข้อมูล
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='db_itshop'
            )
            cursor = connection.cursor()
            print(product_type)

            # ดึงข้อมูล product_code ที่ตรงกับประเภทสินค้า
            query = """SELECT product_code FROM products WHERE product_code LIKE %s"""
            like_pattern = f"{product_type}%"
            cursor.execute(query, (like_pattern,))
            results = cursor.fetchall()  # ดึงข้อมูลทั้งหมด
            cursor.close()
            connection.close()

            if not results:
                # หากไม่มีข้อมูล ให้เริ่มต้นรันจาก 1
                return 1

            # ตัดตัวอักษร 4 ตัวแรกออกและแปลงตัวเลขที่เหลือ
            running_numbers = []
            for row in results:
                product_code = row[0]  # product_code ในแต่ละแถว
                number_part = product_code[4:]  # ตัดตัวอักษร 4 ตัวแรกออก
                if number_part.isdigit():  # ตรวจสอบว่าเป็นตัวเลขหรือไม่
                    running_numbers.append(int(number_part))

            # หาเลขรันสูงสุด
            max_running_number = max(running_numbers, default=0)
            max_running_number += 1  # เพิ่มค่า 1 สำหรับรันถัดไป
            max_running_number_str = str(max_running_number)

            # เติม 0 ขึ้นอยู่กับจำนวนหลักของ max_running_number
            if len(max_running_number_str) == 1:
                product_number = "000" + max_running_number_str  # เติม 0 ไป 3 ตัว
            elif len(max_running_number_str) == 2:
                product_number = "00" + max_running_number_str  # เติม 0 ไป 2 ตัว
            elif len(max_running_number_str) == 3:
                product_number = "0" + max_running_number_str  # เติม 0 ไป 1 ตัว
            else:
                product_number = max_running_number_str  # ถ้ามี 4 หลักแล้วไม่ต้องเติม 0

            # สร้าง new_product_code โดยใช้ product_type, brand, และ max_running_number
            new_product_code = f"{product_type[:2]}{brand[:2]}{product_number}"
            print(new_product_code)

            return new_product_code

        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return None




# =================================== UPLOAD IMAGE PAGE ==================================================#
class UploadImageWindow(QtWidgets.QWidget):
    def __init__(self, product_code):
        super().__init__()
        self.setWindowTitle("Upload Product Image")
        self.setWindowIcon(QIcon('image/IT ZONE LOGO.png'))
        self.product_code = product_code  # รับรหัสสินค้าเพื่อใช้ในการจัดเก็บภาพ
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # เพิ่มการปรับขนาดหน้าต่างให้ใหญ่ขึ้น
        self.resize(800, 600)  # ขนาดหน้าต่างใหม่ที่ใหญ่ขึ้น

        label_header = QtWidgets.QLabel("Upload Image for Product")
        label_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label_header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 20px;
        """)
        layout.addWidget(label_header)

        # เพิ่ม QLabel สำหรับแสดงภาพและตั้งค่าการจัดตำแหน่ง
        self.product_image_label = QtWidgets.QLabel()
        self.product_image_label.setText("No image selected")
        self.product_image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # จัดภาพให้อยู่ตรงกลาง
        layout.addWidget(self.product_image_label)

        # ปุ่มอัพโหลด
        upload_button = QtWidgets.QPushButton("Upload Image")
        upload_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                font-size: 16px;
                padding: 10px 20px;
            }
        """)
        upload_button.clicked.connect(self.upload_image)
        layout.addWidget(upload_button)

        self.setLayout(layout)

    def upload_image(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Product Image", "", "Images (*.png *.jpg *.bmp *.jpeg)")

        if file_path:
            destination_path = f"assets/product_image/{self.product_code}_pic.png"
            try:
                shutil.copy(file_path, destination_path)
                pixmap = QtGui.QPixmap(destination_path)
                self.product_image_label.setPixmap(pixmap)
                self.product_image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # จัดภาพให้ตรงกลาง
                self.product_image_label.setScaledContents(True)
                self.product_image_label.setFixedSize(250, 250)  # ขนาดภาพที่แสดง
                QtWidgets.QMessageBox.information(self, "Success", "Image uploaded successfully!")
                        
                # หลังจากบันทึกแล้ว ให้กลับไปที่ EditProductWindow
                self.go_to_admin_editpage()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to upload image: {e}")

    #================= ฟังค์ชั่นไปหน้า admin edit product ========================#

    def go_to_admin_editpage(self):
        self.admin_editpage_window = Admin_Editpage()
        self.admin_editpage_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า edit product ========================#

    def go_to_report(self):
        self.edit_product_window = AdminReportWindow()
        self.edit_product_window.show()




# =================================== ADMIN HOME PAGE ==================================================#

class AdminReportWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Admin Edit Page')
        self.setStyleSheet('background-color: #ffffff; border-radius: 15px;')
        self.showMaximized()
        self.setWindowIcon(QIcon('image/IT ZONE LOGO.png'))


        # สร้าง container แนวตั้งมาเป็น layout หลัก
        Main_Layout = QtWidgets.QVBoxLayout()  # สร้าง instance ของ QVBoxLayout
        self.setLayout(Main_Layout)  
        Main_Layout.setContentsMargins(0, 0, 0, 0)



# ========================= MENU TOP BAR PART ========================= #

        # สร้าง MenuBar_Widget และเพิ่ม title
        self.MenuBar_Widget = QWidget()
        self.MenuBar_Area = QHBoxLayout(self.MenuBar_Widget)
        self.MenuBar_Widget.setFixedHeight(100)  # ความสูงเมนูด้านบน
        self.MenuBar_Widget.setStyleSheet('background-color: #295CA5; border-radius: 0px;')

# ============================================ ITZONE ICON ซ้ายบน ============================================ #    

        icon_ITZONE_label = QLabel(self)
        icon_pixmap = QPixmap("assets/image/ITZONEEDIT W.png")  # ระบุที่อยู่ของไฟล์ไอคอน
        icon_pixmap = icon_pixmap.scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_ITZONE_label.setPixmap(icon_pixmap)

        IT_ZONE_TOP_TITLE = QWidget()
        IT_ZONE_TOP_TITLE.setLayout(QHBoxLayout())
        IT_ZONE_TOP_TITLE.layout().addWidget(icon_ITZONE_label)

        self.MenuBar_Area.addWidget(IT_ZONE_TOP_TITLE)

# ============================================ SEARCHBAR ด้านบน ============================================ #
        # เพิ่มแถบค้นหา
        search_bar_container = QWidget()
        search_bar_layout = QHBoxLayout(search_bar_container)
        search_bar_layout.setContentsMargins(0, 0, 0, 0)

        # สร้าง QLineEdit สำหรับแถบค้นหา
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("ค้นหาสินค้า...")
        search_bar.setFixedHeight(30)
        search_bar.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;  /* กำหนดสีของข้อความที่พิมพ์ลงไปในช่องค้นหา */
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
                padding-left: 10px;
                font-size: 14px;
                font-family: 'PK Nakhon Pathom Demo';
            }
            QLineEdit::placeholder { 
                color: gray;  /* เปลี่ยนเป็นสีที่คุณต้องการ */
                font-family: 'PK Nakhon Pathom Demo';
            }
        """)

        # สร้าง QLabel สำหรับไอคอนแว่นขยาย
        search_icon = QLabel()
        icon_pixmap = QPixmap("assets/image/magnifying glass icon.png").scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        search_icon.setPixmap(icon_pixmap)
        search_icon.setStyleSheet("""
            background-color: #295CA5;
            border-top-right-radius: 15px;
            border-bottom-right-radius: 15px;
            padding: 5px;
        """)

        # ใส่ search_bar และ search_icon ลงใน layout ของ search_bar_container
        search_bar_layout.addWidget(search_bar)
        search_bar_layout.addWidget(search_icon)

        # เพิ่ม search_bar_container ลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(search_bar_container)

# ============================================ รถเข็นสินค้า ============================================ #

        # # สร้างปุ่มสำหรับรถเข็นสินค้า
        # cart_button = QPushButton("   รถเข็นสินค้า")
        # cart_button.setIcon(QIcon("assets/image/cart icon.png"))  # ระบุ path ไปยังไอคอนรถเข็น
        # cart_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        # cart_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม
        # cart_button.setStyleSheet("""
        #     QPushButton {
        #         background-color: #295CA5;
        #         color: white;
        #         border-radius: 10px;
        #         padding: 5px 10px;
        #         padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
        #     }
        #     QPushButton:hover {
        #         background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
        #     }
        # """)
        # if logged_in_user == None:
        #     cart_button.clicked.connect(
        #         lambda: self.show_message("ยังไม่ล็อคอิน", "กรุณาล็อคอินเข้าสู่ระบบก่อน!", QtWidgets.QMessageBox.Icon.Warning)
        #     )
        # else:
        #     cart_button.clicked.connect(self.go_to_cart)
        # # ตั้งค่าฟอนต์
        # cart_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        # cart_button.setFont(cart_button_font)
        # # cart_button.clicked.connect()

        # # เพิ่มปุ่มลงใน MenuBar_Area
        # self.MenuBar_Area.addWidget(cart_button)

# ============================================ เข้าสู่ระบบ ============================================ #

        # # ใช้ global เพื่อตรวจสอบข้อมูลผู้ใช้งาน

        # ตรวจสอบว่ามีผู้ใช้งานล็อกอินหรือไม่
        if logged_in_user:
            # ถ้ามีผู้ใช้งานล็อกอิน แสดงชื่อผู้ใช้งานในปุ่ม
            user_button = QPushButton(f"   {logged_in_user}")
        else:
            # ถ้าไม่มีผู้ใช้งาน แสดงปุ่มเข้าสู่ระบบ
            user_button = QPushButton("   เข้าสู่ระบบ")

        # ตั้งค่าไอคอน
        user_button.setIcon(QIcon("assets/image/user icon.png"))  # ระบุ path ไปยังไอคอน
        user_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        user_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม

        # ตั้งค่า StyleSheet
        user_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;  /* เพิ่มระยะห่างซ้ายสำหรับไอคอน */
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* เปลี่ยนสีเมื่อเอาเมาส์ชี้ */
            }
        """)

        # ตั้งค่าฟอนต์
        user_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        user_button.setFont(user_button_font)
        user_button.clicked.connect(self.go_to_login)

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(user_button)

        # เพิ่ม MenuBar_Widget ลงใน Main_Layout
        Main_Layout.addWidget(self.MenuBar_Widget)


# ================================================================= 

#                         - CONTENT PART -

# ================================================================= 

        # สร้าง Container ของ MainContent ไว้เพื่อใส่เนื้อหา
        self.MainContent_Widget = QWidget()
        self.MainContent_Area = QHBoxLayout(self.MainContent_Widget)
        Main_Layout.addWidget(self.MainContent_Widget)
        self.MainContent_Widget.setContentsMargins(0, 0, 0, 0)
        self.MainContent_Area.setContentsMargins(0, 0, 0, 0)
        self.MainContent_Area.setAlignment(Qt.AlignmentFlag.AlignLeft)
# ========================= เมนูด้านแถบซ้าย ========================= #

        # สร้าง SideBar Menu เพื่อเพิ่มเมนู
        self.SideBar_Widget = QWidget()
        self.SideBar_Area = QVBoxLayout(self.SideBar_Widget)
        self.SideBar_Widget.setFixedWidth(80)  # กำหนดความกว้างของแถบด้านซ้าย
        self.SideBar_Widget.setStyleSheet('background-color: #295CA5; border-radius: 0px;')
        self.SideBar_Area.setContentsMargins(0, 0, 0, 0)

# ============================================ EDIT PRODUCT Button ============================================ #

        self.Addmin_edite_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.Addmin_edite_ICON.setIcon(QIcon("assets/image/edit_product icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.Addmin_edite_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.Addmin_edite_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.Addmin_edite_ICON.clicked.connect(self.go_to_admin_editpage)
        self.SideBar_Area.addWidget(self.Addmin_edite_ICON)

# ============================================ ADD NEW PRODUCT Button ============================================ #

        self.NOTEBOOK_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.NOTEBOOK_ICON.setIcon(QIcon("assets/image/add_product icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.NOTEBOOK_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.NOTEBOOK_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.NOTEBOOK_ICON.clicked.connect(self.go_to_add_new_product)
        self.SideBar_Area.addWidget(self.NOTEBOOK_ICON)

# ============================================ REPORT Button ============================================ #

        self.REPORT_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.REPORT_ICON.setIcon(QIcon("assets/image/report icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.REPORT_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.REPORT_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.REPORT_ICON.clicked.connect(self.go_to_report)
        self.SideBar_Area.addWidget(self.REPORT_ICON)

# ============================================ EXIT Button ============================================ #

        self.EXIT_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        self.EXIT_ICON.setIcon(QIcon("assets/image/EXIT icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        self.EXIT_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        self.EXIT_ICON.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #295CA5;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;  /* สีเมื่อ hover */
            }
        """)
        self.EXIT_ICON.clicked.connect(self.go_to_login)

        self.SideBar_Area.addWidget(self.EXIT_ICON) 
        self.EXIT_ICON.setContentsMargins(0, 0, 0, 0)       

        self.MainContent_Area.addWidget(self.SideBar_Widget)


    # ========================= สร้าง หน้าแสดงรายการสินค้า ============================= #

        # Scroll Area
        self.content_area = QtWidgets.QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setContentsMargins(0, 0, 0, 0)

    # ========================= สร้าง หน้าแสดงรายการสินค้า ============================= #

        # Scroll Area
        self.content_area = QtWidgets.QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setContentsMargins(0, 0, 0, 0)

        # Content widget
        self.content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QGridLayout(self.content_widget)
        self.content_widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.content_area.setWidget(self.content_widget)
        self.content_widget.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(20)
        self.content_layout.setContentsMargins(10, 10, 10, 10)

        # Dropdown
        self.number_dropdown = QtWidgets.QComboBox(self)
        self.number_dropdown.addItems([str(i) for i in range(1, 13)])
        self.number_dropdown.setFixedSize(500, 100)
        self.number_dropdown.setStyleSheet("""
            QComboBox {
                background-color: #f1f8ff;  /* สีฟ้าอ่อน */
                border: 1px solid #007bff;  /* กรอบน้ำเงิน */
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                color: #007bff;  /* ตัวหนังสือสีน้ำเงิน */
            }
            QComboBox::drop-down {
                border: none;
                background-color: #f1f8ff;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                border: 1px solid #007bff;  /* กรอบสีฟ้า */
                color: #007bff;
            }
        """)

        # Download button
        self.download_button = QtWidgets.QPushButton("Download", self)
        self.download_button.clicked.connect(self.download_action)
        self.download_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;  /* น้ำเงิน */
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #0056b3;  /* สีฟ้าเข้มเมื่อเอาเมาส์ไป */
            }
            QPushButton:pressed {
                background-color: #004085;  /* น้ำเงินเข้มเมื่อกด */
            }
        """)

        self.content_layout.addWidget(self.number_dropdown)
        self.content_layout.addWidget(self.download_button)

        # Add scroll area to main layout
        self.MainContent_Area.addWidget(self.content_area)
        self.content_area.setStyleSheet("""
            QScrollBar:vertical {
                background: #e0e0e0;
                width: 10px;
                margin: 22px 0 22px 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #a0a0a0;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
        """)


    def download_action(self):
        month = int(self.number_dropdown.currentText())  # Get month from dropdown
        self.create_pdf_report(month)

    def get_product_data(self):
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

    def get_saled_quantity(self, product_code, month):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='db_itshop'
            )
            cursor = connection.cursor()
            query = """
            SELECT SUM(quantity) AS total_saled 
            FROM order_detail 
            WHERE product_code = %s 
            AND MONTH(order_date) = %s
            """
            cursor.execute(query, (product_code, month))
            result = cursor.fetchone()
            return result[0] if result[0] else 0  # Return total quantity sold
        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return 0
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def truncate_text(self, text, max_length=10):
        return text[:max_length] + "..." if len(text) > max_length else text

    def format_price(self, price):
        return f"฿{price:,.2f}"  # Format price with ฿ and commas for thousands

    def get_month_name(self, month):
        thai_months = [
            "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
            "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
        ]
        return thai_months[month - 1] if 1 <= month <= 12 else "ไม่ทราบเดือน"

    def create_pdf_report(self, month):
        saled_total = 0
        month_name = self.get_month_name(month)

        # Setup for PDF creation
        font_path = "fonts/Kanit/Kanit-ExtraLight.ttf"
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"ไม่พบไฟล์ฟอนต์ที่: {font_path}")
        pdfmetrics.registerFont(TTFont('THSarabun', font_path))

        styles = getSampleStyleSheet()
        thai_style_left = ParagraphStyle(name='ThaiStyleLeft', fontName='THSarabun', fontSize=14, alignment=0)
        thai_style_right = ParagraphStyle(name='ThaiStyleRight', fontName='THSarabun', fontSize=14, alignment=2)

        pdf_file = "product_report.pdf"
        pdf = SimpleDocTemplate(
            pdf_file, 
            pagesize=letter,
            topMargin=20,  # Reduce top margin
            leftMargin=50,
            rightMargin=50,
            bottomMargin=30
        )

        heading_center = Paragraph(
            f"รายงานผลประกอบการประจำเดือน {month_name}<br/>ของร้าน IT ZONE Shop",
            ParagraphStyle(
                name='CenterHeading',
                fontName='THSarabun',
                fontSize=16,
                alignment=1,  # Center alignment
                leading=24,
                spaceAfter=6
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

        # Get product data from the database
        product_data = self.get_product_data()

        data = [["PRODUCT_CODE", "PRODUCT_NAME", "PRICE", "SALED_QUANTITY", "STOCK", "TOTAL"]]
        for product in product_data:
            truncated_name = self.truncate_text(product['product_name'])
            formatted_price = self.format_price(product['price'])
            saled_quantity = self.get_saled_quantity(product['product_code'], month)  # Get quantity sold for the selected month
            total = product['price'] * saled_quantity
            saled_total += total
            formatted_total = self.format_price(total)
            
            data.append([
                product['product_code'],
                truncated_name,
                formatted_price,
                saled_quantity,
                product['stock'],
                formatted_total
            ])

        formatted_saled_total = self.format_price(saled_total)
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        heading_left = Paragraph(f"STORE: Online store<br/>ผู้พิมพ์: admin<br/>PRINT DATE: {current_date}", thai_style_left)
        heading_right = Paragraph(f"SALED TOTAL: {formatted_saled_total}", thai_style_right)

        header_data = [[heading_left, heading_right]]
        header_table = Table(header_data, colWidths=[300, 300])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (0, -1), 40),
            ('RIGHTPADDING', (1, 0), (1, -1), 40),
            ('FONTNAME', (0, 0), (-1, -1), 'THSarabun'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
        ]))

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#DAE9F7')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
            ('ALIGN', (0, 1), (1, -1), 'LEFT'),
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),
            ('ALIGN', (5, 1), (5, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'THSarabun'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ]))

        elements = [heading_center, header_table, table]
        pdf.build(elements)

        print(f"PDF report created: {pdf_file}")




    #================= ฟังค์ชั่นไปหน้า LOGIN ================#

    def go_to_login(self):
        global logged_in_user
        logged_in_user = None  # รีเซ็ตค่า logged_in_user
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


    #================= ฟังค์ชั่นไปหน้า Comset ========================#

    def go_to_admin_editpage(self):
        self.admin_editpage_window = Admin_Editpage()
        self.admin_editpage_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า Notebook ========================#

    def go_to_add_new_product(self):
        self.add_new_product_window = AddNewProductWindow()
        self.add_new_product_window.show()
        self.close()

    #================= ฟังค์ชั่นไปหน้า edit product ========================#

    def go_to_edit_product(self, product_code):
        self.edit_product_window = EditProductWindow(product_code)
        self.edit_product_window.show()

    #================= ฟังค์ชั่นไปหน้า edit product ========================#

    def go_to_report(self):
        self.report_window = AdminReportWindow()
        self.report_window.show()
        self.close()

# =================================== Message แจ้งเตือน =====================================================

    def show_message(self, title, message, icon):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.setWindowIcon(QtGui.QIcon("image/IT ZONE LOGO.png"))
        msg_box.exec()






# พวกสีของกล่องข้อความ QMessageBox เบสท์แต่งไว้แล้วนะ
def main():
    app = QtWidgets.QApplication(sys.argv)
    home_page = Homepage()
    home_page.resize(1920, 1080)  # หรือใช้ขนาดตามที่คุณต้องการ
    home_page.show() 
    sys.exit(app.exec())

main()


# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     admin_home_page = Admin_Editpage()
#     admin_home_page.resize(1920, 1080)  # หรือใช้ขนาดตามที่คุณต้องการ
#     admin_home_page.show() 
#     sys.exit(app.exec())

# main()