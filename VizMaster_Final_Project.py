
# coding: utf-8

# # VizMaster Final Project
# ## Group Members:  Ran Li, Xinzhe Deng, Yanyu Wang

# In[1]:


import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.path import Path

import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM
import cartopy.feature as cfeature

import ipywidgets
from ipywidgets import widgets
from ipywidgets import Label
from IPython.display import display
import IPython

from bqplot import (
    Figure, Map, Mercator, Orthographic, ColorScale, ColorAxis,
    AlbersUSA, topo_load, Tooltip, DateScale, LinearScale, Lines, Axis, Scatter
    )
from bqplot.interacts import (
    HandDraw
    )
import time

import traitlets
import datetime
import calendar
import warnings
warnings.filterwarnings('ignore')


# In[2]:


data_loc = input('Place enter the path of the file: ')


# In[3]:


daily_2017 = pd.read_csv(data_loc)
group_daily_2017 = daily_2017.groupby(["Latitude", "Longitude"])
group_daily_2017 = pd.DataFrame(group_daily_2017.count())
group_daily_2017 = group_daily_2017.reset_index()


# In[4]:


plt.rcParams["figure.dpi"] = 1000
def main():
    imagery = OSM()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([-60, -131, 51, 22], crs=ccrs.PlateCarree())
    
    states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')

    ax.add_image(imagery, 5)
    ax.scatter(group_daily_2017["Longitude"], group_daily_2017["Latitude"], s=0.1,color='b')
    plt.title('The locations of monitoring points')
    
    plt.show()


if __name__ == '__main__':
    main()


# #### This figure is representing the location of each AQI monitoring point in the United State. According to the map, the density of the distribution of AQI monitoring points can be clearly identified.

# In[5]:


daily_2017 = pd.read_csv(data_loc)
def read_data(df_name):
    data = df_name
    return data

# read_data(daily_2017)


# In[11]:


def read_data(df_name):
    data = df_name
    return data

data= pd.read_csv(data_loc)
dat = pd.read_csv(data_loc)
state_names = data["State Name"].unique()
state_list = ipywidgets.Dropdown(options = list(state_names), value='Illinois', description='State Name: ',)

@ipywidgets.interact(state = list(state_names))

def state_scatter(state = "Illinois"):
    data = read_data(dat)
    state_aqi = data.loc[data['State Name'] == state]
    state_aqi["Date Local"] = pd.to_datetime(state_aqi["Date Local"])
    
    x_date = state_aqi['Date Local'].unique()
    y_aqi = state_aqi.groupby("Date Local")["AQI"].mean()
    c_index = state_aqi.groupby("Date Local")["AQI"].mean()
    
    sc_x = DateScale()
    sc_y = LinearScale()
    sc_c = ColorScale(schema = 'GnYlRd_r')
    def_tt = Tooltip(fields=['x', 'y'], formats=['', '.2f'], labels = ['Date Local', 'Average AQI'])
    
    scatter = Scatter(x = x_date, y = y_aqi, color = c_index, scales={'x': sc_x, 'y': sc_y, 'color': sc_c}, 
                  tooltip=def_tt)
    
    ax_x = Axis(label='Date Local', scale=sc_x, label_location='end')
    ax_y = Axis(label='Daily Average AQI', scale=sc_y, 
                orientation='vertical', side='left')
    ax_c = ColorAxis(scale=sc_c, label='AQI', orientation='vertical', side='right')
    
    m_chart = dict(top=50, bottom=70, left=50, right=60)
    
    fig = Figure(axes=[ax_x, ax_c, ax_y], marks=[scatter], fig_margin=m_chart, title = "Daily Average AQI of "+state+" in 2017")
    
    return fig


# #### Since the dataset consists of the daily AQI data in 2017, it would be nice to show the AQI data in the state that the users would like to check. Therefore, the graph above makes it possible for the users to first select the state that they'd like to check through the drop down menu in the top-left part; then the plot would change accordingly and the users can also check the AQI of any single day throughout 2017. 

# In[7]:


def extract_pollution_dic(a_date,top_num):
        tem = data_through_time[data_through_time['Date Local']==a_date].sort_values(by='AQI').head(top_num)
        dic = {list(tem['State Code'])[_]:list(tem['AQI'])[_] for _ in range(len(list(tem['State Code'])))}
        return dic


# In[8]:


