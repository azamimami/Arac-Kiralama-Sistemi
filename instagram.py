# randevular = []
# class Hasta:
#   def __init__(self,hasta_id,ad,tc,telefon):
#     self.hasta_id = hasta_id
#     self.ad = ad
#     self.tc = tc
#     self.telefon = telefon



#   def randevu_al(self,doktor,tarih,saat):
#     if doktor.uygunluk_kontrol(saat):
#       Randevu.randevu_olustur(tarih,saat,doktor,self)
#       doktor.uygun_saatler.remove(saat)
#       print("Randevu olusturuldu.")

#     else:
#       print("Bu saat uygun degil!")



# class Doktor:
#   def __init__(self,doktor_id,ad,uzmanlik,uygun_saatler):
#     self.doktor_id = doktor_id
#     self.ad = ad
#     self.uzmanlik = uzmanlik
#     self.uygun_saatler = uygun_saatler


#   def uygunluk_kontrol(self,saat):
#     return saat in self.uygun_saatler



# class Randevu:
#   def __init__(self,randevu_id,tarih,saat,doktor,hasta):
#     self.randevu_id = randevu_id
#     self.tarih = tarih
#     self.saat = saat
#     self.doktor = doktor
#     self.hasta = hasta

#   @staticmethod
#   def randevu_olustur(tarih, saat, doktor, hasta):
#       r = Randevu(len(randevular)+1, tarih, saat, doktor, hasta)
#       randevular.append(r)


#   def randevu_iptal(self):
#       self.doktor.uygun_saatler.append(self.saat)
#       randevular.remove(self)
#       print("Randevu iptal edildi.")


#   @staticmethod
#   def gunluk_randevu_goruntulenme(tarih):
#     bulundu = False

#     for r in randevular:
#       if r.tarih == tarih:
#         print(f"{r.randevu_id} - {r.hasta.ad} - {r.doktor.ad} - {r.saat}")
#         bulundu = True

#     if not bulundu:
#       print("Bu tarihte randevu yok.")



# def menu():
#   print("\n --- Hos geldiniz ---")
#   print("1 - Hasta giris yapin ")
#   print("2 - Randevu alma islemi")
#   return input("Seciminiz hangisi: ")

# while True:
#   secim = menu()

#   if secim == "1":
#     print(f"Hos geldiniz, {Hasta.ad}")

#   elif secim == "2":
#     Hasta.ad.randevu_al()


randevular = []

class Hasta:
    def __init__(self, hasta_id, ad, tc, telefon):
        self.hasta_id = hasta_id
        self.ad = ad
        self.tc = tc
        self.telefon = telefon

    def randevu_al(self, doktor, tarih, saat):  # Metod 1
        if doktor.uygunluk_kontrol(saat):
            Randevu.randevu_olustur(tarih, saat, doktor, self)
            doktor.uygun_saatler.remove(saat)
            print("Randevu olusturuldu")
        else:
            print("Saat uygun degil")

class Doktor:
    def __init__(self, doktor_id, ad, uzmanlik, uygun_saatler):
        self.doktor_id = doktor_id
        self.ad = ad
        self.uzmanlik = uzmanlik
        self.uygun_saatler = uygun_saatler

    def uygunluk_kontrol(self, saat):  # Metod 2
        return saat in self.uygun_saatler

class Randevu:
    def __init__(self, randevu_id, tarih, saat, doktor, hasta):
        self.randevu_id = randevu_id
        self.tarih = tarih
        self.saat = saat
        self.doktor = doktor
        self.hasta = hasta

    @staticmethod
    def randevu_olustur(tarih, saat, doktor, hasta):  # Metod 3
        randevular.append(Randevu(len(randevular)+1, tarih, saat, doktor, hasta))

    def randevu_iptal(self):  # Metod 4
        self.doktor.uygun_saatler.append(self.saat)
        randevular.remove(self)
        print("Randevu iptal edildi")

    @staticmethod
    def gunluk_randevu_goruntule(tarih):  # Metod 5
        print(f"\n{tarih} randevulari:")
        var = False
        for r in randevular:
            if r.tarih == tarih:
                print(f"{r.saat} - {r.hasta.ad} - {r.doktor.ad}")
                var = True
        if not var:
            print("Randevu yok")

# 5 hasta
hastalar = [
    Hasta(1, "Ali", "111", "5551"),
    Hasta(2, "Ayse", "222", "5552"),
    Hasta(3, "Mehmet", "333", "5553"),
    Hasta(4, "Zeynep", "444", "5554"),
    Hasta(5, "Can", "555", "5555")
]

