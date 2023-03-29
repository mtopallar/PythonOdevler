from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

class Manuel_Test_Suace:
    
    # test_sauce olan doysa ismi, pytest de görünmemesi için manuel_test_suace olarak değiştirildi.
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    
    def connectSite(self):
        self.driver.get("https://www.saucedemo.com/")
        sleep(5)
    
    def checkUserNameAndPasswordIsEmpty(self):
        self.connectSite()        
        btnLogin = self.driver.find_element(By.ID,"login-button")
        btnLogin.click()
        sleep(3)
        errorMessage = self.driver.find_element(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")
        errorMessageResult = errorMessage.text == "Epic sadface: Username is required"
        print(f"UserName and Password Empty Test Passed: {errorMessageResult}")
        sleep(3)
    
    def checkIfPasswordEmpty(self):
        self.connectSite()
        inputUserName = self.driver.find_element(By.ID,"user-name")
        inputUserName.send_keys("User Name")
        btnLogin = self.driver.find_element(By.ID,"login-button")
        btnLogin.click()
        sleep(3)
        errorMessage = self.driver.find_element(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")
        errorMessageResult = errorMessage.text == "Epic sadface: Password is required"
        print(f"Only Password Empty Test Passed: {errorMessageResult}")
        sleep(3)
    
    def checkLockedOutUser(self):
        self.connectSite()
        inputUserName = self.driver.find_element(By.ID,"user-name")
        inputUserPassword = self.driver.find_element(By.ID,"password")
        btnLogin = self.driver.find_element(By.ID,"login-button")
        inputUserName.send_keys("locked_out_user")
        inputUserPassword.send_keys("secret_sauce")
        btnLogin.click()
        sleep(3)
        errorMessage = self.driver.find_element(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")
        errorMessageResult = errorMessage.text == "Epic sadface: Sorry, this user has been locked out."
        print(f"Locked Out User Test Passed: {errorMessageResult}")
        sleep(3)
    
    def checkFormValidationIcons(self):
        
        #kullanici adı ve parola boş girildiğinde validasyon hatasını gösteren X işaretleri çıkmalı, hata mesajındaki kapat butonuna basıldığında validasyon işaretleri kaybolmalı.
        
        self.checkUserNameAndPasswordIsEmpty()
        userNameError = self.driver.find_element(By.CSS_SELECTOR, ".form_group:nth-child(1) > .svg-inline--fa")
        passwordError = self.driver.find_element(By.CSS_SELECTOR, ".form_group:nth-child(2) > .svg-inline--fa")        
        result = (userNameError.is_displayed() and passwordError.is_displayed()) == True
        print(f"X icons displayed? {result}")

        clearErrorButton = self.driver.find_element(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3/button")        
        clearErrorButton.click()   
        sleep(2)
        
        userNameError = self.check_element_exists_by_locator(By.CSS_SELECTOR, ".form_group:nth-child(1) > .svg-inline--fa")
        passwordError = self.check_element_exists_by_locator(By.CSS_SELECTOR, ".form_group:nth-child(2) > .svg-inline--fa")
        resultCleared = (userNameError and passwordError) == False
        print(f"X icons cleared? {resultCleared}")
    
    def checkValidLogin(self):
        self.connectSite()
        inputUserName = self.driver.find_element(By.ID,"user-name")
        inputUserPassword = self.driver.find_element(By.ID,"password")
        btnLogin = self.driver.find_element(By.ID,"login-button")
        inputUserName.send_keys("standard_user")
        inputUserPassword.send_keys("secret_sauce")
        btnLogin.click()
        sleep(3)
        checkUrl = self.driver.current_url
        isUrlTrue = checkUrl == "https://www.saucedemo.com/inventory.html"
        print(f"Redirection test passed: {isUrlTrue}")
    
    def checkCountOfProducts(self):
        self.checkValidLogin()
        countOfProducts = self.driver.find_elements(By.CLASS_NAME,"inventory_item")
        print(f"Count of products test passed: {len(countOfProducts) == 6}")

    #Helper Mothods
    def check_element_exists_by_locator(self,by,locator):
        try:
            self.driver.find_element(by, locator)
        except NoSuchElementException:
            return False
        return True

testSouce = Manuel_Test_Suace()
testSouce.checkCountOfProducts()

