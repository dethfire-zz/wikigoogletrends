import pandas as pd
import requests
import json
from pytrends.request import TrendReq
import streamlit as st
import matplotlib.pyplot as plt
import string

st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown("""
<style>
.big-font {
    font-size:50px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<p class="big-font">Wiki and Google Trends</p>
<p>Compare Wikipedia Search and Google Search Trends. 3 month range available for Wiki. 12 Month for Google because 3 month view is always a rollercoaster.</p>
<b>Directions: </b></ br><ol>
<li>Try to be concise and specific. Wiki doesn't handle disambiguation and variations well. Think entity names.</li>
</ol>
""", unsafe_allow_html=True)

with st.form("data"):
    query = st.text_input('Enter your keyword','ie - Olympic Games')
    submitted = st.form_submit_button("Process")

    if submitted:
        query1 = string.capwords(query)
        query = string.capwords(query)
        query = query.replace(" ","_")

        url = f'https://en.wikipedia.org/w/api.php?action=query&prop=pageviews&titles={query}&format=json'
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        getjson = json.loads(response.text)

        df = pd.DataFrame(columns = ['Date', 'Hits'])

        for k,item in getjson['query']['pages'].items():
          for k,item in item['pageviews'].items():
            data = {'Date': k, 'Hits': item}
            df = df.append(data, ignore_index=True)
            
        df.plot(kind='line', x='Date', y='Hits')
        
        
        st.title("Wiki Pageviews 3 Month")
        plt.xticks(rotation = 15)
        st.pyplot()
        #df.plot.line(x='Date',y='Hits',ylabel='Views',figsize=(10,5),title='Wiki PageView Trend for Python')


        pytrends = TrendReq(hl='en-US', tz=360)
        kw_list = [query1]
        pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='', gprop='')
        df2 = pytrends.interest_over_time()
        
        df2.plot(kind='line')
        
        st.title("Google Trend 12 Month")
        plt.xticks(rotation = 15)
        st.pyplot()
        #df2.plot.line(ylabel='Views',figsize=(10,5),title='Google Trends for Python')
st.write('Author: [Greg Bernhardt](https://twitter.com/GregBernhardt4) | Friends: [Rocket Clicks](https://www.rocketclicks.com), [importSEM](https://importsem.com) and [Physics Forums](https://www.physicsforums.com)')

