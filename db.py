import mysql.connector

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='db_itshop'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def get_user_id(uname):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_itshop'
    )
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT user_id FROM user_register WHERE uname = %s"
        cursor.execute(query, (uname,))
        result = cursor.fetchone()

        if result:
            return result['user_id']  # คืนค่า user_id
        return None  # กรณีไม่พบข้อมูล
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None
    finally:
        cursor.close()
        connection.close()

def get_data_cart_items(user_id):
    # สร้างการเชื่อมต่อฐานข้อมูล
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_itshop'
    )
    cursor = connection.cursor(dictionary=True)
    query = """SELECT product_code, quantity FROM cart_items WHERE user_id = %s"""
    cursor.execute(query, (user_id,))
    data_cart_items = cursor.fetchall()

    cursor.close()
    connection.close()

    return data_cart_items

def get_product_name(product_code):
    # สร้างการเชื่อมต่อฐานข้อมูล
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_itshop'
    )
    cursor = connection.cursor(dictionary=True)
    query = """SELECT product_name FROM products WHERE product_code = %s"""
    cursor.execute(query, (product_code,))
    result = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    # คืนค่าชื่อสินค้า หากไม่มีข้อมูลคืนค่าเป็น None
    return result['product_name'] if result else None

def get_product_price(product_code):
    # สร้างการเชื่อมต่อฐานข้อมูล
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_itshop'
    )
    cursor = connection.cursor(dictionary=True)
    query = """SELECT price FROM products WHERE product_code = %s"""
    cursor.execute(query, (product_code,))
    result = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    # คืนค่าชื่อสินค้า หากไม่มีข้อมูลคืนค่าเป็น None
    return result['price'] if result else None

# ฟังก์ชันสำหรับอัปเดตจำนวนสินค้าในฐานข้อมูล
def update_quantity_in_database(product_code, new_quantity):
    try:
        # เชื่อมต่อฐานข้อมูล
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='db_itshop'
        )
        cursor = connection.cursor()

        # อัปเดตจำนวนสินค้า
        query = "UPDATE cart_items SET quantity = %s WHERE product_code = %s"
        cursor.execute(query, (new_quantity, product_code))
        connection.commit()
        
        cursor.close()
        connection.close()
        print(f"อัปเดตจำนวนสินค้าในฐานข้อมูลสำเร็จ: {new_quantity}")
    except mysql.connector.Error as e:
        print(f"เกิดข้อผิดพลาดในการอัปเดตฐานข้อมูล: {e}")

# # ฟังก์ชันสำหรับอัปเดตจำนวนสินค้าในฐานข้อมูล
# def lastest_quantity_in_database(product_code):
#     # สร้างการเชื่อมต่อฐานข้อมูล
#     connection = mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='',
#         database='db_itshop'
#     )
#     cursor = connection.cursor(dictionary=True)
#     query = """SELECT quantity FROM cart_items WHERE product_code = %s"""
#     cursor.execute(query, (product_code,))
#     result = cursor.fetchone()
    
#     cursor.close()
#     connection.close()
    
#     return result






def get_headphone_products():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_itshop'
    )
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT product_code, product_name, price FROM products WHERE product_code LIKE 'HP%'
    """
    cursor.execute(query)
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return products

def get_phone_products():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_itshop'
    )
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT product_code, product_name, price FROM products WHERE product_code LIKE 'PH%'
    """
    cursor.execute(query)
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return products


def get_notebook_products():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_itshop'
    )
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT product_code, product_name, price FROM products WHERE product_code LIKE 'NB%'
    """
    cursor.execute(query)
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return products


def get_comset_products():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_itshop'
    )
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT product_code, product_name, price FROM products WHERE product_code LIKE 'CS%'
        """
    cursor.execute(query)
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return products


