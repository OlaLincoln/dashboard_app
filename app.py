import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components


def main():

    #----------Embed Tablue Dashboard--------------------#
    html_temp = """<div class='tableauPlaceholder' id='viz1613366219180' style='position: relative'><noscript>
    <a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bo&#47;Book1_16133477825310&#47;NationalPerformaceDashboard&#47;1_rss.png' style='border: none' />
    </a></noscript><object class='tableauViz'  style='display:none;'>
    <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
    <param name='embed_code_version' value='3' /> <param name='site_root' value='' />
    <param name='name' value='Book1_16133477825310&#47;NationalPerformaceDashboard' />
    <param name='tabs' value='no' />
    <param name='toolbar' value='yes' />
    <param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Bo&#47;Book1_16133477825310&#47;NationalPerformaceDashboard&#47;1.png' />
     <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' />
     <param name='display_spinner' value='yes' />
     <param name='display_overlay' value='yes' />
     <param name='display_count' value='yes' />
     <param name='language' value='en' />
     <param name='filter' value='publish=yes' /></object></div>
     <script type='text/javascript'> var divElement = document.getElementById('viz1613366219180'); var vizElement = divElement.getElementsByTagName('object')[0]; if ( divElement.offsetWidth > 800 ) { vizElement.style.minWidth='420px';vizElement.style.maxWidth='1080px';vizElement.style.width='100%';vizElement.style.minHeight='587px';vizElement.style.maxHeight='747px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.minWidth='420px';vizElement.style.maxWidth='1080px';vizElement.style.width='100%';vizElement.style.minHeight='587px';vizElement.style.maxHeight='747px';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='1027px';}
     var scriptElement = document.createElement('script');
     scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
      vizElement.parentNode.insertBefore(scriptElement, vizElement); </script>"""
    components.html(html_temp, width=900, height=1000)

    DATA_URL = ('superstoredata.csv')

    # ---------- Loading and Cleaning Dataset--------------#

    @st.cache(persist=True, allow_output_mutation=True)
    def load_data():
        data = pd.read_csv(DATA_URL, parse_dates=[
                           'Order Date', 'Ship Date'])
        data.dropna()
        def lowercase(x): return str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)

        return data

    data = load_data()

    # -----Dataset that can be changed without affecting original.---------#
    data_copy = data

    # --------- Total Sales----------------#
    st.header('See Total Sales by Metric')
    select = st.selectbox(
        'Choose Filter', ['segment', 'category', 'sub-category'])
    seg_sales = pd.DataFrame(
        data_copy.groupby(select).sum()[['sales', 'profit', 'quantity', 'discount']])
    st.write(seg_sales)

    # ------------Sales Trend--------------
    st.header('What is the Overrall Sales Trend')
    data_copy['month year'] = data_copy['order date'].apply(
        lambda x: x.strftime('%Y-%m'))
    df_temp = pd.DataFrame(data_copy.groupby(
        'month year').sum()['sales'].reset_index())
    fig1 = plt.figure(figsize=(16, 5))
    plt.plot(df_temp['month year'], df_temp['sales'], color='#b80045')
    plt.xticks(rotation='vertical', size=8)
    plt.show()
    st.pyplot(fig1)

    # ------------Overrall Profit trend---------------
    st.header(' Overrall Profit Trend')
    df_temp2 = pd.DataFrame(data_copy.groupby(
        'month year').sum()['sales'].reset_index())
    fig2 = plt.figure(figsize=(16, 5))
    plt.plot(df_temp2['month year'], df_temp2['sales'], color='#129CF7')
    plt.xticks(rotation='vertical', size=8)
    plt.show()
    st.pyplot(fig2)

    # ------------Top 10 products---------------
    st.header('Top 10 Products by(Sales, Profit and Quantity )')
    select = st.selectbox(
        'Choose Filter', ['sales', 'profit', 'quantity'])
    prod_tops = pd.DataFrame(data_copy.groupby('product name').sum()['sales'])
    prod_tops.sort_values(by=['sales'], inplace=True, ascending=False)
    prod_tops[:10]

    st.header('The most prefer shipping mode ')
    fig3 = plt.figure(figsize=(10, 8))
    # countplot: Show the counts of observations in each categorical bin using bars
    sns.countplot(x='ship mode', data=data_copy)
    plt.show()
    st.pyplot(fig3)

    if st.checkbox('Show Raw Data', False):
        st.subheader('Raw Data')
        st.write(data)


if __name__ == "__main__":
    main()
