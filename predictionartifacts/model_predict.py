# import
import requests
import json
import pandas as pd
import datetime, time
from predictionartifacts  import predict
import random, logging

#from django.contrib.staticfiles.storage import staticfiles_storage

#trafficdatacsvurl = staticfiles_storage.url('traffic_data_avg.csv')
from django.conf import settings
from django.templatetags.static import static
import os.path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

trafficdatacsvurl1 = static( '../vagrant/static/traffic_data_avg_1.csv')
trafficdatacsvurl2 = static( '../vagrant/static/traffic_data_avg_2.csv')

allsitedatacsvurl = static( '../vagrant/static/all_sites_coordinates.csv')

# trafficdatacsvurl1 = '/usr/local/apps/airpot-predictor/static/traffic_data_avg_1.csv'
# trafficdatacsvurl2 = '/usr/local/apps/airpot-predictor/static/traffic_data_avg_2.csv'

# allsitedatacsvurl = '/usr/local/apps/airpot-predictor/static/all_sites_coordinates.csv'




# ['CO', 'SO2', 'NO', 'TSP', 'PM1', 'FINE', 'O3', 'PM25', 'PM10', 'NO2']
def forecast(forecast_type, postcode, date='none'):
    pollutants = ['PM10', 'PM1', 'PM25',  'NO2', 'SO2', 'O3', 'CO', 'NO']
    prediction = []
    df_coordinates = pd.read_csv(allsitedatacsvurl)
    df_coord = df_coordinates[df_coordinates['postal_code'] == postcode]
    if not df_coord.empty:
        df_coord = df_coord.head(1)
        df_coord = df_coord.reset_index(drop=True)
        #print(df_coord)
        df_coord = df_coord.loc[0, ['latitude', 'longitude']]
        #print(df_coord)
        lat = df_coord['latitude']
        long = df_coord['longitude']
        if forecast_type == 'sevenDaysForecast':
            prediction = sevenDaysForecast(latitude=lat, longitude=long, pollutants=pollutants)
        elif forecast_type == 'pollutantsForecast':
            prediction = pollutantsForecast(latitude=lat, longitude=long, pollutants=pollutants)
        elif forecast_type == 'getForecast':
            prediction = getForecast(latitude=lat, longitude=long, pollutants=pollutants, date=date)
        else:  # forecast_type == 'sevenDaysForecast':
            prediction = sevenDaysForecast(latitude=lat, longitude=long, pollutants=pollutants)

        # get the max
        dt = prediction[['date', 'time']]
        print(prediction)
        prediction = prediction.drop(columns=['date', 'time'], axis=1)
        shape = prediction.shape
        cols = prediction.columns

        # get AQI
        prediction_aqi = prediction.copy(deep=True)
        # print(prediction)
        for i in range(shape[0]):
            for j in range(shape[1]):
                aqi, band = get_aqi(cols[j], prediction_aqi.iloc[i, j])
                prediction_aqi.iloc[i, j] = int(aqi)
        prediction = pd.concat([dt, prediction], axis=1)
        prediction_aqi = pd.concat([dt, prediction_aqi], axis=1)
        #print(prediction)
        #print(prediction_aqi)
        return prediction, prediction_aqi
    else:
        logging.ERROR('Postcode does not exist in record')
        return 'Postcode does not exist in record'


def sevenDaysForecast(latitude, longitude, pollutants):
    indep_variable, dt = get_data(latitude, longitude, data_size='daily')
    prediction = predict.forecast(indep_variables=indep_variable, dep_variables=pollutants)
    prediction = trim_pred(prediction, dt)
    return prediction


def pollutantsForecast(latitude, longitude, pollutants):
    indep_variable, dt = get_data(latitude, longitude, data_size='hourly')
    prediction = predict.forecast(indep_variables=indep_variable, dep_variables=pollutants)
    prediction = trim_pred(prediction, dt)
    return prediction


# date should be restricted to 2days (for hourly), or 7days (for daily)
def getForecast(date, latitude, longitude, pollutants):
    # filter data by date

    indep_variable, dt = get_data(latitude, longitude, data_size='hourly')
    prediction = predict.forecast(indep_variables=indep_variable, dep_variables=pollutants)
    prediction = trim_pred(prediction, dt)
    try:
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        dt_split = str(date).split(' ')
        prediction = prediction[(prediction['date'] == dt_split[0]) & (prediction['time'] == dt_split[1])]
    except:
        prediction = prediction.head(1)

    return prediction


