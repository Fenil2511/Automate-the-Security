import os
import xml.etree.ElementTree as ET
from jinja2 import Environment, FileSystemLoader


def main():
    filename = input("Enter nmap output file: ")
    if not os.path.exists(filename):
        print(f"File {filename} does not exists.")
        exit(1)

    with open(filename) as f:
        generate_report(f.read())


def generate_report(xml_data):
    template_data = parse_xml(xml_data)
    # Load the Jinja2 template
    env = Environment(
        loader=FileSystemLoader("templates")
    )  # Assuming the template is in the 'templates' directory
    template = env.get_template("nmap_scan_report_template.html")

    # Render the HTML
    output_html = template.render(template_data)

    # Save the rendered HTML to a file
    with open("nmap_scan_report.html", "w") as file:
        file.write(output_html)

    print("Report saved as 'nmap_scan_report.html'")


def parse_xml(xml_data):
    # Parse the XML
    root = ET.fromstring(xml_data)

    # Extract the current scan time
    scan_time = root.get("startstr")

    # Extract hosts and their data
    hosts = []
    total_open_ports = 0

    for host in root.findall(".//host"):
        host_info = {
            "address": host.find("address").get("addr"),
            "status": host.find("status").get("state"),
            "hostnames": [hn.text for hn in host.findall(".//hostname") if hn is not None],
            "ports": [],
        }

        ports = host.findall(".//ports/port")
        for port in ports:
            port_info = {
                "portid": port.get("portid"),
                "protocol": port.get("protocol"),
                "state": port.find("state").get("state"),
                "service_name": port.find("service").get("name"),
                "version": port.find("service").get("version", "N/A"),
                "extrainfo": port.find("service").get("extrainfo", "N/A"),
            }
            host_info["ports"].append(port_info)
            total_open_ports += 1

        hosts.append(host_info)

    # Extract scan summary details
    runstats = root.find(".//runstats/finished")
    elapsed_time = runstats.get("elapsed")
    scan_summary = runstats.get("summary")

    # Prepare data to pass into the template
    template_data = {
        "scan_time": scan_time,
        "hosts": hosts,
        "total_hosts": len(hosts),
        "total_open_ports": total_open_ports,
        "elapsed_time": elapsed_time,
        "scan_summary": scan_summary,
    }

    return template_data


if __name__ == "__main__":
    main()
