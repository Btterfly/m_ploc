from flask import Flask, request,make_response,jsonify
import os
from feature import *
from werkzeug.datastructures import ImmutableMultiDict
from flask_cors import CORS
from train import pre_main
import load
app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/getone_feature',methods=["GET"])
def getone():
    form=ImmutableMultiDict(request.args).to_dict()
    print(form)
    res=getone_feature(form['seq'],float(form['w']),int(form['u']))
    response = jsonify({"feature":str(res)})
    return response
@app.route('/pre',methods=["GET"])
def pre():
    form=ImmutableMultiDict(request.args).to_dict()
    print(form)
    uuid=form['uuid']
    x=form['x']
    y=load.getyy()
    res=pre_main(uuid,x,y)
    response = jsonify({"feature":str(res)})
    return response
if __name__ == '__main__':
    app.run(host='127.0.0.1',port=2233)