def get_aqi(pollutant, value):
    aqi = 0
    band = ''
    value = round(value)
    if str(pollutant).upper() == 'O3':
        if value in range(0, 33+1):
            aqi = 1
            band = 'Low'
        elif value in range(34, 66+1):
            aqi = 2
            band = 'Low'
        elif value in range(67, 100+1):
            aqi = 3
            band = 'Low'
        elif value in range(101, 120+1):
            aqi = 4
            band = 'Moderate'
        elif value in range(121, 140+1):
            aqi = 5
            band = 'Moderate'
        elif value in range(141, 160+1):
            aqi = 6
            band = 'Moderate'
        elif value in range(161, 187+1):
            aqi = 7
            band = 'High'
        elif value in range(188, 213+1):
            aqi = 8
            band = 'High'
        elif value in range(214, 240+1):
            aqi = 9
            band = 'High'
        elif value >= 241:
            aqi = 10
            band = 'Very High'
    elif str(pollutant).upper() == 'NO2':
        if value in range(0, 67+1):
            aqi = 1
            band = 'Low'
        elif value in range(68, 134+1):
            aqi = 2
            band = 'Low'
        elif value in range(135, 200+1):
            aqi = 3
            band = 'Low'
        elif value in range(201, 267+1):
            aqi = 4
            band = 'Moderate'
        elif value in range(268, 334+1):
            aqi = 5
            band = 'Moderate'
        elif value in range(335, 400+1):
            aqi = 6
            band = 'Moderate'
        elif value in range(401, 467+1):
            aqi = 7
            band = 'High'
        elif value in range(468, 534+1):
            aqi = 8
            band = 'High'
        elif value in range(535, 600+1):
            aqi = 9
            band = 'High'
        elif value >= 601:
            aqi = 10
            band = 'Very High'
    elif str(pollutant).upper() == 'SO2':
        if value in range(0, 88+1):
            aqi = 1
            band = 'Low'
        elif value in range(89, 177+1):
            aqi = 2
            band = 'Low'
        elif value in range(178, 266+1):
            aqi = 3
            band = 'Low'
        elif value in range(267, 354+1):
            aqi = 4
            band = 'Moderate'
        elif value in range(355, 443+1):
            aqi = 5
            band = 'Moderate'
        elif value in range(444, 532+1):
            aqi = 6
            band = 'Moderate'
        elif value in range(533, 710+1):
            aqi = 7
            band = 'High'
        elif value in range(711, 887+1):
            aqi = 8
            band = 'High'
        elif value in range(888, 1064+1):
            aqi = 9
            band = 'High'
        elif value >= 1065:
            aqi = 10
            band = 'Very High'
    elif str(pollutant).upper() == 'PM25':
        if value in range(0, 11+1):
            aqi = 1
            band = 'Low'
        elif value in range(12, 23+1):
            aqi = 2
            band = 'Low'
        elif value in range(24, 35+1):
            aqi = 3
            band = 'Low'
        elif value in range(36, 41+1):
            aqi = 4
            band = 'Moderate'
        elif value in range(42, 47+1):
            aqi = 5
            band = 'Moderate'
        elif value in range(48, 53+1):
            aqi = 6
            band = 'Moderate'
        elif value in range(54, 58+1):
            aqi = 7
            band = 'High'
        elif value in range(59, 64+1):
            aqi = 8
            band = 'High'
        elif value in range(65, 70+1):
            aqi = 9
            band = 'High'
        elif value >= 71:
            aqi = 10
            band = 'Very High'
    elif str(pollutant).upper() == 'PM10':
        if value in range(0, 16+1):
            aqi = 1
            band = 'Low'
        elif value in range(17, 33+1):
            aqi = 2
            band = 'Low'
        elif value in range(34, 50+1):
            aqi = 3
            band = 'Low'
        elif value in range(51, 58+1):
            aqi = 4
            band = 'Moderate'
        elif value in range(59, 66+1):
            aqi = 5
            band = 'Moderate'
        elif value in range(67, 75+1):
            aqi = 6
            band = 'Moderate'
        elif value in range(76, 83+1):
            aqi = 7
            band = 'High'
        elif value in range(84, 91+1):
            aqi = 8
            band = 'High'
        elif value in range(92, 100+1):
            aqi = 9
            band = 'High'
        elif value >= 101:
            aqi = 10
            band = 'Very High'
    else:
        if value in range(0, 33+1):
            aqi = 1
            band = 'Low'
        elif value in range(34, 66+1):
            aqi = 2
            band = 'Low'
        elif value in range(67, 100+1):
            aqi = 3
            band = 'Low'
        elif value in range(101, 120+1):
            aqi = 4
            band = 'Moderate'
        elif value in range(121, 140+1):
            aqi = 5
            band = 'Moderate'
        elif value in range(141, 160+1):
            aqi = 6
            band = 'Moderate'
        elif value in range(161, 187+1):
            aqi = 7
            band = 'High'
        elif value in range(188, 213+1):
            aqi = 8
            band = 'High'
        elif value in range(214, 240+1):
            aqi = 9
            band = 'High'
        elif value >= 241:
            aqi = 10
            band = 'Very High'
    return aqi, band


