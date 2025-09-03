import sys
import mysql
from db import create_connection
from PyQt6 import QtWidgets, QtGui, QtCore 
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

# เก็บข้อมูลบัญชีผู้ใช้ #
user_data = {}
logged_in_user = None  # เก็บชื่อผู้ใช้ที่เข้าสู่ระบบ #

class CartWindow(QtWidgets.QWidget):
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

        # ตั้งค่าฟอนต์
        cart_button_font = QFont("PK Nakhon Pathom Demo", 12)  # กำหนดชื่อฟอนต์และขนาด
        cart_button.setFont(cart_button_font)
        # cart_button.clicked.connect()

        # เพิ่มปุ่มลงใน MenuBar_Area
        self.MenuBar_Area.addWidget(cart_button)

# ============================================ เข้าสู่ระบบ ============================================ #

        # สร้างปุ่มสำหรับรถเข็นสินค้า
        user_button = QPushButton("   เข้าสู่ระบบ")
        user_button.setIcon(QIcon("assets/image/user icon.png"))  # ระบุ path ไปยังไอคอนรถเข็น
        user_button.setIconSize(QSize(30, 30))  # ตั้งขนาดไอคอนตามที่ต้องการ
        user_button.setFixedHeight(30)  # กำหนดความสูงของปุ่ม
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
        # user_button.clicked.connect(self.go_to_login)

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

        COMSET_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        COMSET_ICON.setIcon(QIcon("assets/image/COMSET icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        COMSET_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        COMSET_ICON.setStyleSheet("""
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
        
        self.SideBar_Area.addWidget(COMSET_ICON)

# ============================================ NOTEBOOK Button ============================================ #

        NOTEBOOK_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        NOTEBOOK_ICON.setIcon(QIcon("assets/image/NOTEBOOK icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        NOTEBOOK_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        NOTEBOOK_ICON.setStyleSheet("""
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

        self.SideBar_Area.addWidget(NOTEBOOK_ICON)

# ============================================ PHONE Button ============================================ #

        PHONE_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        PHONE_ICON.setIcon(QIcon("assets/image/PHONE icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        PHONE_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        PHONE_ICON.setStyleSheet("""
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

        self.SideBar_Area.addWidget(PHONE_ICON)

# ============================================ HEADPHONE Button ============================================ #

        HEADPHONE_ICON = QPushButton()  # ปุ่มที่มีข้อความ
        HEADPHONE_ICON.setIcon(QIcon("assets/image/HEADPHONE icon.png"))  # เปลี่ยน path ให้ถูกต้องกับไฟล์ไอคอนของคุณ
        HEADPHONE_ICON.setIconSize(QSize(40, 40))  # ขนาดไอคอน
        HEADPHONE_ICON.setStyleSheet("""
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

        self.SideBar_Area.addWidget(HEADPHONE_ICON)

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
        # self.EXIT_ICON.clicked.connect(self.go_to_login)

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

        # เริ่มต้นตัวแปร cart_count เพื่อเก็บจำนวนสินค้าในตะกร้า
        self.cart_count = 20  # สมมุติว่ามีสินค้าเริ่มต้น 20 รายการ
        # Cart Title = ตะกร้าสินค้า
        self.Cart_Title = QLabel(f'ตะกร้าสินค้า ({self.cart_count})')
        self.product_selected_layout.addWidget(self.Cart_Title)
        self.Cart_Title.setStyleSheet("""
        QLabel {
                font-size: 20px;
                color: black;
                font-weight: 400;
        }
        """)
# ========================= สร้าง แถบรายละเอียดและจำนวนสินค้าในตะกร้า ========================= # ไว้ใส่ รูป ชื่อ ราคา จำนวน และ ถังขยะ
        # เพิ่มวิดเจ็ตลงใน inner_widget
        for i in range(self.cart_count):  # เพิ่มวิดเจ็ต 20 ตัวเพื่อทดสอบการเลื่อน
            self.product_inner_widget = QtWidgets.QWidget()
            self.product_inner_layout = QtWidgets.QHBoxLayout(self.product_inner_widget)
            self.product_inner_widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum) # ปรับขนาดให้ fixed

# ========================= style สำหรับ product inner ========================= #
            self.product_inner_widget.setObjectName("productInnerWidget")
            self.product_inner_widget.setStyleSheet("""
            #productInnerWidget {
                background-color: white;
                border-bottom: 1px solid #d3d3d3;
                border-radius: 0px;
            }
            """)
            #เพิ่ม product_inner_widget ลงใน content_layout
            self.product_selected_layout.addWidget(self.product_inner_widget) 
            self.product_inner_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
            self.product_selected_layout.addWidget(self.product_inner_widget, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
            self.product_selected_widget.setFixedWidth(1000)

# ========================= เพิ่มรูปสินค้า ในแถบรายละเอียดและจำนวนสินค้า ========================= #
            # สร้าง widget สำหรับรูปภาพเพื่อจัดการ margin
            self.image_widget = QtWidgets.QWidget()
            self.image_layout = QtWidgets.QHBoxLayout(self.image_widget)
            self.image_layout.setContentsMargins(0, 0, 16, 0)  # เพิ่มระยะห่างด้านขวา  # (Left, Top, Right, Bottom)
            self.image_layout.setSpacing(0)  # ไม่ให้มีช่องว่างเพิ่มระหว่าง layout และ widget ภายใน

            # เพิ่ม QLabel สำหรับรูปสินค้า
            image_label = QtWidgets.QLabel()
            pixmap = QPixmap(r'assets\product_image\NBGB0001_pic.jpg')  # ใส่ชื่อไฟล์รูปสินค้า
            pixmap = pixmap.scaled(85, 85)  # กำหนดขนาดของรูปภาพ
            image_label.setPixmap(pixmap)

            # เพิ่ม image_label เข้าไปใน image_layout
            self.image_layout.addWidget(image_label)

            # เพิ่ม image_widget เข้าไปใน product_inner_layout
            self.product_inner_layout.addWidget(self.image_widget)
            self.product_inner_layout.setStretch(self.product_inner_layout.count() - 1, 0)  # รูปภาพไม่ให้ยืด

# ========================= เพิ่มชื่อสินค้า ในแถบรายละเอียดและจำนวนสินค้า ========================= #
            # เพิ่ม QLabel สำหรับชื่อสินค้า
            label = QtWidgets.QLabel('โน๊ตบุ๊ค Gigabyte AORUS 15 BSF-73TH754SH Black')
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)  # ตั้งค่าให้ข้อความชิดขอบบน
            label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: black;
            }
            """)
            self.product_inner_layout.addWidget(label)
            self.product_inner_layout.setStretch(self.product_inner_layout.count() - 1, 1)  # ชื่อสินค้าให้ยืด

# ========================= เพิ่มช่องไว้ใส่ ราคาสินค้าและส่วนลด ในแถบรายละเอียดและจำนวนสินค้า ========================= #
            self.product_price_widget = QtWidgets.QWidget()
            self.product_price_layout = QtWidgets.QVBoxLayout(self.product_price_widget)
            self.product_price_widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum) # ปรับขนาดให้ fixed
            self.product_inner_layout.addSpacing(32)  # เพิ่มระยะห่าง 32px ก่อนจะเพิ่ม widget 
            self.product_inner_layout.addWidget(self.product_price_widget) #เพิ่ม product_price_widget ลงใน product_inner_layout
            self.product_price_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop) # ตั้งค่า layout ชิดขอบบน
            # เพิ่มราคาสินค้า
            price_label = QtWidgets.QLabel('฿52,000')
            price_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)  # ชิดขอบซ้ายและบน
            price_label.setStyleSheet("""
            QLabel {
                color: #F1574F;
                font-size: 16px;
            }
            """)
            self.product_price_layout.addWidget(price_label)
            self.product_inner_layout.setStretch(self.product_inner_layout.count() - 1, 1)  # ราคาสินค้าให้ยืด
            # เพิ่มส่วนลด
            sale_price_label = QtWidgets.QLabel('ประหยัด ฿13,000')
            price_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)  # ชิดขอบซ้ายและบน
            sale_price_label.setStyleSheet("""
            QLabel {
                color: #878787;
                font-size: 12px;
            }
            """)
            self.product_price_layout.addWidget(sale_price_label)
            self.product_inner_layout.setStretch(self.product_inner_layout.count() - 1, 1)  # ลดราคาสินค้าให้ยืด
            # กำหนดระยะห่างใน layout
            self.product_price_layout.setContentsMargins(0, 0, 0, 0)  # กำหนดขอบ

# ========================= เพิ่มช่องไว้ใส่ จำนวนสินค้า ในแถบรายละเอียดและจำนวนสินค้า ========================= #
            self.product_quantity_widget = QtWidgets.QWidget()
            self.product_quantity_layout = QtWidgets.QHBoxLayout(self.product_quantity_widget)
            self.product_quantity_widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)  # ปรับขนาดให้ fixed
            self.product_quantity_layout.addSpacing(32)  # เพิ่มระยะห่าง 32px ก่อนจะเพิ่ม widget 
            self.product_inner_layout.addWidget(self.product_quantity_widget)  # เพิ่ม product_quantity_widget ลงใน product_inner_layout
            self.product_quantity_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)  # ตั้งค่าชิดขอบบน
            self.product_quantity_layout.setContentsMargins(0, 0, 0, 0)  # ตั้งค่าระยะขอบเป็น 0
            # ปุ่มลดจำนวนสินค้า
            decrease_button = QPushButton("-")
            decrease_button.setFixedSize(40, 30)
            self.product_quantity_layout.addWidget(decrease_button)
            self.product_inner_layout.setStretch(self.product_inner_layout.count() - 1, 0)  # ไม่ยืดสำหรับปุ่มลด
            decrease_button.setStyleSheet("""
            QPushButton {
                color: black;
            }
            """)
            # QLabel แสดงจำนวนสินค้า
            quantity_label = QtWidgets.QLabel("1")  # เริ่มต้นที่จำนวน 1
            quantity_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            quantity_label.setFixedSize(50, 30)
            quantity_label.setStyleSheet("""
            QLabel {
                border: 1px solid red;
                padding: 10px;
                border-radius: 5px;
                border-color: #d3d3d3;
                padding: 0px 8px;
                color: red;
            }
            """)
            self.product_quantity_layout.addWidget(quantity_label)
            self.product_inner_layout.setStretch(self.product_inner_layout.count() - 1, 0)  # ไม่ยืดสำหรับจำนวน
            # ปุ่มเพิ่มจำนวนสินค้า
            increase_button = QPushButton("+")
            increase_button.setFixedSize(40, 30)
            self.product_quantity_layout.addWidget(increase_button)
            self.product_inner_layout.setStretch(self.product_inner_layout.count() - 1, 0)  # ไม่ยืดสำหรับปุ่มเพิ่ม
            # ตั้งค่า layout ของ product_quantity_widget ให้มีการจัดเรียงชิดขอบบน
            self.product_quantity_widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
            self.product_quantity_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
            increase_button.setStyleSheet("""
            QPushButton {
            color: black;
            }
            """)

            # ปุ่มเพิ่มจำนวนสินค้า
            increase_button.clicked.connect(lambda _, lbl=quantity_label: increase_quantity(lbl))
            # ปุ่มลดจำนวนสินค้า
            decrease_button.clicked.connect(lambda _, lbl=quantity_label: decrease_quantity(lbl))
            # ฟังก์ชันเพิ่มจำนวนสินค้า
            def increase_quantity(lbl):
                current_quantity = int(lbl.text())
                lbl.setText(str(current_quantity + 1))
            # ฟังก์ชันลดจำนวนสินค้า
            def decrease_quantity(lbl):
                current_quantity = int(lbl.text())
                if current_quantity > 1:
                    lbl.setText(str(current_quantity - 1))

