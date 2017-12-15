from flask import Flask, render_template, request, redirect, url_for
import os
import requests
import pandas as pd
import json
from bokeh.plotting import figure, output_notebook, output_file, show, save, reset_output
from bokeh.embed import components

app = Flask(__name__)

app.vars = {}

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('stock_template.html')
    else:
        #request was a POST
        app.vars['tick_name'] = request.form['ticker_name']
        url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?ticker='+app.vars['tick_name']+'&date.gt=2010-01-01&qopts.columns=date,close,adj_close&api_key=HS5YecSeHt4-kfPLMuff'
        r = requests.get(url)
        r_new = r.json()
        r_list = r_new['datatable']['data']
        labels = ['date','close','adj_close']
        df = pd.DataFrame(r_list, columns=labels)
        df_last_month = df.iloc[-1:-22:-1,0:3]
        df_last_month['date'] = pd.to_datetime(df_last_month['date'])
        if request.form['closing'] ==  'closing_price':
            p = figure(title='Closing Stock Price for '+app.vars['tick_name']+' over Last Month', x_axis_label='Date', y_axis_label='Price (Dollars)',x_axis_type="datetime")
            p.line(df_last_month['date'],df_last_month['close'],color="blue")
            p.circle(df_last_month['date'],df_last_month['close'],color="red")
            script, div = components(p)
            return redirect('/price_plot')
        else:
            p = figure(title='Adj. Closing Stock Price for '+app.vars['tick_name']+' over Last Month', x_axis_label='Date', y_axis_label='Price (Dollars)',x_axis_type="datetime")
            p.line(df_last_month['date'],df_last_month['adj_close'],color="blue")
            p.circle(df_last_month['date'],df_last_month['adj_close'],color="red")
            script, div = components(p)
            return redirect('/price_plot')
    
@app.route('/price_plot', methods=['GET','POST']) 
def price_plot():
    return render_template('stock_price.html', script=script, div=div)

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
   

#port=33507