def trim_pred(prediction, date_time):
    drop_cols = ['temp', 'feels_like', 'pressure', 'humidity', 'temp_min', 'temp_max', 'speed', 'deg', 'all', '1h',
                 ' currentSpeed', ' freeFlowSpeed', ' current_freeFlowSpeed', ' currentTravelTime', ' freeFlowTravelTime',
                 ' freeFlow_currentTravelTime', ' confidence', ' roadClosure']
    prediction = prediction.drop(columns=drop_cols, axis=1)
    trimmed_prediction = pd.concat([date_time, prediction], axis=1)
    trimmed_prediction = trimmed_prediction.sort_values(by=['date', 'time'], ascending=True)
    return trimmed_prediction


def merge_data(df_weather, df_traffic):
    df_weather = df_weather.fillna(0)
    # print('Merging data...')
    df_wp_latlong = df_weather[['time', 'dayOfTheWeek', 'latitude', 'longitude']].drop_duplicates()

    cols = df_weather.columns.append(df_traffic.columns)

    df_wpt_merged = pd.DataFrame(columns=cols)
    rec_wt_td = 0
    for d in df_wp_latlong.values:
        wp_data = df_weather[((df_weather['time'] == d[0]) & (df_weather['dayOfTheWeek'] == d[1]) & (df_weather['latitude'] == d[2]) &
                              (df_weather['longitude'] == d[3]))]
        wp_data.reset_index(drop=True, inplace=True)
        traffic_data = df_traffic[((df_traffic[' time_approx'] == d[0]) & (df_traffic['dayOfTheWeek_t'] == d[1]) &
                                        (df_traffic[' latitude_t'] == d[2]) & (df_traffic[' longitude_t'] == d[3]))]
        traffic_data.reset_index(drop=True, inplace=True)
        if len(traffic_data) > 0:
            wp_d_copy = wp_data.copy(deep=True)
            t_d_copy = traffic_data.copy(deep=True)
            t_val = traffic_data.append([t_d_copy]*(len(wp_d_copy) - 1), ignore_index=True)
            wp_d_copy[df_traffic.columns] = t_val

            df_wpt_merged = df_wpt_merged.append(wp_d_copy)
            rec_wt_td += 1

    return df_wpt_merged


# temp,feels_like,pressure,humidity,temp_min,temp_max,speed,deg,all,1h, currentSpeed, freeFlowSpeed, current_freeFlowSpeed, currentTravelTime, freeFlowTravelTime, freeFlow_currentTravelTime, confidence, roadClosure
# 279.55,274.2,1022,70,278.71,281.15,5.1,300,88,,0.4,17.33333333,21.0,0.825396825,95.0,73.5,0.820923134,0.999166667,0.0
def get_data(latitude, longitude, data_size):  # data_size == 'hourly' or 'daily'

    # get traffic data
    df_traffic = get_trafficData(latitude, longitude)

    # get weather
    df_weather = get_weatherData(latitude, longitude, type=data_size)

    # merge data
    df_W_T = merge_data(df_weather, df_traffic)

    df_dt = df_W_T[['date', 'time']]
    drop_cols = ['dt', 'date', 'time', 'dayOfTheWeek', 'latitude', 'longitude', 'dayOfTheWeek_t', ' time_approx',
                 ' coordinates', ' latitude_t', ' longitude_t', ' dt_t', 'latitude4', 'longitude4']
    df_W_T = df_W_T.drop(columns=drop_cols, axis=1)

    return df_W_T, df_dt


def get_trafficData(latitude, longitude):
    df_traffic1 = pd.read_csv(trafficdatacsvurl1)
    df_traffic2 = pd.read_csv(trafficdatacsvurl2)
    df_traffic = df_traffic1.append(df_traffic2, ignore_index=True)
    df_t = df_traffic[(df_traffic[' latitude_t'] == latitude) & (df_traffic[' longitude_t'] == longitude)]
    #print('Is empty'+ df_t)
    if df_t.empty:
        i = random.randint(0, 100)
        lat = df_traffic.loc[i, ' latitude_t']
        long = df_traffic.loc[i, ' longitude_t']
        df_t = df_traffic[(df_traffic[' latitude_t'] == lat) & (df_traffic[' longitude_t'] == long)]
        df_t = df_t.copy(deep=True)
        df_t[' latitude_t'].replace({lat: latitude}, inplace=True)
        df_t[' longitude_t'].replace({long: longitude}, inplace=True)

    return df_t


