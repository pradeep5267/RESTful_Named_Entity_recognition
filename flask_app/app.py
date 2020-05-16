from flask import Flask, render_template, render_template_string, \
    jsonify, request
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/test_link')
def test_link():
    return render_template('test.html')

@app.route('/check_data', methods = ['GET','POST'])
def check_data():
    if (request.method == 'POST'):
        input_data = request.form.get('input_text')
        # print(data)
        output_data = get_answers(input_data)
        if (output_data == 'GPE'):
            output_data = str('City/Country')
        if(output_data == None):
            output_data = str('not found')
        if (output_data == 'PERSON'):
            output_data = str('Person')
        return render_template('check_data.html', value= output_data)
        # return render_template('check_data.html')
    if (request.method == 'GET'):
        return render_template('check_data.html')

def get_answers(input_data):
    with open('./flask_app/data_entity_list_full.json','r') as json_file:
        json_data = json.load(json_file)
        for i in range(len(json_data)):
            if (str(input_data).lower() in json_data[i]['data'].lower()):
                print(json_data[i]['entity'])
                return json_data[i]['entity']

    
if __name__ == "__main__":
    app.run(debug=True)
