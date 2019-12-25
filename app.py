from flask import Flask, render_template, request
from wtforms import Form, FloatField, SubmitField, validators, ValidationError
import numpy as np
from sklearn.externals import joblib

# 学習モデルを読み込み予測する
def predict(parameters):
    # モデル読み込み
    model = joblib.load('./nn.pkl')
    params = parameters.reshape(1,-1)
    pred = model.predict(params)
    return pred

# ラベルからTitanicの名前を取得
def getLife(life):
    print(life)
    if life == 0:
        return "生還し"
    elif life == 1: 
        return "死亡し"
    else: 
        return "Error"

app = Flask(__name__)

# Flaskとwtformsを使い、index.html側で表示させるフォームを構築する
class TitanicForm(Form):
    Sex = FloatField("Sex(male = 0, female = 1)（性別）",
                     [validators.InputRequired("この項目は入力必須です"),
                     validators.NumberRange(min=0, max=1)])

    Age  = FloatField("Age(歳)（年齢）",
                     [validators.InputRequired("この項目は入力必須です"),
                     validators.NumberRange(min=0, max=100)])

    SibSp = FloatField("SibSp(人)（兄弟、配偶者の数）",
                     [validators.InputRequired("この項目は入力必須です"),
                     validators.NumberRange(min=0, max=10)])

    Parch  = FloatField("Parch(人)（両親、子供の数）",
                     [validators.InputRequired("この項目は入力必須です"),
                     validators.NumberRange(min=0, max=10)])

    # html側で表示するsubmitボタンの表示
    submit = SubmitField("判定")

@app.route('/', methods = ['GET', 'POST'])
def predicts():
    form = TitanicForm(request.form)
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('index.html', form=form)
        else:            
            Sex = float(request.form["Sex"])            
            Age  = float(request.form["Age"])            
            SibSp = float(request.form["SibSp"])            
            Parch  = float(request.form["Parch"])

            x = np.array([Sex, Age, SibSp, Parch])
            pred = predict(x)
            titanicLife = getLife(pred)

            return render_template('result.html', titanicLife=titanicLife)
    elif request.method == 'GET':

        return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run()