def get_weatherData(latitude, longitude, type='daily'):
    api_key = "d60f1d45eda257dedf7303347dd034f2"

    columns = ['dt', 'date', 'time', 'dayOfTheWeek', 'latitude', 'longitude', 'temp', 'feels_like', 'pressure', 'humidity', 'temp_min', 'temp_max',
               'speed', 'deg', 'all', '1h']  # 'id', 'main', 'description', 'icon',
    full_data = pd.DataFrame(columns=columns)
    try:
        if type=='hourly':
            url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,daily,alerts&appid={}'.format(latitude, longitude, api_key)
            response = requests.get(url)
            data = json.loads(response.text)

            dataList = pd.DataFrame.from_dict(data['hourly'], orient='columns')  # list
            for i in range(len(dataList)):
                dt = dataList['dt'][i]
                lat = latitude
                long = longitude
                temp = dataList['temp'][i]
                feels_like = dataList['feels_like'][i]
                pressure = dataList['pressure'][i]
                humidity = dataList['humidity'][i]
                temp_min = temp
                temp_max = temp
                speed = dataList['wind_speed'][i]
                deg = dataList['wind_deg'][i]
                all = dataList['clouds'][i]
                _1h = 0
                data = [dt, 0, 0, 0, lat, long, temp, feels_like, pressure, humidity, temp_min, temp_max, speed, deg, all, _1h]
                data = pd.DataFrame(columns=columns, data=[data])
                full_data = full_data.append(data, ignore_index=True)
        else:  # type=='daily'
            url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'.format(latitude, longitude, api_key)
            response = requests.get(url)
            data = json.loads(response.text)

            dataList = pd.DataFrame.from_dict(data['daily'], orient='columns')  # list
            for i in range(len(dataList)):
                dt = dataList['dt'][i]
                lat = latitude
                long = longitude
                temp_data = dataList['temp'][i]  # pd.DataFrame.from_dict(dataList['temp'][i], orient='columns')
                temp = temp_data['day']
                feels_like_data = dataList['feels_like'][i]
                feels_like = feels_like_data['day']
                pressure = dataList['pressure'][i]
                humidity = dataList['humidity'][i]
                temp_min = temp_data['min']
                temp_max = temp_data['max']
                speed = dataList['wind_speed'][i]
                deg = dataList['wind_deg'][i]
                all = dataList['clouds'][i]
                _1h = dataList['rain'][i]
                data = [dt, 0, 0, 0, lat, long, temp, feels_like, pressure, humidity, temp_min, temp_max, speed, deg, all, _1h]
                data = pd.DataFrame(columns=columns, data=[data])
                full_data = full_data.append(data, ignore_index=True)

        for d in full_data.values:
            date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(d[0])))
            dayOfTheWeek = time.strftime('%A', time.gmtime(d[0]))
            d_dt = str(date_time).split(' ')
            full_data.loc[full_data['dt'] == d[0], 'date'] = d_dt[0]
            full_data.loc[full_data['dt'] == d[0], 'time'] = d_dt[1]
            full_data.loc[full_data['dt'] == d[0], 'dayOfTheWeek'] = dayOfTheWeek
    except:
        logging.ERROR('Failure getting weather data')
    return full_data

'''
lat = 50.37167  # 51.76147
long = -4.142361  # -0.25146
# df, dt = get_data(latitude=lat, longitude=long, data_size='hourly')  # hourly, daily
# forecst = sevenDaysForecast(latitude=lat, longitude=long)
# forecst = pollutantsForecast(latitude=lat, longitude=long, pollutants=['no', 'SO2'])
forecst = getForecast(latitude=lat, longitude=long, date='2021-06-20 03:00:00')

'''
##forecst = forecast(forecast_type='pollutantsForecast', postcode='BN435DE', date='2021-06-20 03:00:00')
#print(forecst)
#forecast, aqi = forecast(forecast_type='getForecast', postcode='BN435DE', date='2021-06-28 03:00:00')
#aqi = aqi.drop(columns=['date','time'], axis=1)
#print (aqi.iloc[0,0])
# print (aqi.iloc[1,0])
#print (forecast.iloc[0,0])

