import time
import RPi.GPIO as GPIO

class Dht11:
	def __init__(self, pin):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

		self._pin = pin
		self.temperature_c = 0.0
		self.temperature_f = 0.0
		self.relative_humidity = 0.0

	def poll_data(self):
		GPIO.setup(self._pin, GPIO.OUT)
		GPIO.output(self._pin, GPIO.HIGH)
		time.sleep(0.1)

		GPIO.output(self._pin, GPIO.LOW)
		time.sleep(0.018)

		GPIO.output(self._pin, GPIO.HIGH)

		last_value = GPIO.HIGH
		transitions = [last_value]
		timestamp = time.monotonic()
		GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		while time.monotonic() - timestamp < 0.25:
			if GPIO.input(self._pin) != last_value:
				last_value = not last_value
				transitions.append(time.monotonic())

		if len(transitions) < 81:
			raise Exception("Not enough data received")

		if len(transitions) % 2 == 0:
			raise Exception("Invalid parity data recevied")

		data = []
		start = max(1, len(transitions) - 81)
		for i in range(start + 1, len(transitions), 2):
			delta = transitions[i] - transitions[i - 1]
			data.append(GPIO.LOW if delta < 0.000051 else GPIO.HIGH)

		bytes = []
		for i in range(0, 40, 8):
			bytes.append(self._decode_data(data, i, i + 8))

		check = 0
		for i in range(len(bytes) - 1):
			check += bytes[i]

		if check & 0xFF != bytes[4]:
			raise Exception("Mismatched integrity checksum")

		self.temperature_c = bytes[2] + bytes[3] / 256
		self.temperature_f = (9 / 5) * self.temperature_c + 32
		self.relative_humidity = bytes[0] + bytes[1] / 256

	def _decode_data(self, data, start, stop):
		result = 0
		for i in range(start, stop):
			result = (result << 1) | data[i]
		return result

pin = 6
device = Dht11(pin)
while True:
	try:
		time.sleep(1)
		device.poll_data()

		timestamp = int(time.time())
		temperature = device.temperature_f
		relative_humidity = device.relative_humidity

		print(f"Temperature: {temperature}")
		print(f"Relative Humidity: {relative_humidity}")

		with open("static/temperature.txt", "w") as stream:
			stream.write(f"{temperature}")

		with open("static/relative_humidity.txt", "w") as stream:
			stream.write(f"{relative_humidity}")

		with open("static/temperature_and_humidity.log", "a") as stream:
			stream.write(f"{timestamp},{temperature},{relative_humidity}\n")

		time.sleep(30)
	except:
		pass