class dynamic_plot:
        
    def data_process(data_loc):
        global daily_2017, data_through_time, extract_date, extract_state_dic
        daily_2017 = pd.read_csv(data_loc)
        data_through_time = daily_2017.groupby(['State Code', 'State Name', 'Date Local'])
        data_through_time = data_through_time.mean()
        data_through_time = data_through_time.reset_index()
        extract_date = sorted(list(set(daily_2017['Date Local'])))
        extract_state = sorted(list(set(daily_2017['State Name'])))
        extract_state_dic = {extract_state[_]:extract_state[_] for _ in range(len(extract_state))}
    
    def line_plot(the_index, the_state='Illinois'):
        _ = the_index
        print(_)
        line_hd.x=pd.to_datetime(list(data_through_time[data_through_time['State Name']==the_state].sort_values(by='Date Local').head(_)['Date Local']))
        line_hd.y=list(data_through_time[data_through_time['State Name']==the_state].sort_values(by='Date Local').head(_)['AQI'])
        line_figure.title = 'The Air Quality Index of {}'.format(the_state)
        
    def us_polution_line(): # color_={1:50}
        xs_hd = DateScale()
        ys_hd = LinearScale()
        global line_hd
        line_hd = Lines(x=pd.to_datetime(list(data_through_time[data_through_time['State Code']==45].sort_values(by='Date Local')['Date Local'])),
                        y=list(data_through_time[data_through_time['State Code']==45].sort_values(by='Date Local')['AQI']),
                        scales={'x': xs_hd, 'y': ys_hd}, colors=['red'])

    #     handdraw = HandDraw(lines=line_hd)
        xax = Axis(scale=xs_hd, label='Date', grid_lines='none')
        yax = Axis(scale=ys_hd, label='AQI', orientation='vertical', grid_lines='none')
        
        global line_figure
        line_figure = Figure(marks=[line_hd], axes=[xax, yax], title = 'The Air Quality Index of ')
        
        return line_figure
    
            
    def us_polution(): # color_={1:50}
        sc_geo = AlbersUSA()
        sc_c1 = ColorScale(scheme='YlOrRd',min=0,max=100)
        def_tt = Tooltip(fields=['id', 'name'])
        global states_map
        states_map = Map(map_data=topo_load('map_data/USStatesMap.json'), scales={'projection': sc_geo,'color': sc_c1},
                     color={}, colors={'default_color': 'Grey'}, interactions = {'click': 'select', 'hover': 'tooltip'},
                        tooltip=def_tt, label='1')
        axis = ColorAxis(scale=sc_c1, label='AQI  ')
        
        global map_figure
        map_figure = Figure(marks=[states_map], axes=[axis],title='US Air Quality Index for States in',
                      fig_margin={'bottom': 50, 'left': 10, 'right': 10, 'top': 70}, legend_style={'fill': 'black'},
                     legend_text={'name':'111'})
        return map_figure
    
    def map_plot(the_index):
        a_date=extract_date[the_index]
        for __ in [1]:
            try:
                states_map.color=extract_pollution_dic(a_date,100)
                print(3)
                map_figure.title='US Air Quality Index for States in {}'.format(a_date)
                print(states_map.title)
            except:
                continue


# In[9]:


bf = dynamic_plot
bf.data_process(data_loc=data_loc)

play = widgets.Play(
#     interval=10,
    value=0,
    min=0,
    max=len(list(data_through_time[data_through_time['State Code']==45].sort_values(by='Date Local')['Date Local']))-1,
    step=1,
    description="Press play",
    disabled=False
)

time_progress= widgets.IntProgress(
    value=0,
    min=0,
    max=len(list(data_through_time[data_through_time['State Code']==45].sort_values(by='Date Local')['Date Local']))-1,
    step=1,
    description='Data Prog:',
    bar_style='', # 'success', 'info', 'warning', 'danger' or ''
    orientation='horizontal'
)

select_state=widgets.Dropdown(
    options=extract_state_dic,
    value='California',
    description='The State:',
)

widgets.jslink((play, 'value'), (time_progress, 'value'))
widgets.interactive_output(bf.line_plot, {'the_index': play,'the_state':select_state})
widgets.interactive_output(bf.map_plot, {'the_index': play})

top_ = widgets.HBox([play,time_progress,select_state])
middle_ = widgets.HBox([bf.us_polution(),bf.us_polution_line()])
widgets.VBox([top_,middle_])
#         return aa, bb, cc, dd


# #### The figures in this block are representing the AQI of each states and the variation trend of the selected state in the US, respectively. In the left figure, the color of each state is corresponding to the actual AQI value of the selected date. With the date changing, AQI is changing accoring to the date too. On the right side, the line represents the AQI of the chosen state. The line grows when time is iterating.
# #### For the widgets above the figures, the progressing of the time can be controlled by the most left widgets. The figures changes when time is iterating. The widget in the middle represents how is the progress of the time. Gray in the progressing bar is meaning the remaining dates to plot. Blue means the dates that already showed. The last widgets represents which state that shows in the right line graph. The state can be selected via the drop-down menu.

# In[10]:


t=pd.read_csv(data_loc)
def add_month(Ozone_data):    
    c=[]
    for i in Ozone_data["Date Local"]:
        datee = datetime.datetime.strptime(i, "%Y-%m-%d")
        c.append(datee.month)
    b=Ozone_data.assign(month=c)
    return b

from ipywidgets import widgets 
@ipywidgets.interact(Select_Month={'Jan':1,'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,'Nov': 11, 'Dec': 12},
                 Options={'Greatest': 10, 'Worst': -10})    
def show_month(Select_Month,Options):
    Ozone_data = add_month(t)
    real_month=Ozone_data.loc[Ozone_data["month"]==Select_Month]
    real_month=real_month.groupby(["State Name"])
    real_month=real_month.mean()
    real_month=real_month.reset_index()
    real_month.sort_values("AQI", inplace=True)
    if Options==10:
        b=real_month[0:Options].reset_index()
    if Options==-10:
        b=real_month[Options:].reset_index()
    plt.bar(b["State Name"],b["AQI"],width=0.5, color='#D55D43')
    plt.xlabel('State Names', fontsize=20)
    plt.xticks(rotation = 45, fontsize = 14)
    plt.ylabel('Average AQI', fontsize=20)
    plt.yticks(rotation = 45, fontsize = 14)
    plt.title('Top 10 States in '+ calendar.month_name[Select_Month], fontsize =28)
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    plt.show()


# #### We are interested in mean AQI in each state in United States because we could find the top 10 greatest and top 10 worst AQI state in United States. The users could use this to predict which state is better to live in terms of air quality. It can be done through two drop-down boxes containing the month and whether the best or the worst when plotting the average AQI
