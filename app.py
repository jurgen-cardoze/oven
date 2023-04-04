from flask import Flask, render_template, url_for, jsonify, request, redirect
import csv
import os
import time
import threading

app = Flask(__name__)


@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        # Get order information from the form
        order_info = request.form['order_info']
        customer_name = ''
        customer_number = ''
        
        # Write the order information to temporary_database.csv file
        with open('temporary_database.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([order_info, customer_name, customer_number])
        
        return redirect('/customer_info')
    
    return render_template('order.html')


@app.route('/customer_info', methods=['GET'])
def show_customer_info():
    return render_template('customer_info.html')


@app.route('/arduino', methods=['POST'])
def arduino():
    global switch
    switch = request.form.get('switch')
    # Do something with the switch variable
    print(switch)
    return 'Switch received'


@app.route('/')
def home():
    return render_template('index.html', image_url=url_for('static', filename='pizza_bros.jpg'))


@app.route('/save_customer_info', methods=['POST'])
def save_customer_info():
    # Get customer information from the form
    customer_name = request.form['customer_name']
    customer_number = request.form['customer_number']
    
    # Read the temporary_database.csv file and update the customer information
    with open('temporary_database.csv', mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        row_count = len(rows)
        
        # Get the last row and update the customer information
        order_info = rows[row_count-1][0]
        rows[row_count-1] = [order_info, customer_name, customer_number]
        
        # Skip rows with empty fields
        complete_rows = []
        for row in rows:
            if all(row):
                complete_rows.append(row)
        
        # Append complete rows to the main_database.csv file
        with open('main_database.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(complete_rows)
                
        # Remove complete rows from the temporary_database.csv file
        rows = [row for row in rows if row not in complete_rows]
        
        # Write the updated data back to the temporary_database.csv file
        with open('temporary_database.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        
        return redirect('/')

@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/basket')
def basket():
    return render_template('basket.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/orderMethod')
def ordermethod():
    return render_template('ordermethod.html', image_url=url_for('static', filename='pizza_bros.jpg'))


@app.route('/deliveryInformation')
def deliveryInformation():
    return render_template('deliveryInformation.html')


@app.route('/orderFinished')
def orderfinished():
    return render_template('orderFinished.html')


@app.route('/ourProgram')
def ourProgram():
    return render_template('ourProgram.html', image_url=url_for('static', filename='pizza_bros.jpg'))

@app.route("/productsPage")
def productsPage():
    return render_template("productsPage.html")

@app.route("/test")
def test():
    return render_template("test.html")

def start_loop():
    last_switch = None
    while True:
        # Check if the value of switch has changed
        if last_switch != switch:
            # Update last_switch to the new value
            last_switch = switch

            # Check if there is a row in the queue_database.csv file
            with open('queue_database.csv', mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                order = next(reader, None)

            if switch == "1" and order is None:
                # Get the first complete row from main_database.csv and append it to the queue_database.csv file
                with open('main_database.csv', mode='r') as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip header row
                    for row in reader:
                        if all(row):
                            order = row
                            break
                
                if order is not None:
                    with open('queue_database.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(order)

                    # Delete the order from the main_database.csv file
                    with open('main_database.csv', mode='r') as file:
                        reader = csv.reader(file)
                        rows = list(reader)
                        rows.remove(order)

                    with open('main_database.csv', mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(rows)

            elif switch == "0" and order is not None:
                # Delete the last row from queue_database.csv
                with open('queue_database.csv', mode='r') as file:
                    rows = list(csv.reader(file))
                    rows.pop()
                
                with open('queue_database.csv', mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
                
                order = None
        
        # Wait for 5 seconds before checking again
        time.sleep(5)

if __name__ == '__main__':
    switch = "1"
    import threading
    thread = threading.Thread(target=start_loop)
    thread.start()
    app.run(debug=True)