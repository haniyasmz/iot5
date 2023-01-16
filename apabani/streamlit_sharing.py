'''
Created on 12 Jan 2023

@author: hanimurnizam
'''

import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
# from sqlalchemy import URL
from datetime import datetime, timezone
import time


st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)

# url_object = URL.create(
#     "postgresql+psycopg2",
#     username="postgres",
#     password="rocky99",  # plain (unescaped) text
#     host="localhost",
#     database="smart_hand_sanitizer",
# )



# conn = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user,password,host,port,database))
# except (Exception, Error) as error:
#     print("Error while connecting to PostgreSQL", error)

engine = create_engine("postgresql+psycopg2://postgres:rocky99@localhost/smart_hand_sanitizer")
# ses = sessionmaker(bind=engine)

# conn = engine.raw_connection()
# cursor = conn.cursor()
# cursor = con.cursor()
@st.experimental_singleton
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

# def init_connection():
#     return engine
# conn = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user,password,host,port,database))

# def init_connection():
#     return psycopg2.connect(host='localhost',
#         database='smart_hand_sanitizer',
#         user='postgres',
#         password='rocky99')

# cursor = session.connection().connection.cursor()
    

conn = init_connection()
# conn.autocommit = True

# creating a cursor
# creating a cursor
cursor = conn.cursor()


@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_sql('SELECT * FROM sanitizer_records2', engine)

def get_data2() -> pd.DataFrame:
    return pd.read_sql('SELECT * FROM sanitizer_records3', engine)


SQL_Query = get_data()
SQL_Query2 = get_data2()

st.title("Real-Time / Live IoT Hand Santisier Dispenser")
# top-level filters
# hour_filter = st.selectbox("Select the Hour", pd.unique(SQL_Query["hours"]))
#
# # dataframe filter
# SQL_Query = SQL_Query[SQL_Query["hours"] == hour_filter]
#
# # create three columns
# kpi1, kpi2, kpi3 = st.columns(3)
#
# kpi1.metric(
#     label="Age ⏳",
#     value=round(avg_age),
#     delta=round(avg_age) - 10,
# )
#
# kpi2.metric(
#     label="Married Count 💍",
#     value=int(count_married),
#     delta=-10 + count_married,
# )
#
# kpi3.metric(
#     label="A/C Balance ＄",
#     value=f"$ {round(balance,2)} ",
#     delta=-round(balance / count_married) * 100,
# )



# st.write("My First Streamlit Web App")


#
# df = pd.DataFrame({"one": [1, 2, 3], "two": [4, 5, 6], "three": [7, 8, 9]})
# st.write(df)

# streamlit_app.py

# Initialize connection.

# def init_connection():
#     return psycopg2.connect(**st.secrets["postgres"])

# dataset_url = "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv"

# SQL_Query = pd.read_sql('SELECT id, date, hours FROM sanitizer_records1
df = pd.DataFrame(SQL_Query, columns=['id','date', 'hours'])
df2 = pd.DataFrame(SQL_Query2, columns=['id','date', 'hours'])

st.write("Number of people using Smart Hand Sanitiser")
st.line_chart(df2, x = "date", y="id")
    
st.write("Frequency of Smart Hand Sanitiser used")


frequency = df['hours'].value_counts()
df_val_counts = pd.DataFrame(frequency) 
df_val_counts = df_val_counts.reset_index()
df_val_counts.columns = ['hour', 'frequency']

# frequency_df = df.value_counts().rename_axis('unique_values').to_frame('hours')
# print (df)
# frequency_df = pd.DataFrame()
# st.line_chart(df_val_counts, x = "hour", y="frequency")
# st.line_chart(df, x = "id", y="date")

# df = pd.DataFrame(SQL_Query, columns=['hours', 'date'])
# st.line_chart(df)
#
# df = pd.DataFrame(SQL_Query, columns=['hours'])
st.line_chart(df_val_counts, x = "hour", y="frequency")
# st.area_chart(df_val_counts, x = "hour", y="frequency")
# st.bar_chart(df_val_counts, x = "hour", y="frequency")
frequency_used = len(df['id'])


# # create two columns for charts
# fig_col1, fig_col2 = st.columns(2)
#
# with fig_col1:
#     st.markdown("### First Chart")
#     st.line_chart(df_val_counts, x = "hour", y="frequency")
#     # fig = px.density_heatmap(
#     #     data_frame=df, y="age_new", x="marital"
#     # )
#     # st.write(fig)

# st.line_chart(data=df,x='date', y='hours' )

# conn = psycopg2.connect(
#         host='localhost',
#         database='smart_hand_sanitizer',
#         user='postgres',
#         password='rocky99')
# st.markdown("### Detailed Data View")
# st.dataframe(df)

used_amount = 10
dt = datetime.now(timezone.utc)

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

t = time.localtime()
current_time = time.strftime("%H", t)
# print(current_time)

# inserting values
cursor.execute('INSERT INTO sanitizer_records3 (date, amount_used, hours) VALUES (%s,%s,%s)', (now,used_amount,current_time))
# for i in (time):
#     cursor.execute('INSERT INTO sanitizer_records2 (date, amount_used, hours) VALUES (%s,%s,%s)', (i,used_amount,i[11:13]))

# fetching rows
sql1 = '''select * from sanitizer_records3;'''
cursor.execute(sql1)
for i in cursor.fetchall():
    print(i)

conn.commit()


# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=60)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


rows = run_query("SELECT * from sanitizer_records3;")

st.markdown("### Detailed Data View")
st.dataframe(SQL_Query2)


# creating a single-element container.


# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
    
# exit() 
    
    
    
    
    
    