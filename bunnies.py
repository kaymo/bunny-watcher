# Requires Flask and SQLite3
from flask import Flask, url_for, render_template

# Create the app
app = Flask('sybil')
app.config['DEBUG'] = False

# Index page
@app.route("/") 
def show_capture():
    return render_template('main.html')

# Start the app and make available to all
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
