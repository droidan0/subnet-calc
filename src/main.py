import re
from colorama import Fore, Style
def get_ip():
    ip = input("Type ip/mask: ")
    re_format = r"^(((?!25?[6-9])[12]\d|[1-9])?\d\.?\b){4}\/(3[0-2]|[1-2]?[0-9])$"
    if re.search(re_format, ip):
        res = ip.split('/')
        return res[0], int(res[1])
    else:
        raise Exception("Ip or mask isn't valid")

        
def host_count(mask: int):
    hosts = 2 ** (32 - mask) - 2
    return hosts

def subnet_mask(mask: int, ip_address):
    ip_binary = "00000000000000000000000000000000"
    ip_bin = list(ip_binary)
    for i in range(0, mask):
        ip_bin[i] = "1"
    result_binary = "".join(ip_bin)
    result = [result_binary[i:i + 8] for i in range(0, 4 * 8, 8)]
    i = 0
    subnetmask = "" 
    for el in result:
        if i == 3:
            subnetmask += f"{int(el, 2)}"
        else:
            subnetmask += f"{int(el, 2)}."
        i += 1
    return subnetmask

def network_id(subnetmask, ip):
    ip_octets = [int(x) for x in ip.split(".")] 
    mask_octets = [int(x) for x in subnetmask.split(".")]
    net_octets = [ip_octets[i] & mask_octets[i] for i in range(4)]
    return ".".join(map(str, net_octets)), net_octets

def wildcard_mask(binary_subnetmask):
    return [x ^ 255 for x in binary_subnetmask]

def broadcast_adress(net_octets, wildcard):
    result = [str(net_octets[i] | wildcard[i]) for i in range(4)]
    return ".".join(result)

        

    
def main():
    (ip, mask) = get_ip()
    subnetmask = subnet_mask(mask, ip)
    (networkid, net_octets) = network_id(subnetmask, ip)
    hosts = host_count(mask)
    wildcard = wildcard_mask([int(i) for i in subnetmask.split(".")])
    broadcastadress = broadcast_adress(net_octets, wildcard)
    
    print(f"""
          1. ip/mask - {ip}/{mask}
          2. subnetmask - {subnetmask}
          3. network id - {networkid}
          4. broadcast adress - {broadcastadress}
          5. hosts count - {hosts}
          6. wildcard - {".".join(str(x) for x in wildcard)}
          """)

    

if __name__ == "__main__":
    main()