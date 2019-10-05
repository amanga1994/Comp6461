import socket
import argparse
import sys
import urllib.parse
import re



DOMAIN_FORMAT = re.compile(
    r"(?:^(\w{1,255}):(.{1,255})@|^)" # http basic authentication [optional]
    r"(?:(?:(?=\S{0,253}(?:$|:))" # check full domain length to be less than or equal to 253 (starting after http basic auth, stopping before port)
    r"((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+" # check for at least one subdomain (maximum length per subdomain: 63 characters), dashes in between allowed
    r"(?:[a-z0-9]{1,63})))" # check for top level domain, no dashes allowed
    r"|localhost)" # accept also "localhost" only
    r"(:\d{1,5})?", # port [optional]
    re.IGNORECASE
)
SCHEME_FORMAT = re.compile(
    r"^(http|hxxp|ftp|fxp)s?$", # scheme: http(s) or ftp(s)
    re.IGNORECASE
)


def validate_url(url):
    # print("URL:"+url)
    url=url.strip("'")
    # url=url.strip("'")
    # print("URL:" + url)
    url = url.strip()
    if not url:
        raise Exception("No URL specified")

    if len(url) > 2048:
        raise Exception("URL exceeds its maximum length of 2048 characters (given length={})".format(len(url)))

    result = urllib.parse.urlparse(url)
    scheme = result.scheme
    domain = result.netloc

    if not scheme:
        raise Exception("No URL scheme specified")

    if not re.fullmatch(SCHEME_FORMAT, scheme):
        raise Exception("URL scheme must either be http(s) or ftp(s) (given scheme={})".format(scheme))

    if not domain:
        raise Exception("No URL domain specified")

    if not re.fullmatch(DOMAIN_FORMAT, domain):
        raise Exception("URL domain malformed (domain={})".format(domain))
    return url


def key_value_validator(x):
    if not(x.find(":") >= 0):
        raise Exception("Invalid header format")
    else:
        if not (len(x.split(":")[0]) >= 0 and len(x.split(":")[1]) >= 0):
            raise Exception("Invalid header format")
    return x


'''def read_from_file(path):
    out = ""
    try:
        f = open(path, "r")
        out = f.read()
    except Exception as e:
        raise argparse.ArgumentParser(e)'''


'''def write_to_file(file_path, output):
    try:
        f = open(file_path, "a+")
        f.write(output)
        print(f"Output write to file:{file_path}")
        f.close()
    except Exception as e:
        print(e)
        print("Please find below the output:\n" + output)'''


def http_client(host, request):
    # print(request)
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    output = ""
    # conn.settimeout(100000)
    try:
        conn.connect((host, 80))
        # print("Type any thing then ENTER. Press Ctrl+C to terminate")
        # print(ord(" "))
        request = request.encode("utf-8")
        conn.sendall(request)
        while True:
            # MSG_WAITALL waits for full request or error
            response = conn.recv(len(request), socket.MSG_WAITALL)
            if len(response) > 0:
                output += response.decode("utf-8")
            else:
                break
        # print("hi"+output)

        responseCode = ""
        if len(output) > 0:
            responseCode = output.split("\n")[0].split(" ")[1];

        if responseCode[0] == '3':
            # location = reply.split("\r\n")[5].split(": ")[1];
            for i in output.split("\r\n"):
                if i.split(": ")[0] == "Location":
                    location = i.split(": ")[1];

            queryParamIndex = location.index(location.split("/")[3]);
            path = "/" + location[queryParamIndex:len(location)];
            # print("sys", sys.argv)

            if sys.argv[1].lower().find("get") >=0:
                output = http_client(host, get_header(path, args));
                # print("out", output)

            else:
                output = http_client(host, post_header(path, args));
            # final_output = output
        # else:
        #     final_output = output
        return output
    except Exception as e:
        print(e)
        sys.exit()
    finally:
        conn.close()


def implement_help(args):
    #print("help")
    if len(sys.argv) == 3 and args.help_method is not None:
        if args.help_method.lower() == "get":
            print("""
            usage: httpc get [-v] [-h key:value] URL 
            Get executes a HTTP GET request for a given URL. 
            -v Prints the detail of the response such as protocol, status, 
            and headers. 
            -h key:value Associates headers to HTTP Request with the format 
            'key:value'.
            """)
        elif args.help_method.lower() == "post":
            print(""" 
            usage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL 
            Post executes a HTTP POST request for a given URL with inline data or from file. 
            -v Prints the detail of the response such as protocol, status, and headers. 
            -h key:value Associates headers to HTTP Request with the format 'key:value'. 
            -d string Associates an inline data to the body HTTP POST request. 
            -f file Associates the content of a file to the body HTTP POST request. 
            Either [-d] or [-f] can be used but not both.
            """)
    elif len(sys.argv) == 2:
        print("""
            httpc is a curl-like application but supports HTTP protocol only.
            Usage:
                httpc command [arguments] 
                The commands are: 
                get executes a HTTP GET request and prints the response. 
                post executes a HTTP POST request and prints the response. 
                help prints this screen. 
            Use "httpc help [command]" for more information about a command.""")
    else:
        print("Invalid input")


