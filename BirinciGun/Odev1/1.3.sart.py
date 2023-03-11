#login butonu / karsilama ekranı (benzer şekilde kullanıcı menüsü veya çıkış butonu da aynı mantıkla buraya eklenebilir.)
girisYapildiMi = False
if girisYapildiMi:
    print("Hoşgeldiniz.")
else:
    print("Lütfen giris yapiniz.")

#ödevin tamamlandığını gösteren tik işareti
odevTamamlandiMi = True
if odevTamamlandiMi:
    print("Tik işareti")
else:
    print("Yarım daire işareti")

#Kursa kaydol veya kurs içeriği
kursaKayitliMi = False
if kursaKayitliMi:
    print("Kurs içeriği")
else:
    print("İçeriği görüntüleyebilmek için giriy yapın ya da kursa kaydolun.")

#Yoruma Metin Ekleyin Uyarısı
metinUzunluğu = 0 #trim edilmiş metnin uzunluğu
if metinUzunluğu > 0 :
    print("Yorumunuz başarıyla gönderildi.")
else:
    print("Lütfen yoruma metin ekleyin.")
