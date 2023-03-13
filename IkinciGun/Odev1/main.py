# 1) listeye tek öğrenci ekleme
# 2) listeden tek öğrenci kaldırma (isim - soyisim ile)
# 3) listeye liste şeklinde öğrenci ekleme
# 4) listeden birden fazla öğrenci kaldırma (döngü ile)
# 5) tüm öğrencileri öğrenci numaraları ile ekrana yazdırma

students = ["Engin Demiroğ","Halit Kalaycı","Murat Kurtboğan"]
studentList = []
selection = ""

print("")
print("Yapmak istediğiniz işlemin işlem numarasını girip enter a basınız.")
print("1) Listeye öğrenci ekle...")
print("2) Listeden seçili öğrenciyi kaldır...")
print("3) Listeye birden fazla öğrenci ekle...")
print("4) Listeden birden fazla öğrenci kaldır...")
print("5) Öğrenci listesini göster...")
print("")
selection = input("Seçiminiz: ")
print("")

def addSingleStudentToList(studentName):
    if checkStudentNameIfItIsEmpty(studentName):
        students.append(studentName)    

def removeSingleStudentFromList(studentName):
    if checkStudentNameIfItIsEmpty(studentName):
        students.remove(studentName)

def extendStudentListWithAnotherList(listToAdd):
    if checkStudentListIfItIsEmpty(listToAdd):
        students.extend(listToAdd)

def removeStudentsByList(listToRemove):
    if checkStudentListIfItIsEmpty(listToRemove):
        for studentForDelete in studentList:
            students.remove(studentForDelete)

def getStudentList():
    for i in range(len(students)):
        print(f"Öğrenci numarası: {i} / Ad - Soyad: {students[i]}")

#Helper Methods
def checkStudentNameIfItIsEmpty(studentName):
    if len(studentName) == 0:
        print("Öğrenci bilgileri boş bırakılamaz.")
        return False
    else:
        return True

def checkStudentListIfItIsEmpty(listToCheck):
    if len(listToCheck) == 0:
        print("Boş liste ile işlem yapılamaz.")
        return False
    else:
        return True
    
def checkListIfIncludesEmptyString(listToCheck):
    flag = False
    for student in listToCheck:
        if len(student) == 0:
            print("Listeye belirttiğiniz sayıda isim girmediniz.")
            flag = False
            break
        else:
            flag = True
    return flag
#End of helper methods

if selection == "1":
    studentToAdd = input ("Öğrenci Ad - Soyad : ")
    addSingleStudentToList(studentToAdd)
    # Öğrencileri listele
    print("Güncel liste: ")
    getStudentList()
elif selection == "2":
    studentToRemove = input("Silinecek öğrencinin Ad - Soyad : ")
    removeSingleStudentFromList(studentToRemove)
    #Öğrencileri listele
    print("Güncel liste: ")
    getStudentList()
elif selection == "3":
    count = int(input("Kaç öğrenci eklemek istediğinizi belirtiniz: "))
    i = 0
    while i < count:
        if count == 0:
            break
        studentList.append(input(f"{i+1}. Öğrenci Ad - Soyadı: "))
        i += 1
    
    if checkListIfIncludesEmptyString(studentList):        
        extendStudentListWithAnotherList(studentList)
        studentList=[]
        print("İşlem tamamlandı.")
        # Öğrencileri listele        
        print("Güncel liste: ")
        getStudentList()
elif selection == "4":
    count = int(input("Kaç öğrenci silmek istediğinizi belirtiniz: "))
    if count > len(students):
        print(f"Listede toplam {len(students)} adet öğrenci mevcut.")
    else:
        i = 0
        while i < count:
            if count == 0:
                break
            studentList.append(input(f"Silinecek {i+1}. Öğrenci: Ad - Soyadı: "))
            i += 1    
        if checkListIfIncludesEmptyString(studentList):        
            removeStudentsByList(studentList)
            studentList = []
            print("İşlem tamamlandı.")
            # Öğrencileri listele
            print("Güncel liste: ")
            getStudentList()
elif selection == "5":
    getStudentList()
else:
    print("Hatalı bir seçim yaptınız.")  
    