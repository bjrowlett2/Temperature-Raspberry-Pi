from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
	temperature = "Unknown"
	relative_humidity = "Unknown"

	try:
		with open("static/temperature.txt", "r") as stream:
			data = stream.read()
			temperature = float(data.strip())
			temperature = str(round(temperature, 2))

		with open("static/relative_humidity.txt", "r") as stream:
			data = stream.read()
			relative_humidity = float(data.strip())
			relative_humidity = str(round(relative_humidity, 2))
	except:
		pass

	return (f"<html>"
	        f"  <head>"
	        f"    <title>DHT11 - Raspberry Pi</title>"
	        f"  </head>"
	        f"  <body>"
	        f"    <h3>Temperature: {temperature} &deg;F</h3>"
	        f"    <h3>Relative Humidity: {relative_humidity}%</h3>"
	        f"    <script type=\"text/javascript\">"
	        f"      setInterval(() => location.reload(), 15000);"
	        f"    </script>"
	        f"  </body>"
	        f"</html>")
