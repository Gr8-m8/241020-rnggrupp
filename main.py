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
        groups, entries = self.gg.gengroup()
        print(f"{text.CYAN}Generate:{text.END}")
        
        if groups:
            for group in groups:
                print(f"\tGroup {groups.index(group)}: {text.BLUE}{group}{text.END}")
        else:
            print(f"No groups generated")
        
        print(f"{text.RED}Rest group:\n\t{text.BLUE}{entries}{text.END}")
    
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

    def filenamefiletype(self, args):
        filename = None
        filetype = None
        if not args:
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
        Command(qexit, ['exit','x','e'], "Exit", "Exit Application"),
        Command(qlist, ['list','l', '='], "List", "Lists List and Size"),
        Command(add, ['add','+','a'], "Add Person", "Add Person to List [PERSON, PERSON, PERSON...]"),
        Command(remove, ['remove','-','r'], "Remove Person", "Remove Person from List [PERSON, PERSON, PERSON...]"),
        Command(sizeset, ['size','s'], "Set Group Size", "Set Size for generated groups [SIZE]"),
        Command(gengroup, ['gen','*','g'], "Generate Group List", "Generate groups by List and Size"),
        Command(save, ['save'], "Save instance", "Save current List and Size to File [FILENAME]"),
        Command(load, ['load'], "Load instance", "Load List and Size from File [FILENAME]"),
        Command(help, ['help','?','h'], "Help", "Display Commands"),
    ]


gg = GroupGenerator()
GUI = gui(gg)
try:
    GUI.main()
except KeyboardInterrupt:
    exit(1)