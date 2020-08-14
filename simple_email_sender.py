class EmailSender:
	def __init__(self):
		pass

	@staticmethod
	def send_email(send_to, message):
		print("EMAIL ON THE WAY -> {}\n\twith message -> {}".format(send_to, message))
