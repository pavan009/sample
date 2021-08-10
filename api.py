# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
from flask_mail import Mail, Message
import os
import smtplib
import pandas as pd
import re
import json
# creating a Flask app
app = Flask(__name__)
# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/Get_Vendor_Name', methods = ['GET', 'POST'])
def getVendor():
    user_string = request.args.get('Vendor_Name')
    print(user_string)
    data_path = "data.csv"
    df = pd.read_csv(data_path)
    df['VN'] = [re.split(r'(_Low|_High|_Medium)', i)[0].replace("_", " ") for i in df["col1"]]
    result = df[df['VN'].str.lower().str.contains(user_string.lower())] 
    if (result.empty):
        res = {'status': 'no record found'}
        end = json.dumps(res)
        return end
    else:
        num_result = len(result.index)
        print("Bot: we found %s records for you" %num_result)    
        res = {'Vendor Name': [i for i in result['VN']],'status':'records found'}
        end=json.dumps(res)
        return end

@app.route('/Get_Vendor_Details', methods = ['GET', 'POST'])
def pavan():
    Vendor = request.args.get('Actual_Vendor')
    print(Vendor)
    data_path = "data.csv"
    df = pd.read_csv(data_path)
    df['VN']=[re.split(r'(_Low|_High|_Medium)', i)[0].replace("_", " ") for i in df["col1"]]
    res = df[df['VN'] == Vendor]
    res.pop('VN')
    end = res.to_json()
    #end.update({"status": "no record found"})
    return end
# driver function
if __name__ == '__main__':

    app.run(debug = True)