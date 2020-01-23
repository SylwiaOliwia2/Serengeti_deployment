# app/app.py# Common python package imports.
from flask import Flask, render_template, request
from PIL import Image
from predict import predict_single_image

app = Flask(__name__,  template_folder='templates')

## to call the app type  python app/app.py ANd open the lik displayed afterwards
@app.route('/')
def index():
    html = 'index.html'
    return render_template(html)


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    print("STARTED ANALYZING!!!")
    data = request.files['file']
    img = Image.open(data)
    label = predict_single_image(img)
    print("#---------------------- %s" % label)
    return {"result": str(label)}


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port="5000")
