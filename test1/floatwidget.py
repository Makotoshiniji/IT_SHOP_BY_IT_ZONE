from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QScrollArea
from PyQt6.QtCore import Qt

app = QApplication([])

# วิดเจ็ตหลักที่มี ScrollArea
main_widget = QWidget()
main_layout = QVBoxLayout(main_widget)

# สร้าง ScrollArea และตั้งค่าให้อยู่ใน main_layout
scroll_area = QScrollArea()
scroll_area.setWidgetResizable(True)

# วิดเจ็ตเนื้อหาภายใน ScrollArea
content_widget = QWidget()
content_layout = QVBoxLayout(content_widget)

# เพิ่มข้อความหลายบรรทัดลงใน content_layout เพื่อให้มีเนื้อหามากพอสำหรับการเลื่อน
for i in range(1, 21):
    label = QLabel(f"เนื้อหาบรรทัดที่ {i}")
    label.setStyleSheet("padding: 10px;")
    content_layout.addWidget(label)

# ตั้งค่า content_widget ให้เป็นวิดเจ็ตของ ScrollArea
scroll_area.setWidget(content_widget)
main_layout.addWidget(scroll_area)

# เพิ่มปุ่มแสดง Floating Widget
button = QPushButton("Show Floating Widget")
main_layout.addWidget(button)

# สร้างวิดเจ็ตที่เป็น Floating Widget
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

floating_widget.setFixedSize(300, 500)  # กำหนดขนาดของ floating widget
floating_widget.move(1000, 50)  # ตั้งตำแหน่งที่ต้องการให้ลอย
floating_widget.hide()  # เริ่มต้นโดยซ่อน floating widget ไว้

# ฟังก์ชันแสดง floating widget
def show_floating_widget():
    floating_widget.show()
    floating_widget.raise_()

button.clicked.connect(show_floating_widget)

# กำหนดขนาดของหน้าต่างหลักและแสดงหน้าต่างหลัก
main_widget.setGeometry(100, 100, 400, 300)
main_widget.show()
app.exec()
