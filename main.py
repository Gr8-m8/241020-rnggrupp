from saver import Saver
import random
from datetime import datetime

class text:
    #console text decoration codes
    BGWHITE = '\033[107m'
    BGCYAN = '\033[106m'
    BGPURPLE = '\033[105m'
    BGBLUE = '\033[104m'
    BGYELLOW = '\033[103m'
    BGGREEN = '\033[102m'
    BGRED = '\033[101m'
    BGGRAY = '\033[100m'
    BGBLACK = '\033[40m'
    
    CYAN = '\033[96m'
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    GRAY = '\033[90m'

    STRIKETHROUGH = '\033[28m'
    UNDERLINE = '\033[4m'
    ITALICS = '\033[3m'
    BOLD = '\033[1m'
    END = '\033[0m'

class Command:
    def __init__(self, func, command, desc, help) -> None:
        self.func = func
        self.command = command
        self.desc = desc
        self.help = help

class GroupGenerator:
    def __init__(self) -> None:
        self.saver = Saver()

        self.entries = []
        self.group_size = 1
        self.groups = [],[]

    KEY_FUNC = 0
    KEY_COMMAND = 1
    KEY_DESC = 2
    KEY_HELP = 3


    def add(self, args = []):
        for name in args:
            self.entries.append(name)
        

    def remove(self, args = []):
        if args[0] in ['all']:
                self.entries = []
                return

        for name in args:
            self.entries.remove(name)
            print(f"\t{text.BLUE}{name}{text.END}")

    def sizeset(self, args = 2):
        try:
            self.group_size = abs(int(args[0]))
            return self.group_size
        except:
            return None
        

    def gengroup(self, args = None):
        groups = []
        entries = self.entries.copy()
        
        while len(entries)>=self.group_size or self.group_size == 0:
            group = random.sample(entries, self.group_size)
            groups.append(group)
            [entries.remove(entry) for entry in group]
        
        if not len(groups)>0:
            return None, entries

        self.groups = groups.copy(), entries.copy()
        self.saver.save(f"result {datetime.now().strftime('%Y-%m-%d [%H-%M-%S]')}.json", {"groups": groups, "Rest Group": entries})
        return groups, entries
    
    def qlist(self, args = None):
        return self.entries, self.group_size, self.groups

    def save(self, args = datetime.now().strftime('%Y-%m-%d [%H-%M-%S]')):
        if args[0]:
            name = f"{args[0]}.json"
            content = {"size": self.group_size, "entries": self.entries}
            self.saver.save(name, content)
            return name
        else:
            return None

    def load(self, args = None):
        if args:
            name = f"{args[0]}.json"
            data = self.saver.load(name)
            self.entries = data['entries']
            self.group_size = data['size']
            return name, {self.entries, self.group_size}
        else:
            return None

