import os,subprocess
# ""D:\vscode\git\UploadingT1kt0kVideoAutomation\imgFolder""
def checkFolder(folder_name):
    base_path = input(r'Folder ImgFolder path(Ex: "D:\vscode\git\UploadingT1kt0kVideoAutomation\imgFolder"): ')
    folder_path = os.path.join(base_path,folder_name)
    if not os.path.exists(folder_path):
        # If not, create the folder_path
        os.makedirs(folder_path)
        print(f'Creating folder {folder_name}...')
def GetDevices():
        devices = subprocess.check_output("adb devices")
        p = str(devices).replace("b'List of devices attached","").replace('\\r\\n',"").replace(" ","").replace("'","").replace('b*daemonnotrunning.startingitnowonport5037**daemonstartedsuccessfully*Listofdevicesattached',"")
        if int(len(p)) > 0:
            listDevices = p.split("\\tdevice")
            listDevices.pop()
            return listDevices
        else:
            return 


if __name__ == "__main__":
    for device in GetDevices():
         checkFolder(device)
    