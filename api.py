import socket
import requests
import json
import time

# Getting the daily covid-19 cases in Turkey from another api  
def get_daily_data_from_api():
    api_url = "https://api.covid19api.com/country/turkey/status/confirmed"

    payload  = {}
    headers= {}

    response = requests.request("GET", api_url, headers=headers, data = payload)

    daily_covid_data = json.loads(response.text)
    
    return daily_covid_data

# Calculates the increase rate of new covid-19 cases in Turkey from daily data day by day
def calculate_increase_rates(data):
    increase_rates = []
    
    for i,daily in enumerate(data):
        if(i == 0):
            continue

        day = dict()
        day["Date"] = daily["Date"]
        
        if(data[i-1]["Cases"] != 0 and (daily["Cases"] != data[i-1]["Cases"])):
            day["IncreaseRate"] = '%' + str(((daily["Cases"] - data[i-1]["Cases"]) / data[i-1]["Cases"]) * 100)
        else:
            day["IncreaseRate"] = 0

        increase_rates.append(day)
    
    return increase_rates

#Generating headers for responses
def generate_header(response_code):
        """
        Generate HTTP response headers.
        Parameters:
            - response_code: HTTP response code to add to the header. 200 and 404 supported
        Returns:
            A formatted HTTP header for the given response_code
        """
        header = ''
        if response_code == 200:
            header += 'HTTP/1.1 200 OK\n'
        elif response_code == 400:
            header += 'HTTP/1.1 400 Bad Request\n'
        elif response_code == 404:
            header += 'HTTP/1.1 404 Not Found\n'

        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: {now}\n'.format(now=time_now)
        header += 'Server: Simple-Python-Server\n'
        header += 'Connection: close\n\n' # Signal that connection will be closed after completing the request
        return header

#Get request response
def get_response(index_str,daily_data,increase_data):

    response_header = generate_header(400)
    response_body = json.dumps({"status": 400,"error": "Bad Request","message": "No message available"})

    if('/' in index_str):
        index = index_str[index_str.rfind('/'):]
        if(index == '/'):
            response_header = generate_header(200)
            response_body = json.dumps(daily_data)
        elif(index == '/increaserate'):
            response_header = generate_header(200)
            response_body = json.dumps(increase_data)
        elif('/increaserate?date=' in index):
            date = index[19:]
            response_header = generate_header(404)
            response_body = json.dumps({"status": 404,"error": "Not Found","message": "No message available"})
            for i in increase_data:
                if(date in i["Date"]):
                    response_header = generate_header(200)
                    response_body = json.dumps(i)
            
        else:
            response_header = generate_header(404)
            response_body = json.dumps({"status": 404,"error": "Not Found","message": "No message available"})
    
    return response_header,response_body

#Post request response
def post_response(index_str,body,daily_data,increase_data):

    response_header = generate_header(400)
    response_body = json.dumps({"status": 400,"error": "Bad Request","message": "No message available"})
    

    if('/' in index_str):
        index = index_str[index_str.rfind('/'):]
        if(index == '/'):
            response_header = generate_header(200)
            response_body = json.dumps(daily_data)
        elif(index == '/increaserate' and len(body) == 0):
            response_header = generate_header(200)
            response_body = json.dumps(increase_data)
        elif(index == '/increaserate' and len(body) != 0):
            response_header = generate_header(404)
            response_body = json.dumps({"status": 404,"error": "Not Found","message": "No message available"})
            req_body = json.loads(body)
            
            if("date" in req_body.keys()):
                date = req_body["date"]
                
                for i in increase_data:
                    if(date in i["Date"]):
                        response_header = generate_header(200)
                        response_body = json.dumps(i)
            else:
                response_header = generate_header(400)
                response_body = json.dumps({"status": 400,"error": "Bad Request","message": "No message available"})

        else:
            response_header = generate_header(404)
            response_body = json.dumps({"status": 404,"error": "Not Found","message": "No message available"})
    
    return response_header,response_body
        


def start_server(host,port):
    
    daily_data = get_daily_data_from_api()
    increase_data = calculate_increase_rates(daily_data)
    

    PACKET_SIZE = 1024

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    print("starting the server on {}:{}".format(host,port))
    server_socket.bind((host,port))
    server_socket.listen()
    print("server is ready for connections.")

    while True:
        conn,adr = server_socket.accept()
        
        with conn:

            req = conn.recv(PACKET_SIZE).decode()
            
            if(not req):
                break

            req_method = req.split(' ')[0]
            index = req.split(' ')[1]

            response_header = generate_header(400)
            response_body = json.dumps({"status": 400,"error": "Bad Request","message": "No message available"})

            if req_method == 'GET':
                response_header, response_body = get_response(index,daily_data,increase_data)
            
            elif req_method == 'POST':
                lines = req.splitlines()
                
                flag = 0
                req_body = ""
                
                
                for line in lines:
                    
                    if(flag == 1):
                        req_body += line
                    if(line == ''):
                        flag = 1
                response_header, response_body = post_response(index,req_body,daily_data,increase_data)
            
            response_header = response_header.encode()
            response_body = response_body.encode()

            response = response_header + "\n".encode() + response_body

            conn.send(response)

            conn.close()




if __name__ == "__main__":
    start_server('127.0.0.1',8080)