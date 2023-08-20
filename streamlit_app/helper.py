
import pandas as pd
def medal_tally(df):
    df = df.drop_duplicates(['Team',"NOC",'Games','Year','City','Sport',"Event","Medal"])
    medal_tally = df.groupby(['region'])[['Gold','Silver','Bronze']].sum().sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def get_country_year_list(df):

    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0,'Overall')

    return years,country

def filter_medal_tally(df,year_selected,country_selected):
    filtered_df = df

    if year_selected != 'Overall':
        filtered_df = filtered_df[filtered_df['Year']==int(year_selected)]
    if country_selected != 'Overall':
        filtered_df = filtered_df[filtered_df['region']==country_selected]

    return filtered_df

def get_medal_tally_title(df,year_selected,country_selected):

    if year_selected=='Overall' and country_selected=='Overall':
        return "Overall Tally"

    if year_selected!='Overall' and country_selected=='Overall':
        return f"Medal Tally in {year_selected} Olympics"
    
    if year_selected=='Overall' and country_selected!='Overall':
        return f"{country_selected} overall Olympics performance"
    
    if year_selected!="overall" and country_selected!="Overall":
        return f"{country_selected} performance in {year_selected} Olympics"
    

def data_over_time(df,column):
    data_over_time = df.drop_duplicates(['Year',column])[['Year']].value_counts().reset_index().sort_values(by='Year')
    data_over_time = data_over_time.rename(columns={'Year':"Edition",0:'Count'})
    return data_over_time

def most_successful_athletes(df,sport):
    sport_df = df.dropna(subset=['Medal'])
    
    
    if sport != 'Overall':
        sport_df = df[df['Sport']==sport]
    
    result_df = sport_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport',"region"]].drop_duplicates()
    result_df = result_df.rename(columns={'index':'Name','Name_x':'Medal_count'}).reset_index(drop=True)
    return result_df

def drop_duplicate_medals(df):
    # removing dupilcates medals from same team, issue discussed in previous line
    cw_df = df.dropna(subset=['Medal'])
    cw_df = cw_df.drop_duplicates(['Team',"NOC",'Games','Year','City','Sport',"Event","Medal"])
    
    return cw_df

def year_wise_medal_tally(df,country):
    cw_df = drop_duplicate_medals(df)
    country_df = cw_df[cw_df['region']==country]
    country_df = country_df.groupby('Year')['Medal'].count().reset_index()
    return country_df

def country_event_heatmap(df,country):
    
    cw_df = drop_duplicate_medals(df)
    country_df = cw_df[cw_df['region']==country]
    country_df = pd.pivot_table(data=country_df,index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return country_df

def most_successful_athletes_in_the_country(df,country):

    country_df = df.dropna(subset=['Medal'])
    country_df = country_df[country_df['region']==country]
    
    result_df = country_df['Name'].value_counts().reset_index().head(10).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport']].drop_duplicates()
    result_df = result_df.rename(columns={'index':'Name','Name_x':'Medal_count'}).reset_index(drop=True)
    return result_df

def get_sports_df_list(athletes_df):
    sports_df_list = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                    'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                    'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                    'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                    'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                    'Tennis', 'Golf', 'Softball', 'Archery',
                    'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                    'Rhythmic Gymnastics', 'Rugby Sevens',
                    'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athletes_df[athletes_df['Sport'] == sport]
        sports_df_list.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    
    return sports_df_list,name


def get_gender_data(athletes_df):
    men = athletes_df[athletes_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women = athletes_df[athletes_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()

    gender_df = men.merge(women,on='Year',how='left')
    gender_df.rename(columns={'Name_x':'Male',"Name_y":'Female'},inplace=True)
    gender_df.fillna(0,inplace=True)
    return gender_df