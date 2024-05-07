import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import time

import time
start_time = time.time()

MyPrint = False
#Function that prints time. it'll also do that in other terminals, therefore the bool "MyPrint" is set to false.
def PrintTime(text):
    if MyPrint == True:
        print(round((time.time()) - start_time,4),text,)
        print()

#Prints the time
PrintTime("Start")

SmallestAcceptableTime = 2 # in seconds 
uploaded_file =st.file_uploader("Upload a CSV file", type=['csv'])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, sep=";" ,dtype=str, usecols=["No.", "Time"])
PrintTime("Load Data")

import numpy as np

#Make empty arrayes

ConvertedTimesIndexes = []
ConvertedTimes = []

PlottableTimeIndexes = []
PlottableTime = []

def ConverCSVtimeToSeconds(time):
    #Remove plusses from the string. they will always be the last element of the string
    if time[-1:] == "+":
        time = time[:-1]

    #Removes times that didnt finnish. They are in parentheses, so the first four elements and the last are removed.
    if time[0:3] == "DNF":
        time = time[4:-1]

    #Checks if the time contains minutes. else it would return an error
    if len(time)>5:
        min=int(time[:-6])
    else: min = 0

    # Converts the relevant elements in the string to a float representing the seconds.
    sec = float(time[-5:])

    sum = (60*min)+sec

    return sum

#Function to make other code more readable. Returns an element from the data.
def DataAccess(index, column):
   return df.iloc[index][column]

#Fills in the Converted times and its index with values.
def ConvertedArray():
    for i in range(len(df)):
        #print(ConverCSVtimeToSeconds(DataAccess(i,"Time")),DataAccess(i,"No."))
        ConvertedTimes.append(ConverCSVtimeToSeconds(DataAccess(i,"Time")))
        ConvertedTimesIndexes.append(int(DataAccess(i,"No.")))

ConvertedArray()

#Prints the time
PrintTime("Convert time from CSV")

#Exludes Junk data. Some datapoints are "DNF" meaning that it should be ignored. Also ex
def ExludeJunk(time,index):
    for element in range(len(time)):
        #If the three first elements if the string are "DNF", Dont add it to the final arrays
        if DataAccess(element,"Time")[0:3] == "DNF":
            continue
        #Likewise, if the 
        elif time[element] > SmallestAcceptableTime:
                PlottableTime.append(time[element])
                PlottableTimeIndexes.append(index[element])
        else: continue
    return PlottableTime, PlottableTimeIndexes

ExludeJunk(ConvertedTimes,ConvertedTimesIndexes)


AllTimes = [PlottableTime, PlottableTimeIndexes]

print(len(PlottableTime),len(ConvertedTimes))
# df.insert(2,"TimeInSeconds",PlottableTime,True)


PrintTime("Exlude DNF")
d = {"Time":PlottableTime,"No.":PlottableTimeIndexes}
GG = pd.DataFrame(d)

col1, col2 = st.columns(2)

columns = df.columns.tolist()

with col2:
        st.write("")
        st.write(df.head(len(df)))

with col1:
        # Create a slider for the x-value
        max_x_value = st.slider("max x-value", 0, len(df), len(df), 2000)
        max_y_value = st.slider("max y-value", 0, len(df), 20000, 2000)

        # Allow the user to select columns for plotting
        x_axis = st.selectbox('Select the X-axis', options=columns+["None"])
        y_axis = st.selectbox('Select the Y-axis', options=columns+["None"])

        plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
        # Allow the user to select the type of plot
        plot_type = st.selectbox('Select the type of plot', options=plot_list)

# Remove rows containing "DNF"
#df = df[~df['Time'].str.contains("DNF" or "+")]

# Use the slider value to select the x-values


x_values = df[x_axis][:max_x_value]
y_values = df[y_axis][:max_y_value]

# x_values = GG.loc("No.")
# y_values = GG.iloc("Time")

# Generate the plot
if st.button('Generate Plot'):
    fig, ax = plt.subplots(figsize=(6, 4))

    if plot_type == 'Line Plot':
        sns.lineplot(x=x_values, y=y_values, ax=ax)
    elif plot_type == 'Bar Chart':
        sns.barplot(x=x_values, y=y_values, ax=ax)
    elif plot_type == 'Scatter Plot':
        sns.scatterplot(x=x_values, y=y_values, ax=ax,legend=False)
    elif plot_type == 'Distribution Plot':
        sns.histplot(x_values, kde=True, ax=ax)
        y_axis='Density'
    elif plot_type == 'Count Plot':
        sns.countplot(x=x_values, ax=ax)
        y_axis = 'Count'

    # Adjust label sizes
    ax.tick_params(axis='x', labelsize=10)  # Adjust x-axis label size
    ax.tick_params(axis='y', labelsize=10)  # Adjust y-axis label size

    # Adjust title and axis labels with a smaller font size
    plt.title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=12)
    plt.xlabel(x_axis, fontsize=10)
    plt.ylabel(y_axis, fontsize=10)

    # Show the results
    st.pyplot(fig)