# 5 doktor
doktorlar = [
    Doktor(1, "Dr.Ahmet", "Kardiyoloji", ["09:00", "10:00"]),
    Doktor(2, "Dr.Elif", "Dahiliye", ["09:30", "10:30"]),
    Doktor(3, "Dr.Murat", "Ortopedi", ["11:00", "14:00"]),
    Doktor(4, "Dr.Selin", "Goz", ["13:00", "15:00"]),
    Doktor(5, "Dr.Burak", "KBB", ["14:30", "16:00"])
]

def menu():
    print("\n1-Hasta Giris")
    print("2-Randevu Al")
    print("3-Randevu Iptal")
    print("4-Gunluk Randevu ")
    print("5-Cikis")
    return input("Secim: ")

# Ana program
aktif = None
while True:
    secim = menu()

    if secim == "1":
        print("\nHastalar:")
        for h in hastalar:
            print(f"{h.hasta_id}-{h.ad}")
        id = int(input("Hasta ID: "))
        for h in hastalar:
            if h.hasta_id == id:
                aktif = h
                print(f"Hosgeldin {h.ad}")
                break
        else:
            print("Hata")

    elif secim == "2":
        if not aktif:
            print("Once giris yapin")
        else:
            print("\nDoktorlar:")
            for d in doktorlar:
                print(f"{d.doktor_id}-{d.ad}({d.uzmanlik})")
            did = int(input("Doktor ID: "))
            for d in doktorlar:
                if d.doktor_id == did:
                    print(f"Musait saatler: {d.uygun_saatler}")
                    tarih = input("Tarih: ")
                    saat = input("Saat: ")
                    aktif.randevu_al(d, tarih, saat)
                    break
            else:
                print("Hata")

    elif secim == "3":
        if not aktif:
            print("Once giris yapin")
        else:
            print("\nRandevulariniz:")
            for r in randevular:
                if r.hasta == aktif:
                    print(f"{r.randevu_id}-{r.doktor.ad} {r.tarih} {r.saat}")
            rid = int(input("Iptal ID: "))
            for r in randevular:
                if r.randevu_id == rid and r.hasta == aktif:
                    r.randevu_iptal()
                    break
            else:
                print("Hata")

    elif secim == "4":
        tarih = input("Tarih: ")
        Randevu.gunluk_randevu_goruntule(tarih)

    elif secim == "5":
        print("Cikis")
        break

    else:
        print("Gecersiz")












# Mukkemmel olan
# """
# ARAÇ PAYLAŞIM SİSTEMİ (CAR SHARING SYSTEM)
# Proje Geliştirme Adımlarına Uygun Tam Proje
# """

# import datetime
# from datetime import datetime as dt
# import time


# # ==================== 1. SINIFLAR ====================

# class Arac:
#     """Araç sınıfı - Araç özelliklerini ve metodlarını içerir"""

#     def __init__(self, arac_id, marka, model, kilometre, musait_mi=True):
#         self.arac_id = arac_id          # Araç ID'si (str veya int)
#         self.marka = marka              # Araç markası (str)
#         self.model = model              # Araç modeli (str)
#         self.kilometre = kilometre      # Araç kilometresi (float/int)
#         self.musait_mi = musait_mi      # Araç müsait mi? (bool)

#     def arac_durumu_guncelle(self, durum):
#         """
#         Aracın müsaitlik durumunu günceller
#         Parametre: durum (True/False)
#         """
#         self.musait_mi = durum
#         durum_str = "MÜSAİT" if durum else "KİRALANDI"
#         print(f"🚗 {self.marka} {self.model} aracının durumu: {durum_str}")

#     def kilometre_guncelle(self, yeni_kilometre):
#         """
#         Aracın kilometresini günceller
#         Parametre: yeni_kilometre (float/int)
#         """
#         eski_kilometre = self.kilometre
#         self.kilometre = yeni_kilometre
#         print(f"📊 Kilometre güncellendi: {eski_kilometre} km → {self.kilometre} km")

#     def arac_bilgisi_goster(self):
#         """Aracın tüm bilgilerini ekrana yazdırır"""
#         durum = "✅ MÜSAİT" if self.musait_mi else "❌ KİRALANDI"
#         print(f"  ID: {self.arac_id} | {self.marka} {self.model} | Km: {self.kilometre} | {durum}")


# class Kullanici:
#     """Kullanıcı sınıfı - Kullanıcı bilgilerini ve işlemlerini içerir"""

