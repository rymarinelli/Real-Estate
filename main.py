from flask import Flask, render_template, request,send_file
from forms import MyForm
from extract import extract_data
from flaskwebgui import FlaskUI
import pandas as pd
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
ui = FlaskUI(app)

#@app.route("/")
#def hello_world():
#    return "<p>Hello, World!</p>"


@app.route("/", methods=['GET', 'POST'])
def login():
    form = MyForm()
    default_value = '0'
    state = request.form.get('state', default_value)
    city = request.form.get('city', default_value)
    zip_code = request.form.get('zip_code', default_value)
    if(city != "" and state != "" and len(state) == 2):
        extract_data(city, state)

        con = sqlite3.connect('Housing.db')
        df = pd.read_sql_query("SELECT * FROM mytable", con)
        con.close()

        def get_download_path():
            """Returns the default downloads path for linux or windows"""
            if os.name == 'nt':
                import winreg
                sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
                downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                    location = winreg.QueryValueEx(key, downloads_guid)[0]
                return location
            else:
                return os.path.join(os.path.expanduser('~'), 'downloads')

        df.to_csv(f"{get_download_path()}\\{city}_{state}_extract_df.csv")

        return send_file(f"{get_download_path()}\\{city}_{state}_extract_df.csv",
                     mimetype='text/csv',
                     attachment_filename="extract_df.csv",
                     as_attachment=True)
    return render_template("login.html",title='Login', form=form)


if __name__ == "__main__":
    ui.run()