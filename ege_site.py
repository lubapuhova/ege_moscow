from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)
app.debug = True

def get_data():
    url = "http://api.data.mos.ru/v1/datasets/2072/rows"
    r = requests.get(url)
    return r.json()


@app.route('/')
def main_page():
    data = get_data()
    districts = [row['Cells']['District'] for row in data if 'Cells' in row]
    return render_template("main_page.html",
                             districts = districts)

@app.route('/district/<int:n>')
def show_district(n):
    data = get_data()
    districts = [row['Cells']['District'] for row in data if 'Cells' in row]
    new_data = []
    district = ""
    for row in data:
        if row['Cells']['District'] == districts[n]:
            new_data.append(row)
    return render_template("show_district.html",
                            new_data = new_data)



@app.route('/list_schools')
def list_schools():
    data = get_data()
    return render_template("list_schools.html",
                           data=data)



@app.route('/school/<int:n>')
def show_school(n):
    data = get_data()
    row = data[n]
    return render_template("show_school.html",
                        row=row)

@app.route('/json_table/<int:n>')
def json_table (n):
    data = get_data()
    table = data[n]['Cells']
    all = table['PASSED_NUMBER_FULL']
    mi = table['PASSER_UNDER_160']
    ma = table['PASSES_OVER_220']
    another = all - mi - ma
    x = [another, mi, ma]
    y = ['Another', "Less than 160", 'More than 220']
    return jsonify(x=x, y=y)

if __name__ == '__main__':
    app.run()