#     def __init__(self, kullanici_id, ad, ehliyet_no):
#         self.kullanici_id = kullanici_id      # Kullanıcı ID'si
#         self.ad = ad                          # Kullanıcı adı
#         self.ehliyet_no = ehliyet_no          # Ehliyet numarası
#         self.kiralama_listesi = []            # Kullanıcının kiralama geçmişi (List)

#     def kiralama_gecmisi(self, kiralama_sistemi=None):
#         """
#         Kullanıcının kiralama geçmişini gösterir
#         Parametre: kiralama_sistemi (Kiralama nesnelerinin listesi)
#         """
#         if not self.kiralama_listesi:
#             print(f"📝 {self.ad} henüz hiç araç kiralamamış.")
#             return

#         print(f"\n📋 {self.ad} - KİRALAMA GEÇMİŞİ")
#         print("-" * 50)
#         for kiralama_id in self.kiralama_listesi:
#             if kiralama_sistemi and kiralama_id in kiralama_sistemi:
#                 kiralama_sistemi[kiralama_id].kiralama_bilgisi()
#             else:
#                 print(f"  Kiralama ID: {kiralama_id}")

#     def bilgi_goster(self):
#         """Kullanıcı bilgilerini ekrana yazdırır"""
#         print(f"  👤 ID: {self.kullanici_id} | Ad: {self.ad} | Ehliyet: {self.ehliyet_no}")


# class Kiralama:
#     """Kiralama sınıfı - Kiralama işlemlerini yönetir"""

#     def __init__(self, kiralama_id, arac, kullanici, baslangic_saati=None):
#         self.kiralama_id = kiralama_id
#         self.arac = arac                      # Arac nesnesi
#         self.kullanici = kullanici            # Kullanici nesnesi
#         self.baslangic_saati = baslangic_saati or dt.now()
#         self.bitis_saati = None
#         self.ucret = 0
#         self._saatlik_ucret = 50  # TL/saat

#     def kiralama_baslat(self):
#         """
#         Kiralamayı başlatır - Aracı kullanıcıya tahsis eder
#         """
#         if not self.arac.musait_mi:
#             print(f"❌ {self.arac.marka} {self.arac.model} aracı zaten kiralanmış durumda!")
#             return False

#         # Aracı kiralandı olarak işaretle
#         self.arac.arac_durumu_guncelle(False)
#         self.baslangic_saati = dt.now()

#         # Kiralama ID'sini kullanıcının geçmişine ekle
#         self.kullanici.kiralama_listesi.append(self.kiralama_id)

#         print(f"\n✅ KİRALAMA BAŞLATILDI!")
#         print(f"   Kiralama ID: {self.kiralama_id}")
#         print(f"   Kullanıcı: {self.kullanici.ad}")
#         print(f"   Araç: {self.arac.marka} {self.arac.model}")
#         print(f"   Başlangıç: {self.baslangic_saati.strftime('%d/%m/%Y %H:%M:%S')}")
#         return True

#     def kiralama_bitir(self, yeni_kilometre):
#         """
#         Kiralamayı bitirir - Ücret hesaplar ve aracı tekrar müsait yapar
#         Parametre: yeni_kilometre (kiralama sonundaki kilometre)
#         """
#         if self.bitis_saati is not None:
#             print("❌ Bu kiralama zaten bitirilmiş!")
#             return False

#         self.bitis_saati = dt.now()

#         # Kiralama süresini hesapla (saat cinsinden)
#         sure = (self.bitis_saati - self.baslangic_saati).total_seconds() / 3600
#         self.ucret = round(sure * self._saatlik_ucret, 2)

#         # Kilometreyi güncelle
#         self.arac.kilometre_guncelle(yeni_kilometre)

#         # Aracı tekrar müsait yap
#         self.arac.arac_durumu_guncelle(True)

#         print(f"\n🏁 KİRALAMA BİTİRİLDİ!")
#         print(f"   Kiralama ID: {self.kiralama_id}")
#         print(f"   Bitiş: {self.bitis_saati.strftime('%d/%m/%Y %H:%M:%S')}")
#         print(f"   Kiralama süresi: {sure:.2f} saat")
#         print(f"   Toplam ücret: {self.ucret} TL")
#         return True

