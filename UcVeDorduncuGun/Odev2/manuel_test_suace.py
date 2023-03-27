from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.by import By

class Manuel_Test_Suace:
    
    #test_sauce olan doysa ismi, pytest de görünmemesi için manuel_test_suace olarak değiştirildi.
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
        self.checkUserNameAndPasswordIsEmpty()
        inputUserName = self.driver.find_element(By.ID,"user-name")
        userNameErrorClass = inputUserName.get_attribute("class")

        inputPassword = self.driver.find_element(By.ID,"password")
        passwordErrorClass = inputPassword.get_attribute("class")

        validateErrorClasses = userNameErrorClass and passwordErrorClass == "input_error form_input error" 
        print(f"Validation failed icons displayed: {validateErrorClasses}")
        sleep(3)
        clearErrorButton = self.driver.find_element(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3/button")
        clearErrorButton.click()        
       
        classUserName = inputUserName.get_attribute("class")      
        classPassword = inputPassword.get_attribute("class") 
        isCleared =  classUserName and classPassword == "input_error form_input"
        print(f"Validation errors cleared: {isCleared}")       
        sleep(3)
    
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

testSouce = Manuel_Test_Suace()
testSouce.checkCountOfProducts()