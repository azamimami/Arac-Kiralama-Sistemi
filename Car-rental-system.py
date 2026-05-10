

import sys
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QDialog, QLabel,
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QMessageBox,
    QTabWidget, QFrame, QTextEdit, QDateEdit
)
from PyQt5.QtCore import Qt, QTimer, QDate
from PyQt5.QtGui import QFont, QColor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# ============ YARDIMCI FONKSİYONLAR ==========

def email_gecerli_mi(email):
    """Email doğrulama"""
    return "@" in email and "." in email


def telefon_gecerli_mi(telefon):
    """Telefon numarası doğrulama (10 haneli)"""
    return telefon.isdigit() and len(telefon) >= 10


# ============ SINIFLAR ==========

class Arac:
    """Araç sınıfı - Kiralama sistemi için araç verileri"""
    sayac = 1

    def __init__(self, marka, model, kilometre, yil, plaka):
        """
        Args:
            marka (str): Araç markası
            model (str): Araç modeli
            kilometre (int): Araç kilometre bilgisi
            yil (int): Araç üretim yılı
            plaka (str): Araç plakası
        """
        self.arac_id = Arac.sayac
        Arac.sayac += 1
        self.marka = marka
        self.model = model
        self.kilometre = kilometre
        self.yil = yil
        self.plaka = plaka
        self.musait_mi = True
        self.olusturulma_tarihi = datetime.now()

    def __str__(self):
        durum = "✓ Müsait" if self.musait_mi else "✗ Kirada"
        return f"[{self.arac_id}] {self.marka} {self.model} ({self.yil}) | KM: {self.kilometre} | Plaka: {self.plaka} | {durum}"

    def bilgi_al(self):
        """Araç bilgilerini detaylı olarak döndür"""
        return {
            "id": self.arac_id,
            "marka": self.marka,
            "model": self.model,
            "kilometre": self.kilometre,
            "yil": self.yil,
            "plaka": self.plaka,
            "musait": self.musait_mi,
            "durum": "✓ Müsait" if self.musait_mi else "✗ Kirada"
        }


class Kullanici:
    """Kullanıcı sınıfı - Kiralayan müşteri verileri"""
    sayac = 1

    def __init__(self, ad, soyad, ehliyet_no, telefon, email):
        """
        Args:
            ad (str): Adı
            soyad (str): Soyadı
            ehliyet_no (str): Ehliyet numarası
            telefon (str): Telefon numarası
            email (str): Email adresi
        """
        self.kullanici_id = Kullanici.sayac
        Kullanici.sayac += 1
        self.ad = ad
        self.soyad = soyad
        self.ehliyet_no = ehliyet_no
        self.telefon = telefon
        self.email = email
        self.gecmis = []
        self.olusturulma_tarihi = datetime.now()

    def __str__(self):
        return f"[{self.kullanici_id}] {self.ad} {self.soyad} | {self.telefon}"

    def bilgi_al(self):
        """Kullanıcı bilgilerini detaylı olarak döndür"""
        return {
            "id": self.kullanici_id,
            "ad": self.ad,
            "soyad": self.soyad,
            "ehliyet": self.ehliyet_no,
            "telefon": self.telefon,
            "email": self.email,
            "kiralama_sayisi": len(self.gecmis)
        }

    def toplam_kilometre(self):
        """Kullanıcının toplam kullanılan kilometre"""
        toplam = 0
        for kiralama in self.gecmis:
            if kiralama.bitis_km and kiralama.baslangic_km:
                toplam += kiralama.bitis_km - kiralama.baslangic_km
        return toplam


