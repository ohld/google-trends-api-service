import datetime
from pytrends.request import TrendReq
from flask import Flask, jsonify, Response

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
        year_start=week_before.year, month_start=week_before.month, day_start=week_before.day, hour_start=week_before.hour, 
        year_end=today.year, month_end=today.month, day_end=today.day, hour_end=today.hour, 
        cat=0, geo='', gprop='', sleep=0
    )
    # Remove duplicates
    data = data.loc[~data.index.duplicated(keep='first')]
    
    return Response(data[trend].to_json(), mimetype="text/json")

if __name__ == '__main__':
    app.run(debug=True)