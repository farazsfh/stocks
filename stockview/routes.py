from flask import render_template, url_for, flash, redirect, request
from stockview import app
from apscheduler.schedulers.background import BackgroundScheduler
from stockview.forms import AddStockForm
import finnhub

configuration = finnhub.Configuration(
    api_key={
        'token': 'TOKEN'
    }
)

finnhub_client = finnhub.DefaultApi(finnhub.ApiClient(configuration))

stock_cards = {}
forex_rates = finnhub_client.forex_rates(base='USD').to_dict()['quote']

app.config['SECRET_KEY'] = 'Qpe55kiRdMWX7Fz2gQUTN0QRHsZ39KKL'


@app.route("/")
@app.route("/stock")
def stock():
    form = AddStockForm()
    return render_template('stock.html', stock_cards=stock_cards, form=form)

@app.route("/forex")
def forex():
    return render_template('forex.html', forex_rates=forex_rates)

@app.route("/updateStocks", methods=["GET", "POST"])
def updateStocks():
    if request.method == 'POST':
        stock_cards[request.form['ticker']] = finnhub_client.quote(request.form['ticker'])
        return redirect(url_for('stock'), code=302)
    else:
        return "Error: no GET requests allowed on this page"

def updateStockPrices():
    for ticker in stock_cards:
        stock_cards[ticker] = finnhub_client.quote(ticker)

def updateForexRates():
    forex_rates = finnhub_client.forex_rates(base='USD').to_dict()['quote']

scheduler = BackgroundScheduler()
job = scheduler.add_job(updateStockPrices, 'interval', seconds=30)
job = scheduler.add_job(updateForexRates, 'interval', seconds=30)
scheduler.start()
