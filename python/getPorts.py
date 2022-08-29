#!/bin/python3

#requirements:
#   pyperclip

import sys
import os
import pyperclip

def main():
    if len(sys.argv) < 2:
        print("Syntax error, check args!")
        print("Example: ./getPorts.py <FilePath> [-tcp|-udp|]")
        exit()
    else:
        ports = []
        nmap_file = open(sys.argv[1], 'r')
        if sys.argv[1] == '-tcp':
            for line in nmap_file:
                if "/tcp" in line:
                    ports.append(line.split("/tcp")[0])

            print (','.join(ports))
            pyperclip.copy(','.join(ports))
            print("TCP ports copied to the clipboard")

        elif sys.argv[1] == '-udp':
            for line in nmap_file:
                if "/udp" in line:
                    ports.append(line.split("/udp")[0])

            print (','.join(ports))
            pyperclip.copy(','.join(ports))
            print("UDP ports copied to the clipboard")

        else:
            print("No protocol selected, TCP/UDP by default")
            for line in nmap_file:
                if "/udp" in line:
                    ports.append(line.split("/udp")[0])
                if "/tcp" in line:
                    ports.append(line.split("/tcp")[0])

            print (','.join(ports))
            pyperclip.copy(','.join(ports))
            print("TCP/UDP ports copied to the clipboard")

if __name__ == "__main__":
    main()