#     def kiralama_bilgisi(self):
#         """Kiralama bilgilerini ekrana yazdırır"""
#         print(f"\n📄 KİRALAMA #{self.kiralama_id}")
#         print(f"   👤 Kullanıcı: {self.kullanici.ad}")
#         print(f"   🚗 Araç: {self.arac.marka} {self.arac.model}")
#         print(f"   🕐 Başlangıç: {self.baslangic_saati.strftime('%d/%m/%Y %H:%M:%S')}")
#         if self.bitis_saati:
#             print(f"   🕒 Bitiş: {self.bitis_saati.strftime('%d/%m/%Y %H:%M:%S')}")
#             print(f"   💰 Ücret: {self.ucret} TL")
#         else:
#             print(f"   ⏳ Durum: Kiralama devam ediyor")


# # ==================== 2. SİSTEM SINIFI (Ana Sistem) ====================

# class AraçPaylaşımSistemi:
#     """Ana sistem sınıfı - Tüm işlemleri yönetir"""

#     def __init__(self):
#         # Veri yapıları: Dictionary kullanımı
#         self.araclar = {}          # {arac_id: Arac nesnesi}
#         self.kullanicilar = {}     # {kullanici_id: Kullanici nesnesi}
#         self.kiralamalar = {}      # {kiralama_id: Kiralama nesnesi}
#         self._sonraki_kiralama_id = 1

#         # Örnek verilerle sistemi başlat
#         self._ornek_veri_ekle()

#     def _ornek_veri_ekle(self):
#         """Sisteme örnek araç ve kullanıcı ekler"""
#         # Araçlar ekle
#         araclar_list = [
#             Arac(101, "Renault", "Clio", 24500, True),
#             Arac(102, "Fiat", "Egea", 18750, True),
#             Arac(103, "Volkswagen", "Polo", 31200, True),
#             Arac(104, "Hyundai", "i20", 9800, True),
#             Arac(105, "Toyota", "Corolla", 15600, True)
#         ]

#         for arac in araclar_list:
#             self.araclar[arac.arac_id] = arac

#         # Kullanıcılar ekle
#         kullanicilar_list = [
#             Kullanici(1, "Ahmet Yılmaz", "34A12345"),
#             Kullanici(2, "Ayşe Demir", "06B67890"),
#             Kullanici(3, "Mehmet Kaya", "35C11223")
#         ]

#         for kullanici in kullanicilar_list:
#             self.kullanicilar[kullanici.kullanici_id] = kullanici

#     def tum_aracları_goster(self):
#         """Tüm araçları listeler"""
#         print("\n" + "=" * 60)
#         print("🚗 TÜM ARAÇLAR")
#         print("=" * 60)
#         for arac in self.araclar.values():
#             arac.arac_bilgisi_goster()

#     def musait_aracları_goster(self):
#         """Müsait araçları listeler"""
#         print("\n" + "=" * 60)
#         print("✅ MÜSAİT ARAÇLAR")
#         print("=" * 60)
#         musaitler = [a for a in self.araclar.values() if a.musait_mi]
#         if musaitler:
#             for arac in musaitler:
#                 arac.arac_bilgisi_goster()
#         else:
#             print("   Şu anda müsait araç bulunmamaktadır!")

#     def tum_kullanicilari_goster(self):
#         """Tüm kullanıcıları listeler"""
#         print("\n" + "=" * 60)
#         print("👤 TÜM KULLANICILAR")
#         print("=" * 60)
#         for kullanici in self.kullanicilar.values():
#             kullanici.bilgi_goster()

#     def arac_kirala(self):
#         """Kullanıcıdan input alarak yeni kiralama oluşturur"""
#         print("\n" + "=" * 60)
#         print("🚗 YENİ ARAÇ KİRALAMA")
#         print("=" * 60)

#         # Önce müsait araçları göster
#         self.musait_aracları_goster()

#         # Araç seçimi
#         while True:
#             try:
#                 arac_id = int(input("\n🔢 Kiralanacak aracın ID'sini giriniz: "))
#                 if arac_id in self.araclar:
#                     arac = self.araclar[arac_id]
#                     if not arac.musait_mi:
#                         print("❌ Bu araç şu anda kiralanmış durumda!")
#                         continue
#                     break
#                 else:
#                     print(f"❌ {arac_id} ID'li araç bulunamadı!")
#             except ValueError:
#                 print("❌ Lütfen geçerli bir sayı giriniz!")

#         # Kullanıcı seçimi
#         self.tum_kullanicilari_goster()
#         while True:
#             try:
#                 kullanici_id = int(input("\n🔢 Kiralama yapacak kullanıcının ID'sini giriniz: "))
#                 if kullanici_id in self.kullanicilar:
#                     kullanici = self.kullanicilar[kullanici_id]
#                     break
#                 else:
#                     print(f"❌ {kullanici_id} ID'li kullanıcı bulunamadı!")
#             except ValueError:
#                 print("❌ Lütfen geçerli bir sayı giriniz!")

