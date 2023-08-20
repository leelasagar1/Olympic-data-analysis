import pandas as pd

def read_data():
    df = pd.read_csv('data/athlete_events.csv')
    regions_df = pd.read_csv('data/noc_regions.csv')
    return df,regions_df

def preprocess():
    df,regions_df = read_data()
    df = df.drop_duplicates()
    df = df[df['Season']=='Summer']
    df.loc[df['NOC']=='SGP','NOC'] = 'SIN'
    df=df.merge(regions_df,on='NOC',how='left')
    df = pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    return df