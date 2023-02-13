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
        if not os.path.exists(ip):
            os.makedirs(ip)

        for port in host.findall('ports/port'):
            port_number = port.get('portid')
            protocol = port.get('protocol')
            print(port_number)

            with open(os.path.join(ip, protocol + "-" + port_number + ".md"), 'w') as f:
                f.write('# ' + protocol + "-" + port_number + "\n\n")
                f.write("'''bash\n")
                for element in port.iter():
                    if element.tag == "state":
                        f.write(f"State: {element.get('state')}\n")
                        f.write(f"{element.get('reason')}\n")
                    elif element.tag == "service":
                        f.write(f"Service: {element.get('name')}\n")
                        f.write(f"Product: {element.get('product')}\n")
                        f.write(f"Version: {element.get('version')}\n")
                    elif element.tag == "script":
                        f.write(f"Script: {element.get('id')}\n")
                        f.write(f"Output: {element.get('output')}\n")
                f.write("'''\n")


if __name__ == '__main__':
    main()
