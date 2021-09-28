#import pandas as pd
#from IPython.display import display
#dataset_weather = pd.read_csv('datasets/weather.csv')
#dataset_station = pd.read_csv('datasets/station.csv')
#dataset_trip = pd.read_csv('datasets/trip.csv',error_bad_lines=False)
#exact
def mean_humidity_to_date (weather_df,humidity):
    date_df = (weather_df.loc[weather_df['Mean_Humidity'] == humidity, ['Date']])
    return date_df
def min_humidity_to_date (weather_df,humidity):
    date_df = (weather_df.loc[weather_df['Min_Humidity'] == humidity, ['Date']])
    return date_df
def max_humidity_to_date (weather_df,humidity):
    date_df = (weather_df.loc[weather_df['Max_Humidity'] == humidity, ['Date']])
    return date_df

def mean_temperature_to_date (weather_df,temp):
    date_df = (weather_df.loc[weather_df['Mean_Temperature_F'] == temp, ['Date']])
    return date_df
def min_temperature_to_date (weather_df,temp):
    date_df = (weather_df.loc[weather_df['Min_Temperature_F'] == temp, ['Date']])
    return date_df
def max_temperature_to_date (weather_df,temp):
    dates_df = (weather_df.loc[weather_df['Max_Temperature_F'] == temp,['Date']])
    return dates_df

def mean_to_date (weather_df,humidity,temp):
    date_df = (weather_df.loc[(weather_df['Mean_Temperature_F'] == temp) & (weather_df['Mean_Humidity'] == humidity), ['Date']])
    return date_df

def min_to_date (weather_df,humidity,temp):
    date_df = (weather_df.loc[(weather_df['Min_Temperature_F'] == temp) & (weather_df['Min_Humidity'] == humidity), ['Date']])
    return date_df

def max_to_date (weather_df,humidity,temp):
    date_df = (weather_df.loc[(weather_df['Max_Temperature_F'] == temp) & (weather_df['Max_Humidity'] == humidity), ['Date']])
    return date_df
#interval
def in_df_to_date (weather_df,humidity,temp):
    date_df = (weather_df.loc[((weather_df['Max_Temperature_F'] >= temp) & (weather_df['Min_Temperature_F'] <= temp)) & ((weather_df['Max_Humidity'] >= temp) & (weather_df['Min_Humidity'] <= humidity)), ['Date']])
    return date_df

#date_df = in_df_to_date(dataset_weather,62,68)
#display(date_df)

def from_count (df, id):
    count_df = df['from_station_id'].value_counts()
    count = count_df.loc[[id]]
    return count[0]

def to_count (df, id):
    count_df = df['to_station_id'].value_counts()
    count = count_df.loc[[id]]
    return count[0]

#display(from_count(dataset_trip, 'WF-01'))
#display(to_count(dataset_trip, 'WF-01'))

#tratar a parada (n equecer do pronto shop)
#display(dataset_trip.describe())
def outlier_ext_rmv (df):
    quantile_25 = df.tripduration.quantile(q=0.25)
    quantile_75 = df.tripduration.quantile(q=0.75)

    amp_interquartil = quantile_75 - quantile_25

    df = df.drop(df[df.tripduration < quantile_25 - 3 * amp_interquartil].index)
    df = df.drop(df[df.tripduration > quantile_75 + 3 * amp_interquartil].index)

    return df

def outlier_mod_rmv (df):
    quantile_25 = df.tripduration.quantile(q=0.25)
    quantile_75 = df.tripduration.quantile(q=0.75)

    amp_interquartil = quantile_75 - quantile_25

    df = df.drop(df[df.tripduration < quantile_25 - 1.5 * amp_interquartil].index)
    df = df.drop(df[df.tripduration > quantile_75 + 1.5 * amp_interquartil].index)

    return df

#dataset_trip = outlier_mod_rmv(dataset_trip)
#display(dataset_trip.describe())

def clean_from_station(dfA,dfB):
    return dfA.drop(dfA.loc[~dfA['from_station_id'].isin(dfB['station_id'])].index)

def clean_to_station(dfA,dfB):
    return dfA.drop(dfA.loc[~dfA['to_station_id'].isin(dfB['station_id'])].index)


#sera = clean_from_station(dataset_trip,dataset_station)
#sera = clean_to_station(sera,dataset_station)

#display(sera)
#display(sera['from_station_id'].value_counts())
#display(sera['to_station_id'].value_counts())
#display(dataset_trip['to_station_id'].value_counts())