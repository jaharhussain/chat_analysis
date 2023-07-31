from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import re


extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
            df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media = df[df['message']=="<Media omitted>\n"].shape[0]

    links = []

    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media,len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts() / df.shape[0]) * 100,2).reset_index().rename(columns = {'index':'name','user':'percent'})
    return x,new_df

def create_wc(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
             if word not in stop_words:
                  y.append(word)
        return " ".join(y)

    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]     
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
         for word in message.lower().split():
              if word not in stop_words:
                   words.append(word)


    return_df = pd.DataFrame(Counter(words).most_common(20)) 
    return return_df


def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emoji_ctr = Counter()
    emojis_list = ["😀", "😃", "😄", "😁", "😆", "😅","😂","🤣","❤️","🙃","😭","😒"]  # Add more emojis to the list as needed
    r = re.compile('|'.join(re.escape(p) for p in emojis_list))

    for idx, row in df.iterrows():
        emojis_found = r.findall(row["message"])
        for emoji_found in emojis_found:
            emoji_ctr[emoji_found] += 1
    top10emojis = pd.DataFrame()
    # top10emojis = pd.DataFrame(data, columns={"emoji", "emoji_description", "emoji_count"}) 
    top10emojis['emoji'] = [''] * 10
    top10emojis['emoji_count'] = [0] * 10
    top10emojis['emoji_description'] = [''] * 10

    i = 0
    for item in emoji_ctr.most_common(10):
        # will be using another helper column, since during visualization, the emojis won't be rendered.
        description = emoji.demojize(item[0])[1:-1]    # using `[1:-1]` to remove the colons ':' at the end of the demojized strin

        # appending top 10 data of emojis.  # Loading into a DataFrame.
        top10emojis.emoji[i] = item[0]
        top10emojis.emoji_count[i] = int(item[1])
        top10emojis.emoji_description[i] = description
        i += 1

    return top10emojis



