import os,time
try:
 import threading,subprocess,base64,cv2,random,requests
 import numpy as np
except:
  os.system("pip install opencv-python")
  os.system("pip install numpy")
  os.system("pip install requests")
import threading,subprocess,base64,cv2,random,hashlib,sys,requests
import numpy as np
from datetime import datetime
from  xml.dom.minidom import parse
import time
import pandas as pd
from random import randint
import matplotlib.pyplot as plt

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
        subprocess.check_output(f"adb -s {self.handle} shell pm clear {package}", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
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
        #image = cv2.rectangle(img2, retVal[0],(retVal[0][0]+img.shape[0],retVal[0][1]+img.shape[1]), (0,250,0), 2)
        #cv2.imshow("test",image)
        #cv2.waitKey(0)
        #cv2.destroyWindow("test")
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



class starts(threading.Thread):
    def __init__(self, nameLD, i):
        super().__init__()
        self.nameLD = nameLD
        self.device = i
        self.auto = Auto(self.device)
        self.videoList = []
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
        systemapp =auto.find(systemapp_img)
        if len(systemapp) == 0:
            auto.BackToHomeScreen()
        else:
            print('The phone is at home screen!')
    def findTiktok(self):
        auto = self.auto
        tiktok_image_path = 'imgs/tiktok.png'
        auto.tapimg(tiktok_image_path)
    def UploadVideoButton(self):
        auto = self.auto
        button = 'imgs/uploadvideobutton.png'
        auto.tapimg(button)
    def AcceptAccessingCamera(self):
        auto = self.auto
        camera_img = 'imgs/cameraimg.png'
        camera = auto.find(camera_img)
        if len(camera) != 0:
            accept_img = 'imgs/acceptcamera.png'
            auto.tapimg(accept_img)
        else:
            print('No camera access!')
    def AcceptAccessingDevice(self):
        auto = self.auto
        device_img = 'imgs/accessdevice.png'
        device = auto.find(device_img)
        if len(device) != 0:
            accept_img = 'imgs/acceptaccessdevice.png'
            auto.tapimg(accept_img)
        else:
            print('No device access!')
    def UploadVideo(self):
        auto = self.auto
        upload_button = 'imgs/uploadline.png'
        auto.tapimg(upload_button)
    def SelectVideoSite(self):
        auto = self.auto
        video_button_img = 'imgs/videobutton.png'
        auto.tapimg(video_button_img)
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
    # Select video
    def SelectVideo(self, nth_video = 1):
        auto = self.auto
        x1, x2, x3, y1, y2, y3, header, body, footer = self.GetInfo()
        _x1, _x2, _x3, _y1, _y2, _y3 = self.xy_position()
        srceen = auto.screen_capture()
        match nth_video:
            case 1:
                x, y = x1, y1
                self.videoList.append(srceen[y1[0]:y1[1], x1[0]:x1[1]])
            case 2:
                x, y = x2, y1
                self.videoList.append(srceen[y2[0]:y2[1], x1[0]:x1[1]])
            case 3:
                x, y = x3, y1
                self.videoList.append(srceen[y3[0]:y3[1], x1[0]:x1[1]])
            case 4:
                x, y = x1, y2
                self.videoList.append(srceen[y1[0]:y1[1], x2[0]:x2[1]])
            case 5:
                x, y = x2, y2
                self.videoList.append(srceen[y2[0]:y2[1], x2[0]:x2[1]])
            case 6:
                x, y = x3, y2
                self.videoList.append(srceen[y3[0]:y3[1], x2[0]:x2[1]])
            case 7:
                x, y = x1, y3
                self.videoList.append(srceen[y1[0]:y1[1], x3[0]:x3[1]])
            case 8:
                x, y = x2, y3
                self.videoList.append(srceen[y2[0]:y2[1], x3[0]:x3[1]])
            case 9:
                x, y = x3, y3
                self.videoList.append(srceen[y3[0]:y3[1], x3[0]:x3[1]])
        auto.click(x=x, y=y)
    # Get to the music directly
    def GoToMusicLink(self):
        auto = self.auto
        # Check if the device is at home
        self.isHome()
        time.sleep(2)
        # Open System Apps folder
        systemapp = 'imgs/systemapp.png'
        auto.tapimg(systemapp)
        time.sleep(2)
        # Open browser
        browser = 'imgs/browser.png'
        auto.tapimg(browser)
        print('Opening browser...')
        time.sleep(2)
        # Click at the searching bar
        searching_bar = 'imgs/musicsearch.png'
        auto.tapimg(searching_bar)

        searching_bar = 'imgs/tiktoklink.png'
        auto.tapimg(searching_bar)
        # Select music
        music = self.TiktokMusics(self.random_music())
        # Access the music link
        auto.InpuText(music)
        auto.Enter()
        time.sleep(7)
        # Open TikTok
        while True:
            open_tikok_button = 'imgs/opentiktokbuttoncamera.png'
            button = auto.find(open_tikok_button)
            if len(button) != 0:
                auto.tapimg(open_tikok_button)
                print(button)
                print('Opening TikTok...')
                break
    # Use the music
    def UseSound(self):
        auto = self.auto
        # Click "Use this sound" button
        usethissound_button = 'imgs/usethissoundbutton.png'
        auto.tapimg(usethissound_button)
    # Check if TikTok opens
    def didTiktokOpen(self):
        auto = self.auto
        while True:
            tiktokLoading_img = 'tiktokloading.png'
            tiktokLoading= auto.find(tiktokLoading_img)
            hasOpen = len(tiktokLoading)

            if hasOpen == 0:
                print('TikTok has opened!')
                break
    def OpenTikTokError(self):
        auto = self.auto
        error_img = 'imgs/occurederror.png'
        errorOccured = auto.find()
        if len(errorOccured) != 0:
            tryagainbutton_img = 'imgs/tryagainbutton.png' 
            auto.tapimg(tryagainbutton_img)
    def xy_position(self):
        auto = self.auto
        # Calculate each video and save these video
        x_res, y_res = auto.GetScreenResolution()
        x1, x2, x3, y1, y2, y3, header, body, footer = self.GetInfo()
        # Get the body which contains videos
        videoContain = srceen[header:header+body,:]
        srceen = auto.screen_capture()
        # Seperate y of body into 3 part in accordance with 3 videos
        y_total = header+body - header+10
        y_mean = y_total // 3
        # y position [start,end]
        y_bias = 5
        y1 = [header+y_bias,header+y_mean-y_bias]
        y2 = [header+y_mean+y_bias, header+y_mean*2-y_bias]
        y3 = [header+y_mean*2+y_bias,header+body-y_bias]
        # Seperate x of body into 3 part in accordance with 3 videos
        x_mean = x_res // 3
        # x position [start,end]
        x_bias = 5
        x1 = [x_bias, x_mean-x_bias]
        x2 = [x_mean+x_bias, x_mean*2-x_bias]
        x3 = [x_mean*2+x_bias, x_res-x_bias]
        return x1, x2, x3, y1, y2, y3
    def checkExistence(self, nth_video= 1):
        auto = self.auto
        # Function is used to check if the video has used
        def find(img='', img2='',threshold=0.99):
            result = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
            loc = np.where(result >= threshold)
            retVal = list(zip(*loc[::-1]))
            return retVal
        # Get the screen
        srceen = auto.screen_capture()
        
        x1, x2, x3, y1, y2, y3 = self.xy_position()
        # Select video posion
        match nth_video:
            case 1:
                the_video = srceen[y1[0]:y1[1], x1[0]:x1[1]]
            case 2:
                the_video = srceen[y2[0]:y2[1], x1[0]:x1[1]]
            case 3:
                the_video = srceen[y3[0]:y3[1], x1[0]:x1[1]]
            case 4:
                the_video = srceen[y1[0]:y1[1], x2[0]:x2[1]]
            case 5:
                the_video = srceen[y2[0]:y2[1], x2[0]:x2[1]]
            case 6:
                the_video = srceen[y3[0]:y3[1], x2[0]:x2[1]]
            case 7:
                the_video = srceen[y1[0]:y1[1], x3[0]:x3[1]]
            case 8:
                the_video = srceen[y2[0]:y2[1], x3[0]:x3[1]]
            case 9:
                the_video = srceen[y3[0]:y3[1], x3[0]:x3[1]]
        # Check if the video exists
        if len(self.videoList) != 0:
            for vid in self.videoList:
                hasExisted= find(the_video,vid)
                if len(hasExisted) != 0:
                    return 0
        return 1

        
    # def solveCaptcha(self):
        
    #     device = self.device
    #     print(device)
    #     d = Auto(device)
    #     d.TapXml(text="Làm mới",classname="android.widget.TextView")
    #     def capcha(d):
    #         poin  = d.find('img\\keo.png')
    #         if poin > [(0, 0)] :
    #             d.slideCaptcha(poin[0][0],poin[0][1])
    #             print(" \033[1;31m |\033[1;37m[",self.nameLD,"]\033[1;31m Mở Face | Time:", time.ctime(time.time()))
    #             time.sleep(2)
    #     def min1(d):
    #         poin  = d.find('img\\1.png')
    #         if poin > [(0, 0)] :
    #             d.click(poin[0][0],poin[0][1])
    #             capcha(d)
    #     min1(d)
def main(m):
    
    device = GetDevices()
    thread_count = len(GetDevices())
    for i in device:
        run = starts(i,i,)
        # # Check if it's at homesreen or not
        # run.isHome()
        run.GoToMusicLink()
        
if __name__ == "__main__":
    for m in range(1):
        threading.Thread(target=main, args=(m,)).start()