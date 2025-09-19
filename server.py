import socket
import os

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8080))
    server.listen(1)
    
    print("Server running at http://localhost:8080")
    
    while True:
        client, address = server.accept()
        
        request = client.recv(1024).decode()
        print(f"Request: {request.split()[1]}")
        
        lines = request.split('\n')
        path = lines[0].split()[1]
        
        if path == '/':
            path = '/index.html'
        
        filename = path[1:]
        
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                content = file.read()
            
            if filename.endswith('.html'):
                content_type = 'text/html'
            elif filename.endswith('.css'):
                content_type = 'text/css'
            else:
                content_type = 'text/plain'
            
            response = f"HTTP/1.0 200 OK\r\n"
            response += f"Content-Type: {content_type}\r\n"
            response += f"Content-Length: {len(content)}\r\n"
            response += "\r\n"
            
            client.send(response.encode())
            client.send(content)
            print(f"Served: {filename}")
        
        else:
            error_content = "File Not Found."
            response = f"HTTP/1.0 404 Not Found\r\n"
            response += "Content-Type: text/plain\r\n"
            response += f"Content-Length: {len(error_content)}\r\n"
            response += "\r\n"
            response += error_content
            
            client.send(response.encode())
            print(f"404: {filename} not found")
        
        client.close()

if __name__ == "__main__":
    start_server()