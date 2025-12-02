import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import sys
import joblib
import os 
from dotenv import load_dotenv
env = load_dotenv(dotenv_path=r"C:\Users\Com\OneDrive\Documents\GitHub\Crypto_bot\.env")
from sklearn.preprocessing import StandardScaler
# sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../../Pipeline")))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add repo root to PYTHONPATH
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from Pipeline import GetData
import importlib
import requests


# Should Run once a  day
# First Get Fear and Greed Index using Coin Stat api
def get_dom_fag():
    # get dom 
    dom_url = "https://openapiv1.coinstats.app/insights/btc-dominance"
    querystring = {"type":"24h"}
    headers = {"X-API-KEY":os.getenv('COINSTAT_API_KEY')}
    response = requests.get(dom_url, headers=headers,params=querystring)
    dom_respo = response.json()
    res_pd = pd.DataFrame(dom_respo['data'], columns=['timestamp', 'DOM'])
    res_pd['DATE_STR'] = pd.to_datetime(res_pd["timestamp"], unit='s').dt.strftime('%Y-%m-%d %H:%M:%S').str.split(' ').str[0]
    res_pd['HOUR_STR'] = pd.to_datetime(res_pd['timestamp'], unit='s').dt.strftime('%Y-%m-%d %H:%M:%S').str.split(' ').str[1].str.split(':').str[0].astype(int)
    res_pd = res_pd.groupby(['DATE_STR','HOUR_STR'], as_index=False).mean(numeric_only=True)

    fag_url = "https://openapiv1.coinstats.app/insights/fear-and-greed"
    headers = {"X-API-KEY": os.getenv('COINSTAT_API_KEY')}
    response = requests.get(fag_url, headers=headers)
    fag_respo = response.json()
    # fag_respo['now']['update_time'].split(":")[0].replace("T"," ")
    res_pd['fag'] = fag_respo['now']['value']
    return res_pd


