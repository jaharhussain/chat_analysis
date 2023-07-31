import re
import pandas as pd

def preprocess(data, key):
    split_formats = {
        '12hr': r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][mM]\s-\s',
        '24hr': r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s',
        'custom': ''
    }
    datetime_formats = {
        '12hr': '%d/%m/%Y, %I:%M %p - ',
        '24hr': '%d/%m/%Y, %H:%M - ',
        'custom': ''
    }

    raw_string = data.decode('utf-8')    
    user_msg = re.split(split_formats[key], raw_string)[1:]  # splits at all the date-time pattern, resulting in a list of all the messages with user names
    date_time = re.findall(split_formats[key], raw_string)  # finds all the date-time patterns

    df = pd.DataFrame({'date_time': date_time, 'user_msg': user_msg})  # exporting it to a df

    df['date_time'] = pd.to_datetime(df['date_time'], format=datetime_formats[key])

    # split user and msg
    usernames = []
    msgs = []
    for i in df['user_msg']:
        a = re.split('([\w\W]+?):\s', i)  # lazy pattern match to the first {user_name}: pattern and splitting it, i.e., each msg from a user
        if a[1:]:  # user typed messages
            usernames.append(a[1])
            msgs.append(a[2])
        else:  # other notifications in the group (e.g., someone was added, someone left...)
            usernames.append("group_notification")
            msgs.append(a[0])
    # create new columns
    df['user'] = usernames
    df['message'] = msgs
    df['message_count'] = [1] * df.shape[0]    # helper column to keep a count.

    # drop the old user_msg column
    df.drop('user_msg', axis=1, inplace=True)
    df['day'] = df['date_time'].dt.strftime('%a')
    df['month'] = df['date_time'].dt.strftime('%b')
    df['year'] = df['date_time'].dt.year
    df['date'] = df['date_time'].apply(lambda x: x.date())

    return df
