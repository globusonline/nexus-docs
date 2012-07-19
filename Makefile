
.PHONY: docs
docs: api.html

api.html: api.restdown
	./vendor/python/bin/python vendor/restdown/bin/restdown -b brand/ api.restdown

api.restdown: vendor/python/lib/python2.7/site-packages/pystache/__init__.py
	./vendor/python/bin/python sample.py

vendor/python/lib/python2.7/site-packages/pystache/__init__.py: vendor/python/bin/pip
	PIP_DOWNLOAD_CACHE=vendor/cache ./vendor/python/bin/pip install -r requirements.txt

vendor/python/bin/pip: vendor/virtualenv.py
	virtualenv --distribute vendor/python

vendor/virtualenv.py:
	curl -o vendor/virtualenv.py https://raw.github.com/pypa/virtualenv/master/virtualenv.py 


.PHONY: clean
clean:
	rm -f api.restdown
	rm -f api.html
	rm -f api.json
