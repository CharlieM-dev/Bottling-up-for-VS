import mysql.connector


def log_sale(drink_id, quantity_sold):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='M4a1cqbr!',
        database='fridge_tracker'
    )
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT name FROM Drinks WHERE id = %s', (drink_id,))
        result = cursor.fetchone()
        if not result:
            print(
                f'No drinks found with ID {drink_id}. Check the drinks table!')
            return
        drink_name = result[0]


# we need to check if column drink_name exists in Sales Table
        cursor.execute('SHOW COLUMNS FROM Sales LIKE "drink_name";')
        has_name_column = cursor.fetchone() is not None

        if has_name_column:
            cursor.execute("""
                INSERT INTO Sales (drink_id, drink_name, quantity_sold)
                VALUES (%s, %s, %s)
                """, (drink_id, drink_name, quantity_sold))
        else:
            cursor.execute("""
            INSERT INTO Sales (drink_id, quantity_sold)
            VALUES (%s, %s)""",
                           (drink_id, quantity_sold))

            # get updated stock and threshold

        cursor.execute("""
            UPDATE drinks
            SET stock_current = stock_current - %s
            WHERE id = %s""", (quantity_sold, drink_id))

        cursor.execute("""
            SELECT stock_current, threshold
                           FROM Drinks
                           WHERE id = %s
                           """, (drink_id,))
        stock_current, threshold = cursor.fetchone()

        if stock_current < threshold:
            alert_message = f'Stock low! Only {stock_current} left of {drink_name}.'
            cursor.execute("""
                INSERT INTO Alerts (drink_id, alert_message)
                VALUES (%s, %s)
            """, (drink_id, alert_message))

        conn.commit()

        print(
            f'Sale logged: {quantity_sold}x {drink_name} ID {drink_id}.')
        print(f'Current stock: {stock_current}.')

    except Exception as e:
        conn.rollback()
        print('Error:', e)
    finally:
        cursor.close()
        conn.close()


try:
    drink_id = int(input('Enter the drink ID: '))
    quantity_sold = int(input('Enter the quantity sold: '))
    log_sale(drink_id, quantity_sold)
except ValueError:
    print('Invalid input - please, enter numbers only.')
# the next step is to create
