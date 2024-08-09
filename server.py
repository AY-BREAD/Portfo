from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

def write_to_file(data):
    file_exists = os.path.isfile('database.txt')

    with open('database.txt', mode='a') as database:
        if not file_exists:
            # Write header if the file is new
            database.write('Email,Subject,Message\n')
        
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        database.write(f'{email},{subject},{message}\n')

def write_to_csv(data):
    file_exists = os.path.isfile('database.csv')

    with open('database.csv', mode='a', newline='') as database2:
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Write header if the file is new
        if not file_exists:
            csv_writer.writerow(['Email', 'Subject', 'Message'])
        
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer.writerow([email, subject, message])

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
    	try:
         data = request.form.to_dict()
         write_to_csv(data)
         write_to_file(data)
         return redirect('./thankyou.html')
        except:
        	return 'Did not save to Database'
    else:
        return 'Something went wrong. Try again!'

if __name__ == "__main__":
    app.run(debug=True)
