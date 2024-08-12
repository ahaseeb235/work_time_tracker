from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    time_in = request.form['time_in']
    time_out = request.form['time_out']
    month = request.form['month']
    date = request.form['date']
    workday_type = request.form['workday_type']

    # Calculate total hours worked
    time_in_dt = datetime.strptime(time_in, '%H:%M')
    time_out_dt = datetime.strptime(time_out, '%H:%M')
    total_hours = (time_out_dt - time_in_dt).seconds / 3600

    # Save data to a file or database (not implemented here)
@app.route('/export')
def export():
    # Fetch data from file or database (not implemented here)
    data = [
        ['Name', 'Time In', 'Time Out', 'Date', 'Workday Type', 'Total Hours'],
        ['John Doe', '09:00', '17:00', '2023-10-01', 'Worked', 8],
        # Add more rows as needed
    ]

    with open('employee_hours.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return redirect(url_for('index'))
    # ...

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
