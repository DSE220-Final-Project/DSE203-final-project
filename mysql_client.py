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
    
# Sample output
# {u'eventid': 201201010001}
# {u'eventid': 201201010002}
# {u'eventid': 201201010003}
# {u'eventid': 201201010004}
# {u'eventid': 201201010005}
# {u'eventid': 201201010006}
# {u'eventid': 201201010007}
# {u'eventid': 201201010008}
# {u'eventid': 201201010009}
# {u'eventid': 201201010012}