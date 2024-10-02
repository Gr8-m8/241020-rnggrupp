from saver import Saver
import random

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

class GroupGenerator:
    def __init__(self) -> None:
        self.saver = Saver()

        self.entries = []
        self.group_size = 1
        self.groups = []

    KEY_FUNC = 0
    KEY_COMMAND = 1
    KEY_DESC = 2


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
            for entry in group:
                entries.remove(entry)
            print(f"\t{text.BLUE}{group}{text.END}")
        
        print(f"{text.RED}Rest group:\n\t{text.BLUE}{entries}{text.END}")

        if not len(groups)>0:
            print(f"{text.RED}No one is in groups{text.END}")
    
    def qlist(self, args = None):
        print(f"{text.CYAN}List:{text.END}")
        print(f"\t{text.BLUE}{self.entries}{text.END}")
        print(f"\t{text.BLUE}{self.group_size}{text.END}")

    def qexit(self, args = None):
        print(f"{text.PURPLE}Exit:{text.END}")
        exit(0)

    def save(self, args):
        qinput = None
        if not args:
            qinput = f"{input("Set File Name\n> ")}"
        else:
            qinput = f"{args[0]}"
        
        self.saver.save(f"{qinput}.json", {"size": self.group_size, "entries": self.entries})

    def load(self, args):
        qinput = None
        if not args:
            qinput = f"{input("Get File Name\n> ")}"
        else:
            qinput = f"{args[0]}"

        data = self.saver.load(f"{qinput}.json")
        self.entries = data['entries']
        self.group_size = data['size']

    def main(self):

        commands = [
            [self.qlist, ['list','l', '='], "List"],
            [self.add, ['add','+','a'], "Add Person"],
            [self.remove, ['remove','-','r'], "Remove Person"],
            [self.sizeset, ['size','s'], "Set Group Size"],
            [self.gengroup, ['gen','*','g'], "Generate Group List"],
            [self.save, ['save'], "Save instance"],
            [self.load, ['load'], "Load instance"],
            [self.qexit, ['exit','x','e'], "Exit"],
        ]
        
        main_loop_active = True
        while (main_loop_active):
            
            for command in commands:
                print(f"{text.CYAN}[{command[self.KEY_COMMAND][0]}] {text.BLUE}{command[self.KEY_DESC]}{text.END}")

            qinput = input(f"{text.YELLOW}> "); print(text.END)
            qinput = qinput.split(' ')

            for command in commands:
                if qinput[0] in command[self.KEY_COMMAND]:
                    command[self.KEY_FUNC](qinput[1:])

gr = GroupGenerator()
try:
    gr.main()
except KeyboardInterrupt:
    exit(1)