
def mean_humidity_to_date (weather_df,humidity):
    dates_df = (weather_df.loc[weather_df['Mean_Humidity'] == humidity,['Date']])
    return dates_df
def min_humidity_to_date (weather_df,humidity):
    dates_df = (weather_df.loc[weather_df['Min_Humidity'] == humidity,['Date']])
    return dates_df
def max_humidity_to_date (weather_df,humidity):
    dates_df = (weather_df.loc[weather_df['Max_Humidity'] == humidity,['Date']])
    return dates_df

def mean_temperature_to_date (weather_df,temp):
    dates_df = (weather_df.loc[weather_df['Mean_Temperature_F'] == temp,['Date']])
    return dates_df
def min_temperature_to_date (weather_df,temp):
    dates_df = (weather_df.loc[weather_df['Min_Temperature_F'] == temp,['Date']])
    return dates_df
def max_temperature_to_date (weather_df,temp):
    dates_df = (weather_df.loc[weather_df['Max_Temperature_F'] == temp,['Date']])
    return dates_df

def mean_to_date (weather_df,humidity,temp):
    dates_df = (weather_df.loc[(weather_df['Mean_Temperature_F'] == temp) & (weather_df['Mean_Humidity'] == humidity), ['Date']])
    return dates_df

def min_to_date (weather_df,humidity,temp):
    dates_df = (weather_df.loc[(weather_df['Min_Temperature_F'] == temp) & (weather_df['Min_Humidity'] == humidity), ['Date']])
    return dates_df

def max_to_date (weather_df,humidity,temp):
    dates_df = (weather_df.loc[(weather_df['Max_Temperature_F'] == temp) & (weather_df['Max_Humidity'] == humidity), ['Date']])
    return dates_df