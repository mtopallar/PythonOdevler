class Matematik:
    def __init__(self,sayi1,sayi2) -> None: # instance oluştururkenki parantez aslında bu. (ctor) ctor sefl parametresi istediği için self i kullanıyoruz. Yine ctor içindeki değişkene sadece ctor bloğundan erişilebildiğinden atama yapmamız gerekiyor.
        print("Matematik Başladı / referansı oluştu.")
        self.sayi1 = sayi1
        self.sayi2 = sayi2
        pass

    def topla(self):
        return self.sayi1 + self.sayi2
    
    def cikar(self):
        return self.sayi1 - self.sayi2
    
    def bol(self):
        return self.sayi1 / self.sayi2
    
    def carp(self):
        return self.sayi1 * self.sayi2

matematik = Matematik(6,7) #instance / ctor
sonuc = matematik.bol()
print("Sonuç : "+ str(sonuc))

class Istatistik(Matematik):
    def __init__(self, sayi1, sayi2) -> None:
        super().__init__(sayi1, sayi2)
    
    def varyansHesapla(self):
        return self.sayi1 * self.sayi2

istatistik = Istatistik(5,8) #Matematiği inherit ettiği için matematiğin sayi1 ve sayi 2 sini istiyor bizden.
varyans = istatistik.varyansHesapla()
bolum = istatistik.bol() # istatistik sınıfı Matematik sınıfının fonksiyonlarına da erişebilir. => inheritance(kalıtım)
print(varyans)

#Yine Pythonda da bir sınıf sadece 1 sınıftan miras alabilir.
#istatistik sınıfının base class ı Matematiktir. Yani Istatistik sınıfındaki super() keywordu Matematik sınıfını işaret eder. 