import urllib.request
import json
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from PIL import ImageGrab
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import csv
from datetime import datetime
import os.path
import errno
import threading



""" For future use, URL provides 'RadarMap' GIF """

# https://image.buienradar.nl/2.0/image/animation/RadarMapRainNL?height=512&width=500&extension=gif&renderBackground=True&renderBranding=False&renderText=True&history=0&forecast=10&skip=0
# customisable variables in image url:
# height(1~512), width(1~800), extension(gif,img)
# renderBackground(True, False), renderBranding(True, False)
# renderText(True, False), history(-30~30), False), forecast(0-10) skip(0-10)
# For future use



class WeatherDataFromInternet(object):
    """ Provides getting the weather data from the internet. """
    def __init__(self):
        self.weather_json = 'https://api.buienradar.nl/data/public/2.0/jsonfeed'
        self.response = urllib.request.urlopen(self.weather_json)
        self.result = json.loads(self.response.read())
        self.actual = self.result['actual']
        self.forecast = self.result['forecast']

class WeatherStation(WeatherDataFromInternet):
    """ Contains all the actual weather data of all weather stations' """
    def __init__(self):
        super().__init__()
        self.stationmeasurements = self.actual['stationmeasurements']
        self.weatherreport = self.forecast['weatherreport']
        self.shortterm = self.forecast['shortterm']
        self.longterm = self.forecast['longterm']
        self.fivedayforecast = self.forecast['fivedayforecast'][0]




class WeatherDataFiles(WeatherStation):
    def __init__(self):
        # Creates a new file or overwrites file with the same name,
        # writes dictionaries to CSV-file with added current time.
        super().__init__()
        def savestationdata():
            # Creates path if it doesn't exist and saves station data per station, in CSV format.
            save_path = './WeatherDataLog'
            try:
                os.makedirs(save_path)
            except FileExistsError:
                # directory already exists
                pass
            # for each dict in list, append value to csv file and write header if it doesnt exist.
            for x in self.stationmeasurements:
                file_name = os.path.join(save_path, x['stationname'])
                with open(file_name + '.csv', 'a') as f:
                    w = csv.DictWriter(f, x.keys())
                    if f.tell() == 0:
                        w.writeheader()
                        w.writerow(x)
                    else:
                        w.writerow(x)

            print("Logging...")
            threading.Timer(600.0, savestationdata).start()
            print(datetime.now())
        savestationdata()




