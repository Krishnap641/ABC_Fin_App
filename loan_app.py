'''
Project: ABC finance loan application processing
Created by: Krishna Prakash
Date created : 17-Oct-2016
Purpose:
This is a sample web based online loan application form
Features:
1. Online submission of loan application
2. Storing the loan application data in SQLite database
3. Optionally, approve the loan application using a machine learning model
'''

from flask import Flask, render_template, request
import sqlite3
import logging


#initialize logging
LOG_FILE_NAME = 'LoanAppLog.txt'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=LOG_FILE_NAME,
                    filemode='w')
#initialize database
def db_connect():
    # establsih the connection
    db_name = 'loan_data.db'
    db_con = sqlite3.connect(db_name)
    logging.info('Connected to '+db_name)
    return db_con

# establsih the connection
conn = db_connect()

# REST API service
app = Flask(__name__)
@app.route('/',methods=['POST', 'GET'])
def home():
    home_page = '<html><h1>ABC BANK HOME PAGE</h1><body><a href="/application.html">Click here to submit loan application form</a></html>'
    return home_page

@app.route('/application.html',methods=['POST', 'GET'])
def loan_application():
    loan_data = []
    loan_status = ""
    if request.method == 'POST':
        try:
            logging.info("Capturing app data " + request.form['name'])
            loan_data.append(request.form['name'])
            loan_data.append(request.form['email'])
            loan_data.append(request.form['age'])
            loan_data.append(request.form['gender'])
            loan_data.append(request.form['married'])
            loan_data.append(request.form['dependents'])
            loan_data.append(request.form['education'])
            loan_data.append(request.form['employment'])
            loan_data.append(request.form['appincome'])
            loan_data.append(request.form['coappincome'])
            loan_data.append(request.form['loan_amount'])
            loan_data.append(request.form['loan_term'])
            loan_data.append(request.form['credit_history'])
            loan_data.append(request.form['area'])

            logging.info(loan_data)
            refno = write_loan_data(loan_data)
            # if you want to use ML model to automatically approve the loan
            #pred_loan_status = loan_app.predict(loan_data)
            #if (pred_loan_status == 1):
            loan_status = 'Your loan application with ID [ ' + str(refno) + ' ] is submitted successfully'
            logging.info(loan_status)
        except:
            loan_status = 'Error!'
            logging.exception(loan_status)
    return render_template('application.html',loan_status = loan_status)

# function to write loan data to db
def write_loan_data(loan_data):

    # establsih the connection
    conn = db_connect()

    # create a cursor
    cur = conn.cursor()
    # execute sql command
    sql = 'insert into loan_application(' \
          'name,' \
          'email,' \
          'age, ' \
          'gender, ' \
          'married, ' \
          'dependents, ' \
          'education,' \
          'employment, ' \
          'appincome, ' \
          'coappincome, ' \
          'loan_amount, ' \
          'loan_term, ' \
          'credit_history, ' \
          'area'  \
          ') values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    # verifying the sql statement for debug
    print(sql)
    cur.execute(sql,[x for x in loan_data])
    cur.execute("commit")
    refno = cur.lastrowid
    print(refno)
    cur.close()
    conn.close()
    logging.info("DB commit successful")
    return refno

if __name__ == '__main__':
    app.run(debug=True)


# unit test database sql
#loan_data = ['Prakash', 'p@gmail.com', '32', '1', '1', '2', '1', '1', '10000', '100000', '1000', '100', '1', '1']
#write_loan_data(loan_data)
