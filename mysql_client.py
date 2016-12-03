import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='dse203gtd.cvnmpos6almn.us-east-1.rds.amazonaws.com',
                             user='student',
                             password='LEbKqX3q',
                             db='gtd',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
                             
                             
try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "select eventid from gtd limit 10"
        cursor.execute(sql)

        for row in cursor:
            print(row)
finally:
    connection.close()