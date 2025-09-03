from PyQt6 import QtWidgets

class BillWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ใบเสร็จ 7-Eleven")
        self.setGeometry(100, 100, 600, 800)

        # สร้าง QTextBrowser
        self.text_browser = QtWidgets.QTextBrowser(self)

        # ข้อมูล HTML และ CSS สำหรับใบเสร็จ
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                @import url("https://fonts.googleapis.com/css2?family=Redressed&family=Ubuntu:wght@400;700&display=swap");

                :root {
                  --bg-clr: #ead376;
                  --white: #fff;
                  --primary-clr: #2f2929;
                  --secondary-clr: #5265a7;
                }

                * {
                  margin: 0;
                  padding: 0;
                  box-sizing: border-box;
                  font-family: "Ubuntu", sans-serif;
                }

                body {
                  background: var(--bg-clr);
                  font-size: 12px;
                  line-height: 20px;
                  color: var(--primary-clr);
                }

                .invoice {
                  width: 100%;
                  height: auto;
                  background: var(--white);
                  padding: 30px;
                  position: relative;
                }

                .w_15 {
                  width: 15%;
                }

                .w_50 {
                  width: 50%;
                }

                .w_55 {
                  width: 55%;
                }

                .p_title {
                  font-weight: 700;
                  font-size: 14px;
                }

                .i_row {
                  display: flex;
                }

                .text_right {
                  text-align: right;
                }

                .header {
                  margin-bottom: 20px;
                }

                .header .i_row {
                  justify-content: space-between;
                }

                .header .i_logo p {
                  font-family: "Redressed", cursive;
                  font-size: 32px;
                  color: var(--secondary-clr);
                }

                .body .i_table .i_col p {
                  font-weight: 700;
                }

                .footer {
                  margin-top: 20px;
                }

                .grand_total {
                  background: var(--secondary-clr);
                  color: var(--white);
                  padding: 10px;
                }
            </style>
        </head>
        <body>
        <section>
          <div class="invoice">
            <div class="header">
              <div class="i_row">
                <div class="i_logo">
                  <p>Coding Market</p>
                </div>
                <div class="i_title">
                  <h2>INVOICE</h2>
                  <p class="p_title text_right">
                    April 20, 2023
                  </p>
                </div>
              </div>
              <div class="i_row">
                <div class="i_number">
                  <p class="p_title">INVOICE NO: 3452324</p>
                </div>
                <div class="i_address text_right">
                  <p>TO</p>
                  <p class="p_title">
                    Facebook <br />
                    <span>Menlo Park, California</span><br />
                    <span>United States</span>
                  </p>
                </div>
              </div>
            </div>
            <div class="body">
              <div class="i_table">
                <div class="i_table_head">
                  <div class="i_row">
                    <div class="i_col w_15">
                      <p class="p_title">QTY</p>
                    </div>
                    <div class="i_col w_55">
                      <p class="p_title">DESCRIPTION</p>
                    </div>
                    <div class="i_col w_15">
                      <p class="p_title">PRICE</p>
                    </div>
                    <div class="i_col w_15">
                      <p class="p_title">TOTAL</p>
                    </div>
                  </div>
                </div>
                <div class="i_table_body">
                  <div class="i_row">
                    <div class="i_col w_15">
                      <p>3</p>
                    </div>
                    <div class="i_col w_55">
                      <p>Lorem, ipsum.</p>
                    </div>
                    <div class="i_col w_15">
                      <p>$10.00</p>
                    </div>
                    <div class="i_col w_15">
                      <p>$30.00</p>
                    </div>
                  </div>
                  <div class="i_row">
                    <div class="i_col w_15">
                      <p>2</p>
                    </div>
                    <div class="i_col w_55">
                      <p>Lorem, ipsum.</p>
                    </div>
                    <div class="i_col w_15">
                      <p>$10.00</p>
                    </div>
                    <div class="i_col w_15">
                      <p>$20.00</p>
                    </div>
                  </div>
                </div>
                <div class="i_table_foot">
                  <div class="i_row grand_total">
                    <p><span>GRAND TOTAL:</span>
                      <span>$165.00</span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
        </body>
        </html>
        """

        # ใส่ข้อมูล HTML ไปใน QTextBrowser
        self.text_browser.setHtml(html_content)

        # layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.text_browser)
        self.setLayout(layout)

# สร้างแอปพลิเคชัน
app = QtWidgets.QApplication([])
window = BillWindow()
window.show()
app.exec()
