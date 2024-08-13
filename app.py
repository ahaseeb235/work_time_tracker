from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Load employee data from JSON
def load_data():
    with open('data/employees.json', 'r') as file:
        return json.load(file)

# Save employee data to JSON
def save_data(data):
    with open('data/employees.json', 'w') as file:
        json.dump(data, file, indent=4)

# Home page route
@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)

# Add hours page route
@app.route('/add', methods=['GET', 'POST'])
def add_hours():
    if request.method == 'POST':
        employee_name = request.form['employee_name']
        time_in = request.form['time_in']
        time_out = request.form['time_out']
        workday_type = request.form['workday_type']
        date = request.form['date']
        month = request.form['month']
        
        # Calculate total hours worked for the day
        time_in_obj = datetime.strptime(time_in, '%H:%M')
        time_out_obj = datetime.strptime(time_out, '%H:%M')
        total_hours = (time_out_obj - time_in_obj).seconds / 3600
        
        # Update employee data
        data = load_data()
        if employee_name not in data:
            data[employee_name] = {}
        if month not in data[employee_name]:
            data[employee_name][month] = {
                'Worked': 0,
                'Training': 0,
                'Bank Holiday': 0,
                'Annual Leave': 0,
                'Sick Leave': 0,
                'Over time': 0
            }
        data[employee_name][month][workday_type] += total_hours
        save_data(data)
        
        return redirect(url_for('index'))
    
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
