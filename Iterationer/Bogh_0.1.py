# import streamlit as st
# import pandas as pd
from SortData import PlottableTime, PlottableTimeIndexes

SmallestAcceptableTime = 2 # in seconds 

# st.title('Title')
# st.write(len(PlottableTime),len(PlottableTimeIndexes))    


# st.button('Hit me')


# st.line_chart(PlottableTime)

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd 
from SortData import ConvertedArray, ExludeJunk

def Sortandexlude(DF):
    ConvertedTimesIndexes = []
    ConvertedTimes = []

    PlottableTimeIndexes = []
    PlottableTime = []
    
    ConvertedArray(DF)
    
    ExludeJunk(ConvertedTimes,ConvertedTimesIndexes)
    
    return PlottableTime, PlottableTimeIndexes
 


st.title("Streamline Graph App")

# Create a button to trigger graph plotting
show_graph = st.checkbox(":100:",True)

# If the checkbox is checked, show the graph
if show_graph:
    st.line_chart(PlottableTime[:st.slider("max",0,len(PlottableTime),20000,2000)])
    
st.markdown('<div style="font-size: 40px; text-align: center">Welcome to Bögh!</div>', 
unsafe_allow_html=True)
    # Load the .csv file
csv_file = st.file_uploader("Upload a CSV file", type=['csv'])
if csv_file is not None:
    data = pd.read_csv(csv_file, sep=";" ,dtype=str, usecols=["No.", "Time"]
                        )
    st.text(data)
    #print(Sortandexlude(data))
