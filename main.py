from generator import GroupGenerator
from textdecoration import textdecoration as text

class Command:
    def __init__(self, func, command: list, desc: str, help: str, argsdesc: str = "") -> None:
        self.func = func
        self.command = command
        self.argsdesc = argsdesc
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
                print(text.YELLOW)
                filename = f"{input(f"Set File Name\n> ")}"
                filetype = f"{input(f"Set File Type\n> ")}"
                print(text.END)
        else:
            try: filetype = args[1] 
            except: filetype = None
            try: 
                filename = args[0]
                if len(filename.split('.'))>1:
                    filetype = filename.split('.')[1]
                    filename = filename.split('.')[0]
            except: filename = None

        if not filetype in self.gg.saver.FileTypes():
            filetype = None

        return filename, filetype
    
    def main(self):
        main_loop_active = True
        while (main_loop_active):
            print()
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
            names_in = self.gg.saver.loadList(filename, filetype)
        
        print(f"{text.CYAN}Add:{text.END}")
        names_out = self.gg.add(names_in)
        print(f"{text.BLUE}{names_out}{text.END}") 
        

    def remove(self, args = None):
        if not args:
            names_in = input(f"{text.YELLOW} Enter names you want to remove:\n> "); print(text.END)
        else:
            names_in = args

        print(f"{text.CYAN}Remove:{text.END}")
        names_out, namesNo_out = self.gg.remove(names_in)
        for name in names_out.split(' '):
            print(f"{text.BLUE}{name}{text.END}")

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
            print(f"{text.BLUE}{group_size_out}{text.END}")
        else:
            print(f"{text.RED}Invalid Input: {group_size_in}{text.END}")

    def gengroup(self, args = None):
        filename, filetype = self.filenamefiletype(args, force=False)
        groups, entries = self.gg.gengroup(filename, filetype)
        
        tag1 = f"{text.END}\n|- {text.GREEN}"
        print(f"{text.CYAN}Generate:{text.END}")
        if groups:
            for group in groups:
                print(f"{text.BLUE}Group {groups.index(group)+1}: {tag1}{tag1.join(group)}{text.END}")
        else:
            print(f"No groups generated")
        
        print(f"{text.RED}Rest group:{tag1}{tag1.join(entries)}{text.END}")
    
    def qlist(self, args = None):
        entries, group_size, groups = self.gg.qlist()
        try: groupsrest = groups[1]
        except: groupsrest = entries
        groups = groups[0]

        tag1 = f"{text.END}\n|- {text.BLUE}"
        tag2 = f"{text.END}\n:  |- {text.GREEN}"
        print(f"{text.CYAN}List:{text.END}")
        print(f"{text.BLUE}Persons: {f"{tag1}{text.GREEN}"}{f"{tag1}{text.GREEN}".join(entries)}{text.END}")
        print(f"{text.BLUE}Group Size: {text.GREEN}{group_size}{text.END}")
        print(f"{text.BLUE}Latest Groups:{" ".join([f"{tag1}Group {groups.index(group)+1}: {tag2}{tag2.join(group)}" for group in groups])}{tag1}Rest Group: {tag2}{tag2.join(groupsrest)}{text.END}")
        print(f"{text.BLUE}DataFiles: {f"{tag1}{text.GREEN}"}{f"{tag1}{text.GREEN}".join(self.gg.saver.DataFiles())}")

    def qexit(self, args = None):
        print(f"{text.PURPLE}Exit.{text.END}")
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
            print(f"{text.BLUE}{command.desc}:{text.END}\n|- {text.GREEN}{command.help}{text.END}\n|- Commands: {text.CYAN}{f" {text.END}OR{text.CYAN} ".join([f"'{command}'" for command in command.command])}{text.END} {command.argsdesc}{text.END}")
    
    commands = [
        Command(qexit, ['x','e', 'q', 'exit',], "Exit", f"Exit Application"),
        Command(qlist, ['!', 'list',], "List", f"Lists List, Size, Last Group Generation, Available Datafiles"),
        Command(add, ['+', 'add',], "Add Person", f"Add Person to List", f"ARGS: {text.YELLOW}[PERSON PERSON PERSON ...]{text.END} OR {text.YELLOW}[FILENAME FILETYPE]{text.END} OR {text.YELLOW}[FILENAME.FILETYPE]{text.END} {text.GREEN}valid FILE if FILETYPE is 'csv' AND FILELOCATION is 'data/'{text.END}"),
        Command(remove, ['-','remove','rem'], "Remove Person", f"Remove Person from List", f"ARGS: {text.YELLOW}[PERSON PERSON PERSON ...]{text.END} OR {text.YELLOW}[ALL]{text.END}"),
        Command(sizeset, ['=', '#','size',], "Set Group Size", f"Set Size for generated groups", f"ARGS: {text.YELLOW}[SIZE]{text.END}"),
        Command(gengroup, ['*','generate','gen',], "Generate Group List", f"Generate groups by List and Size", f"OPTIONAL ARGS: {text.YELLOW}[OUTPUTFILENAME FILETYPE]{text.END} OR {text.YELLOW}[OUTPUTFILENAME.FILETYPE]{text.END} {text.GREEN}OUTPUTFILELOCATION is 'data/'{text.END}"),
        Command(save, ['>>', 's', 'save',], "Save instance", f"Save current List and Size to File", f"ARGS: {text.YELLOW}[FILENAME FILETYPE]{text.END} OR {text.YELLOW}[FILENAME.FILETYPE]{text.END} {text.GREEN}valid FILE if FILETYPE is 'csv' OR 'json' AND FILELOCATION is 'data/'{text.END}"),
        Command(load, ['<<', 'l', 'load',], "Load instance", f"Load List and Size from File", f"ARGS: {text.YELLOW}[FILENAME FILETYPE]{text.END} OR {text.YELLOW}[FILENAME.FILETYPE]{text.END} {text.GREEN}valid FILE if FILETYPE is 'csv' OR 'json' AND FILELOCATION is 'data/'{text.END}"),
        Command(help, ['?', 'help','h',], "Help", f"Display Commands"),
    ]


gg = GroupGenerator()
GUI = gui(gg)
try:
    GUI.main()
except KeyboardInterrupt:
    print()
    GUI.qexit()
    exit(1)