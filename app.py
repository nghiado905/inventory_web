from flask import Flask, render_template, request, redirect, url_for
from models import db, ThuChi, HoaBinh, Deo
from calculate import sum_of_name, count_product, sum_today
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost/my_inventory'
db.init_app(app)


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
    data_type = request.form.get('data_type')

    if data_type == 'thu_chi':
        thu = request.form.get('thu')
        chi = request.form.get('chi')
        reason = request.form.get('reason')

        new_data = ThuChi(thu=thu, chi=chi, reason=reason)
        db.session.add(new_data)
        db.session.commit()

    elif data_type in ['hoa_binh', 'deo']:
        name = request.form.get('name')
        quantity = request.form.get('quantity')

        model = HoaBinh if data_type == 'hoa_binh' else Deo
        new_data = model(name=name, quantity=int(quantity))
        db.session.add(new_data)
        db.session.commit()

    else:
        return "Invalid data type", 400

    return redirect(url_for('index', data_type=data_type))

@app.route('/result', methods=['GET'])
def results_page():
    data_type = request.args.get('data_type', '')
    return render_template('result.html', data_type=data_type)

@app.route('/result_name_hoa_binh', methods=['POST'])
def result_name_hoa_binh():
    result = sum_of_name(HoaBinh.query.all())
    return render_template('result.html', result=result, result_name_hoa_binh=True, data_type='hoa_binh')

@app.route('/result_name_deo', methods=['POST'])
def result_name_deo():
    result = sum_of_name(Deo.query.all())
    return render_template('result.html', result=result, result_name_deo=True, data_type='deo')

@app.route('/result_count_hoa_binh', methods=['POST'])
def result_count_hoa_binh():
    result = count_product(HoaBinh.query.all())
    return render_template('result.html', result=result, result_count_hoa_binh=True, data_type='hoa_binh')

@app.route('/result_count_deo', methods=['POST'])
def result_count_deo():
    result = count_product(Deo.query.all())
    return render_template('result.html', result=result, result_count_deo=True, data_type='deo')

@app.route('/result_today', methods=['POST'])
def result_today():
    result = sum_today(ThuChi.query.all())
    return render_template('result.html', result=result, result_today=True, data_type='thu_chi')

@app.route('/end')
def end():
    return render_template('end.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
