#!/usr/bin/env python3
import os
import re
import sys
from optparse import OptionParser

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
            guid = ''
            rail_letter = ''
            output_in_dict = {
                
            }
            with open(self.file_location, "r") as file_r:
                for string in file_r:
                    guid_pattern = re.search(r"([A-Z0-9]{3};[A-Z0-9]{1,5}-\d{1,3}-\d{1,3}:[A-Z0-9]+\/[A-Z0-9]{2,3}) GUID=(0x[0-9a-f]{16})", string)
                    rail_pattern = re.search(r"rail ([A-Z]+)\(([0-9a-f]{4}:[0-9a-f]{2}\.[0-9a-f]{2}\.[0-9a-f]{2})\): ([0-9]+)", string)
                    ports_pattern = re.search(r"([A-Z0-9]{1,5}-\d{1,3}-\d{1,3}(?:\/[A-Za-z0-9]+)+) <--> ([A-Z0-9]{1,4}-\d{1,3}-\d{1,3}(?:\/[A-Za-z0-9]+)+)", string)
                    
                    if string[0] == "#":  # Check for comments:
                        continue
                    if guid_pattern:  # For getting GUID
                        guid = guid_pattern.group(2)
                        output_in_dict[guid] = {
                            'switch': guid_pattern.group(1),
                            'rails': {}
                        }
                    elif rail_pattern:  # For getting all info about rail
                        rail_letter = rail_pattern.group(1)
                        output_in_dict[guid]['rails'][rail_letter] = {
                                'rail_pci': rail_pattern.group(2),
                                'number_of_ports': rail_pattern.group(3),
                                'ports': [

                                ]
                            }
                    elif ports_pattern:  # For getting ports from rail
                        output_in_dict[guid]['rails'][rail_letter]['ports'].append(
                            (
                                ports_pattern.group(1), 
                                ports_pattern.group(2)
                            )
                        )

            return output_in_dict

    def show_output(self):
        print(self.convert_output())
        sys.exit(0)

parser_obj = MainParser()
parser_obj.show_output()
