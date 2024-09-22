import pandas as pd
import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv(r"Education Level.csv")

# Add a new column that extracts the text after the last "/"
df['Extracted_Text'] = df['refArea'].apply(lambda x: x.split('/')[-1])

q1 = df['PercentageofEducationlevelofresidents-illeterate'].quantile(0.25)
q3 = df['PercentageofEducationlevelofresidents-illeterate'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

df_filtered = df[(df['PercentageofEducationlevelofresidents-illeterate'] >= lower_bound) &
                 (df['PercentageofEducationlevelofresidents-illeterate'] <= upper_bound)]

# Add a new column that extracts the text after the last "/"
df['Extracted_Text'] = df['refArea'].apply(lambda x: x.split('/')[-1])

# Sidebar filters for interactivity
st.sidebar.header("Filter Options")
selected_regions = st.sidebar.multiselect("Select Regions", options=df['Extracted_Text'].unique(), default=df['Extracted_Text'].unique())
selected_metric = st.sidebar.selectbox("Select Metric", 
                                       options=['PercentageofEducationlevelofresidents-illeterate', 
                                                'PercentageofEducationlevelofresidents-university',
                                                'PercentageofSchooldropout'], 
                                       index=1)

# Filter the data based on user selection
df_filtered = df[df['Extracted_Text'].isin(selected_regions)]

# Title and introduction
st.title("Education and Dropout Rates Analysis")
st.write("This page provides an interactive exploration of education and school dropout rates across various regions. "
         "Use the filters on the sidebar to select specific regions and metrics of interest.")

# Visualization 1: Bar Chart (Grouped)
st.subheader("Bar Chart: University Education vs Illiteracy Rate by Region")
fig1 = px.bar(df_filtered, x='Extracted_Text', y=['PercentageofEducationlevelofresidents-university', 
                                                  'PercentageofEducationlevelofresidents-illeterate'], 
              barmode='group', labels={'value': 'Percentage (%)'})
st.plotly_chart(fig1)

st.write("### Insights:")
st.write("- This grouped bar chart allows for a comparison of university education levels and illiteracy rates across different regions.")
st.write("- Regions with higher university education levels tend to have lower illiteracy rates, providing insights into educational disparities.")

# Visualization 2: Box Plot
st.subheader("Box Plot: School Dropout Rate by Region")
fig2 = px.box(df_filtered, x='Extracted_Text', y='PercentageofSchooldropout', 
              labels={'PercentageofSchooldropout': 'School Dropout Rate (%)'})
st.plotly_chart(fig2)

st.write("### Insights:")
st.write("- The box plot shows the distribution of school dropout rates by region.")
st.write("- Outliers indicate regions with particularly high dropout rates, which may need further investigation.")

# Footer and public access link information
st.write("### Conclusion:")
st.write("The interactive visualizations above offer key insights into the educational dynamics across regions. Using the filters, you can customize the analysis and uncover deeper patterns related to university education, illiteracy, and dropout rates.")

st.write("**Note**: The app is accessible via a public link.")
