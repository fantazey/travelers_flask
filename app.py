from flask import Flask
from flask_restful import Api, Resource, reqparse
from db_adapter import get_place_list, get_place, add_place

app = Flask(__name__)
api = Api(app)
place_parser = reqparse.RequestParser()
place_parser.add_argument('name', required=True)
place_parser.add_argument('details', required=False)
place_parser.add_argument('longitude', type=float, required=True)
place_parser.add_argument('latitude', type=float, required=True)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('/favicon.ico')


@app.route('/js/<path:path>')
def js(path):
    return app.send_static_file('js/' + path)


@app.route('/css/<path:path>')
def css(path):
    return app.send_static_file('css/' + path)


class Place(Resource):
    def get(self, place_id):
        place = get_place(place_id)
        return place


class PlaceList(Resource):
    def get(self):
        place_list = get_place_list()
        return place_list

    def post(self):
        place = place_parser.parse_args()
        place_id = add_place(place)
        return get_place(place_id)


api.add_resource(PlaceList, '/api/places')
api.add_resource(Place, '/api/places/<place_id>')

if __name__ == '__main__':
    app.run()
