from flask import Flask, render_template, request
import toml
import sqlite3

settings = toml.load('settings.toml')
flask_settings = settings["flask_settings"]
route_settings = settings["html_routes"]


app = Flask(__name__, static_folder=flask_settings["static_folder"], template_folder=flask_settings["template_folder"])



@app.route('/')
def home():
    html_path = route_settings["/"]

    return render_template(html_path)

@app.route('/menu')
def menu():
    html_path = route_settings["/menu"]

    return render_template(html_path)

@app.route('/order', methods=['GET', 'POST'])
def order():
    # Get the ?id= parameter
    item_id  = request.args.get('id')

    if item_id is None:
        return "Error: No item ID provided."

    # Connect to the database and fetch the item with the given id
    try:
        conn = sqlite3.connect('sqlite/db.sqlite3')
        conn.row_factory = sqlite3.Row  # Make the cursor return a dictionary-like object
        cursor = conn.cursor()

        # Query the menu table for the item with the id
        cursor.execute('SELECT * FROM menu WHERE id=?', (item_id,))
        item = cursor.fetchone()

        if item:
            # Return a formatted response with item details
            return f"You selected item: <br><h2>{item['name']}</h2><br>Description: {item['description']}<br>Price: {item['price']}"
        else:
            return f"Item with ID {item_id} not found."
    except sqlite3.Error as e:
        return f"Database error: {str(e)}"
    finally:
        conn.close()  # Make sure to close the connection

if __name__ == '__main__':
    app.run()
