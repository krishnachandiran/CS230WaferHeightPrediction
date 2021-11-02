# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 15:35:13 2021

@author: krishnachandiran.r
"""
from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import ws_generator_default
import os
from logging.config import dictConfig
import logging
import json


#os.environ["FLASK_ENV"] = "development"

app = Flask(__name__)
api = Api(app)

@app.route("/")
def hello():
    message = ""
    return render_template('index.html', message=message)

class DataGenerator(Resource):
    def post(self):
        request_data = request.get_json()

        die = request_data['die']
        streetWidth = request_data['street_width']
        swath = request_data['swath']
        userId = request_data['user_id']
        careAreas = request_data['care_areas']
        exclusionZones = request_data['exclusion_zones']
        impuritiesPerDie = request_data['impurities_per_die']
        pattern = request_data['pattern']
        patternAttr = request_data['pattern_attr']
        impurityLuminance = request_data['impurity_luminance']
        
        del request_data['swath'] 
        del request_data['user_id']
        del request_data['pattern'] 
        del request_data['pattern_attr']
        del request_data['impurity_luminance'] 
        del request_data['impurities_per_die']
        
            
        if not os.path.exists(userId):
            os.makedirs(userId)
        dirname = os.path.dirname(__file__)
        datafolder = os.path.join(dirname, userId + '/data')
        if not os.path.exists(datafolder):    
            os.mkdir(datafolder) 
        datafolder = os.path.join(dirname, userId + '/internal')
        if not os.path.exists(datafolder):    
            os.mkdir(datafolder) 
            
        with open(userId + "/data/" +'input.json', 'w') as fp:
            json.dump(request_data, fp)
            
            
        (waferWidth , waferHeight) = ws_generator_default.generate_wafer_image(die['width'], die['height'], die['rows'], die['columns'], streetWidth, userId , swath['width'], swath['height'], pattern , patternAttr, impuritiesPerDie,impurityLuminance, careAreas, exclusionZones)
        

        
      #  print(language, framework, python_version, example, boolean_test)
       # data = pd.read_csv('users.csv')  # read CSV
       # data = data.to_dict()  # convert dataframe to dictionary
        return {
            'wafer_width': waferWidth,
            'wafer_height' : waferHeight
                }, 200  # return data and 200 OK code
    
    
api.add_resource(DataGenerator, '/data/generate')


if __name__ == '__main__':
    app.run(host='0.0.0.0')  # run our Flask app