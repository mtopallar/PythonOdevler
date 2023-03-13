class Person:
    def __init__(self,name,lastName) -> None:
        self.name = name #self için bir name oluşturup gönderilen name e onu atıyoruz.
        self.lastName = lastName #self için bir lastName oluşturup gönderilen lastName i ona atıyoruz.
        pass


musteri1 = Person("Ahmet","Demiroğ")
musteri2 = Person("Kerem","Varış")
musteri3 = Person("İlker","Tural")
print(musteri1.name)
print(musteri1.lastName)