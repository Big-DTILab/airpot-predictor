from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from predictionartifacts import model_predict

import random


from airpot_api import serializers
from airpot_api import models
from airpot_api import permissions
from datetime import datetime, timedelta


class AirpotAfordApiView(APIView):
    """Air-quality-forecast-model (AFord) API by DTI-Lab UH"""
    serializer_class = serializers.AirpotAfordSerializer


    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs',
        ]

        Day1 = random.randint(1, 250)
        Day2 = random.randint(1, 250)
        Day3 = random.randint(1, 250)
        Day4 = random.randint(1, 250)
        Day5 = random.randint(1, 250)
        Day6 = random.randint(1, 250)
        Day7 = random.randint(1, 250)

        return Response(
            {
            'Day1': Day1, 
            'Day2': Day2, 
            'Day3': Day3,
            'Day4': Day4,
            'Day5': Day5,
            'Day6': Day6,
            'Day7': Day7
            })

    
    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        # if serializer.is_valid():
        #     name = serializer.validated_data.get('day')
        #     message = f'Hello {name}'
        #     return Response({'message': message})
        # else:
        #     return Response(
        #         serializer.errors, 
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        return Response({'method': 'POST'})
    

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch (self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})



#forecast = model_predict.sevenDaysForecast(latitude=51.45258004, longitude=0.070766)

class SevenDaysForcastViewSet(viewsets.ViewSet):
    """Air-quality-forecast-model (AFord) API by DTI-Lab UH"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = serializers.SevenDaysForcastSerializer
    




    def list(self, request):
        """Return a hello message"""
        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]
        forecast, aqi = model_predict.forecast(forecast_type='sevenDaysForecast', postcode='BN435DE', date='none')
        
        aqi = aqi.drop(columns=['date','time'], axis=1)
        
        Day1 = int(aqi.iloc[0,0])
        Day2 = int(aqi.iloc[1,0])
        Day3 = int(aqi.iloc[2,0])
        Day4 = int(aqi.iloc[3,0])
        Day5 = int(aqi.iloc[4,0])
        Day6 = int(aqi.iloc[5,0])
        Day7 = int(aqi.iloc[6,0])


        return Response(
            {
            'Day1': Day1, 
            'Day2': Day2, 
            'Day3': Day3,
            'Day4': Day4,
            'Day5': Day5,
            'Day6': Day6,
            'Day7': Day7
            })


    def create (self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        # if serializer.is_valid():
        #     name = serializer.validated_data.get('name')
        #     message = f'Hello {name}'
        #     return Response({'message': message})
        # else:
        #     return Response(
        #         serializer.errors, 
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        return Response({'http_method': 'POST'})
    

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})

    
    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})

    def delete(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})



class PollutantsForcastViewSet(viewsets.ViewSet):
    """Air-quality-forecast-model (AFord) API by DTI-Lab UH"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = serializers.PollutantsForcastSerializer

    def list(self, request):
        """Return a hello message"""
        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]

        forecast, aqi = model_predict.forecast(forecast_type='sevenDaysForecast', postcode='BN435DE', date='none')
        
        forecast = forecast.drop(columns=['date','time'], axis=1)
        


        PM10 = round(forecast.iloc[0,0], 2)
        PM1 = round(forecast.iloc[0,1], 2)
        PM25 = round(forecast.iloc[0,2],2)
        NO2 = round(forecast.iloc[0,3], 2)
        SO2 = round(forecast.iloc[0,4], 2)
        O3 = round(forecast.iloc[0,5], 2)
        CO = round(forecast.iloc[0,6], 2)
        NO = round(forecast.iloc[0,7], 2)

        return Response(
            {
            'PM10': PM10, 
            'PM1': PM1,
            'PM25': PM25,
            'NO2': NO2,
            'SO2': SO2,
            'O3': O3,
            'CO': CO,
            'NO': NO
            })


    def create (self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        forecast, aqi = model_predict.forecast(forecast_type='sevenDaysForecast', postcode='BN435DE', date='none')
        forecast = forecast.drop(columns=['date','time'], axis=1)

        

        if serializer.is_valid():
            temp = -1
            temp2 = -2

            # PM10 = 1
            # PM1 = 2
            # PM25 = 3
            # NO2 = 4
            # SO2 = 5
            # O3 = 6
            # CO = 7
            # NO = 8

            pollutantId = serializer.validated_data.get('pollutantId')

            Pollutants = ['PM10',  'PM1', 'PM25', 'NO2', 'SO2', 'O3', 'CO', 'NO']

            polID = pollutantId - 1

            temp2  = Pollutants[polID]

            
            

            # if pollutantId == 1:
            #     temp = round(forecast.iloc[pollutantId - 1,1], 2)
            #     temp2 = 'PM10'
            # elif pollutantId == 2:
            #     temp = round(random.uniform(1,100), 1)
            #     temp2 = 'PM1'
            # elif pollutantId == 3:
            #     temp = random.randint(1, 80)
            #     temp2 = 'PM25'
            # elif pollutantId == 4:
            #     temp = round(random.uniform(1,610), 1)
            #     temp2 = 'NO2'
            # elif pollutantId == 5:
            #     temp = round(random.uniform(1,1100), 1)
            #     temp2 = 'SO2'
            # elif pollutantId == 6:
            #     temp = random.randint(1,250)
            #     temp2 = 'O3'
            # elif pollutantId == 7:
            #     temp = round(random.uniform(1,100), 1)
            #     temp2 = 'CO'
            # elif pollutantId == 8:
            #     temp = round(random.uniform(1,300), 1)
            #     temp2 = 'NO'
            # else:
            #     return Response(
            #         serializer.errors, 
            #         status=status.HTTP_400_BAD_REQUEST
            #     )

            # return Response(
            #     {
            #         temp2 +'Day1': temp, 
            #         temp2 +'Day2': temp + round(random.uniform(1,5), 1), 
            #         temp2 +'Day3': temp + round(random.uniform(1,100), 1),
            #         temp2 +'Day4': temp + round(random.uniform(1,40), 1),
            #         temp2+'Day5': temp +round(random.uniform(1,88), 1),
            #         temp2+'Day6': temp+round(random.uniform(1,300), 1),
            #         temp2+'Day7': temp + round(random.uniform(1,543), 1)
            #     })

            return Response(

            {
                temp2 +'Day1': round(forecast.iloc[0, pollutantId - 1], 2),

                temp2 +'Day2': round(forecast.iloc[1, pollutantId - 1], 2),

                temp2 +'Day3': round(forecast.iloc[2, pollutantId - 1], 2),

                temp2 +'Day4': round(forecast.iloc[3, pollutantId - 1], 2),

                temp2+'Day5': round(forecast.iloc[4, pollutantId - 1], 2),

                temp2+'Day6': round(forecast.iloc[5, pollutantId - 1], 2),

                temp2+'Day7': round(forecast.iloc[6, pollutantId - 1], 2),

            })
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
        # return Response({'http_method': 'POST'})
    

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})

    
    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})

    def delete(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})