class WeatherDisplay(WeatherStation, tk.Frame):
    """ Provides the GUI, powered by the Tkinter module. """
    def __init__(self, parent):
        super().__init__()
        # Initializes super class variables, tabControl for adding tabs, pack as grid manager
        # fires create_widgets function to initialize widgets.
        tk.Frame.__init__(self, parent)
        self.tabControl = ttk.Notebook(root)
        self.parent = parent
        self.pack()
        self.create_widgets()


    def create_widgets(parent):
        # Function to create widgets in root.
        print("Creating widgets...")


        def updatetab1drop1(stationname):
            # Function to update  tab1textbox1 based on DropDownMenu selection.

            # Blacklisting keys to filter out useless information.
            keyBlacklist = ['$id', 'iconurl', 'graphUrl']

            # Iterates through a list of dictionaries and appends the output to a new variable.
            newkeys = ""
            newvalues = ""
            for d in parent.stationmeasurements:
                for key, value in d.items():
                    if value == stationname:
                        for key, value in d.items():
                            if key not in keyBlacklist:
                                newkeys += str(key) + "\n"
                                newvalues += str(value) + "\n"
            # Strips new variables of empty lines at the end of file.
            newkeys = newkeys.strip()
            newvalues = newvalues.strip()

            # TAB 1 textbox1, 2 CONFIG
            tab1textbox1.configure(text=newkeys, borderwidth=3, relief="ridge")
            tab1textbox2.configure(text=newvalues, borderwidth=3, relief="ridge")

        def updatetab1drop2(stationname):
            # Function to update  tab1textbox2 based on DropDownMenu selection.

            # Blacklisting keys to filter out useless information.
            keyBlacklist = ['$id', 'iconurl', 'graphUrl']


            # Iterates through a list of dictionaries and appends the output to a new variable.
            newkeys = ""
            newvalues = ""
            for d in parent.stationmeasurements:
                for key, value in d.items():
                    if value == stationname:
                        for key, value in d.items():
                            if key not in keyBlacklist:
                                newkeys += str(key) + "\n"
                                newvalues += str(value) + "\n"

            # Strips new variables of empty lines at the end of file.
            newkeys = newkeys.strip()
            newvalues = newvalues.strip()

            # TAB 1 textbox3, 4 CONFIG
            tab1textbox3.configure(text=newkeys, borderwidth=3, relief="ridge")
            tab1textbox4.configure(text=newvalues, borderwidth=3, relief="ridge")



        # TAB 1
        tab1 = ttk.Frame(parent.tabControl)
        parent.tabControl.add(tab1, text="Actual")
        parent.tabControl.pack(expand=1, fill="both")

        tab1textbox1 = tk.Label(tab1, text="Select Station", anchor=tk.W, justify=tk.LEFT, font="Ariel 10 bold"
                                ,borderwidth=3, relief="ridge")
        tab1textbox1.pack(side=tk.LEFT, anchor=tk.N)

        tab1textbox2 = tk.Label(tab1, text="Select Station", anchor=tk.W, justify=tk.LEFT, font="Ariel 10"
                                ,borderwidth=3, relief="ridge")
        tab1textbox2.pack(side=tk.LEFT, anchor=tk.N)

        tab1textbox3 = tk.Label(tab1, text="Select Station", anchor=tk.W, justify=tk.LEFT, font="Ariel 10 bold"
                                , borderwidth=3, relief="ridge")
        tab1textbox3.pack(side=tk.LEFT, anchor=tk.N)

        tab1textbox4 = tk.Label(tab1, text="Select Station", anchor=tk.W, justify=tk.LEFT, font="Ariel 10"
                                , borderwidth=3, relief="ridge")
        tab1textbox4.pack(side=tk.LEFT, anchor=tk.N)


        # Iterates through list and dict to find key value and appending it to the empty options list.
        options = []
        for x in parent.stationmeasurements:
            for key, value in x.items():
                if key == 'stationname':
                    options.append(value)

        # Sets clicked var to StringVar and sets the first item in the list as default selection on app start.
        clicked1 = tk.StringVar()
        clicked1.set(options[0])

        # creates menus in GUI to select a station with, fires command to display information in textbox1, 2.
        DropDownMenu1 = tk.OptionMenu(tab1, clicked1, *options, command=updatetab1drop1)
        DropDownMenu1.pack()

        # Sets clicked var to StringVar and sets the second item in the list as default selection on app start.
        clicked2 = tk.StringVar()
        clicked2.set(options[1])
        # creates menus in GUI to select a station with, fires command to display information in textbox3, 4.
        DropDownMenu2 = tk.OptionMenu(tab1, clicked2, *options, command=updatetab1drop2)
        DropDownMenu2.pack()



        # TAB 2
        tab2 = ttk.Frame(parent.tabControl)
        parent.tabControl.add(tab2, text="History")
        parent.tabControl.pack(expand=1, fill="both")

        tab2textbox1 = tk.Label(tab2, text="", anchor=tk.W, justify=tk.LEFT, font="Ariel 10 bold",
                                )
        tab2textbox1.pack(side=tk.LEFT, anchor=tk.N)

        tab2textbox2 = tk.Label(tab2, text="", anchor=tk.W, justify=tk.LEFT, font="Ariel 10",
                                )
        tab2textbox2.pack(side=tk.LEFT, anchor=tk.N)

        df1 = pd.read_csv('Meetstation Arcen.csv', parse_dates=['timestamp'])

        df1['timestamp'] = pd.to_datetime(df1['timestamp'])
        df1.sort_values('timestamp', inplace=True)

        time = df1['timestamp']
        temperature = df1['temperature']
        rain = df1['rainFallLastHour']
        sunpower = df1['sunpower']
        windgusts = df1['windgusts']
        windspeed = df1['windspeed']
        windspeedBft = df1['windspeedBft']
        humidity = df1['humidity']


        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        canvas = FigureCanvasTkAgg(fig, master=tab2)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, tab2)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        ax.plot_date(time, temperature, linestyle='solid', label='temperature')
        ax.plot_date(time, humidity, linestyle='solid', label='humidity')

        fig.autofmt_xdate()

        # ax.set_xticks()
        # ax.set_xticklabels(topresults, fontdict=None, minor=False)
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.legend()
        plt.tight_layout()
        ax.set_title('History graph')
        print("Finished creating widgets.")
        print(df1)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDisplay(root)
    WeatherDataFiles = WeatherDataFiles()
    root.title("WeatherStationNL")
    root.geometry("800x800")
    root.resizable(True, True)
    root.mainloop()
