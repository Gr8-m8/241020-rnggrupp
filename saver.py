import json
import os

#simplify json save/load
class Saver:
    def __init__(self):
        os.makedirs(Saver.PATH, exist_ok=True)
    
    PATH = "data/"

    def save(self, path, content):
        try:
            open(Saver.PATH+path, "x")
        except:
            pass

        try:
            save_file = open(Saver.PATH+path, "w")
            save_file.write(json.dumps(content))
            save_file.close()
            print(f"Content: '{content}', saved to file '{path}'")
        except:
            print(f"Failed: Content: '{content}', saved to file '{path}'")
            pass

    def load(self, path):
        content = None
        try:
            save_file = open(Saver.PATH+path, "r")
            content = json.loads(save_file.read())
            save_file.close()
            print(f"Content: '{content}', loaded from file '{path}'")
        except:
            try:
                open(Saver.PATH+path, "x")
                print(f"file {path} created")
            except:
                print(f"Failed: file {path} created")
                pass
            
        return content