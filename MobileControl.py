import os,time

import threading,subprocess,base64,cv2,random,requests,shutil
import numpy as np
from datetime import datetime
from  xml.dom.minidom import parse
import time
import pandas as pd
from random import randint


# def proxy():
#     https_proxy = requests.get(f'http://proxy.shoplike.vn/Api/getNewProxy?access_token=198e93ed1c3818afab7fdee82d519d67&location=&provider=')
#     if https_proxy.json()["status"] == "error":
#         return
#     else :
#      https_proxyz = https_proxy.json()["data"] 
#     yz = https_proxyz["proxy"]
#     return yz 
    
# def resetServer():
#         """
#         Reset Server ADB
#         """
#         subprocess.call("adb kill-server", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
#         time.sleep(2)
#         subprocess.call("adb start-server", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
#         time.sleep(3)
def LDpath():
    with open('ldplayer_path.txt', 'r') as file:
        content = file.read()
        file.close()
    return content
def ImgFolderPath():
    base_path = os.getcwd()
    imgFolder = os.path.join(base_path,'imgFolder')
    return imgFolder
path = ImgFolderPath()
def getImgFolder(path= path):
    return path
def move_file(folder_name):
    imgFolder = getImgFolder()
    imgs = os.listdir(imgFolder)
    imgs = [img for img in imgs if '.' in img]
    choosenImg = random.choice(imgs)
    imgPath = os.path.join(imgFolder,choosenImg)
    destination_path = os.path.join(imgFolder,folder_name)
    while True:
        try:
            shutil.move(imgPath, destination_path)
            print(f"File '{choosenImg}' moved successfully from '{imgFolder}' to '{destination_path}'")
            break
        except:
            continue
def remove_file(folder_name):
    imgFolder = getImgFolder()
    trash_bin = os.path.join(imgFolder,'uploadeditems')
    folder_path = os.path.join(imgFolder,folder_name)
    imgs = os.listdir(folder_path)
    imgs = [img for img in imgs if '.' in img]
    for i in range(len(imgs)):
        choosenImg = imgs[i]
        imgPath = os.path.join(folder_path,choosenImg)
        while True:
            try:
                shutil.move(imgPath, trash_bin)
                print(f"File '{choosenImg}' removed successfully from '{imgPath}' to '{trash_bin}'")
                break
            except:
                continue
def checkFolder(folder_name):
    base_path = getImgFolder()
    folder_path = os.path.join(base_path,folder_name)
    if not os.path.exists(folder_path):
        # If not, create the folder_path
        os.makedirs(folder_path)
def crop_image(input_path, x, y, width, height):
    # Read the image
    image = cv2.imread(input_path)

    # Crop the image
    cropped_image = image[y:y+height, x:x+width]

    # Save the cropped image
    return cropped_image
def bypass_slide(devices):
    pipe = subprocess.Popen(f'adb -s {devices} exec-out screencap -p',
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, shell=True)
        #image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
    image_bytes = pipe.stdout.read()
    image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    # img = image[430:765, 102:648] # cắt chỗ có captcha # cut zone captcha
    img = image[360:580, 100:440]
    # img = image[400:1505, 80:1248]
    #cv2.imshow("a", img)
    #cv2.waitKey(0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img3 = cv2.Canny(gray, 200, 200, L2gradient=True)
    kernel = np.ones([23,23]) # Tạo kernel
    kernel[2:,2:] = -0.1
    im = cv2.filter2D(img3/255, -1, kernel)
    im1 = im[:,:125]
    y1,x1 = np.argmax(im1)//im1.shape[1], np.argmax(im1)%im1.shape[1] # Tìm vị trí 1 chính xác
    im2 = im[:,125:]
    y2,x2 = np.argmax(im2)//im2.shape[1], np.argmax(im2)%im2.shape[1] + 125 # Tìm vị trí 1 chính xác
    # cv2.rectangle(img, (x1,y1), (x1+50, y1+50), 255, 2)
    # cv2.rectangle(img, (x2,y2), (x2+50, y2+50), 255, 2)
    # plt.imshow(img)
    # plt.show()
    return x2-x1

