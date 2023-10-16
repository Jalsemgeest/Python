import sys
from time import sleep
from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pystray
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image
JakeIsCool = True

# 1. Find all the files within a directory
# 2. Move the file to another directory
# 3. If there is a file with the same name, rename the first file

sourceDir = 'C:/Users/cptli/Downloads/ExampleDir'

# print(exists(f'{sourceDir}/python.png'))
# for entry in scandir(sourceDir):
#     print(entry)
#     print(entry.is_dir())
#     print(entry.is_file())

imageDestDir = 'C:/Users/cptli/Downloads/ExampleDir/Images'

def moveFile(dest, currDir, name):
    # Check if the file exists first, rename if it does
    fileExists = exists(f'{dest}/{name}')
    newName = name
    if fileExists:
        filename, ext = splitext(name)
        count = 1
        while exists(f'{dest}/{newName}'):
            newName = f'{filename} ({str(count)}){ext}'
            count += 1
        oldName = join(currDir, name)
        newName = join(currDir, newName)
        rename(oldName, newName)
    move(newName, dest)

imageExt = ['.png', '.jpeg', '.jpg', '.jfi', '.jpe', '.jif', '.jfif', '.heif', '.heic',
            '.gif', '.svg', '.svg2', '.eps', '.webp', '.tiff', '.tif', '.ind', '.ai', '.psd']


class Watcher(FileSystemEventHandler):
    def on_modified(self, _):
        self.clean()
    
    def clean(self):
        with scandir(sourceDir) as entries:
            for entry in entries:
                if entry.is_dir():
                    continue
                for ext in imageExt:
                    if entry.name.endswith(ext):
                        moveFile(imageDestDir, sourceDir, entry.name)
                        break


watcher = Watcher()
observer = Observer()
observer.schedule(watcher, sourceDir, recursive=True)
observer.start()
# sleep(20)
# observer.stop()
# observer.join()

image = Image.new('RGB', (64, 64), 'red')
def stop(icon, _):
    observer.stop()
    observer.join()
    icon.stop()

tray = icon(
    'Computer Cleaner',
    icon=image,
    menu=menu(
        item('Exit', stop))
).run()






























# audioExt = ['.wav', '.wma', '.aac', '.mp3', '.flac', '.m4a', '.ogg', '.alac']
# videoExt = ['.webm', '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.mp4', '.m4p', '.m4v', '.avi',
#             '.wmv', '.mov', '.qt', '.flv', '.swf', '.avchd']
# docExt = ['.doc', '.docx', '.pdf']

# audioDestDir = 'C:/Users/cptli/Downloads/ExampleDir/Audio'
# videoDestDir = 'C:/Users/cptli/Downloads/ExampleDir/Video'
# docDestDir = 'C:/Users/cptli/Downloads/ExampleDir/Docs'

    #             for ext in audioExt:
    #                 if entry.name.endswith(ext):
    #                     moveFile(audioDestDir, entry, entry.name)
    #             for ext in videoExt:
    #                 if entry.name.endswith(ext):
    #                     moveFile(videoDestDir, entry, entry.name)
    #             for ext in docExt:
    #                 if entry.name.endswith(ext):
    #                     moveFile(docDestDir, entry, entry.name)