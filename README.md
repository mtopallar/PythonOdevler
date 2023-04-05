# Python Ödevler

## 5.Gün Ödevleri
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

### 5.Gün Testing Area Görseli
![](https://github.com/mtopallar/PythonOdevler/blob/master/BesinciGun/Odev2/testing_area.jpg)

## 6.Gün Ödevleri

### Ödev 1
Daha önceki ödevlerde VS Code ile yazdığımız test senaryolarını Selenium IDE ile tekrar gerçekleştirip, kodları IDE'den export ederek yine VS Code ortamında inceledik. Kod yazarak yaptığımız ancak IDE ortamında nasıl yapılacağını bilmediğim konuları incelerken yeni yöntemler öğrendim.

![](https://github.com/mtopallar/PythonOdevler/blob/master/AltinciGun/Odev1/altinciGun_1.odev.jpg)

### Ödev 2

> Testlerimizi gerçekleştirdiğimiz "https://www.saucedemo.com/" sitesinde, kendi belirlediğiniz tüm aksiyonları test edecek bir proje geliştiriniz. Bu projeyi geliştirirken Selenium IDE kullanabilir, testlerinizi buradan export edip refactor edebilirsiniz. Bu projeyi tamamlarken derste kullandığımız yaklaşımlara uymaya dikkat ediniz.

Bu ödevde selenium IDE kullanmadım. Kodları VS Code ile kendim yazmayı tercih ettim. Belirlediğim senaryolar şu şekilde oldu:

Senaryolar:
1. Hatalı kullanıcı adı ve parola kombinasyonu ile veya boş bırakılan veri ile giriş yapılamadığını doğrula
2. Doğru kullanıcı adı ve giriş ile giriş yapılabildiğini doğrula
3. Sandwich menüden logout butonunu doğrula
4. Flitre öğelerinin çalıştığını doğrula
    - A to Z
    - Z to A
    - low to high
    - high to low
5. Her bir öğenin resmine tıklandığında detay sayfasına gittiğini doğrula
6. Her bir öğenin başlığına tıklandığıda detay sayfasına gittiğini doğrula
7. Add to cart butonunun çalışmasını doğrula
8. Remove butonunun çalışmasını doğrula
9. Checkout işlemi öncesi information kısmının boş geçilemediğini doğrula
10. Toplam verginin ve vergi dahil fiyatın doğru hesaplandığını doğrula
11. Baştan sonra bir alışverişin tamamlandığını doğrula

Belirlediğim senaryolara göre testlerimi yazdım, gerekli helper metodlarımı oluşturdum, karşılaştığım bazı klasör hatalarının çözümlerinin nasıl olabileceğini araştırıp çözüme kavuşturdum. openpyxl gibi paketlerle çalışırken pytest bazen kendi çalışma lokasyonundan ötürü "./data" gibi kısa adres belirlemelerinde yol doğru olsa da klasörü görmediğini ifade edebiliyor. Bu sorunu klasör adını "./data" gibi kısa şekilde belirtmek yerine tam adres olarak verdiğimizde aşabiliyoruz ancak, bu sürdürülebilir bir yapı değil. Öyle ki bu repositorydeki kodları bir başka bilgisayarda çalıştırmak için adres kısmının her bilgisayara göre yeniden düzenlenmesi gerekir. Bunun önüne geçebilmek için klasör lokasyonunun otomatik bir şekilde yakalanması gerekir. Bunu sağlamak için;

```python
    import pathlib
    import os
    path = pathlib.Path(__file__).parent.resolve()    
    os.chdir(f"{path}")
```
paketlerini ve yöntemini kullandım. Buradaki path değişkeni projenin klasör hiyerarşisine göre düzenlenmelidir. Bu yöntem ile pytest in bakması gerektiği yol belirtilmiş oluyor. Farklı yöntemler de mutlaka ki mevcuttur ancak ben bu yöntemi tercih ettim. Detaylı kullanım için ilgili repositorydeki kodlarımı inceleyebilirsiniz.

Testlerin hepsi için ekran görüntüsü alma işlevini ekledim. Daha kontrol edilebilir bir yapı için önce o testin çalıştırıldığı günün tarihini gg-aa-yyyy şeklinde formatlayıp bunu isim olarak kullanan bir klasör oluşturduktan sonra, bu klasörün içine her metod için ilgili metod ismini isim olarak kullanan ikinci bir klasörü oluşturan ve bu ikinci klasörün içine ilgili test için istenen resimleri kaydeden bir yapı oluşturdum ve ilgili metodlarda doğru noktalarda bu yapıyı çağırdım.

Screenshot alırken bazı pencerelerin scroll ile kaydırılması gerektiğinden, bu işlem için yardımcı bir metod yazdım. Sayfanın scroll ederek görüntüleri alındığında resmin adına _1_ _2_ _3_ gibi ibarelerle eklenerek resmin yeniden adlandırılması sağlandı.

Testlerin yazımı bittikten sonra magic string den kurtulabilmek adına over-design a kaçmamaya çalışarak gerekli refactoring işlemlerini yaptım. Ve test senaryolarını pytest aracılığı ile çalıştırdım:

![](https://github.com/mtopallar/PythonOdevler/blob/master/AltinciGun/Odev2/altinciGun_2.odev.jpg)