def implement_post(args):
    url = args.URL
    path = urllib.parse.urlparse(url).path
    query = urllib.parse.urlparse(url).query
    host = urllib.parse.urlparse(url).netloc
    if len(query) > 0:
        # print(query)
        if query.lower().find("url") >= 0:
            val = urllib.parse.quote(query[4:])
            query=query[0:4]+val
        else:
            query = urllib.parse.urlencode(urllib.parse.parse_qsl(query))
        # print(path)
        path += "?" + query
    # path +="?"+query

    # print(path)
    reply = http_client(host, post_header(path, args))
    # Redirect functionality starts
    responseCode = ""
    if len(reply) > 0:
        responseCode = reply.split("\n")[0].split(" ")[1];
    # Redirect functionality ends
    final_output = ""
    if args.v:
        final_output = reply
    else:
        if responseCode == '200':
            flag = 0
            for i in reply.split("\r\n"):
                if len(i) == 0:
                    flag = 1
                if flag == 1:
                    final_output += i
        # # Redirect functionality starts
        # elif responseCode == "302":
        #     # location = reply.split("\r\n")[5].split(": ")[1];
        #     for i in reply.split("\r\n"):
        #         if i.split(": ")[0] == "Location":
        #             location = i.split(": ")[1];
        #     queryParamIndex = location.index(location.split("/")[3]);
        #     path = "/" + location[queryParamIndex:len(location)];
        #     reply = http_client(host, post_header(path, args));
        #     final_output = reply
        # # Redirect functionality ends
        else:
            final_output = reply

    if args.o.name != "<stdout>":
        args.o.write(final_output)
    else:
        print(final_output)


def implement_get(args):
    url = args.URL
    path = urllib.parse.urlparse(url).path
    query = urllib.parse.urlparse(url).query
    host = urllib.parse.urlparse(url).netloc
    if len(query) > 0:
        # print(query)
        if query.lower().find("url") >= 0:
            val = urllib.parse.quote(query[4:])
            query = query[0:4] + val
        else:
            query = urllib.parse.urlencode(urllib.parse.parse_qsl(query))
        path += "?" + query
    reply = http_client(host, get_header(path,args))
    # Redirect functionality starts
    responseCode = ""
    if len(reply) > 0:
        responseCode = reply.split("\n")[0].split(" ")[1];
    # Redirect functionality ends
    final_output = ""
    if args.v:
        final_output = reply
    else:
        if responseCode == '200':
            flag = 0
            for i in reply.split("\r\n"):
                if len(i) == 0:
                    flag = 1
                if flag == 1:
                    final_output += i
        # # Redirect functionality starts
        # elif responseCode == "302":
        #     for i in reply.split("\r\n"):
        #         if i.split(": ")[0] == "Location":
        #             location = i.split(": ")[1];
        #     queryParamIndex = location.index(location.split("/")[3]);
        #     path = "/" + location[queryParamIndex:len(location)];
        #     reply = http_client(host, get_header(path, args));
        else:
            final_output = reply

    if args.o.name != "<stdout>":
        args.o.write(final_output)
    else:
        print(final_output)


def get_header(path, args):
    if args.h is None:
        request = f"GET {path} HTTP/1.0\r\nAccept:application/json\r\n\r\n"
    else:
        request = f"GET {path} HTTP/1.0\r\n"
        if "".join("".join(i) for i in args.h).lower().find("accept:") < 0:
            request += "Accept:application/json\r\n"
        for i in args.h:
            request += "".join(i) + "\r\n"
        request += "\r\n"
    return request


def post_header(path, args):
    # print(path)
    if args.h is None:
        request = f"POST {path} HTTP/1.0\r\nAccept:application/json\r\n"
    else:

        request = f"POST {path} HTTP/1.0\r\n"
        if "".join("".join(i) for i in args.h).lower().find("accept") < 0:
            request += "Accept:application/json\r\n"
        for i in args.h:
            request += "".join(i) + "\r\n"
    if args.d is not None:
        if not request.lower().find("content-length:") >= 0:
            request += f"Content-length:{len(args.d)}\r\n"
        request += "\r\n"
        request += args.d + "\r\n\r\n"
    elif args.f.name != "<stdin>":
        if not request.lower().find("content-length:") >= 0:
            filedata = args.f.read()
            request += f"Content-length:{len(filedata)}\r\n"
        request += "\r\n"
        request += f"{filedata}"
        request +="\r\n\r\n"
    else:
        request += "\r\n"
    # print(request)
    return request


# Usage: python echoclient.py --host host --port port
parser = argparse.ArgumentParser(prog="httpc")
subparsers = parser.add_subparsers()

# create the parser for the "help" command
parser_help = subparsers.add_parser('help', aliases=["HELP", "Help"])
parser_help.add_argument('help_method', help='help menu', nargs="?", choices=["get", "GET", "post", "POST"])
parser_help.set_defaults(function=implement_help)

# create the parser for the "get" command
parser_get = subparsers.add_parser('get', add_help=False, aliases=["Get", "GET"])
parser_get.add_argument("-v", "--v", action="store_true", help="Display additional information")
parser_get.add_argument("-h", "--h", action="append", type=key_value_validator, nargs="?", help= "Input headers for the request")
parser_get.add_argument("-o", "--o", type=argparse.FileType('a+'), default=sys.stdout)
parser_get.add_argument("URL", type=str, help="URL for sending request")
parser_get.set_defaults(function=implement_get)


# create the parser for the "post" command
parser_post = subparsers.add_parser('post', add_help=False, aliases=["Post", "POST"])
group = parser_post.add_mutually_exclusive_group()
parser_post.add_argument("-v", "--v", action="store_true", help="Display additional information")
parser_post.add_argument("-h", "--h", action="append", nargs="?", type=key_value_validator, help= "Input headers for the request")
parser_post.add_argument("-o", "--o", type=argparse.FileType('a+'), default=sys.stdout)
group.add_argument("-d", "--d", help="Input data for body from the console")
group.add_argument("-f", "--f",  type=argparse.FileType('r'), default=sys.stdin)
parser_post.add_argument("URL", type=validate_url, help="URL for sending request")
parser_post.set_defaults(function=implement_post)
args = parser.parse_args()
args.function(args)



# http_client(args.host, args.port)