#         # Kiralama oluştur
#         kiralama = Kiralama(self._sonraki_kiralama_id, arac, kullanici)
#         self.kiralamalar[self._sonraki_kiralama_id] = kiralama

#         if kiralama.kiralama_baslat():
#             self._sonraki_kiralama_id += 1
#             return True
#         return False

#     def kiralama_bitir(self):
#         """Kullanıcıdan input alarak kiralamayı bitirir"""
#         print("\n" + "=" * 60)
#         print("🏁 KİRALAMA BİTİR")
#         print("=" * 60)

#         # Devam eden kiralamaları göster
#         devam_edenler = [k for k in self.kiralamalar.values() if k.bitis_saati is None]

#         if not devam_edenler:
#             print("📝 Devam eden kiralama bulunmamaktadır!")
#             return False

#         print("\n📋 Devam Eden Kiralamalar:")
#         for k in devam_edenler:
#             print(f"   ID: {k.kiralama_id} | {k.kullanici.ad} → {k.arac.marka} {k.arac.model}")

#         while True:
#             try:
#                 kiralama_id = int(input("\n🔢 Bitirilecek kiralama ID'sini giriniz: "))
#                 if kiralama_id in self.kiralamalar:
#                     kiralama = self.kiralamalar[kiralama_id]
#                     if kiralama.bitis_saati is not None:
#                         print("❌ Bu kiralama zaten bitirilmiş!")
#                         continue

#                     # Yeni kilometre bilgisi al
#                     while True:
#                         try:
#                             yeni_km = float(input(f"📊 Aracın güncel kilometresi ({kiralama.arac.kilometre} km → ?): "))
#                             if yeni_km >= kiralama.arac.kilometre:
#                                 kiralama.kiralama_bitir(yeni_km)
#                                 return True
#                             else:
#                                 print("❌ Yeni kilometre eski kilometreden küçük olamaz!")
#                         except ValueError:
#                             print("❌ Lütfen geçerli bir sayı giriniz!")
#                     break
#                 else:
#                     print(f"❌ {kiralama_id} ID'li kiralama bulunamadı!")
#             except ValueError:
#                 print("❌ Lütfen geçerli bir sayı giriniz!")
#         return False

#     def kiralama_gecmisi_goster(self):
#         """Kullanıcı seçerek kiralama geçmişini gösterir"""
#         print("\n" + "=" * 60)
#         print("📋 KİRALAMA GEÇMİŞİ")
#         print("=" * 60)

#         self.tum_kullanicilari_goster()

#         while True:
#             try:
#                 kullanici_id = int(input("\n🔢 Geçmişini görmek istediğiniz kullanıcının ID'sini giriniz: "))
#                 if kullanici_id in self.kullanicilar:
#                     kullanici = self.kullanicilar[kullanici_id]
#                     kullanici.kiralama_gecmisi(self.kiralamalar)
#                     break
#                 else:
#                     print(f"❌ {kullanici_id} ID'li kullanıcı bulunamadı!")
#             except ValueError:
#                 print("❌ Lütfen geçerli bir sayı giriniz!")

#     def tum_kiralamalari_goster(self):
#         """Tüm kiralama kayıtlarını gösterir"""
#         print("\n" + "=" * 60)
#         print("📋 TÜM KİRALAMA KAYITLARI")
#         print("=" * 60)

#         if not self.kiralamalar:
#             print("   Henüz hiç kiralama kaydı bulunmamaktadır!")
#         else:
#             for kiralama in self.kiralamalar.values():
#                 kiralama.kiralama_bilgisi()

#     def menu_goster(self):
#         """Ana menüyü gösterir"""
#         print("\n" + "=" * 60)
#         print("🚗 ARAÇ PAYLAŞIM SİSTEMİ")
#         print("=" * 60)
#         print("1️⃣  Tüm Araçları Listele")
#         print("2️⃣  Müsait Araçları Listele")
#         print("3️⃣  Tüm Kullanıcıları Listele")
#         print("4️⃣  Yeni Araç Kirala")
#         print("5️⃣  Kiralamayı Bitir")
#         print("6️⃣  Kiralama Geçmişi Göster (Kullanıcı Bazlı)")
#         print("7️⃣  Tüm Kiralama Kayıtlarını Göster")
#         print("8️⃣  Sistemden Çıkış")
#         print("-" * 60)

