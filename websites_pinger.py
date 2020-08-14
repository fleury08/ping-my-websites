class Pinger:

	def __init__(self, _website):
		self.website = _website
		self.success = False
		self.response = None

	def ping(self, website=None):
		from urllib import request
		from urllib import error
		_to_ping = website["url"] if website else self.website["url"]
		try:
			self.response = request.urlopen(_to_ping)
			self.success = True
		except Exception:
			self.success = False
		return self