class Kiralama:
    """Kiralama sınıfı - Kiralama işlemleri"""
    sayac = 1

    def __init__(self, arac, kullanici, gunluk_fiyat):
        """
        Args:
            arac (Arac): Kiralanacak araç
            kullanici (Kullanici): Kiralayan kullanıcı
            gunluk_fiyat (float): Günlük kiralama fiyatı
        """
        self.kiralama_id = Kiralama.sayac
        Kiralama.sayac += 1
        self.arac = arac
        self.kullanici = kullanici
        self.gunluk_fiyat = gunluk_fiyat
        self.baslangic = None
        self.bitis = None
        self.baslangic_km = None
        self.bitis_km = None
        self.durum = "Bekleme"

    def kiralama_baslat(self):
        """Kiralama işlemini başlat"""
        if not self.arac.musait_mi:
            return False, "✖ Araç müsait değil"

        self.arac.musait_mi = False
        self.baslangic = datetime.now()
        self.baslangic_km = self.arac.kilometre
        self.durum = "Devam ediyor"

        self.kullanici.gecmis.append(self)

        return True, "✔ Kiralama başladı"

    def kiralama_bitir(self, yeni_km):
        """Kiralama işlemini bitir"""
        if self.bitis is not None:
            return False, "✖ Bu kiralama zaten bitmiş"

        if yeni_km < self.baslangic_km:
            return False, "✖ Bitiş KM, başlangıç KM'den düşük olamaz"

        self.bitis = datetime.now()
        self.bitis_km = yeni_km
        self.arac.kilometre = yeni_km
        self.arac.musait_mi = True
        self.durum = "Tamamlandı"

        return True, "✔ Kiralama bitti"

    def kira_hesapla(self):
        """Kiralama ücretini hesapla"""
        if self.bitis is None:
            return 0

        gun_farki = (self.bitis - self.baslangic).days
        if gun_farki == 0:
            gun_farki = 1

        return gun_farki * self.gunluk_fiyat

    def __str__(self):
        durum = "Devam ediyor" if self.bitis is None else "Tamamlandı"
        kullanilan_km = 0

        if self.bitis_km is not None and self.baslangic_km is not None:
            kullanilan_km = self.bitis_km - self.baslangic_km

        return f"[{self.kiralama_id}] {self.arac.marka} {self.arac.model} -> {self.kullanici.ad} | KM: {kullanilan_km} | {durum}"


# ============ DIALOG PENCERELERİ ==========