class Auto:
    def __init__(self,handle):
        self.handle = handle
    def screen_capture(self):
        #os.system(f'adb -s {self.handle} exec-out screencap -p > {name}.png')
        pipe = subprocess.Popen(f'adb -s {self.handle} exec-out screencap -p',
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, shell=True)
        #image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
        image_bytes = pipe.stdout.read()
        image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        return image
    def changeProxy(self, ip):
        """
        Input Proxy Http IP:PORT
        Thêm Proxy Http IP:PORT
        """
        subprocess.call(f'adb -s {self.handle} shell settings put global http_proxy {ip}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def remProxy(self):
        """
        Input Proxy Http IP:PORT
        Thêm Proxy Http IP:PORT
        """
        subprocess.call(f'adb -s {self.handle} shell settings put global http_proxy :0', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def runCMD(self,command):
        subprocess.call(command,stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,shell=True)
    def checkoutputCMD(self,command):
        return subprocess.check_output(command,shell=True, text=True)
    def GetScreenResolution(self):
        command = f'adb -s {self.handle} shell wm size'
        result = str(subprocess.check_output(command, shell=True, text=True)).replace(' ','').replace('\n','').split(':')[-1].split('x')
        return [int(item) for item in result]
    def Enter(self):
        subprocess.call(f'adb -s {self.handle} shell input keyevent KEYCODE_ENTER', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def swipeUp(self):
        x_res, y_res = self.GetScreenResolution()
        self.swipe(x_res//2, y_res*0.9, x_res//2, y_res*0.2)
    def BackToHomeScreen(self):
        subprocess.call(f'adb -s {self.handle} shell input keyevent KEYCODE_HOME', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def click(self,x,y):
        subprocess.call(f'adb -s {self.handle} shell input tap {x} {y}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def swipe(self, x1, y1, x2, y2):
        subprocess.call(f"adb -s {self.handle} shell input touchscreen swipe {x1} {y1} {x2} {y2} 1000", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def Back(self):
        subprocess.call(f"adb -s {self.handle} shell input keyevent 3", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def DeleteCache(self, package):
        subprocess.check_output(f"adb -s {self.handle} shell pm clear {package}", stderr=subprocess.STDOUT)
    def off(self, package):
        subprocess.call(f"adb -s {self.handle} shell am force-stop {package}", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def InpuText(self, text=None, VN=None):
        if text == None:
            text =  str(base64.b64encode(VN.encode('utf-8')))[1:]
            subprocess.call(f"adb -s {self.handle} shell ime set com.android.adbkeyboard/.AdbIME", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            subprocess.call(f"adb -s {self.handle} shell am broadcast -a ADB_INPUT_B64 --es msg {text}", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            return
        subprocess.call(f"adb -s {self.handle} shell input text '{text}'", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def find(self,img='',threshold=0.99):
        img = cv2.imread(img) #sys.path[0]+"/"+img)
        img2 = self.screen_capture()    
        result = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        retVal = list(zip(*loc[::-1]))
        return retVal
    def findTF(self,img='',threshold=0.99):
        img = cv2.imread(img) #sys.path[0]+"/"+img)
        img2 = self.screen_capture()    
        result = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        retVal = list(zip(*loc[::-1]))
        if len(retVal) != 0: return True
        else: return False
    def findCustom2(self,img='',threshold=0.99):
        img2 = self.screen_capture()    
        result = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        retVal = list(zip(*loc[::-1]))
        return retVal
    def findCustom(self,img='',img2='',threshold=0.99):
        result = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        retVal = list(zip(*loc[::-1]))
        return retVal
    def tapimg(self,img='',threshold=0.99):
        img = cv2.imread(img) #sys.path[0]+"/"+img)
        # tap = cv2.imread(tap)
        img2 = self.screen_capture()    
        result = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        retVal = list(zip(*loc[::-1]))
        # result2 = cv2.matchTemplate(img,tap,cv2.TM_CCOEFF_NORMED)
        # loc2 = np.where(result2 >= threshold)
        # retVal2 = list(zip(*loc2[::-1]))
        if retVal > [(0, 0)]:
            self.click(retVal[0][0],retVal[0][1])
            
        else:
            return 0
    def slideCaptcha(self,x,y):
        # adb.excuteAdb(sr, "adb shell screencap -p /sdcard/cap.png")
        # adb.excuteAdb(sr, f"adb pull /sdcard/cap.png {sr}/captcha.png")
        captcha = bypass_slide(self.handle)
        self.swipe(round(x), round(y), int(x)+int(captcha), round(y))
        return True
    def showDevice(self, width: int, height: int, x:int , y: int, title: str):
        """Hiển thị điện thoại của bạn lên màn hình máy tính"""
        subprocess.Popen(f'scrcpy -s {self.handle} --window-title "{title}" --window-x {x} --window-y {y} --window-width {width} --window-height {height}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def DumpXML(self):
        name = self.handle
        if ":" in self.handle:
            name = name.replace(":", "").replace(".", "")
        #print(name)
        os.system(f"adb -s {self.handle} shell uiautomator dump && adb -s {self.handle} pull /sdcard/window_dump.xml {name}.xml")
        return name
    def GetXml(self):
        self.DumpXML()
        with parse(self.handle.replace(":", "").replace(".", "")+".xml") as file:
            node = file.getElementsByTagName("node")
            for element in node:
                text = element.getAttribute("text")
                classname = element.getAttribute("class")
                contentdesc = element.getAttribute("content-desc")
                print(classname, text, contentdesc)

    def TapXml(self, text=None, classname=None, content=None, taps=1, typesearch="text&class"):
        self.DumpXML()
        devices = self.handle
        with parse(devices.replace(":", "").replace(".", "")+".xml") as file:
            node = file.getElementsByTagName("node")
            for element in node:
                name = element.getAttribute("text")
                classnames = element.getAttribute("class")
                contentdesc = element.getAttribute("content-desc")
                x, y = element.getAttribute("bounds").split("][")[0].replace("[", "").split(",")
                if name == text and classnames == classname and typesearch == "text&class" or typesearch == "text&class":
                    print("x:"+x, "y:"+y, "Text:"+name)
                    for tap in range(taps):
                        self.click(x, y)
                elif contentdesc == content and classnames == classname and typesearch == "content&class" or typesearch == "class&content":
                    print("x:"+x, "y:"+y, "Text:"+name)
                    for tap in range(taps):
                        self.Click(x, y)
                elif name == text and contentdesc == content and typesearch == "content&text" or typesearch == "text&content":
                    print("x:"+x, "y:"+y, "Text:"+name)
                    for tap in range(taps):
                        self.Click(x, y)




def GetDevices():
        devices = subprocess.check_output("adb devices")
        p = str(devices).replace("b'List of devices attached","").replace('\\r\\n',"").replace(" ","").replace("'","").replace('b*daemonnotrunning.startingitnowonport5037**daemonstartedsuccessfully*Listofdevicesattached',"")
        if int(len(p)) > 0:
            listDevices = p.split("\\tdevice")
            listDevices.pop()
            return listDevices
        else:
            return 

ldpath = LDpath()

class starts(threading.Thread):
    def __init__(self, nameLD, i):
        super().__init__()
        self.nameLD = nameLD
        self.device = i
        self.auto = Auto(self.nameLD)
        self.openedApps = []
    def random_music(self):
        return random.randint(0,38)
    def random_amount_of_the_uploaded_video(self):
        return random.randint(1,10)
    def TiktokMusics(self, num):
        df = pd.read_csv('tiktokmusics.csv')
        # Extract the second column values into a list
        names = df.iloc[:, 0].tolist()
        links = df.iloc[:, 1].tolist()
        # Enumerate the values
        enumerated_links = list(enumerate(links))
        # Return the link has index equal to num 
        return next((value for index, value in enumerated_links if index == num), None)
    def isHome(self):
        auto = self.auto

        systemapp_img = 'imgs/systemapp.png'
        while True:
            systemapp =auto.findTF(systemapp_img)
            if systemapp:
                break

    def OpenGallery(self,device):
        target = "com.android.gallery3d"
        self.openedApps.append(target)
        cmd_target = f"{target}/com.android.gallery3d.app.GalleryActivity"
        command = f'adb -s {device} shell am start -n {cmd_target}'
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell= True)
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell= True)
    def OpenTikTok(self,device):
        target = 'com.ss.android.ugc.trill'
        self.openedApps.append(target)
        cmd_target = f'{target}/com.ss.android.ugc.aweme.splash.SplashActivity'
        command = f'adb -s {device} shell am start -n {cmd_target}'
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell= True)
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell= True)
    def OpenBrowser(self,device):
        target = 'com.android.browser'
        self.openedApps.append(target)
        cmd_target = f'{target}/com.android.browser.BrowserActivity'
        command = f'adb -s {device} shell am start -n {cmd_target}'
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell= True)
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell= True)
    def OpenSetting(self,device):
        target = 'com.android.settings'
        self.openedApps.append(target)
        cmd_target = f'{target}/com.android.settings.Settings'
        command = f'adb -s {device} shell am start -n {cmd_target}'
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell= True)
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell= True)
    def OpenDocumentSUI(self,device):
        target = 'com.android.documentsui'
        self.openedApps.append(target)
        cmd_target = f'{target}/com.android.documentsui.LauncherActivity'
        command = f'adb -s {device} shell am start -n {cmd_target}'
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell= True)
        subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell= True)
    def clearOpenedApps(self,device):
        auto = self.auto
        auto.BackToHomeScreen()
        time.sleep(2)
        for target in self.openedApps:
            command = f'adb -s {device} shell pm clear {target}'
            subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell= True)
            print(f'{auto.handle}: {target} closed!')
            time.sleep(1)
    def UploadVideoButton(self):
        auto = self.auto
        button = 'imgs/uploadvideobutton.png'
        auto.tapimg(button)
    def SelectVideoSite(self):
        auto = self.auto
        video_button_img = 'imgs/videobutton.png'
        auto.tapimg(video_button_img)
    def PressNext(self):
        auto = self.auto
        diaryButton = 'imgs/yourdiary.png'
        nextButton = 'imgs/next.png'
        upButton = "imgs/upButton.png"

        x_rex,y_res = auto.GetScreenResolution()
        while True:
            cond1 = auto.findTF(diaryButton)
            cond2 = auto.findTF(nextButton)
            if any([cond1,cond2]):
                auto.click(x_rex*0.79,y_res*0.95)
                time.sleep(3)
            if auto.findTF(upButton):
                break
                  
    def GoPublic(self):
        auto = self.auto
        x_res,y_res = auto.GetScreenResolution()
        upButton = 'imgs/upButton.png'
        auto.tapimg(upButton)
        print(f'{auto.handle}: The video has been public!')


        while True:
            target = 'imgs/complete.png'
            if auto.findTF(target):

                break
    # Get click position of the video
    def GetInfo(self):
        auto = self.auto

        x_res, y_res = auto.GetScreenResolution()
        # _3_x_res = x_res//3
        x_mean = x_res//3
        # x_blank = x_res * 0.01
        x1 = x_mean*0.5
        x2 = x_mean*1.5
        x3 = x_mean*2.5

        header = 172
        body = 540
        footer = y_res - header - body
        y_mean = body//3
        y1 = header + y_mean*0.5
        y2 = header + y_mean*1.5
        y3 = header + y_mean*2.5

        return x1, x2, x3, y1, y2, y3, header, body, footer
    # Swipe up to refresh body which contain videos
    def refreshVideo(self):
        auto = self.auto
        x1, x2, x3, y1, y2, y3, header, body, footer = self.GetInfo()
        x_res, y_res = auto.GetScreenResolution()
        y_start = header + body
        y_end = header + 15

        auto.swipe(x_res//2, y_start, x_res//2, y_end)
    # Get to the music directly
    def GoToMusicLink(self,index):
        auto = self.auto

        x_res, y_res = auto.GetScreenResolution()

        # Open System Apps folder
        print(f'{auto.handle}: Opening browser...')
        self.OpenBrowser(index)
        time.sleep(2)
        # Click at the searching bar
        auto.click(x_res//2,y_res*0.076)
        # Select music
        print(f'{auto.handle}: Choosing random music...')
        music = self.TiktokMusics(self.random_music())
        try:
            # Access the music link
            auto.InpuText(music)
        except:
            music = self.TiktokMusics(self.random_music())
            auto.InpuText(music)
        auto.Enter()
        time.sleep(10)
        # Open tiktok   
        print(f'{auto.handle}: Opening TikTok...')
        while True:
            muavuinoibuon = 'imgs/muavuinoibuon.png'
            if auto.findTF(muavuinoibuon):
                time.sleep(3)
                auto.click(x_res//2, y_res*0.75)
                print('Special case!')
                break
            case1 = 'imgs/seemoremusics.png'
            case1_found = auto.findTF(case1)
            if case1_found: 
                auto.click(x_res//2,y_res*0.873)
                print("Case 1 found!")
                break
            case2 = 'imgs/enjoyallthefeature2.png'
            case2_found = auto.findTF(case2)
            if case2_found:
                auto.click(x_res//2,y_res*0.75)
                print("Case 2 found!")
                break
            case3 = 'imgs/enjoyallthefeature.png'
            case3_found = auto.findTF(case3)
            if case3_found:
                auto.swipe(x_res//2,y_res*0.8,x_res//2,y_res*0.7)
                auto.click(x_res//2,y_res*0.934)
                print("Case 3 found!")
                break
            case4 = 'imgs/theresnovideousethissound.png'
            case4_found = auto.findTF(case4)
            if case4_found:
                auto.swipe(x_res//2,y_res*0.8,x_res//2,y_res*0.4)
                time.sleep(2)
                auto.click(x_res//2,y_res*0.934)
                print("Case 4 found!")
                break
            else:
                auto.click(x_res//2,y_res*0.92)
                print("Last case found!")
                break

            

    # Use the music
    def OpeningTikTok(self):
        auto = self.auto

        x_res,y_res = auto.GetScreenResolution()

        cond1_img = 'imgs/musicnote.png'
        cond2_img = 'imgs/opentiktokbuttoncamera.png'
        print(f'{auto.handle}: Opening TikTok...')
        while True:
            cond1,cond2= auto.findTF(cond1_img), auto.findTF(cond2_img)
            if cond1 and cond2:
                print(f'{auto.handle}: Use this sound!')
                x,y = x_res*0.78, y_res*0.93
                auto.click(x,y)
            elif cond2 and not cond1:
                print(f'{auto.handle}: Use this sound!')
                x,y = x_res//2, y_res*0.93
                auto.click(x,y)
            break

    def OpeningTikTokGallery(self):
        auto = self.auto
        x_res,y_res = auto.GetScreenResolution()
        target1 = 'imgs/allbar.png'
        target2 = 'imgs/accessdevice.png'
        print(f'{auto.handle}: Opening TikTok gallery...')
        while True:
            if auto.findTF(target1):
                time.sleep(5)
                if auto.findTF(target2):
                    auto.click(x_res*0.72,y_res*0.59)
                    time.sleep(3)
                break


    def OpeningCompletedSelection(self):
        auto = self.auto

        diaryButton = "imgs/yourdiary.png"
        nextButton = "imgs/next.png"
        print(f'{auto.handle}: Confirming video uploading...')
        while True:
            cond1 = auto.findTF(diaryButton)
            cond2 = auto.findTF(nextButton)
            if any([cond1,cond2]):
                break

    def OpeningFinalUploadStep(self):
        auto = self.auto

        img = "imgs/upButton.png"
        target = auto.findTF(img)
        print(f'{auto.handle}: Opening final step...')
        while True:
            if target:
                break
        
    def OpeningErrorLoadingTikTok(self):
        auto = self.auto

        img = "imgs/tryagainsign.png"
        target = auto.findTF(img)
        while True:
            target = auto.find(img)
            if target:
                break
    def UploadVideo(self):
        auto = self.auto
        x_res,y_res = auto.GetScreenResolution()
        target1 = "imgs/redbutton.png"
        target2 = 'imgs/cameraimg.png'
        time.sleep(3)
        while True:
            if auto.findTF(target2):
                auto.click(x_res*0.72,y_res*0.59)
                while True:
                    target3 = 'imgs/microphoneimg.png'
                    if auto.findTF(target3):
                        auto.click(x_res*0.72,y_res*0.59)
                        break
                break
            elif auto.findTF(target1):
                while True:
                    auto.click(x_res*0.813,y_res*0.833)
                    target3 = 'imgs/allbar.png'
                    
                    if auto.findTF(target3):
                        break      
                    time.sleep(5)
                break
    def test(self):
        auto = self.auto
        x_res,y_res = auto.GetScreenResolution()
        target1 = "imgs/redbutton.png"
        target2 = 'imgs/cameraimg.png'
        print(auto.findTF(target2))                      
    # Check if TikTok opens
    def didTiktokOpen(self):
        auto = self.auto
        while True:
            tiktokLoading_img = 'imgs/tiktokloading.png'
            tiktokLoading= auto.find(tiktokLoading_img)
            hasOpen = len(tiktokLoading)

            if hasOpen == 0:
                print(f'{auto.handle}: TikTok has opened!')
                break
    def OpenTikTokError(self):
        auto = self.auto
        x_res,y_res = auto.GetScreenResolution()
        target1 = 'imgs/tryagainsign.png'
        target2 = 'imgs/choosseyourhobby.png'
        while True:
            if auto.findTF(target1):
                print(f"{auto.handle}: Opening TikTok error found!")
                auto.click(x_res//2,y_res*0.83)
                print(f'{auto.handle}: Error solved!')
                break
            elif auto.findTF(target2):
                auto.click(x_res*0.3,y_res*0.95)
                break
        time.sleep(3)
    
    def SelectVideo(self,device):
        auto = self.auto
        
        x_res, y_res = auto.GetScreenResolution()
        print(f'{auto.handle}: Selecting video...')

        auto.click(x_res*0.49,y_res*0.15)
        time.sleep(2)
        auto.click(x_res*0.163,y_res*0.275)

    def accessFB(self):
        auto = self.auto
        x_res, y_res = auto.GetScreenResolution()
        target_img = "imgs/accessfb.png"
        if auto.findTF(target_img):
            auto.click(x_res*0.72,y_res*0.59)
    def accessCamera(self):
        auto = self.auto
        x_res, y_res = auto.GetScreenResolution()
        target_img = "imgs/cameraimg.png"
        if auto.findTF(target_img):
            auto.click(x_res*0.72,y_res*0.59)
    def accessMicrophone(self):
        auto = self.auto
        x_res, y_res = auto.GetScreenResolution()
        target_img = "imgs/microphoneimg.png"
        if auto.findTF(target_img):
            auto.click(x_res*0.72,y_res*0.59)
    def accessDevice(self):
        auto = self.auto
        x_res, y_res = auto.GetScreenResolution()
        target_img = "imgs/accessdevice.png"
        if auto.findTF(target_img):
            auto.click(x_res*0.72,y_res*0.59)
    def accessContacts(self):
        auto = self.auto
        x_res, y_res = auto.GetScreenResolution()
        target_img = "imgs/accesscontacts.png"
        if auto.findTF(target_img):
            auto.click(x_res*0.72,y_res*0.59)
    def GalleryCache(self,device):
        auto = self.auto
        x_res, y_res = auto.GetScreenResolution()
        self.OpenDocumentSUI(device)

        
        target1 = 'imgs/documentsui_3bars.png'
        target2 = 'imgs/documentsui_tep.png'
        target3 = 'imgs/documentsui_video.png'
        target4 = 'imgs/documentsui_camera_optionbar.png'
        target5 = 'imgs/documentsui_camera_all.png'
        target6 = 'imgs/documentsui_camera_trashbin.png'
        target7 = 'imgs/documentsui_camera_cancelok.png'
        target8 = 'imgs/documentsui_camera_nofile.png'
        while True:
            if auto.findTF(target1):
                auto.click(x_res*0.073,y_res*0.082)
                break
        while True:
            if auto.findTF(target2):
                auto.click(x_res*0.274,y_res*0.253)
                break
        while True:
            if auto.findTF(target3):
                auto.click(x_res*0.253,y_res*0.282)
                break
        while True:
            if auto.findTF(target4):
                auto.click(x_res*0.939,y_res*0.084)
                break
        while True:
            if auto.findTF(target5):
                auto.click(x_res*0.602,y_res*0.233)
                break
        while True:
            if auto.find(target6):
                auto.click(x_res*0.819,y_res*0.081)
                break
        while True:
            if auto.find(target7):
                auto.click(x_res*0.813,y_res*0.558)
                break
        while True:
            if auto.find(target8):
                print(f'{auto.handle}: Cache deleted!')
                break
def main(m):
    threads = []
    devices = GetDevices()
    thread_count = len(GetDevices())
    for i, device in enumerate(devices):
        thread = threading.Thread(target=start_thread, args=(device, i))
        threads.append(thread)
        thread.start()
def start_thread(device, thread_number):
    print(f"Thread {thread_number}: Using device - {device}")
    run = starts(device, thread_number)

    # Create img folder of the device
    checkFolder(device)
    # Move img to the folder
    move_file(device)
    
    subprocess.call('adb devices',stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,shell=True)
    time.sleep(2)
    subprocess.call('adb devices',stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,shell=True)
    time.sleep(2)
    run.OpenGallery(device)
    time.sleep(3)
    run.GoToMusicLink(device)
    # Loading TikTok
    # Click if there's error
    run.OpenTikTokError()
    # Wait for tiktok opening
    run.OpeningTikTok()

    run.UploadVideo()

    # Wait for TikTok gallery opening
    run.OpeningTikTokGallery()
    # Select video
    run.SelectVideo(device)
    # Wait for confirmation
    run.OpeningCompletedSelection()
    # Press "Next"
    run.PressNext()
    # Wait for final step
    run.OpeningFinalUploadStep()
    # Uppppppppppp
    run.GoPublic()
    time.sleep(3)
    remove_file(device)

    run.GalleryCache(device)
    run.clearOpenedApps(device)
if __name__ == "__main__":
    for m in range(1):
        threading.Thread(target=main, args=(m,)).start()