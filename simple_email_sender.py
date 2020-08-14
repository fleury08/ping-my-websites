class EmailSender:

	def __init__(self, host: str, port: int, user: str=None, password: str=None):
		import smtplib
		self._client = smtplib.SMTP(host, port)
		if user and password:
			self._client.starttls()
			self._client.login(user, password)

	def send_email(self, send_to, subject, message, send_from=""):
		from email.message import EmailMessage
		msg = EmailMessage()
		msg['Subject'] = subject
		msg['To'] = send_to
		msg['From'] = send_from
		msg.set_content(message)
		self._client.sendmail(msg["From"], msg["To"], msg.as_string())
