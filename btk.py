class Arac:
  def __init__(self,arac_id,marka,model,kilometre,musait_mi=True):
    self.arac_id = arac_id
    self.marka = marka
    self.model = model
    self.kilometre = kilometre
    self.musait_mi = musait_mi

  def arac_durumu_guncelle(self,durum):
    self.musait_mi = durum
    if durum == True:
      print("Arac Musait")
    else:
      print("Arac suanda musait degil")

  def kilometre_guncelle(self,kilometre):
    print(f"Aracin Mevcut kilometresi {self.kilometre}")
    if kilometre >= self.kilometre:
      self.kilometre = kilometre
      print(f"yeni Kilometre {kilometre}")
    else:
      print("Aracin yeni km. yanlis")

class Kullanici:
  def __init__(self,kullanici_id,ad,ehliyet_no):
    self.kullanici_id = kullanici_id
    self.ad = ad
    self.ehliyet_no = ehliyet_no

from datetime import datetime
class Kiralama:
  def __init__(self,kiralama_id,arac,kullanici,baslangic_saati,bitis_saati):
    self.kiralama_id = kiralama_id
    self.arac = arac
    self.kullanici = kullanici
    self.baslangic_saati = baslangic_saati
    self.bitis_saati = bitis_saati

  def kiralama_baslat(self,tarih,saat):
    self.baslangic_saati = saat
    self.arac.musait_mi = False
    print(f"Arac {self.arac.marka} kiralamasi basladi")

  def kiralama_bitir(self):
    self.bitis_saati = datetime.now()
    self.arac.musait_mi = True
    print("arac kiralamasi bitti")

arac1 = Arac(1, "BMW", "X5", 50000, True)
kullanici1 = Kullanici(101, "Ahmad", 12345)
kiralama1 = Kiralama(1, arac1, kullanici1, None, None)

kiralama1.kiralama_baslat("2026-04-23","14:00")