class GetForcastViewSet(viewsets.ViewSet):
    """Air-quality-forecast-model (AFord) API by DTI-Lab UH"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = serializers.GetForcastSerializer

    # def list(self, request):
    #     """Return a hello message"""
    
    #     return Response({'http_method': 'GET'})


    def create (self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            date = serializer.validated_data.get('date')
            location = serializer.validated_data.get('location')
            # time = serializer.validated_data.get('time')

            # choices = serializer.validated_data.get('choices')

            PM10 = random.randint(1, 120)
            PM1 = round(random.uniform(1,100), 1)
            PM25 = random.randint(1, 80)
            NO2 = round(random.uniform(1,610), 1)
            SO2 = round(random.uniform(1,1100), 1)
            O3 = random.randint(1,250)
            CO = round(random.uniform(1,100), 1)
            NO = round(random.uniform(1,300), 1)
            AQI = random.randint(1, 3)
            dateFormated = str(date).replace('T', ' ').replace('Z', '').replace('+00:00', '')

            dt = dateFormated.split(' ')
            d_time = dt[1].split(':')[0]
            d_time = str(d_time) + ':00' + ':00'
            dateFormated = dt[0] + ' ' + d_time

            # Date Conversion 
            datetime_object = datetime.strptime(dateFormated, '%Y-%m-%d %H:%M:%S')
            datetime46hr = datetime.now()  + timedelta(hours=46)
            datetime7Days = datetime.now()  + timedelta(days=7)

            if (datetime_object < datetime46hr ):
                forecast, aqi = model_predict.forecast(forecast_type='getForecast', postcode=location, date=dateFormated)
                forecast = forecast.drop(columns=['date','time'], axis=1)
                aqi = aqi.drop(columns=['date','time'], axis=1)

                PM10 = round(forecast.iloc[0, 0], 2)
                PM1 = round(forecast.iloc[0, 1], 2)
                PM25 = round(forecast.iloc[0, 2], 2)
                NO2 = round(forecast.iloc[0, 3], 2)
                SO2 = round(forecast.iloc[0, 4], 2)
                O3 = round(forecast.iloc[0, 5], 2)
                CO = round(forecast.iloc[0, 6], 2)
                NO = round(forecast.iloc[0, 7], 2)
                AQI = int(aqi.iloc[0, 1])

                return Response(
                    {
                        'PM10': PM10, 
                        'PM1': PM1,
                        'PM25': PM25,
                        'NO2': NO2,
                        'SO2': SO2,
                        'O3': O3,
                        'CO': CO,
                        'NO': NO,
                        'AQI': AQI,
                        'misc':{
                            'date':dateFormated,
                            'location':location,
                            # 'time':time,
                            # 'choices': choices
                        }
                    })

            elif (datetime_object > datetime46hr and  datetime_object <= datetime7Days):
                forecast, aqi = model_predict.forecast(forecast_type='sevenDaysForecast', postcode=location, date='none')
                forecast = forecast[forecast['date'] == dt[0]]
                forecast = forecast.drop(columns=['date','time'], axis=1)
                aqi = aqi[aqi['date'] == dt[0]]
                aqi = aqi.drop(columns=['date','time'], axis=1)

                PM10 = round(forecast.iloc[0, 0], 2)
                PM1 = round(forecast.iloc[0, 1], 2)
                PM25 = round(forecast.iloc[0, 2], 2)
                NO2 = round(forecast.iloc[0, 3], 2)
                SO2 = round(forecast.iloc[0, 4], 2)
                O3 = round(forecast.iloc[0, 5], 2)
                CO = round(forecast.iloc[0, 6], 2)
                NO = round(forecast.iloc[0, 7], 2)
                AQI = int(aqi.iloc[0, 1])

                return Response(
                    {
                        'PM10': PM10, 
                        'PM1': PM1,
                        'PM25': PM25,
                        'NO2': NO2,
                        'SO2': SO2,
                        'O3': O3,
                        'CO': CO,
                        'NO': NO,
                        'AQI': AQI,
                        'misc':{
                            'date':dateFormated,
                            'location':location,
                            # 'time':time,
                            # 'choices': choices
                        }
                    })

            else:
               return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )

            
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
    

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})

    
    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})

    def delete(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
