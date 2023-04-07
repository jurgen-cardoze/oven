from flask import Flask, request, render_template, redirect, url_for
import csv
import random
import os
import time
import threading

app = Flask(__name__)
@app.route('/cashier')
def cashier():
    return render_template('cashier.html')
@app.route('/menu')
def menu():
    return render_template('menu.html')
@app.route("/submit-order", methods=["POST"])
def submit_order():
    if request.method == "POST":
        item_type = request.form.getlist("itemType")
        item_size = request.form.getlist("itemSize")
        quantity = request.form.getlist("quantity")
        total_amount = request.form.getlist("totalAmount")
# Read existing orders from temporary CSV file
    with open("temporary_database.csv", mode="a", newline="") as temp_csv_file:
        fieldnames = ["item_type", "item_size", "quantity", "total_amount"]
        writer = csv.DictWriter(temp_csv_file, fieldnames=fieldnames)
        if temp_csv_file.tell() == 0:
            writer.writeheader()
        for i in range(len(item_type)):
            writer.writerow({
                "item_type": item_type[i],
                "item_size": item_size[i],
                "quantity": quantity[i],
                "total_amount": total_amount[i]
            })

    # Redirect to the customer-info route
    return redirect(url_for("customer_info"))
    



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


@app.route("/customer-info", methods=["GET", "POST"])
def customer_info():
    if request.method == "POST":
        name = request.form["name"]
        phone_number = request.form["phone_number"]

        # Read existing orders from temporary CSV file
        with open("temporary_database.csv", mode="r", newline="") as temp_csv_file:
            temp_reader = csv.DictReader(temp_csv_file)
            temp_rows = list(temp_reader)

        # Add name and phone number to each row
        for row in temp_rows:
            row["name"] = name
            row["phone_number"] = phone_number

        # Generate a unique order ID for all rows
        order_id = random.randint(1, 100)
        for row in temp_rows:
            row["orderID"] = order_id

        # Check if all values in each row are filled
        complete_rows = []
        for row in temp_rows:
            if all(row.values()):
                complete_rows.append(row)

        # Append complete rows to the main_database.csv file
        with open("main_database.csv", mode="a", newline="") as main_csv_file:
            fieldnames = ["pizza_type", "pizza_size", "quantity", "total_amount", "name", "phone_number", "orderID"]
            writer = csv.DictWriter(main_csv_file, fieldnames=fieldnames)
            if main_csv_file.tell() == 0:
                writer.writeheader()
            writer.writerows(complete_rows)

        # Remove complete rows from the temporary_database.csv file
        rows = [row for row in temp_rows if row not in complete_rows]

        # Write the updated data back to the temporary_database.csv file
        with open("temporary_database.csv", mode="w", newline="") as temp_csv_file:
            fieldnames = ["pizza_type", "pizza_size", "quantity", "total_amount", "name", "phone_number", "orderID"]
            writer = csv.DictWriter(temp_csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        return "Thank you for your order!"

    return render_template("customer_info.html")




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
def productsPagePasta():
    return render_template("productsPagePasta.html")

@app.route("/productsPage/Pizza")
def productsPagePizza():
    return render_template("productsPagePizza.html")

@app.route("/productsPage/Desserts")
def productsPage():
    return render_template("productsPageDessert.html")

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
                next(reader, None)  # Skip header row
                order = next(reader, None)

            if switch == "1" and order is None:
                # Get the first complete row from main_database.csv and append all rows with the same orderid to the queue_database.csv file
                with open('main_database.csv', mode='r') as file:
                    reader = csv.reader(file)
                    next(reader, None)  # Skip header row
                    rows = []
                    orderid = None
                    for row in reader:
                        if not all(row) or (orderid is not None and row[-1] != orderid):
                            break
                        rows.append(row)
                        orderid = row[-1]
                    if rows:
                        x = len(rows)  # Get number of rows with same order ID
                        with open('queue_database.csv', mode='a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerows(rows)

                        # Delete the rows with the same order ID from the main_database.csv file
                        with open('main_database.csv', mode='r') as file:
                            reader = csv.reader(file)
                            rows = [row for row in reader if row[-1] != orderid]

                        with open('main_database.csv', mode='w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerows(rows)

            elif switch == "0" and order is not None:
                # Delete the rows with the same order ID from queue_database.csv
                with open('queue_database.csv', mode='r') as file:
                    reader = csv.reader(file)
                    rows = list(reader)
                    orderid = rows[1][-1]  # Get order ID from second row
                    rows_to_keep = [rows[0]] + [row for row in rows[1:] if row[-1] != orderid]
                    with open('queue_database.csv', mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(rows_to_keep)

                order = None
        
        # Wait for 5 seconds before checking again
        time.sleep(5)

if __name__ == '__main__':
    switch = "1"
    import threading
    thread = threading.Thread(target=start_loop)
    thread.start()
    app.run(debug=True)