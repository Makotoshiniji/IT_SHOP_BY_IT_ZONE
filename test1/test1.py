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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IT SHOP")
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
            #sidebar {
                padding: 10px;
            }
            #sidebar::item {
                padding: 10px;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout()

        # Horizontal layout for search and buttons
        search_and_buttons_layout = QHBoxLayout()

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("ค้นหา...")
        self.search_bar.textChanged.connect(self.search_content)

        # Cart and Login buttons
        self.cart_button = QPushButton("รถเข็น")
        self.login_button = QPushButton("เข้าสู่ระบบ")

        # Add search bar and buttons to layout
        search_and_buttons_layout.addWidget(self.search_bar)
        search_and_buttons_layout.addWidget(self.cart_button)
        search_and_buttons_layout.addWidget(self.login_button)

        # Add search and buttons layout to main layout
        main_layout.addLayout(search_and_buttons_layout)

        # Content and menu layout
        content_menu_layout = QHBoxLayout()

        # Sidebar menu
        self.sidebar = QListWidget()
        self.sidebar.addItems(["เมนู 1", "เมนู 2", "เมนู 3", "เมนู 4", "เมนู 5"])
        self.sidebar.setFixedWidth(150)
        self.sidebar.currentItemChanged.connect(self.menu_changed)
        self.sidebar.setObjectName('sidebar')

        # Add sidebar to content layout
        content_menu_layout.addWidget(self.sidebar)

        # Scroll area for content
        self.content_area = QScrollArea()
        self.content_area.setWidgetResizable(True)

        # Content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        
        # ปรับให้ content_layout และ content_widget ใช้ QSizePolicy แบบ Expanding
        self.content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.content_area.setWidget(self.content_widget)

        # Add content area to content layout
        content_menu_layout.addWidget(self.content_area)

        # Add content layout to main layout
        main_layout.addLayout(content_menu_layout)

        # Set main layout to central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def menu_changed(self, current, previous):
        # ลบวิดเจ็ตทั้งหมดใน content_layout ก่อนเพิ่มเนื้อหาใหม่
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            self.content_layout.removeWidget(widget)
            widget.deleteLater()

        # เพิ่มข้อความเมื่อเลือกเมนู
        if current:
            label = QLabel(f"คุณเลือก: {current.text()}")
            self.content_layout.addWidget(label)

            # เพิ่มข้อความ "บรรทัดที่ ..." จำนวน 100 บรรทัด
            for i in range(100):
                self.content_layout.addWidget(QLabel(f"บรรทัดที่ {i + 1}"))
            
            # บังคับให้ content_widget อัปเดตขนาดใหม่ตามเนื้อหาจริง
            self.content_widget.setMinimumHeight(self.content_layout.sizeHint().height())
            self.content_widget.adjustSize()

    def search_content(self, text):
        for i in range(self.content_layout.count()):
            widget = self.content_layout.itemAt(i).widget()
            if isinstance(widget, QLabel):
                widget.setVisible(text.lower() in widget.text().lower())

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