# Function to transform LIVE Data into format that is similar to locally stored data
def transform_live(data_frame):
  # MAKE A DATAFRAME of BTC price and other PARAMS
  hr_by_hr = pd.DataFrame()
  # main params 
  hr_by_hr['TIME_UNIX'] = data_frame['timestamp']
  hr_by_hr['DATE_STR'] = pd.to_datetime(hr_by_hr['TIME_UNIX'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S').str.split(' ').str[0]
  hr_by_hr['HOUR_STR'] = pd.to_datetime(hr_by_hr['TIME_UNIX'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S').str.split(' ').str[1].str.split(':').str[0].astype(int)
  hr_by_hr['OPEN_PRICE'] = data_frame['open']
  hr_by_hr['HIGH_PRICE'] = data_frame['high']
  hr_by_hr['CLOSE_PRICE'] = data_frame['close']
  hr_by_hr['LOW_PRICE'] = data_frame['low']
  hr_by_hr['VOLUME_FROM'] = data_frame['volume']
  hr_by_hr['VOLUME_TO'] =  hr_by_hr['VOLUME_FROM']/((hr_by_hr['HIGH_PRICE'] +hr_by_hr['LOW_PRICE']+hr_by_hr['CLOSE_PRICE'])/3)
  return hr_by_hr

# MAKE A DATAFRAME of BTC price and other PARAMS for the model
def Feat_extract(data_frame):
  hr_by_hr = pd.DataFrame()
  # main params 
  hr_by_hr['HOUR_STR'] = data_frame['HOUR_STR']
  hr_by_hr['OPEN_PRICE'] = data_frame['OPEN_PRICE']
  hr_by_hr['HIGH_PRICE'] = data_frame['HIGH_PRICE']
  hr_by_hr['CLOSE_PRICE'] = data_frame['CLOSE_PRICE']
  hr_by_hr['LOW_PRICE'] = data_frame['LOW_PRICE']
  hr_by_hr['VOLUME_FROM'] = data_frame['VOLUME_FROM']
  hr_by_hr['VOLUME_TO'] =  data_frame['VOLUME_TO']
  # Fear and Greed Index
  hr_by_hr['FAG'] = data_frame['fag']
  hr_by_hr['FAG'] = hr_by_hr['FAG'] /100  
  # Avg params
  hr_by_hr['ma_24h'] = hr_by_hr['CLOSE_PRICE'].rolling(24).mean()
  hr_by_hr['ma_72h'] = hr_by_hr['CLOSE_PRICE'].rolling(72).mean()
  hr_by_hr['ma_168h'] = hr_by_hr['CLOSE_PRICE'].rolling(168).mean()
  hr_by_hr['TIME_UNIX'] = data_frame['TIME_UNIX']
  # Percentage change with moving avg
  hr_by_hr['vol_8h'] = hr_by_hr['CLOSE_PRICE'].pct_change().rolling(8).std()# 8 hrs
  hr_by_hr['vol_24h'] = hr_by_hr['CLOSE_PRICE'].pct_change().rolling(24).std() # 1 day
  hr_by_hr['vol_72h'] = hr_by_hr['CLOSE_PRICE'].pct_change().rolling(72).std() # 3 days
  # Percentage change
  hr_by_hr['r_24h'] = hr_by_hr['CLOSE_PRICE'].pct_change(24) # 1 day
  hr_by_hr['r_72h'] = hr_by_hr['CLOSE_PRICE'].pct_change(72) # 3 day
  hr_by_hr['r_168h'] = hr_by_hr['CLOSE_PRICE'].pct_change(168) # 1 week
  # Date and time related features
  hr_by_hr['TIME_UNIXs'] = pd.to_datetime(hr_by_hr['TIME_UNIX'], unit='ms')
  hr_by_hr['dayofweek'] = hr_by_hr['TIME_UNIXs'].dt.dayofweek  # 0=Monday
  hr_by_hr['is_weekend'] = (hr_by_hr['TIME_UNIXs'].dt.dayofweek >= 5).astype(int)
  hr_by_hr['hour_sin'] = np.sin(2*np.pi*hr_by_hr['HOUR_STR']/24)
  hr_by_hr['hour_cos'] = np.cos(2*np.pi*hr_by_hr['HOUR_STR']/24)
  hr_by_hr['month'] = hr_by_hr['TIME_UNIXs'].dt.month
  # Add DMOMINANCE to ALL 24 hrs
  hr_by_hr['Dominance'] = data_frame['Dominance']
  hr_by_hr['Dominance'] = hr_by_hr['Dominance'] /100 
  hr_by_hr = hr_by_hr.drop(columns=['TIME_UNIXs','TIME_UNIX']) 
  # hr_by_hr.dropna(inplace=True)
  # hr_by_hr.to_csv( 'BTC_USD_1H_FEAT.csv', index=False)
  return hr_by_hr


# Function to create sequences for LSTM input
def create_sequences(X, time_steps=60):
    Xs= []
    for i in range(len(X) - time_steps):
        Xs.append(X[i : i + time_steps])
    return np.array(Xs)

# Extract LIVE DATA
importlib.reload(GetData)
data  = GetData.Manage_data()
live_data  =  data.fetch_ohlcv(limit=500)

live_data['timestamp'] = live_data.index

# Transform LIVE DATA to data similar to local data
live = transform_live(live_data)
# Load local csv
local_df = pd.read_csv("current_data.csv")
# Get Dom and fear 
dom_fag  =  get_dom_fag()


live_data['timestamp'] = live_data.index
transformed_live_data = transform_live(live_data)

new_live = transformed_live_data[
    (transformed_live_data['DATE_STR'] > local_df['DATE_STR'].iloc[-1]) |
    ((transformed_live_data['DATE_STR'] == local_df['DATE_STR'].iloc[-1]) & (transformed_live_data['HOUR_STR'] > local_df['HOUR_STR'].iloc[-1]))
]

if not new_live.empty:
   
  final_df = pd.concat([local_df, new_live], ignore_index=True)
  final_df = final_df.drop_duplicates(subset=['DATE_STR','HOUR_STR'],keep='last')
  final_df.drop(columns=['Unnamed: 0'], inplace=True, errors='ignore')
  final_df.iloc[-24:, final_df.columns.get_loc('Dominance')] = dom_fag['DOM'].values[:24]
  final_df.iloc[-24:, final_df.columns.get_loc('fag')] = dom_fag['fag'].values[:24]
  # Interpolate any NaN values in these columns (optional)
  final_df[['Dominance', 'fag']] = final_df[['Dominance', 'fag']].interpolate(method='linear')
  final_df.to_csv('current_data.csv', index =False)
  print('CSV updated!!!')
else:
   print("CSV Uptodate")
   


ready_data = Feat_extract(local_df)
cl = ready_data.dropna()
model = load_model("best_lstm_model_v2.keras", compile=False)

scaler_X = joblib.load('scaler_X.pkl')
Xx =np.array(cl)
X_scaled = scaler_X.fit_transform(Xx)  
X_seq= create_sequences(X_scaled, 168)
val = model.predict(X_seq)
# val = model.predict(X_seq[-1:])