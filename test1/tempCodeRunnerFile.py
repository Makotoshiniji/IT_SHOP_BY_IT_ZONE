import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QScrollArea,
    QLabel,
    QSizePolicy,
    QLineEdit,
    QPushButton
)

# สร้างคลาสหลัก MainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IT SHOP")  # ตั้งชื่อหน้าต่าง
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
            QListWidget {
                background-color: #2E8B57;
                color: white;
                font-size: 18px;
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #3CB371;
                color: #FFFFFF;
            }
            QLineEdit {
                background-color: #FFFFFF;
                border: 2px solid #2E8B57;
                border-radius: 10px;
                padding: 8px;
                font-size: 16px;
                color: #333333;
            }
            QScrollArea {
                background-color: #FFFFFF;
                border: none;
            }
            QLabel {
                font-size: 16px;
                color: #333333;
            }
            QPushButton {
                background-color: #2E8B57;
                color: white;
                padding: 8px 15px;
                border-radius: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #3CB371;
            }
            #sidebar{
                padding: 10px;
            }
            #sidebar::item {
                padding: 10px;
            }
        """)

        # สร้างเลย์เอาต์หลักแบบแนวนอน
        main_layout = QHBoxLayout()

        # สร้างแถบด้านข้าง
        self.sidebar = QListWidget()
        self.sidebar.addItems(["เมนู 1", "เมนู 2", "เมนู 3", "เมนู 4", "เมนู 5"])
        self.sidebar.setFixedWidth(150)
        self.sidebar.currentItemChanged.connect(self.menu_changed)
        self.sidebar.setObjectName('sidebar')

        # เพิ่มแถบด้านข้างไปยังเลย์เอาต์หลัก
        main_layout.addWidget(self.sidebar)

        # สร้างเลย์เอาต์แนวตั้งสำหรับพื้นที่เนื้อหาด้านขวา
        content_layout = QVBoxLayout()

        # สร้างเลย์เอาต์แนวนอนสำหรับแถบค้นหาและปุ่มต่าง ๆ
        search_and_buttons_layout = QHBoxLayout()

        # สร้างแถบค้นหา
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("ค้นหา...")
        self.search_bar.textChanged.connect(self.search_content)
        
        # สร้างปุ่มรถเข็นและปุ่มเข้าสู่ระบบ
        self.cart_button = QPushButton("รถเข็น")
        self.login_button = QPushButton("เข้าสู่ระบบ")

        # เพิ่มแถบค้นหาและปุ่มไปยังเลย์เอาต์
        search_and_buttons_layout.addWidget(self.search_bar)
        search_and_buttons_layout.addWidget(self.cart_button)
        search_and_buttons_layout.addWidget(self.login_button)

        # เพิ่มเลย์เอาต์แถบค้นหาและปุ่มไปยังเลย์เอาต์เนื้อหา
        content_layout.addLayout(search_and_buttons_layout)

        # สร้างพื้นที่แสดงเนื้อหาพร้อมแถบเลื่อน
        self.content_area = QScrollArea()
        self.content_area.setWidgetResizable(True)

        # สร้างวิดเจ็ตสำหรับเนื้อหา
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.content_area.setWidget(self.content_widget)

        # เพิ่มพื้นที่แสดงเนื้อหาไปยังเลย์เอาต์ของเนื้อหา
        content_layout.addWidget(self.content_area)

        # เพิ่มเลย์เอาต์เนื้อหาไปยังเลย์เอาต์หลัก
        main_layout.addLayout(content_layout)

        # ตั้งค่าเลย์เอาต์หลักในวิดเจ็ตกลาง
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    # ฟังก์ชันที่ทำงานเมื่อเปลี่ยนเมนู
    def menu_changed(self, current, previous):
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            self.content_layout.removeWidget(widget)
            widget.deleteLater()

        if current:
            label = QLabel(f"คุณเลือก: {current.text()}")
            self.content_layout.addWidget(label)

            for i in range(100):
                self.content_layout.addWidget(QLabel(f"บรรทัดที่ {i + 1}"))

    # ฟังก์ชันค้นหาเนื้อหาในพื้นที่แสดงเนื้อหา
    def search_content(self, text):
        for i in range(self.content_layout.count()):
            widget = self.content_layout.itemAt(i).widget()
            if isinstance(widget, QLabel):
                widget.setVisible(text.lower() in widget.text().lower())

# ส่วนของการเรียกใช้งานโปรแกรม
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()  # เปิดหน้าต่างในโหมดเต็มจอ
    sys.exit(app.exec())
