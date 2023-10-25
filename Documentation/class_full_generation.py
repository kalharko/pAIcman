import os



targets = (
    'utils/',
    'back/',
    'algorithms/',
    'front/cli/',
)

out = '@startuml class_full\n'
out += 'title Auto generated class diagram\n'


for target in targets:
    out += f"package {target[:-1]} " + '{\n'
    for path in os.listdir(target):
        if path.split('.')[-1] != 'py' or path == '__init__.py':
            continue

        with open(target + path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        print()
        print(target + path)
        for line in lines:
            print(line, end='')

        # find class, attributs and function definitions
        try:
            pos_defs = []
            for i, line in enumerate(lines):
                splited = line.lstrip(' ').split(' ')
                if splited[0] == 'class':
                    pos_class = i
                elif splited[0] == 'def':
                    pos_defs.append(i)
            pos_atts = []
            for i in range(pos_class + 1, pos_defs[0]):
                if lines[i] != '\n':
                    pos_atts.append(i)
            line_class = lines[pos_class].rstrip('\n')
            line_atts = [
                lines[i].lstrip(' ').rstrip('\n') for i in pos_atts
            ]
            line_defs = [
                lines[i].lstrip(' ').rstrip('\n') for i in pos_defs
            ]

            # write class
            class_name = line_class.split(' ')[1].split('(')[0]
            inheritance = line_class.split(' ')[1].split('(')[1].rstrip('):')
            out += 'class ' + class_name + '{\n'
            # write attributes
            for line in line_atts:
                if line[0] == '_':
                    out += '-'
                else:
                    out += '+'
                out += line + '\n'
            # write defs
            for line in line_defs:
                line = line[len(line.split(' ')[0]):].rstrip(':')
                if line[0] == '_':
                    out += '-'
                else:
                    out += '+'
                out += line + '\n'
            # close class
            out += '}\n'
            # links
            if inheritance != '':
                out += class_name + ' <|-- ' + inheritance + '\n'
            for line in line_atts:
                att_name = line.split(': ')[0]
                att_type = line.split(': ')[-1]
                if '[' in att_type:
                    att_type = att_type.split('[')[-1]
                    att_type = att_type.split(']')[0]
                if att_type in ('int', 'float', 'bool', 'str') or ',' in att_type:
                    continue
                out += class_name + ' *-- ' + att_type + f' : {att_name}' + '\n'
            out += '\n'

        except IndexError:
            pass

    # close package
    out += '}\n'

out += '@enduml\n'
with open('Documentation/class_full_auto.puml', 'w') as file:
    file.write(out)
