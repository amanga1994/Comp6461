import socket
import argparse
import sys
import urllib.parse


def uri_validator(x):
    try:
        result = urllib.urlparse(x)
        return all([result.scheme, result.netloc, result.path])
    except Exception as e:
        print(e)
        sys.exit()
        return False


def read_from_file(path):
    out=""
    try:
        f = open(path, "r")
        out = f.read()
        return True, out
    except Exception as e:
        out = e
        return False, out


def write_to_file(file_path, output):
    try:
        f = open(file_path,"a+")
        f.write(output)
        print(f"Output write to file:{file_path}")
        f.close()
    except Exception as e:
        print(e)
        print("Please find below the output:\n"+output)


def http_client(host, request):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    output = ""
    try:
        conn.connect((host, 80))
        print("Type any thing then ENTER. Press Ctrl+C to terminate")
        print(ord(" "))
        request = request.encode("utf-8")
        conn.send(request)
        while True:
            # MSG_WAITALL waits for full request or error
            response = conn.recv(len(request), socket.MSG_WAITALL)
            if len(response) > 0:
                output += response.decode("utf-8")
            else:
                break
        return output
    finally:
        conn.close()


def implement_help():
    parser.add_argument("help_for", nargs="?", help="get help for", choices=["get", "post", "GET", "POST"])
    args = parser.parse_args()
    if len(sys.argv) == 3 and args.help_for is not None:
        if args.help_for.lower() == "get":
            print("get help")
        elif args.help_for.lower() == "post":
            print("post help")
    elif len(sys.argv) == 2:
        print("program help")
    else:
        print("Invalid input")


def implement_post():
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("-v", "--v", action="store_true", help="Display additional information")
    parser.add_argument("-h", "--h", action="append", nargs="+", help="Input headers for the request")
    parser.add_argument("-o", "--o", help="Output data to file")
    group.add_argument("-d", "--d", help="Input data for body from the console")
    group.add_argument("-f", "--f", help="Input data for body from the file")
    parser.add_argument("URL", help="URL for sending request")
    args = parser.parse_args()
    url = args.URL
    if uri_validator(url):
        print("valid")
        start = url.find("/")
        n = 3
        while start >= 0 and n > 1:
            start = url.find(url, start + len("/"))
            n -= 1
            """if URL.find("?") >= 0:
                path = URL.substring(start, URL.find())
            else:
                path = URL.substring(start, len(URL))"""
        path = url.substring(start, len(url))
        start_path = start
        path = urllib.parse.quote(path)
        start = url.find("/")
        n = 2
        while start >= 0 and n > 1:
            start = url.find(url, start + len("/"))
            n -= 1
        host = url.substring(start+1, start_path)

        if args.h is None:
            request = f"GET {path} HTTP/1.0\r\nAccept:application/json\r\n\r\n"
        else:
            request = f"GET {path} HTTP/1.0\r\n"
            if "".join("".join(i) for i in args.h).lower().find("Accept") < 0:
                request += "Accept:application/json\r\n"
            for i in args.h:
                request += "".join(i)+"\r\n"
            request += "\r\n"
        if args.d is not None and args.f is not None:
            print("-d and -f both are not allowed in the same command")
            sys.exit()
        elif args.d is not None:
            request += args.d+"\r\n\r\n"
        else:
            read_successful, output = read_from_file(args.f)
            if read_successful:
                request += output+"\r\n\r\n"
            else:
                print(output)
                sys.exit()
        reply = http_client(host, request)
        final_output = ""
        if args.v:
            final_output = reply
        else:
            if str.find("200 OK"):
                flag = 0
                for i in reply.split("\r\n"):
                    if len(i) == 0:
                        flag = 1
                    if flag == 1:
                        final_output += i
            else:
                final_output = reply
        if args.o is not None:
            write_to_file(args.o, final_output)
        else:
            print(final_output)
    else:
        print("Please enter valid URL")


def implement_get():
    parser.add_argument("-v", "--v", action="store_true", help="Display additional information")
    parser.add_argument("-h", "--h", action="append", nargs="+", help="Input headers for the request")
    parser.add_argument("-o", "--o", help="Output data to file")
    parser.add_argument("URL", help="URL for sending request")
    print(parser.parse_args())
    args = parser.parse_args()
    url = args.URL
    if uri_validator(url):
        print("valid")
        start = url.find("/")
        n = 3
        while start >= 0 and n > 1:
            start = url.find(url, start + len("/"))
            n -= 1
            """if URL.find("?") >= 0:
                path = URL.substring(start, URL.find())
            else:
                path = URL.substring(start, len(URL))"""
        path = url.substring(start, len(url))
        start_path = start
        path = urllib.parse.quote(path)
        start = url.find("/")
        n = 2
        while start >= 0 and n > 1:
            start = url.find(url, start + len("/"))
            n -= 1
        host = url.substring(start+1, start_path)

        if args.h is None:
            request = f"GET {path} HTTP/1.0\r\nAccept:application/json\r\n\r\n"
        else:
            request = f"GET {path} HTTP/1.0\r\n"
            if "".join("".join(i) for i in args.h).lower().find("Accept") < 0:
                request += "Accept:application/json\r\n"
            for i in args.h:
                request += "".join(i)+"\r\n"
            request += "\r\n"
        reply = http_client(host, request)
        final_output = ""
        if args.v:
            final_output = reply
        else:
            if str.find("200 OK"):
                flag = 0
                for i in reply.split("\r\n"):
                    if len(i) == 0:
                        flag = 1
                    if flag == 1:
                        final_output += i
            else:
                final_output = reply
        if args.o is not None:
            write_to_file(args.output, final_output)
        else:
            print(final_output)
    else:
        print("Please enter valid URL")


# Usage: python echoclient.py --host host --port port
parser = argparse.ArgumentParser(add_help=False, prog = "httpc")
parser.add_argument("method", help="HTTP method needed to implement", type=str, choices=["get", "post", "GET", "POST", "help", "HELP"])
arg = parser.parse_args()
if arg.method.lower() == "get":
    implement_get()
elif arg.method.lower() == "help":
    implement_help()
elif arg.method.lower() == "post":
    implement_post()
# http_client(args.host, args.port)
