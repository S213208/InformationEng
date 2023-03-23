import mysql.connector

def update_month_names_to_numbers():
    connection = mysql.connector.connect(
        user='root',
        password='Beenandgone1$',
        host='127.0.0.1',
        database='traffic',
        auth_plugin='mysql_native_password'
    )

    cursor = connection.cursor()

    # Define a dictionary to map month names to their numeric values
    month_name_to_number = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }

    # Update the Accident_month values in the table
    for month_name, month_number in month_name_to_number.items():
        update_query = f"UPDATE accident_data SET Accident_month = {month_number} WHERE Accident_month = '{month_name}';"
        cursor.execute(update_query)
        print("DOne")


    connection.commit()
    cursor.close()
    connection.close()

# Call the function to update the month na
update_month_names_to_numbers()