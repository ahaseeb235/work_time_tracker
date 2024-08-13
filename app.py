from flask import Flask, render_template, request, redirect, url_for, send_file
import csv
import os
from datetime import datetime

app = Flask(__name__)

# File path for storing data
CSV_FILE_PATH = 'data/working_hours.csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Read data from CSV
    data = []
    with open(CSV_FILE_PATH, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)

    # Calculate totals for the dashboard
    total_hours = sum(float(row['Hours Worked']) for row in data)
    total_bank_holiday = sum(float(row['Hours Worked']) for row in data if row['Workday Type'] == 'Bank Holiday')
    total_sick_leave = sum(float(row['Hours Worked']) for row in data if row['Workday Type'] == 'Sick Leave')
    total_annual_leave = sum(float(row['Hours Worked']) for row in data if row['Workday Type'] == 'Annual Leave')
    total_training = sum(float(row['Hours Worked']) for row in data if row['Workday Type'] == 'Training')
    total_overtime = sum(float(row['Hours Worked']) for row in data if row['Workday Type'] == 'Over time')

    return render_template('dashboard.html', total_hours=total_hours, total_bank_holiday=total_bank_holiday,
                           total_sick_leave=total_sick_leave, total_annual_leave=total_annual_leave,
                           total_training=total_training, total_overtime=total_overtime, data=data)

@app.route('/submit', methods=['POST'])
def submit():
    # Capture form data
    # Correctly get the value from the form
    employee_name = request.form['employee_name']  # Use get() to safely retrieve the value
    if not employee_name:
        return "Employee name is missing", 400
    
    time_in = request.form['time_in']
    time_out = request.form['time_out']
    date = request.form['date']
    workday_type = request.form['workday_type']

    # Calculate hours worked
    time_in_dt = datetime.strptime(time_in, '%H:%M')
    time_out_dt = datetime.strptime(time_out, '%H:%M')
    hours_worked = (time_out_dt - time_in_dt).seconds / 3600

    # Write to CSV
    with open(CSV_FILE_PATH, 'a', newline='') as csvfile:
        fieldnames = ['Date', 'Employee Name', 'Time In', 'Time Out', 'Hours Worked', 'Workday Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header if file is new
        if os.stat(CSV_FILE_PATH).st_size == 0:
            writer.writeheader()

        writer.writerow({'Date': date, 'Employee Name': employee_name, 'Time In': time_in, 'Time Out': time_out,
                         'Hours Worked': hours_worked, 'Workday Type': workday_type})

    return redirect(url_for('index'))

@app.route('/export')
def export():
    return send_file(CSV_FILE_PATH, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
