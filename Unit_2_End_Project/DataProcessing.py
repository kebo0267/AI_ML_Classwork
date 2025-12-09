import base64
import json
from datetime import datetime, timedelta
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import make_friedman1
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, root_mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder,StandardScaler

class DataProcessing:
    def __init__(self):
        self.df = None
        self.df_orig = None
        self.scaled_df = None
        self.dateFormat = "%Y-%m-%d %H:%M:%S"
   
    def loadFromJson(self,filename):
        self.df_orig = pd.read_json(filename)
        self.reset_processor()

    def loadFrom_CSV(self,filename):
        self.df_orig = pd.read_csv(filename)
        self.reset_processor()

    def reset_processor(self):
        self.df = self.df_orig.copy()


    def get_copy(self):
        return self.df.copy()
    
    def get_original_copy(self):
        return self.df_orig.copy()
    
    def get_scaled_data(self):
        return self.scaled_df
    
    def get_info(self):
        retVal = ""
        for col in self.df.columns:
            retVal = f'{retVal} Column: {col} - Data Type {self.df[col].dtype}\n'

        return retVal
    
    def get_mean(self,parameter):
        ret_val = None
        if (not self.df[parameter].dtype is object):
            ret_val = self.df[parameter].mean()

        return ret_val;

    def get_min(self,parameter):
        ret_val = None
        if (not self.df[parameter].dtype is object):
            ret_val = self.df[parameter].min()

        return ret_val;

    def get_max(self,parameter):
        ret_val = None
        if (not self.df[parameter].dtype is object):
            ret_val = self.df[parameter].max()

        return ret_val;

    def get_std(self,parameter):
        ret_val = None
        if (not self.df[parameter].dtype is object):
            ret_val = self.df[parameter].std()

        return ret_val;

    def describe(self,parameter,data=None):
        ret_val = None
        if (not self.df[parameter].dtype is object):
            ret_val = self.df[parameter].describe()

        return ret_val;


    def locateMissingData(self):
        missing_data = {}
        if not self.df is None:
            df_size = len(self.df)
            for col in self.df.columns:
                if (self.df[col].dtype == object):
                    if len(self.df[self.df[col].astype(str).str.strip().eq("")]) > 0:
                        missing_data[col] = self.df[self.df[col].astype(str).str.strip().eq("")].index.tolist()
                else:
                    if (len(self.df[self.df[col].isna()] == True) > 0) or (len(self.df[self.df[col].isnull()] == True) > 0):
                        null_indexes = set()
                        null_indexes.update(self.df[self.df[col].isna()].index.tolist())
                        null_indexes.update(self.df[self.df[col].isnull()].index.tolist())
                        missing_data[col] = null_indexes
        return missing_data
    
    def processNumericDataTypes(self):
        if not self.df is None:
            for col in self.df.columns:
                if self.df[col].dtype == "int64":
                    if (self.df[col].max() <= np.iinfo(np.int8).max) and (self.df[col].min() >= np.iinfo(np.int8).min):
                        self.df[col] = self.df[col].astype("int8")
                    elif (self.df[col].max() <= np.iinfo(np.int16).max) and (self.df[col].min() >= np.iinfo(np.int16).min):
                      self.df[col] = self.df[col].astype("int16")
                elif self.df[col].dtype == "float64":
                    if (self.df[col].max() <= np.finfo(np.float32).max) and (self.df[col].min() >= np.finfo(np.float32).min):
                        self.df[col] = self.df[col].astype("float32")

    def processBinaryDataTypes(self,parameter,options=None):
        if not self.df is None:

            if self.df[parameter].dtype == object:
                unique_values = self.df[parameter].unique()
                if (len(unique_values) == 2):
                    choice_map = {}
                    if options == None:
                        choice_map[unique_values[0]] = False
                        choice_map[unique_values[0]] = True
                    else:
                        choice_map = options

                    self.df[parameter] = self.df[parameter].map(choice_map).astype("bool")



    def processObjectDataTypes(self,excluded_parameters=None):
        if not self.df is None:
            df_columns = self.df.columns
            for col in df_columns:
                if col in excluded_parameters:
                    continue
                if self.df[col].dtype == object:
                    unique_values = self.df[col].unique()
                    if (len(unique_values) == 2):
                        self.processBinaryDataTypes(col)
                    else:
                        if (len(unique_values)/len(self.df[col]) < 0.15):
                            encoder = OneHotEncoder(sparse_output=False,handle_unknown="ignore").set_output(transform='pandas')
                            encode_data = encoder.fit_transform(self.df[[col]])
                            self.df = pd.concat([self.df, encode_data],axis=1).drop(columns=[col])

    def processDateTimeParameters(self,parameter,format='%d/%m/%Y %H'):
        if not self.df is None:
            self.df[parameter] = pd.to_datetime(self.df[parameter],format=format)
            self.df[f'{parameter}_Year'] = self.df[parameter].dt.year.astype("int16")
            self.df[f'{parameter}_Month'] = self.df[parameter].dt.month.astype("int16")
            self.df[f'{parameter}_Day'] = self.df[parameter].dt.day.astype("int16")
            self.df[f'{parameter}_hour'] = self.df[parameter].dt.hour.astype("int16")
            self.df[f'{parameter}_Min'] = self.df[parameter].dt.minute.astype("int16")
            self.df[f'{parameter}_sec'] = self.df[parameter].dt.second.astype("int16")
            self.df[f'{parameter}_micro'] = self.df[parameter].dt.microsecond.astype("int16")

    def processWithStandardScaler(self):
        drop_columns = []
        scale_columns = []
        for col in self.df.columns:
            if (str(self.df[col].dtype).startswith("float")) or (str(self.df[col].dtype).startswith("int")):
                scale_columns.append(col)
            else:
                drop_columns.append(col)
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(self.df.drop(columns=drop_columns))
        self.scaled_df = pd.DataFrame(scaled_data,columns=scale_columns)

    def get_groupby_data(self,cateagories=None):
        ret_value = self.get_copy()
        if not cateagories is None:
           ret_value = ret_value.groupby(cateagories)

        return ret_value
    
    def get_scatter_plot(self,paramters=None):
        if not paramters is None:
        
        # Visualize
        fig, axes = plt.subplots(1, 2, figsize=(8, 3))

        axes[0].set_title('Original distribution')
        axes[0].hist(df[feature], bins=50, edgecolor='black', color='grey')
        axes[0].set_xlabel(feature)
        axes[0].set_ylabel('Frequency')

        axes[1].set_title('Square root-transformed distribution')
        axes[1].hist(df[f'{feature}_sqrt'], bins=50, edgecolor='black', color='grey')
        axes[1].set_xlabel(f'{feature}_sqrt')
        axes[1].set_ylabel('Frequency')



        plt.tight_layout()
        plt.show()
    


