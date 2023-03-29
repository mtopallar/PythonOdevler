# Python Ödevler
### Pytest'de Anotasyonlar (Decoratörler)
Anotasyonlar birçok yazılım dilinde mevcuttur ve üzerlerine yazıldıkları nesneye çeşitli özellikler kazandırmak, onlara nitelik katmak için kullanılırlar. Pytest içerisinde bulunan mark modülü içinde kullanabileceğimiz bazı hazır anotasyonlar mevcuttur. Bunlar:

- pytest.mark.filterwarnings
- pytest.mark.parametrize
- pytest.mark.skip
- pytest.mark.skipif
- pytest.mark.usefixtures
- pytest.mark.xfail
- Custom marks

#### -pytest.mark.filterwarnings(filter)
Pytest'in web sitesinde ilgili anotasyon için aşağıdaki açıklama mevcuttur:
> Belirli test öğelerine uyarı filtreleri eklemek için kullanabilirsiniz , bu da test, sınıf ve hatta modül düzeyinde hangi uyarıların yakalanması gerektiğini daha iyi kontrol etmenizi sağlar.

Özetlemek gerekirse bu anotasyon ile ilgili metod, class hatta modül düzeyince uyarı flitrelemesi yapılabilmektedir.

#### -pytest.mark.parametrize
Bir test sırasında aynı test senaryosunu birden fazla değişken ile çalıştırmak istediğimizde bu anotasyonu kullanırız. Anotasyon ile verilen değerler sırası ile aynı fonksiyon kullanılarak koşulur ve her koşum için bize testin başarılı olup olmadığı bildirilir.

```python
@pytest.mark.parametrize("username,password",[("1","1"),("kullaniciAdim","sifrem")])
    def test_invalid_login(self,username,password):   
        driver = webdriver.Chrome(ChromeDriverManager().install())        
        driver.get("https://www.saucedemo.com/")     
        userNameInput = driver.find_element(By.ID,"user-name")        
        passwordInput = driver.find_element(By.ID,"password")
        userNameInput.send_keys(username)
        passwordInput.send_keys(password)
        loginButton = driver.find_element(By.ID,"login-button")
        loginButton.click()
        errorMessage = self.driver.find_element(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")                
        assert errorMessage.text == "Epic sadface: Username and password do not match any user in this service"
```
örnekteki test sırasıyla username ve password değişkenleri için tuple içindeki değerleri sırasıyla atar. Yani test ilk koşumda username için 1 ve password için 1 değerlerini kullanarak ilgili testi gerçekleştirir, ardından, aynı fonksiyon bu sefer username için kullaniciAdim, password için ise sifrem değeri ile test edilir. Her iki durumda da dönen cevabın "Epic sadface: Username and password do not match any user in this service" olması durumunda test başarılı kabul edilir.

#### -pytest.mark.skip
Bu anotasyon ilgili test fonksiyonunu herhangi bir koşul belirtmek zorunda olmaksızın atlamayı sağlar. İstenirse ilgili testin neden atlandığına dair bir not (reason) belirtilebilir.

#### -pytest.mark.skipif
`pytest.mark.skip` anotasyonuna benzer şekilde yine bir testi atlamak için kullanılır. Ancak bu sefer atlama işlemi verilen bir şarta bağlıdır. Bu anotasyon için koşul vermek zorunlu bir parametre iken, sebep belirtmek yine tercihen yapılabilir.

#### -pytest.mark.usefixtures
Bu dekoratör daha önceden fixture olarak işaretlenmiş bir yapıyı (örneğin bir metodu) bir test koşulmadan önce çağırıp kullanmaya yarar. Örnek vermek gerekirse;

```python
@pytest.fixture
def cleandir():
    # içeriğinin temizlenmesi istenen direction ile ilgili kodlar
```

```python
@pytest.mark.usefixtures("cleandir")
class TestClass:
    def test_methodu(self):
       # Bir yukarıda tanımlanan ve fixture olarak işaretlenen metodu, 
       # buradaki test metodumuz koşulurken kullanabilmek için .usefixtures 
       # anotasyonunu kullandık ve anotasyon içine fixture olan metodumuzun adını 
       # verdik: @pytest.mark.usefixtures("cleandir")
```

#### -pytest.mark.xfail
Bir test işleminden "başarısız sonuç beklediğimizi" belirtmek için bu anotasyonu kullanırız.

#### Custom marks
Custom marks ise kendi anotasyonlarımızı oluşturup kullanmak istediğimizde başvuracağımız bir yapıdır. Genel anlamda pytest.mark objesi yardımı ile dinamik olarak oluşturulur ve kullanılır.