# ========================= เพิ่มช่องใส่ปุ้มถังขยะ ========================= #
            # เพิ่มปุ่มถังขยะ 
            trash_button = QPushButton()
            trash_button.setFixedSize(30, 30)
            trash_button.setIcon(QtGui.QIcon(r'assets\image\trash_icon.png'))  # ใส่ไอคอนถังขยะ
            trash_button.setIconSize(QtCore.QSize(20, 20))  # กำหนดขนาดไอคอนให้พอดีกับปุ่ม
            trash_button.setStyleSheet("""
            QPushButton {
                padding: 0px;
            }
            """)
            self.product_inner_layout.addWidget(trash_button, alignment=QtCore.Qt.AlignmentFlag.AlignTop)  # เพิ่ม alignment ที่นี่
            self.product_inner_layout.setStretch(self.product_inner_layout.count() - 1, 0)  # ไม่ยืดสำหรับปุ่มถังขยะ
            # เชื่อมต่อปุ่มถังขยะกับฟังก์ชันลบสินค้า
            trash_button.clicked.connect(lambda _, widget=self.product_inner_widget: remove_item(widget))
            # ฟังก์ชันลบสินค้า
            def remove_item(widget):
                widget.setParent(None)  # ลบ widget ของสินค้านั้นๆ ออกจาก layout
                self.cart_count -= 1  # ลดจำนวนสินค้าลง 1
                self.Cart_Title.setText(f'ตะกร้าสินค้า ({self.cart_count})')  # อัปเดตจำนวนสินค้าใน QLabel

