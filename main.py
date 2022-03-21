#!/usr/bin/env python3
import os
import re
import sys
from optparse import OptionParser
from tkinter import N

parser = OptionParser()
parser.add_option("-p", "--path", dest="path",
                  help="PATH to file.", metavar="FILE")
(options, args) = parser.parse_args()


class MainParser:
    def __init__(self):
        self.file_location = options.path

    def check_for_errors(self):
        """This method using for catch most common erros"""
        if self.file_location is None or self.file_location == "":
            print("[!] Output from " + __file__ + "\nYou need to specify path to file")
            sys.exit(1)
        elif not os.path.exists(self.file_location):
            print("[!] Output from " + __file__ + "\nFile " + self.file_location + " not found!")
            sys.exit(1)
        return True

    
    def convert_output(self):
        """This method return dictionary from file, specified in constructor"""
        if self.check_for_errors():
            output_in_dict = {
                
            }
            with open(self.file_location, "r") as file_r:
                blocks_array = re.findall(r"[^\s\n\r]+[^\r\n]+(?:\r?\n\s{4,}[^\r\n]+)+", file_r.read())
                if blocks_array is None:
                    print("[!] Output from " + __file__ + "\nSpecified file has incorrect format for parser")
                    sys.exit(1)
                for block in blocks_array:
                    guid_and_switch = re.search(r"^[^\r\n]+: ([^\s\r\n]+) GUID=(0x[0-9A-Fa-f]{16})", block)
                    
                    if guid_and_switch is None:
                        print("[!] Output from " + __file__ + "\nGUID or switch not found. Please check specified file")
                        sys.exit(1)
                    
                    switch = guid_and_switch.group(1)
                    guid = guid_and_switch.group(2)
                    output_in_dict[guid] = {
                        'switch': switch,
                        'rails': {}
                    }
                    rail_array = re.findall(r"\s{4}rail[^\r\n]+(?:\r?\n\s{8,}[^\r\n]+)+", block)
                    for rail in rail_array:
                        rail_params = re.search(r"rail ([A-Z0-9]+)\(([^)]+)\): (\d+)", rail)
                        rail_letter = rail_params.group(1)
                        rail_pci = rail_params.group(2)
                        number_of_ports = rail_params.group(3)
                        rail_ports_list = []
                        rail_ports_regex_output = re.findall(r"\s{8,}\S+ <--> [^\s\r\n]+", rail)
                        for rail_port in rail_ports_regex_output:
                            rail_port_params = re.search(r"(\S+) <--> ([^\s\r\n]+)", rail_port)
                            rail_ports_list.append(rail_port_params.group(1))
                        
                        output_in_dict[guid]['rails'][rail_letter] = {
                            'rail_pci': rail_pci,
                            'number_of_ports': number_of_ports,
                            'ports': tuple(rail_ports_list)
                        }
            return output_in_dict

    def show_output(self):
        print(self.convert_output())
        sys.exit(0)

parser_obj = MainParser()
parser_obj.show_output()
