from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt

app = QApplication([])

# วิดเจ็ตหลักที่มี Layout หลัก
main_widget = QWidget()
main_layout = QVBoxLayout(main_widget)

# สร้าง Container ของ MainContent
main_content_widget = QWidget()
main_content_area = QHBoxLayout(main_content_widget)
main_layout.addWidget(main_content_widget)

# ========================= SIDEBAR MENU ========================= #
# สร้าง SideBar Menu
sidebar_widget = QWidget()
sidebar_area = QVBoxLayout(sidebar_widget)
sidebar_widget.setObjectName('SideBar_Widget')

# เพิ่มเมนูต่างๆ
menu1 = QLabel('first menu')
menu2 = QLabel('second menu')
menu3 = QLabel('third menu')
sidebar_area.addWidget(menu1)
sidebar_area.addWidget(menu2)
sidebar_area.addWidget(menu3)

# ตั้งค่า Style สำหรับ Sidebar
sidebar_widget.setStyleSheet("""
#SideBar_Widget {
    background-color: blue;
    padding: 10px;
}
""")
main_content_area.addWidget(sidebar_widget)

# ========================= ส่วนของคอนเท้นหลักและ scroll เลื่อนหน้า ========================= #
# Scroll เลื่อน
content_area = QScrollArea()
content_area.setWidgetResizable(True)

# Content widget
content_widget = QWidget()
content_layout = QVBoxLayout(content_widget)
content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
content_area.setWidget(content_widget)
content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # ตั้งค่า alignment ของเลย์เอาต์

# เพิ่มหัวข้อและปุ่มแสดง Floating Widget
cart_title = QLabel('ตระกร้าสินค้า')
content_layout.addWidget(cart_title)

button = QPushButton("Show Floating Widget")
content_layout.addWidget(button)

# เพิ่มเนื้อหาเพิ่มเติมเพื่อให้เกิดการเลื่อนใน content_area
for i in range(1, 21):
    label = QLabel(f"เนื้อหาบรรทัดที่ {i}")
    label.setStyleSheet("padding: 10px;")
    content_layout.addWidget(label)

# เพิ่ม ScrollArea เข้าไปใน MainContent Area
main_content_area.addWidget(content_area)

# สร้าง floating_widget ที่ลอยอยู่ด้านบนสุด
floating_widget = QWidget(main_widget)
floating_widget.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
floating_widget.setStyleSheet("background-color: rgba(50, 50, 200, 0.8); padding: 10px; color: white; border-radius: 10px;")
floating_layout = QVBoxLayout(floating_widget)

# เพิ่มป้ายข้อความและปุ่มจ่ายเงินใน floating_widget
floating_label = QLabel("I'm a floating widget")
pay_button = QPushButton("จ่ายเงิน")
pay_button.setStyleSheet("""
    QPushButton {
        background-color: green;
        color: white;
        padding: 5px 15px;
        border-radius: 5px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: darkgreen;
    }
""")
floating_layout.addWidget(floating_label)
floating_layout.addWidget(pay_button)
floating_widget.setFixedSize(150, 100)  # ขนาด floating widget
floating_widget.move(200, 50)  # ตำแหน่งที่ต้องการให้ลอย
floating_widget.hide()  # เริ่มต้นซ่อน floating widget

# ฟังก์ชันแสดง floating widget
def show_floating_widget():
    floating_widget.show()
    floating_widget.raise_()

button.clicked.connect(show_floating_widget)

main_widget.setGeometry(100, 100, 500, 400)  # ขนาดของหน้าต่างหลัก
main_widget.show()
app.exec()
