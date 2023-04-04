import random
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
import pytest
from data import dataGetter
from pathlib import Path
from datetime import date

"""
Senaryolar:
1) Hatalı kullanıcı adı ve parola kombinasyonu ile veya boş bırakılan veri ile giriş yapılamadığını doğrula => ok
2) Doğru kullanıcı adı ve giriş ile giriş yapılabildiğini doğrula => ok
3) Sandwich menüden logOut butonunu doğrula => ok
4) Flitre öğelerinin çalıştığını doğrula => ok
    -A to Z => ok
    -Z to A => ok
    -Low to high => ok
    -High to Low => ok
5) Her bir öğenin resmine tıklandığında detay sayfasına gittiğini doğrula => //*[@id="item_0_img_link"] => ok
6) Her bir öğenin başlığına tıklandığıda detay sayfasına gittiğini doğrula. => //*[@id="item_0_title_link"] => ok
                                                        https://www.saucedemo.com/inventory-item.html?id=0
7) Add to cart çalışmasını doğrula => ok
8) Remove butonunun çalışmasını doğrula => ok
9) Checkout işlemi öncesi information kısmının boş geçilemediğini onayla => ok
10) Toplam fiyatın doğru hesaplandığını test et (Kdv %8 ve mesela 16.4476 16.45 e yuvarlanıyor.) => ok
11) Alışverişi tamamla.
"""
class Test_Sauce:

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
        # self.folderPath = str(date.today().strftime('%d-%m-%Y'))
        # Path(self.folderPath).mkdir(exist_ok=True)        
    
    def teardown_method(self):
        self.driver.quit()  

    def getInvalidLoginData():          
        selectedSheet = dataGetter.getExcelDataWithSelectedSheet("invalid_test_datas.xlsx","invalid_login") 
        totalRows = selectedSheet.max_row
        data = []
        for i in range(2,totalRows + 1):
            username = "" if selectedSheet.cell(i,1).value == '""' else selectedSheet.cell(i,1).value
            password = "" if selectedSheet.cell(i,2).value == '""' else selectedSheet.cell(i,2).value            
            tupleData = (username,password)
            data.append(tupleData)
        return data

    @pytest.mark.parametrize("username,password",getInvalidLoginData())
    def test_invalidLogin(self,username,password):
       self.userNameInput.send_keys(username)
       self.passwordInput.send_keys(password)
       self.loginButton.click()
       userNameError = self.checkElementExistsByLocator(By.CSS_SELECTOR, ".form_group:nth-child(1) > .svg-inline--fa")
       passwordError = self.checkElementExistsByLocator(By.CSS_SELECTOR, ".form_group:nth-child(2) > .svg-inline--fa")
       errorMessageDiv = self.getElementByLocator(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]")
       if (userNameError and passwordError) and errorMessageDiv.is_displayed():
           assert True
       else:
           assert False

    def test_validLogin(self):        
        validUserName = "standard_user"
        validPassword = "secret_sauce"
        expectedUrl = "https://www.saucedemo.com/inventory.html"
        self.userNameInput.send_keys(validUserName)
        self.passwordInput.send_keys(validPassword)
        self.loginButton.click()        
        checkUrl = self.driver.current_url
        #self.driver.save_screenshot(f"{self.folderPath}/test_validLogin.png")
        assert checkUrl == expectedUrl        

    def test_logOutFromBurgerMenu(self):    
        expectedUrl = "https://www.saucedemo.com/"     
        self.login()
        sandwichButton = self.getElementByLocator(By.ID,"react-burger-menu-btn")
        sandwichButton.click()
        logOutLink = self.getElementByLocator(By.ID,"logout_sidebar_link")
        logOutLink.click()
        currentUrl = self.driver.current_url
        assert currentUrl == expectedUrl

    def test_filterNameAToZ(self):
        flag = False
        self.login()        
        filterMenu = self.getElementByLocator(By.XPATH,"//*[@id='header_container']/div[2]/div/span/select")
        filterAToZ = self.getElementByLocator(By.XPATH,"//*[@id='header_container']/div[2]/div/span/select/option[1]")
        filterMenu.click()
        filterAToZ.click()
        productNameDivs = self.getElementsByLocator(By.XPATH,"//div[@class='inventory_item_name']")
        productNameAToZ = self.getProductNameList(productNameDivs)               
        if sorted(productNameAToZ):
            flag = True
        else:
            flag = False
        assert flag

    def test_filterNameZToA(self):        
        flag = False
        self.login()
        filterMenu = self.getElementByLocator(By.XPATH,"//*[@id='header_container']/div[2]/div/span/select")
        filterZtoA = self.getElementByLocator(By.XPATH,"//*[@id='header_container']/div[2]/div/span/select/option[2]")
        filterMenu.click()
        filterZtoA.click()
        productNameDivs = self.getElementsByLocator(By.XPATH,"//div[@class='inventory_item_name']")
        productNameZToA = self.getProductNameList(productNameDivs)              
        if sorted(productNameZToA,reverse=True):
            flag = True
        else:
            flag = False        
        assert flag
    
    def test_filterPriceLowToHigh(self):
        flag = False
        self.login()        
        filterMenu = self.getElementByLocator(By.XPATH,"//*[@id='header_container']/div[2]/div/span/select")
        filterPriceLowToHigh = self.getElementByLocator(By.XPATH,"//*[@id='header_container']/div[2]/div/span/select/option[3]")
        filterMenu.click()
        filterPriceLowToHigh.click()
        productPricesDivs = self.getElementsByLocator(By.XPATH,"//div[@class='inventory_item_price']")
        productPricesSortedToHigher = self.getProductPriceList(productPricesDivs)                
        if sorted(productPricesSortedToHigher):
            flag = True
        else:
            flag = False
        assert flag

    def test_filterPriceHighToLow(self):
        flag = False
        self.login()        
        filterMenu = self.getElementByLocator(By.XPATH,"//*[@id='header_container']/div[2]/div/span/select")
        filterPriceHighToLow = self.getElementByLocator(By.XPATH,"//*[@id='header_container']/div[2]/div/span/select/option[4]")
        filterMenu.click()
        filterPriceHighToLow.click()
        productPricesDivs = self.getElementsByLocator(By.XPATH,"//div[@class='inventory_item_price']")
        productPricesSortedToLower = self.getProductPriceList(productPricesDivs)              
        if sorted(productPricesSortedToLower,reverse=True):
            flag = True
        else:
            flag = False
        assert flag

    def test_imageGoesToProductDetail(self):
        selectRandomProduct = random.randint(0,5)
        expectedUrl = f"https://www.saucedemo.com/inventory-item.html?id={selectRandomProduct}"
        self.login()
        productImage = self.getElementByLocator(By.ID,f"item_{selectRandomProduct}_img_link")
        productImage.click()
        currentLocation = self.driver.current_url
        assert currentLocation == expectedUrl
    
    def test_titleGoesToProductDetail(self):
        selectRandomProduct = random.randint(0,5)
        expectedUrl = f"https://www.saucedemo.com/inventory-item.html?id={selectRandomProduct}"
        self.login()
        productTitleLink = self.getElementByLocator(By.ID,f"item_{selectRandomProduct}_title_link")
        productTitleLink.click()
        currentLocation = self.driver.current_url
        assert currentLocation == expectedUrl
            
    def test_addToCartButton(self):
        self.login()        
        buttonsToClick = len(self.randomClickToAddToCartButton())    
        cartIcon = self.getElementByLocator(By.CLASS_NAME,"shopping_cart_link")
        cartIcon.click()
        cartItemsList = self.getElementsByLocator(By.CLASS_NAME,"cart_item")
        assert buttonsToClick == len(cartItemsList)   

    def test_removeButton(self):
        self.login()    
        flag = False        
        addButtonsToClick = self.randomClickToAddToCartButton()
        randomRemove = random.randint(1,len(addButtonsToClick))        
        for i in range(1,randomRemove + 1):
            if addButtonsToClick[i-1] == 1:
                productRemoveButton = self.getElementByLocator(By.XPATH,f"//*[@id='inventory_container']/div/div/div[2]/div[2]/button")                
            else:
                productRemoveButton = self.getElementByLocator(By.XPATH,f"//*[@id='inventory_container']/div/div[{addButtonsToClick[i-1]}]/div[2]/div[2]/button")    
            productRemoveButton.click()
        cartIcon = self.getElementByLocator(By.CLASS_NAME,"shopping_cart_link")
        cartIcon.click()
        isCartItemsListExists = self.checkElementExistsByLocator(By.CLASS_NAME,"cart_item")
        if isCartItemsListExists == True:
            cartItemsList = self.getElementsByLocator(By.CLASS_NAME,"cart_item")        
        if isCartItemsListExists == False or (isCartItemsListExists == True and len(cartItemsList) == (len(addButtonsToClick) - randomRemove)):
            flag = True        
        assert flag
    
    def getInvalidCheckoutData():
        selectedSheet = dataGetter.getExcelDataWithSelectedSheet("invalid_test_datas.xlsx","invalid_checkouts") 
        totalRows = selectedSheet.max_row
        data = []
        for i in range(2,totalRows + 1):    
            firstName = "" if selectedSheet.cell(i,1).value == '""' else selectedSheet.cell(i,1).value
            lastName = "" if selectedSheet.cell(i,2).value == '""' else selectedSheet.cell(i,2).value
            postalCode = "" if selectedSheet.cell(i,3).value == '""' else selectedSheet.cell(i,3).value            
            tupleData = (firstName,lastName,postalCode)
            data.append(tupleData)
        return data

    @pytest.mark.parametrize("firstName,lastName,postalCode",getInvalidCheckoutData())
    def test_checkoutDataMustBeFull(self,firstName,lastName,postalCode):
        self.login()
        self.randomClickToAddToCartButton()
        cartIcon = self.getElementByLocator(By.CLASS_NAME,"shopping_cart_link")
        cartIcon.click()
        checkoutButton = self.getElementByLocator(By.ID,"checkout")
        checkoutButton.click()
        firstNameInput = self.getElementByLocator(By.ID,"first-name")
        lastNameInput = self.getElementByLocator(By.ID,"last-name")
        postalCodeInput = self.getElementByLocator(By.ID,"postal-code")
        continueButton = self.getElementByLocator(By.ID,"continue")
        firstNameInput.send_keys(firstName)
        lastNameInput.send_keys(lastName)
        postalCodeInput.send_keys(postalCode)
        continueButton.click()
        firstNameErrorIcon = self.checkElementExistsByLocator(By.CSS_SELECTOR,".form_group:nth-child(1) > .svg-inline--fa")
        lastNameErrorIcon = self.checkElementExistsByLocator(By.CSS_SELECTOR,".form_group:nth-child(2) > .svg-inline--fa")
        postalCodeErrorIcon = self.checkElementExistsByLocator(By.CSS_SELECTOR,".form_group:nth-child(3) > .svg-inline--fa")
        errorDiv = self.getElementByLocator(By.XPATH,"//*[@id='checkout_info_container']/div/form/div[1]/div[4]").is_displayed()
        if firstNameErrorIcon and lastNameErrorIcon and postalCodeErrorIcon and errorDiv:
            assert True
        else:
            assert False
    
    def test_isTotalPriceCorrect(self):
        totalTaxTrue = False
        totalPriceTrue = False
        expectedPrice = 0
        expectedTax = 0        
        self.login()
        self.randomClickToAddToCartButton()
        cartIcon = self.getElementByLocator(By.CLASS_NAME,"shopping_cart_link")
        cartIcon.click()
        checkoutButton = self.getElementByLocator(By.ID,"checkout")
        checkoutButton.click()
        firstNameInput = self.getElementByLocator(By.ID,"first-name")
        lastNameInput = self.getElementByLocator(By.ID,"last-name")
        postalCodeInput = self.getElementByLocator(By.ID,"postal-code")
        continueButton = self.getElementByLocator(By.ID,"continue")
        firstNameInput.send_keys("test")
        lastNameInput.send_keys("test")
        postalCodeInput.send_keys("12345")
        continueButton.click()
        getPricesInTheCart = self.getElementsByLocator(By.CLASS_NAME,"inventory_item_price")
        tax = self.getElementByLocator(By.CLASS_NAME,"summary_tax_label").text        
        total = self.getElementByLocator(By.CLASS_NAME,"summary_total_label").text
        getPrices = self.getProductPriceList(getPricesInTheCart)
        for price in getPrices:            
            expectedPrice += price 
            expectedTax += (price*8)/100
        calculatedTotalPrice = expectedTax + expectedPrice       
        formattedTax = format(expectedTax,'.2f')
        formattedTotalPrice = format(calculatedTotalPrice,'.2f')        
        if tax == (f"Tax: ${formattedTax}"):
            totalTaxTrue = True        
        if total == (f"Total: ${formattedTotalPrice}"):
            totalPriceTrue = True
        if totalTaxTrue and totalPriceTrue:            
            assert True
        else:
            assert False
    
    def test_completeShopping(self):
        expectedAdress = "https://www.saucedemo.com/checkout-complete.html"
        self.login()
        self.randomClickToAddToCartButton()
        cartIcon = self.getElementByLocator(By.CLASS_NAME,"shopping_cart_link")
        cartIcon.click()
        checkoutButton = self.getElementByLocator(By.ID,"checkout")
        checkoutButton.click()
        firstNameInput = self.getElementByLocator(By.ID,"first-name")
        lastNameInput = self.getElementByLocator(By.ID,"last-name")
        postalCodeInput = self.getElementByLocator(By.ID,"postal-code")
        continueButton = self.getElementByLocator(By.ID,"continue")
        firstNameInput.send_keys("kodlama")
        lastNameInput.send_keys("io")
        postalCodeInput.send_keys("12345")
        continueButton.click()
        finishButton = self.getElementByLocator(By.ID,"finish")
        finishButton.click()
        currentAdress = self.driver.current_url
        if expectedAdress == currentAdress:
            assert True
        else:
            assert False


        







        


        
        
        

            

    # id ile getirilen elementleri class içinde global e taşıyabilirsin.
    #Helpers
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
    
    def login(self):
        userName = "standard_user"
        password = "secret_sauce"       

        self.userNameInput.send_keys(userName)
        self.passwordInput.send_keys(password)
        self.loginButton.click()        
    
    def getProductPriceList(self, productList):
        productPriceList = []
        for price in productList:
            productPriceList.append(float(price.text.split("$")[1])) 
        return productPriceList
    
    def getProductNameList(self,productList):
        productNameList = []
        for normalListedNames in productList:
            productNameList.append(normalListedNames.text)
        return productNameList

    def randomClickToAddToCartButton(self):
        randomProductToAddToCart = random.randint(2,6)
        clickedButtons = []
        for i in range(1,randomProductToAddToCart + 1):
            if i == 1:
                productButton = self.getElementByLocator(By.XPATH,f"//*[@id='inventory_container']/div/div/div[2]/div[2]/button")                
            else:
                productButton = self.getElementByLocator(By.XPATH,f"//*[@id='inventory_container']/div/div[{i}]/div[2]/div[2]/button")            
            clickedButtons.append(i)
            productButton.click()
        return clickedButtons
    
    