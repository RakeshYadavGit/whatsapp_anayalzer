import streamlit as st
import helper
import seaborn as sns
from extract import extraction
from preprocessor import date_time, getDatapoint
from helper import fetch_stats
import matplotlib.pyplot as plt
st.sidebar.title("Whatsapp chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a File")
messageBuffer = []
data = []
date, time, author = None, None, None
if uploaded_file is not None:
    decoded_data = uploaded_file.getvalue().decode("utf-8")
    for line in decoded_data.split('\n'):
        if date_time(line):
            if len(messageBuffer) > 0:
                data.append([date, time, author, ' '.join(messageBuffer)])
            messageBuffer.clear()
            date, time, author, message = getDatapoint(line)
            messageBuffer.append(message)
        else:
            messageBuffer.append(line)
    df = extraction(data)

    st.title('Top Statistics')

    user_list = df['user'].unique().tolist()
    user_list.remove(None)
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)
    num_messages, num_words,num_media, num_links = fetch_stats(selected_user, df)

    if st.sidebar.button("Show Analysis"):
       col1, col2, col3, col4 = st.columns(4)
       with col1:
           st.header("Total Messages")
           st.title(num_messages)
       with col2:
           st.header("Total Words")
           st.title(num_words)

       with col3:
           st.header("Total Media Messages")
           st.title(num_media)

       with col4:
           st.header("Total Shared Links")
           st.title(num_links)

           # finding the busiest users in the group(Group level)
       if selected_user == 'Overall':
           st.title('Most Busy Users')
           x, new_df = helper.most_busy_users(df)
           fig, ax = plt.subplots()

           col1, col2 = st.columns(2)

           with col1:
               ax.bar(x.index, x.values, color='red')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)
           with col2:
               st.dataframe(new_df)

               # activity map
       st.title('Activity Map')
       col1, col2 = st.columns(2)

       with col1:
           st.header("Most busy day")
           busy_day = helper.week_activity_map(selected_user, df)
           fig, ax = plt.subplots()
           ax.bar(busy_day.index, busy_day.values, color='purple')
           plt.xticks(rotation='vertical')
           st.pyplot(fig)

       with col2:
           st.header("Most busy month")
           busy_month = helper.month_activity_map(selected_user, df)
           fig, ax = plt.subplots()
           ax.bar(busy_month.index, busy_month.values, color='orange')
           plt.xticks(rotation='vertical')
           st.pyplot(fig)
       # WordCloud
       st.title("Wordcloud")
       df_wc = helper.create_wordcloud(selected_user, df)
       fig, ax = plt.subplots()
       ax.imshow(df_wc)
       st.pyplot(fig)

       # most common words
       most_common_df = helper.most_common_words(selected_user, df)

       fig, ax = plt.subplots()

       ax.barh(most_common_df[0], most_common_df[1])
       plt.xticks(rotation='vertical')

       st.title('Most commmon words')
       st.pyplot(fig)

       # emoji analysis
       emoji_df = helper.emoji_helper(selected_user, df)
       st.title("Emoji Analysis")

       col1, col2 = st.columns(2)

       with col1:
           st.dataframe(emoji_df)
       with col2:
           fig, ax = plt.subplots()
           ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
           st.pyplot(fig)

       # monthly timeline
       st.title("Monthly Timeline")
       timeline = helper.monthly_timeline(selected_user, df)
       fig, ax = plt.subplots()
       ax.plot(timeline['time'], timeline['message'], color='green')
       plt.xticks(rotation='vertical')
       st.pyplot(fig)

       # daily timeline
       st.title("Daily Timeline")
       daily_timeline = helper.daily_timeline(selected_user, df)
       fig, ax = plt.subplots()
       ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
       plt.xticks(rotation='vertical')
       st.pyplot(fig)


       st.title("Weekly Activity Map")
       user_heatmap = helper.activity_heatmap(selected_user, df)
       fig, ax = plt.subplots()
       ax = sns.heatmap(user_heatmap)
       st.pyplot(fig)



