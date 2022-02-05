import pickle
import bz2
import _pickle as cPickle
from math                        import ceil
from math                        import floor
import pandas as pd
import numpy as np
import json



class Data_prep(object):
    
    def __init__(self):        
        self.amount_scaler          =  pickle.load(open('encoders/amount_scaler.pkl', 'rb')) # Opening scaler        
        self.day_of_month_scaler    =  pickle.load(open('encoders/day_of_month_scaler.pkl', 'rb')) # Opening scaler        
        self.newbalanceDest_scaler  =  pickle.load(open('encoders/newbalanceDest_scaler.pkl', 'rb')) # Opening scaler        
                
        self.newbalanceOrig_scaler  =  pickle.load(open('encoders/newbalanceOrig_scaler.pkl', 'rb')) # Opening scaler        
        self.oldbalanceDest_scaler  =  pickle.load(open('encoders/oldbalanceDest_scaler.pkl', 'rb')) # Opening scaler        
        self.oldbalanceOrg_scaler   =  pickle.load(open('encoders/oldbalanceOrg_scaler.pkl', 'rb')) # Opening scaler        
        self.step_scaler            =  pickle.load(open('encoders/step_scaler.pkl', 'rb')) # Opening scaler        
        self.type_encoder           =  pickle.load(open('encoders/type_encoder.pkl', 'rb')) # Opening encoder        
        self.week_of_month_scaler   =  pickle.load(open('encoders/week_of_month_scaler.pkl', 'rb')) # Opening scaler
        
        
    
    
    
    def feature_engineering(self, df1):
                
        # Day of month

        df1['day_of_month'] = df1['step'].apply(lambda x: ceil(x/24))
        
        # Week of month

        df1['week_of_month'] = df1['step'].apply(lambda x: ceil(x/168))
        
        # Creating aux column 'min_step_of_day'

        for i in df1['day_of_month'].unique():
            df1.loc[df1['day_of_month']==i,'min_step_of_day'] = df1.loc[df1['day_of_month']==i, 'step'].min()
        
        
        # Creating 'hour_of_day' column

        df1['hour_of_day'] = df1['step'] - df1['min_step_of_day']
        
        
        # Creating aux column 'min_day_of_week'

        for i in df1['week_of_month'].unique():
            df1.loc[df1['week_of_month']==i, 'min_day_of_week'] = df1.loc[df1['week_of_month']==i, 'day_of_month'].min()


        # Creating 'day_of_week' column
        
        df1['day_of_week'] = ((df1['day_of_month'] - df1['min_day_of_week'])+1)
        
        
        # Creating 'is_weekend' column

        df1['is_weekend'] = df1['day_of_week'].apply(lambda x: 'weekend' if x == 1 or x == 7 else 'weekdays')
        
        
        # Creating 'time_of_day' column

        df1['time_of_day'] = df1['hour_of_day'].apply(lambda x: 'AM' if x <= 12 else 'PM')
        
        
        # Creating 'period_of_day' column

        df1['period_of_day'] = ['Morning' if i<=12 else 'Afternoon' if i>12 and i<=18 else 'Evening' for i in df1['hour_of_day']]
        
        
        # Creating 'orig_type' column

        df1['orig_type'] = ['Merchant' if i[0]== 'M' else 'Costumer' for i in df1['nameOrig']]
        
        
        # Creating 'dest_type' column

        df1['dest_type'] = ['Merchant' if i[0]== 'M' else 'Costumer' for i in df1['nameDest']]
        
        
        # Creating 'oldbalanceOrg_status'

        df1['oldbalanceOrg_status'] = ['zero' if i==0 else 'non-zero' for i in df1['oldbalanceOrg']]
        
        
        # Creating 'newbalanceOrig_status'

        df1['newbalanceOrig_status'] = ['zero' if i==0 else 'non-zero' for i in df1['newbalanceOrig']]
        
        
        # Creating 'oldbalanceDest_status'

        df1['oldbalanceDest_status'] = ['zero' if i==0 else 'non-zero' for i in df1['oldbalanceDest']]
        
        
        # Creating 'newbalanceDest_status'

        df1['newbalanceDest_status'] = ['zero' if i==0 else 'non-zero' for i in df1['newbalanceDest']]
        
        
        # Creating the column 'is_orig_equal_dest'

        df1['is_orig_equal_dest'] = ['yes' if i==it else 'no' for i, it in zip(df1['nameOrig'], df1['nameDest'])]
        
        
        # Creating the column 'is_oldbalanceOrg_higherthan_newbalanceOrig'

        df1['is_oldbalanceOrg_higherthan_newbalanceOrig'] = ['yes'if i>it else 'no' for i, it in zip(df1['oldbalanceOrg'], df1['newbalanceOrig'])]
        
        
        # Creating the column 'is_oldbalanceDest_higherthan_newbalanceDest'

        df1['is_oldbalanceDest_higherthan_newbalanceDest'] = ['yes'if i>it else 'no' for i, it in zip(df1['oldbalanceDest'], df1['newbalanceDest'])]
        
        
        # Creating the column 'transaction_direction'

        df1['transaction_direction'] = [i[0]+'2'+it[0] for i, it in zip(df1['orig_type'], df1['dest_type'])]
        
        
        # Converting 'isFlaggedFraud' column to categorical (to further corr calculation)

        df1['isFlaggedFraud'] = ['no' if i==0 else 'yes' for i in df1['isFlaggedFraud']]
        
        
        # Droping aux column 'min_step_of_day'

        df1 = df1.drop(columns=['min_step_of_day', 'min_day_of_week'])
        
        
        # Converting 'hour_of_day' and 'day_of_week' columns to int

        df1[['hour_of_day','day_of_week']] = df1[['hour_of_day','day_of_week']].astype(int)
        
        
        
        
        #========================================================
        # Data filtering
        #========================================================
        
        df1 = df1.drop(columns=['orig_type','is_orig_equal_dest'])
        
        df1 = df1.drop(columns=['nameOrig'])
        
        return df1
        
        
    def data_preparation(self, df2):
        
        X_train = df2
        
        
        # Scaling: Numeric attributes
        
        
        # Numeric non-cyclic attributes - Robust Scaler (each of them has extreme values)
        
        # 'amount'
        
        X_train['amount'] = self.amount_scaler.transform(X_train[['amount']].values)
        
        # 'oldbalanceOrg'
        
        X_train['oldbalanceOrg'] = self.oldbalanceOrg_scaler.transform(X_train[['oldbalanceOrg']].values)
        
        # 'newbalanceOrig'
        
        X_train['newbalanceOrig'] = self.newbalanceOrig_scaler.transform(X_train[['newbalanceOrig']].values)
        
        # 'oldbalanceDest'
        
        X_train['oldbalanceDest'] = self.oldbalanceDest_scaler.transform(X_train[['oldbalanceDest']].values)
        
        # 'newbalanceDest'
        
        X_train['newbalanceDest'] = self.newbalanceDest_scaler.transform(X_train[['newbalanceDest']].values)
        
        # 'day_of_month'
        
        X_train['day_of_month'] = self.day_of_month_scaler.transform(X_train[['day_of_month']].values)
        
        # 'week_of_month'
        
        X_train['week_of_month'] = self.week_of_month_scaler.transform(X_train[['week_of_month']].values)
        
        # 'step'
        
        X_train['step'] = self.step_scaler.transform(X_train[['step']].values)
        
        
        
        # Encoding: Categorical attributes
        
        
        # Dummies
        
        # Features to encode via Dummies:
        
        # 'isFlaggedFraud',
        # 'is_weekend',
        # 'time_of_day',
        # 'dest_type',
        # 'oldbalanceOrg_status',
        # 'newbalanceOrig_status',
        # 'oldbalanceDest_status',
        # 'newbalanceDest_status',
        # 'is_oldbalanceOrg_higherthan_newbalanceOrig',
        # 'is_oldbalanceDest_higherthan_newbalanceDest',
        # 'transaction_direction'
        
        
        # Getting Dummie variables 
        
                
        X_train['isFlaggedFraud_no'] = [1 if i=='no' else 0 for i in X_train['isFlaggedFraud']]
        
        X_train['isFlaggedFraud_yes'] = [1 if i=='yes' else 0 for i in X_train['isFlaggedFraud']]
        
        X_train['is_weekend_weekdays'] = [1 if i=='weekdays' else 0 for i in X_train['is_weekend']]
        
        X_train['is_weekend_weekend'] = [1 if i=='weekend' else 0 for i in X_train['is_weekend']]
        
        X_train['time_of_day_AM'] = [1 if i=='AM' else 0 for i in X_train['time_of_day']]
        
        X_train['time_of_day_PM'] = [1 if i=='PM' else 0 for i in X_train['time_of_day']]
        
        X_train['dest_type_Costumer'] = [1 if i=='Costumer' else 0 for i in X_train['dest_type']]
        
        X_train['dest_type_Merchant'] = [1 if i=='Merchant' else 0 for i in X_train['dest_type']]
        
        X_train['oldbalanceOrg_status_non-zero'] = [1 if i=='non-zero' else 0 for i in X_train['oldbalanceOrg_status']]
        
        X_train['oldbalanceOrg_status_zero'] = [1 if i=='zero' else 0 for i in X_train['oldbalanceOrg_status']]
        
        X_train['newbalanceOrig_status_non-zero'] = [1 if i=='non-zero' else 0 for i in X_train['newbalanceOrig_status']]
        
        X_train['newbalanceOrig_status_zero'] = [1 if i=='zero' else 0 for i in X_train['newbalanceOrig_status']]
        
        X_train['oldbalanceDest_status_non-zero'] = [1 if i=='non-zero' else 0 for i in X_train['oldbalanceDest_status']]
        
        X_train['oldbalanceDest_status_zero'] = [1 if i=='zero' else 0 for i in X_train['oldbalanceDest_status']]
        
        X_train['newbalanceDest_status_non-zero'] = [1 if i=='non-zero' else 0 for i in X_train['newbalanceDest_status']]
        
        X_train['newbalanceDest_status_zero'] = [1 if i=='zero' else 0 for i in X_train['newbalanceDest_status']]
        
        X_train['is_oldbalanceOrg_higherthan_newbalanceOrig_no'] = [1 if i=='no' else 0 for i in X_train['is_oldbalanceOrg_higherthan_newbalanceOrig']]
        
        X_train['is_oldbalanceOrg_higherthan_newbalanceOrig_yes'] = [1 if i=='yes' else 0 for i in X_train['is_oldbalanceOrg_higherthan_newbalanceOrig']]
        
        X_train['is_oldbalanceDest_higherthan_newbalanceDest_no'] = [1 if i=='no' else 0 for i in X_train['is_oldbalanceDest_higherthan_newbalanceDest']]
        
        X_train['is_oldbalanceDest_higherthan_newbalanceDest_yes'] = [1 if i=='yes' else 0 for i in X_train['is_oldbalanceDest_higherthan_newbalanceDest']]
        
        X_train['transaction_direction_C2C'] = [1 if i=='C2C' else 0 for i in X_train['transaction_direction']]
        
        X_train['transaction_direction_C2M'] = [1 if i=='C2M' else 0 for i in X_train['transaction_direction']]
        
        X_train = X_train.drop(columns=['isFlaggedFraud', 'is_weekend', 'time_of_day', 'dest_type', 'oldbalanceOrg_status', 'newbalanceOrig_status', 'oldbalanceDest_status', 'newbalanceDest_status', 'is_oldbalanceOrg_higherthan_newbalanceOrig', 'is_oldbalanceDest_higherthan_newbalanceDest', 'transaction_direction'])
        
        

        
        
        # Label encoding - 'type'
        
        X_train['type'] = self.type_encoder.transform(X_train['type'])
        
        
        
        
        # Cyclic transform
        
        
        # Cyclic variables:
        
        # hour_of_day
        # day_of_week
        # period_of_day
        
        
        # First let's just encode 'period_of_day' from string to numbers
        
        # period_of_day (Label encoder)
        
        period_of_day_encoding_map = {'Morning': 1, 'Afternoon':2, 'Evening':3}
        
        X_train['period_of_day'] = X_train['period_of_day'].map(period_of_day_encoding_map)
        
        
        # Transforming the attributes
        
        # hour_of_day
        
        X_train['hour_of_day_sin'] = X_train['hour_of_day'].apply(lambda x: np.sin(x*(2.*np.pi/24)))
        X_train['hour_of_day_cos'] = X_train['hour_of_day'].apply(lambda x: np.cos(x*(2.*np.pi/24)))
        
        # day_of_week
        
        X_train['day_of_week_sin'] = X_train['day_of_week'].apply(lambda x: np.sin(x*(2.*np.pi/7)))
        X_train['day_of_week_cos'] = X_train['day_of_week'].apply(lambda x: np.cos(x*(2.*np.pi/7)))
        
        # period_of_day
        
        X_train['period_of_day_sin'] = X_train['period_of_day'].apply(lambda x: np.sin(x*(2.*np.pi/3)))
        X_train['period_of_day_cos'] = X_train['period_of_day'].apply(lambda x: np.cos(x*(2.*np.pi/3)))
        
        
        
        # Dropping the precursor attributes
        
        X_train = X_train.drop(columns=['hour_of_day','day_of_week', 'period_of_day'])
        
        
        # Columns selected by Boruta        
        
        cols_selected_boruta = ['step',
                                'type',
                                'amount',
                                'oldbalanceOrg',
                                'oldbalanceDest',
                                'newbalanceDest',
                                'day_of_month',
                                'oldbalanceDest_status_non-zero',
                                'newbalanceDest_status_non-zero',
                                'newbalanceDest_status_zero',
                                'hour_of_day_sin',
                                'hour_of_day_cos']
        
        return X_train[cols_selected_boruta]


    def get_predictions(self, model, test_raw, df_3):
        
        # prediction
        predictions = model.predict(df_3)
        
        # join predictions into the original data
        test_raw.loc[df_3.index, 'Predictions'] = predictions
        
        # return desired columns
        test_raw = test_raw[['step', 'type', 'amount', 'nameOrig', 'oldbalanceOrg', 'newbalanceOrig', 'nameDest', 'oldbalanceDest', 'newbalanceDest', 'isFlaggedFraud', 'Predictions']]
        
        
        return test_raw.to_json(orient='records', date_format='iso')


