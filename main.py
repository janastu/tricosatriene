from flask import Flask
from flask_cors import CORS
from tricosatriene import TricoServer
import logging
import json

def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--bind", dest="address",
                      help="Binds an address to listen")
    parser.add_option("--mongodb-host", dest="mongodb_host",
                      help="MongoDB host", default="localhost")
    parser.add_option("--mongodb-port", dest="mongodb_port",
                      help="MongoDB port", default=27017)
    parser.add_option("-d", "--database", dest="database",
                      help="MongoDB database name", default="trico")
    parser.add_option('-p', '--prefix', dest="url_prefix", 
                      help="URL Prefix in API pattern", default="")
    parser.add_option('-s', '--sort-keys', dest="sort_keys", default=True,
                       help="Should json output have sorted keys?")
    parser.add_option('--compact-json', dest="compact_json", default=False,
                       help="Should json output have compact whitespace?")
    parser.add_option('--indent-json', dest="indent_json", default=2, type=int,
                       help="Number of spaces to indent json output")
    parser.add_option('--json-ld', dest="json_ld", default=True,
                       help="Should return json-ld media type instead of json?")
    parser.add_option('--debug', dest="debug", default=True)

    options, args = parser.parse_args()

    host, port = (options.address or 'localhost'), 8080
    if ':' in host:
        host, port = host.rsplit(':', 1)

    # make booleans
    debug = options.debug in ['True', True, 1]
    sort_keys = options.sort_keys in ['True', True, '1']
    compact_json = options.compact_json in ['True', True, '1']
    jsonld = options.json_ld in ['True', True, '1']

    mr = TricoServer(
        host=options.mongodb_host,
        port=options.mongodb_port,
        database=options.database,
        sort_keys=sort_keys,
        compact_json=compact_json,
        indent_json=options.indent_json,
        url_host = "http://%s:%s" % (host, port),
        url_prefix=options.url_prefix,
        json_ld=jsonld
    )

    app = mr.get_flask_app()
    CORS(app)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
    app.logger.addHandler(ch)
    app.logger.setLevel(logging.DEBUG)
    app.run(host=host, port=port, debug=debug)


def wsgi():
    with open('config.json') as f:
        data = f.read()
    conf = json.loads(data)
    ms = TricoServer(**conf)
    return ms.get_flask_app()


if __name__ == '__main__':
    main()
else:
    application = wsgi()
