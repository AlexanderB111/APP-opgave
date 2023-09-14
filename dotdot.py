# Import necessary libraries
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import random

# Function to load the dataset
@st.cache_data  # Cache the function to enhance performance
def load_data():
    # Define the file path
    file_path = 'https://raw.githubusercontent.com/AlexanderB111/APP-opgave/main/wine_market.csv'
    
    # Load the CSV file into a pandas dataframe
    df = pd.read_csv(file_path)

   # Create income groups and add as a new column
    bin_edges = [1893, 1940, 1960, 1980, 1996]
    bin_labels = ['1893-1940', '1940-1960', '1960-1980', '1980-1996']
    df['Age_Group'] = pd.cut(df['Year_Birth'], bins=bin_edges, labels=bin_labels, right=False)

    bin_edges2 = [0, 20, 40, 60, 80,100]
    bin_labels2 = ['0-20', '21-40', '41-60', '61-80','81-100']
    df['Last_Purchase'] = pd.cut(df['Recency'], bins=bin_edges2, labels=bin_labels2, right=False)

    return df

# Load the data using the defined function
df = load_data()

# Set the app title and sidebar header
st.title("Wine 😊📈")
st.sidebar.header("Filters 📊")

# Introduction

# HR Attrition Dashboard
st.image('MicrosoftTeams-image.png')
st.markdown("""
            Welcome to the 'Wine Wonderland' dataset, where every sip is an adventure, and every data point is a grape waiting to tell its story. Just like a fine wine, this dataset has been aged to perfection, with notes of statistics, flavors of features, and a bouquet of insights that will leave you swirling with excitement. Explore the world of wines through the lens of data, and who knows, you might just discover the secret recipe for the world's most data-driven wine tasting party. 
            So, grab your data glasses, toast to the data sommelier, and let's embark on a journey that's as smooth as a silky Pinot Noir and as intriguing as a complex Bordeaux. Cheers to data, insights, and a little wine-induced laughter along the way! 🍷📊🤣""")
with st.expander("📊 **Objective**"):
                 st.markdown("""
At the heart of this dashboard is the mission to visually decode data, which can be usefull to get a deeper understanding of the client base and help the marketing
"""
)

                             
# Tutorial Expander
with st.expander("How to Use the Dashboard 📚"):
    st.markdown("""
    1. **Filter Data** - Use the sidebar filters to narrow down specific data sets.
    2. **Visualize Data** - From the dropdown, select a visualization type to view patterns.
    3. **Insights & Recommendations** - Scroll down to see insights derived from the visualizations and actionable recommendations.
    """)

    # Sidebar filter: Income Group
selected_Year_Birth = st.sidebar.multiselect("Select Age Groups 🕰️", df['Age_Group'].unique().tolist(), default=df['Age_Group'].unique().tolist())
if not selected_Year_Birth:
    st.warning("Please select an income group from the sidebar ⚠️")
    st.stop()
filtered_df = df[df['Age_Group'].isin(selected_Year_Birth)]

# Sidebar filter: Marital Status
MS = df['Marital_Status'].unique().tolist()
selected_MS = st.sidebar.multiselect("Marital Status 🏢", MS, default=MS)
if not selected_MS:
    st.warning("Please select a Marital Status from the sidebar ⚠️")
    st.stop()
filtered_df = filtered_df[filtered_df['Marital_Status'].isin(selected_MS)]

# Sidebar filter: Income Range
min_income = int(df['Income'].min())
max_income = int(df['Income'].max())
income_range = st.sidebar.slider("Select Income Range 💰", min_income, max_income, (min_income, max_income))
filtered_df = filtered_df[(filtered_df['Income'] >= income_range[0]) & (filtered_df['Income'] <= income_range[1])]

    # Sidebar filter: Income Group
selected_Edu = st.sidebar.multiselect("Select Educational Status 🕰️", df['Education'].unique().tolist(), default=df['Education'].unique().tolist())
if not selected_Edu:
    st.warning("Please select an Educational status from the sidebar ⚠️")
    st.stop()
