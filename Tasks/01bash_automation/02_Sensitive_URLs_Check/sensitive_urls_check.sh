#!/bin/bash

# Emptying the file
> result.txt

# Check if hosts.txt and endpoints.txt exist
if [[ ! -f "hosts.txt" || ! -f "endpoints.txt" ]]; then
    echo "[!] hosts.txt or endpoints.txt not found."
    exit 1
fi

echo "[*] Starting URL checks"

# Loop through each host in hosts.txt
while IFS= read -r host
do
    # Loop through each endpoint in urls.txt
    while IFS= read -r endpoint
    do
        # Construct the full URL
        url="https://$host$endpoint"
        echo "[*] Checking $url"

        # Make a GET request and check if status code is 2xx or 3xx
        status_code=$(curl -s -o /dev/null -w "%{http_code}" "$url")

        if [[ "$status_code" -ge 200 && "$status_code" -lt 400 ]]; then
            echo "[+] $url is reachable (Status: $status_code)"
            echo $url >> result.txt
        else
            echo "[-] $url returned status: $status_code"
        fi
    done < endpoints.txt
    echo

done < hosts.txt

echo "[*] URL check completed."
