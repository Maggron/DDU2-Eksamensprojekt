import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set the page config
st.set_page_config(page_title='Bögh',
                   layout='centered',
                   page_icon='📊')

# Title
st.title('📊  Bögh')

# Specify the folder where your CSV files are located
uploaded_file = st.file_uploader("Upload a CSV file", type=['csv'])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, delimiter=';')

    col1, col2 = st.columns(2)

    columns = df.columns.tolist()

    with col2:
        st.write("")
        st.write(df.head(100))

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
df = df[~df['Time'].str.contains("DNF")]

# Use the slider value to select the x-values
x_values = df[x_axis][:max_x_value]


# Generate the plot
if st.button('Generate Plot'):
    fig, ax = plt.subplots(figsize=(6, 4))

    if plot_type == 'Line Plot':
        sns.lineplot(x=x_values, y=df[y_axis][:max_x_value], ax=ax)
    elif plot_type == 'Bar Chart':
        sns.barplot(x=x_values, y=df[y_axis][:max_x_value], ax=ax)
    elif plot_type == 'Scatter Plot':
        sns.scatterplot(x=x_values, y=df[y_axis][:max_x_value], ax=ax)
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