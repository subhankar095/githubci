import mysql.connector
from flask import Flask, request
import os

password = os.environ['MYSQL_ROOT_PASSWORD']
db_connection = mysql.connector.connect(
  host="mysql-service",
  user="root",
  passwd=password,
  database="test"
  )
counter=3
app = Flask(__name__)
@app.route('/', methods=['POST'])
def index():
    global counter
    if request.method == "POST":
        data = request.json
        name = data['name']
        salary = int(data['salary'])
        db_cursor = db_connection.cursor()
        sql="INSERT INTO employee(id,name,salary) VALUES(%s, %s, %s)"
        val=(counter,name,salary)
        db_cursor.execute(sql,val)
        #db_cursor.execute("INSERT INTO employee (%s, '%s', %s)", (counter, name, salary))
        db_connection.commit()
        db_cursor.close()
        counter = counter + 1
        print("testing jenkins")
        return 'success'


if __name__ == '__main__':
    app.run(host='0.0.0.0')