class gui:
    def __init__(self, groupgenerator: GroupGenerator) -> None:
        self.gg = groupgenerator

    def main(self):
        main_loop_active = True
        while (main_loop_active):
            
            for command in self.commands:
                #print(f"{text.CYAN}[{command[self.KEY_COMMAND][0]}] {text.BLUE}{command[self.KEY_DESC]}{text.END}")
                print(f"{text.CYAN}[{self.commands.index(command)}] {text.BLUE}{command[self.KEY_DESC]}{text.END}")

            qinput = input(f"{text.YELLOW}> "); print(text.END)
            qinput = qinput.split(' ')

            for command in self.commands:
                if qinput[0] in command[self.KEY_COMMAND] or qinput[0] == str(self.commands.index(command)):
                    command[self.KEY_FUNC](self, qinput[1:])

    def add(self, args = None):
        print(f"{text.CYAN}Add:{text.END}")
        if not args:
            name = input(f"{text.YELLOW}Enter the name you want to add list:\n> "); print(text.END)
            self.entries.append(name)
            print(f"\t{text.BLUE}{name}{text.END}")
        else:
            for name in args:
                self.entries.append(name)
                print(f"\t{text.BLUE}{name}{text.END}")
        

    def remove(self, args = None):
        print(f"{text.CYAN}Remove:{text.END}")
        if not args:
            name = input(f"{text.YELLOW} Enter the name you want to remove:\n> "); print(text.END)
            self.entries.remove(name)
            print(f"\t{text.BLUE}{name}{text.END}")
        else:
            if args[0] in ['all']:
                self.entries = []
                return

            for name in args:
                self.entries.remove(name)
                print(f"\t{text.BLUE}{name}{text.END}")

    def sizeset(self, args = None):
        try:
            print(f"{text.CYAN}Size:{text.END}")
            if not args:
                self.group_size = abs(int(input(f"{text.YELLOW}Enter the group size you want to create:\n> "))); print(text.END)
                print(f"\t{text.BLUE}{self.group_size}{text.END}")
            else:    
                self.group_size = abs(int(args[0]))
                print(f"\t{text.BLUE}{self.group_size}{text.END}")
        except:
            print(f"{text.RED}Invalid Input{text.END}")
        

    def gengroup(self, args = None):
        print(f"{text.CYAN}Generate:{text.END}")
        groups = []
        entries = self.entries.copy()
        
        while len(entries)>=self.group_size or self.group_size == 0:
            group = random.sample(entries, self.group_size)
            groups.append(group)
            [entries.remove(entry) for entry in group]
                
            print(f"\t{text.BLUE}{group}{text.END}")
        
        print(f"{text.RED}Rest group:\n\t{text.BLUE}{entries}{text.END}")

        if not len(groups)>0:
            print(f"{text.RED}No one is in groups{text.END}")

        self.saver.save(f"result {datetime.now().strftime('%Y-%m-%d_[%H-%M-%S]')}.json", {"groups": groups, "Rest Group": entries})
    
    def qlist(self, args = None):
        print(f"{text.CYAN}List:{text.END}")
        print(f"\t{text.BLUE}{self.entries}{text.END}")
        print(f"\t{text.BLUE}{self.group_size}{text.END}")

    def qexit(self, args = None):
        print(f"{text.PURPLE}Exit:{text.END}")
        exit(0)

    def save(self, args = None):
        qinput = None
        if not args:
            qinput = f"{input("Set File Name\n> ")}"
        else:
            qinput = f"{args[0]}"
        
        self.saver.save(f"{qinput}.json", {"size": self.group_size, "entries": self.entries})

    def load(self, args = None):
        qinput = None
        if not args:
            qinput = f"{input("Get File Name\n> ")}"
        else:
            qinput = f"{args[0]}"

        data = self.saver.load(f"{qinput}.json")
        self.entries = data['entries']
        self.group_size = data['size']

    def help(self, args = None):
        commands = self.commands
        for command in commands:
            print(f"{text.CYAN}{command[self.KEY_DESC]}: {text.BLUE}{command[self.KEY_COMMAND]} {text.GREEN}{command[self.KEY_HELP]}{text.END}")
        print()
    
    commands = [
        [qlist, ['list','l', '='], "List", "Lists List and Size"],
        [add, ['add','+','a'], "Add Person", "Add Person to List [PERSON, PERSON, PERSON...]"],
        [remove, ['remove','-','r'], "Remove Person", "Remove Person from List [PERSON, PERSON, PERSON...]"],
        [sizeset, ['size','s'], "Set Group Size", "Set Size for generated groups [SIZE]"],
        [gengroup, ['gen','*','g'], "Generate Group List", "Generate groups by List and Size"],
        [save, ['save'], "Save instance", "Save current List and Size to File [FILENAME]"],
        [load, ['load'], "Load instance", "Load List and Size from File [FILENAME]"],
        [qexit, ['exit','x','e'], "Exit", "Exit Application"],
        [help, ['help','?','h'], "Help", "Display Commands"],
    ]



    

gg = GroupGenerator()
GUI = gui(gg)
try:
    GUI.main()
except KeyboardInterrupt:
    exit(1)