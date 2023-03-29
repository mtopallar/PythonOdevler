from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import pytest
from pathlib import Path
from datetime import date
class Test_Suace:

    # testUrl = "https://www.saucedemo.com/"
    # userNameInputId = "user-name"
    # passwordInputId = "password"
    # loginButtonId = "login-button"

    def setup_method(self):
        testUrl = "https://www.saucedemo.com/"
        userNameInputId = "user-name"
        passwordInputId = "password"
        loginButtonId = "login-button"

        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.driver.get(testUrl)
        self.userNameInput = self.getElementByLocator(By.ID,userNameInputId)
        self.passwordInput = self.getElementByLocator(By.ID,passwordInputId)
        self.loginButton = self.getElementByLocator(By.ID,loginButtonId)
    
    def teardown_method(self):
        self.driver.quit()        
    
    def test_userNameAndPasswordIsEmpty(self): 
        expectedMessage = "Epic sadface: Username is required"       
          
        self.loginButton.click()
        errorMessage = self.getElementByLocator(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")
        assert errorMessage.text == expectedMessage        
    
    def test_ifPasswordEmpty(self):        
        userNameText = "kullaniciAdim"
        expectedText = "Epic sadface: Password is required"        

        self.userNameInput.send_keys(userNameText)        
        self.loginButton.click()        
        errorMessage = self.getElementByLocator(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")        
        assert errorMessage.text == expectedText        
    
    def test_lockedOutUser(self):        
        lockedOutUserName = "locked_out_user"
        lockedOutPassword = "secret_sauce"   
        expectedText = "Epic sadface: Sorry, this user has been locked out."     

        self.userNameInput.send_keys(lockedOutUserName)
        self.passwordInput.send_keys(lockedOutPassword)        
        self.loginButton.click()        
        errorMessage = self.getElementByLocator(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")        
        assert errorMessage.text == expectedText
        
    
    def test_formValidationIcons(self):
        xIconsDisplayed = False
        xIconsCleared = False

        self.loginButton.click()
        userNameError = self.getElementByLocator(By.CSS_SELECTOR, ".form_group:nth-child(1) > .svg-inline--fa")
        passwordError = self.getElementByLocator(By.CSS_SELECTOR, ".form_group:nth-child(2) > .svg-inline--fa")        
        xIconsDisplayed = (userNameError.is_displayed() and passwordError.is_displayed()) == True

        clearErrorButton = self.getElementByLocator(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3/button")
        clearErrorButton.click()        
       
        userNameError = self.check_element_exists_by_locator(By.CSS_SELECTOR, ".form_group:nth-child(1) > .svg-inline--fa")
        passwordError = self.check_element_exists_by_locator(By.CSS_SELECTOR, ".form_group:nth-child(2) > .svg-inline--fa")
        xIconsCleared = (userNameError and passwordError) == False
        assert (xIconsDisplayed and xIconsCleared) == True
        
    
    def test_validLogin(self):        
        validUserName = "standard_user"
        validPassword = "secret_sauce"
        expectedUrl = "https://www.saucedemo.com/inventory.html"

        self.userNameInput.send_keys(validUserName)
        self.passwordInput.send_keys(validPassword)
        self.loginButton.click()        
        checkUrl = self.driver.current_url
        assert checkUrl == expectedUrl        
    
    def test_countOfProducts(self):
        validUserName = "standard_user"
        validPassword = "secret_sauce"
        expectedCount = 6

        self.userNameInput.send_keys(validUserName)
        self.passwordInput.send_keys(validPassword)
        self.loginButton.click()        
        countOfProducts = len(self.getElementsByLocator(By.CLASS_NAME,"inventory_item"))
        assert countOfProducts == expectedCount

    #Helper Methods
    def waitForElementVisible(self,locator,timeout=5):
        WebDriverWait(self.driver,timeout).until(ec.visibility_of_element_located(locator))
    
    def getElementByLocator(self,by,locator,timeout=5):
        self.waitForElementVisible((by,locator),timeout)
        return self.driver.find_element(by,locator)
    
    def getElementsByLocator(self,by,locator,timeout=5):
        self.waitForElementVisible((by,locator),timeout)
        return self.driver.find_elements(by,locator)
    
    def check_element_exists_by_locator(self,by,locator):
        try:
            self.driver.find_element(by, locator)
        except NoSuchElementException:
            return False
        return True
