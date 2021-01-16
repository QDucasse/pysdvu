# -*- coding: utf-8 -*-
# ================================================
# Project: sdvu
# Author: Quentin Ducasse
# Email: quentin.ducasse@ensta-bretagne.org
# Repository: https://github.com/QDucasse/pysdvu
# ================================================

# FORMATTER
# =========
# Process the file and propagate the different type definitions to their variables


class Formatter():
    '''
    Preprocess an sdve program into a version with propagated types.
    '''

    # Dictionary with the different variables and their corresponding types

    @classmethod
    def process_file(cls, filename):
        '''
        Process a file with propagated types.
        '''
        temp_types = {}
        glob_decl, temp_decl, proc = cls.preprocess(filename)
        new_content = glob_decl

        # Process temporary types
        for line in temp_decl:
            split_line = line.split(" ")
            type = split_line[1]
            id = split_line.index("=")
            name = split_line[id-1]
            temp_types[name] = type
        # Propagate type
        for line in proc:
            if line.startswith("t_"):
                name = line.split(" ")[0]
                new_content.append("temp " + temp_types[name] + " " + line)
            else:
                new_content.append(line)

        return new_content


    @classmethod
    def preprocess(cls, filename):
        '''
        Run through the file and separate the lines in global declarations,
        temporary declarations and processes.
        '''
        with open(filename) as sdve_file:
            content = sdve_file.readlines()
        content = [line.strip() for line in content] # Remove trailing and leading spaces
        content = [line for line in content if line] # Remove empty strings
        # Find indexes to cut the content in: glob decl, temp decl and process
        id = 0
        temp_id = 0
        proc_id = 0
        temp_passed = False
        for line in content:
            if (line.startswith("temp") and not(temp_passed)):
                temp_id = id
                temp_passed =  True
            if (line.startswith("process")):
                proc_id = id
                break
            id += 1
        return content[:temp_id], content[temp_id:proc_id], content[proc_id:]


if __name__ == "__main__":
    print(Formatter.process_file("../sdve-beem-benchmark/adding/adding.1.sdve"))
