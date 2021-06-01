from flask import Flask, render_template, request 
from wtforms import Form, TextAreaField, validators
import __classification_init__
from __classification_init__ import predict_emotion
app = Flask(__name__)

class FindEmotionForm(Form):
    text_ = TextAreaField('', [validators.DataRequired()])
    
@app.route('/')
def index():
    form = FindEmotionForm(request.form)
    return render_template('first_page.html', form=form)
   

@app.route('/result', methods=['POST'])
def find_emotion():
    form = FindEmotionForm(request.form)
    if request.method == 'POST' and form.validate():
        text=request.form['text_']
        output = predict_emotion(text)
        return render_template('result.html', output=output)
    return render_template('first_page.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
    