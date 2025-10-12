
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='M4a1cqbr!',
    database='fridge_tracker'
)
cursor = conn.cursor()

# now we're going to insert the list
drinks_to_insert = [
    ("Diet Coke", 16, 16, 6),
    ('Coke Zero', 16, 16, 6),
    ('Lemonade', 16, 16, 6),
    ('Sprite 330 ml', 10, 10, 5),
    ('Fanta 330 ml', 10, 10, 5),
    ('Fever Tree Tonic Water', 30, 30, 10),
    ('Fever Tree Slim Line Tonic', 30, 30, 10),
    ('Red Bull', 10, 10, 5),
    ('Red Bull Sugar Free', 10, 10, 5),
]
cursor.executemany("""
INSERT INTO Drinks (name, stock_start, stock_current, threshold)
VALUES (%s, %s, %s, %s)
""", drinks_to_insert)

conn.commit()
print(f"Inserted {cursor.rowcount} drinks successfully!")


def log_sale(drink_id, quantity_sold):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='M4a1cqbr!',
        database='fridge_tracker'
    )


cursor = conn.cursor()

try:
    cursor.execute("""
    INSERT INTO Sales (drink_id, quantity_sold)
    VALUES (%s, %s)
    """, (drink_id, quantity_sold))

    cursor.execute("""
    UPDATE Drinks
    SET stock_current = stock_current - %s
    WHERE id = %s                   
""", (quantity_sold, drink_id))

    cursor.execute("""
SELECT stock_current, threshold
                    FROM Drinks
                    WHERE id = %s
""", (drink_id,))
    stock_current, threshold = cursor.fetchall()

    if stock_current < threshold:
        alert_message = f'Stock low! Only {stock_current} left.'
        cursor.execute("""
INSERT INTO Alert (drink_id, alert_message)
VALUES (%s, %s)                       
""", (drink_id, alert_message))
    conn.commit()
    print(
        f'Sale logged for drink ID {drink_id}. Current stock: {stock_current}')

except Exception as e:
    conn.rollback()
    print('Error is', e)

finally:
    cursor.close()
conn.close()

drink_id = int(input("Enter the drink ID: "))
quantity_sold = int(input("Enter the quantity sold: "))

log_sale(drink_id, quantity_sold=2)
