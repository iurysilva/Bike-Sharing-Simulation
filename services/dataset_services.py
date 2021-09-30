import pandas as pd
from IPython.display import display
import numpy as np


# exact
def mean_humidity_to_date(weather_df,humidity):
    date_df = (weather_df.loc[weather_df['Mean_Humidity'] == humidity, ['Date']])
    return date_df


def min_humidity_to_date(weather_df,humidity):
    date_df = (weather_df.loc[weather_df['Min_Humidity'] == humidity, ['Date']])
    return date_df


def max_humidity_to_date(weather_df,humidity):
    date_df = (weather_df.loc[weather_df['Max_Humidity'] == humidity, ['Date']])
    return date_df


def mean_temperature_to_date(weather_df,temp):
    date_df = (weather_df.loc[weather_df['Mean_Temperature_F'] == temp, ['Date']])
    return date_df


def min_temperature_to_date(weather_df,temp):
    date_df = (weather_df.loc[weather_df['Min_Temperature_F'] == temp, ['Date']])
    return date_df


def max_temperature_to_date(weather_df,temp):
    dates_df = (weather_df.loc[weather_df['Max_Temperature_F'] == temp,['Date']])
    return dates_df


def mean_to_date(weather_df,humidity,temp):
    date_df = (weather_df.loc[(weather_df['Mean_Temperature_F'] == temp) & (weather_df['Mean_Humidity'] == humidity), ['Date']])
    return date_df


def min_to_date(weather_df,humidity,temp):
    date_df = (weather_df.loc[(weather_df['Min_Temperature_F'] == temp) & (weather_df['Min_Humidity'] == humidity), ['Date']])
    return date_df


def max_to_date(weather_df,humidity,temp):
    date_df = (weather_df.loc[(weather_df['Max_Temperature_F'] == temp) & (weather_df['Max_Humidity'] == humidity), ['Date']])
    return date_df


# interval
def in_df_to_date(weather_df,humidity,temp):
    date_df = (weather_df.loc[((weather_df['Max_Temperature_F'] >= temp) & (weather_df['Min_Temperature_F'] <= temp)) &
                              ((weather_df['Max_Humidity'] >= humidity) & (weather_df['Min_Humidity'] <= humidity)), ['Date']])
    return date_df


def from_count(df, id):
    count_df = df['from_station_id'].value_counts()
    try:
        count = count_df.loc[[id]]
        return count[0]
    except KeyError:
        return 0


def to_count(df, id):
    count_df = df['to_station_id'].value_counts()
    try:
        count = count_df.loc[[id]]
        return count[0]
    except KeyError:
        return 0


def outlier_ext_rmv(df):
    quantile_25 = df.tripduration.quantile(q=0.25)
    quantile_75 = df.tripduration.quantile(q=0.75)

    amp_interquartil = quantile_75 - quantile_25

    df = df.drop(df[df.tripduration < quantile_25 - 3 * amp_interquartil].index)
    df = df.drop(df[df.tripduration > quantile_75 + 3 * amp_interquartil].index)

    return df


def outlier_mod_rmv(df):
    quantile_25 = df.tripduration.quantile(q=0.25)
    quantile_75 = df.tripduration.quantile(q=0.75)

    amp_interquartil = quantile_75 - quantile_25

    df = df.drop(df[df.tripduration < quantile_25 - 1.5 * amp_interquartil].index)
    df = df.drop(df[df.tripduration > quantile_75 + 1.5 * amp_interquartil].index)

    return df


def clean_from_station(dfA,dfB):
    return dfA.drop(dfA.loc[~dfA['from_station_id'].isin(dfB['station_id'])].index)


def clean_to_station(dfA,dfB):
    return dfA.drop(dfA.loc[~dfA['to_station_id'].isin(dfB['station_id'])].index)

def temp(df_trip,df_Date):

    return df_trip.drop(df_trip.loc[~df_trip['Date'].isin(df_Date['Date'])].index)

def clean_dataset():
    dataset_station = pd.read_csv('datasets/station_cleaned.csv')
    dataset_trip = pd.read_csv('datasets/trip_cleaned.csv')
    dataset_weather = pd.read_csv('datasets/weather.csv')

    dataset_weather['Date'] = pd.to_datetime(dataset_weather['Date']).dt.date
    dataset_trip['Date'] = pd.to_datetime(dataset_trip['starttime']).dt.date

    dataset_trip = outlier_ext_rmv(dataset_trip)

    cleaned_dataset = clean_from_station(dataset_trip, dataset_station)
    cleaned_dataset = clean_to_station(cleaned_dataset, dataset_station)
    cleaned_dataset = temp(cleaned_dataset, dataset_weather)
    cleaned_dataset.to_csv("datasets/trip_cleaned.csv", index=False)


def return_bad_stations(path):
    dataset_station = pd.read_csv(path)
    ids = []
    for row in range(len(dataset_station)):
        if dataset_station["current_dockcount"][row] == 0:
            ids.append(dataset_station["station_id"][row])
    return ids

def get_stations_rank(stations):
    popularity_number = np.zeros(len(stations))
    station_id = []
    for station in stations:
        lista = list(stations)
        popularity_number[lista.index(station)] = stations[station].popularity
        station_id.append(station)
    id = np.argsort(popularity_number)
    station_id = np.array(station_id)
    station_id = station_id[id[::-1]]
    print(popularity_number)
    print(station_id)
