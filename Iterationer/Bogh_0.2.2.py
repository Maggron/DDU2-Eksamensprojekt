import streamlit as st
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

# Import the Bögh icon
icon = Image.open("Bögh_transparent.png")

# Set the page config
st.set_page_config(page_title = 'Bögh',
                   layout = 'centered',
                   page_icon = icon)

# Title
st.title('Bögh')

# Specify the folder where your CSV files are located
uploaded_file = st.file_uploader("Upload a .CSV file", type=['csv'])
if uploaded_file is not None:
    # Try reading with ',' as the delimiter
    df = pd.read_csv(uploaded_file, delimiter=',')
    columns = df.columns.tolist()

    # If the number of columns equals 2, try again with ';' as the delimiter
    if len(columns) <= 2:
        uploaded_file.seek(0)  # Reset the file pointer to the beginning
        df = pd.read_csv(uploaded_file, delimiter=';')
        columns = df.columns.tolist()

    #if 'Time' in df.columns:
        #df = df[~df['Time'].str.contains("DNF" or "+")]
        #df['Time'] = pd.to_timedelta(df['Time']).dt.total_seconds()


    col1, col2 = st.columns(2)

    with col2:
        st.write("")
        st.write(df.head(len(df)))

    with col1:
        # Create a slider for the x-value
        max_x_value = st.slider("max x-value", value = [0, len(df)])
        max_y_value = st.slider("max y-value", value = [0, len(df)])

        # Allow the user to select columns for plotting
        x_axis = st.selectbox('Select the X-axis', options=columns+["None"])
        y_axis = st.selectbox('Select the Y-axis', options=columns+["None"])

        plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
        # Allow the user to select the type of plot
        plot_type = st.selectbox('Select the type of plot', options=plot_list)

# Remove rows containing "DNF"


# Use the slider value to select the x-values
x_values = df[x_axis][max_x_value[0]:max_x_value[1]]
y_values = df[y_axis][max_y_value[0]:max_y_value[1]]

# Generate the plot
if st.button('Generate Plot'):
    fig, ax = plt.subplots(figsize=(6, 4))

    if plot_type == 'Line Plot':
        sns.lineplot(x=x_values, y=y_values, ax=ax)
    elif plot_type == 'Bar Chart':
        sns.barplot(x=x_values, y=y_values, ax=ax)
    elif plot_type == 'Scatter Plot':
        sns.scatterplot(x=x_values, y=y_values, ax=ax)
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