#     def calistir(self):
#         """Sistemin ana akışını çalıştırır"""
#         print("\n" + "🌟" * 30)
#         print("   ARAÇ PAYLAŞIM SİSTEMİNE HOŞ GELDİNİZ")
#         print("🌟" * 30)

#         while True:
#             self.menu_goster()

#             secim = input("\n👉 Lütfen bir seçenek giriniz (1-8): ")

#             if secim == "1":
#                 self.tum_aracları_goster()
#             elif secim == "2":
#                 self.musait_aracları_goster()
#             elif secim == "3":
#                 self.tum_kullanicilari_goster()
#             elif secim == "4":
#                 self.arac_kirala()
#             elif secim == "5":
#                 self.kiralama_bitir()
#             elif secim == "6":
#                 self.kiralama_gecmisi_goster()
#             elif secim == "7":
#                 self.tum_kiralamalari_goster()
#             elif secim == "8":
#                 print("\n👋 Sistemden çıkış yapılıyor... İyi günler dileriz!")
#                 break
#             else:
#                 print("❌ Geçersiz seçenek! Lütfen 1-8 arasında bir sayı giriniz.")

#             input("\n🔄 Devam etmek için Enter tuşuna basın...")


# # ==================== 3. PROGRAMIN BAŞLATILMASI ====================

# def main():
#     """Programın ana giriş noktası"""
#     sistem = AraçPaylaşımSistemi()
#     sistem.calistir()


# # Program çalıştırıldığında main() fonksiyonunu çağır
# if __name__ == "__main__":
#     main()





















# from datetime import datetime

# class Arac:
#   def __init__(self,arac_id,marka,model,kilometre,musait_mi):
#     self.arac_id = arac_id
#     self.marka = marka
#     self.model = model
#     self.kilometre = kilometre
#     self.musait_mi= musait_mi

#   def arac_durumu_guncelle(self,durum):
#     self.musait_mi = durum
#     if durum == False:
#         print("Arac kiralandi")
#     else:
#         print("Arac musait")

#   def kilometre_guncelle(self,yeni_km):
#     if yeni_km > self.kilometre:
#       self.kilometre = yeni_km





# class Kullanici:
#   def __init__(self,kullanici_id,ad,ehliyet_no):
#     self.kullanici_id = kullanici_id
#     self.ad = ad
#     self.ehliyet_no = ehliyet_no
#     self.kiralama_gecmisi_listesi = []

#   def kiralama_gecmisi(self):
#     return self.kiralama_gecmisi_listesi

#   def gecmis_ekle(self,kiralama):
#     self.kiralama_gecmisi_listesi.append(kiralama)




# class Kiralama:
#   def __init__(self,kiralama_id,arac,kullanici):
#       self.kiralama_id = kiralama_id
#       self.arac = arac
#       self.kullanici = kullanici
#       self.baslangic_saati = None
#       self.bitis_saati = None

#   def kiralama_baslat(self):
#     if self.arac.musait_mi:
#       self.baslangic_saati = datetime.now()
#       self.arac.arac_durumu_guncelle(False)
#       print("Kiralama basladi")
#     else:
#       print("Arac musati degil")


#   def kiralama_bitir(self,yeni_km):
#       self.bitis_saati = datetime.now()
#       self.arac.arac_durumu_guncelle(True)
#       self.arac.kilometre_guncelle(yeni_km)
#       self.kullanici.gecmis_ekle(self)
#       print("Kiralama bitti")

#   def kiralama_bilgisi(self):
#     return {
#       "Kiralama_id": self.kiralama_id,
#       "arac" : self.arac.marka + " " + self.arac.model,
#       "kullanici" : self.kullanici.ad,
#       "baslangic": self.baslangic_saati,
#       "bitis":  self.bitis_saati}


# # Veri tabani

# araclar = []
# kullanicilar = []
# kiralamalar = []

# araclar.append (Arac (1,"BMW","X7",80000,True))
# araclar.append (Arac (2,"Skoda","octavia",120000,True))




# # Kullanici Input
# def kullanici_olustur():
#   print("\n --- Kullanici Kayit ---")
#   ad = str(input("Adiniz giriniz"))
#   ehliyet = input("Ehliyet No: ")

#   kullanici_id = len(kullanicilar) + 1
#   kullanici = Kullanici(kullanici_id,ad,ehliyet)

#   kullanicilar.append(kullanici)
#   print("Kullanici Olusturuldu!")

#   return kullanici
# kullanici1 = kullanici_olustur()

