import subprocess
devices = subprocess.check_output("adb devices")
p = str(devices).replace("b'List of devices attached","").replace('\\r\\n',"").replace(" ","").replace("'","").replace('b*daemonnotrunning.startingitnowonport5037**daemonstartedsuccessfully*Listofdevicesattached',"")
if int(len(p)) > 0:
    listDevices = p.split("\\tdevice")
    listDevices.pop()

print(listDevices)