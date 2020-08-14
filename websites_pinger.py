class Pinger:

	def __init__(self, _website):
		self.website = _website
		self.success = None
		self._prev_status = None
		self.response = None

	def ping(self, website=None):
		from urllib import request
		_to_ping = website["url"] if website else self.website["url"]
		self._prev_status = self.success
		try:
			self.response = request.urlopen(_to_ping)
			self.success = True
		except Exception:
			self.success = False
		return self

	def status_changed(self):
		if self._prev_status is not None:
			return self._prev_status != self.success
		return False