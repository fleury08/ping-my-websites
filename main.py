import json
import threading
from websites_pinger import Pinger
from simple_email_sender import EmailSender


def main(_args):
    with open(_args.source, "r", encoding='utf-8') as f:
        _json = json.load(f)
        pingers = [Pinger(w) for w in _json["websites"]]
        emailer = EmailSender(_args.host, _args.port, _args.username, _args.password)
        ping_websites(pingers, _args.delay, emailer)


def ping_websites(pingers, delay, emailer):
    threading.Timer(delay*1.0, ping_websites, [pingers, delay, emailer]).start()
    results = [pinger.ping() for pinger in pingers]
    for result in results:
        if not result.success:
            message = "Address {} not responding".format(result.website["url"])
            print(message)
            emailer.send_email(result.website["email_to"], message, result.response)
        else:
            message = "OK {}".format(result.website["url"])
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

