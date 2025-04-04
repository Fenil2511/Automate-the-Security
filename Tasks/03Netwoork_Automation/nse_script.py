from nmap import nmap


# Function to scan ports
def scan_ports(hostname, ports, script_name):
    nm = nmap.PortScanner()
    script_result = {}

    nmap_options = f"--script {script_name}"
    result = nm.scan(hostname, ports=ports, arguments=nmap_options)
    for hostname in result["scan"]:
        for port, port_result in (
            result["scan"].get(hostname, {}).get("tcp", {}).items()
        ):
            if "script" in port_result and script_name in port_result["script"]:
                script_result[port] = port_result["script"][script_name]

    return script_result


# Main function to control the scanning
def main():
    hostname = input("Enter the target hostname: ") # localhost
    ports = input("Enter the target port(s): ") # 80
    nse_script_name = input("Enter the target NSE Script Name: ") # http-title

    print(f"Scanning ports on {hostname}...")

    # Perform the port scan
    scan_results = scan_ports(hostname, ports, nse_script_name)

    print(f"\n{'='*50}")
    print(f" Nmap Scan Results for Target: {hostname}")
    print(f" NSE Script: {nse_script_name}")
    print("=" * 50)

    # Show basic host information
    print(f"\nHost: {hostname}")
    print(f"Output for NSE script '{nse_script_name}' on port(s) {ports}:")
    for port, script_output in scan_results.items():
        print(f"\nPort {port}:")
        print(f"  Script Output: {script_output}")


# Run the main function
if __name__ == "__main__":
    main()