filtered_df = filtered_df[filtered_df['Education'].isin(selected_Edu)]

visualization_option = st.selectbox(
      "Select Visualization 🎨",
    ["Money spent on wine filtered by education",
     "Money spent on wine filtered age groups",
     "Money spent on wine filtered by number of kids",
     "Money spent on wine filtered by number of teens",
     "Which campaign is working",
     "KDE Plot: Amount spent on wine by marital status" ]
)

if visualization_option == "Money spent on wine filtered by education":
     # Bar chart for attrition by age group
    chart = alt.Chart(data=filtered_df).mark_bar().encode(
          x='Education',
          y='count()',
          color= 'Marital_Status'
          ).properties( 
          title='Bought wine dependding on their education'
          )
    st.altair_chart(chart, use_container_width=True)

elif visualization_option == "Which campaign is working":
    columnss_to_melt = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3','AcceptedCmp4','AcceptedCmp5']
    df_melted = pd.melt(filtered_df, value_vars=columnss_to_melt, var_name="Purchase Type", value_name="Count")
    chart = alt.Chart(df_melted).mark_bar().encode(
        x=alt.X('Purchase Type', title='Campaign', axis=alt.Axis(labelAngle=-45)),  
        y=alt.Y('sum(Count):Q', title='Counts'),
        color=alt.Color('Purchase Type:N', legend=None)  
    ).properties(
        title='Purchase Types'
    ).configure_axis(
        labelFontSize=12, titleFontSize=14
    )
    st.altair_chart(chart, use_container_width=True)

if visualization_option == "Money spent on wine filtered age groups":
    # Bar chart for money spent on wine by age group with color and size customization
    chart2 = alt.Chart(data=filtered_df).mark_boxplot().encode(
        x='Age_Group',
        y='MntWines',
        color=alt.Color('Age_Group', scale=alt.Scale(scheme='category20b')),  # Color customization
    ).properties(
        title='Amount of dollars spent on wine by age group',
        width=600,  # Adjust the width of the chart
        height=400,  # Adjust the height of the chart
    )
    st.altair_chart(chart2, use_container_width=True)


elif visualization_option == "KDE Plot: Amount spent on wine by marital status":
    # KDE plot for Distance from Home based on Attrition
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=filtered_df, x='MntWines',hue='Marital_Status', fill=True, palette='Set2')
    plt.xlabel('Amount spent on wine')
    plt.ylabel('Density')
    plt.title('KDE Plot: Amount spent on wine by marital status')
    st.pyplot(plt)

if visualization_option == "Money spent on wine filtered by number of kids":
    # Money spent on wine by number of kids
    fig = sns.catplot(x="Kidhome", y="MntWines", kind='box', data=filtered_df)
    plt.title('Money on wine by number of kids in the household')
    plt.xlabel('Number of kids')
    plt.ylabel('Money spend on wines over 2 years')
    st.pyplot(fig)


if visualization_option == "Money spent on wine filtered by number of teens":
    # Money spent on wine by number of kids
    fig = sns.catplot(x="Teenhome", y="MntWines", kind='box', data=filtered_df)
    plt.title('Money on wine by number of teens in the household')
    plt.xlabel('Number of teens')
    plt.ylabel('Money spend on wines over 2 years')
    st.pyplot(fig)


# Display dataset overview
st.header("Dataset Overview")
st.dataframe(df.describe())

st.sidebar.subheader("Chat")
user_message = st.text_area("User", "Hello, do you wanna hear a joke? 👋")

user_input = st.text_input("Say something")

funny_responses = [
    "Why did the wine refuse to fight the beer? Because it didn't want to get corked!",
    "Why did the grape go to the doctor? Because it was feeling a little winey",
    "Why don't scientists trust atoms? Because they make up everything, just like a good wine!",
]

if st.button("Send"):
    if user_input:
        user_message += f"\nYou: {user_input}"
        st.text_area("User", user_message)

        # Generate a random funny response from the chatbot.
        bot_response = random.choice(funny_responses)
        st.text_area("Chatbot", bot_response)
