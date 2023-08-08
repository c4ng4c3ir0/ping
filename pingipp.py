import argparse
import subprocess
import ipaddress

def ping_ips(ips):
    for ip in ips:
        ping_process = subprocess.Popen(['ping', '-c', '1', '-W', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, error = ping_process.communicate()

        if ping_process.returncode == 0:
            print(f'{ip} está ON')
        else:
            print(f'{ip} está OFF')

# Configurar o parser de argumentos
parser = argparse.ArgumentParser(description='Script de ping')
parser.add_argument('-subnet', metavar='SUBNET', type=str, help='Sub-rede a ser verificada')
parser.add_argument('-ips', metavar='IP_FILE', type=str, help='Arquivo contendo a lista de IPs, um abaixo do outro')
parser.add_argument('-o', metavar='OUTPUT', type=str, help='Arquivo de saída')

# Analisar os argumentos da linha de comando
args = parser.parse_args()

# Verificar se o argumento -subnet foi fornecido
if args.subnet:
    subnet = ipaddress.IPv4Network(args.subnet, strict=False)
    subnet_ips = [str(ip) for ip in subnet.hosts()]
    ips = subnet_ips
elif args.ips:
    with open(args.ips, 'r') as ip_file:
        ips = [line.strip() for line in ip_file.readlines() if line.strip()]
else:
    print('É necessário fornecer a sub-rede via argumento -subnet ou fornecer um arquivo contendo a lista de IPs via argumento -ips.')
    exit()

# Realizar o ping nos IPs
ping_results = []
for ip in ips:
    ping_process = subprocess.Popen(['ping', '-c', '1', '-W', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, error = ping_process.communicate()

    if ping_process.returncode == 0:
        result = f'{ip} está ON'
    else:
        result = f'{ip} está OFF'
    ping_results.append(result)

# Exibir resultados na tela
for result in ping_results:
    print(result)

# Salvar resultados em arquivo de saída, se especificado
if args.o:
    with open(args.o, 'w') as output_file:
        for result in ping_results:
            output_file.write(result + '\n')
