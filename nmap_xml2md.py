#!/usr/bin/python3

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
    parser.add_argument('output_folder', help="this is the folder where the script will save the files and folders")

    args = parser.parse_args()
    if not os.path.exists(args.filename):
        print("[-] File does not exist")
    else:
        basepath = args.output_folder
        parse_nmap_xml(args.filename, basepath)


def parse_nmap_xml(xml_file, basepath):
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()
    if not os.path.exists(basepath):
        print(f'[+] Created folder: {basepath}')
        os.makedirs(basepath)
    else:
        print(f'[+] {basepath} exists. Using it.')

    with open(os.path.join(basepath, basepath + ".md"), 'w') as fb:
        fb.write(">[!info] Scanned IPs list\n")
        for host in root.findall('host'):
            ip = host.find('address').get('addr')
            os.makedirs(basepath + "/" + ip)
            fb.write(">- [[" + ip + "]]\n")
            print(f"[+] Created folder {ip}")

            with open(os.path.join(basepath, ip, ip + ".md"), 'w') as fi:
                fi.write(">[!info] Open ports\n")
                for port in host.findall('ports/port'):
                    port_number = port.get('portid')
                    protocol = port.get('protocol')
                    fi.write(">- [[" + protocol + "-" + port_number + "]]\n")
                    with open(os.path.join(basepath, ip, protocol + "-" + port_number + ".md"), 'w') as fp:
                        fp.write("```nmap\n")

                        for element in port.iter():
                            if element.tag == "state":
                                state = element.get('state')
                                fp.write(f"State: {state}\n")
                                fp.write(f"{element.get('reason')}\n")
                            elif element.tag == "service":
                                fp.write(f"Service: {element.get('name')}\n")
                                fp.write(f"Product: {element.get('product')}\n")
                                fp.write(f"Version: {element.get('version')}\n")
                            elif element.tag == "script":
                                fp.write(f"Script: {element.get('id')}\n")
                                fp.write(f"Output: {element.get('output')}\n")

                        fp.write("```\n")
                        fp.write(f"\n---\n\n#nmap #{protocol}/{port_number} #state/{state}\n")
                fi.write("\n")
        fb.write("\n")


if __name__ == '__main__':
    main()
