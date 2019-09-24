import socket
import argparse
import sys
import urllib.parse


def http_client(host, port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((host, port))
        print("Type any thing then ENTER. Press Ctrl+C to terminate")
        print(ord(" "))
        a="{element:'fire'"
        q=urllib.parse.quote("name=' aman'")
        while True:
            line = f"PUT /put?{q} HTTP/1.0\r\nAccept:application/json\r\n\r\n"
            request = line.encode("utf-8")
            conn.send(request)
            # MSG_WAITALL waits for full request or error
            response = conn.recv(len(request), socket.MSG_WAITALL)
            if(len(response)>0):
                sys.stdout.write(response.decode("utf-8"))
            else:
                break
    finally:
        conn.close()


# Usage: python echoclient.py --host host --port port
parser = argparse.ArgumentParser()
parser.add_argument("--host", help="server host", default="httpbin.org")
parser.add_argument("--port", help="server port", type=int, default=80)
args = parser.parse_args()
http_client(args.host, args.port)