# ========================= เพิ่มเส้นแบ่ง ========================= #
        line_separator = QtWidgets.QFrame()
        line_separator.setFrameShape(QtWidgets.QFrame.Shape.HLine)  # ตั้งค่าให้เป็นเส้นแนวนอน
        line_separator.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)  # เงาให้ดูดีขึ้น
        self.product_selected_layout.addWidget(line_separator)  # เพิ่มเส้นแบ่งลงใน layout


# ========================= สร้าง Wrapper Widget สำหรับ Product Summary ========================= #
        self.wrapper_widget = QtWidgets.QWidget()
        self.wrapper_layout = QtWidgets.QVBoxLayout(self.wrapper_widget)
        self.wrapper_layout.setContentsMargins(0, 40, 0, 0)  # กำหนด margins (Left, Top, Right, Bottom)
        self.content_layout.addWidget(self.wrapper_widget, alignment=QtCore.Qt.AlignmentFlag.AlignTop)

# ========================= สร้าง แถบรวมราคาสินค้า ========================= #
        self.product_summary_widget = QtWidgets.QWidget()
        self.product_summary_layout = QtWidgets.QVBoxLayout(self.product_summary_widget)
        self.product_summary_widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)

        self.wrapper_widget.setFixedWidth(400)  # กำหนดความกว้างให้กับ wrapper_widget

        # กำหนดความสูงสูงสุดให้กับ widget
        self.product_summary_widget.setMaximumHeight(400)  # กำหนดความสูงสูงสุด
        self.product_summary_widget.setMinimumHeight(100)  # กำหนดความสูงขั้นต่ำ
        self.product_summary_layout.setContentsMargins(20, 20, 20, 20)  # (Left, Top, Right, Bottom)

        # ตั้งค่ารูปแบบ widget
        self.product_summary_widget.setStyleSheet("""
        QWidget {
            background-color: #F8F8F8;
        }
        """)

        # เพิ่ม product_summary_widget ลงใน wrapper_layout
        self.wrapper_layout.addWidget(self.product_summary_widget)

