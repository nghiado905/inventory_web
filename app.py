from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import io
from calculate import *

app = Flask(__name__)

# Authenticate and create the PyDrive client
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
drive = GoogleDrive(gauth)

# Define the data directories
data_directories = {
    'thu_chi': 'thu_chi',
    'hoa_binh': 'hoa_binh',
    'deo': 'deo'
}

# Define file paths
def get_file_path(data_type):
    today = datetime.today().strftime('%d-%m-%Y')
    return f"{data_type.capitalize()}_{today}.xlsx"

# Initialize DataFrames
def initialize_dataframe(file_path, columns):
    file_list = drive.ListFile({'q': f"title='{file_path}' and trashed=false"}).GetList()
    if file_list:
        file_id = file_list[0]['id']
        file = drive.CreateFile({'id': file_id})
        file_content = file.GetContentString()
        return pd.read_excel(io.StringIO(file_content))
    else:
        return pd.DataFrame(columns=columns)

df_thu_chi = initialize_dataframe(get_file_path('thu_chi'), ['Thu', 'Chi', 'Lí do'])
df_hoa_binh = initialize_dataframe(get_file_path('hoa_binh'), ['Tên', 'Số lượng'])
df_deo = initialize_dataframe(get_file_path('deo'), ['Tên', 'Số lượng'])

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/index')
def index():
    data_type = request.args.get('data_type', None)
    return render_template('index.html', data_type=data_type)

@app.route('/submit', methods=['POST'])
def submit():
    global df_thu_chi, df_hoa_binh, df_deo

    data_type = request.form.get('data_type')

    if data_type == 'thu_chi':
        thu = request.form.get('thu')
        chi = request.form.get('chi')
        reason = request.form.get('reason')

        new_data = {'Thu': thu, 'Chi': chi, 'Lí do': reason}
        df_thu_chi = pd.concat([df_thu_chi, pd.DataFrame([new_data])], ignore_index=True)
        file_path = get_file_path('thu_chi')
        
        buffer = io.BytesIO()
        df_thu_chi.to_excel(buffer, index=False)
        buffer.seek(0)
        
        file_list = drive.ListFile({'q': f"title='{file_path}' and trashed=false"}).GetList()
        if file_list:
            file_id = file_list[0]['id']
            file = drive.CreateFile({'id': file_id})
            file.Upload(content=buffer.read())
        else:
            file = drive.CreateFile({'title': file_path})
            file.Upload(content=buffer.read())

    elif data_type in ['hoa_binh', 'deo']:
        name = request.form.get('name')
        quantity = request.form.get('quantity')

        new_data = {'Tên': name, 'Số lượng': int(quantity)}
        df = df_hoa_binh if data_type == 'hoa_binh' else df_deo
        file_path = get_file_path(data_type)
        
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        
        file_list = drive.ListFile({'q': f"title='{file_path}' and trashed=false"}).GetList()
        if file_list:
            file_id = file_list[0]['id']
            file = drive.CreateFile({'id': file_id})
            file.Upload(content=buffer.read())
        else:
            file = drive.CreateFile({'title': file_path})
            file.Upload(content=buffer.read())
        
        if data_type == 'hoa_binh':
            df_hoa_binh = df
        else:
            df_deo = df

    else:
        return "Invalid data type", 400

    return redirect(url_for('index', data_type=data_type))

@app.route('/result', methods=['GET'])
def results_page():
    data_type = request.args.get('data_type', '')
    return render_template('result.html', data_type=data_type)

@app.route('/result_name_hoa_binh', methods=['POST'])
def result_name_hoa_binh():
    result = sum_of_name(df_hoa_binh)
    return render_template('result.html', result=result, result_name_hoa_binh=True, data_type='hoa_binh')

@app.route('/result_name_deo', methods=['POST'])
def result_name_deo():
    result = sum_of_name(df_deo)
    return render_template('result.html', result=result, result_name_deo=True, data_type='deo')

@app.route('/result_count_hoa_binh', methods=['POST'])
def result_count_hoa_binh():
    result = count_product(df_hoa_binh)
    return render_template('result.html', result=result, result_count_hoa_binh=True, data_type='hoa_binh')

@app.route('/result_count_deo', methods=['POST'])
def result_count_deo():
    result = count_product(df_deo)
    return render_template('result.html', result=result, result_count_deo=True, data_type='deo')

@app.route('/result_today', methods=['POST'])
def result_today():
    result = sum_today(df_thu_chi)
    return render_template('result.html', result=result, result_today=True, data_type='thu_chi')

@app.route('/end')
def end():
    return render_template('end.html')

if __name__ == "__main__":
    app.run(debug=True)
