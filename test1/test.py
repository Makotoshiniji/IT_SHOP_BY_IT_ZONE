import sys
from PyQt6 import QtWidgets, QtGui, QtCore 
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class CartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('หน้าหลัก')
        self.setStyleSheet('background-color: #ffffff; border-radius: 15px;')
        self.showMaximized()
        self.setWindowIcon(QIcon('image/IT ZONE LOGO.png'))

        # สร้าง container แนวตั้งมาเป็น layout หลัก
        Main_Layout = QVBoxLayout()
        self.setLayout(Main_Layout)
        Main_Layout.setContentsMargins(0, 0, 0, 0)

        # ========================= MENU TOP BAR PART ========================= #

        # สร้าง MenuBar_Widget และเพิ่ม title
        self.MenuBar_Widget = QWidget()
        self.MenuBar_Area = QHBoxLayout(self.MenuBar_Widget)
        self.MenuBar_Widget.setFixedHeight(100)
        self.MenuBar_Widget.setStyleSheet('background-color: #295CA5; border-radius: 0px;')

        # ไอคอนและปุ่มค้นหา
        icon_ITZONE_label = QLabel(self)
        icon_pixmap = QPixmap("assets/image/ITZONEEDIT W.png")
        icon_pixmap = icon_pixmap.scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_ITZONE_label.setPixmap(icon_pixmap)

        IT_ZONE_TOP_TITLE = QWidget()
        IT_ZONE_TOP_TITLE.setLayout(QHBoxLayout())
        IT_ZONE_TOP_TITLE.layout().addWidget(icon_ITZONE_label)
        self.MenuBar_Area.addWidget(IT_ZONE_TOP_TITLE)





        #สร้างแถบในแนวตั้ง QVbox
        search_n_tmenu_widget = QtWidgets.QWidget()
        search_n_tmenu_layout = QVBoxLayout(search_n_tmenu_widget)
        search_n_tmenu_layout.setContentsMargins(0, 0, 0, 0)

        # แถบค้นหา
        search_bar_container = QWidget()
        search_bar_layout = QHBoxLayout(search_bar_container)
        search_bar_layout.setContentsMargins(0, 0, 0, 0)
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("ค้นหาสินค้า...")
        search_bar.setFixedHeight(30)
        search_bar.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
                padding-left: 10px;
                font-size: 14px;
                font-family: 'PK Nakhon Pathom Demo';
            }
            QLineEdit::placeholder { 
                color: gray;
                font-family: 'PK Nakhon Pathom Demo';
            }
        """)
        search_icon = QLabel()
        icon_pixmap = QPixmap("assets/image/magnifying glass icon.png").scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        search_icon.setPixmap(icon_pixmap)
        search_icon.setStyleSheet("""
            background-color: #295CA5;
            border-top-right-radius: 15px;
            border-bottom-right-radius: 15px;
            padding: 5px;
        """)
        search_bar_layout.addWidget(search_bar)
        search_bar_layout.addWidget(search_icon)
        search_n_tmenu_layout.addWidget(search_bar_container)

        # ปุ่มรถเข็นและเข้าสู่ระบบ
        cart_button = QPushButton("   รถเข็นสินค้า")
        cart_button.setIcon(QIcon("assets/image/cart icon.png"))
        cart_button.setIconSize(QSize(30, 30))
        cart_button.setFixedHeight(30)
        cart_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;
            }
        """)
        cart_button.setFont(QFont("PK Nakhon Pathom Demo", 12))
        search_n_tmenu_layout.addWidget(cart_button)

        user_button = QPushButton("   เข้าสู่ระบบ")
        user_button.setIcon(QIcon("assets/image/user icon.png"))
        user_button.setIconSize(QSize(30, 30))
        user_button.setFixedHeight(30)
        user_button.setStyleSheet("""
            QPushButton {
                background-color: #295CA5;
                color: white;
                border-radius: 10px;
                padding: 5px 10px;
                padding-left: 5px;
            }
            QPushButton:hover {
                background-color: #3A7BD5;
            }
        """)
        user_button.setFont(QFont("PK Nakhon Pathom Demo", 12))
        search_n_tmenu_layout.addWidget(user_button)


        #เพิ่มแถบรวมค้นหาและเมนูด้านบน ใส่ใน menu bar
        self.MenuBar_Area.addWidget(search_n_tmenu_layout)






        # เพิ่ม MenuBar_Widget ลงใน Main_Layout
        Main_Layout.addWidget(self.MenuBar_Widget)

        # ========================= HORIZONTAL MENU BAR ========================= #

        # สร้างแถบเมนูด้านล่างแถบค้นหา
        horizontal_menu_container = QWidget()
        horizontal_menu_layout = QHBoxLayout(horizontal_menu_container)
        horizontal_menu_container.setFixedHeight(50)
        horizontal_menu_container.setStyleSheet("background-color: #f0f0f0;")

        # ปุ่มเมนูในแถบแนวนอน
        button1 = QPushButton("เมนู 1")
        button2 = QPushButton("เมนู 2")
        button3 = QPushButton("เมนู 3")
        for button in [button1, button2, button3]:
            button.setStyleSheet("background-color: #295CA5; color: white; padding: 10px; border-radius: 10px;")
            button.setFont(QFont("PK Nakhon Pathom Demo", 12))
            horizontal_menu_layout.addWidget(button)

        # เพิ่มแถบเมนูแนวนอนลงใน Main_Layout
        Main_Layout.addWidget(horizontal_menu_container)


# เรียกใช้งานโปรแกรม
app = QApplication([])
window = CartWindow()
window.show()
app.exec()
