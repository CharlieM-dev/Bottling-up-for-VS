import mysql.connector


def get_bottle_up_list():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='M4a1cqbr!',
        database='fridge_tracker'
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT drink_name, SUM(quantity_sold)
        FROM Sales
        WHERE DATE(timestamp) = CURDATE()
        GROUP BY drink_name
        ORDER BY drink_name;
        """)

    results = cursor.fetchall()

    if not results:
        print("No sales recorded today. There is nothing in bottling up list.")
    else:
        print("\n=== Bottle-Up List ===")
        for drink_name, total_sold in results:
            print(f"{drink_name}: {total_sold}")
    cursor.close()
    conn.close()


if __name__ == "__main__":
    get_bottle_up_list()
