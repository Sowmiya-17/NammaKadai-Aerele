from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
app=Flask(__name__)

VALID_USERNAME='sowmi'
VALID_PASSWORD='123'

@app.route('/')
def home():
    return render_template('nm.html')

@app.route('/process_form',methods=['POST'])
def process_form():
    username=request.form.get('username')
    pwd=request.form.get('password')
    if username==VALID_USERNAME and pwd==VALID_PASSWORD:
        return redirect(url_for('sales_purchases_form'))

@app.route('/sales_purchases_form')
def sales_purchases_form():
    return render_template('sales_purchases.html')

@app.route('/choose_form', methods=['POST'])
def choose_form():
    submit_but=request.form.get('submit_button')
    if submit_but == 'sale':
        return render_template('sales_view.html')
    elif submit_but == 'purchase':
        return render_template('purchase_view.html')
    elif submit_but == 'checkbalance':
        return render_template('checkbal.html')
    
@app.route('/chooseupdate_form',methods=['POST'])
def chooseupdate_form():
    submit_but=request.form.get('submit_button2')
    if submit_but == 'updateuser':
        return render_template('updateuser.html')
    elif submit_but == 'setbalance':
        return render_template('setbalance.html')
    elif submit_but == 'checkstock':
        return render_template('checkstock.html')
    
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='1234'
app.config['MYSQL_DB']='aerele'

mysql = MySQL(app)

@app.route('/salessubmit',methods=['GET','POST'])
def salessubmit():
    if request.method=='POST':
       itemname=request.form.get('itemname')
       item_id=request.form.get('item_id')
       price=request.form.get('price')
       quantity=request.form.get('quantity')
       amount=float(request.form.get('amount'))

       cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       
       cursor.execute('SELECT item_id FROM Item where item_id=%s',(item_id,))
       result=cursor.fetchone()
       if result:
           cursor.execute('INSERT INTO sales(item_id,quantity,rate,amount,item_name) VALUES (%s,%s,%s,%s,%s)',(item_id,quantity,price,amount,itemname))
           mysql.connection.commit()
           cursor.execute("""UPDATE Item SET Item.quantity=Item.quantity-(%s) where Item.item_id=%s""",(quantity,item_id,))
           mysql.connection.commit()
           return "Done"
       else:
           cursor.execute('INSERT INTO Item(item_id,item_name,quantity) VALUES(%s,%s,%s)',(item_id,itemname,quantity))
           mysql.connection.commit()
           cursor.execute('INSERT INTO sales(item_id,quantity,rate,amount,item_name) VALUES (%s,%s,%s,%s,%s)',(item_id,quantity,price,amount,itemname))
           mysql.connection.commit()
           return "Done"
    cursor.execute("UPDATE company SET cash_balance=cash_balance+%s where com_name='Namma Kadai'",(amount))
    mysql.connection.commit()
    mysql.connection.close()
    return "updated"

@app.route('/purchasesubmit',methods=['GET','POST'])
def purchasesubmit():
    if request.method=='POST':
       itemname=request.form.get('itemname')
       item_id=request.form.get('item_id')
       price=request.form.get('price')
       quantity=request.form.get('quantity')
       amount=float(request.form.get('amount'))

       cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       
       cursor.execute('SELECT item_id FROM Item where item_id=%s',(item_id,))
       result=cursor.fetchone()
       if result:
           cursor.execute('INSERT INTO purchase(item_id,quantity,rate,amount,item_name) VALUES (%s,%s,%s,%s,%s)',(item_id,quantity,price,amount,itemname))
           mysql.connection.commit()
           cursor.execute("""UPDATE Item SET Item.quantity=Item.quantity+(%s) where Item.item_id=%s""",(quantity,item_id,))
           mysql.connection.commit()
           return "Done"
       else:
           cursor.execute('INSERT INTO Item(item_id,item_name,quantity) VALUES(%s,%s,%s)',(item_id,itemname,quantity))
           mysql.connection.commit()
           cursor.execute('INSERT INTO purchase(item_id,quantity,rate,amount,item_name) VALUES (%s,%s,%s,%s,%s)',(item_id,quantity,price,amount,itemname))
           mysql.connection.commit()
           return "Done"
    update_query="UPDATE company SET cash_balance=cash_balance-%s where com_name='Namma Kadai'"
    cursor.execute(update_query,(amount))
    mysql.connection.commit()
    mysql.connection.close()
    return "updated"

@app.route('/checkstock',methods=['GET','POST'])  
def checkstock():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM Item"
        cursor.execute(query)
        data = cursor.fetchall()
        #print(data)
        return render_template('checkstock.html',data=data)

@app.route('/checkbal')  
def checkbal():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM company"
        cursor.execute(query)
        data = cursor.fetchall()
        #print(data)
        return render_template('checkbal.html',data=data)
    
    
if('__name__'=='__main__'):
    app.run(debug=True)