# TSharp GO — Değişiklik Günlüğü

![Lisans](https://img.shields.io/badge/Lisans-GNU_AGPL_v3-red.svg)
![Sürüm](https://img.shields.io/badge/Sürüm-v4.1-blue.svg)
![Statü](https://img.shields.io/badge/Proje-Solo_Açık_Kaynak-green.svg)
![Derleyici](https://img.shields.io/badge/Derleyici-TCompile-yellow.svg)
 ---
## Başlangıç v0.1 A

> Stabil olmayan arayüz
> Hata sistemi yanlış bilgilendiriyor











## v0.2 A — PyQt6 Geçişi

> Tkinter altyapısından PyQt6'ya tam geçiş. Tüm özellikler korunmuş, performans ve görsel kalite önemli ölçüde artmıştır.

---

## Kazanımlar

### Performans

- **Syntax highlighting artık ayrı bir thread bloğu oluşturmuyor.** Tkinter'da `tag_add()` çağrıları her tuş vuruşunda tüm editörü yeniden tarıyordu. PyQt6'daki `QSyntaxHighlighter`, yalnızca değişen bloğu yeniden renklendirir — büyük dosyalarda fark çok belirgin.
- **Process çıktısı artık UI'ı dondurmyor.** Eski yapıda `threading.Thread` terminale yazarken `root.after()` kuyruğu dolabiliyordu. Yeni `RunThread (QThread)` sistemi sinyal/slot mimarisiyle ana thread'i tamamen serbest bırakır.
- **Satır numarası paneli artık ayrı bir widget.** Tkinter'da ikinci bir `tk.Text` widget'ı ile senkron tutuluyordu; bu hem CPU hem bellek israfıydı. Yeni `LineNumberArea`, `QPainter` ile doğrudan ekrana çizer — widget oluşturma maliyeti sıfır.

### Görsel & UX

- **Native scrollbar.** Tkinter scrollbar'ları platforma göre çirkin görünürdü (özellikle Linux/Pi'de). `QScrollBar` ile tema rengine tam uyan, ince ve modern scrollbar.
- **Splitter tutamaçları artık renklendirilebilir.** Tkinter `PanedWindow` sash'leri tema rengine uymuyordu. `QSplitter` stylesheet ile tam kontrol altında.
- **Menü çubuğu tema rengi alıyor.** Tkinter `Menu` widget'ı sistem temasını zorla kullanırdı; arka plan rengi verilemezdi (bazı Linux WM'lerinde). `QMenuBar` stylesheet ile tamamen özelleştirilebilir.
- **Buton hover efektleri CSS ile tanımlı.** Eski yapıda `<Enter>` / `<Leave>` event binding ile manuel yapılıyordu; şimdi `QPushButton:hover` selector yeterli.
- **Cursor genişliği artık gerçekten 2px.** Tkinter `insertwidth=2` Pi'de görmezden gelinebiliyordu. `QPlainTextEdit.setCursorWidth(2)` her platformda çalışır.

### Kararlılık & Güvenilirlik

- **`tabs=("    ",)` crash'i tamamen ortadan kalktı.** Bu Tkinter'a özgü bir bug'dı; PyQt6'da `setTabStopDistance(40)` ile temiz çözüm.
- **`TclError` artık mümkün değil.** Tkinter, Tcl/Tk köprüsü üzerinden çalıştığı için beklenmedik `TclError` fırlatabiliyordu. PyQt6 doğrudan Qt C++ katmanına bağlanır.
- **Thread-safe terminal yazma.** Eski `root.after(0, self._terminal_write, ...)` çağrısı teorik olarak race condition içeriyordu. `pyqtSignal` mekanizması thread-safe olduğu Qt tarafından garanti edilir.
- **`closeEvent` override ile güvenli kapanış.** Tkinter'da `WM_DELETE_WINDOW` protokol binding gerekiyordu; kolayca unutulabiliyordu. `QMainWindow.closeEvent` her zaman çağrılır.

### Geliştirilebilirlik

- **Tema sistemi tamamen CSS tabanlı.** Renk eklemek veya değiştirmek için artık `_apply_theme()` içinde tek tek widget config'lemek gerekmiyor; stylesheet'e bir satır eklemek yeterli.
- **`QSyntaxHighlighter` subclass edilebilir.** Yeni dil desteği veya kural eklemek için `_build_rules()` metoduna pattern eklemek yeterli — Tkinter `tag_configure` sisteminden çok daha temiz.
- **`QThread` subclass pattern.** Yeni arka plan işlemleri (örneğin format, lint) için `RunThread` kopyalanıp sinyal eklenerek kolayca genişletilebilir.
- **`QSplitter` boyutları kayıt altına alınabilir.** İleride `QSettings` ile panel boyutları oturum başına hatırlanabilir; Tkinter `PanedWindow` ile bu zahmetliydi.

---

## Değişiklik Günlüğü

### Eklenenler

- `QSyntaxHighlighter` tabanlı `TSharpHighlighter` sınıfı
- `QPlainTextEdit` + `LineNumberArea` tabanlı `CodeEditor` sınıfı (satır no paneli dahili)
- `QThread` tabanlı `RunThread` sınıfı — process çıktısı sinyal ile iletilir
- `QDialog` tabanlı `DownloadPopup` sınıfı
- `QSplitter` ile yeniden boyutlandırılabilir panel sistemi
- `QTimer` (singleShot) ile debounce — highlight 120ms, diagnostics 400ms
- `QAction` ile menü kısayolları (`Ctrl+N`, `Ctrl+O`, `Ctrl+S`, `Ctrl+Z`, `Ctrl+Y`)
- `app.setStyle("Fusion")` — tüm platformlarda tutarlı widget görünümü
- Çok satırlı `liste` ve `sozluk` desteği analizörde
- Satır sonu `:` karakteri blok komutlarında artık kabul ediliyor (`her x icinde y:`)
- Bilinmeyen keyword / tanımlanmamış değişken hata tespiti

### Değiştirilenler

| Eski (Tkinter) | Yeni (PyQt6) |
|---|---|
| `tk.Tk` + `tk.Text` (editör) | `QMainWindow` + `CodeEditor` |
| `tk.Text` (satır numarası) | `LineNumberArea` (QPainter) |
| `ttk.Treeview` | `QTreeWidget` |
| `tk.Listbox` (diagnostics) | `QListWidget` |
| `tk.PanedWindow` | `QSplitter` |
| `tk.Menu` + `add_command` | `QMenuBar` + `QAction` |
| `messagebox.*` | `QMessageBox` |
| `filedialog.*` | `QFileDialog` |
| `tk.Toplevel` (popup) | `QDialog` subclass |
| `tag_configure` + `tag_add` | `QSyntaxHighlighter.setFormat` |
| `root.after()` debounce | `QTimer.singleShot` |
| `threading.Thread` (process) | `QThread` + `pyqtSignal` |
| `tkfont.Font` | `QFont` |
| `widget.config(bg=...)` x50 | Global stylesheet |
| `tabs=("    ",)` ← crash | `setTabStopDistance(40)` |
| `insertwidth=2` (unreliable) | `setCursorWidth(2)` |

### Kaldırılanlar

- `import tkinter as tk` ve tüm bağımlılıkları
- `from tkinter import ttk, filedialog, messagebox, font as tkfont`
- `_setup_fonts()` metodu — `QFont` inline tanımlanıyor
- `_setup_syntax_tags()` metodu — `TSharpHighlighter._build_rules()` ile değiştirildi
- `_sync_scroll()` ve `_on_scroll()` metodları — `QScrollBar` otomatik senkronize eder
- `_update_lineno()` metodu — `LineNumberArea.paintEvent` ile değiştirildi
- `self._all_widgets` sözlüğü — stylesheet global uygulanıyor
- `windll` DPI farkındalığı bloğu — Qt otomatik yönetir

### Düzeltilen Hatalar

- `TclError: bad screen distance "    "` — `tabs` argümanı hatalıydı
- Çok satırlı `liste [ ... ]` tanımı yanlış hata veriyordu
- Türkçe karakterler (ç, ş, ğ, ü, ö, ı) string literallerde bozuktu
- `severity_icons` emoji yerine harf kullanıyor (`E`, `U`, `B`)

---

## Gereksinimler

```
python3 >= 3.10
PyQt6 >= 6.4
```

Raspberry Pi için kurulum:

```bash
pip install PyQt6 --break-system-packages
```

---

*TSharp GO — GNU AGPL v3 — Artfical*
