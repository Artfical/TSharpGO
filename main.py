#!/usr/bin/env python3
"""
TSharp GO - TSharp Geliştirme Ortamı
GNU AGPL v3 Licensed
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font as tkfont
import subprocess
import threading
import os
import re
import shutil
import webbrowser
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────
# TEMA
# ─────────────────────────────────────────────────────────────────────
THEMES = {
    "dark": {
        "bg":           "#0d1117",
        "sidebar_bg":   "#161b22",
        "editor_bg":    "#0d1117",
        "terminal_bg":  "#010409",
        "panel_bg":     "#161b22",
        "border":       "#30363d",
        "fg":           "#e6edf3",
        "fg_dim":       "#8b949e",
        "fg_faint":     "#484f58",
        "accent":       "#1f6feb",
        "accent_hover": "#388bfd",
        "tab_active":   "#0d1117",
        "tab_inactive": "#161b22",
        "sel_bg":       "#1f3a5f",
        "cursor":       "#e6edf3",
        "line_no":      "#484f58",
        "scrollbar":    "#30363d",
        "btn_bg":       "#21262d",
        "btn_fg":       "#e6edf3",
        "btn_hover":    "#30363d",
        "run_bg":       "#238636",
        "run_hover":    "#2ea043",
        "compile_bg":   "#1f6feb",
        "compile_hover":"#388bfd",
        "err_bg":       "#161b22",
        "err_border":   "#30363d",
        # syntax
        "syn_keyword":  "#ff7b72",
        "syn_string":   "#a5d6ff",
        "syn_number":   "#79c0ff",
        "syn_comment":  "#8b949e",
        "syn_function": "#d2a8ff",
        "syn_builtin":  "#ffa657",
        "syn_operator": "#ff7b72",
        "syn_boolean":  "#79c0ff",
        # diagnostics
        "diag_error":   "#f85149",
        "diag_warning": "#d29922",
        "diag_info":    "#3fb950",
        "diag_bg":      "#161b22",
    },
    "light": {
        "bg":           "#ffffff",
        "sidebar_bg":   "#f6f8fa",
        "editor_bg":    "#ffffff",
        "terminal_bg":  "#f6f8fa",
        "panel_bg":     "#f6f8fa",
        "border":       "#d0d7de",
        "fg":           "#1f2328",
        "fg_dim":       "#57606a",
        "fg_faint":     "#afb8c1",
        "accent":       "#0969da",
        "accent_hover": "#0550ae",
        "tab_active":   "#ffffff",
        "tab_inactive": "#f6f8fa",
        "sel_bg":       "#dbeafe",
        "cursor":       "#1f2328",
        "line_no":      "#afb8c1",
        "scrollbar":    "#d0d7de",
        "btn_bg":       "#f6f8fa",
        "btn_fg":       "#1f2328",
        "btn_hover":    "#e5e9ec",
        "run_bg":       "#1a7f37",
        "run_hover":    "#2ea043",
        "compile_bg":   "#0969da",
        "compile_hover":"#0550ae",
        "err_bg":       "#f6f8fa",
        "err_border":   "#d0d7de",
        # syntax
        "syn_keyword":  "#cf222e",
        "syn_string":   "#0a3069",
        "syn_number":   "#0550ae",
        "syn_comment":  "#6e7781",
        "syn_function": "#8250df",
        "syn_builtin":  "#953800",
        "syn_operator": "#cf222e",
        "syn_boolean":  "#0550ae",
        # diagnostics
        "diag_error":   "#cf222e",
        "diag_warning": "#9a6700",
        "diag_info":    "#1a7f37",
        "diag_bg":      "#f6f8fa",
    }
}

# ─────────────────────────────────────────────────────────────────────
# T# SÖZ DIZIMI TANIMALARI
# ─────────────────────────────────────────────────────────────────────
TSHARP_KEYWORDS = [
    "degisken", "liste", "sozluk", "fonksiyon", "dondur", "son",
    "eger", "degilse", "dongu", "her", "icinde", "dur", "devam",
    "girdi", "yazdır", "yazdır", "yaz", "kullan", "ag", "gui", "gui6",
    "zip_olustur", "zip_ekle", "zip_listele", "zip_ac", "zip_cikar", "zip_sil",
    "klasor_olustur", "gpio_baslat", "gpio_kapat", "gpio_mod", "gpio_yaz",
    "gpio_oku", "gpio_yukari_cek", "gpio_asagi_cek", "gpio_kesme",
    "gpio_kesme_kaldir", "pwm_baslat", "pwm_ayarla", "pwm_frekans", "pwm_durdur",
    "i2c_baslat", "i2c_kapat", "i2c_yaz", "i2c_oku", "i2c_kayit_yaz", "i2c_kayit_oku",
    "spi_baslat", "spi_kapat", "spi_transfer",
    "http_get", "http_post", "http_put", "http_delete", "http_patch", "http_head",
    "json_al", "json_gonder", "dosya_indir", "stream_indir", "coklu_dosya_gonder",
    "ping", "baslik_ekle", "cerez_ekle", "timeout_ayarla", "proxy_ayarla", "durum_kodu",
    "pencere", "pencere_goster", "pencere_baslik", "pencere_boyut", "pencere_renk", "pencere_kapat",
    "guncelle", "etiket", "buton", "giriskutusu", "metin_alani", "onay_kutusu",
    "radyo_buton", "combo_kutu", "liste_kutusu", "kaydirici", "ilerleme_cubugu",
    "sayac_kutu", "widget_deger", "widget_ayarla", "widget_renk", "widget_font",
    "widget_yerlestir", "widget_gizle", "widget_goster", "widget_etkinlestir",
    "widget_devre_disi", "widget_sil", "canvas", "frame", "ayirici",
    "menu_cubugu", "menu_ekle", "menu_madde_ekle", "menu_ayirici_ekle",
    "notebook", "notebook_sekme", "agac", "agac_ekle", "tablo", "tablo_sutun",
    "tablo_satir", "kaydirma_alani", "mesaj_kutusu", "uyari_kutusu", "hata_kutusu",
    "soru_kutusu", "giris_kutusu", "renk_sec", "dosya_sec", "klasor_sec", "yazi_sec",
    "olay_bagla", "timer_olustur",
    "qt_pencere", "qt_pencere_goster", "qt_calistir", "qt_layout", "qt_etiket",
    "qt_buton", "qt_giriskutusu", "qt_metin_alani", "qt_onay_kutusu", "qt_radyo_buton",
    "qt_combo_kutu", "qt_kaydirici", "qt_ilerleme_cubugu", "qt_spin_kutu",
    "qt_tarih_secici", "qt_saat_secici", "qt_takvim", "qt_liste_widget",
    "qt_tablo_widget", "qt_agac_widget", "qt_sekme_widget", "qt_menu",
    "qt_toolbar", "qt_statusbar", "qt_grafik", "qt_web_tarayici",
    "qt_video_oynatici", "qt_timer", "qt_mesaj_kutusu", "qt_dosya_dialog",
    "qt_renk_dialog",
    "canvas_cizgi", "canvas_dikdortgen", "canvas_oval", "canvas_metin",
    "canvas_resim", "canvas_temizle", "canvas_nesne_sil",
]

TSHARP_BUILTINS = [
    "yaziya", "sayiya", "ondalikliya", "tur", "mutlak", "karekok", "yuvarla",
    "taban", "tavan", "us", "rastgele_sayi", "uzunluk", "buyuk_harf", "kucuk_harf",
    "basa_bas", "bol", "birlestir", "degistir", "bul", "dilim", "baslar_mi",
    "biter_mi", "ekle", "cikar", "sirala", "tersine_cevir", "icindemi",
    "toplam", "ortalama", "minimum", "maksimum", "dilimleme", "zaman",
    "dosya_oku", "dosya_yaz", "dosya_ekle", "dosya_var_mi",
]

TSHARP_BOOLEANS = ["dogru", "yanlis", "hic", "ve", "veya", "degil",
                    "esittir", "degildir", "buyuktur", "kucuktur",
                    "buyuk_esit", "kucuk_esit", "bolum", "mod"]

# ─────────────────────────────────────────────────────────────────────
# HATA ANALİZÖRÜ
# ─────────────────────────────────────────────────────────────────────
def analyze_tsharp(code: str) -> list:
    """Returns list of (line_no, severity, message) tuples."""
    diagnostics = []
    lines = code.split("\n")

    open_blocks    = []  # stack: ("eger"/"dongu"/"her"/"fonksiyon", line_no)
    declared_vars  = set()
    declared_funcs = set()

    KEYWORD_SET = set(TSHARP_KEYWORDS)
    BUILTIN_SET = set(TSHARP_BUILTINS)
    BOOLEAN_SET = set(TSHARP_BOOLEANS)
    ALL_KNOWN   = KEYWORD_SET | BUILTIN_SET | BOOLEAN_SET

    # Çok satırlı liste/sozluk takibi
    ml_open_char  = None  # '[' veya '{'
    ml_close_char = None  # ']' veya '}'
    ml_depth      = 0

    for i, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()

        # Yorum satırı veya boş satır
        if line.startswith("//") or line == "":
            continue

        # Yorum kısmını temizle (string içindeki // ignore et)
        if "//" in line:
            in_str   = False
            str_char = None
            for ci, ch in enumerate(line):
                if not in_str and ch in ('"', "'"):
                    in_str   = True
                    str_char = ch
                elif in_str and ch == str_char:
                    in_str = False
                elif not in_str and ch == '/' and ci + 1 < len(line) and line[ci+1] == '/':
                    line = line[:ci].strip()
                    break

        # Çok satırlı liste/sozluk devam satırı — sadece parantez say, başka kontrol yapma
        if ml_open_char is not None:
            for ch in line:
                if ch == ml_open_char:
                    ml_depth += 1
                elif ch == ml_close_char:
                    ml_depth -= 1
            if ml_depth <= 0:
                ml_open_char  = None
                ml_close_char = None
                ml_depth      = 0
            continue

        # Açılmamış string kontrolü
        quote_count_d = line.count('"') - line.count('\\"')
        quote_count_s = line.count("'") - line.count("\\'")
        if quote_count_d % 2 != 0:
            diagnostics.append((i, "error", 'Kapatılmamış çift tırnak (") tespit edildi.'))
        if quote_count_s % 2 != 0:
            diagnostics.append((i, "error", "Kapatılmamış tek tırnak (') tespit edildi."))

        tokens = line.split()
        if not tokens:
            continue

        # Satır sonu ':' T#'da blok başlangıcı olarak da kullanılabilir — temizle
        cmd = tokens[0].rstrip(":")

        # Blok açan komutlar
        if cmd in ("eger", "dongu", "her", "fonksiyon"):
            if cmd == "eger" and len(tokens) < 2:
                diagnostics.append((i, "error", "'eger' komutu bir koşul gerektirir."))
            if cmd == "dongu" and len(tokens) < 2:
                diagnostics.append((i, "error", "'dongu' komutu bir koşul gerektirir."))
            if cmd == "her":
                clean_tokens = [t.rstrip(":") for t in tokens]
                if "icinde" not in clean_tokens:
                    diagnostics.append((i, "error",
                        "'her' döngüsü 'icinde' anahtar kelimesini gerektirir. Örnek: her eleman icinde liste"))
            if cmd == "fonksiyon":
                if len(tokens) < 2:
                    diagnostics.append((i, "error", "'fonksiyon' bir isim gerektirir."))
                else:
                    fname = tokens[1].split("(")[0]
                    declared_funcs.add(fname)
            open_blocks.append((cmd, i))

        # 'son' kapama
        elif cmd == "son":
            if not open_blocks:
                diagnostics.append((i, "error", "Eşleşmeyen 'son': Açık bir blok bulunamadı."))
            else:
                open_blocks.pop()

        # 'degilse' kontrolü
        elif cmd == "degilse":
            if not open_blocks or open_blocks[-1][0] != "eger":
                diagnostics.append((i, "error", "'degilse' yalnızca 'eger' bloğunun ardından gelebilir."))

        # Değişken tanımlama
        elif cmd == "degisken":
            if len(tokens) < 2:
                diagnostics.append((i, "error", "'degisken' komutu bir isim gerektirir."))
            else:
                vname = tokens[1]
                if len(tokens) < 4 or tokens[2] != "=":
                    diagnostics.append((i, "warning",
                        f"'{vname}' değişkeni atama olmadan tanımlanmış olabilir. '=' operatörü bekleniyor."))
                declared_vars.add(vname)

        # Liste tanımlama — çok satırlı desteği ile
        elif cmd == "liste":
            if len(tokens) < 2:
                diagnostics.append((i, "error", "'liste' komutu bir isim gerektirir."))
            else:
                declared_vars.add(tokens[1])
                rest = " ".join(tokens[2:])
                if rest:
                    if not rest.startswith("["):
                        diagnostics.append((i, "warning", "Liste tanımlaması '[' ile başlamalıdır."))
                    else:
                        open_br  = rest.count("[")
                        close_br = rest.count("]")
                        if open_br != close_br:
                            # Çok satırlı liste — kapanana kadar devam satırlarını izle
                            ml_open_char  = "["
                            ml_close_char = "]"
                            ml_depth      = open_br - close_br
                        # open_br == close_br ise tek satırda tamam, hata yok

        # Sözlük tanımlama — çok satırlı desteği ile
        elif cmd == "sozluk":
            if len(tokens) < 2:
                diagnostics.append((i, "error", "'sozluk' komutu bir isim gerektirir."))
            else:
                declared_vars.add(tokens[1])
                rest = " ".join(tokens[2:])
                if rest:
                    if not rest.startswith("{"):
                        diagnostics.append((i, "warning", "Sözlük tanımlaması '{' ile başlamalıdır."))
                    else:
                        open_br  = rest.count("{")
                        close_br = rest.count("}")
                        if open_br != close_br:
                            # Çok satırlı sözlük — kapanana kadar devam satırlarını izle
                            ml_open_char  = "{"
                            ml_close_char = "}"
                            ml_depth      = open_br - close_br
                        # open_br == close_br ise tek satırda tamam, hata yok

        # yazdır / yaz
        elif cmd in ("yazdır", "yaz"):
            pass  # boş yazdır geçerli

        # girdi
        elif cmd == "girdi":
            if len(tokens) < 2:
                diagnostics.append((i, "error", "'girdi' komutu bir değişken ismi gerektirir."))
            else:
                declared_vars.add(tokens[1])

        # dondur — fonksiyon dışında kullanım
        elif cmd == "dondur":
            in_func = any(b[0] == "fonksiyon" for b in open_blocks)
            if not in_func:
                diagnostics.append((i, "warning", "'dondur' komutu bir fonksiyon dışında kullanılmış."))

        # dur / devam — döngü dışında kullanım
        elif cmd in ("dur", "devam"):
            in_loop = any(b[0] in ("dongu", "her") for b in open_blocks)
            if not in_loop:
                diagnostics.append((i, "warning", f"'{cmd}' komutu bir döngü dışında kullanılmış."))

        # kullan
        elif cmd == "kullan":
            if len(tokens) < 2:
                diagnostics.append((i, "error", "'kullan' komutu bir modül ismi gerektirir. Örnek: kullan ag"))
            else:
                modul = tokens[1]
                if modul not in ("ag", "gui", "gui6"):
                    diagnostics.append((i, "warning",
                        f"Bilinmeyen modül: '{modul}'. Geçerli modüller: ag, gui, gui6"))

        # Bilinmeyen komut / tanımlanmamış değişken
        elif cmd not in ALL_KNOWN:
            if re.match(r'^[a-zA-Z_\u00c0-\u024f][a-zA-Z0-9_\u00c0-\u024f]*$', cmd):
                if cmd not in declared_vars and cmd not in declared_funcs:
                    diagnostics.append((i, "error",
                        f"Bilinmeyen komut veya tanımlanmamış değişken: '{cmd}'. "
                        f"Bir değişken ise 'degisken {cmd} = ...' ile tanımlayın."))

        # Python tarzı print() kullanımı
        if re.search(r'\bprint\s*\(', line):
            diagnostics.append((i, "warning",
                "Python 'print()' kullanımı tespit edildi. T#'da 'yazdır' veya 'yaz' kullanın."))

        # Python tarzı for/if/while kullanımı
        if re.match(r'^(for|if|while|def|class|import|from|return)\b', line):
            python_kw = tokens[0]
            tsharp_eq = {"for": "her ... icinde ...", "if": "eger", "while": "dongu",
                         "def": "fonksiyon", "return": "dondur", "import": "kullan"}
            eq   = tsharp_eq.get(python_kw, "")
            hint = f" T#'da '{eq}' kullanın." if eq else ""
            diagnostics.append((i, "warning",
                f"Python anahtar kelimesi '{python_kw}' tespit edildi.{hint}"))

    # Kapanmamış bloklar
    for blk_type, blk_line in open_blocks:
        diagnostics.append((blk_line, "error",
            f"'{blk_type}' bloğu kapatılmamış: 'son' eksik."))

    return diagnostics


# ─────────────────────────────────────────────────────────────────────
# ANA IDE SINIFI
# ─────────────────────────────────────────────────────────────────────
class TSharpGO:
    def __init__(self, root):
        self.root = root
        self.root.title("TSharp GO")
        self.root.geometry("1400x850")
        self.root.minsize(900, 600)
        
        self.current_theme = "dark"
        self.T = THEMES["dark"]
        
        self.current_file = None
        self.saved = True
        self.diagnostics = []
        self.diag_vars = {}       # line -> list of diag
        self.highlight_job = None
        self.diag_job = None
        
        self._setup_fonts()
        self._build_ui()
        self._apply_theme()
        self._load_sidebar_dir(str(Path.home()))
        
        # İlk boş dosya
        self._new_file()
    
    # ─────────────────────────────────────
    # FONTLAR
    # ─────────────────────────────────────
    def _setup_fonts(self):
        self.font_editor   = tkfont.Font(family="Courier New", size=13)
        self.font_ui       = tkfont.Font(family="Segoe UI",    size=10)
        self.font_ui_bold  = tkfont.Font(family="Segoe UI",    size=10, weight="bold")
        self.font_sidebar  = tkfont.Font(family="Segoe UI",    size=9)
        self.font_terminal = tkfont.Font(family="Courier New", size=11)
        self.font_diag     = tkfont.Font(family="Segoe UI",    size=9)
        self.font_lineno   = tkfont.Font(family="Courier New", size=13)
        self.font_title    = tkfont.Font(family="Segoe UI",    size=10, weight="bold")
    
    # ─────────────────────────────────────
    # UI KURULUM
    # ─────────────────────────────────────
    def _build_ui(self):
        T = self.T
        
        # ── Menubar ──
        self.menubar = tk.Menu(self.root, tearoff=0)
        self.root.config(menu=self.menubar)
        
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Dosya", menu=file_menu)
        file_menu.add_command(label="Yeni",            command=self._new_file,   accelerator="Ctrl+N")
        file_menu.add_command(label="Aç",              command=self._open_file,  accelerator="Ctrl+O")
        file_menu.add_command(label="Kaydet",          command=self._save_file,  accelerator="Ctrl+S")
        file_menu.add_command(label="Farklı Kaydet",   command=self._save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış",           command=self.root.quit)
        
        edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Düzenle", menu=edit_menu)
        edit_menu.add_command(label="Geri Al",    command=lambda: self.editor.event_generate("<<Undo>>"),  accelerator="Ctrl+Z")
        edit_menu.add_command(label="Yinele",     command=lambda: self.editor.event_generate("<<Redo>>"),  accelerator="Ctrl+Y")
        
        view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Görünüm", menu=view_menu)
        view_menu.add_command(label="Karanlık Tema", command=lambda: self._switch_theme("dark"))
        view_menu.add_command(label="Açık Tema",     command=lambda: self._switch_theme("light"))
        
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Yardım", menu=help_menu)
        help_menu.add_command(label="TSharp Hakkında", command=lambda: webbrowser.open("https://github.com/Artfical/TSharp"))
        
        # ── Klavye kisayollari ──
        self.root.bind("<Control-n>", lambda e: self._new_file())
        self.root.bind("<Control-o>", lambda e: self._open_file())
        self.root.bind("<Control-s>", lambda e: self._save_file())
        
        # ── Toolbar ──
        self.toolbar = tk.Frame(self.root, height=44)
        self.toolbar.pack(side="top", fill="x")
        self.toolbar.pack_propagate(False)
        
        # Sol grup: dosya butonları
        left_bar = tk.Frame(self.toolbar)
        left_bar.pack(side="left", padx=8, pady=6)
        
        self.btn_new  = self._tb_btn(left_bar, "Yeni",           self._new_file,  width=6)
        self.btn_open = self._tb_btn(left_bar, "Aç",             self._open_file, width=6)
        self.btn_save = self._tb_btn(left_bar, "Kaydet",         self._save_file, width=7)
        
        # Orta: dosya adı
        self.title_var = tk.StringVar(value="adsiz.tsh")
        title_lbl = tk.Label(self.toolbar, textvariable=self.title_var, font=self.font_title)
        title_lbl.pack(side="left", padx=20)
        self.title_label = title_lbl
        
        # Sağ grup: tema + çalıştır + derle
        right_bar = tk.Frame(self.toolbar)
        right_bar.pack(side="right", padx=8, pady=6)
        
        self.btn_theme   = self._tb_btn(right_bar, "Açık Tema",  self._toggle_theme, width=10)
        
        sep = tk.Frame(right_bar, width=1, height=24)
        sep.pack(side="left", padx=6)
        self.sep_toolbar = sep
        
        self.btn_compile = self._tb_btn(right_bar, "Derle",  self._compile,  width=7, kind="compile")
        self.btn_run     = self._tb_btn(right_bar, "Çalıştır", self._run,    width=9, kind="run")
        
        # ── Ana icerik alani ──
        self.paned_main = tk.PanedWindow(self.root, orient="horizontal", sashwidth=4, sashrelief="flat")
        self.paned_main.pack(side="top", fill="both", expand=True)
        
        # Sidebar
        self.sidebar = tk.Frame(self.paned_main, width=210)
        self.paned_main.add(self.sidebar, minsize=140)
        
        sidebar_hdr = tk.Frame(self.sidebar, height=32)
        sidebar_hdr.pack(fill="x")
        sidebar_hdr.pack_propagate(False)
        sidebar_title = tk.Label(sidebar_hdr, text="DOSYA GEZGİNİ", font=self.font_ui_bold)
        sidebar_title.pack(side="left", padx=10, pady=6)
        self.sidebar_title_lbl = sidebar_title
        
        # Sidebar treeview
        self.file_tree = ttk.Treeview(self.sidebar, show="tree", selectmode="browse")
        self.file_tree.pack(fill="both", expand=True, pady=(0, 0))
        self.file_tree.bind("<Double-1>", self._sidebar_double_click)
        self.file_tree.bind("<Button-1>", self._sidebar_click)
        
        # Orta: editor + diagnostics
        self.center_paned = tk.PanedWindow(self.paned_main, orient="horizontal", sashwidth=4, sashrelief="flat")
        self.paned_main.add(self.center_paned, minsize=400)
        
        # Editör bölümü (lineno + editor)
        editor_outer = tk.Frame(self.center_paned)
        self.center_paned.add(editor_outer, minsize=350)
        
        # Editör / terminal dikey
        self.editor_paned = tk.PanedWindow(editor_outer, orient="vertical", sashwidth=4, sashrelief="flat")
        self.editor_paned.pack(fill="both", expand=True)
        
        # Editör frame
        self.editor_frame = tk.Frame(self.editor_paned)
        self.editor_paned.add(self.editor_frame, minsize=200)
        
        # Satır numaraları
        self.lineno = tk.Text(self.editor_frame, width=4, state="disabled",
                              padx=6, takefocus=0, bd=0, wrap="none",
                              cursor="arrow")
        self.lineno.pack(side="left", fill="y")
        
        # Editör scrollbar
        editor_scroll = tk.Scrollbar(self.editor_frame, orient="vertical")
        editor_scroll.pack(side="right", fill="y")
        
        editor_hscroll = tk.Scrollbar(self.editor_frame, orient="horizontal")
        editor_hscroll.pack(side="bottom", fill="x")
        
        self.editor = tk.Text(self.editor_frame, wrap="none", undo=True, maxundo=-1,
                              bd=0, padx=10, pady=8,
                              yscrollcommand=self._sync_scroll,
                              xscrollcommand=editor_hscroll.set,
                              insertwidth=2, tabs=("40",))
        self.editor.pack(side="left", fill="both", expand=True)
        
        editor_scroll.config(command=self._on_scroll)
        editor_hscroll.config(command=self.editor.xview)
        self.editor_vscroll = editor_scroll
        
        self.editor.bind("<KeyRelease>", self._on_key_release)
        self.editor.bind("<ButtonRelease>", self._update_lineno)
        
        # Terminal frame
        self.terminal_frame = tk.Frame(self.editor_paned, height=180)
        self.editor_paned.add(self.terminal_frame, minsize=100)
        
        term_hdr = tk.Frame(self.terminal_frame, height=28)
        term_hdr.pack(fill="x")
        term_hdr.pack_propagate(False)
        tk.Label(term_hdr, text="TERMINAL", font=self.font_ui_bold).pack(side="left", padx=10, pady=4)
        self.term_hdr = term_hdr
        
        btn_clear = tk.Button(term_hdr, text="Temizle", font=self.font_sidebar,
                              bd=0, padx=8, pady=2, cursor="hand2",
                              command=self._clear_terminal)
        btn_clear.pack(side="right", padx=8, pady=3)
        self.btn_clear_term = btn_clear
        
        term_scroll = tk.Scrollbar(self.terminal_frame)
        term_scroll.pack(side="right", fill="y")
        
        self.terminal = tk.Text(self.terminal_frame, state="disabled", wrap="word",
                                bd=0, padx=10, pady=8,
                                yscrollcommand=term_scroll.set)
        self.terminal.pack(fill="both", expand=True)
        term_scroll.config(command=self.terminal.yview)
        
        # Diagnostics panel (sağ)
        self.diag_frame = tk.Frame(self.center_paned, width=220)
        self.center_paned.add(self.diag_frame, minsize=180)
        
        diag_hdr = tk.Frame(self.diag_frame, height=32)
        diag_hdr.pack(fill="x")
        diag_hdr.pack_propagate(False)
        tk.Label(diag_hdr, text="SORUNLAR", font=self.font_ui_bold).pack(side="left", padx=10, pady=6)
        self.diag_hdr = diag_hdr
        self.diag_title_lbl = diag_hdr.winfo_children()[0]
        
        self.diag_count_var = tk.StringVar(value="")
        diag_count_lbl = tk.Label(diag_hdr, textvariable=self.diag_count_var, font=self.font_sidebar)
        diag_count_lbl.pack(side="right", padx=8)
        self.diag_count_lbl = diag_count_lbl
        
        diag_scroll = tk.Scrollbar(self.diag_frame)
        diag_scroll.pack(side="right", fill="y")
        
        self.diag_list = tk.Listbox(self.diag_frame, bd=0, activestyle="none",
                                     selectmode="browse", yscrollcommand=diag_scroll.set)
        self.diag_list.pack(fill="both", expand=True)
        diag_scroll.config(command=self.diag_list.yview)
        self.diag_list.bind("<<ListboxSelect>>", self._diag_goto_line)
        
        # Durum cubugu
        self.statusbar = tk.Frame(self.root, height=22)
        self.statusbar.pack(side="bottom", fill="x")
        self.statusbar.pack_propagate(False)
        
        self.status_var = tk.StringVar(value="Hazır")
        status_lbl = tk.Label(self.statusbar, textvariable=self.status_var, font=self.font_sidebar, anchor="w")
        status_lbl.pack(side="left", padx=10)
        self.status_lbl = status_lbl
        
        self.cursor_var = tk.StringVar(value="Satır 1, Sütun 1")
        cursor_lbl = tk.Label(self.statusbar, textvariable=self.cursor_var, font=self.font_sidebar, anchor="e")
        cursor_lbl.pack(side="right", padx=10)
        self.cursor_lbl = cursor_lbl
        
        # Tüm widget referanslari (tema icin)
        self._all_widgets = {
            "root": self.root,
            "toolbar": self.toolbar,
            "left_bar": left_bar,
            "right_bar": right_bar,
            "sidebar": self.sidebar,
            "sidebar_hdr": sidebar_hdr,
            "center_paned": self.center_paned,
            "paned_main": self.paned_main,
            "editor_outer": editor_outer,
            "editor_paned": self.editor_paned,
            "editor_frame": self.editor_frame,
            "terminal_frame": self.terminal_frame,
            "term_hdr": term_hdr,
            "diag_frame": self.diag_frame,
            "diag_hdr": diag_hdr,
            "statusbar": self.statusbar,
        }
    
    def _tb_btn(self, parent, text, cmd, width=8, kind="normal"):
        btn = tk.Button(parent, text=text, command=cmd, font=self.font_ui,
                        bd=0, padx=10, pady=3, cursor="hand2", width=width)
        btn.pack(side="left", padx=3)
        btn._kind = kind
        
        def on_enter(e):
            T = self.T
            if kind == "run":     btn.config(bg=T["run_hover"])
            elif kind == "compile": btn.config(bg=T["compile_hover"])
            else:                  btn.config(bg=T["btn_hover"])
        
        def on_leave(e):
            T = self.T
            if kind == "run":     btn.config(bg=T["run_bg"])
            elif kind == "compile": btn.config(bg=T["compile_bg"])
            else:                  btn.config(bg=T["btn_bg"])
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn
    
    # ─────────────────────────────────────
    # TEMA
    # ─────────────────────────────────────
    def _apply_theme(self):
        T = self.T
        
        self.root.config(bg=T["bg"])
        self.menubar.config(bg=T["panel_bg"], fg=T["fg"], activebackground=T["accent"],
                            activeforeground="#ffffff")
        
        # Toolbar
        self.toolbar.config(bg=T["panel_bg"])
        for w in self.toolbar.winfo_children():
            try: w.config(bg=T["panel_bg"])
            except: pass
        
        for frame in [self._all_widgets.get("left_bar"), self._all_widgets.get("right_bar")]:
            if frame:
                try: frame.config(bg=T["panel_bg"])
                except: pass
                for child in frame.winfo_children():
                    try:
                        kind = getattr(child, "_kind", "normal")
                        if kind == "run":
                            child.config(bg=T["run_bg"], fg="#ffffff")
                        elif kind == "compile":
                            child.config(bg=T["compile_bg"], fg="#ffffff")
                        else:
                            child.config(bg=T["btn_bg"], fg=T["btn_fg"])
                    except: pass
        
        self.title_label.config(bg=T["panel_bg"], fg=T["fg"])
        self.btn_theme.config(text="Açık Tema" if self.current_theme == "dark" else "Karanlık Tema")
        self.sep_toolbar.config(bg=T["border"])
        
        # Sidebar
        self.sidebar.config(bg=T["sidebar_bg"])
        self.sidebar_title_lbl.master.config(bg=T["sidebar_bg"])
        self.sidebar_title_lbl.config(bg=T["sidebar_bg"], fg=T["fg_dim"])
        
        # Treeview stili
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
            background=T["sidebar_bg"], foreground=T["fg"],
            fieldbackground=T["sidebar_bg"], borderwidth=0,
            rowheight=22, font=self.font_sidebar)
        style.configure("Treeview.Heading",
            background=T["sidebar_bg"], foreground=T["fg_dim"])
        style.map("Treeview",
            background=[("selected", T["sel_bg"])],
            foreground=[("selected", T["fg"])])
        style.configure("Vertical.TScrollbar",
            background=T["panel_bg"], troughcolor=T["panel_bg"],
            bordercolor=T["panel_bg"], arrowcolor=T["fg_dim"])
        
        # Editor
        self.editor_frame.config(bg=T["editor_bg"])
        self.editor.config(bg=T["editor_bg"], fg=T["fg"], insertbackground=T["cursor"],
                           selectbackground=T["sel_bg"], selectforeground=T["fg"],
                           font=self.font_editor)
        self.lineno.config(bg=T["sidebar_bg"], fg=T["line_no"], font=self.font_lineno)
        self.editor_vscroll.config(bg=T["panel_bg"], troughcolor=T["editor_bg"],
                                   activebackground=T["scrollbar"])
        
        # Terminal
        self.terminal_frame.config(bg=T["terminal_bg"])
        self.term_hdr.config(bg=T["panel_bg"])
        for child in self.term_hdr.winfo_children():
            try: child.config(bg=T["panel_bg"], fg=T["fg_dim"])
            except: pass
        self.btn_clear_term.config(bg=T["btn_bg"], fg=T["btn_fg"])
        self.terminal.config(bg=T["terminal_bg"], fg=T["fg"], font=self.font_terminal,
                             insertbackground=T["cursor"])
        
        # Diagnostics
        self.diag_frame.config(bg=T["diag_bg"])
        self.diag_hdr.config(bg=T["panel_bg"])
        self.diag_title_lbl.config(bg=T["panel_bg"], fg=T["fg_dim"])
        self.diag_count_lbl.config(bg=T["panel_bg"], fg=T["fg_dim"])
        self.diag_list.config(bg=T["diag_bg"], fg=T["fg"], selectbackground=T["sel_bg"],
                               selectforeground=T["fg"], font=self.font_diag)
        
        # Statusbar
        self.statusbar.config(bg=T["panel_bg"])
        self.status_lbl.config(bg=T["panel_bg"], fg=T["fg_dim"])
        self.cursor_lbl.config(bg=T["panel_bg"], fg=T["fg_dim"])
        
        # Paned
        self.paned_main.config(bg=T["border"])
        self.center_paned.config(bg=T["border"])
        self.editor_paned.config(bg=T["border"])
        
        # Editör syntax tagları yeniden tanımla
        self._setup_syntax_tags()
        self._highlight_syntax()
        self._update_lineno()
    
    def _setup_syntax_tags(self):
        T = self.T
        self.editor.tag_configure("keyword",  foreground=T["syn_keyword"])
        self.editor.tag_configure("string",   foreground=T["syn_string"])
        self.editor.tag_configure("number",   foreground=T["syn_number"])
        self.editor.tag_configure("comment",  foreground=T["syn_comment"], font=(self.font_editor.actual()["family"], self.font_editor.actual()["size"], "italic"))
        self.editor.tag_configure("function", foreground=T["syn_function"])
        self.editor.tag_configure("builtin",  foreground=T["syn_builtin"])
        self.editor.tag_configure("operator", foreground=T["syn_operator"])
        self.editor.tag_configure("boolean",  foreground=T["syn_boolean"])
        
        self.editor.tag_configure("diag_error",   underline=True, foreground=T["diag_error"])
        self.editor.tag_configure("diag_warning",  underline=True, foreground=T["diag_warning"])
        self.editor.tag_configure("diag_info",     underline=True, foreground=T["diag_info"])
        
        self.terminal.tag_configure("stdout", foreground=T["fg"])
        self.terminal.tag_configure("stderr", foreground=T["diag_error"])
        self.terminal.tag_configure("info",   foreground=T["diag_info"])
        self.terminal.tag_configure("cmd",    foreground=T["syn_function"])
    
    def _switch_theme(self, theme_name):
        self.current_theme = theme_name
        self.T = THEMES[theme_name]
        self._apply_theme()
    
    def _toggle_theme(self):
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self._switch_theme(new_theme)
    
    # ─────────────────────────────────────
    # SYNTAX HIGHLIGHTING
    # ─────────────────────────────────────
    def _highlight_syntax(self, event=None):
        code = self.editor.get("1.0", "end-1c")
        
        # Tüm tagları temizle
        for tag in ["keyword", "string", "number", "comment", "function", "builtin", "operator", "boolean",
                    "diag_error", "diag_warning", "diag_info"]:
            self.editor.tag_remove(tag, "1.0", "end")
        
        lines = code.split("\n")
        
        for i, line in enumerate(lines):
            line_start = f"{i+1}.0"
            
            # Yorum
            comment_match = re.search(r'(?<!:)(//)', line)
            in_str_pos = self._first_string_pos(line)
            if comment_match:
                cm_start = comment_match.start()
                if in_str_pos < 0 or cm_start < in_str_pos:
                    self.editor.tag_add("comment", f"{i+1}.{cm_start}", f"{i+1}.{len(line)}")
                    line = line[:cm_start]
            
            # String'ler
            for m in re.finditer(r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', line):
                self.editor.tag_add("string", f"{i+1}.{m.start()}", f"{i+1}.{m.end()}")
            
            # Sayılar
            for m in re.finditer(r'\b\d+\.?\d*\b', line):
                self.editor.tag_add("number", f"{i+1}.{m.start()}", f"{i+1}.{m.end()}")
            
            # Tokenlar
            tokens = re.finditer(r'\b([a-zA-Z_\u00c0-\u024f][a-zA-Z0-9_\u00c0-\u024f]*)\b', line)
            for m in tokens:
                word = m.group(1)
                col_s = m.start()
                col_e = m.end()
                if word in TSHARP_KEYWORDS:
                    self.editor.tag_add("keyword", f"{i+1}.{col_s}", f"{i+1}.{col_e}")
                elif word in TSHARP_BUILTINS:
                    self.editor.tag_add("builtin", f"{i+1}.{col_s}", f"{i+1}.{col_e}")
                elif word in TSHARP_BOOLEANS:
                    self.editor.tag_add("boolean", f"{i+1}.{col_s}", f"{i+1}.{col_e}")
            
            # Operatörler
            for m in re.finditer(r'(\+\+|--|==|!=|<=|>=|[+\-*/%=<>!])', line):
                self.editor.tag_add("operator", f"{i+1}.{m.start()}", f"{i+1}.{m.end()}")
        
        # Diagnostics işaretleme
        for line_no, severity, msg in self.diagnostics:
            tag = f"diag_{severity}"
            try:
                line_content = self.editor.get(f"{line_no}.0", f"{line_no}.end")
                if line_content.strip():
                    self.editor.tag_add(tag, f"{line_no}.0", f"{line_no}.end")
            except:
                pass
    
    def _first_string_pos(self, line):
        for i, ch in enumerate(line):
            if ch in ('"', "'"):
                return i
        return -1
    
    # ─────────────────────────────────────
    # SATIR NUMARALARI
    # ─────────────────────────────────────
    def _update_lineno(self, event=None):
        self.lineno.config(state="normal")
        self.lineno.delete("1.0", "end")
        count = int(self.editor.index("end-1c").split(".")[0])
        nums = "\n".join(str(n) for n in range(1, count + 1))
        self.lineno.insert("1.0", nums)
        self.lineno.config(state="disabled")
        
        # Cursor pozisyonu
        try:
            pos = self.editor.index("insert")
            row, col = pos.split(".")
            self.cursor_var.set(f"Satır {row}, Sütun {int(col)+1}")
        except:
            pass
    
    def _sync_scroll(self, *args):
        self.editor_vscroll.set(*args)
        self.lineno.yview_moveto(args[0])
    
    def _on_scroll(self, *args):
        self.editor.yview(*args)
        self.lineno.yview(*args)
    
    # ─────────────────────────────────────
    # TUSLAMA OLAYLARI
    # ─────────────────────────────────────
    def _on_key_release(self, event=None):
        self.saved = False
        self._update_title()
        self._update_lineno()
        
        # Debounce highlight
        if self.highlight_job:
            self.root.after_cancel(self.highlight_job)
        self.highlight_job = self.root.after(120, self._highlight_syntax)
        
        # Debounce diagnostics
        if self.diag_job:
            self.root.after_cancel(self.diag_job)
        self.diag_job = self.root.after(400, self._run_diagnostics)
    
    def _run_diagnostics(self):
        code = self.editor.get("1.0", "end-1c")
        self.diagnostics = analyze_tsharp(code)
        self._update_diag_panel()
        self._highlight_syntax()
    
    def _update_diag_panel(self):
        T = self.T
        self.diag_list.delete(0, "end")
        
        errors   = sum(1 for d in self.diagnostics if d[1] == "error")
        warnings = sum(1 for d in self.diagnostics if d[1] == "warning")
        
        count_str = ""
        if errors:   count_str += f"{errors} hata  "
        if warnings: count_str += f"{warnings} uyarı"
        if not self.diagnostics: count_str = "Sorun yok"
        self.diag_count_var.set(count_str)
        
        severity_icons = {"error": "E", "warning": "U", "info": "B"}
        severity_colors = {
            "error":   T["diag_error"],
            "warning": T["diag_warning"],
            "info":    T["diag_info"],
        }
        
        self._diag_colors = []
        for (line_no, severity, msg) in self.diagnostics:
            icon = severity_icons.get(severity, "?")
            text = f"  [{icon}] Sat.{line_no}: {msg}"
            if len(text) > 52:
                text = text[:49] + "..."
            self.diag_list.insert("end", text)
            self._diag_colors.append(severity_colors.get(severity, T["fg"]))
        
        for idx, color in enumerate(self._diag_colors):
            self.diag_list.itemconfig(idx, foreground=color)
    
    def _diag_goto_line(self, event=None):
        sel = self.diag_list.curselection()
        if not sel:
            return
        idx = sel[0]
        if idx < len(self.diagnostics):
            line_no = self.diagnostics[idx][0]
            self.editor.see(f"{line_no}.0")
            self.editor.mark_set("insert", f"{line_no}.0")
            self.editor.focus_set()
    
    # ─────────────────────────────────────
    # SIDEBAR - DOSYA GEZGİNİ
    # ─────────────────────────────────────
    def _load_sidebar_dir(self, path):
        self.file_tree.delete(*self.file_tree.get_children())
        self._sidebar_path = path
        self._populate_tree("", path)
    
    def _populate_tree(self, parent, path):
        try:
            entries = sorted(os.scandir(path), key=lambda e: (not e.is_dir(), e.name.lower()))
        except PermissionError:
            return
        
        for entry in entries:
            if entry.name.startswith("."):
                continue
            is_dir = entry.is_dir()
            is_tsh = entry.name.endswith((".tsh", ".tsharp"))
            
            if is_dir or is_tsh:
                prefix = "D " if is_dir else "  "
                node = self.file_tree.insert(parent, "end", text=f"{prefix}{entry.name}",
                                              values=(entry.path,), open=False)
                if is_dir:
                    # yer tutucu
                    self.file_tree.insert(node, "end", text="__placeholder__", values=("",))
        
        self.file_tree.bind("<<TreeviewOpen>>", self._on_tree_open)
    
    def _on_tree_open(self, event):
        node = self.file_tree.focus()
        children = self.file_tree.get_children(node)
        if len(children) == 1 and self.file_tree.item(children[0], "text") == "__placeholder__":
            self.file_tree.delete(children[0])
            path = self.file_tree.item(node, "values")[0]
            if path:
                self._populate_tree(node, path)
    
    def _sidebar_click(self, event):
        pass
    
    def _sidebar_double_click(self, event):
        node = self.file_tree.focus()
        vals = self.file_tree.item(node, "values")
        if not vals or not vals[0]:
            return
        path = vals[0]
        if os.path.isfile(path) and path.endswith((".tsh", ".tsharp")):
            self._open_path(path)
    
    # ─────────────────────────────────────
    # DOSYA İŞLEMLERİ
    # ─────────────────────────────────────
    def _new_file(self):
        if not self._confirm_discard():
            return
        self.editor.delete("1.0", "end")
        self.current_file = None
        self.saved = True
        self.title_var.set("adsiz.tsh")
        self.root.title("TSharp GO - adsiz.tsh")
        self._clear_diagnostics()
        self._update_lineno()
        self._highlight_syntax()
    
    def _open_file(self):
        if not self._confirm_discard():
            return
        path = filedialog.askopenfilename(
            title="Dosya Aç",
            filetypes=[("T# Dosyaları", "*.tsh *.tsharp"), ("Tüm Dosyalar", "*.*")]
        )
        if path:
            self._open_path(path)
    
    def _open_path(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.editor.delete("1.0", "end")
            self.editor.insert("1.0", content)
            self.current_file = path
            self.saved = True
            name = os.path.basename(path)
            self.title_var.set(name)
            self.root.title(f"TSharp GO - {name}")
            self._run_diagnostics()
            self._update_lineno()
            self._highlight_syntax()
            self.status_var.set(f"Açıldı: {path}")
        except Exception as ex:
            messagebox.showerror("Hata", f"Dosya okunamadı:\n{ex}")
    
    def _save_file(self):
        if self.current_file is None:
            self._save_as()
            return
        self._write_file(self.current_file)
    
    def _save_as(self):
        path = filedialog.asksaveasfilename(
            title="Farklı Kaydet",
            defaultextension=".tsh",
            filetypes=[("T# Dosyası", "*.tsh"), ("T# Uzun", "*.tsharp"), ("Tüm Dosyalar", "*.*")]
        )
        if path:
            self.current_file = path
            self._write_file(path)
    
    def _write_file(self, path):
        try:
            content = self.editor.get("1.0", "end-1c")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            self.saved = True
            name = os.path.basename(path)
            self.title_var.set(name)
            self.root.title(f"TSharp GO - {name}")
            self.status_var.set(f"Kaydedildi: {path}")
        except Exception as ex:
            messagebox.showerror("Hata", f"Dosya kaydedilemedi:\n{ex}")
    
    def _confirm_discard(self):
        if not self.saved:
            ans = messagebox.askyesnocancel(
                "Kaydedilmemiş Değişiklikler",
                "Dosyada kaydedilmemiş değişiklikler var. Devam etmek istiyor musunuz?"
            )
            if ans is None:
                return False
            if ans:
                self._save_file()
        return True
    
    def _update_title(self):
        base = os.path.basename(self.current_file) if self.current_file else "adsiz.tsh"
        marker = " *" if not self.saved else ""
        self.title_var.set(base + marker)
        self.root.title(f"TSharp GO - {base}{marker}")
    
    def _clear_diagnostics(self):
        self.diagnostics = []
        self._update_diag_panel()
    
    # ─────────────────────────────────────
    # TERMINAL
    # ─────────────────────────────────────
    def _terminal_write(self, text, tag="stdout"):
        self.terminal.config(state="normal")
        self.terminal.insert("end", text, tag)
        self.terminal.see("end")
        self.terminal.config(state="disabled")
    
    def _clear_terminal(self):
        self.terminal.config(state="normal")
        self.terminal.delete("1.0", "end")
        self.terminal.config(state="disabled")
    
    # ─────────────────────────────────────
    # ÇALIŞTIR
    # ─────────────────────────────────────
    def _run(self):
        if not self._save_before_run():
            return
        
        tsharp_cmd = shutil.which("tsharp")
        if tsharp_cmd is None:
            self._show_download_popup(
                "TSharp Bulunamadı",
                "TSharp çalıştırıcısı sisteminizde bulunamadı.\nTSharp'i indirmek için aşağıdaki düğmeye basın:",
                "TSharp İndir",
                "https://github.com/Artfical/TSharp/releases"
            )
            return
        
        cmd = [tsharp_cmd, self.current_file]
        cmd_str = " ".join(cmd)
        self._clear_terminal()
        self._terminal_write(f"> {cmd_str}\n", "cmd")
        self.status_var.set("Çalıştırılıyor...")
        
        threading.Thread(target=self._exec_cmd, args=(cmd,), daemon=True).start()
    
    # ─────────────────────────────────────
    # DERLE
    # ─────────────────────────────────────
    def _compile(self):
        if not self._save_before_run():
            return
        
        compile_cmd = shutil.which("tcompile") or shutil.which("derle")
        if compile_cmd is None:
            self._show_download_popup(
                "TCompile Bulunamadı",
                "TCompile derleyicisi sisteminizde bulunamadı.\nTCompile'i indirmek için aşağıdaki düğmeye basın:",
                "TCompile İndir",
                "https://github.com/Artfical/TCompile/releases"
            )
            return
        
        cmd = [compile_cmd, "--tekdosya", self.current_file]
        cmd_str = " ".join(cmd)
        self._clear_terminal()
        self._terminal_write(f"> {cmd_str}\n", "cmd")
        self.status_var.set("Derleniyor...")
        
        threading.Thread(target=self._exec_cmd, args=(cmd,), daemon=True).start()
    
    def _save_before_run(self):
        if self.current_file is None:
            path = filedialog.asksaveasfilename(
                title="Önce Dosyayı Kaydedin",
                defaultextension=".tsh",
                filetypes=[("T# Dosyası", "*.tsh"), ("T# Uzun", "*.tsharp")]
            )
            if not path:
                return False
            self.current_file = path
            self._write_file(path)
        elif not self.saved:
            self._save_file()
        return True
    
    def _exec_cmd(self, cmd):
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            
            def read_stream(stream, tag):
                for line in iter(stream.readline, ""):
                    self.root.after(0, self._terminal_write, line, tag)
                stream.close()
            
            t_out = threading.Thread(target=read_stream, args=(proc.stdout, "stdout"), daemon=True)
            t_err = threading.Thread(target=read_stream, args=(proc.stderr, "stderr"), daemon=True)
            t_out.start()
            t_err.start()
            t_out.join()
            t_err.join()
            
            ret = proc.wait()
            msg = f"\n[Islem tamamlandi, çıkış kodu: {ret}]\n"
            tag = "info" if ret == 0 else "stderr"
            self.root.after(0, self._terminal_write, msg, tag)
            self.root.after(0, self.status_var.set, "Hazır" if ret == 0 else f"Hata (kod {ret})")
        
        except Exception as ex:
            self.root.after(0, self._terminal_write, f"\n[Hata: {ex}]\n", "stderr")
            self.root.after(0, self.status_var.set, "Hata")
    
    # ─────────────────────────────────────
    # DOWNLOAD POPUP
    # ─────────────────────────────────────
    def _show_download_popup(self, title, message, btn_text, url):
        T = self.T
        
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.resizable(False, False)
        popup.grab_set()
        popup.config(bg=T["panel_bg"])
        
        # Lisans bilgisi
        license_frame = tk.Frame(popup, bg=T["sidebar_bg"])
        license_frame.pack(fill="x", padx=0, pady=0)
        
        license_text = "TSharp ve diğer tüm Artfical ürünlerini kullanarak GNU AGPL v3 lisansını kabul edersiniz."
        lbl_license = tk.Label(license_frame, text=license_text, font=self.font_sidebar,
                                bg=T["sidebar_bg"], fg=T["fg_dim"], wraplength=380, pady=6, padx=12)
        lbl_license.pack(side="left")
        
        gnu_link = tk.Label(license_frame, text="GNU AGPL v3", font=self.font_sidebar,
                             bg=T["sidebar_bg"], fg=T["accent"], cursor="hand2")
        gnu_link.pack(side="left", padx=(0, 12))
        gnu_link.bind("<Button-1>", lambda e: webbrowser.open("https://www.gnu.org/licenses/agpl-3.0.html"))
        
        # İçerik
        content_frame = tk.Frame(popup, bg=T["panel_bg"])
        content_frame.pack(fill="both", expand=True, padx=24, pady=20)
        
        lbl_title = tk.Label(content_frame, text=title, font=self.font_ui_bold,
                              bg=T["panel_bg"], fg=T["fg"])
        lbl_title.pack(anchor="w", pady=(0, 10))
        
        lbl_msg = tk.Label(content_frame, text=message, font=self.font_ui,
                            bg=T["panel_bg"], fg=T["fg"], wraplength=380, justify="left")
        lbl_msg.pack(anchor="w", pady=(0, 16))
        
        btn_download = tk.Button(
            content_frame, text=btn_text,
            font=self.font_ui_bold,
            bg=T["run_bg"], fg="#ffffff",
            bd=0, padx=14, pady=6, cursor="hand2",
            command=lambda: [webbrowser.open(url), popup.destroy()]
        )
        btn_download.pack(anchor="w")
        
        btn_close = tk.Button(
            content_frame, text="Kapat",
            font=self.font_ui,
            bg=T["btn_bg"], fg=T["btn_fg"],
            bd=0, padx=10, pady=4, cursor="hand2",
            command=popup.destroy
        )
        btn_close.pack(anchor="w", pady=(8, 0))
        
        # Ortala
        popup.update_idletasks()
        w, h = popup.winfo_width(), popup.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        popup.geometry(f"+{(sw-w)//2}+{(sh-h)//2}")


# ─────────────────────────────────────────────────────────────────────
# BAŞLANGIÇ
# ─────────────────────────────────────────────────────────────────────
def main():
    root = tk.Tk()
    root.title("TSharp GO")
    
    try:
        # Windows için DPI farkındalığı
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    app = TSharpGO(root)
    root.mainloop()


if __name__ == "__main__":
    main()
