#!/usr/bin/env python3
import os
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
                    if string[0] == "#":  # Check for comments:
                        continue
                    if "Node rail connectivity mismatch on the switch" in string:  # For getting GUID
                        guid = string.split("=")[-1].replace("\n", "")
                        output_in_dict[guid] = {
                            'switch': string.split(": ")[-1].split(" ")[0],
                            'rails': {}
                        }
                    elif ' rail ' in string:  # For getting all info about rail
                        rail_letter = string.split("(")[0].split(" ")[-1]
                        output_in_dict[guid]['rails'][rail_letter] = {
                                'rail_pci': string.split("(")[-1].split(")")[0],
                                'number_of_ports': string.split(": ")[-1].split(" ")[0],
                                'ports': [

                                ]
                            }
                    elif ' <--> ' in string:  # For getting ports from rail
                        output_in_dict[guid]['rails'][rail_letter]['ports'].append(
                            (
                                string.split(' <--> ')[0].replace(" ", "").replace("\n", ""), 
                                string.split(' <--> ')[1].replace(" ", "").replace("\n", "")
                            )
                        )

            return output_in_dict

    def show_output(self):
        print(self.convert_output())
        sys.exit(0)

parser_obj = MainParser()
parser_obj.show_output()
