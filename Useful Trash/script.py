import xml.etree.ElementTree as ET
import struct

def parse_xdf(xdf_path):
    tree = ET.parse(xdf_path)
    root = tree.getroot()

    parameters = []
    for table in root.findall('.//XDFTABLE'):
        name = table.find('title').text if table.find('title') is not None else "Unnamed"
        address_elem = table.find('address')
        size_elem = table.find('datasize')
        
        if address_elem is not None and size_elem is not None:
            address = int(address_elem.text, 16)
            size = int(size_elem.text)
            parameters.append({
                "name": name,
                "address": address,
                "size": size
            })
    return parameters

def read_bin(bin_path, parameters):
    with open(bin_path, 'rb') as bin_file:
        bin_data = bin_file.read()

    values = {}
    for param in parameters:
        address = param["address"]
        size = param["size"]
        
        if size == 8:
            value_format = 'B'  # unsigned char (1 byte)
        elif size == 16:
            value_format = 'H'  # unsigned short (2 bytes)
        elif size == 32:
            value_format = 'I'  # unsigned int (4 bytes)
        else:
            continue
        
        value = struct.unpack_from(value_format, bin_data, address)[0]
        values[param["name"]] = value

    return values

def main():
    xdf_path = 'C:\\Users\\adkri\\OneDrive\\Desktop\\New folder\\12212156 - 2002 512k V1.xdf'
    bin_path = 'C:\\Users\\adkri\\OneDrive\\Desktop\\New folder\\Pull 1.bin'
    
    parameters = parse_xdf(xdf_path)
    values = read_bin(bin_path, parameters)
    
    for name, value in values.items():
        print(f"{name}: {value}")

if __name__ == "__main__":
    main()
