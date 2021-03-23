import random
from flask import Flask, render_template
import data

app = Flask(__name__)


@app.route('/')
def render_main():
    attrib_sort = random.choice(['price', 'nights', 'date', 'title'])
    hotels = sorted([[data.tours[tour_id][attrib_sort], tour_id] for tour_id in data.tours])[0:6]
    hotels = dict([(hotel[1], data.tours[hotel[1]]) for hotel in hotels])
    return render_template('index.html', title=data.title, subtitle=data.subtitle, description=data.description,
                           departures=data.departures, hotels=hotels)


@app.route('/departures/<departure>/')
def render_departures(departure):
    if departure not in data.departures:
        return render_template('str_404.html', title=data.title, subtitle=data.subtitle, description=data.description,
                               departures=data.departures, error='Такого пункта вылета нет.')
    hotels = dict([(hotel_id, hotel) for hotel_id, hotel in data.tours.items() if hotel["departure"] == departure])
    price_hotels = sorted([hotel_item["price"] for hotel_id, hotel_item in hotels.items()])
    nights_hotels = sorted([hotel_item["nights"] for hotel_id, hotel_item in hotels.items()])
    param_departures = [price_hotels[0], price_hotels[-1], nights_hotels[0], nights_hotels[-1]]
    return render_template('departure.html', title=data.title, departure=departure, departures=data.departures,
                           hotels=hotels, param_departures=param_departures)


@app.route('/tours/<int:tour_id>/')
def render_tours(tour_id):
    if tour_id not in data.tours:
        return render_template('str_404.html', title=data.title, subtitle=data.subtitle, description=data.description,
                               departures=data.departures, error='Такого отеля в списке нет.')
    return render_template('tour.html', title=data.title, departures=data.departures, tour=data.tours[tour_id])


@app.errorhandler(404)
def render_not_found(error):
    return render_template('str_404.html', title=data.title, subtitle=data.subtitle, description=data.description,
                           departures=data.departures, error=error)


if __name__ == '__main__':
    app.run()
