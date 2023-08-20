import streamlit as st
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.figure_factory as ff

df = preprocessor.preprocess()

st.sidebar.title("Olympic Analysis")
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)


if user_menu == 'Medal Tally':
    
    years,country = helper.get_country_year_list(df)
    year_selected = st.sidebar.selectbox("Select Year",years)
    country_selected = st.sidebar.selectbox("Select Country",country)
    filtered_df = helper.filter_medal_tally(df,year_selected,country_selected)
    medal_tally = helper.medal_tally(filtered_df)

    title = helper.get_medal_tally_title(df,year_selected,country_selected)
    st.title(title)
    
    st.dataframe(medal_tally)
    
if user_menu == 'Overall Analysis':
    
    editions = df['Year'].unique().shape[0] -1 
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    cities = df['City'].unique().shape[0]


    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    st.title('Participating Nations over the Years')
    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time,x='Edition',y='Count')
    st.plotly_chart(fig)

    st.title('Events organized over the Years')
    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time,x='Edition',y='Count')
    st.plotly_chart(fig)

    st.title('Athletes participated over the Years')
    athlete_over_time = helper.data_over_time(df,'Name')
    fig = px.line(athlete_over_time,x='Edition',y='Count')
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    events_per_sports = df.drop_duplicates(['Year','Event'])
    event_per_sports = pd.pivot_table(data=events_per_sports,columns='Year',index='Sport',values='Event',aggfunc='count').fillna(0).astype(int)
    ax = sns.heatmap(event_per_sports,annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    
    sports = df['Sport'].unique().tolist()
    sports.sort()
    sports.insert(0,'Overall')
    selected_sport = st.selectbox("Select Sport",sports)
    successful_athletes = helper.most_successful_athletes(df,sport=selected_sport)

    st.table(successful_athletes)

if user_menu == 'Country-wise Analysis':

    country = df['region'].dropna().unique().tolist()
    country.sort()
    selected_country = st.sidebar.selectbox('Select Country',country)
    country_df = helper.year_wise_medal_tally(df,selected_country)
    st.title("Medal Tally Over the years")
    fig = px.line(country_df,x='Year',y='Medal')
    st.plotly_chart(fig)
    
    
    country_pt = helper.country_event_heatmap(df,selected_country)
    if len(country_df)>0:
        st.title(f"{selected_country} excels in following sports")
        fig,ax = plt.subplots(figsize=(20,20))
        ax = sns.heatmap(country_pt,annot=True)
        st.pyplot(fig)
    else:
        st.title(f'{selected_country} has not won any medals')

    st.title(f"Top 10 athletes of {selected_country}")
    top10_athletes_df = helper.most_successful_athletes_in_the_country(df,selected_country)
    st.table(top10_athletes_df)
    

if user_menu == 'Athlete wise Analysis':
    
    
    st.title("Age distribution of medal-winning athletes")

    athletes_df = df.drop_duplicates(subset=['Name','region'])

    x1 = athletes_df['Age'].dropna()
    x2 = athletes_df[athletes_df['Medal']=='Gold']['Age'].dropna()
    x3 = athletes_df[athletes_df['Medal']=='Silver']['Age'].dropna()
    x4 = athletes_df[athletes_df['Medal']=='Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)

    st.plotly_chart(fig)

    sport_df_list, sports = helper.get_sports_df_list(athletes_df)
    fig = ff.create_distplot(sport_df_list, sports, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    st.title("Height vs Weight")
    sports = df['Sport'].dropna().unique().tolist()
    sports.sort()
    selected_sport = st.selectbox('Select Sport',sports)
    fig,ax = plt.subplots(figsize=(10,10))
    athletes_df['Medal'].fillna('No Medal',inplace=True)
    sport_df = athletes_df[athletes_df['Sport']==selected_sport ]

    ax = sns.scatterplot(x=sport_df['Weight'],y=sport_df['Height'],hue=sport_df['Medal'],style=sport_df['Sex'])
    st.pyplot(fig)

    st.title('Men vs Women participation over the Years')
    gender_df = helper.get_gender_data(athletes_df)
    fig = px.line(gender_df,x='Year',y=['Male','Female'])
    st.plotly_chart(fig)