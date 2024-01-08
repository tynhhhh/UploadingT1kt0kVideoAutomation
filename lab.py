from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.touch_action import TouchAction
from pynput.keyboard import Controller
import time
from bypassSlideCaptcha import bypass_slide

keyboard = Controller()

devi = "emulator-5554"
class app():
    desired_cap ={
        "uuid": "emulator-5554",
        "platformName": "Android",
        "appPackage": "com.ldmnq.launcher3",
        "appActivity": "com.android.launcher3.Launcher"
    }
    options = UiAutomator2Options()

    options.load_capabilities(desired_cap)

    driver = webdriver.Remote("http://localhost:4723/wd/hub",options=options)
    
    def ele_byID(self, input):
        return self.driver.find_element(AppiumBy.ID,input)

    def eles_byID(self, input):
        return self.driver.find_element(AppiumBy.ID,input)

    def ele_byXPATH(self, input):
        return self.driver.find_element(AppiumBy.XPATH,input)

    def eles_byXPATH(self, input):
        return self.driver.find_element(AppiumBy.XPATH,input)

    def eles_byCLASS(self, input):
        return self.driver.find_elements(AppiumBy.CLASS_NAME, input)
    
    def ele_byAID(self, input):
        return self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, input)

    def enter(self):
        self.driver.press_keycode(66)
    
    def HomeScreen(self):
        self.driver.press_keycode(3)

    def checkTimesCounter(times):
        print('Check times: ',times+1)
    

    def scroll_down_to_element(self, element_locator, max_attempts=10):
        attempts = 0
        while attempts < max_attempts:
            try:
                # Attempt to find the element
                self.driver.find_element(*element_locator)
                break  # Element found, exit the loop
            except:
                # Scroll down using TouchAction
                action = TouchAction(self.driver)
                action.press(x=500, y=1800).move_to(x=500, y=1000).release().perform()
                self.driver.implicitly_wait(5)  # Add a short delay to let the scroll take effect
                attempts += 1

    def appCheck(self, itemList, appName):
        for itemplace in range(len(itemList)):
            self.checkTimesCounter(itemplace)

            item = itemList[itemplace]
            if item.text == appName:
                print(f'{item.text} found!')
                return item
            
    def inHomeScreen(self):
        try:
            screenhomeElement= self.ele_byID('com.ldmnq.launcher3:id/preview_background')
            return True
        except:
            return False
        
    def gotoHomeScrren(self):
        if not self.inHomeScreen():
            self.HomeScreen()


    def TikTokDownload(self):
        self.gotoHomeScrren()

        searchButton = self.driver.find_element(AppiumBy.ID,"com.ldmnq.launcher3:id/searchInputView")
        searchButton.click()
        self.driver.implicitly_wait(30)

        AppStoreSearchButton = self.driver.find_element(AppiumBy.ID, "com.android.ld.appstore:id/et_search")
        AppStoreSearchButton.click()
        AppStoreSearchButton.send_keys('TikTok')

        self.driver.press_keycode(66)

        # SearchResults = self.driver.find_elements(AppiumBy.ID, "com.android.ld.appstore:id/searchResult_list_game_name")

        # tiktokApp = self.appCheck(SearchResults, "TikTok")

        tiktokApp = self.ele_byXPATH('//android.view.View[@text="TikTok"]')
        tiktokApp.click()
        self.driver.implicitly_wait(30)

        downloadButton = self.ele_byXPATH('//android.widget.Button[@resource-id="com.android.vending:id/0_resource_name_obfuscated"]')
        downloadButton.click()

    def tiktokHere(self):
        self.gotoHomeScrren()

        tiktokHasDownloaded = False
        while not tiktokHasDownloaded:
            try:
                tiktokApp = self.ele_byAID('TikTok')
            except:
                continue
            break
        if tiktokApp:
            return tiktokApp

    def TikTok(self, usern, passw, SignInMethod = 'email'):
        tiktok = self.tiktokHere()
        tiktok.click()
        self.driver.implicitly_wait(30)

        uploadVideo = self.eles_byID('com.ss.android.ugc.trill:id/gql')
        uploadVideo.click()
        self.driver.implicitly_wait(30)

        # policyAcceptions = self.eles_byCLASS('android.widget.Button')
        # policyAcceptions[-1].click()
        # self.driver.implicitly_wait(30)

        profileButton = self.ele_byID('com.ss.android.ugc.trill:id/gqq')
        profileButton.click()
        self.driver.implicitly_wait(30)

        match SignInMethod:
            case 'email':
                SignInByPhoneNumberEmailUsername = self.ele_byAID('Số điện thoại/email/tên người dùng')
                SignInByPhoneNumberEmailUsername.click()
                self.driver.implicitly_wait(30)

                EmailSignIn = self.ele_byAID('Email/tên người dùng')
                EmailSignIn.click()
                self.driver.implicitly_wait(30)

                UserName = self.ele_byID('com.ss.android.ugc.trill:id/f1_')
                UserName.click()
                UserName.send_keys(usern)
                
                PassWord = self.ele_byID('com.ss.android.ugc.trill:id/d87')
                PassWord.click()
                PassWord.send_keys(passw)

                SignIn = self.ele_byID('com.ss.android.ugc.trill:id/glo')
                SignIn.click()
                self.driver.implicitly_wait(30)

                bypass_slide(devi)




        # Sign in by Google
        # SignInByGoogle = self.ele_byAID('Tiếp tục với Google')
        # SignInByGoogle.click()
        # self.driver.implicitly_wait(30)



    def appstoreSignin(self, user, passw):
        self.gotoHomeScrren()

        SysApps= self.ele_byID('com.ldmnq.launcher3:id/preview_background')
        SysApps.click()
        self.driver.implicitly_wait(30)

        appStore = self.ele_byXPATH('//android.widget.TextView[@content-desc="Cửa hàng Play"]')
        appStore.click()
        self.driver.implicitly_wait(30)

        signinButton = self.ele_byXPATH('//android.widget.Button[@resource-id="com.android.vending:id/0_resource_name_obfuscated"]')
        signinButton.click()
        self.driver.implicitly_wait(30)

        username = self.ele_byXPATH('//android.view.View[@resource-id="yDmH0d"]/android.view.View[4]/android.view.View/android.view.View[1]/android.view.View[2]')
        username.click()
        time.sleep(0.5)
        keyboard.type(user)
        self.enter()
        self.driver.implicitly_wait(30)

        password = self.ele_byXPATH('//android.view.View[@resource-id="password"]/android.view.View/android.view.View[3]')
        password.click()
        time.sleep(0.5)
        keyboard.type(passw)
        self.enter()
        self.driver.implicitly_wait(30)

        try:
            self.scroll_down_to_element((AppiumBy.ID,'signinconsentNext'))
            signinconsentNext = self.ele_byID('signinconsentNext')
        except:
            signinconsentNext = None
        
        if signinconsentNext:
            signinconsentNext.click()

            laterButtons = self.eles_byCLASS('android.widget.Button')
            laterButtons[-1].click()

            acceptButtons = self.eles_byCLASS('android.widget.Button')
            for i in acceptButtons:
                print(i.text)

            PolicyAcceptedButton = self.ele_byXPATH('//android.widget.Button[@resource-id="com.android.vending:id/0_resource_name_obfuscated" and @text="Chấp nhận"]')
            PolicyAcceptedButton.click()
        else:
            demoList= self.eles_byCLASS()
            print('demoList')
            for i in demoList:
                print(i.text)


if __name__ == "__main__":
    sys = app()
    tiktokApp = sys.tiktokHere()
    tiktokApp.click()