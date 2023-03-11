krediler = ["Hızlı Kredi","Maaşını Halkbank'tan Alanlara Özel","Mutlu Emekli İhtiyaç Kredisi"]

#for in döngüsü, alias takma ad
for kredi in krediler:
    print(kredi)

for i in range(len(krediler)):
    print(krediler[i])

for i in range(3,10): #saymaya 3 ten başlıyor. 3 dahil 9 dahil (10 dahil değil)
    print(i)

for i in range(0,10,2): # 0 dan başla, 10 a kadar git, 2 şerli arttır.
    print(i)

for kredi in krediler:
    print("<option>" + kredi+ "</option>")