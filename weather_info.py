# -*- coding: utf-8 -*-
import gzip
import urllib.request
from urllib import parse
import json
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


class Weather:
    def __init__(self, city):
        city_name = parse.quote_plus(city)
        only_now = parse.quote_plus("")
        
        # download data using the API
        appid = "0b194ffd0b8273c0e43ca06ea0edf059"
        url = "https://api.shenjian.io/weather/city/?appid="+appid+"&city_name="+city_name+"&only_now="+only_now
        request = urllib.request.Request(url, headers={
        	"Accept-Encoding": "gzip",
        })
        response = urllib.request.urlopen(request)
        gzipFile = gzip.GzipFile(fileobj=response)
        text = gzipFile.read().decode('UTF-8')
        
        # store the temperature data
        self.data = json.loads(text)
        if self.data['error_code'] == 0:
            self.data_now = self.data['data']['now'][0]

    def day_temp(self):
        day_array = self.data['data']['forecast7'][0]['hourForcast3']
        list_time = []
        list_temp = []
        for hour in day_array:
            time = hour['time']
            temprature = hour['temprature']
            list_time.append(time)
            list_temp.append(float(temprature[:-1]))
            
        # set .ttc file in order to show Chinese
        font = FontProperties(fname=r"C:\\WINDOWS\\Fonts\\simsun.ttc", size=14)
        length = len(list_time)
        
        # draw the temperature distribution in 24 hours and save it
        plt.plot(range(length), list_temp, color='b', marker='o')
        plt.xticks(range(length), list_time, rotation=15, 
                   fontproperties=font)
        for a, b in zip(range(length), list_temp):
            plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
        plt.xlabel("Time", fontsize=15)
        plt.ylabel("Temperature(℃)", fontsize=15)
        plt.title("Temperature in 24 hours.", fontsize=15)
        plt.tight_layout()
        plt.savefig("day_temp.png")
        plt.close()        
    
    def week_temp(self):
        week_array = self.data['data']['forecast7']
        list_date = []
        list_morning = []
        list_night = []
        for i in range(6):
            day = week_array[i+1]
            date = day['date']
            temp_morning = day['day'][0]['temprature']
            temp_night = day['night'][0]['temprature']
            list_date.append(date)
            list_morning.append(float(temp_morning[:-1]))
            list_night.append(float(temp_night[:-1]))
        
        font = FontProperties(fname=r"C:\\WINDOWS\\Fonts\\simsun.ttc", size=14)
        length = len(list_date)
        
        # draw the temperature distribution in 6 days and save it
        
        # plot the temperature in the mornings
        plt.plot(range(length), list_night, color='r', marker='o', label='night')
        for a, b in zip(range(length), list_night):
            plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
        
        # plot the temperature in the evenings
        plt.plot(range(length), list_morning, color='b', marker='o', label='morning')
        for a, b in zip(range(length), list_morning):
            plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
        
        # set the legend, axises and labels.
        plt.legend()
        plt.xticks(range(length), list_date, rotation=15,
                   fontproperties=font)
        plt.xlabel('Date', fontsize=15)
        plt.ylabel('Temperature(℃)', fontsize=15)
        plt.title('Temperature in 6 days', fontsize=15)
        plt.tight_layout()
        plt.savefig("week_temp.png")
        plt.close()
        return 0
  
      
if __name__ == '__main__':
    weather = Weather("合肥")
    # get the data of temprature in 7 days.
    #weather.week_temp()



