import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
import pytest
from pathlib import Path
from datetime import date
class Test_Suace:

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
        self.folderPath = str(date.today().strftime('%d-%m-%Y'))
        Path(self.folderPath).mkdir(exist_ok=True)        
    
    def teardown_method(self):
        self.driver.quit()        
    
    def test_userNameAndPasswordIsEmpty(self): 
        expectedMessage = "Epic sadface: Username is required"       
          
        self.loginButton.click()
        errorMessage = self.getElementByLocator(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")
        self.driver.save_screenshot(f"{self.folderPath}/test_userNameAndPasswordIsEmpty.png")
        assert errorMessage.text == expectedMessage        
    
    def test_ifPasswordEmpty(self):        
        userNameText = "kullaniciAdim"
        expectedText = "Epic sadface: Password is required"        

        self.userNameInput.send_keys(userNameText)        
        self.loginButton.click()        
        errorMessage = self.getElementByLocator(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")  
        self.driver.save_screenshot(f"{self.folderPath}/test_ifPasswordEmpty.{userNameText}.png")      
        assert errorMessage.text == expectedText        
    
    def test_lockedOutUser(self):        
        lockedOutUserName = "locked_out_user"
        lockedOutPassword = "secret_sauce"   
        expectedText = "Epic sadface: Sorry, this user has been locked out."     

        self.userNameInput.send_keys(lockedOutUserName)
        self.passwordInput.send_keys(lockedOutPassword)        
        self.loginButton.click()        
        errorMessage = self.getElementByLocator(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3") 
        self.driver.save_screenshot(f"{self.folderPath}/test_lockedOutUser.{lockedOutUserName}.{lockedOutPassword}.png")       
        assert errorMessage.text == expectedText
        
    
    def test_formValidationIcons(self):
        xIconsDisplayed = False
        xIconsCleared = False

        self.loginButton.click()
        userNameError = self.getElementByLocator(By.CSS_SELECTOR, ".form_group:nth-child(1) > .svg-inline--fa")
        passwordError = self.getElementByLocator(By.CSS_SELECTOR, ".form_group:nth-child(2) > .svg-inline--fa")        
        xIconsDisplayed = (userNameError.is_displayed() and passwordError.is_displayed()) == True
        self.driver.save_screenshot(f"{self.folderPath}/test_formValidationIcons.xIcnonsDisplayed.{xIconsDisplayed}.png")
        clearErrorButton = self.getElementByLocator(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3/button")
        clearErrorButton.click()        
       
        userNameError = self.checkElementExistsByLocator(By.CSS_SELECTOR, ".form_group:nth-child(1) > .svg-inline--fa")
        passwordError = self.checkElementExistsByLocator(By.CSS_SELECTOR, ".form_group:nth-child(2) > .svg-inline--fa")
        xIconsCleared = (userNameError and passwordError) == False
        self.driver.save_screenshot(f"{self.folderPath}/test_formValidationIcons.xIcnonsClearedd.{xIconsCleared}.png")
        assert (xIconsDisplayed and xIconsCleared) == True
        
    
    def test_validLogin(self):        
        validUserName = "standard_user"
        validPassword = "secret_sauce"
        expectedUrl = "https://www.saucedemo.com/inventory.html"

        self.userNameInput.send_keys(validUserName)
        self.passwordInput.send_keys(validPassword)
        self.loginButton.click()        
        checkUrl = self.driver.current_url
        self.driver.save_screenshot(f"{self.folderPath}/test_validLogin.png")
        assert checkUrl == expectedUrl        
    
    def test_countOfProducts(self):
        validUserName = "standard_user"
        validPassword = "secret_sauce"
        expectedCount = 6

        self.userNameInput.send_keys(validUserName)
        self.passwordInput.send_keys(validPassword)
        self.loginButton.click()        
        countOfProducts = len(self.getElementsByLocator(By.CLASS_NAME,"inventory_item"))
        self.driver.save_screenshot(f"{self.folderPath}/test_countOfProducts.{str(countOfProducts)}.png")
        assert countOfProducts == expectedCount

    # En az 3 Case daha yazınız:
    def test_checkRemoveButtonVisible(self):
        """
        6 ürün içinden rastgele birini seçip sepete eklemek için "Add to cart" butonunun olduğunu doğrulayan, bu butona tıkladıktan sonra, "Add to cart" butonu yerine "Remove" butonunun geldiğini doğrulayan test.
        """
        validUserName = "standard_user"
        validPassword = "secret_sauce"   
        expectedAddButtonText = "Add to cart"
        expectedRemoveButtonText = "Remove" 
        addButtonText = ""
        removeButtonText = ""   

        self.userNameInput.send_keys(validUserName)
        self.passwordInput.send_keys(validPassword)
        self.loginButton.click()          
        selectionsFromList = random.randint(1,6)
        addButton = self.getElementByLocator(By.XPATH,f"//*[@id='inventory_container']/div/div[{selectionsFromList}]/div[2]/div[2]/button")
        addButtonText = addButton.text     
        self.driver.save_screenshot(f"{self.folderPath}/test_checkRemoveButtonVisible.{addButton.text}.png")   
        addButton.click()  
        removeButtonText = self.getElementByLocator(By.XPATH,f"//*[@id='inventory_container']/div/div[{selectionsFromList}]/div[2]/div[2]/button").text
        self.driver.save_screenshot(f"{self.folderPath}/test_checkRemoveButtonVisible.{removeButtonText}.png")
        assert (addButtonText == expectedAddButtonText) and (removeButtonText == expectedRemoveButtonText)


    def test_checkBasketBadgeVisible(self): 
        """
        Sepette ürün yokken sepet logosunda adet belirten badge'in olmadığını, sepete ürün eklendikten sonra sepet ikonunda badge işareti çıktığını doğrulayan test. (Badge içindeki rakam ile ilgilenmez, bagde in görünüp görünmediği ile alakalı bir test.)
        """   
        isBadgeVisibleBeforeAddToCart = False
        isBadgeVisibleAfterAddToCart = False
        validUserName = "standard_user"
        validPassword = "secret_sauce"  

        self.userNameInput.send_keys(validUserName)
        self.passwordInput.send_keys(validPassword)
        self.loginButton.click() 
        isBadgeVisibleBeforeAddToCart = self.checkElementExistsByLocator(By.XPATH,"//*[@id='shopping_cart_container']/a/span")  
        self.driver.save_screenshot(f"{self.folderPath}/test_checkBasketBadgeVisible{isBadgeVisibleBeforeAddToCart}.png")       
        selectionsFromList = random.randint(1,6)
        addButton = self.getElementByLocator(By.XPATH,f"//*[@id='inventory_container']/div/div[{selectionsFromList}]/div[2]/div[2]/button")    
        addButton.click()
        isBadgeVisibleAfterAddToCart = self.checkElementExistsByLocator(By.XPATH,"//*[@id='shopping_cart_container']/a/span") 
        self.driver.save_screenshot(f"{self.folderPath}/test_checkBasketBadgeVisible.{isBadgeVisibleAfterAddToCart}.png") 
        assert (isBadgeVisibleBeforeAddToCart == False and isBadgeVisibleAfterAddToCart == True)

    def test_checkBasketBadgeNumberCorrect(self): 
        """
        Çalıştığında 1 ile 6 arasındaki rasgele bir sayıda ürünü sepete ekleyen (bu iki rakam da dahil), ve sepette eklenen ürün sayısı ile sepet badgeinde yazan ürün adedinin doğruluğunu test eden method.
        """       
        validUserName = "standard_user"
        validPassword = "secret_sauce"  
        productNumberToAddCart = []
        randomProductNumberToAddCart = random.randint(1,6)
        for i in range(1,randomProductNumberToAddCart + 1):            
            productNumberToAddCart.append(i)         
        self.userNameInput.send_keys(validUserName)
        self.passwordInput.send_keys(validPassword)
        self.loginButton.click()  
        for number in productNumberToAddCart:
            addButton = self.getElementByLocator(By.XPATH,f"//*[@id='inventory_container']/div/div[{number}]/div[2]/div[2]/button")    
            addButton.click()
        numberInBadge = self.getElementByLocator(By.XPATH,"//*[@id='shopping_cart_container']/a/span").text
        self.driver.save_screenshot(f"{self.folderPath}/test_checkBasketBadgeNumberCorrect.{str(randomProductNumberToAddCart)}.png")
        assert str(randomProductNumberToAddCart) == numberInBadge 
    
    def invoiceInfoEmptyChecker():
        invoiceData = []
        for i in range(0,3):
            if i == 0:
                firstName = ""
                lastName = "Soyadim"
                postalCode = "Posta Kodum"
                tupleData = (firstName,lastName,postalCode)
                invoiceData.append(tupleData)
            elif i == 1:
                firstName = "Adim"
                lastName = ""
                postalCode = "Posta Kodum"
                tupleData = (firstName,lastName,postalCode)
                invoiceData.append(tupleData)
            else:
                firstName = "Adim"
                lastName = "Soyadim"
                postalCode = ""
                tupleData = (firstName,lastName,postalCode)
                invoiceData.append(tupleData)
        return invoiceData

    @pytest.mark.parametrize("firstName,lastName,postalCode",invoiceInfoEmptyChecker())
    def test_invalidCheckoutData(self,firstName,lastName,postalCode):
        """
        Sepete ürün eklendikten sonra Checkout:Your Information kısmında herhangi bir alanın boş bırakıldığında hata mesajı alındığını test eden method.
        """
        validUserName = "standard_user"
        validPassword = "secret_sauce" 
           
        self.userNameInput.send_keys(validUserName)
        self.passwordInput.send_keys(validPassword)
        self.loginButton.click()  
        addButton = self.getElementByLocator(By.XPATH,f"//*[@id='inventory_container']/div/div[1]/div[2]/div[2]/button")    
        addButton.click()
        cartButton = self.getElementByLocator(By.XPATH,"//*[@id='shopping_cart_container']/a")
        cartButton.click()
        checkOutButton = self.getElementByLocator(By.ID,"checkout")
        checkOutButton.click()
        firstNameArea = self.getElementByLocator(By.ID,"first-name")
        lastNameArea = self.getElementByLocator(By.ID,"last-name")
        postalCodeArea = self.getElementByLocator(By.ID,"postal-code")
        firstNameArea.send_keys(firstName)
        lastNameArea.send_keys(lastName)
        postalCodeArea.send_keys(postalCode)
        continueButton = self.getElementByLocator(By.ID,"continue") 
        continueButton.click()        
        errorDiv = self.getElementByLocator(By.XPATH,"//*[@id='checkout_info_container']/div/form/div[1]/div[4]")
        self.driver.save_screenshot(f"{self.folderPath}/test_invalidInvoiceData.{firstName}.{lastName}.{postalCode}.png")
        assert errorDiv.is_displayed()
            
        
    #Helper Methods
    def waitForElementVisible(self,locator,timeout=5):
        WebDriverWait(self.driver,timeout).until(ec.visibility_of_element_located(locator))
    
    def getElementByLocator(self,by,locator,timeout=5):
        self.waitForElementVisible((by,locator),timeout)
        return self.driver.find_element(by,locator)
    
    def getElementsByLocator(self,by,locator,timeout=5):
        self.waitForElementVisible((by,locator),timeout)
        return self.driver.find_elements(by,locator)
    
    def checkElementExistsByLocator(self,by,locator):
        try:
            self.driver.find_element(by, locator)
        except NoSuchElementException:
            return False
        return True
    
    


    
    