# #Ana menu
# def menu():
#   print("\n =====Arac Kiralama Sistemi")
#   print("1 - Araclari listele ")
#   print("2 - Kiralama baslat")
#   print ("3 - kiralama bitir")
#   print ("4 - Kullanici Gecmisi")
#   print(" 5 - Cikis")

#   # Sistem Fonksiyonlari
# def araclari_listele():
#   for i in araclar:
#     durum = "Musait" if i.musait_mi else "Dolu"
#     print(f"{i.arac_id} - {i.marka} {i.model} | Km: {i.kilometre} | {durum} ")


# def kiralama_baslat():
#   arac_id = int(input("Arac ID: "))
#   arac = next((i for i in araclar if i.arac_id == arac_id), None)

#   kullanici_id = int(input("Kullanici ID: "))
#   kullanici = next((k for k in kullanicilar if k.kullanici_id == kullanici_id), None)

#   if not arac:
#     print("Arac bulunamadi")
#     return
#   if not kullanici:
#     print(" Kullanici bulunamadi")
#     return

#   kiralama = Kiralama(len(kiralamalar)+1,arac, kullanici)
#   kiralamalar.append(kiralama)
#   kiralama.kiralama_baslat()
#   print(f"Kiralama ID: {kiralama.kiralama_id}")


# def kiralama_bitir():
#   kiralama_id = int (input("Kiralama ID: "))
#   yeni_km = int (input("yeni KM: "))

#   kiralama = next ((k for k in kiralamalar if k.kiralama_id == kiralama_id), None)

#   if kiralama:
#     kiralama.kiralama_bitir(yeni_km)
#   else:
#     print("Kiralama bulunamadi")


# def kullanici_gecmisi():
#   kullanici_id = int(input("Kullanici ID: "))
#   kullanici = next((k for k in kullanicilar if k.kullanici_id == kullanici_id),None)
#   if not kullanici:
#     print("kullanici bulunamadi")
#     return
#   for k in kullanici.kiralama_gecmisi():
#     print(k.kiralama_bilgisi())

#     #Program Akisi

# while True:
#   menu()
#   secim = input("secim yap: ")

#   if secim == "1":
#     araclari_listele()
#   elif secim == "2":
#     kiralama_baslat()
#   elif secim == "3":
#     kiralama_bitir()
#   elif secim == "4":
#     kullanici_gecmisi()
#   elif secim == "5":
#     print("Cikis yapiliyor...")
#     break
#   else:
#     print("Gecersiz secim")






#2 second formule -----------------------------------

# from datetime import datetime

# # ----------------- SINIFLAR -----------------

# class Arac:
#     def __init__(self, arac_id, marka, model, kilometre):
#         self.arac_id = arac_id
#         self.marka = marka
#         self.model = model
#         self.kilometre = kilometre
#         self.musait_mi = True

#     def arac_durumu_guncelle(self, durum):
#         self.musait_mi = durum

#     def kilometre_guncelle(self, yeni_km):
#         if yeni_km > self.kilometre:
#             self.kilometre = yeni_km


# class Kullanici:
#     def __init__(self, kullanici_id, ad, ehliyet_no):
#         self.kullanici_id = kullanici_id
#         self.ad = ad
#         self.ehliyet_no = ehliyet_no
#         self.kiralama_gecmisi = []

#     def kiralama_ekle(self, kiralama):
#         self.kiralama_gecmisi.append(kiralama)

#     def gecmisi_goster(self):
#         print(f"\n--- {self.ad} Kiralama Geçmişi ---")
#         if not self.kiralama_gecmisi:
#             print("Geçmiş yok")
#         else:
#             for k in self.kiralama_gecmisi:
#                 print(k.kiralama_bilgisi())


# class Kiralama:
#     def __init__(self, kiralama_id, arac, kullanici):
#         self.kiralama_id = kiralama_id
#         self.arac = arac
#         self.kullanici = kullanici
#         self.baslangic_saati = None
#         self.bitis_saati = None

#     def kiralama_baslat(self):
#         if self.arac.musait_mi:
#             self.baslangic_saati = datetime.now()
#             self.arac.arac_durumu_guncelle(False)
#             print(f"✅ Kiralama başladı | Kullanıcı: {self.kullanici.ad} | Araç: {self.arac.marka}")
#         else:
#             print("❌ Araç müsait değil")

#     def kiralama_bitir(self, yeni_km):
#         self.bitis_saati = datetime.now()
#         self.arac.arac_durumu_guncelle(True)
#         self.arac.kilometre_guncelle(yeni_km)
#         print(f"🏁 Kiralama bitti | Araç: {self.arac.marka}")

