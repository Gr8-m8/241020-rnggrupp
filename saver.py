import json
import os
import csv

#simplify json save/load
class Saver:
    def __init__(self):
        os.makedirs(Saver.PATH, exist_ok=True)
    
    PATH = "data/"

    KEY_FILETYPE_JSON = 'json'
    KEY_FILETYPE_CSV = 'csv'
    KEY_FILETYPE_EXCEL = 'xlsx'

    KEY_CONTENT_ENTRIES = 'entries'
    KEY_CONTENT_SIZE = 'size'
    KEY_CONTENT_GROUPS = 'groups'
    KEY_CONTENT_GROUP = 'group'
    KEY_CONTENT_GROUPREST = 'restgroup'

    @staticmethod
    def FileTypes():
        return [Saver.KEY_FILETYPE_JSON]+[Saver.KEY_FILETYPE_CSV]

    def save(self, filename, filetype, content):
        if (filetype in self.FileTypes()):
            if (not os.path.isfile(f"{Saver.PATH}{filename}.{filetype}")):
                open(f"{Saver.PATH}{filename}.{filetype}", "x")
        else:
            print(f"filetype: '{filetype}' not supported")
            return False

        if filetype == Saver.KEY_FILETYPE_JSON:
            return self.JSONsave(f"{filename}.{filetype}", content)
        
        if filetype == Saver.KEY_FILETYPE_CSV:
            return self.CSVsave(f"{filename}.{filetype}", content)
        
        return False
    
    def load(self, filename, filetype):
        if not os.path.isfile(f"{Saver.PATH}{filename}.{filetype}"):
            return None

        if filetype == Saver.KEY_FILETYPE_JSON:
            return self.JSONload(f"{filename}.{filetype}")
        
        if filetype == Saver.KEY_FILETYPE_CSV:
            return self.CSVload(f"{filename}.{filetype}")
        return None

    def JSONsave(self, name, content):
        try:
            save_file = open(Saver.PATH+name, "w")
            save_file.write(json.dumps(content))
            save_file.close()
            print(f"'{content}' --> '{name}'")
            return True
        except:
            print(f"'{content}' -X-> '{name}'")
            return False

    def JSONload(self, name):
        content = None
        try:
            save_file = open(Saver.PATH+name, "r")
            content = json.loads(save_file.read())
            save_file.close()
        except:
            return content
        
        entries = content[Saver.KEY_CONTENT_ENTRIES]
        group_size = content[Saver.KEY_CONTENT_SIZE]
        groupcontent = content[Saver.KEY_CONTENT_GROUPS]
        groups = [v for k,v in groupcontent.items()]
        groups.remove(groups[-1])
        restgroup = groupcontent[Saver.KEY_CONTENT_GROUPREST]
        return entries, group_size, [groups, restgroup]
            
    def CSVsave(self, name, content: dict):
        with open(Saver.PATH+name, 'w', newline='') as savefile:        
            fieldnames = [content.keys()]
            fieldnames += [content[Saver.KEY_CONTENT_GROUPS].keys()]
            writer = csv.writer(savefile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            row = [Saver.KEY_CONTENT_ENTRIES]+content[Saver.KEY_CONTENT_ENTRIES]
            writer.writerow(row)
            row = [Saver.KEY_CONTENT_SIZE]+[content[Saver.KEY_CONTENT_SIZE]]
            writer.writerow(row)
            groups = content[Saver.KEY_CONTENT_GROUPS]
            for id, group in groups.items():
                if not id == Saver.KEY_CONTENT_GROUPREST:
                    row = [id]+group
                    writer.writerow(row)
            row = [Saver.KEY_CONTENT_GROUPREST]+groups[Saver.KEY_CONTENT_GROUPREST]
            writer.writerow(row)
            
    def CSVload(self, name):
        entries = None
        size = None
        groups = []
        restgroup = None
        with open(Saver.PATH+name, newline='') as savefile:
            reader = csv.reader(savefile, delimiter=" ", quotechar="|")
            for row in reader:
                if row[0] == self.KEY_CONTENT_ENTRIES:
                    entries = row[1:]
                if row[0] == self.KEY_CONTENT_SIZE:
                    size = int(row[1])
                if row[0].startswith(self.KEY_CONTENT_GROUP):
                    groups.append(row[1:])
                if row[0] == self.KEY_CONTENT_GROUPREST:
                    restgroup = row[1:]
        return entries, size, [groups, restgroup]
    
    def loadList(self, filename, filetype):
        entries = []
        path = f"{Saver.PATH}{filename}.{filetype}"
        if not os.path.isfile(path):
            print(f"FAILED: FILE {path}")
            return entries
        else:
            print(f"FILE {path}")

        if filetype == Saver.KEY_FILETYPE_CSV:
            return self.CSVloadList(path)
        
        return entries
        #if filetype == Saver.KEY_FILETYPE_EXCEL:
        #    return self.EXCELloadList(path)


    def CSVloadList(self, path):
        entries = []
        with open(path, "r", newline='') as savefile:
            reader = csv.DictReader(savefile, delimiter=',', quotechar='|')
            headers = reader.fieldnames
            närvaro = ['x', 'X']
            for row in reader:
                if row[headers[-1]] in närvaro:
                    name = row[headers[0]] 
                    try: name += f" {row[headers[1]]}"
                    except: pass
                    entries.append(f"'{name}'")
        return entries

    def EXCELloadList(self, path):
        entries = []
        savefile = open(path, "r")
        content = savefile.readlines()
        savefile.close()
        print(content)