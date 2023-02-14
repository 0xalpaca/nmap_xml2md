import os
import xml.etree.ElementTree as ElementTree
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="nmap_xml2md",
        description="This script transform XML output from nmap into different folder (IP) and file (open ports)",
        epilog="Credit: 0xalpaca",
    )
    parser.add_argument('filename', help="must be an xml file")

    args = parser.parse_args()
    if not args.filename:
        parser.print_help()
    elif not os.path.exists(args.filename):
        print("File does not exist")
    else:
        parse_nmap_xml(args.filename)


def parse_nmap_xml(xml_file):
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()
    for host in root.findall('host'):
        ip = host.find('address').get('addr')
        os.makedirs(ip)

        print(f"[+] Created folder {ip}")

        with open(os.path.join(ip, ip + ".md"), 'a') as fi:

            fi.write(">[!info] Open ports\n")

            for port in host.findall('ports/port'):
                port_number = port.get('portid')
                protocol = port.get('protocol')

                fi.write(">- [[" + protocol + "-" + port_number + "]]\n")

                with open(os.path.join(ip, protocol + "-" + port_number + ".md"), 'w') as fp:
                    fp.write("```nmap\n")
                    for element in port.iter():
                        if element.tag == "state":
                            fp.write(f"State: {element.get('state')}\n")
                            fp.write(f"{element.get('reason')}\n")
                        elif element.tag == "service":
                            fp.write(f"Service: {element.get('name')}\n")
                            fp.write(f"Product: {element.get('product')}\n")
                            fp.write(f"Version: {element.get('version')}\n")
                        elif element.tag == "script":
                            fp.write(f"Script: {element.get('id')}\n")
                            fp.write(f"Output: {element.get('output')}\n")
                    fp.write("```\n")


if __name__ == '__main__':
    main()
