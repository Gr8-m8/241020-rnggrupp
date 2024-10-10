from generator import GroupGenerator
from textdecoration import textdecoration as text

class Command:
    def __init__(self, func, command: list, desc: str, help: str) -> None:
        self.func = func
        self.command = command
        self.desc = desc
        self.help = help

class gui:
    def __init__(self, groupgenerator: GroupGenerator) -> None:
        self.gg = groupgenerator

    def filenamefiletype(self, args, force=True):
        filename = None
        filetype = None
        if not args:
            if force:
                filename = f"{input("Set File Name\n> ")}"
                filetype = f"{input("Set File Type\n> ")}"
        else:
            try: filetype = args[1] 
            except: filetype = None
            try: 
                filename = args[0]
                if len(filename.split('.'))>1:
                    filetype = filename.split('.')[1]
                    filename = filename.split('.')[0]
            except: filename = None

        return filename, filetype
    
    def main(self):
        main_loop_active = True
        while (main_loop_active):
            
            for command in self.commands[1:]:
                print(f"{text.CYAN}[{self.commands.index(command)}] {text.BLUE}{command.desc}{text.END}")
            print(f"{text.CYAN}[{self.commands.index(self.commands[0])}] {text.BLUE}{self.commands[0].desc}{text.END}")

            qinput = input(f"{text.YELLOW}> "); print(text.END)
            qinput = qinput.split(' ')

            for command in self.commands:
                if qinput[0] in command.command or qinput[0] == str(self.commands.index(command)):
                    command.func(self, qinput[1:])

    def add(self, args = None):
        if not args:
            names_in: str = [input(f"{text.YELLOW}Enter names you want to add:\n> ")]; print(text.END)
        else:
            names_in = args
        
        filename, filetype = self.filenamefiletype(names_in, force=False)
        if filename and filetype:
            if filetype == self.gg.saver.KEY_FILETYPE_CSV:
                names_in = self.gg.saver.CSVloadList(filename)
        
        print(f"{text.CYAN}Add:{text.END}")
        names_out = self.gg.add(names_in)
        print(f"\t{text.BLUE}{names_out}{text.END}") 
        #for name in names_out.split(' '):
        #    print(f"\t{text.BLUE}{name}{text.END}") 
        

    def remove(self, args = None):
        if not args:
            names_in = input(f"{text.YELLOW} Enter names you want to remove:\n> "); print(text.END)
        else:
            names_in = args

        print(f"{text.CYAN}Remove:{text.END}")
        names_out, namesNo_out = self.gg.remove(names_in)
        for name in names_out.split(' '):
            print(f"\t{text.BLUE}{name}{text.END}")

        if namesNo_out != "" and len(namesNo_out.split(' '))>0:
            print(f"{text.RED}Names are not in list")
            for name in namesNo_out.split(' '):
                print(f"\t{text.RED}{name}{text.END}")

    def sizeset(self, args = None):
        if not args:
            group_size_in = input(f"{text.YELLOW}Enter group size of generated groups:\n> "); print(text.END)    
        else:    
            group_size_in = args[0]

        group_size_out = self.gg.sizeset(group_size_in)
        if group_size_out:
            print(f"{text.CYAN}Size:{text.END}")
            print(f"\t{text.BLUE}{group_size_out}{text.END}")
        else:
            print(f"{text.RED}Invalid Input: {group_size_in}{text.END}")

    def gengroup(self, args = None):
        filename, filetype = self.filenamefiletype(args, force=False)
        groups, entries = self.gg.gengroup(filename, filetype)
        print(f"{text.CYAN}Generate:{text.END}")
        
        #delimiter = f"{text.END}, {text.UNDERLINE}{text.CYAN}"
        delimiter = f"\n\t\t"
        if groups:
            for group in groups:
                print(f"\t{text.BLUE}Group {groups.index(group)}: {delimiter}{delimiter.join(group)}{text.END}")
        else:
            print(f"No groups generated")
        
        print(f"\t{text.RED}Rest group:{delimiter}{delimiter.join(entries)}{text.END}")
    
    def qlist(self, args = None):
        entries, group_size, groups = self.gg.qlist()
        print(f"{text.CYAN}List:{text.END}")
        print(f"\t{text.BLUE}Persons: {", ".join(entries)}{text.END}")
        print(f"\t{text.BLUE}Group Size: {group_size}{text.END}")
        print(f"\t{text.BLUE}Latest Groups:{" ".join([f"\n\t\tGroup {groups[0].index(group)}: {", ".join(group)}" for group in groups[0]])}\n\t\tRest Group: {", ".join(groups[1])}{text.END}")
        print()

    def qexit(self, args = None):
        print(f"{text.PURPLE}Exit:{text.END}")
        exit(0)

    def save(self, args = None):
        filename, filetype = self.filenamefiletype(args)
        if self.gg.save(filename, filetype):
            print(f"Save {filename}.{filetype}")
        else:
            print(f"Failed: Save {filename}.{filetype}")

    def load(self, args = None):
        filename, filetype = self.filenamefiletype(args)

        if self.gg.load(filename, filetype):
            print(f"Load {filename}.{filetype}")
            self.qlist()
        else:
            print(f"Failed: Load {filename}.{filetype}")

    def help(self, args = None):
        for command in self.commands:
            print(f"{text.CYAN}{command.desc}: {text.BLUE}{command.command} {text.GREEN}{command.help}{text.END}")
        print()
    
    commands = [
        Command(qexit, ['exit','x','e'], "Exit", f"Exit Application"),
        Command(qlist, ['list','l', '='], "List", f"Lists List, Size, Last Group Generation"),
        Command(add, ['add','+','a'], "Add Person", f"Add Person to List {text.YELLOW}[PERSON PERSON PERSON ...]{text.END}"),
        Command(remove, ['remove','-','r'], "Remove Person", f"Remove Person from List {text.YELLOW}[PERSON PERSON PERSON ...]{text.END} OR {text.YELLOW}[ALL]{text.END}"),
        Command(sizeset, ['size','s'], "Set Group Size", f"Set Size for generated groups {text.YELLOW}[SIZE]{text.END}"),
        Command(gengroup, ['gen','*','g'], "Generate Group List", f"Generate groups by List and Size{text.END} OPTIONAL {text.YELLOW}[OUTPUTFILENAME FILETYPE]{text.END} OR {text.YELLOW}[OUTPUTFILENAME.FILETYPE]{text.END}"),
        Command(save, ['save'], "Save instance", f"Save current List and Size to File {text.YELLOW}[FILENAME FILETYPE]{text.END} OR {text.YELLOW}[FILENAME.FILETYPE]{text.END} (valid FILETYPE is 'csv' OR 'json')"),
        Command(load, ['load'], "Load instance", f"Load List and Size from File {text.YELLOW}[FILENAME FILETYPE]{text.END} OR {text.YELLOW}[FILENAME.FILETYPE]{text.END} (valid FILETYPE is 'csv' OR 'json')"),
        Command(help, ['help','?','h'], "Help", f"Display Commands"),
    ]


gg = GroupGenerator()
GUI = gui(gg)
try:
    GUI.main()
except KeyboardInterrupt:
    exit(1)