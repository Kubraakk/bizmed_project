# 🏥 Hasta Kayıt Kabul Sistemi

Proje, sağlık kurumlarındaki hasta kabul süreçlerini yönetmek için geliştirilmiş bir web uygulamasıdır. Projede hastalar sisteme kaydedilir, doktorlara atanır ve hastaların geçmiş muayene kayıtlarına ulaşılır. Sistem Django ile geliştirilmiş olup Docker üzerinde PostgreSQL veritabanı ile çalışmaktadır.

---

## 🚀 Özellikler

- ✅ Doktor ve bölüm tanımlama
- ✅ Hasta kayıt işlemleri (T.C, İsim, Soyisim, Telefon, Adres)
- ✅ Hastayı doktora bağlayarak kayıt (registration) oluşturma
- ✅ T.C Kimlik Numarası ile hasta sorgulama
- ✅ Hastanın geçmiş kayıtlarını görüntüleme
- ✅ İlişkisel veritabanı mimarisi (PostgreSQL)
- ✅ Docker üzerinden kolay kurulum ve çalıştırma

---

## 🛠 Kullanılan Teknolojiler

| Teknoloji | Açıklama |
|-----------|----------|
| Python | Programlama dili |
| Django | Backend framework |
| Django ORM | Veritabanı yönetimi |
| PostgreSQL | Veritabanı |
| Docker & Docker Compose | Container teknolojisi |
| HTML, CSS | Basit arayüz |
| MVT | Django mimarisi |

--- 

## 🧩 Veri Tabanı Diyagramı (ER Diagram) 
<img width="750" height="555" alt="Ekran Resmi 2025-10-15 12 57 34" src="https://github.com/user-attachments/assets/a2b52dde-1d0b-45d9-ae9c-f891fb93c0b2" />

## 📦 Kurulum (Docker ile Çalıştırma) 
Projeyi docker-compose kullanarak kolayca ayağa kaldırabilirsiniz.

```bash
# Projeyi klonlayın
git clone https://github.com/kullanici/hasta-kayit-kabul.git
cd hasta-kayit-kabul

# Docker ile çalıştırın
docker-compose up --build

# Uygulama http://localhost:8000
 adresinde çalışacaktır.
```

## 🔗 API Endpointleri 

| Endpoint | Method | Açıklama |
|----------|--------|-----------|
| `/api/patients/` | GET | Tüm hastaları listele |
| `/api/patients/` | POST | Yeni hasta kaydet |
| `/api/patients/<id>/` | GET | Hasta detay |
| `/api/patients/search/?tc=12345678901` | GET | T.C ile hasta sorgula |
| `/api/doctors/` | GET | Tüm doktorları listele |
| `/api/doctors/` | POST | Yeni doktor ekle |
| `/api/departments/` | GET | Bölümleri listele |
| `/api/registrations/` | POST | Hasta için kayıt oluştur |
| `/api/registrations/<id>/` | GET | Kayıt detay | 

Not: API'ler Django REST Framework ile geliştirilmiştir. 

## 🧪 API Testi

Projede API geliştirme ve test süreçleri için aşağıdaki araçlar kullanılmıştır:

| Araç | Amaç |
|------|------|
| **Swagger UI** | API dokümantasyonu ve canlı test |
| **Postman** | API isteklerinin manuel ve koleksiyon bazlı test edilmesi |

<img width="1010" height="627" alt="Ekran Resmi 2025-10-15 12 37 07" src="https://github.com/user-attachments/assets/4ec31e6b-2217-4500-a2b1-59b91339f715" />

## 🔧 Ortam Değişkenleri 
Docker ile birlikte aşağıdaki environment ayarları kullanılmaktadır: 

```bash
DB_HOST = db
DB_NAME = bizmed_db
DB_USER = user
DB_PASS = pass
```

## 📸 Ekran Görselleri  
<img width="1904" height="973" alt="Ekran Resmi 2025-10-15 12 38 58" src="https://github.com/user-attachments/assets/9c45e886-e51a-4b93-b9f1-4bdd4d2dddab" />
<img width="1906" height="972" alt="Ekran Resmi 2025-10-15 12 39 15" src="https://github.com/user-attachments/assets/a4be588d-222c-4c4d-8ecc-f34aa149f87c" />
<img width="1903" height="965" alt="Ekran Resmi 2025-10-15 12 39 39" src="https://github.com/user-attachments/assets/89c71581-be65-4950-b02f-fc3d2acd7797" />
<img width="1920" height="966" alt="Ekran Resmi 2025-10-15 12 40 58" src="https://github.com/user-attachments/assets/62eb825e-96e1-4c79-8a94-b7c81cdbcf96" />

## 👩‍💻 Geliştirici
Kübra Akpunar
🔗 LinkedIn: [https://www.linkedin.com/in/](https://www.linkedin.com/in/k%C3%BCbra-akpunar-1758b8205/)
