import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns



st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Upload a chat data file", type=["txt"])
if uploaded_file is not None:
    file_contents = uploaded_file.read()
    #key = st.radio("Select the date-time format", ("12hr", "24hr", "custom"))
    #if st.button("Preprocess"):
    df = preprocessor.preprocess(file_contents, '12hr')
    st.dataframe(df)


    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show analysis"):
        num_messages,words,num_media,num_links = helper.fetch_stats(selected_user,df)
     
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media)
        with col4:
            st.header("Links Shared")
            st.title(num_links)










        #finding busiest users in the grp

        if selected_user == "Overall":
            st.title("Most Busy Users")
            x,new_df = helper.most_busy_users(df)
            fig,ax = plt.subplots()
            
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index,x.values,color = 'red')
                plt.xticks(rotation = 45)
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df.head(8))
        st.title("Word Cloud")
        df_wc = helper.create_wc(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        return_df = helper.most_common_words(selected_user,df)
        st.title('Most Common Words')
        fig,ax = plt.subplots()
        ax.barh(return_df[0],return_df[1],color = 'red')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df.head(4))
        with col2:
            plt.figure(figsize=(15, 6))
            plt.rcParams['font.size'] = 15

            sns.set_style("darkgrid")
            fig, ax = plt.subplots()


            sns.barplot(x = emoji_df.emoji_count,y = emoji_df.emoji_description, palette = "Paired_r")

            st.pyplot(fig)

        grouped_by_time = helper.hourmap(selected_user,df)
        plt.rcParams['font.size'] = 16
        plt.rcParams['figure.figsize'] = (20, 8)

    # Beautifying Default Styles using Seaborn
        sns.set_style("darkgrid")

    # PLOT: grouped by hour
        sns.barplot(grouped_by_time.hour, grouped_by_time.message_count)
        fig,ax = plt.subplots()
        st.title('Most Active Hours');
        st.pyplot(fig)
