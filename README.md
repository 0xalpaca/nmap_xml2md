# nmap_xml2md
This is a simple 50 lines script, which transform XML output from nmap into different folder (IP) and file (open ports).

```
usage: nmap_xml2md [-h] filename output_folder

This script transform XML output from nmap into different folder (IP) and file
(open ports)

positional arguments:
  filename       must be an xml file
  output_folder  this is the folder where the script will save the files and
                 folders

options:
  -h, --help     show this help message and exit

Credit: 0xalpaca
```
## Example usage

```bash
./nmap_xml2md nmap_output.xml example.com
```

## Output in Obsidian
The idea is to use these different folders and files inside markdown-based note taking app to organise our assessments (like Obsidian.md).

Once you have executed the script, you will find multiple files and folders. Files are the different ports found and folder are the ip(s) scanned.

This could be represented like this:

- example.com
  - example.com.md
  - 192.168.0.1
    - 192.168.0.1.md
    - 80.md
    - 8080.md
  - 192.168.0.54
    - 192.168.0.54.md
    - 80.md
    - 443.md
    - 3389.md
  - 192.168.0.56
    - 192.168.0.56.md
    - 53.md
