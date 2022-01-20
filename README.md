# DHT11 - Raspberry Pi

```sh
$ sudo apt -y update
$ DEBIAN_FRONTEND=noninteractive \
	sudo apt --no-install-recommends -y install \
		build-essential python3.9-dev python3.9-venv

$ python -m venv .venv
$ source .venv/bin/activate
(.venv)$ CFLAGS="-fcommon" pip3 install -r Requirements

(.venv)$ sudo .venv/bin/python3 src/server.py
(.venv)$ FLASK_APP=src/app.py flask run --host=0.0.0.0
```

https://www.mouser.com/datasheet/2/758/DHT11-Technical-Data-Sheet-Translated-Version-1143054.pdf
