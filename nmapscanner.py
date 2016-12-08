import nmap
from app import models, db

nmap = nmap.PortScanner()

def fullEnumeration(ip_range):
    nmap.scan(ip_range, arguments='-O -sC')
    print(nmap.command_line())
    #print(nmap.scaninfo())
    print(nmap.all_hosts())

    ips = nmap.all_hosts()

    for ip in ips:
        #Print out the IP on Screen
        print(ip + ' Information \n')
        #Retrieve all TCP Ports Scanned

        ports = nmap[ip].all_tcp()
        for port in ports:
            #Check for only open TCP ports
            try:
                if nmap[ip]['tcp'][port]['state'] == 'open':
                    print(nmap[ip]['tcp'][port]['state'],
                    port,
                    nmap[ip]['tcp'][port]['name'],
                    nmap[ip]['tcp'][port]['product'],
                    nmap[ip]['tcp'][port]['version'],
                    nmap[ip]['tcp'][port]['script'])
            except:
                print(nmap[ip]['tcp'][port]['state'],
                port,
                nmap[ip]['tcp'][port]['name'],
                nmap[ip]['tcp'][port]['product'],
                nmap[ip]['tcp'][port]['version'])

def top20Ports(ip_range):
    nmap.scan(ip_range, arguments='-sV --top-ports 20')
    print(nmap.command_line())
    print(nmap.scaninfo())
    ips = nmap.all_hosts()

    for ip in ips:
        #Print out the IP on Screen
        print(ip + ' Information \n')
        ips_add = {}
        ret = db.session.query(db.exists().where(models.Hosts.host_ip==ip)).scalar()
        if ret == False:
            #Adding the IP to the Database
            ips_add.update({
            'host_ip': ip,
            'host_name': nmap[ip].hostname(),
            'ports_open': 0
            })

            add_ip = models.Hosts(**ips_add)
            db.session.add(add_ip)
            db.session.commit()
        #Set the amount of Open Ports to 0
        open_ports = 0
        #Retrieve all TCP Ports Scanned
        ports = nmap[ip].all_tcp()
        for port in ports:
            #Check for only open TCP ports
            if nmap[ip]['tcp'][port]['state'] == 'open':
                print(nmap[ip]['tcp'][port]['state'],
                port,
                nmap[ip]['tcp'][port]['name'],
                nmap[ip]['tcp'][port]['product'],
                nmap[ip]['tcp'][port]['version'])

                host_information = {}
                host_information.update({
                'host': ip,
                'port_state': nmap[ip]['tcp'][port]['state'],
                'port_number': port,
                'port_name': nmap[ip]['tcp'][port]['name'],
                'product_used': nmap[ip]['tcp'][port]['product'],
                'product_version': nmap[ip]['tcp'][port]['version']
                })

                open_ports += 1

                host_information_add = models.HostInformation(**host_information)
                db.session.add(host_information_add)
                db.session.commit()

        port_update = models.Hosts.query.filter_by(host_ip=ip).first()
        port_update.ports_open = open_ports
        db.session.commit()

def main():
    print("""
    Python NMAP Scanner

    1. Full Scan
    2. Top 20 Port Scan

    """)
    scanType = input('      > ')

    print("""
    1. Scan a Single IP
    2. Scan a Range

    """)
    ipAmount = input('      > ')

    if ipAmount == '1':
        ip_range = input('Enter the IP you\'d like to scan > ')
        if scanType == '1':
            fullEnumeration(ip_range)
        elif scanType == '2':
            top20Ports(ip_range)
        else:
            print("Unrecognized Command")
    elif ipAmount == '2':
        ip_prefix = input('Enter the IP prefix that you\'d like to scan > ')
        range_start = input('Enter the start of the range > ')
        range_end = input('Enter the end of the range > ')

        address = ip_prefix + '.' + range_start + '-' + range_end
        if scanType == '1':
            fullEnumeration(address)
        elif scanType == '2':
            top20Ports(address)
        else:
            print("Unrecognized Command")

if __name__ == "__main__":
    main()
