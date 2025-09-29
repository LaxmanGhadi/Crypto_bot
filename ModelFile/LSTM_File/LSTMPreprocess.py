import numpy as np 
import pandas as pd 


class LSTm_process :
    def __init__(self):
        self.feature_map = ['TIME_UNIX', 'DATE_STR', 'HOUR_STR', 'OPEN_PRICE', 'HIGH_PRICE',
        'CLOSE_PRICE', 'LOW_PRICE', 'VOLUME_FROM', 'VOLUME_TO',
        'Fear_Greed_Index', 'Sentiment', 'ma_24h', 'ma_72h', 'ma_168h',
        'vol_8h', 'vol_24h', 'vol_72h', 'r_24h', 'r_72h',
        'r_168h', 'TIME_UNIXs', 'dayofweek', 'is_weekend',
        'hour_sin', 'hour_cos', 'month', 'Dominance','Fear_Greed_Index','Sentiment'],
    def make_csv(csv1_path, csv2_path,):
        hr_by_hr = pd.read_csv(csv1_path)
        f_a_g = pd.read_csv(csv2_path)
        hr_by_hr['Fear_Greed_Index'] = np.nan
        hr_by_hr['Sentiment'] = np.nan
        for i in f_a_g['Date']:
            hr_by_hr.loc[hr_by_hr['DATE_STR'] == i, 'Fear_Greed_Index'] = f_a_g[f_a_g['Date'] == i]['Fear_Greed_Index'].iloc[0]
            hr_by_hr.loc[hr_by_hr['DATE_STR'] == i, 'Sentiment'] = f_a_g[f_a_g['Date'] == i]['Sentiment'].iloc[0]
        

        #
        hr_by_hr['ma_24h'] = hr_by_hr['CLOSE_PRICE'].rolling(24).mean()
        hr_by_hr['ma_72h'] = hr_by_hr['CLOSE_PRICE'].rolling(72).mean()
        hr_by_hr['ma_168h'] = hr_by_hr['CLOSE_PRICE'].rolling(168).mean()

        # Percentage change with moving avg
        hr_by_hr['vol_8h'] = hr_by_hr['CLOSE_PRICE'].pct_change().rolling(8).std()# 8 hrs
        hr_by_hr['vol_24h'] = hr_by_hr['CLOSE_PRICE'].pct_change().rolling(24).std() # 1 day
        hr_by_hr['vol_72h'] = hr_by_hr['CLOSE_PRICE'].pct_change().rolling(72).std() # 3 days
        # Percentage change
        hr_by_hr['r_24h'] = hr_by_hr['CLOSE_PRICE'].pct_change(24) # 1 day
        hr_by_hr['r_72h'] = hr_by_hr['CLOSE_PRICE'].pct_change(72) # 3 day
        hr_by_hr['r_168h'] = hr_by_hr['CLOSE_PRICE'].pct_change(168) # 1 week
        # Close price change
        # hr_by_hr['24_hr_close'] = hr_by_hr['CLOSE_PRICE'].pct_change(periods=24).shift(-24)
        # hr_by_hr['return_24h'] =  hr_by_hr['CLOSE_PRICE'].pct_change(periods=24).shift(-24)#  Remove this one

        hr_by_hr['TIME_UNIXs'] = pd.to_datetime(hr_by_hr['TIME_UNIX'], unit='s')
        hr_by_hr['dayofweek'] = hr_by_hr['TIME_UNIXs'].dt.dayofweek  # 0=Monday
        hr_by_hr['is_weekend'] = (hr_by_hr['TIME_UNIXs'].dt.dayofweek >= 5).astype(int)
        hr_by_hr['hour_sin'] = np.sin(2*np.pi*hr_by_hr['HOUR_STR']/24)
        hr_by_hr['hour_cos'] = np.cos(2*np.pi*hr_by_hr['HOUR_STR']/24)
        hr_by_hr['month'] = hr_by_hr['TIME_UNIXs'].dt.month


        hr_by_hr.dropna(inplace=True)
        return hr_by_hr