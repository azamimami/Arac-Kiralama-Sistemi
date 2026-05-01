from datetime import datetime

# =========================
# YARDIMCI FONKSİYON
# =========================

def int_input(mesaj):
    while True:
        try:
            return int(input(mesaj))
        except ValueError:
            print("⚠ Sayı giriniz")


def bos_mu(x):
    return x.strip() == ""


# =========================
# SINIFLAR
# =========================

class Arac:
    sayac = 1

    def __init__(self, marka, model, kilometre):
        self.arac_id = Arac.sayac
        Arac.sayac += 1
        self.marka = marka
        self.model = model
        self.kilometre = kilometre
        self.musait_mi = True

    def __str__(self):
        return f"{self.arac_id} | {self.marka} {self.model} | KM:{self.kilometre} | Müsait:{self.musait_mi}"


class Kullanici:
    sayac = 1

    def __init__(self, ad, soyad, ehliyet_no):
        self.kullanici_id = Kullanici.sayac
        Kullanici.sayac += 1
        self.ad = ad
        self.soyad = soyad
        self.ehliyet_no = ehliyet_no
        self.gecmis = []

    def __str__(self):
        return f"{self.kullanici_id} | {self.ad} {self.soyad}"


class Kiralama:
    def __init__(self, kiralama_id, arac, kullanici):
        self.kiralama_id = kiralama_id
        self.arac = arac
        self.kullanici = kullanici
        self.baslangic = None
        self.bitis = None
        self.baslangic_km = None
        self.bitis_km = None

    def kiralama_baslat(self):
        if not self.arac.musait_mi:
            print("✖ Araç müsait değil")
            return False

        self.arac.musait_mi = False
        self.baslangic = datetime.now()
        self.baslangic_km = self.arac.kilometre

        self.kullanici.gecmis.append(self)

        print("✔ Kiralama başladı")
        return True

    def kiralama_bitir(self, yeni_km):
        if self.bitis is not None:
            print("✖ Bu kiralama zaten bitmiş")
            return

        self.bitis = datetime.now()
        self.bitis_km = yeni_km

        # Araç KM güncelleme (direkt yeni km)
        self.arac.kilometre = yeni_km
        self.arac.musait_mi = True

        print("✔ Kiralama bitti")


# =========================
# VERİLER
# =========================

araclar = []
kullanicilar = []
kiralamalar = []


# =========================
# MENÜ
# =========================

def menu():
    while True:
        print("""
=========================
 ARAÇ KİRALAMA SİSTEMİ
=========================
1- Araç ekle
2- Araç sil
3- Kullanıcı ekle
4- Araç listele
5- Kullanıcı listele
6- Kiralama başlat
7- Kiralama bitir
8- Kiralama geçmişi
0- Çıkış
""")

        secim = int_input("Seçim: ")

        # ---- ARAÇ EKLE ----
        if secim == 1:
            marka = input("Marka: ")
            model = input("Model: ")
            km = int_input("KM: ")
            araclar.append(Arac(marka, model, km))
            print("✔ Araç eklendi")

        # ---- ARAÇ SİL ----
        elif secim == 2:
            if not araclar:
                print("Araç yok")
                continue

            for a in araclar:
                print(a)

            aid = int_input("Silinecek Araç ID: ")

            arac = next((a for a in araclar if a.arac_id == aid), None)

            if not arac:
                print("✖ Araç bulunamadı")
                continue

            if not arac.musait_mi:
                print("✖ Araç kirada, silinemez")
                continue

            araclar.remove(arac)
            print("✔ Araç silindi")

        # ---- KULLANICI EKLE ----
        elif secim == 3:
            ad = input("Ad: ")
            soyad = input("Soyad: ")
            eh = input("Ehliyet No: ")
            kullanicilar.append(Kullanici(ad, soyad, eh))
            print("✔ Kullanıcı eklendi")

        # ---- LİSTELE ----
        elif secim == 4:
            for a in araclar:
                print(a)

        elif secim == 5:
            for k in kullanicilar:
                print(k)

        # ---- KİRALAMA BAŞLAT ----
        elif secim == 6:
            if not araclar or not kullanicilar:
                print("✖ Eksik veri")
                continue

            for a in araclar:
                print(a)
            for k in kullanicilar:
                print(k)

            aid = int_input("Araç ID: ")
            kid = int_input("Kullanıcı ID: ")

            arac = next((a for a in araclar if a.arac_id == aid), None)
            kul = next((k for k in kullanicilar if k.kullanici_id == kid), None)

            if arac and kul:
                kiralama = Kiralama(len(kiralamalar)+1, arac, kul)

                if kiralama.kiralama_baslat():
                    kiralamalar.append(kiralama)
            else:
                print("✖ Hatalı seçim")

        # ---- KİRALAMA BİTİR ----
        elif secim == 7:
            aktif = [k for k in kiralamalar if k.bitis is None]

            if not aktif:
                print("Aktif kiralama yok")
                continue

            for k in aktif:
                print(f"{k.kiralama_id} | {k.arac.marka} | {k.kullanici.ad}")

            kid = int_input("Kiralama ID: ")

            k = next((x for x in kiralamalar if x.kiralama_id == kid), None)

            if k:
                yeni_km = int_input("Araç son KM: ")
                k.kiralama_bitir(yeni_km)
            else:
                print("✖ Bulunamadı")

        # ---- GEÇMİŞ ----
        elif secim == 8:
            if not kiralamalar:
                print("Geçmiş yok")
            else:
                for k in kiralamalar:
                    durum = "Devam ediyor" if k.bitis is None else "Bitti"

                    kullanilan_km = 0
                    if k.bitis_km is not None:
                        kullanilan_km = k.bitis_km - k.baslangic_km

                    print(f"""
ID: {k.kiralama_id}
Araç: {k.arac.marka} {k.arac.model}
Kullanıcı: {k.kullanici.ad} {k.kullanici.soyad}
Başlangıç KM: {k.baslangic_km}
Bitiş KM: {k.bitis_km}
Kullanılan KM: {kullanilan_km}
Durum: {durum}
""")

        elif secim == 0:
            break


menu()