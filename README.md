# TSharp GO (Geliştirme Ortamı) - T-Sharp İçin Resmi IDE

![Lisans](https://img.shields.io/badge/Lisans-GNU_AGPL_v3-red.svg)
![Sürüm](https://img.shields.io/badge/Sürüm-v0.2_Alpha-blue.svg)
![Statü](https://img.shields.io/badge/Statü-Aktif_Geliştirme-green.svg)
![Sistem](https://img.shields.io/badge/Sistem-Linux-lightgrey.svg)

---

## Proje Geliştiricisi ve Mimarı

TSharp GO, T-Sharp programlama dilinin resmi ve yerleşik entegre geliştirme ortamıdır (IDE). Projenin tüm arayüz mimarisi, metin işleme motoru, sözdizimi analizörü ve derleyici entegrasyonları tamamen bağımsız bir mühendislik çalışması olarak aşağıdaki geliştirici tarafından %100 oranında tamamlanmıştır.

| Geliştirici | Katkı Oranı | Portfolyo |
| :--- | :---: | :--- |
| [**Talha Berk Arslan**](https://github.com/Codertalha5524) | %100 | Baş Geliştirici / Yazılım Mimarı |

---

## 1. TSharp GO Nedir ve Neden Geliştirildi?

TSharp GO, T-Sharp (T#) programlama dili için özel olarak tasarlanmış, hafif, yüksek performanslı ve akıllı bir Entegre Geliştirme Ortamıdır. Standart ve genel amaçlı metin editörlerinin aksine, T-Sharp'ın Türkçe sözdizimini (syntax) yerel olarak anlar. Geliştiriciye kod yazım aşamasında anlık rehberlik eder, mantıksal hataları daha derleme aşamasına geçmeden tespit eder ve geliştirme sürecini büyük ölçüde hızlandırır.

Önemli Sürüm Notu (v0.1 Alpha): TSharp GO şu anda erken geliştirme (v0.1 Alpha) aşamasındadır. Bu nedenle proje dizininde derlenmiş, doğrudan çalıştırılabilir (.exe veya ELF formatında) kurulum dosyaları henüz bulunmamaktadır. Test uzmanlarının ve geliştiricilerin, ortamı doğrudan kaynak kod üzerinden Python yorumlayıcısı ile çalıştırması gerekmektedir.

---

## 2. Çekirdek Özellikler ve Performans Avantajları

TSharp GO, günümüzün donanım canavarı hantal IDE'lerinin aksine, sadece ihtiyaç duyulan özelliklere odaklanarak maksimum performans ve stabilite sunmayı hedefler.

### Ultra Düşük Kaynak Tüketimi ve Optimizasyon
Arka planda gereksiz telemetri servisleri veya ağır indeksleme motorları çalıştırmaz. Bellek (RAM) ve işlemci (CPU) kullanımı minimum düzeyde tutulmuştur. Bu mimari tercih sayesinde, eski nesil bilgisayarlarda, kısıtlı donanıma sahip eğitim laboratuvarlarında ve Raspberry Pi gibi tek kartlı sistemlerde bile anında açılır ve sıfır gecikme ile çalışır.

### Gelişmiş Veri Güvenliği: Otomatik Kayıt ve Periyodik Yedekleme
Yazılım geliştirme sürecindeki en büyük risk olan veri kaybı, TSharp GO ile tarihe karışıyor. 
* Otomatik Kayıt (Auto-Save): Sistem, arka planda çalışan son derece hafif, asenkron bir döngü ile yazdığınız kodları her 10 saniyede bir otomatik olarak geçici belleğe ve diske kaydeder.
* Periyodik Yedekleme (Interval Backup): Sadece üzerine yazmakla kalmaz, belirlediğiniz aralıklarla projenizin zaman damgalı tam bir yedeğini (backup) oluşturur. Olası bir elektrik kesintisi veya sistem çökmesi durumunda, saniyeler öncesine dönerek emeğinizi %100 oranında koruma altına alır.

### Akıllı Sözdizimi Vurgulama (Syntax Highlighting)
Gelişmiş bir metin ayrıştırıcı (parser) kullanarak T-Sharp'ın komut setine (eğer, döngü, kullan, fonksiyon, yazdır vb.) tam entegre çalışır. Rezerve edilmiş kelimeleri, kullanıcı tanımlı değişkenleri, metin dizilerini (string) ve sayısal değerleri anında tanır ve farklı renk paletleriyle vurgular. Bu sayede kod okunabilirliği en üst düzeye çıkar ve yapısal hataların gözle tespiti kolaylaşır.

### Gerçek Zamanlı Hata Denetimi ve Analiz (Real-time Linter)
Siz kod yazarken, TSharp GO arka planda sürekli olarak sözdizimi kurallarını denetler. 
* Kapatılmamış bloklar (örneğin bir "eğer" veya "döngü" bloğunun "son" komutu ile bitirilmemesi),
* Eksik veya hatalı parametre girişleri,
* Tanımlanmamış değişken kullanımları anında tespit edilir. 
Derleme (compile) aşamasına geçmeden önce editör üzerinde görsel uyarılar verilerek geliştiriciye rehberlik edilir.

---

## 3. Ekosistem Entegrasyonu ve Tek Tuşla Otomasyon

TSharp GO, tek başına izole bir metin editörü değildir; tüm T-Sharp ekosisteminin merkezi kontrol istasyonudur. Gerekli motorlar işletim sisteminize entegre edildiyse, yazdığınız kodu tek bir tuşa basarak test edebilir veya nihai bir yazılıma dönüştürebilirsiniz.

Bu otomasyon özelliklerinin çalışması için aşağıdaki iki modülün sisteminizde kurulu olması ve işletim sisteminizin Çevre Değişkenlerine (PATH) kesin olarak eklenmiş olması zorunludur:

1. Ana Yorumlayıcı (T-Sharp Çekirdeği)
   Yazdığınız kodları anında yorumlamak, test etmek ve hata ayıklamak için gereklidir.
   Bağlantı: https://github.com/Artfical/TSharp

2. Derleme Motoru (TCompile)
   Geliştirdiğiniz projeyi, çalışmak için hiçbir dış bağımlılığa ihtiyaç duymayan, son kullanıcıya hazır bağımsız dosyalar (.exe / ELF) haline getirmek için gereklidir.
   Bağlantı: https://github.com/Artfical/TCompile

Sistem Gereksinimi Notu: İşletim sisteminizin terminalinde "tsharp" ve "derle" komutları global olarak çalışıyorsa (PATH yapılandırması başarılıysa), TSharp GO arayüzünün üst menüsünde bulunan "Çalıştır" ve "Tek Tuşla Derle" butonları, ilgili repoları otomatik olarak tetikleyecek ve işlemleri kusursuz şekilde gerçekleştirecektir.

---

## 4. Kurulum ve Çalıştırma Talimatları (Kaynak Kod Üzerinden)

TSharp GO v0.1 Alpha sürümünü bilgisayarınızda derlemek ve çalıştırmak için aşağıdaki adımları sırasıyla izlemeniz gerekmektedir:

1. Depoyu Klonlama: Bu repoyu bilgisayarınıza indirin veya Git üzerinden klonlayın.
2. Dizin Erişimi: Terminal (CMD, PowerShell, Bash) üzerinden indirdiğiniz proje dizinine giriş yapın.
3. Bağımlılıkların Yüklenmesi: Arayüz motorunun çalışabilmesi için gerekli olan Python kütüphanelerini sisteminize kurun (Örneğin: PySide6, Tkinter veya projenin requirements.txt dosyasında belirtilen diğer modüller).
4. Uygulamayı Başlatma: Ana başlatıcı dosyayı Python yorumlayıcısı ile çalıştırın:

   python main.py

---

## 5. Gelecek Vizyonu ve Yol Haritası (Roadmap)

Şu an v0.1 aşamasında olan TSharp GO için planlanan gelecekteki geliştirmeler:

* Görsel Hata Ayıklayıcı (Visual Debugger): Kodun adım adım (step-by-step) çalıştırılabildiği ve bellek durumunun anlık izlenebildiği bir debug arayüzü.
.

---

## 6. Lisans ve Kullanım Hakları

Bu yazılım ve T-Sharp ekosisteminin tüm bileşenleri GNU Affero General Public License v3.0 (AGPL-3.0) altında özgür yazılım olarak lisanslanmıştır. 

Özgür yazılım felsefesine sıkı sıkıya bağlı kalarak; yazılımın kaynak kodları incelenebilir, eğitim veya ticari amaçlarla kullanılabilir, değiştirilebilir ve aynı lisans koşulları altında yeniden dağıtılabilir. Ekosisteme yapılan her türlü geri bildirim ve kod katkısı, açık kaynak topluluğunun büyümesine ve yerli teknoloji üretim bilincine doğrudan destek sağlayacaktır.
