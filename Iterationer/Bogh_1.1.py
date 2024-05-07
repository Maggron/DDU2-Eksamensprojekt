import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import time
import numpy as np
import base64
from PIL import Image

# Import the Bögh icon
icon = Image.open("Bögh_transparent.png")

# Plot style
sns.set_style("whitegrid")

# Set the page config
st.set_page_config(page_title = 'Bögh',
                   layout = 'centered',
                   page_icon = icon)

# Title
st.title('Bögh')

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
    df = pd.read_csv(uploaded_file, delimiter=",")
    columns = df.columns.tolist()

    # If the number of columns equals 2, try again with ';' as the delimiter
    if len(columns) <= 2:
        uploaded_file.seek(0)  # Reset the file pointer to the beginning
        df = pd.read_csv(uploaded_file, delimiter=';')
        columns = df.columns.tolist()
PrintTime("Load Data")


#Make empty arrayes
ConvertedTimesIndexes = []
ConvertedTimes = []

PlottableTimeIndexes = []
PlottableTime = []

def ConverCSVtimeToSeconds(time):
    if 'Time' in df.columns:
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
    if 'Time' in df.columns:
        return df.iloc[index][column]

#Fills in the Converted times and its index with values.
def ConvertedArray():
    if 'Time' in df.columns:
        for i in range(len(df)):
            #print(ConverCSVtimeToSeconds(DataAccess(i,"Time")),DataAccess(i,"No."))
            ConvertedTimes.append(ConverCSVtimeToSeconds(DataAccess(i,"Time")))
            ConvertedTimesIndexes.append(int(DataAccess(i,"No.")))

if 'Time' in df.columns:
    ConvertedArray()

    #Prints the time
    PrintTime("Convert time from CSV")

#Exludes Junk data. Some datapoints are "DNF" meaning that it should be ignored. Also ex
def ExludeJunk(time,index):
    if 'Time' in df.columns:
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

if 'Time' in df.columns:
    ExludeJunk(ConvertedTimes,ConvertedTimesIndexes)

    AllTimes = [PlottableTime, PlottableTimeIndexes]

    print(len(PlottableTime),len(ConvertedTimes),"YESSIR")
# df.insert(2,"TimeInSeconds",PlottableTime,True)


PrintTime("Exlude DNF")
#d = {"Time":PlottableTime,"No.":PlottableTimeIndexes}
#df = pd.DataFrame(d)
if 'Time' in df.columns:
    df['TimeInSeconds'] = pd.Series(PlottableTime)

def get_binary_file_downloader_html(bin_file, file_label='File', button_text='Download',):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}.png">{button_text}</a>'
    return href

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns([1, 1, 3])

columns = df.columns.tolist()

with col2:
        st.write("")
        st.write(df.head(len(df)))

with col1:
                # Allow the user to select columns for plotting
        x_axis = st.selectbox('Select the X-axis', options=columns+["None"])
        y_axis = st.selectbox('Select the Y-axis', options=columns+["None"])

        # Create a slider for the x-value
        max_x_value = st.slider("x-values", value = [0, len(df)])
        max_y_value = st.slider("y-values", value = [0, len(df)])

        plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
        # Allow the user to select the type of plot
        plot_type = st.selectbox('Select the type of plot', options=plot_list)

# Remove rows containing "DNF"
#df = df[~df['Time'].str.contains("DNF" or "+")]

# Use the slider value to select the x-values


x_values = df[x_axis][max_x_value[0]:max_x_value[1]]
if y_axis != "None":
    y_values = df[y_axis][max_y_value[0]:max_y_value[1]]

# x_values = GG.loc("No.")
# y_values = GG.iloc("Time")


# Generate the plot
if col3.button('Generate Plot'):
    fig, ax = plt.subplots(figsize=(6, 4))

    if plot_type == 'Line Plot':
        sns.lineplot(x=x_values, y=y_values, ax=ax)
    elif plot_type == 'Bar Chart':
        sns.barplot(x=x_values, y=y_values, ax=ax, edgecolor=None)
    elif plot_type == 'Scatter Plot':
        sns.scatterplot(x=x_values, y=y_values, ax=ax, marker='.', edgecolor=None)
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

    #st.text(np.quantile(y_values,0/4))
    #st.text(np.quantile(y_values,1/4))
    #st.text(np.quantile(y_values,2/4))
    #st.text(np.quantile(y_values,3/4))
    #st.text(np.quantile(y_values,4/4))

# Add a button to export the plot
if col4.button('Export Plot'):
    fig, ax = plt.subplots(figsize=(6, 4))

    if plot_type == 'Line Plot':
        sns.lineplot(x=x_values, y=y_values, ax=ax)
    elif plot_type == 'Bar Chart':
        sns.barplot(x=x_values, y=y_values, ax=ax, edgecolor=None)
    elif plot_type == 'Scatter Plot':
        sns.scatterplot(x=x_values, y=y_values, ax=ax, marker='.', edgecolor=None)
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


    # Save the plot to a temporary file
    tmp_file = 'temp_plot.png'
    fig.savefig(tmp_file)
    plt.close(fig)  # Close the plot to free up memory

    # Render a download link for the plot
    st.markdown(get_binary_file_downloader_html(tmp_file, 'Plot', 'Click here to download the plot as .png'), unsafe_allow_html=True)
    
