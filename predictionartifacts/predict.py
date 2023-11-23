# import libraries
import math
import pandas as pd
import joblib

from django.templatetags.static import static
modeldataurl = static( '../vagrant/static/')

# modeldataurl = '/usr/local/apps/airpot-predictor/static/'

R = 6378137  # meters: the approximate radius of the earth.


def convert_coordinate(lat, long):
    # convert coordinate (Latitude,Longitude) to cartesian coordinate (x,y,z).
    x = R * math.cos(lat) * math.cos(long)
    y = R * math.cos(lat) * math.sin(long)
    z = R * math.sin(lat)

    return x, y, z


def truncate(number, decimal):
    factor = 10.0 ** decimal
    truncated_number = math.trunc(number * factor) / factor
    return truncated_number


'''
In accordance to the way the model was trained, the independent variables should be 24 as listed below;

# temp, feels_like, pressure, humidity,temp_min,temp_max,speed,deg,all,1h, currentSpeed, freeFlowSpeed, current_freeFlowSpeed, currentTravelTime, freeFlowTravelTime, freeFlow_currentTravelTime, confidence, roadClosure
# 279.55,274.2,1022,70,278.71,281.15,5.1,300,88,,0.4,17.33333333,21.0,0.825396825,95.0,73.5,0.820923134,0.999166667,0.0

Future models will most likely have some variables (such as latitude and longitude) dropped.
Also, the data would have been preprocessed further.
'''
POLLUTANTS = ('SO2', 'CO', 'FINE', 'NO', 'NO2', 'O3', 'PM1', 'PM10', 'PM25', 'TSP')


def forecast(indep_variables, dep_variables=POLLUTANTS):
    df = pd.DataFrame(indep_variables)
    if df.shape[1] == 18:
        df_copy = df.copy(deep=True)
        for d in dep_variables:
            d_up = str(d).upper()
            if d_up in POLLUTANTS:
                # print('predicting for {}'.format(d_up))
                model_file = modeldataurl+'/{}_model.h5'.format(d_up)
                reg = joblib.load(model_file)
                forecasts = reg.predict(df_copy)
                df[d_up] = forecasts
            else:
                if len(dep_variables) > 1:
                    continue
                else:
                    return 'There is no ML model defined for the specified pollutant/dependent-variable ({}).'.format(d)
        return df
    else:
        return 'Some data is missing.'

'''
# --- PLEASE REMOVE BEFORE DEPLOYMENT! !! !!! !!!! !!!!! ----
# sample implementation
data_file = 'data/sample_data.csv'
df = pd.read_csv(data_file)
df_copy = df.copy(deep=True)

# to predict for all pollutants
data_all = forecast(indep_variables=df)
print(data_all)

# to predict for some of the pollutants (e.g NO, SO2)
data_some = forecast(indep_variables=df_copy, dep_variables=['no', 'SO2'])
print(data_some)
# --- PLEASE REMOVE UP TO THIS LINE! !! !!! !!!! !!!!! ----
'''

