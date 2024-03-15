import mysql.connector
from mysql.connector import errorcode
import json
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'sys',
}

conn = mysql.connector.connect(**db_config)

# Create a MySQL cursor
cursor = conn.cursor()


# Create the table if it doesn't exist
# Create the table if it doesn't exist
# cursor.execute('''DROP TABLE ProductData ''')
def create(data):
    # Your MySQL connection parameters
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'sys',
    }

    conn = mysql.connector.connect(**db_config)

    # Create a MySQL cursor
    cursor = conn.cursor()


    # Create the table if it doesn't exist
    # Create the table if it doesn't exist
    # Create the table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS ProductData (
                        ID INTEGER AUTO_INCREMENT PRIMARY KEY,
                        StoreName TEXT,
                        Asin TEXT,
                        Category TEXT,
                        Title TEXT,
                        MRP TEXT,
                        Price TEXT,
                        ShippingPrice TEXT,
                        Manufacturer TEXT,
                        StarRating TEXT,
                        IsPrime TEXT,
                        CustomerReview TEXT,
                        Weight TEXT,
                        Color TEXT,
                        Size TEXT,
                        PackageDimensions TEXT,
                        ItemModelNumber TEXT,
                        Department TEXT,
                        DateFirstAvailable TEXT,
                        BestSellersRank1 TEXT,
                        BestSellersRank2 TEXT,
                        BestSellersRank3 TEXT,
                        BulletPoint1 TEXT,
                        BulletPoint2 TEXT,
                        BulletPoint3 TEXT,
                        BulletPoint4 TEXT,
                        BulletPoint5 TEXT,
                        BulletPoint6 TEXT,
                        BulletPoint7 TEXT,
                        BulletPoint8 TEXT,
                        BulletPoint9 TEXT,
                        BulletPoint10 TEXT,
                        ImageURL1 TEXT,
                        ImageURL2 TEXT,
                        ImageURL3 TEXT,
                        ImageURL4 TEXT,
                        ImageURL5 TEXT,
                        ImageURL6 TEXT,
                        ImageURL7 TEXT,
                        ImageURL8 TEXT,
                        ImageURL9 TEXT,
                        ImageURL10 TEXT,
                        ProductUrl TEXT,
                        VedioLink1 TEXT,
                        VedioLink2 TEXT,
                        VedioLink3 TEXT,
                        VedioLink4 TEXT,
                        DeliveryTime TEXT,
                        Description TEXT
                    )''')

    # Insert data into the table
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s' for _ in range(len(data))])
    insert_query = f"INSERT INTO ProductData ({columns}) VALUES ({placeholders})"
    cursor.execute(insert_query, list(data.values()))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()





data = {

        'StoreName': '',
        'Asin': 'asin_value',
        'Category': '',
        'Title': 'title',
        'MRP': '',
        'Price': '',
        'ShippingPrice': '',
        'Manufacturer': '',
        'StarRating': '',
        'IsPrime': '',
        'CustomerReview': '',
        'Weight': '',
        'Color': '',
        'Size': '',
        'PackageDimensions': '',
        'ItemModelNumber': '',
        'Department': '',
        'DateFirstAvailable': '',
        'BestSellersRank1': '',
        'BestSellersRank2': '',
        'BestSellersRank3': '',
        'BulletPoint1': '',
        'BulletPoint2': '',
        'BulletPoint3': '',
        'BulletPoint4': '',
        'BulletPoint5': '',
        'BulletPoint6': '',
        'BulletPoint7': '',
        'BulletPoint8': '',
        'BulletPoint9': '',
        'BulletPoint10': '',
        'ImageURL1': '',
        'ImageURL2': '',
        'ImageURL3': '',
        'ImageURL4': '',
        'ImageURL5': '',
        'ImageURL6': '',
        'ImageURL7': '',
        'ImageURL8': '',
        'ImageURL9': '',
        'ImageURL10': '',
        'ProductUrl': '',
        'VedioLink1': '',
        'VedioLink2': '',
        'VedioLink3': '',
        'VedioLink4': '',
        'DeliveryTime': '',
        'Description': ''
    }
# print(range(len(data)))
# create(data)