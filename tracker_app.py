#-----------------------------------------------------------------------------------------------------------------------------------------------------
#IMPORTING LIBRARIES
#-----------------------------------------------------------------------------------------------------------------------------------------------------
import pandas as pd
import streamlit as st
import altair as alt #VISUALIAZATIONS
import base64
from PIL import Image
from st_aggrid import GridOptionsBuilder, AgGrid
#import webbrowser
import os
#import streamlit_theme as stt
#import streamlit.components.v1 as components
import urllib.request
from bs4 import BeautifulSoup
import yfinance as yf

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#MAKING WIDE MODE DEFAULT
#-----------------------------------------------------------------------------------------------------------------------------------------------------
def do_stuff_on_page_load():
    st.set_page_config(layout="wide")
do_stuff_on_page_load()

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#ADDING MAIN (TITLE) IMAGE
#-----------------------------------------------------------------------------------------------------------------------------------------------------
image = Image.open('pics/Project3.jpg')

st.image(image, use_column_width=True)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#STOCK INDEX TRACKER: BUILDING A FUNCTION TO CALL STOCK PRICES APIS FOR STOCK INDEXES IN NSE
#-----------------------------------------------------------------------------------------------------------------------------------------------------
st.write("""
# Stock Index Tracker
""")


def stocks(index):
    L=0
    import requests

    url = "https://latest-stock-price.p.rapidapi.com/price"

    querystring = {"Indices":index}

    headers = {
        "X-RapidAPI-Host": "latest-stock-price.p.rapidapi.com",
        "X-RapidAPI-Key":  st.secrets["apikey"] #API_key
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()

    L=len(response)

    #print(response)

    #CREATING A LIST TO STORE THE COLLECTED DATA FROM API
    stockdata=[] #emptying
    for i in range(0,L):
        data={'TICKER': response[i]['symbol'],
              #'identifier': response[i]['identifier'],
              'OPEN': response[i]['open'],
              'DAY\'S HIGH': response[i]['dayHigh'],
              'DAY\'S LOW': response[i]['dayLow'],
              'LAST PRICE': response[i]['lastPrice'],
              'PREVIOUS CLOSE': response[i]['previousClose'],
              'CHANGE': response[i]['change'],
              '% CHANGE': response[i]['pChange'],
              'TOTAL TRADED VOLUME': response[i]['totalTradedVolume'],
              #'TOTAL TRADED VALUE': response[i]['totalTradedValue'],
              'LAST UPDATE TIME': response[i]['lastUpdateTime'],
              'YEAR HIGH': response[i]['yearHigh'],
              'YEAR LOW': response[i]['yearLow'],
              '% CHANGE 365D': response[i]['perChange365d'],
              '% CHANGE 30D': response[i]['perChange30d'],

             }
        #print(data)
        stockdata.append(data)
    #print(stockdata)

    #CREATING A DATAFRAME TO STORE THE LIST AND TRANSFORM
    stockdata_df = pd.DataFrame() #emptying
    stockdata_df = pd.DataFrame(stockdata)
    stockdata_df['% FROM YEAR HIGH'] = ((stockdata_df['LAST PRICE'] - stockdata_df['YEAR HIGH'] )/stockdata_df['LAST PRICE'] )*100
    stockdata_df=stockdata_df.round(2)
    stockdata_df['% FROM YEAR LOW'] = ((stockdata_df['LAST PRICE'] - stockdata_df['YEAR LOW'] )/stockdata_df['LAST PRICE'] )*100
    stockdata_df=stockdata_df.round(2)
    stockdata_df=stockdata_df[[c for c in stockdata_df if c not in ['LAST UPDATE TIME']]
       + ['LAST UPDATE TIME']]
    return(stockdata_df)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#STOCK INDEX TRACKER: CREATING A SELECTION WIDGET
#-----------------------------------------------------------------------------------------------------------------------------------------------------
indexes = st.selectbox(
     'Select the market index for latest data: ',
     ('NIFTY 50', 'NIFTY NEXT 50', 'NIFTY 100','NIFTY 200','NIFTY 500', 'NIFTY MIDCAP 50','NIFTY MIDCAP 100','NIFTY MIDCAP 150',
     'NIFTY SMALLCAP 50', 'NIFTY SMALLCAP 100','NIFTY SMALLCAP 250', 'NIFTY BANK',
     'NIFTY AUTO', 'NIFTY FMCG', 'NIFTY IT', 'NIFTY ENERGY', 'NIFTY PHARMA', 'NIFTY PSU BANK', 'NIFTY PVT BANK'))

df=stocks(indexes) #Python calls the function but doesn't save the result in any variable. That is why you got the error.

test = df

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#STOCK INDEX TRACKER: USING AGGRID TO DISPLAY THE DATA FRAME TO ENABLE FILTERING ON STREAMLIT APP
#-----------------------------------------------------------------------------------------------------------------------------------------------------
gb = GridOptionsBuilder.from_dataframe(test)
#gb.configure_side_bar()
gridOptions = gb.build()

# from AgGrid Documentations and other discussions
AgGrid(test,theme='streamlit', gridOptions=gridOptions,
    fit_columns_on_grid_load=False,enable_enterprise_modules=True,
    height=500,
    reload_data=True)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#STOCK INDEX TRACKER: CREATING A DOWNLOAD BUTTON FOR DOWNLOADING THE INDEX DATA
#-----------------------------------------------------------------------------------------------------------------------------------------------------
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806

def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(test)

st.download_button(
     label="Download Market Index data as CSV",
     data=csv,
     file_name='Indexdata.csv',
     mime='text/csv',
 )
#-----------------------------------------------------------------------------------------------------------------------------------------------------
                                                               #SECTION BREAK USING IMAGES
#-----------------------------------------------------------------------------------------------------------------------------------------------------
st.write("")
st.write("")
cola, colb, colc = st.columns([1,6,1])

with cola:
    st.write("")

with colb:
    st.image("pics/dots.png")

with colc:
    st.write("")

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#WATCHLISTS: BUILDING A FUNCTION TO LINK THE IMAGES TO GOOGLE SHEETS CONTAINING CUSTOM MADE WATCHLIST (USED ST.COLUMNS)
#-----------------------------------------------------------------------------------------------------------------------------------------------------
st.write("""
# Watchlists
""")

# from streamlit discussions
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}">
            <img src="data:image/{img_format};base64,{bin_str}" />
        </a>'''
    return html_code

# USING ST.COLUMNS TO DISPLAY WATCHLISTS IN 3 COLUMN SECTIONS
col1, col2, col3 = st.columns(3)

with col1:
    #st.header("A cat")
    gif_html = get_img_with_href('pics/mne4.png', 'https://docs.google.com/spreadsheets/d/1MlSYpuwSn4mjwXLSpPyGgWRFHD1bWp1KhcvBKkS2ZL8/edit?usp=sharing')
    st.markdown(gif_html, unsafe_allow_html=True)
    st.write("""
    > Companies that are __leaders__ in their respective sectors with no or very few competitors. Companies that provide __essential/necessary__ products and services.
    (with GOOGLE FINANCE API in Sheets)""")

with col2:
    gif_html = get_img_with_href('pics/hdy.png', 'https://docs.google.com/spreadsheets/d/12c9C5D5PXhEV6yxhYwkwMu7-h_B9q5-lpKKP_Rb4htU/edit?usp=sharing')
    st.markdown(gif_html, unsafe_allow_html=True)
    st.write("""
    > Stocks that have been __consistently__ paying out dividend.
    """)

with col3:
    gif_html = get_img_with_href('pics/vs.png', 'https://docs.google.com/spreadsheets/d/1Gb-1oktSWFO3j89dE2JD0OrNyecNonicAqzgTt2WZTA/edit?usp=sharing')
    st.markdown(gif_html, unsafe_allow_html=True)
    st.write("""
    > Stocks that have __high ROA, low debt__ and __good EPS.__
    """)
#-----------------------------------------------------------------------------------------------------------------------------------------------------
                                                               #SECTION BREAK USING IMAGES
#-----------------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#CREATING CUSTOM FONT STYLES
#-----------------------------------------------------------------------------------------------------------------------------------------------------
# #https://discuss.streamlit.io/t/how-to-link-a-button-to-a-webpage/1661/2

#https://python.plainenglish.io/three-tips-to-improve-your-streamlit-app-a4c94b4d2b30
st.markdown(""" <style> .font1 {
font-size:25px ; font-family: 'Sans serif'; color: #0EBEB7; text-decoration: none;}
</style> """, unsafe_allow_html=True)
#st.markdown('<p class="font">Guess the object Names</p>', unsafe_allow_html=True)

st.markdown(""" <style> .font2 {
font-size:18px ; font-family: 'Sans serif'; color: #0EBEB7; text-decoration: none;}
</style> """, unsafe_allow_html=True)
cola, colb, colc = st.columns([1,6,1])

with cola:
    st.write("")

with colb:
    st.image("pics/dots.png")

with colc:
    st.write("")



#-----------------------------------------------------------------------------------------------------------------------------------------------------
#CHARTS: USING YAHOO FINANCE API TO CREATE 2 MAJOR INDEX CHARTS FOR LAST 5 YEARS
#-----------------------------------------------------------------------------------------------------------------------------------------------------
st.write("""
# Charts
""")

#-----------------------------------------------------------------------------------------------------------------------------------------------------NIFTY 50
ticker0 = ('^NSEI')
start0 = pd.to_datetime('2022-01-01')
end0 = pd.to_datetime('today')
index1_list0 = yf.download(ticker0, start0, end0)['Adj Close']
# to get the latest value
last_element = index1_list0[-1]

st.markdown('#### **NIFTY 50**: <span class="font1">{}</span>'.format(last_element), unsafe_allow_html=True)

ticker1 = ('^NSEI')

start = st.date_input('Start for Nifty 50', value = pd.to_datetime('2022-01-01'), min_value=pd.to_datetime('2017-01-01'),max_value=pd.to_datetime('2022-01-01'))
end = pd.to_datetime('today')
# for calculating %change
index1_list = yf.download(ticker1, start, end)['Adj Close']
last_element = index1_list[-1]
first_element = index1_list[0]
pchg=round(((last_element-first_element)/first_element)*100,2)

st.markdown('**NIFTY 50** has since changed by: <span class="font2">{}%</span>'.format(pchg), unsafe_allow_html=True)


#st.write(index1_list)
index1_df = pd.DataFrame(index1_list)
index1_df['time']=index1_df.index

# displaying in 2 different configurations based on the time and price changes
if start<pd.to_datetime('2022-01-01'):
    #https://altair-viz.github.io/user_guide/data.html
    c1=alt.Chart(index1_df).mark_line().encode(
    x=('time'),
    y=alt.Y('Adj Close',scale=alt.Scale(domain=[7000, 19500]))
    ).properties(
        width=1370,
        height=500
    ).configure_axis(
        grid=False)
    st.altair_chart(c1)

else:
    #https://altair-viz.github.io/user_guide/data.html
    c1=alt.Chart(index1_df).mark_line().encode(
    x=('time'),
    y=alt.Y('Adj Close',scale=alt.Scale(domain=[14000, 19500]))
    ).properties(
        width=1370,
        height=500
    ).configure_axis(
        grid=False)
    st.altair_chart(c1)
#-----------------------------------------------------------------------------------------------------------------------------------------------------NIFTY BANK
ticker00 = ('^NSEBANK')
start00 = pd.to_datetime('2022-01-01')
end00 = pd.to_datetime('today')
index1_list00 = yf.download(ticker00, start00, end0)['Adj Close']
last_element = round(index1_list00[-1],2)


st.markdown('#### **NIFTY BANK**: <span class="font1">{}</span>'.format(last_element), unsafe_allow_html=True)

ticker_bn = ('^NSEBANK')

start_bn = st.date_input('Start for Bank Nifty', value = pd.to_datetime('2022-01-01'), min_value=pd.to_datetime('2017-01-01'),max_value=pd.to_datetime('2022-01-01'))
end = pd.to_datetime('today')

index1_list = yf.download(ticker_bn, start_bn, end)['Adj Close']
last_element = index1_list[-1]
first_element = index1_list[0]
pchg=round(((last_element-first_element)/first_element)*100,2)

st.markdown('**NIFTY BANK** has since changed by: <span class="font2">{}%</span>'.format(pchg), unsafe_allow_html=True)


#st.write(index1_list)
index1_df = pd.DataFrame(index1_list)
index1_df['time']=index1_df.index
#st.dataframe(index1_df)
if start_bn<pd.to_datetime('2022-01-01'):
    #https://altair-viz.github.io/user_guide/data.html
    c1=alt.Chart(index1_df).mark_line().encode(
    x=('time'),
    y=alt.Y('Adj Close',scale=alt.Scale(domain=[14000, 42500]))
    ).properties(
        width=1370,
        height=500
    ).configure_axis(
        grid=False)
    st.altair_chart(c1)

else:
    #https://altair-viz.github.io/user_guide/data.html
    c1=alt.Chart(index1_df).mark_line().encode(
    x=('time'),
    y=alt.Y('Adj Close',scale=alt.Scale(domain=[32000, 42500]))
    ).properties(
        width=1370,
        height=500
    ).configure_axis(
        grid=False)
    st.altair_chart(c1)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
                                                               #SECTION BREAK USING IMAGES
#-----------------------------------------------------------------------------------------------------------------------------------------------------
st.write("")
st.write("")
cola, colb, colc = st.columns([1,6,1])

with cola:
    st.write("")

with colb:
    st.image("pics/dots.png")

with colc:
    st.write("")

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#INDICATORS
#-----------------------------------------------------------------------------------------------------------------------------------------------------
st.write("""
# Indicators
""")

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#INDICATORS: 1) VIX: WEB SCRAPED DATA FOR CURRENT, CHANGE PER DAY, OPEN, PREVIOUS CLOSE DATA
#            2) Moving Average (MA), Technical Indicators, MA Crossovers for NIFTY 50: WEB SCRAPED DATA
#-----------------------------------------------------------------------------------------------------------------------------------------------------
col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    * VIX Indicator
    """)
    url3="https://www.moneycontrol.com/indian-indices/india-vix-36.html"
    dfda1 = pd.read_html(url3)
    df2=dfda1[1].append(dfda1[0])
    df2.columns=['VIX']
    df3 = (df2['VIX'].str.extract(r'(?P<Overview>.*?)(?P<VIX>\d+(?:\.\d+)?)')
                     .applymap(str.strip))
    df4=df3.loc[(df3['Overview']=='Open') | (df3['Overview']=='Previous Close')]
    ovr0=(df4['Overview'][0])
    vix0=(df4['VIX'][0])
    ovr1=(df4['Overview'][1])
    vix1=(df4['VIX'][1])

    page = urllib.request.urlopen(url3)
    soup = BeautifulSoup(page, "lxml")
    vixrecent=soup.find('div', {'class' :'pcstkspr nsestkcp bsestkcp futstkcp optstkcp'}).text
    c=soup.find("div", {"id": "stick_ch_prch"}).text
    st.markdown('### VIX: <span class="font1">{}</span> | Change: <span class="font1">{}</span> \n ### {}: <span class="font1">{}</span> | {}: <span class="font1">{}</span>'.format(vixrecent,c,ovr0,vix0,ovr1,vix1), unsafe_allow_html=True)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
with col4:

    st.markdown("""
    * Moving Average (MA), Technical Indicators, MA Crossovers for NIFTY 50
    """)

    url4="https://www.moneycontrol.com/indian-indices/nifty-50-9.html"
    dfdb1 = pd.read_html(url4)

    dfdb1[2].columns=['Trend','Daily Indicators']
    dfdb1[5].columns=['Trend1','Weekly Indicators']
    dfdb1[8].columns=['Trend2','Monthly Indicators']
    dfdi1=dfdb1[2]
    dfdi2=dfdb1[5]
    dfdi3=dfdb1[8]
    dfdi4=pd.concat([dfdi1, dfdi2, dfdi3], axis=1)
    #dfdi4
    dfdi4.drop(dfdi4.columns[[4, 2]], axis = 1, inplace = True)

    def color_positive_green(val):
        """
        Takes a scalar and returns a string with
        the css property `'color: green'` for positive
        strings, black otherwise.
        """

        if val == 'Bullish':
            color =  '#ADFF2F'
        elif val == 'Very Bullish':
            color = '#228B22'
        elif val == 'Bearish':
            color = 'red'
        elif val == 'Very Bearish':
            color =  '#a20d44'
        elif val == 'Neutral':
            color =  '#2189d2'
        else:
            color = 'white'
        return 'color: %s' % color

    st.table(dfdi4.style.applymap(color_positive_green))




#-----------------------------------------------------------------------------------------------------------------------------------------------------
#INDICATORS: 3) ECONOMIC INDICATORS: WEB SCRAPED DATA OF INDIAN ECONOMY
#-----------------------------------------------------------------------------------------------------------------------------------------------------
st.markdown("""
* Economic Indicators
""")

url2="https://tradingeconomics.com/india/indicators"
dfda = pd.read_html(url2)
df1=dfda[0]
df1.columns = ['Indicators', 'Last', 'Previous', 'Units', 'Latest Update']
df1=df1.astype({"Last": float, "Previous": float})
df1=df1.round({'Last':2,'Previous':2})
st.table(df1.style.format({'Last': '{:.2f}', 'Previous': '{:.2f}'}))

#-----------------------------------------------------------------------------------------------------------------------------------------------------
                                                               #SECTION BREAK USING IMAGES
#-----------------------------------------------------------------------------------------------------------------------------------------------------
st.write("")
st.write("")
cola, colb, colc = st.columns([1,6,1])

with cola:
    st.write("")

with colb:
    st.image("pics/dots.png")

with colc:
    st.write("")

#-----------------------------------------------------------------------------------------------------------------------------------------------------
                                                               #ADDING LINKS
#-----------------------------------------------------------------------------------------------------------------------------------------------------
gif_html = get_img_with_href('pics/github-32.png', 'https://github.com/s1dewalker/NSE_Tracker_App')
st.markdown(gif_html, unsafe_allow_html=True)
st.markdown("")
gif_html = get_img_with_href('pics/linkedin-32.png', 'http://www.linkedin.com/in/sujay-bhaumik-d12')
st.markdown(gif_html, unsafe_allow_html=True)
st.markdown("")
gif_html = get_img_with_href('pics/gmail-32.png', 'mailto:sujaybhk99@gmail.com')
st.markdown(gif_html, unsafe_allow_html=True)
st.markdown("")
gif_html = get_img_with_href('pics/tableau-32.png', 'https://public.tableau.com/app/profile/sujay.bahumik#!/?newProfile=&activeTab=0')
st.markdown(gif_html, unsafe_allow_html=True)
