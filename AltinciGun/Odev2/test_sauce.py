import random
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
import pathlib
import os

"""
Senaryolar:
1) Hatalı kullanıcı adı ve parola kombinasyonu ile veya boş bırakılan veri ile giriş yapılamadığını doğrula
2) Doğru kullanıcı adı ve giriş ile giriş yapılabildiğini doğrula
3) Sandwich menüden logOut butonunu doğrula
4) Flitre öğelerinin çalıştığını doğrula
    -A to Z
    -Z to A
    -low to high
    -high to low
5) Her bir öğenin resmine tıklandığında detay sayfasına gittiğini doğrula
6) Her bir öğenin başlığına tıklandığıda detay sayfasına gittiğini doğrula.
7) Add to cart butonunun çalışmasını doğrula
8) Remove butonunun çalışmasını doğrula
9) Checkout işlemi öncesi information kısmının boş geçilemediğini doğrula
10) Toplam verginin ve vergi dahil fiyatın doğru hesaplandığını doğrula
11) Baştan sonra bir alışverişin tamamlandığını doğrula.
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
        path = pathlib.Path(__file__).parent.resolve()    
        os.chdir(f"{path}")
        self.folderPath = str(date.today().strftime('%d-%m-%Y'))
        Path(self.folderPath).mkdir(exist_ok=True)        
    
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
       """
       Hatalı kullanıcı adı ve parola kombinasyonu ile giriş yapılamadığını test eden metod.
       """
       self.userNameInput.send_keys(username)
       self.passwordInput.send_keys(password)
       self.loginButton.click()
       userNameError = self.checkElementExistsByLocator(By.CSS_SELECTOR, ".form_group:nth-child(1) > .svg-inline--fa")
       passwordError = self.checkElementExistsByLocator(By.CSS_SELECTOR, ".form_group:nth-child(2) > .svg-inline--fa")
       errorMessageDiv = self.getElementByLocator(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]")
       self.takeAScreenShot("test_invalidLogin",f"usr={username}_psw={password}.png")
       if (userNameError and passwordError) and errorMessageDiv.is_displayed():
           assert True
       else:
           assert False

    def test_validLogin(self):
        """
        Doğru kullanıcı adı ve parola ile giriş yapılabildiğini test eden metod.
        """        
        validUserName = "standard_user"
        validPassword = "secret_sauce"
        expectedUrl = "https://www.saucedemo.com/inventory.html"
        self.userNameInput.send_keys(validUserName)
        self.passwordInput.send_keys(validPassword)
        self.loginButton.click()        
        checkUrl = self.driver.current_url        
        self.takeAScreenShot("test_validLogin","test_validLogin.png")
        assert checkUrl == expectedUrl        

    def test_logOutFromBurgerMenu(self): 
        """
        Başarılı giriş yapıldıktan sonra sandwich menüdeki LogOut butonu ile çıkış yapılabildiğini test eden metod.
        """   
        expectedUrl = "https://www.saucedemo.com/"     
        self.login()
        sandwichButton = self.getElementByLocator(By.ID,"react-burger-menu-btn")
        sandwichButton.click()
        logOutLink = self.getElementByLocator(By.ID,"logout_sidebar_link")
        logOutLink.click()
        currentUrl = self.driver.current_url
        self.takeAScreenShot("test_logOutFromBurgerMenu","test_logOutFromBurgerMenu.png")
        assert currentUrl == expectedUrl

    def test_filterNameAToZ(self):
        """
        Ürünleri isme göre A dan Z ye sıralayan flitrenin işlevini test eden metod.
        """
        flag = False
        self.login()        
        filterMenu = self.getElementByLocator(By.XPATH,"//*[@id='header_container']/div[2]/div/span/select")
        filterAToZ = self.getElementByLocator(By.XPATH,"//*[@id='header_container']/div[2]/div/span/select/option[1]")
        filterMenu.click()
        filterAToZ.click()
        productNameDivs = self.getElementsByLocator(By.XPATH,"//div[@class='inventory_item_name']")
        productNameAToZ = self.getProductNameList(productNameDivs)   
        self.takeAScreenShot("test_filterNameAToZ","test_filterNameAToZ.png")            
        if sorted(productNameAToZ):
            flag = True
        else:
            flag = False
        assert flag

    def test_filterNameZToA(self):   
        """
        Ürünleri isme göre Z den A ya sıralayan flitrenin işlevini test eden metod.
        """     
        flag = False
        self.login()
        filterMenu = self.getElementByLocator(By.XPATH,"//*[@id='header_container']/div[2]/div/span/select")
        filterZtoA = self.getElementByLocator(By.XPATH,"//*[@id='header_container']/div[2]/div/span/select/option[2]")
        filterMenu.click()
        filterZtoA.click()
        productNameDivs = self.getElementsByLocator(By.XPATH,"//div[@class='inventory_item_name']")
        productNameZToA = self.getProductNameList(productNameDivs)    
        self.takeAScreenShot("test_filterNameZToA","test_filterNameZToA.png")          
        if sorted(productNameZToA,reverse=True):
            flag = True
        else:
            flag = False        
        assert flag
    
    def test_filterPriceLowToHigh(self):
        """
        Ürünleri fiyatına göre düşükten dan yükseğe sıralayan flitrenin işlevini test eden metod.
        """
        flag = False
        self.login()        
        filterMenu = self.getElementByLocator(By.XPATH,"//*[@id='header_container']/div[2]/div/span/select")
        filterPriceLowToHigh = self.getElementByLocator(By.XPATH,"//*[@id='header_container']/div[2]/div/span/select/option[3]")
        filterMenu.click()
        filterPriceLowToHigh.click()
        productPricesDivs = self.getElementsByLocator(By.XPATH,"//div[@class='inventory_item_price']")
        productPricesSortedToHigher = self.getProductPriceList(productPricesDivs)     
        self.takeAScreenShot("test_filterPriceLowToHigh","test_filterPriceLowToHigh.png")           
        if sorted(productPricesSortedToHigher):
            flag = True
        else:
            flag = False
        assert flag

    def test_filterPriceHighToLow(self):
        """
        Ürünleri fiyatına göre yüksekten düşüğe sıralayan flitrenin işlevini test eden metod.
        """
        flag = False
        self.login()        
        filterMenu = self.getElementByLocator(By.XPATH,"//*[@id='header_container']/div[2]/div/span/select")
        filterPriceHighToLow = self.getElementByLocator(By.XPATH,"//*[@id='header_container']/div[2]/div/span/select/option[4]")
        filterMenu.click()
        filterPriceHighToLow.click()
        productPricesDivs = self.getElementsByLocator(By.XPATH,"//div[@class='inventory_item_price']")
        productPricesSortedToLower = self.getProductPriceList(productPricesDivs)       
        self.takeAScreenShot("test_filterPriceHighToLow","test_filterPriceHighToLow.png")       
        if sorted(productPricesSortedToLower,reverse=True):
            flag = True
        else:
            flag = False
        assert flag

    def test_imageGoesToProductDetail(self):
        """
        Rastgele bir ürün seçip bu ürünün resmine tıklandığında ürünün detay fayfasına gidilebildiğini test eden metod.
        """
        selectRandomProduct = random.randint(0,5)
        expectedUrl = f"https://www.saucedemo.com/inventory-item.html?id={selectRandomProduct}"
        self.login()
        productImage = self.getElementByLocator(By.ID,f"item_{selectRandomProduct}_img_link")
        productImage.click()
        currentLocation = self.driver.current_url
        self.takeAScreenShot("test_imageGoesToProductDetail","test_imageGoesToProductDetail.png")
        assert currentLocation == expectedUrl
    
    def test_titleGoesToProductDetail(self):
        """
        Rastgele bir ürün seçip bu ürünün başlığına tıklandığında ürünün detay fayfasına gidilebildiğini test eden metod.
        """
        selectRandomProduct = random.randint(0,5)
        expectedUrl = f"https://www.saucedemo.com/inventory-item.html?id={selectRandomProduct}"
        self.login()
        productTitleLink = self.getElementByLocator(By.ID,f"item_{selectRandomProduct}_title_link")
        productTitleLink.click()
        currentLocation = self.driver.current_url
        self.takeAScreenShot("test_titleGoesToProductDetail","test_titleGoesToProductDetail.png")
        assert currentLocation == expectedUrl
            
    def test_addToCartButton(self):
        """
        Rastgele sayıdaki ürün için Add to cart butonu tıklandığında ürünlerin sepete eklendiğini test eden metod.
        """
        self.login()        
        buttonsToClick = len(self.randomClickToAddToCartButton())    
        cartIcon = self.getElementByLocator(By.CLASS_NAME,"shopping_cart_link")
        cartIcon.click()
        cartItemsList = self.getElementsByLocator(By.CLASS_NAME,"cart_item")
        self.takeAScreenShot("test_addToCartButton","test_addToCartButton.png")
        assert buttonsToClick == len(cartItemsList)   

    def test_removeButton(self):
        """
        Önceden sepete eklenmiş ürünler için Remove butonuna basıldığında ürünlerin sepetten çıkarıldığını test eden metod.
        """
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
        self.takeAScreenShot("test_removeButton","test_removeButton.png")       
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
        """
        Ürünler sepete eklendikten sonra "Checkout: Your Information" kısmında sistemin istediği kullanıcı bilgilerinin boş geçilemediğini test eden metod. (Ürünler rastgele olarak sisteme eklenmektedir.)
        """
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
        self.takeAScreenShot("test_checkoutDataMustBeFull",f"first={firstName}_last={lastName}_postal={postalCode}.png")
        if firstNameErrorIcon and lastNameErrorIcon and postalCodeErrorIcon and errorDiv:
            assert True
        else:
            assert False
    
    def test_isTotalPriceCorrect(self):
        """
        Rastgele sayıda sepete eklenen ürünlerin, "Checkout: Overview" ekranında toplam vergi ve vergi dahil fiyat bilgilerinin doğru hesaplandığını test eden metod.
        """
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
        self.takeAScreenShot("test_isTotalPriceCorrect",f"tax={formattedTax}_tprice={formattedTotalPrice}.png")
        if totalTaxTrue and totalPriceTrue:            
            assert True
        else:
            assert False
    
    def test_completeShopping(self):
        """
        Baştan sona sistemden başarı ile satınalma yapılabildiğini test eden metod. (Sepete eklenen ürünler rastgele seçilmektedir.)
        """
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
        self.takeAScreenShot("test_completeShopping","test_completeShopping.png")
        if expectedAdress == currentAdress:
            assert True
        else:
            assert False


        
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
    
    def createMethodsScreenshotFolder(self,methodName):
        methodsPath = (f"{self.folderPath}/{methodName}")
        Path(f"{methodsPath}").mkdir(exist_ok=True)        
        return methodsPath
    
    def takeAScreenShot(self,methodName,imageName):
        methodsPath = self.createMethodsScreenshotFolder(methodName)
        self.driver.save_screenshot(f"{methodsPath}/{imageName}")
    