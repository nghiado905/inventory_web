import pandas as pd
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import os
from calculate import *
app = Flask(__name__)

# Khởi tạo DataFrame toàn cục
data = {
    'Ngày': [],
    'Mã hàng': [],
    'Tên hàng': [],
    'Số lượng': [],
    'Giá bán': []
}
df = pd.DataFrame(data)

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    global df
    day = request.form['ngay']
    type = request.form['ma_hang']
    name = request.form['ten_hang']
    num = request.form['so_luong']
    price = request.form['gia_ban']
    
    # num = int(num)  # Chuyển đổi số lượng thành int
    # price = float(price)

    new_data = {
        'Ngày': day,
        'Mã hàng': type,
        'Tên hàng': name,
        'Số lượng': int(num),
        'Giá bán': int(price)
    }

    new_df = pd.DataFrame([new_data])
    df = pd.concat([df, new_df], ignore_index=True)

    today = datetime.today().strftime('%d-%m-%Y')
    data_directory = 'data'
    
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    today = datetime.today().strftime('%d-%m-%Y')
    file_name = os.path.join(data_directory, f"So_{today}.xlsx")  
    df.to_excel(file_name, index=False)
    return redirect(url_for('index'))

@app.route('/results', methods=['GET'])
def results_page():
    return render_template('results.html')

@app.route('/result_type', methods=['POST'])
def result_type():
    result = sum_of_type(df)
    return render_template('results.html', result=result, result_type=True)

@app.route('/result_name', methods=['POST'])
def result_name():
    result = sum_of_name(df)
    return render_template('results.html', result=result, result_name=True)

@app.route('/result_today', methods=['POST'])
def result_today():
    result = sum_today(df)
    return render_template('results.html', result=result, result_today=True)

if __name__ == "__main__":
    app.run(debug=True)
