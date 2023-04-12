from flask import Flask, request, render_template, redirect, url_for, jsonify
import csv
import random
import os
import requests
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
    






@app.route('/')
def home():
    return render_template('index.html', image_url=url_for('static', filename='pizza_bros.jpg'))


@app.route("/customer-info-cashier", methods=["GET", "POST"])
def customer_info_cashier():
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

        # Redirect the user to the /cashier route
        return redirect(url_for("cashier")) # for the /customer-info-cashier route


    return render_template("customer_info_cashier.html")

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

        # Redirect the user to the /status route with the order ID as a parameter
        return redirect(url_for("order_status", order_id=order_id))

    return render_template("customer_info.html")



@app.route("/status")
def order_status():
    # Get the order ID from the query parameters
    order_id = request.args.get("order_id")

    # Check how many unique IDs are before our ID in the main database
    with open("main_database.csv", mode="r") as main_csv_file:
        csv_reader = csv.reader(main_csv_file)
        # Skip the header row
        next(csv_reader)
        # Count the number of unique order IDs before our ID
        orders_before = 0
        unique_ids = set()
        order_id_found = False
        for row in csv_reader:
            # Check if the row is empty
            if all(elem == '' for elem in row):
                orders_before = 0
                continue
            if row[-1] != '' and row[-1] not in unique_ids:
                unique_ids.add(row[-1])
                if row[-1] != order_id:
                    orders_before += 1
                else:
                    order_id_found = True
                    orders_before += 1  # Increment the count for current order ID
        
        if not order_id_found:
            orders_before = 0
        else:
            orders_before = int(orders_before) # Convert to integer

    print("order_id:", order_id)
    print("orders_before:", orders_before)

    return render_template("order_status.html", order_id=order_id, orders_before=orders_before)


@app.route("/refresh_status")
def refresh_status():
    # Get the current order ID from the page URL
    order_id = request.args.get("order_id")

    # Check how many unique IDs are before our ID in the main database
    with open("main_database.csv", mode="r") as main_csv_file:
        csv_reader = csv.reader(main_csv_file)
        # Skip the header row
        next(csv_reader)
        # Count the number of unique order IDs before our ID
        orders_before = 0
        unique_ids = set()
        order_id_found = False
        for row in csv_reader:
            # Check if the row is empty
            if all(elem == '' for elem in row):
                orders_before = 0
                continue
            if row[-1] != '' and row[-1] not in unique_ids:
                unique_ids.add(row[-1])
                if row[-1] != order_id:
                    orders_before += 1
                else:
                    order_id_found = True
                    orders_before += 1  # Increment the count for current order ID
        
        if not order_id_found:
            orders_before = 0
        else:
            orders_before = int(orders_before) # Convert to integer

    # Get the switch value...Skipped 1 messages
    switch_value = switch
    return jsonify({"orders_before": orders_before, "switch": switch_value})



@app.route('/arduino', methods=['POST'])
def arduino():
    global switch
    switch = request.form.get('switch')
    # Do something with the switch variable
    print(switch)
    return 'Switch received'

@app.route('/data')
def get_data():
    queue_data = []
    with open('queue_database.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            queue_data.append(row)

    main_data = []
    with open('main_database.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            main_data.append(row)

    return jsonify({
        'queue_data': queue_data,
        'main_data': main_data
    })
@app.route('/cook', methods=['GET', 'POST'])
def cook():
    queue_data = []
    with open('queue_database.csv', 'r') as queue_file:
        for line in queue_file:
            queue_data.append(line.strip().split(','))

    main_data = []
    with open('main_database.csv', 'r') as main_file:
        for line in main_file:
            main_data.append(line.strip().split(','))
    global switch
    if request.method == 'POST':
        switch = '0' if switch == '1' else '1'
    switch_text = 'Off' if switch == '0' else 'On'
    return render_template('cook.html', switch=switch, switch_text=switch_text,queue_data=queue_data, main_data=main_data)




    


@app.route('/basket')
def basket():
    return render_template('basket.html')

@app.route('/login')
def renderLogin():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'mario' and password == 'mario':
            return redirect('/cashier')
        elif username == 'luigi' and password == 'luigi':
            return redirect('/cook')
        else:
            return "Invalid login"
    else:
        return '''
            <form action="/login" method="post">
                <p><input type=text name=username>
                <p><input type=password name=password>
                <p><input type=submit value=Login>
            </form>
        '''


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

@app.route("/coming_soon")
def coming_soon():
    return render_template("comig_soon.html")
@app.route("/subscribe", methods=["POST"])
def subscribe():
    email = request.form["email"]
    with open("emails.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([email])
    return render_template("thank_you.html")


def start_loop():
    last_switch = None
    while True:
        switch_value = switch
        # Check if the value of switch has changed
        if last_switch != switch_value:
            # Update last_switch to the new value
            last_switch = switch_value

            # Check if there is a row in the queue_database.csv file
            with open('queue_database.csv', mode='r') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header row
                order = next(reader, None)

            if switch_value == "1" and order is None:
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

            elif switch_value == "0" and order is not None:
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