# ========================= สร้าง แถบกรอกโค้ดส่วนลด ========================= #
        # สร้างแถบกรอกโค้ด และปุ่มใช้งานโค้ด
        self.discount_widget = QtWidgets.QWidget()
        self.discount_layout = QtWidgets.QHBoxLayout(self.discount_widget)
        self.discount_widget.setFixedHeight(65)
        self.discount_layout.setContentsMargins(0, 0, 0, 10)  # กำหนดขอบของ layout # (Left, Top, Right, Bottom)
        self.discount_layout.setSpacing(10)  # ระยะห่างระหว่างช่องกรอกคูปองและปุ่ม
        self.discount_widget.setStyleSheet("""
        QWidget {
            border-bottom: 1px solid #d2d2d2;
            border-radius: 0px;
        }
        """)

        # เพิ่มช่องกรอกโค้ดส่วนลด
        self.discount_code_input = QtWidgets.QLineEdit()
        self.discount_code_input.setFixedSize(260, 45)  # กำหนดความกว้างให้กับช่องกรอกคูปอง
        self.discount_code_input.setPlaceholderText("กรอกคูปองส่วนลด")
        # สร้าง font object
        font = QtGui.QFont()
        font.setPointSize(12)  # ตั้งค่าขนาด font
        # นำ font ที่ตั้งไว้มาใช้กับ QLineEdit
        self.discount_code_input.setFont(font)
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
        self.discount_layout.addWidget(self.discount_code_input)  # เพิ่มช่องกรอกคูปองลงใน layout

        # เพิ่มปุ่มใช้งานโค้ดส่วนลด
        self.apply_discount_button = QtWidgets.QPushButton("ใช้งาน")
        self.apply_discount_button.setFixedSize(80, 45)  # กำหนดขนาดปุ่มที่เหมาะสม
        self.apply_discount_button.setStyleSheet("""QPushButton {
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
        self.discount_layout.addWidget(self.apply_discount_button)  # เพิ่มปุ่มลงใน layout

        # เพิ่ม discount_widget ลงใน layout หลัก
        self.product_summary_layout.addWidget(self.discount_widget, alignment=QtCore.Qt.AlignmentFlag.AlignTop)

# ========================= สร้าง ช่องยอดรวม ========================= #
        # สร้างบล็อก QHBoxLayout สำหรับยอดรวม
        total_amount_layout = QtWidgets.QHBoxLayout()

        # สร้าง QLabel สำหรับคำว่า "ยอดรวม:"
        total_text_label = QtWidgets.QLabel("ยอดรวม")
        total_text_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        # สร้าง QLabel สำหรับจำนวนเงิน "฿52,000"
        total_amount_label = QtWidgets.QLabel("฿52,000")
        total_amount_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)

        # สร้าง font object
        total_amount_layout_font = QtGui.QFont()
        total_amount_layout_font.setPointSize(12)  # ตั้งค่าขนาด font
        # นำ font ที่ตั้งไว้มาใช้
        total_amount_label.setFont(total_amount_layout_font)
        total_text_label.setFont(total_amount_layout_font)

        # เพิ่ม QLabel ทั้งสองลงใน QHBoxLayout
        total_amount_layout.addWidget(total_text_label)
        total_amount_layout.addStretch()  # เพิ่มตัวแบ่งพื้นที่เพื่อดันข้อความยอดรวมไปอีกฝั่ง
        total_amount_layout.addWidget(total_amount_label)

        # เพิ่มระยะห่าง 10 px จากด้านบน
        self.product_summary_layout.addSpacing(5)  # เพิ่มระยะห่าง 10 px

        # เพิ่ม QHBoxLayout ลงใน QVBoxLayout หลัก
        self.product_summary_layout.addLayout(total_amount_layout)

# ========================= สร้าง ช่องส่วนลด ========================= #
        # สร้างบล็อก QHBoxLayout สำหรับส่วนลด
        discount_layout = QtWidgets.QHBoxLayout()

        # สร้าง QLabel สำหรับคำว่า "ส่วนลด:"
        discount_text_label = QtWidgets.QLabel("ส่วนลด")
        discount_text_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        # สร้าง QLabel สำหรับจำนวนเงิน "฿13,000"
        discount_amount_label = QtWidgets.QLabel("฿13,000")
        discount_amount_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)

        # สร้าง font object
        discount_layout_font = QtGui.QFont()
        discount_layout_font.setPointSize(12)  # ตั้งค่าขนาด font
        # นำ font ที่ตั้งไว้มาใช้
        discount_text_label.setFont(discount_layout_font)
        discount_amount_label.setFont(discount_layout_font)

        # เพิ่ม QLabel ทั้งสองลงใน QHBoxLayout
        discount_layout.addWidget(discount_text_label)
        discount_layout.addStretch()  # เพิ่มตัวแบ่งพื้นที่เพื่อดันจำนวนเงินไปอีกฝั่ง
        discount_layout.addWidget(discount_amount_label)

        # เพิ่มระยะห่าง 10 px จากด้านบน
        self.product_summary_layout.addSpacing(5)  # เพิ่มระยะห่าง 10 px

        # เพิ่ม QHBoxLayout ลงใน QVBoxLayout หลัก
        self.product_summary_layout.addLayout(discount_layout)

# ========================= สร้าง ช่องยอดรวมสุทธิ ========================= #
        # สร้างบล็อก QHBoxLayout สำหรับยอดรวมสุทธิ
        net_amount_layout = QtWidgets.QHBoxLayout()

        # สร้าง QLabel สำหรับคำว่า "ยอดรวมสุทธิ:"
        net_amount_text_label = QtWidgets.QLabel("ยอดรวมสุทธิ")
        net_amount_text_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)

        # สร้าง QLabel สำหรับจำนวนเงิน "฿39,000"
        net_amount_value_label = QtWidgets.QLabel("฿39,000")
        net_amount_value_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)

        # สร้าง font object
        net_amount_layout_font = QtGui.QFont()
        net_amount_layout_font.setPointSize(12)  # ตั้งค่าขนาด font
        net_amount_layout_font.setWeight(700)  # ตั้งให้ฟอนต์เป็น Semi Bold
        # นำ font ที่ตั้งไว้มาใช้
        net_amount_text_label.setFont(net_amount_layout_font)
        net_amount_value_label.setFont(net_amount_layout_font)

        # เพิ่ม QLabel ทั้งสองลงใน QHBoxLayout
        net_amount_layout.addWidget(net_amount_text_label)
        net_amount_layout.addStretch()  # เพิ่มตัวแบ่งพื้นที่เพื่อดันจำนวนเงินไปอีกฝั่ง
        net_amount_layout.addWidget(net_amount_value_label)

        # เพิ่มระยะห่าง 10 px จากด้านบน
        self.product_summary_layout.addSpacing(10)  # เพิ่มระยะห่าง 10 px

        # เพิ่ม QHBoxLayout ลงใน QVBoxLayout หลัก
        self.product_summary_layout.addLayout(net_amount_layout)

# ========================= สร้าง ปุ่มซื้อ ========================= #
        # ปุ่มซื้อ
        order_button = QtWidgets.QPushButton("ดำเนินการสั่งซื้อ")
        order_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        order_button.setFixedSize(360, 60)  # กำหนดขนาดปุ่มที่เหมาะสม # กว้าง * สูง
        
        order_button.setStyleSheet("""QPushButton {
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
        # เพิ่มระยะห่าง 10 px จากด้านบน
        self.product_summary_layout.addSpacing(15)  # เพิ่มระยะห่าง 10 px

        self.product_summary_layout.addWidget(order_button)
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









    #================= ฟังค์ชั่นไปหน้า LOGIN ================#
    
    # def go_to_login(self):
    #     self.login_window = LoginWindow()
    #     self.login_window.show()
    #     self.close()
    
    # #================= ฟังค์ชั่นไปหน้า CONTACT ================#
    
    # def go_to_contact(self):
    #     self.contact_window = ContactWindow()
    #     self.contact_window.show()
    
    # #================= ฟังค์ชั่นไปหน้า HOMEPAGE ================#
    
    # def go_to_home(self):
    #     self.home_page = CartWindow()  # สร้างหน้าแรก
    #     self.home_page.show()  # แสดงหน้าแรก
    #     self.home_page.showMaximized()
    #     self.close()



# พวกสีของกล่องข้อความ QMessageBox เบสท์แต่งไว้แล้วนะ
def main():
        app = QtWidgets.QApplication(sys.argv)
        cart_window = CartWindow()
        cart_window.show()
        sys.exit(app.exec())

main()
