# Library imports

import pandas as pd
import os
import pickle
import bz2
import _pickle                   as cPickle
from flask import Flask, request, Response
import json
import sklearn
from Fraud_class.Data_prep import Data_prep



# Loading model
model = cPickle.load(bz2.BZ2File('model/modelXGBoost.pbz2', 'rb'))


# initialize API
app = Flask(__name__)

# criando o endpoint (url que receberá os dados):
@app.route( '/transactiontracker/predict', methods=['POST'] )


# Whenever after receiving a call, the endpoint executes some function. For this case, it will always 
## execute the function after receiving a call, the endpoint executes some function.


def transactiontracker_predict():
    test_json = request.get_json() # the request data will come as json format.
    
   
    if test_json: # there is data
        test_json = json.loads(test_json)
        
        if isinstance( test_json, dict ): #test if the data is a request of only 1 row (will come as dict)
            test_raw = pd.DataFrame( test_json, index=[0] )
            
        else: # otherwise the request will be in the form of a list (with each item being a dictionary):
            test_raw = pd.DataFrame( test_json, columns=test_json[0].keys() )
            
        
        # Instantiate 
        pipeline = Data_prep()
        
        # feature engineering
        df2 = pipeline.feature_engineering( test_raw )
        
        # data preparation
        df3 = pipeline.data_preparation( df2 )
        
        # prediction
        df_response = pipeline.get_predictions( model, test_raw, df3 )
        
        return df_response


    else: # if there is no data
        return Response( '{}', status=200, mimetype='application/json' )
    
    

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run( host='0.0.0.0', port=port, debug=False )
    #      (local host)    
