class Musteri:
    def __init__(self, musteri_id, ad, soyad, telefon):
        self.musteri_id = musteri_id
        self.ad = ad
        self.soyad = soyad
        self.telefon = telefon


class Satis:
    def __init__(self, satis_id, musteri_id, urun, fiyat):
        self.satis_id = satis_id
        self.musteri_id = musteri_id
        self.urun = urun
        self.fiyat = fiyat


class DestekTalebi:
    def __init__(self, talep_id, musteri_id, aciklama):
        self.talep_id = talep_id
        self.musteri_id = musteri_id
        self.aciklama = aciklama


class CRM:
    def __init__(self):
        self.musteriler = {}
        self.satislar = {}
        self.destek_talepleri = []

        # AUTO ID counters
        self.musteri_id_counter = 1
        self.satis_id_counter = 1
        self.talep_id_counter = 1

    # -------- MÜŞTERİ --------
    def musteri_ekle(self):
        ad = input("Ad: ")
        soyad = input("Soyad: ")
        telefon = input("Telefon: ")

        musteri_id = self.musteri_id_counter
        self.musteri_id_counter += 1

        self.musteriler[musteri_id] = Musteri(musteri_id, ad, soyad, telefon)
        print(f"Müşteri eklendi (ID: {musteri_id}{ad})")

    def musteri_sil(self):
        musteri_id = int(input("Müşteri ID: "))

        if musteri_id in self.musteriler:
            del self.musteriler[musteri_id]
            print("Müşteri silindi")
        else:
            print("Müşteri bulunamadı")

    def musterileri_goster(self):
        if not self.musteriler:
            print("Müşteri yok")
            return

        for m in self.musteriler.values():
            print(f"{m.musteri_id} - {m.ad} {m.soyad} - {m.telefon}")

    # -------- SATIŞ --------
    def satis_ekle(self):
        musteri_id = int(input("Müşteri ID: "))

        if musteri_id not in self.musteriler:
            print("Müşteri bulunamadı!")
            return

        urun = input("Ürün: ")
        fiyat = float(input("Fiyat: "))

        satis_id = self.satis_id_counter
        self.satis_id_counter += 1

        self.satislar[satis_id] = Satis(satis_id, musteri_id, urun, fiyat)
        print(f"Satış eklendi (ID: {satis_id})")

    def satis_bul(self):
        satis_id = int(input("Satış ID: "))

        if satis_id in self.satislar:
            s = self.satislar[satis_id]
            print(f"{s.satis_id} - Musteri {s.musteri_id} - {s.urun} - {s.fiyat} TL")
        else:
            print("Satış bulunamadı")

    def satis_sil(self):
        satis_id = int(input("Satış ID: "))

        if satis_id in self.satislar:
            del self.satislar[satis_id]
            print("Satış silindi")
        else:
            print("Satış bulunamadı")

    def satislari_goster(self):
        if not self.satislar:
            print("Satış yok")
            return

        for s in self.satislar.values():
            print(f"{s.satis_id} - Musteri {s.musteri_id} - {s.urun} - {s.fiyat}")

    # -------- DESTEK --------
    def destek_olustur(self):
        musteri_id = int(input("Müşteri ID: "))
        if musteri_id not in self.musteriler:
          print("Hatali Musteri ID si.")
          return
        aciklama = input("Açıklama: ")

        talep_id = self.talep_id_counter
        self.talep_id_counter += 1

        self.destek_talepleri.append(DestekTalebi(talep_id, musteri_id, aciklama))
        print(f"Destek talebi oluşturuldu (ID: {talep_id})")

    def destek_bul(self):
      talep_id = int(input("Talep ID: "))

      for d in self.destek_talepleri:
          if d.talep_id == talep_id:

            musteri = self.musteriler.get(d.musteri_id)

            if musteri:
                print(f"{d.talep_id} - {musteri.ad} {musteri.soyad} - {d.aciklama}")
            else:
                print(f"{d.talep_id} - Musteri bulunamadi - {d.aciklama}")

            return

    print("Talep bulunamadı")


# -------- MENU --------
crm = CRM()

while True:
    print("\n===== CRM SYSTEM =====")
    print("1- Müşteri Ekle")
    print("2- Müşteri Sil")
    print("3- Müşterileri Göster")
    print("4- Satış Ekle")
    print("5- Satış Bul")
    print("6- Satış Sil")
    print("7- Satışları Göster")
    print("8- Destek Oluştur")
    print("9- Destek Bul")
    print("0- Çıkış")

    secim = input("Seçim: ")

    if secim == "1":
        crm.musteri_ekle()

    elif secim == "2":
        crm.musteri_sil()

    elif secim == "3":
        crm.musterileri_goster()

    elif secim == "4":
        crm.satis_ekle()

    elif secim == "5":
        crm.satis_bul()

    elif secim == "6":
        crm.satis_sil()

    elif secim == "7":
        crm.satislari_goster()

    elif secim == "8":
        crm.destek_olustur()

    elif secim == "9":
        crm.destek_bul()

    elif secim == "0":
        print("Çıkış yapılıyor...")
        break

    else:
        print("Hatalı seçim")