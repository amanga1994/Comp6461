import socket
import argparse

def http_client(host,request):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    output = ""



    # request = "POST /redirect-to/ HTTP/1.0\r\n\r\n";
    try:
        conn.connect((host, 80))
        print("Type any thing then ENTER. Press Ctrl+C to terminate")
        print(ord(" "))
        print(request);
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
        responseCode = output.split("\n")[0].split(" ")[1];

        print("Response Code ",responseCode);
        if(responseCode == "302"):
            location = output.split("\r\n")[5].split(": ")[1];
            queryParam = request.split(" ")[1].split("?")[1];
            # print("queryParam ", queryParam);
            print("Redirecting to ", location);
            request = "GET /"+location.split("/")[3]+"?"+queryParam+" HTTP/1.0\r\n\r\n";
            print("fRequest\n",request);
            output = http_client(host, request);
            # print("sssss",output);

        return output
    finally:
        conn.close()

host = "httpbin.org";
# request = "GET /absolute-redirect/1?name=aman HTTP/1.0\r\n\r\n";
# request = "GET /absolute-redirect/1?course=networking&assignment=1 HTTP/1.0\r\n\r\n";
request = "GET /redirect-to/get?course=networking&assignment=1 HTTP/1.0\r\n\r\n"
# request = "GET /redirect-to/?url=/get?course=networking&assignment=1 HTTP/1.0\r\n\r\n";
# request = "POST /redirect-to/ HTTP/1.0\r\n\r\n";
http_client(host, request);