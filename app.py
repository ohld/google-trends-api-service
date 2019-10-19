import datetime
from pytrends.request import TrendReq
from flask import Flask, jsonify

# create the application object
app = Flask(__name__)

pytrends = TrendReq(hl='en-US', tz=360)


@app.route('/')
def home():
    return "Call /<trend> to get last week Google Trend numbers"

@app.route('/<trend>')
def get_trend(trend):
    today = datetime.datetime.today()
    week_before = today - datetime.timedelta(days=7)

    data = pytrends.get_historical_interest(
        [trend], 
        year_start=week_before.year, month_start=week_before.month, day_start=week_before.day, hour_start=0, 
        year_end=today.year, month_end=today.month, day_end=today.day, hour_end=0, 
        cat=0, geo='', gprop='', sleep=0
    )

    return jsonify(data[trend].to_json())

if __name__ == '__main__':
    app.run(debug=True)