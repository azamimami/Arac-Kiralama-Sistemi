# 🚗 Premium Araç Kiralama Sistemi

Modern, kullanıcı dostu ve tam donanımlı bir araç kiralama yönetim sistemi. PyQt5 ile geliştirilmiş, SQLite veritabanı desteğine sahip, grafiksel raporlama ve kullanıcı yönetimi özellikleriyle donatılmıştır.
 user= admin
 password = admin123
 
# 📋 Özellikler

# 🔐 Kullanıcı Yönetimi
- Admin ve normal kullanıcı girişi
- Kullanıcı ekleme/silme (Admin yetkisi)
- Oturum yönetimi ve çıkış

# 🚗 Araç Yönetimi
- Araç ekleme, silme, listeleme
- Araç durumu takibi (Müsait/Kirada)
- Kilometre takibi
- Plaka benzersizlik kontrolü

# 👥 Müşteri Yönetimi
- Müşteri ekleme, silme, listeleme
- Ehliyet no ve email benzersizlik kontrolü
- Telefon ve email doğrulama

# 🔑 Kiralama İşlemleri
- Kiralama başlatma/bitirme
- Günlük fiyat belirleme
- Kilometre takibi ve kontrolü
- Aynı müşteri aynı anda sadece 1 araç kiralayabilir
- Kiradaki araç silinemez
- Aktif kiralaması olan müşteri silinemez

# 📊 Raporlama ve İstatistikler
- Toplam araç, müşteri, aktif kiralama ve ciro gösterimi
- Pasta grafik ile araç durumu dağılımı
- Çubuk grafik ile sistem istatistikleri
- Detaylı metin raporu

# 🔍 Arama Özelliği
- Tüm sekmelerde anlık arama
- Araç: Marka, Model, Plaka, Yıl
- Müşteri: Ad, Soyad, Ehliyet No, Telefon, Email
- Kiralama: Araç adı, Müşteri adı, Durum
- Kullanıcı: Kullanıcı Adı, Ad, Soyad, Rol

# 🖥️ Teknolojiler

- **Python 3.9+**
- **PyQt5** - GUI Framework
- **SQLite3** - Veritabanı
- **Matplotlib** - Grafikler