#     def kiralama_bilgisi(self):
#         return {
#             "Kiralama ID": self.kiralama_id,
#             "Araç": self.arac.marka + " " + self.arac.model,
#             "Kullanıcı": self.kullanici.ad,
#             "Başlangıç": self.baslangic_saati,
#             "Bitiş": self.bitis_saati
#         }


# # ----------------- VERİLER -----------------

# araclar = [
#     Arac(1, "BMW", "X7", 80000),
#     Arac(2, "Skoda", "Octavia", 120000)
# ]

# kullanicilar = []
# kiralamalar = []

# son_kullanici_id = 0
# son_kiralama_id = 0


# # ----------------- FONKSİYONLAR -----------------

# def kullanici_olustur():
#     global son_kullanici_id

#     print("\n--- Kullanıcı Kayıt ---")
#     ad = input("Ad: ")
#     ehliyet = input("Ehliyet No: ")

#     son_kullanici_id += 1
#     kullanici = Kullanici(son_kullanici_id, ad, ehliyet)
#     kullanicilar.append(kullanici)

#     print(f"✅ Kullanıcı oluşturuldu | ID: {son_kullanici_id}")
#     return kullanici


# def araclari_listele():
#     print("\n--- Araçlar ---")
#     for a in araclar:
#         durum = "Müsait" if a.musait_mi else "Dolu"
#         print(f"{a.arac_id} - {a.marka} {a.model} | {a.kilometre} km | {durum}")


# def kiralama_baslat():
#     global son_kiralama_id

#     print("\n--- MEVCUT ARAÇLAR ---")
#     for a in araclar:
#         durum = "Müsait" if a.musait_mi else "Dolu"
#         print(f"{a.arac_id} - {a.marka} {a.model} | {a.kilometre} km | {durum}")

#     kullanici_id = int(input("\nKullanıcı ID: "))
#     arac_id = int(input("Araç ID: "))

#     kullanici = next((k for k in kullanicilar if k.kullanici_id == kullanici_id), None)
#     arac = next((a for a in araclar if a.arac_id == arac_id), None)

#     if not kullanici:
#         print("❌ Kullanıcı yok")
#         return
#     if not arac:
#         print("❌ Araç yok")
#         return

#     if not arac.musait_mi:
#         print("❌ Bu araç şu an kirada")
#         return

#     son_kiralama_id += 1
#     kiralama = Kiralama(son_kiralama_id, arac, kullanici)
#     kiralamalar.append(kiralama)

#     kiralama.kiralama_baslat()
#     print(f"📌 Kiralama ID: {son_kiralama_id}")


# def kiralama_bitir():
#     kiralama_id = int(input("Kiralama ID: "))
#     yeni_km = int(input("Yeni KM: "))

#     kiralama = next((k for k in kiralamalar if k.kiralama_id == kiralama_id), None)

#     if kiralama:
#         kiralama.kiralama_bitir(yeni_km)
#         kiralama.kullanici.kiralama_ekle(kiralama)
#     else:
#         print("❌ Kiralama bulunamadı")


# def kullanici_gecmisi():
#     print("\n===== TÜM KULLANICI GEÇMİŞİ =====")

#     if len(kullanicilar) == 0:
#         print("Hiç kullanıcı yok")
#         return

#     for kullanici in kullanicilar:
#         print(f"\n👤 Kullanıcı: {kullanici.ad} (ID: {kullanici.kullanici_id})")

#         if len(kullanici.kiralama_gecmisi) == 0:
#             print("  📭 Kiralama yok")
#         else:
#             for k in kullanici.kiralama_gecmisi:
#                 print("  ", k.kiralama_bilgisi())


# # ----------------- MENÜ -----------------

# def menu():
#     print("\n===== ARAÇ KİRALAMA SİSTEMİ =====")
#     print("1 - Kullanıcı Oluştur")
#     print("2 - Araçları Listele")
#     print("3 - Kiralama Başlat")
#     print("4 - Kiralama Bitir")
#     print("5 - Kullanıcı Geçmişi")
#     print("6 - Çıkış")


# # ----------------- PROGRAM -----------------

# while True:
#     menu()
#     secim = input("Seçim: ")

#     if secim == "1":
#         kullanici_olustur()
#     elif secim == "2":
#         araclari_listele()
#     elif secim == "3":
#         kiralama_baslat()
#     elif secim == "4":
#         kiralama_bitir()
#     elif secim == "5":
#         kullanici_gecmisi()
#     elif secim == "6":
#         print("Çıkış yapılıyor...")
#         break
#     else:
#         print("Geçersiz seçim")