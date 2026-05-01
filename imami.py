from datetime import datetime

class Arac:
  def __init__(self, arac_id,marka,model,km):
    self.arac_id = arac_id
    self.marka = marka
    self.model = model
    self.kilometre = km
    self.musait_mi= True

  def arac_durumu_guncelle(self,durum):
    self.musait_mi = durum

  def kilometre_guncelle(self, yeni_km):
      if yeni_km >= self.kilometre:
          self.kilometre = yeni_km
          return True
      else:
          print(f"Hatali km! Mevcut km: {self.kilometre}")
          return False



class Kullanici:
  def __init__(self,kullanici_id,ad,ehliyet_no):
    self.kullanici_id = kullanici_id
    self.ad = ad
    self.ehliyet_no = ehliyet_no

  def kiralama_gecmisi (self,kiralamalar):
    print(f"\n {self.ad} - kiralamma gecmisi:")
    for k in kiralamalar:
      if k.kullanici == self:
        print(f"   {k.arac.marka} {k.arac.model}")


class Kiralama:
  def __init__(self,kiralama_id,arac,kullanici):
    self.kiralama_id = kiralama_id
    self.arac = arac
    self.kullanici = kullanici
    self.baslangic_saati = None
    self.bitis_saati = None

  def kiralama_baslat(self):
    if not self.arac.musait_mi:
      print("Arac dolu!")
      return False
    self.arac.arac_durumu_guncelle(False)
    self.baslangic_saati = datetime.now()
    print(f"{self.kullanici.ad} -> {self.arac.marka} {self.arac.model} kiralandi")
    return True

  def kiralama_bitir(self, yeni_km):
    # önce km kontrol
    if not self.arac.kilometre_guncelle(yeni_km):
        print("Kiralama bitirilemedi!")
        return False

    # sadece doğruysa buraya gelir
    self.bitis_saati = datetime.now()
    self.arac.arac_durumu_guncelle(True)

    sure = self.bitis_saati - self.baslangic_saati
    print(f"Kiralama bitti sure: {sure}")
    return True

  def kiralama_bilgisi(self):
    print(f"kiralama # {self.kiralama_id} : {self.kullanici.ad}-> {self.arac.marka} {self.arac.model}")


araclar = {}
kullanicilar = {}
kiralamalar = []
kiralama_id = 1

araclar [100]= Arac(100,"Renault","clio",45000)
araclar [101] = Arac(101,"Fiat","Egea",70000)
araclar [102] = Arac (102,"Volvo","polo",120000)

kullanicilar [1] = Kullanici(1,"Ahmet","Tr343334")
kullanicilar [2] = Kullanici(2,"Azam","tr974649")
kullanicilar [3] = Kullanici(3,"Yilmaz","90000")

while True:
  print("\n" + "="*40)
  print("Arac Paylasim Sistemi")
  print("="*40)
  print("1 - Araclari listele")
  print("2 - Musait Araclar")
  print("3 - Kullanicilari listele")
  print("4 - Arac Kirala")
  print("5 - Kiralamayi Bitir")
  print("6 - Kiralama Gecmisi")
  print("7 - Tum Kiralamalar")
  print("0 - Cikis" )

  secim = input("Secim: ")

  if secim == "1":
    print("\n -- Tum Araclar --")
    for a in araclar.values():
      durum = "Musait" if a.musait_mi else "Kirada"
      print(f"{a.arac_id} | {a.marka} {a.model} | {a.kilometre} km | {durum}")

  elif secim == "2":
    print("\n -- Musait Araclar --")
    for a in araclar.values():
      if a.musait_mi:
        print(f"{a.arac_id} | {a.marka} {a.model}")

  elif secim == "3":
    print("\n -- Kullanicilar Listesi --")
    for k in kullanicilar.values():
      print(f" {k.kullanici_id} | {k.ad} | {k.ehliyet_no}")

  elif secim == "4":
    print("\n -- Yeni Kiralama --")
    arac_id = int(input("Arac ID: "))
    kullanici_id = int(input("Kullanici ID: "))

    if arac_id in araclar and kullanici_id in kullanicilar:
      arac = araclar[arac_id]
      kullanici = kullanicilar[kullanici_id]

      if arac.musait_mi:
        kiralama = Kiralama(kiralama_id,arac,kullanici)
        kiralama.kiralama_baslat()
        kiralamalar.append(kiralama)
        kiralama_id += 1
      else:
        print("Arac Musait Degil")
    else:
      print("Hatali ID")

  elif secim == "5":
    print("\n -- Kiralama Bitir --")
    for k in kiralamalar:
      if k.bitis_saati is None:
        print(f"ID: {k.kiralama_id} | {k.kullanici.ad} | {k.arac.marka}")

    kid = int (input("Kiralama ID: "))
    for k in kiralamalar:
      if k.kiralama_id == kid and k.bitis_saati is None:
        yeni_km = float(input("Yeni Kilometre: "))
        k.kiralama_bitir(yeni_km)
        break
      else:
        print("Bulanamadi")
  elif secim == "6":
    print("\n -- Kiralama Gecmisi --")
    for k in kullanicilar.values():
      print(f"{k.kullanici_id} - {k.ad}")
    kid = int(input("Kullanici ID: "))
    if kid in kullanicilar:
      kullanicilar[kid].kiralama_gecmisi(kiralamalar)

  elif secim == "7":
    print("\n -- Tum Kiralamalar --")
    for k in kiralamalar:
      k.kiralama_bilgisi()

  elif secim == "0":
    print("Cikis yapiliyor...")
    break
  else:
    print("Gecersiz secim")

  input("\n Devam icin ENTER")

