
def main(_args):
    import json
    from websites_pinger import Pinger
    with open(_args.source, "r", encoding='utf-8') as f:
        _json = json.load(f)
        pingers = [Pinger(w) for w in _json["websites"]]
        ping_websites(pingers, _args.delay)


def ping_websites(pingers, delay):
    import threading
    from simple_email_sender import EmailSender
    threading.Timer(delay*1.0, ping_websites, [pingers, delay]).start()
    results = [pinger.ping() for pinger in pingers]
    for result in results:
        if not result.success:
            EmailSender.send_email(result.website["email_to"], "Error on address {}".format(result.website["url"]))
        else:
            print("OK {}".format(result.website["url"]))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='source with websites to ping', type=str)
    parser.add_argument('--delay', help='delay between pings in secs, 5 minutes default', type=int, default=300)
    args = parser.parse_args()
    main(args)

