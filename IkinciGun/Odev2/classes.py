# özellik barındıran nesneler - operasyon barındıran nesneler
# Python case sensitive'dir.
class Banka:
    def krediBasvur(self):
        print("Kredi başvurusu yapıldı")

    def krediHesapla(self):
        print("Hesaplar yapıldı")
    
    # krediHesapla() burada (class içinde) kullanınca self gerekmedi. Class dışından kullanırken self gerekti.    

banka = Banka()
banka.krediBasvur()

#self = this