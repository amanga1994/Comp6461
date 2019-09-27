import socket
import argparse

def http_client():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    output = ""
    host = "httpbin.org";

    # request = "GET /absolute-redirect/1?name=aman HTTP/1.0\r\n\r\n";
    request = "POST /redirect-to/ HTTP/1.0\r\n\r\n";
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
        print(output);

        return output
    finally:
        conn.close()

http_client()

# my_parser = argparse.ArgumentParser()
# my_parser.add_argument('--input', action='store', type=int, required=True)