import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# this is setting for the page, so that charts, tables sab beech me dikhne ki bajay wide poore page pe dikhe
st.set_page_config(layout = 'wide', page_title='Startup Analysis')

# st.title('')
df = pd.read_csv('cleaned_data.csv')

df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year.fillna(0).astype(int)
df['month'] = df['date'].dt.month.fillna(0).astype(int)

# df.shape

st.sidebar.title("Startup Funding Analysis")


# method for overall analysis
def load_overall_details():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.subheader(':blue[Total invested]')
        total = round(df['amount'].sum())
        st.metric('Total ', str(total) + ' crs')
    with col2:
        st.subheader(':green[Maximum Invested]')
        maximum = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('Maximum', str(maximum)+' crs')
    with col3:
        st.subheader(':yellow[Average invested]')
        avg = round(df.groupby('startup')['amount'].sum().mean())
        st.metric('Average', str(avg) + ' crs')
    with col4:
        st.subheader(':orange[Total funded Startups]')
        total_startup = df['startup'].nunique()
        st.metric('Total funded startups', str(total_startup))

    # another selectbox for total no of investor invested and total amount invested in the startups
    selected_option = st.selectbox('Select One', ['Total', 'Count'])
    if selected_option == 'Total':
        temp = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp['x-axis'] = temp['year'].astype(str) + '-' + temp['month'].astype(str)
    fig, ax = plt.subplots()
    # custom_colors2 = ['pink', 'lavender', 'grey', 'blue']
    # line chart
    ax.plot(temp['x-axis'], temp['amount'])
    st.pyplot(fig)


# method for startup details
def load_startup_details(selected_startup):

    st.subheader(":blue[Startup Name: ] "+ f":red[{selected_startup}] :rocket:")
    col1, col2 = st.columns(2)

    with col1:
        try:
            st.subheader('%age of Amount invested in Verticals: ')
            month_on_month = df[df['startup'].str.contains(selected_startup)].groupby('vertical')['amount'].sum()
            fig, ax = plt.subplots()
            custom_colors2 = ['pink', 'lavender', 'grey', 'blue']
            ax.pie(month_on_month, labels=month_on_month.index, autopct="%0.01f%%", colors=custom_colors2)
            st.pyplot(fig)
        except:
            st.write('Not invested in any sector')

    with col2:
        try:
            st.subheader('%age of Amount invested in Cities: ')
            cities = df[df['startup'].str.contains(selected_startup)].groupby('city')['amount'].sum()
            fig1, ax1 = plt.subplots()
            custom_colors2 = ['Green', 'skyblue', 'lavender', 'pink']
            ax1.pie(cities, labels=cities.index, autopct="%0.01f%%", colors=custom_colors2)
            st.pyplot(fig1)
        except:
            st.write('Not invested in any city')

    st.subheader(':green[_Top investor:_]')
    top_investor = df[df['startup'].str.contains(selected_startup)].groupby('investors')['amount'].sum().sort_values(
        ascending=False).reset_index().head(1)
    st.write(f":orange[{top_investor.iloc[0]['investors']}]")


# method for investor details
def investor_details(investor):
    st.title("Investor Name: "+ investor)

#     here we are loading their recent investment
    st.subheader(':Blue[Most recent investments: ]')
    recentinvestment = (df[df['investors'].str.contains(investor)].head()
                 [['date', 'startup', 'vertical', 'city', 'round', 'amount']])

    st.dataframe(recentinvestment)

    col1, col2 = st.columns(2)
    with col1:
        #highest investment
        try:
            st.subheader('Biggest Investments:')
            higher_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
                ascending=False).head(6)

            # st.dataframe(higher_series)

           #  ham yahan ek bar chart banayenge jisme x axis pe series ka index matlab startup ka name wala column hoga aur
           #  y axis pe uski values matlab amount in crores show karega
           #
           #  st.pyplot kaise kam karta hai --> matplolib ki documentation se milega
           #  last me access karne ke liye higher_series.index and .values ka use karna hai aur bar ki zagah histogram banana chaho toh name and arguments change hogi bas


            custom_colors = ['blue', 'lightblue', 'lavender', 'grey', 'purple']
            fig1, ax1 = plt.subplots()
            ax1.bar(higher_series.index, higher_series.values, color = custom_colors)

            st.pyplot(fig1)
        except ValueError:
            print('N/A')
    with col2:
        try:
            st.subheader('Areas invested in: ')
            areas = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
            fig2, ax2 = plt.subplots()
            custom_colors2 = ['pink', 'lavender', 'grey', 'blue']
            ax2.pie(areas, labels=areas.index, autopct="%0.01f%%", colors = custom_colors2)
            st.pyplot(fig2)
        except ValueError:
            print('N/A')

    col3, col4 = st.columns(2)

    with col3:
        try:
            st.subheader('Cities: ')
            City = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
            fig3, ax3 = plt.subplots()
            ax3.pie(City, labels=City.index, autopct="%0.01f%%")
            st.pyplot(fig3)
        except ValueError:
            print('N/A')

    with col4:

        try:
            st.subheader('Investment Round')
            rounds = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
            fig4, ax4 = plt.subplots()
            ax4.pie(rounds, labels=rounds.index, autopct="%0.01f%%")
            st.pyplot(fig4)
        except ValueError:
            print('N/A')

    st.subheader('Year on Year Investment')

    year = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    fig5, ax5 = plt.subplots()
    ax5.plot(year.index, year.values)
    st.pyplot(fig5)


option = st.sidebar.selectbox("Select One", ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    # btn0=st.sidebar.button("Overall Analysis")
    st.subheader("Overall Analysis")

    load_overall_details()

elif option == 'Startup':

    # st.title(':red[click on the startup name to know the insights]')

    selected_startup = st.sidebar.selectbox('Select One', sorted(df['startup'].unique()))

    btn1 = st.sidebar.button('Find startup details')
    if btn1:
        st.title("Startup Analysis")
        load_startup_details(selected_startup)
else:
    selected_investor = st.sidebar.selectbox('Select One', sorted(set((df['investors'].str.split(',').sum()))))
    btn2 = st.sidebar.button('Find investor details')
    if btn2:
        investor_details(selected_investor)


