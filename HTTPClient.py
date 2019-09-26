import socket
import argparse
import sys
import urllib.parse


def uri_validator(x):
    try:
        result = urllib.urlparse(x)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


def http_client(host, string):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    output = ""
    try:
        conn.connect((host, 80))
        print("Type any thing then ENTER. Press Ctrl+C to terminate")
        print(ord(" "))
        a = "{element:'fire'"
        q = urllib.parse.quote("name=' aman'")
        while True:
            line = f"PUT /put?{q} HTTP/1.0\r\nAccept:application/json\r\n\r\n"
            request = line.encode("utf-8")
            conn.send(request)
            # MSG_WAITALL waits for full request or error
            response = conn.recv(len(request), socket.MSG_WAITALL)
            if len(response) > 0:
                output += response.decode("utf-8")
            else:
                break
        return output
    finally:
        conn.close()


def implement_help(name):
    if len(sys.argv)==3:
        if sys.argv[2].lower() == "get":
            print("get help")
        elif sys.argv[2].lower() == "post":
            print("post help")
        else:
            print("invalid argument")
    else:
        print("help")


def implement_get():
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-h", "--h", action="append", nargs="+")
    parser.add_argument("URL")
    args = parser.parse_args()
    URL = args.URL
    if uri_validator(URL):
        print("valid")
        start = URL.find("/")
        n = 3
        while start >= 0 and n > 1:
            start = URL.find(URL, start + len("/"))
            n -= 1
            """if URL.find("?") >= 0:
                path = URL.substring(start, URL.find())
            else:
                path = URL.substring(start, len(URL))"""
        path = URL.substring(start, len(URL))
        start_path =  start
        path = urllib.parse.quote(path)
        start = URL.find("/")
        n = 2
        while start >= 0 and n > 1:
            start = URL.find(URL, start + len("/"))
            n -= 1
        host = URL.substring(start+1,start_path)

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
        final_output =""
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


# Usage: python echoclient.py --host host --port port
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("method", help="HTTP method needed to implement", type=str, default=80)
if parser.parse_args().method.lower() == "get":
    implement_get()
elif parser.parse_args().method.lower() == "help":
    implement_help()



parser.add_argument("URL", help="server host", default="httpbin.org")
args = parser.parse_args()
# http_client(args.host, args.port)
