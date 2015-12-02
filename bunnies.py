# Dependencies: Flask
from flask import Flask, url_for, render_template
import os

# Create the app
app = Flask('sybil')
app.config['DEBUG'] = False

# Index page
@app.route("/") 
def show_capture():
    
    # Get a list of the captures that doesn't include the current captures
    files = sorted( os.listdir('static/captures/'), reverse=True )
    files = files[4:]

    return render_template('main.html', files=files)

# Start the app and make available to all
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
