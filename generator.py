import random
from datetime import datetime

from saver import Saver

class GroupGenerator:
    def __init__(self) -> None:
        self.saver = Saver()

        self.entries = []
        self.group_size = 2
        self.groups = [[], []]

    def content(self):
        groups = {}
        for group in self.groups[0]:
            groups[f"{Saver.KEY_CONTENT_GROUP}{self.groups[0].index(group)}"] = group
        groups[Saver.KEY_CONTENT_GROUPREST] = self.groups[1]
        return {Saver.KEY_CONTENT_ENTRIES: self.entries, Saver.KEY_CONTENT_SIZE:self.group_size, Saver.KEY_CONTENT_GROUPS: groups}

    def add(self, names = []) -> str:
        retur = ""
        for name in names:
            self.entries.append(name)
            retur+=f"{name} "

        return retur
        

    def remove(self, names = []) -> str:
        retur = ""
        returNO = ""
        if names[0] in ['all']:
                self.entries = []
                return 'All', ""

        for name in names:
            if name in self.entries:
                self.entries.remove(name)
                retur+=f"{name} "
            else:
                returNO+=f"{name} "

        return retur, returNO

    def sizeset(self, size = 2) -> int:
        try:
            self.group_size = abs(int(size))
            return self.group_size
        except:
            return None
        

    def gengroup(self, filename = None, filetype = None) -> tuple:
        groups = []
        entries = self.entries.copy()
        
        while len(entries)>=self.group_size or self.group_size == 0:
            group = random.sample(entries, self.group_size)
            groups.append(group)
            [entries.remove(entry) for entry in group]
        
        if not len(groups)>0:
            return None, entries

        self.groups = groups.copy(), entries.copy()

        if filename:
            if not filetype:
                #filename = f"result {datetime.now().strftime('%Y-%m-%d [%H-%M-%S]')}"
                self.saver.save(filename, Saver.KEY_FILETYPE_JSON, self.content())
                self.saver.save(filename, Saver.KEY_FILETYPE_CSV, self.content())
            else:
                self.saver.save(filename, filetype, self.content())
                
        return groups, entries
    
    def qlist(self) -> tuple:
        return self.entries, self.group_size, self.groups

    def save(self, filename = datetime.now().strftime('%Y-%m-%d [%H-%M-%S]'), filetype = Saver.KEY_FILETYPE_CSV) -> str:
        if filetype:
            self.saver.save(filename, filetype, self.content())
            return f"{filename}.{filetype} <-- {self.content()}"
        else:
            for filetype in Saver.FileTypes():
                self.saver.save(filename, filetype, self.content())
            return f"{filename}.{Saver.FileTypes()} <-- {self.content()}"  
        return None

    def load(self, filename = None, filetype = None) -> str:
        if filename and filetype:
            content = self.saver.load(filename, filetype)
            if content:
                self.entries, self.group_size, self.groups = content
                return f"{filename}.{filetype} --> {content}"
            else:
                return None
        
        return None
