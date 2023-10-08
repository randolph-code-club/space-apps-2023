from flask import Flask, render_template, request, make_response, redirect
from dotenv import load_dotenv
import os.path
import os
import uuid
from flask import Flask
from dotenv import load_dotenv
import os
from data import get_eclipse

# Load the .env file and populate DATABASE_URL
load_dotenv()

# Define the configuration for the Flask app
class BaseConfig(object):
    DEBUG = False
    TESTING = False

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(BaseConfig)

class Game:
	def __init__(self):
		self.key = None
		self.status = None

	def new(self):
		self.key = str(uuid.uuid4())
		self.status = "new"
		return self

	def save(self, resp):
		resp.set_cookie('game_key', self.key)
		resp.set_cookie('game_status', self.status)

	def end(self, resp):
		self.status = "end"
		resp.set_cookie('game_key', '')
		resp.set_cookie('game_status', self.status)

	def load(self, request):
		self.key = request.cookies.get('game_key')
		self.status = request.cookies.get('game_status')
		return self


@app.route("/")
def index():
	game = Game().load(request)
	if game.key is None or game.key == '':
		return render_template("index.html")
	else:
		return redirect("/game/{}".format(game.key))
	
@app.route("/quit", methods = ['POST'])
def quit():
	game = Game().load(request)
	resp = make_response(render_template("end.html"))
	game.end(resp)
	return resp

@app.route("/game/new", methods = ['POST'])
def new_game():
	game = Game().new()
	resp = make_response(redirect("/game/{}".format(game.key)))
	game.save(resp)
	return resp

@app.route("/game/<string:key>", methods = ['POST', 'GET'])
def play(key):
	game = Game().load(request)
	eclipse = get_eclipse()
	if key != game.key:
		# TODO stop them from stealing another game
		pass
	else:
		if request.method == "GET":
			resp = make_response(render_template("balls.html", game=game, eclipse=eclipse))
			game.save(resp)
			return resp
		elif request.method == "POST":
			form_data = request.form
			new_status = form_data["status"]
			if new_status == "end":
				resp = make_response(render_template("end.html"))
				game.end(resp)
				return resp
			else:
				game.status = new_status
				resp = make_response(render_template("balls.html", game=game, eclipse=eclipse))
				game.save(resp)
				return resp


if __name__ == "__main__":
	app.run()
