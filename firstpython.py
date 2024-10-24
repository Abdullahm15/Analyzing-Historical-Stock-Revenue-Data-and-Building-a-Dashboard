!pip install yfinance
!pip install bs4
!pip install nbformat
import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
ticker = yf.Ticker('TSLA')
tesla_data = ticker.history(period = 'max')
tesla_data.head()
tesla_data.reset_index(inplace = True)
tesla_data.head()
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
html_data = requests.get(url).text
soup = BeautifulSoup(html_data, 'html5lib')
tables = soup.find_all('table')
table_index = None
for index, table in enumerate(tables):
    if "Tesla Quarterly Revenue" in str(table):
        table_index = index
        break
if table_index is not None:
    rows = []
    for row in tables[table_index].tbody.find_all('tr'):
        col = row.find_all('td')
        if col != []:
            date = col[0].text.strip()
            revenue = col[1].text.strip()
            rows.append({'Date': date, 'Revenue': revenue})
    tesla_revenue = pd.DataFrame(rows, columns=['Date', 'Revenue'])
tesla_revenue
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$', "", regex=True)
tesla_revenue
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
tesla_revenue.tail(5)
gamestop = yf.Ticker('GME')
gme_data = gamestop.history(period = 'max')
gme_data.reset_index(inplace = True)
gme_data.head()
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
html_data_2 = requests.get(url).text
soup = BeautifulSoup(html_data_2, "html5lib")
gme_revenue = pd.DataFrame(columns=['Date','Revenue'])

rows = []
for row in tables[table_index].tbody.find_all('tr'):
    col = row.find_all('td')
    if col:
        date = col[0].text
        revenue = col[1].text
        rows.append({'Date': date, 'Revenue': revenue})

gme_revenue = pd.concat([gme_revenue, pd.DataFrame(rows)], ignore_index=True)

gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$', "", regex=True)
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

gme_revenue
gme_revenue.tail(5)
make_graph(tesla_data, tesla_revenue, 'Tesla')

make_graph(gme_data, gme_revenue, 'GameStop')
