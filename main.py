import json
import threading
from websites_pinger import Pinger
from simple_email_sender import EmailSender


def main(_args):
    with open(_args.source, "r", encoding='utf-8') as f:
        _json = json.load(f)
        _pingers = [Pinger(w) for w in _json["websites"]]
        _emailer = EmailSender(_args.host, _args.port, _args.username, _args.password)
        threading.Thread(target=ping_websites, args=(_pingers, _args.delay, _emailer)).start()


def ping_websites(pingers, delay, emailer: EmailSender):
    import datetime
    threading.Timer(delay*1.0, ping_websites, [pingers, delay, emailer]).start()
    results = [pinger.ping() for pinger in pingers]
    for result in results:
        if result.status_changed():
            message = "[{}] Address {} status has changed to {}".format(datetime.datetime.now(), result.website["url"], "RUNNING" if result.success else "NOT RESPONDING")
            print(message)
            emailer.send_email(result.website["email_to"], message, result.response.getcode())
        else:
            message = "[{}] Status of {} is still {}".format(datetime.datetime.now(), result.website["url"], "RUNNING" if result.success else "NOT RESPONDING")
            print(message)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='source with websites to ping', type=str)
    parser.add_argument('--delay', help='delay between pings in secs, 5 minutes default', type=int, default=300)
    parser.add_argument('--host', help='hostname of smtp mail server', type=str, default="localhost")
    parser.add_argument('--port', help='port of smtp mail server', type=int, default=25)
    parser.add_argument('--username', help='username for authentication', type=str)
    parser.add_argument('--password', help='password for authentication', type=str)

    args = parser.parse_args()
    main(args)

