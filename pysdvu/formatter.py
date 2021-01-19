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

    @classmethod
    def write_file(cls, filename):
        '''
        Rewrite the input file with the propagated types.
        '''
        content = cls.process_file(filename)
        with open(filename, "w") as f:
            indent = 0
            nl = 0
            fpe = 0
            for line in content:

                if line.startswith("process"):
                    fpe = 1
                    nl = 1
                    indent = 1
                elif ((line.startswith("guardBlock") or
                       line.startswith("guardCondition") or
                       line.startswith("effect")) and fpe == 1):
                    nl = 0
                    indent = 2
                elif line.startswith("guardCondition") and fpe == 1:
                    nl = 0
                    indent = 2
                elif line.startswith("system async;") and fpe == 1:
                    nl = 1
                    indent = 0
                elif fpe == 1:
                    indent = 3
                f.write("\n"*nl + "  "*indent + line +"\n")

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
    import glob
    sdve_files = glob.glob("../sdve-beem-benchmark/**/*.sdve", recursive=True)
    for file in sdve_files:
        Formatter.write_file(file)
