import socket
import http.client
from urllib.parse import urlparse


def scan_open_ports(target, ports):
    print(f"\nScanning open ports on {target}...")
    start_port, end_port = map(int, ports.split('-'))
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port}: Open")
        sock.close()


def check_software_version(url):
    try:
        print("\nChecking software version...")
        parsed_url = urlparse(url)
        conn = http.client.HTTPConnection(parsed_url.netloc, timeout=5)
        conn.request("GET", "/")
        response = conn.getresponse()
        server_header = response.getheader('Server')
        if server_header:
            print(f"Server: {server_header}")
        else:
            print("No Server header found.")
        conn.close()
    except Exception as e:
        print(f"Error checking software version: {e}")


def check_misconfigurations(target):
    print("\nChecking common misconfigurations...")
    try:
        conn = http.client.HTTPConnection(target, timeout=5)
        conn.request("GET", "/")
        response = conn.getresponse()
        data = response.read().decode('utf-8', errors="ignore")
        if "Index of" in data:
            print("Warning: Directory listing may be enabled.")
        else:
            print("No misconfiguration detected for directory listing.")
        conn.close()
    except Exception as e:
        print(f"Error checking misconfigurations: {e}")


def main():
    target = input("Enter the target IP or domain: ")
    scan_type = input("Choose scan type (1: Open Ports, 2: Software Version, 3: Misconfigurations, 4: All): ")

    if scan_type in ['1', '4']:
        ports = input("Enter port range (e.g., 1-1024): ")
        scan_open_ports(target, ports)

    if scan_type in ['2', '4']:
        url = f"http://{target}" if not target.startswith("http") else target
        check_software_version(url)

    if scan_type in ['3', '4']:
        check_misconfigurations(target)


if __name__ == "__main__":
    main()