class AracEkleDialog(QDialog):
    """Araç ekleme diyaloğu"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🚗 Araç Ekle")
        self.setGeometry(100, 100, 400, 500)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.init_ui()
        self.result = None

    def init_ui(self):
        layout = QVBoxLayout()

        # Marka
        marka_label = QLabel("Marka:")
        marka_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.marka_input = QLineEdit()
        self.marka_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Model
        model_label = QLabel("Model:")
        model_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.model_input = QLineEdit()
        self.model_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Yıl
        yil_label = QLabel("Üretim Yılı:")
        yil_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.yil_input = QSpinBox()
        self.yil_input.setMinimum(1990)
        self.yil_input.setMaximum(datetime.now().year)
        self.yil_input.setValue(datetime.now().year)
        self.yil_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # KM
        km_label = QLabel("Kilometre:")
        km_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.km_input = QSpinBox()
        self.km_input.setMaximum(1000000)
        self.km_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Plaka
        plaka_label = QLabel("Plaka:")
        plaka_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.plaka_input = QLineEdit()
        self.plaka_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Butonlar
        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("✓ Ekle")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        ekle_btn.clicked.connect(self.ekle)

        iptal_btn = QPushButton("✕ İptal")
        iptal_btn.setStyleSheet("background-color: #9E9E9E; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(iptal_btn)

        layout.addWidget(marka_label)
        layout.addWidget(self.marka_input)
        layout.addWidget(model_label)
        layout.addWidget(self.model_input)
        layout.addWidget(yil_label)
        layout.addWidget(self.yil_input)
        layout.addWidget(km_label)
        layout.addWidget(self.km_input)
        layout.addWidget(plaka_label)
        layout.addWidget(self.plaka_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def ekle(self):
        if (self.marka_input.text().strip() and
            self.model_input.text().strip() and
            self.plaka_input.text().strip()):
            self.result = (
                self.marka_input.text().strip(),
                self.model_input.text().strip(),
                self.yil_input.value(),
                self.km_input.value(),
                self.plaka_input.text().strip()
            )
            self.accept()
        else:
            QMessageBox.warning(self, "Hata", "Tüm alanları doldurun!")


class KullaniciEkleDialog(QDialog):
    """Kullanıcı ekleme diyaloğu"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("👤 Kullanıcı Ekle")
        self.setGeometry(100, 100, 400, 500)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.init_ui()
        self.result = None

    def init_ui(self):
        layout = QVBoxLayout()

        # Ad
        ad_label = QLabel("Ad:")
        ad_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.ad_input = QLineEdit()
        self.ad_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Soyad
        soyad_label = QLabel("Soyad:")
        soyad_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.soyad_input = QLineEdit()
        self.soyad_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Ehliyet
        eh_label = QLabel("Ehliyet No:")
        eh_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.eh_input = QLineEdit()
        self.eh_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Telefon
        tel_label = QLabel("Telefon:")
        tel_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.tel_input = QLineEdit()
        self.tel_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Email
        email_label = QLabel("Email:")
        email_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.email_input = QLineEdit()
        self.email_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Butonlar
        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("✓ Ekle")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        ekle_btn.clicked.connect(self.ekle)

        iptal_btn = QPushButton("✕ İptal")
        iptal_btn.setStyleSheet("background-color: #9E9E9E; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(iptal_btn)

        layout.addWidget(ad_label)
        layout.addWidget(self.ad_input)
        layout.addWidget(soyad_label)
        layout.addWidget(self.soyad_input)
        layout.addWidget(eh_label)
        layout.addWidget(self.eh_input)
        layout.addWidget(tel_label)
        layout.addWidget(self.tel_input)
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def ekle(self):
        if (self.ad_input.text().strip() and
            self.soyad_input.text().strip() and
            self.eh_input.text().strip() and
            self.tel_input.text().strip() and
            self.email_input.text().strip()):

            if not telefon_gecerli_mi(self.tel_input.text()):
                QMessageBox.warning(self, "Hata", "Geçerli telefon numarası giriniz!")
                return

            if not email_gecerli_mi(self.email_input.text()):
                QMessageBox.warning(self, "Hata", "Geçerli email giriniz!")
                return

            self.result = (
                self.ad_input.text().strip(),
                self.soyad_input.text().strip(),
                self.eh_input.text().strip(),
                self.tel_input.text().strip(),
                self.email_input.text().strip()
            )
            self.accept()
        else:
            QMessageBox.warning(self, "Hata", "Tüm alanları doldurun!")


class KiralamaBaslatDialog(QDialog):
    """Kiralama başlatma diyaloğu"""

    def __init__(self, araclar, kullanicilar, parent=None):
        super().__init__(parent)
        self.araclar = araclar
        self.kullanicilar = kullanicilar
        self.setWindowTitle("🔑 Kiralama Başlat")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.init_ui()
        self.result = None

    def init_ui(self):
        layout = QVBoxLayout()

        # Araç seçimi
        arac_label = QLabel("Araç:")
        arac_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.arac_combo = QComboBox()
        self.arac_combo.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        for arac in self.araclar:
            if arac.musait_mi:
                self.arac_combo.addItem(f"{arac.marka} {arac.model} ({arac.yil})", arac.arac_id)

        if self.arac_combo.count() == 0:
            self.arac_combo.addItem("Müsait araç yok", None)

        # Kullanıcı seçimi
        kul_label = QLabel("Kullanıcı:")
        kul_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.kul_combo = QComboBox()
        self.kul_combo.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        for kul in self.kullanicilar:
            self.kul_combo.addItem(f"{kul.ad} {kul.soyad}", kul.kullanici_id)

        if self.kul_combo.count() == 0:
            self.kul_combo.addItem("Kullanıcı yok", None)

        # Fiyat
        fiyat_label = QLabel("Günlük Fiyat (TL):")
        fiyat_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.fiyat_input = QDoubleSpinBox()
        self.fiyat_input.setMaximum(10000)
        self.fiyat_input.setValue(100)
        self.fiyat_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Butonlar
        button_layout = QHBoxLayout()
        baslat_btn = QPushButton("✓ Başlat")
        baslat_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        baslat_btn.clicked.connect(self.baslat)

        iptal_btn = QPushButton("✕ İptal")
        iptal_btn.setStyleSheet("background-color: #9E9E9E; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(baslat_btn)
        button_layout.addWidget(iptal_btn)

        layout.addWidget(arac_label)
        layout.addWidget(self.arac_combo)
        layout.addWidget(kul_label)
        layout.addWidget(self.kul_combo)
        layout.addWidget(fiyat_label)
        layout.addWidget(self.fiyat_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def baslat(self):
        arac_id = self.arac_combo.currentData()
        kul_id = self.kul_combo.currentData()

        if arac_id and kul_id and self.fiyat_input.value() > 0:
            self.result = (arac_id, kul_id, self.fiyat_input.value())
            self.accept()
        else:
            QMessageBox.warning(self, "Hata", "Geçerli seçim yapınız!")


class KiralamaBitirDialog(QDialog):
    """Kiralama bitirme diyaloğu"""

    def __init__(self, kiralamalar, parent=None):
        super().__init__(parent)
        self.kiralamalar = [k for k in kiralamalar if k.bitis is None]
        self.setWindowTitle("🔓 Kiralama Bitir")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.init_ui()
        self.result = None

    def init_ui(self):
        layout = QVBoxLayout()

        # Kiralama seçimi
        kir_label = QLabel("Aktif Kiralama:")
        kir_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.kir_combo = QComboBox()
        self.kir_combo.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        for kir in self.kiralamalar:
            self.kir_combo.addItem(
                f"{kir.arac.marka} {kir.arac.model} -> {kir.kullanici.ad}",
                kir.kiralama_id
            )

        if self.kir_combo.count() == 0:
            self.kir_combo.addItem("Aktif kiralama yok", None)

        # Son KM
        km_label = QLabel("Araç Son Kilometre:")
        km_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.km_input = QSpinBox()
        self.km_input.setMaximum(1000000)
        self.km_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 4px;")

        # Butonlar
        button_layout = QHBoxLayout()
        bitir_btn = QPushButton("✓ Bitir")
        bitir_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        bitir_btn.clicked.connect(self.bitir)

        iptal_btn = QPushButton("✕ İptal")
        iptal_btn.setStyleSheet("background-color: #9E9E9E; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(bitir_btn)
        button_layout.addWidget(iptal_btn)

        layout.addWidget(kir_label)
        layout.addWidget(self.kir_combo)
        layout.addWidget(km_label)
        layout.addWidget(self.km_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def bitir(self):
        kir_id = self.kir_combo.currentData()

        if kir_id and self.km_input.value() > 0:
            self.result = (kir_id, self.km_input.value())
            self.accept()
        else:
            QMessageBox.warning(self, "Hata", "Geçerli seçim yapınız!")


# ============ MATPLOTLIB GRAFİKLERİ ==========

class StatisticsWidget(QWidget):
    """İstatistikler ve grafikler widget"""

    def __init__(self, sistem, parent=None):
        super().__init__(parent)
        self.sistem = sistem
        self.figure = Figure(figsize=(12, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_charts(self):
        """Grafikleri güncelle"""
        self.figure.clear()

        # Pasta grafik - Araç dağılımı
        ax1 = self.figure.add_subplot(121)
        if self.sistem.araclar:
            musait = sum(1 for a in self.sistem.araclar if a.musait_mi)
            kirada = len(self.sistem.araclar) - musait

            sizes = [musait, kirada]
            labels = [f'✓ Müsait ({musait})', f'✗ Kirada ({kirada})']
            colors = ['#4CAF50', '#f44336']

            ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
            ax1.set_title('🚗 Araç Durumu', fontsize=12, fontweight='bold')
        else:
            ax1.text(0.5, 0.5, 'Araç Yok', ha='center', va='center', fontsize=14)

        # Bar grafik - İstatistikler
        ax2 = self.figure.add_subplot(122)
        labels = ['🚗 Araçlar', '👥 Kullanıcılar', '🔑 Kiralamalar']
        values = [len(self.sistem.araclar), len(self.sistem.kullanicilar), len(self.sistem.kiralamalar)]
        colors_bar = ['#2196F3', '#4CAF50', '#FF9800']

        bars = ax2.bar(labels, values, color=colors_bar, edgecolor='black', linewidth=1.5)
        ax2.set_title('📊 Sistem İstatistikleri', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Sayı', fontsize=10)

        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontweight='bold')

        self.canvas.draw()


# ============ ANA PENCERE ==========

class AracKiralamaMainWindow(QMainWindow):
    """Ana pencere"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚗 ARAÇ KİRALAMA YÖNETİM SİSTEMİ")
        self.setGeometry(0, 0, 1400, 800)
        self.setStyleSheet("background-color: #ffffff;")

        # Sistem verileri
        self.sistem = type('Sistem', (), {
            'araclar': [],
            'kullanicilar': [],
            'kiralamalar': []
        })()

        self.init_ui()

    def init_ui(self):
        """UI başlatma"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        # Başlık
        header = QLabel("🚗 ARAÇ KİRALAMA YÖNETİM SİSTEMİ")
        header_font = QFont()
        header_font.setPointSize(20)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #2196F3; padding: 20px;")

        # Dashboard
        dashboard_layout = QHBoxLayout()

        arac_card = self.create_stat_card("🚗 Araçlar", "0", "#2196F3")
        kul_card = self.create_stat_card("👥 Kullanıcılar", "0", "#4CAF50")
        kir_card = self.create_stat_card("🔑 Kiralamalar", "0", "#FF9800")

        dashboard_layout.addWidget(arac_card)
        dashboard_layout.addWidget(kul_card)
        dashboard_layout.addWidget(kir_card)

        self.arac_label = arac_card.findChild(QLabel, "value_label")
        self.kul_label = kul_card.findChild(QLabel, "value_label")
        self.kir_label = kir_card.findChild(QLabel, "value_label")

        # Sekme penceresi
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #2196F3;
                color: white;
            }
        """)

        # Araçlar sekmesi
        self.arac_tab = self.create_arac_tab()
        self.tabs.addTab(self.arac_tab, "🚗 Araçlar")

        # Kullanıcılar sekmesi
        self.kul_tab = self.create_kul_tab()
        self.tabs.addTab(self.kul_tab, "👥 Kullanıcılar")

        # Kiralamalar sekmesi
        self.kir_tab = self.create_kir_tab()
        self.tabs.addTab(self.kir_tab, "🔑 Kiralamalar")

        # Grafikler sekmesi
        self.stats_widget = StatisticsWidget(self.sistem)
        self.tabs.addTab(self.stats_widget, "📊 Grafikler")

        # Raporlar sekmesi
        self.rapor_tab = self.create_rapor_tab()
        self.tabs.addTab(self.rapor_tab, "📄 Raporlar")

        main_layout.addWidget(header)
        main_layout.addLayout(dashboard_layout)
        main_layout.addWidget(self.tabs)

        central_widget.setLayout(main_layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_all)
        self.timer.start(500)

    def create_stat_card(self, title, value, color):
        """İstatistik kartı oluştur"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
                padding: 20px;
                color: white;
            }}
        """)

        layout = QVBoxLayout()
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)

        value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(18)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setObjectName("value_label")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        card.setLayout(layout)

        return card

    def create_arac_tab(self):
        """Araç sekmesi"""
        widget = QWidget()
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("➕ Araç Ekle")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        ekle_btn.clicked.connect(self.arac_ekle)

        sil_btn = QPushButton("🗑️ Seçili Sil")
        sil_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        sil_btn.clicked.connect(self.arac_sil)

        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        yenile_btn.clicked.connect(self.arac_listele)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(sil_btn)
        button_layout.addWidget(yenile_btn)

        self.arac_table = QTableWidget()
        self.arac_table.setColumnCount(7)
        self.arac_table.setHorizontalHeaderLabels(["ID", "Marka", "Model", "Yıl", "KM", "Plaka", "Durum"])
        self.arac_table.setStyleSheet("border: 1px solid #ccc; border-radius: 4px;")

        layout.addLayout(button_layout)
        layout.addWidget(self.arac_table)
        widget.setLayout(layout)

        return widget

    def create_kul_tab(self):
        """Kullanıcı sekmesi"""
        widget = QWidget()
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("➕ Kullanıcı Ekle")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        ekle_btn.clicked.connect(self.kul_ekle)

        sil_btn = QPushButton("🗑️ Seçili Sil")
        sil_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        sil_btn.clicked.connect(self.kul_sil)

        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        yenile_btn.clicked.connect(self.kul_listele)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(sil_btn)
        button_layout.addWidget(yenile_btn)

        self.kul_table = QTableWidget()
        self.kul_table.setColumnCount(6)
        self.kul_table.setHorizontalHeaderLabels(["ID", "Ad", "Soyad", "Ehliyet", "Telefon", "Email"])
        self.kul_table.setStyleSheet("border: 1px solid #ccc; border-radius: 4px;")

        layout.addLayout(button_layout)
        layout.addWidget(self.kul_table)
        widget.setLayout(layout)

        return widget

    def create_kir_tab(self):
        """Kiralama sekmesi"""
        widget = QWidget()
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        baslat_btn = QPushButton("🔑 Kiralama Başlat")
        baslat_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        baslat_btn.clicked.connect(self.kir_baslat)

        bitir_btn = QPushButton("🔓 Kiralama Bitir")
        bitir_btn.setStyleSheet("background-color: #FF9800; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        bitir_btn.clicked.connect(self.kir_bitir)

        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        yenile_btn.clicked.connect(self.kir_listele)

        button_layout.addWidget(baslat_btn)
        button_layout.addWidget(bitir_btn)
        button_layout.addWidget(yenile_btn)

        self.kir_table = QTableWidget()
        self.kir_table.setColumnCount(8)
        self.kir_table.setHorizontalHeaderLabels(["ID", "Araç", "Kullanıcı", "Başlangıç KM", "Bitiş KM", "Kullanılan KM", "Ücret", "Durum"])
        self.kir_table.setStyleSheet("border: 1px solid #ccc; border-radius: 4px;")

        layout.addLayout(button_layout)
        layout.addWidget(self.kir_table)
        widget.setLayout(layout)

        return widget

    def create_rapor_tab(self):
        """Rapor sekmesi"""
        widget = QWidget()
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        rapor_btn = QPushButton("📋 Rapor Oluştur")
        rapor_btn.setStyleSheet("background-color: #9C27B0; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        rapor_btn.clicked.connect(self.rapor_olustur)

        button_layout.addWidget(rapor_btn)

        self.rapor_text = QTextEdit()
        self.rapor_text.setReadOnly(True)
        self.rapor_text.setStyleSheet("border: 1px solid #ccc; border-radius: 4px; padding: 10px;")

        layout.addLayout(button_layout)
        layout.addWidget(self.rapor_text)
        widget.setLayout(layout)

        return widget

    # ============ ARAÇ METODLARI ==========

    def arac_ekle(self):
        """Araç ekleme"""
        try:
            dialog = AracEkleDialog(self)
            if dialog.exec_() == QDialog.Accepted and dialog.result:
                marka, model, yil, km, plaka = dialog.result
                self.sistem.araclar.append(Arac(marka, model, km, yil, plaka))
                QMessageBox.information(self, "Başarılı", "Araç eklendi!")
                self.arac_listele()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Araç eklenirken hata: {str(e)}")

    def arac_sil(self):
        """Araç silme"""
        try:
            row = self.arac_table.currentRow()
            if row >= 0:
                arac_id = int(self.arac_table.item(row, 0).text())
                arac = next((a for a in self.sistem.araclar if a.arac_id == arac_id), None)

                if arac:
                    if not arac.musait_mi:
                        QMessageBox.warning(self, "Hata", "Kirada olan araç silinemez!")
                        return

                    reply = QMessageBox.question(self, "Onay", f"{arac.marka} {arac.model} silinsin mi?", QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.sistem.araclar.remove(arac)
                        QMessageBox.information(self, "Başarılı", "Araç silindi!")
                        self.arac_listele()
            else:
                QMessageBox.warning(self, "Hata", "Lütfen bir araç seçin!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Araç silinirken hata: {str(e)}")

    def arac_listele(self):
        """Araçları listele"""
        try:
            self.arac_table.setRowCount(0)
            for arac in self.sistem.araclar:
                row = self.arac_table.rowCount()
                self.arac_table.insertRow(row)
                self.arac_table.setItem(row, 0, QTableWidgetItem(str(arac.arac_id)))
                self.arac_table.setItem(row, 1, QTableWidgetItem(arac.marka))
                self.arac_table.setItem(row, 2, QTableWidgetItem(arac.model))
                self.arac_table.setItem(row, 3, QTableWidgetItem(str(arac.yil)))
                self.arac_table.setItem(row, 4, QTableWidgetItem(str(arac.kilometre)))
                self.arac_table.setItem(row, 5, QTableWidgetItem(arac.plaka))

                durum = "✓ Müsait" if arac.musait_mi else "✗ Kirada"
                self.arac_table.setItem(row, 6, QTableWidgetItem(durum))
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Araçlar listelenirken hata: {str(e)}")

    # ============ KULLANICI METODLARI ==========

    def kul_ekle(self):
        """Kullanıcı ekleme"""
        try:
            dialog = KullaniciEkleDialog(self)
            if dialog.exec_() == QDialog.Accepted and dialog.result:
                ad, soyad, eh, tel, email = dialog.result
                self.sistem.kullanicilar.append(Kullanici(ad, soyad, eh, tel, email))
                QMessageBox.information(self, "Başarılı", "Kullanıcı eklendi!")
                self.kul_listele()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kullanıcı eklenirken hata: {str(e)}")

    def kul_sil(self):
        """Kullanıcı silme"""
        try:
            row = self.kul_table.currentRow()
            if row >= 0:
                kul_id = int(self.kul_table.item(row, 0).text())
                kul = next((k for k in self.sistem.kullanicilar if k.kullanici_id == kul_id), None)

                if kul:
                    reply = QMessageBox.question(self, "Onay", f"{kul.ad} {kul.soyad} silinsin mi?", QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.sistem.kullanicilar.remove(kul)
                        QMessageBox.information(self, "Başarılı", "Kullanıcı silindi!")
                        self.kul_listele()
            else:
                QMessageBox.warning(self, "Hata", "Lütfen bir kullanıcı seçin!")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kullanıcı silinirken hata: {str(e)}")

    def kul_listele(self):
        """Kullanıcıları listele"""
        try:
            self.kul_table.setRowCount(0)
            for kul in self.sistem.kullanicilar:
                row = self.kul_table.rowCount()
                self.kul_table.insertRow(row)
                self.kul_table.setItem(row, 0, QTableWidgetItem(str(kul.kullanici_id)))
                self.kul_table.setItem(row, 1, QTableWidgetItem(kul.ad))
                self.kul_table.setItem(row, 2, QTableWidgetItem(kul.soyad))
                self.kul_table.setItem(row, 3, QTableWidgetItem(kul.ehliyet_no))
                self.kul_table.setItem(row, 4, QTableWidgetItem(kul.telefon))
                self.kul_table.setItem(row, 5, QTableWidgetItem(kul.email))
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kullanıcılar listelenirken hata: {str(e)}")

    # ============ KİRALAMA METODLARI ==========

    def kir_baslat(self):
        """Kiralama başlatma"""
        try:
            if not self.sistem.araclar or not self.sistem.kullanicilar:
                QMessageBox.warning(self, "Hata", "Araç veya Kullanıcı bulunamadı!")
                return

            dialog = KiralamaBaslatDialog(self.sistem.araclar, self.sistem.kullanicilar, self)
            if dialog.exec_() == QDialog.Accepted and dialog.result:
                arac_id, kul_id, fiyat = dialog.result

                arac = next((a for a in self.sistem.araclar if a.arac_id == arac_id), None)
                kul = next((k for k in self.sistem.kullanicilar if k.kullanici_id == kul_id), None)

                if arac and kul:
                    kiralama = Kiralama(arac, kul, fiyat)
                    basarili, mesaj = kiralama.kiralama_baslat()

                    if basarili:
                        self.sistem.kiralamalar.append(kiralama)
                        QMessageBox.information(self, "Başarılı", mesaj)
                        self.kir_listele()
                    else:
                        QMessageBox.warning(self, "Hata", mesaj)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kiralama başlatılırken hata: {str(e)}")

    def kir_bitir(self):
        """Kiralama bitirme"""
        try:
            aktif = [k for k in self.sistem.kiralamalar if k.bitis is None]

            if not aktif:
                QMessageBox.warning(self, "Hata", "Aktif kiralama bulunamadı!")
                return

            dialog = KiralamaBitirDialog(aktif, self)
            if dialog.exec_() == QDialog.Accepted and dialog.result:
                kir_id, yeni_km = dialog.result

                kiralama = next((k for k in self.sistem.kiralamalar if k.kiralama_id == kir_id), None)

                if kiralama:
                    basarili, mesaj = kiralama.kiralama_bitir(yeni_km)

                    if basarili:
                        QMessageBox.information(self, "Başarılı", mesaj)
                        self.kir_listele()
                    else:
                        QMessageBox.warning(self, "Hata", mesaj)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kiralama bitirirken hata: {str(e)}")

    def kir_listele(self):
        """Kiralamalar listele"""
        try:
            self.kir_table.setRowCount(0)
            for kir in self.sistem.kiralamalar:
                row = self.kir_table.rowCount()
                self.kir_table.insertRow(row)

                kullanilan_km = 0
                if kir.bitis_km and kir.baslangic_km:
                    kullanilan_km = kir.bitis_km - kir.baslangic_km

                ucret = kir.kira_hesapla()

                self.kir_table.setItem(row, 0, QTableWidgetItem(str(kir.kiralama_id)))
                self.kir_table.setItem(row, 1, QTableWidgetItem(f"{kir.arac.marka} {kir.arac.model}"))
                self.kir_table.setItem(row, 2, QTableWidgetItem(f"{kir.kullanici.ad} {kir.kullanici.soyad}"))
                self.kir_table.setItem(row, 3, QTableWidgetItem(str(kir.baslangic_km)))
                self.kir_table.setItem(row, 4, QTableWidgetItem(str(kir.bitis_km) if kir.bitis_km else "-"))
                self.kir_table.setItem(row, 5, QTableWidgetItem(f"{kullanilan_km} KM"))
                self.kir_table.setItem(row, 6, QTableWidgetItem(f"{ucret:.2f} TL"))
                self.kir_table.setItem(row, 7, QTableWidgetItem(kir.durum))
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kiralamalar listelenirken hata: {str(e)}")

    # ============ RAPOR METODLARI ==========

    def rapor_olustur(self):
        """Rapor oluşturma"""
        try:
            rapor = "📊 ARAÇ KİRALAMA SİSTEMİ RAPORU\n"
            rapor += "=" * 50 + "\n\n"

            # Genel İstatistikler
            rapor += "📈 GENEL İSTATİSTİKLER\n"
            rapor += "-" * 50 + "\n"
            rapor += f"Toplam Araç: {len(self.sistem.araclar)}\n"
            rapor += f"Müsait Araç: {sum(1 for a in self.sistem.araclar if a.musait_mi)}\n"
            rapor += f"Kirada Araç: {sum(1 for a in self.sistem.araclar if not a.musait_mi)}\n"
            rapor += f"Toplam Kullanıcı: {len(self.sistem.kullanicilar)}\n"
            rapor += f"Toplam Kiralama: {len(self.sistem.kiralamalar)}\n"
            rapor += f"Aktif Kiralama: {sum(1 for k in self.sistem.kiralamalar if k.bitis is None)}\n"

            # Gelir Raporu
            rapor += "\n💰 GELİR RAPORU\n"
            rapor += "-" * 50 + "\n"
            toplam_gelir = sum(k.kira_hesapla() for k in self.sistem.kiralamalar)
            rapor += f"Toplam Gelir: {toplam_gelir:.2f} TL\n"

            # Araç Raporu
            rapor += "\n🚗 ARAÇ RAPORU\n"
            rapor += "-" * 50 + "\n"
            for arac in self.sistem.araclar:
                durum = "✓ Müsait" if arac.musait_mi else "✗ Kirada"
                rapor += f"{arac.marka} {arac.model} ({arac.yil}) - {arac.plaka} - {durum}\n"

            # Kullanıcı Raporu
            rapor += "\n👥 KULLANICI RAPORU\n"
            rapor += "-" * 50 + "\n"
            for kul in self.sistem.kullanicilar:
                rapor += f"{kul.ad} {kul.soyad} - Kiralamalar: {len(kul.gecmis)} - KM: {kul.toplam_kilometre()}\n"

            # Kiralama Detayları
            rapor += "\n🔑 KİRALAMA DETAYLARı\n"
            rapor += "-" * 50 + "\n"
            for kir in self.sistem.kiralamalar:
                kullanilan_km = kir.bitis_km - kir.baslangic_km if kir.bitis_km and kir.baslangic_km else 0
                ucret = kir.kira_hesapla()
                rapor += f"ID: {kir.kiralama_id} | {kir.arac.marka} -> {kir.kullanici.ad} | {kullanilan_km} KM | {ucret:.2f} TL | {kir.durum}\n"

            self.rapor_text.setText(rapor)
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Rapor oluşturulurken hata: {str(e)}")

    # ============ REFRESH METODU ==========

    def refresh_all(self):
        """Tüm verileri yenile"""
        try:
            self.arac_label.setText(str(len(self.sistem.araclar)))
            self.kul_label.setText(str(len(self.sistem.kullanicilar)))
            self.kir_label.setText(str(len(self.sistem.kiralamalar)))
            self.stats_widget.update_charts()
        except Exception as e:
            print(f"Refresh hatası: {str(e)}")


# ============ MAIN ==========

def main():
    """Ana fonksiyon"""
    app = QApplication(sys.argv)
    window = AracKiralamaMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
