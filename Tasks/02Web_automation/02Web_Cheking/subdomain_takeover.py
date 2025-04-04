import dns.resolver
import requests

from error_messages import ERROR_MESSAGES
from cname_keywords import CNAME_KEYWORDS

requests.packages.urllib3.disable_warnings()


# Function to get CNAME record of a host
def get_cname(host):
    try:
        answers = dns.resolver.resolve(host, 'CNAME')
        for rdata in answers:
            return str(rdata.target).rstrip('.')
    except Exception as e:
        print(f"[!] Failed to resolve CNAME for {host}: {e}")
    return None


# Function to check if the CNAME belongs to a known service
def check_cname(cname):
    for service, keywords in CNAME_KEYWORDS.items():
        for keyword in keywords:
            if keyword in cname:
                return service
    return None


# Function to fetch HTML source and check for error messages
def check_html_source(url, service):
    try:
        response = requests.get(url, timeout=10, verify=False)
        for error_msg in ERROR_MESSAGES[service]:
            if error_msg in response.text:
                return True
    except Exception as e:
        print(f"[!] Failed to fetch {url}: {e}")
    return False


# Main function to check hosts for subdomain takeover
def main():
    vulnerable_hosts = []
    try:
        with open('hosts.txt', 'r') as file:
            hosts = file.read().splitlines()
    except FileNotFoundError:
        print("[-] hosts.txt file not found.")
        return

    print("[*] Starting subdomain takeover check!")

    for host in hosts:
        print(f"\n[*] Checking {host}")
        cname = get_cname(host)
        
        if cname:
            print(f"[*] CNAME found: {cname}")
            service = check_cname(cname)
            
            if service:
                print(f"[+] CNAME matches known service: {service}")
                url = f"https://{host}"
                if check_html_source(url, service):
                    print(f"[+] Potential subdomain takeover detected: {host}")
                    vulnerable_hosts.append(host)
                else:
                    print(f"[-] No takeover signature found.")
            else:
                print("[-] CNAME does not match known vulnerable services.")
        else:
            print("[-] No CNAME record found.")

    print("-----" * 20)
    print(f"\n[*] Subdomain takeover check completed. Following hosts are possibly vulnerable: \n{'\n'.join(vulnerable_hosts)}")

if __name__ == "__main__":
    main()
