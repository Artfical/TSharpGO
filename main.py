#!/usr/bin/env python3
"""
TSharp GO - TSharp Geliştirme Ortamı
GNU AGPL v3 Licensed
"""

import sys
import os
import re
import shutil
import threading
import subprocess
import webbrowser
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QPlainTextEdit, QListWidget, QListWidgetItem,
    QTreeWidget, QTreeWidgetItem, QLabel, QPushButton, QFrame,
    QFileDialog, QMessageBox, QDialog
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QSize, QRect
)
from PyQt6.QtGui import (
    QFont, QColor, QPainter, QTextCharFormat,
    QSyntaxHighlighter, QTextCursor, QAction,
    QPalette
)

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
        "syn_keyword":  "#ff7b72",
        "syn_string":   "#a5d6ff",
        "syn_number":   "#79c0ff",
        "syn_comment":  "#8b949e",
        "syn_function": "#d2a8ff",
        "syn_builtin":  "#ffa657",
        "syn_operator": "#ff7b72",
        "syn_boolean":  "#79c0ff",
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
        "syn_keyword":  "#cf222e",
        "syn_string":   "#0a3069",
        "syn_number":   "#0550ae",
        "syn_comment":  "#6e7781",
        "syn_function": "#8250df",
        "syn_builtin":  "#953800",
        "syn_operator": "#cf222e",
        "syn_boolean":  "#0550ae",
        "diag_error":   "#cf222e",
        "diag_warning": "#9a6700",
        "diag_info":    "#1a7f37",
        "diag_bg":      "#f6f8fa",
    }
}

# ─────────────────────────────────────────────────────────────────────
# T# SÖZ DİZİMİ TANIMLAMALARI
# ─────────────────────────────────────────────────────────────────────
TSHARP_KEYWORDS = [
    "degisken", "liste", "sozluk", "fonksiyon", "dondur", "son",
    "eger", "degilse", "dongu", "her", "icinde", "dur", "devam",
    "girdi", "yazdır", "yaz", "kullan", "ag", "gui", "gui6",
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
    open_blocks = []
    declared_vars = set()
    declared_funcs = set()
    KEYWORD_SET = set(TSHARP_KEYWORDS)
    BUILTIN_SET = set(TSHARP_BUILTINS)
    BOOLEAN_SET = set(TSHARP_BOOLEANS)
    ALL_KNOWN   = KEYWORD_SET | BUILTIN_SET | BOOLEAN_SET
    ml_open_char = ml_close_char = None
    ml_depth = 0

    for i, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if line.startswith("//") or line == "":
            continue
        if "//" in line:
            in_str = False; str_char = None
            for ci, ch in enumerate(line):
                if not in_str and ch in ('"', "'"):
                    in_str = True; str_char = ch
                elif in_str and ch == str_char:
                    in_str = False
                elif not in_str and ch == '/' and ci+1 < len(line) and line[ci+1] == '/':
                    line = line[:ci].strip(); break
        if ml_open_char is not None:
            for ch in line:
                if ch == ml_open_char: ml_depth += 1
                elif ch == ml_close_char: ml_depth -= 1
            if ml_depth <= 0:
                ml_open_char = ml_close_char = None; ml_depth = 0
            continue
        qd = line.count('"') - line.count('\\"')
        qs = line.count("'") - line.count("\\'")
        if qd % 2 != 0:
            diagnostics.append((i, "error", 'Kapatılmamış çift tırnak (") tespit edildi.'))
        if qs % 2 != 0:
            diagnostics.append((i, "error", "Kapatılmamış tek tırnak (') tespit edildi."))
        tokens = line.split()
        if not tokens: continue
        cmd = tokens[0].rstrip(":")

        if cmd in ("eger", "dongu", "her", "fonksiyon"):
            if cmd == "eger" and len(tokens) < 2:
                diagnostics.append((i, "error", "'eger' komutu bir koşul gerektirir."))
            if cmd == "dongu" and len(tokens) < 2:
                diagnostics.append((i, "error", "'dongu' komutu bir koşul gerektirir."))
            if cmd == "her" and "icinde" not in [t.rstrip(":") for t in tokens]:
                diagnostics.append((i, "error",
                    "'her' döngüsü 'icinde' anahtar kelimesini gerektirir. Örnek: her eleman icinde liste"))
            if cmd == "fonksiyon":
                if len(tokens) < 2:
                    diagnostics.append((i, "error", "'fonksiyon' bir isim gerektirir."))
                else:
                    declared_funcs.add(tokens[1].split("(")[0])
            open_blocks.append((cmd, i))
        elif cmd == "son":
            if not open_blocks:
                diagnostics.append((i, "error", "Eşleşmeyen 'son': Açık bir blok bulunamadı."))
            else:
                open_blocks.pop()
        elif cmd == "degilse":
            if not open_blocks or open_blocks[-1][0] != "eger":
                diagnostics.append((i, "error", "'degilse' yalnızca 'eger' bloğunun ardından gelebilir."))
        elif cmd == "degisken":
            if len(tokens) < 2:
                diagnostics.append((i, "error", "'degisken' komutu bir isim gerektirir."))
            else:
                vname = tokens[1]
                if len(tokens) < 4 or tokens[2] != "=":
                    diagnostics.append((i, "warning",
                        f"'{vname}' değişkeni atama olmadan tanımlanmış olabilir. '=' operatörü bekleniyor."))
                declared_vars.add(vname)
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
                        ob, cb = rest.count("["), rest.count("]")
                        if ob != cb:
                            ml_open_char = "["; ml_close_char = "]"; ml_depth = ob - cb
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
                        ob, cb = rest.count("{"), rest.count("}")
                        if ob != cb:
                            ml_open_char = "{"; ml_close_char = "}"; ml_depth = ob - cb
        elif cmd in ("yazdır", "yaz"):
            pass
        elif cmd == "girdi":
            if len(tokens) < 2:
                diagnostics.append((i, "error", "'girdi' komutu bir değişken ismi gerektirir."))
            else:
                declared_vars.add(tokens[1])
        elif cmd == "dondur":
            if not any(b[0] == "fonksiyon" for b in open_blocks):
                diagnostics.append((i, "warning", "'dondur' komutu bir fonksiyon dışında kullanılmış."))
        elif cmd in ("dur", "devam"):
            if not any(b[0] in ("dongu", "her") for b in open_blocks):
                diagnostics.append((i, "warning", f"'{cmd}' komutu bir döngü dışında kullanılmış."))
        elif cmd == "kullan":
            if len(tokens) < 2:
                diagnostics.append((i, "error", "'kullan' komutu bir modül ismi gerektirir. Örnek: kullan ag"))
            else:
                modul = tokens[1]
                if modul not in ("ag", "gui", "gui6"):
                    diagnostics.append((i, "warning",
                        f"Bilinmeyen modül: '{modul}'. Geçerli modüller: ag, gui, gui6"))
        elif cmd not in ALL_KNOWN:
            if re.match(r'^[a-zA-Z_\u00c0-\u024f][a-zA-Z0-9_\u00c0-\u024f]*$', cmd):
                if cmd not in declared_vars and cmd not in declared_funcs:
                    diagnostics.append((i, "error",
                        f"Bilinmeyen komut veya tanımlanmamış değişken: '{cmd}'. "
                        f"Bir değişken ise 'degisken {cmd} = ...' ile tanımlayın."))

        if re.search(r'\bprint\s*\(', line):
            diagnostics.append((i, "warning",
                "Python 'print()' kullanımı tespit edildi. T#'da 'yazdır' veya 'yaz' kullanın."))
        if re.match(r'^(for|if|while|def|class|import|from|return)\b', line):
            pkw = tokens[0]
            eq = {"for": "her ... icinde ...", "if": "eger", "while": "dongu",
                  "def": "fonksiyon", "return": "dondur", "import": "kullan"}.get(pkw, "")
            hint = f" T#'da '{eq}' kullanın." if eq else ""
            diagnostics.append((i, "warning", f"Python anahtar kelimesi '{pkw}' tespit edildi.{hint}"))

    for blk_type, blk_line in open_blocks:
        diagnostics.append((blk_line, "error", f"'{blk_type}' bloğu kapatılmamış: 'son' eksik."))

    return diagnostics


# ─────────────────────────────────────────────────────────────────────
# SYNTAX HIGHLIGHTER
# ─────────────────────────────────────────────────────────────────────
class TSharpHighlighter(QSyntaxHighlighter):
    def __init__(self, document, theme):
        super().__init__(document)
        self.theme = theme
        self._diag_lines = {}
        self._rules = []
        self._comment_fmt = None
        self._string_fmt = None
        self._diag_fmt = {}
        self._build_rules()

    def _fmt(self, color, italic=False, underline=False, ul_color=None):
        f = QTextCharFormat()
        f.setForeground(QColor(color))
        if italic: f.setFontItalic(True)
        if underline:
            f.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SingleUnderline)
            if ul_color: f.setUnderlineColor(QColor(ul_color))
        return f

    def _build_rules(self):
        T = self.theme
        self._rules = []
        self._comment_fmt = self._fmt(T["syn_comment"], italic=True)
        self._string_fmt  = self._fmt(T["syn_string"])

        self._rules.append((re.compile(r'\b\d+\.?\d*\b'), self._fmt(T["syn_number"])))
        self._rules.append((re.compile(r'(\+\+|--|==|!=|<=|>=|[+\-*/%=<>!])'),
                             self._fmt(T["syn_operator"])))

        kw = r'\b(' + '|'.join(re.escape(k) for k in TSHARP_KEYWORDS) + r')\b'
        bl = r'\b(' + '|'.join(re.escape(k) for k in TSHARP_BUILTINS) + r')\b'
        bo = r'\b(' + '|'.join(re.escape(k) for k in TSHARP_BOOLEANS) + r')\b'
        self._rules.append((re.compile(kw), self._fmt(T["syn_keyword"])))
        self._rules.append((re.compile(bl), self._fmt(T["syn_builtin"])))
        self._rules.append((re.compile(bo), self._fmt(T["syn_boolean"])))

        self._diag_fmt = {
            "error":   self._fmt(T["diag_error"],   underline=True, ul_color=T["diag_error"]),
            "warning": self._fmt(T["diag_warning"], underline=True, ul_color=T["diag_warning"]),
            "info":    self._fmt(T["diag_info"],    underline=True, ul_color=T["diag_info"]),
        }

    def set_theme(self, theme):
        self.theme = theme
        self._build_rules()
        self.rehighlight()

    def set_diagnostics(self, diag_list):
        self._diag_lines = {ln - 1: sev for ln, sev, _ in diag_list}
        self.rehighlight()

    def highlightBlock(self, text):
        block_num = self.currentBlock().blockNumber()

        # Yorum başlangıcını bul
        comment_start = -1
        in_str = False; str_char = None
        for ci, ch in enumerate(text):
            if not in_str and ch in ('"', "'"):
                in_str = True; str_char = ch
            elif in_str and ch == str_char:
                in_str = False
            elif not in_str and ch == '/' and ci+1 < len(text) and text[ci+1] == '/':
                comment_start = ci; break

        # String'ler
        for m in re.finditer(r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', text):
            if comment_start >= 0 and m.start() >= comment_start:
                break
            self.setFormat(m.start(), m.end() - m.start(), self._string_fmt)

        # Diğer kurallar
        for pattern, fmt in self._rules:
            for m in pattern.finditer(text):
                if comment_start >= 0 and m.start() >= comment_start:
                    break
                self.setFormat(m.start(), m.end() - m.start(), fmt)

        # Yorum (son — üzerine yazar)
        if comment_start >= 0:
            self.setFormat(comment_start, len(text) - comment_start, self._comment_fmt)

        # Diagnostics altı çizgi
        if block_num in self._diag_lines and text.strip():
            sev = self._diag_lines[block_num]
            if sev in self._diag_fmt:
                self.setFormat(0, len(text), self._diag_fmt[sev])


# ─────────────────────────────────────────────────────────────────────
# SATIR NUMARASI PANELİ
# ─────────────────────────────────────────────────────────────────────
class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor._line_area_width(), 0)

    def paintEvent(self, event):
        self.editor._paint_line_numbers(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self, theme, parent=None):
        super().__init__(parent)
        self.theme = theme
        self._line_area = LineNumberArea(self)
        self.blockCountChanged.connect(self._update_line_area_width)
        self.updateRequest.connect(self._update_line_area)
        self._update_line_area_width()
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setTabStopDistance(40)

    def _line_area_width(self):
        digits = max(1, len(str(max(1, self.blockCount()))))
        return 10 + self.fontMetrics().horizontalAdvance('9') * (digits + 1)

    def _update_line_area_width(self):
        self.setViewportMargins(self._line_area_width(), 0, 0, 0)

    def _update_line_area(self, rect, dy):
        if dy:
            self._line_area.scroll(0, dy)
        else:
            self._line_area.update(0, rect.y(), self._line_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self._update_line_area_width()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self._line_area.setGeometry(QRect(cr.left(), cr.top(),
                                          self._line_area_width(), cr.height()))

    def _paint_line_numbers(self, event):
        T = self.theme
        painter = QPainter(self._line_area)
        painter.fillRect(event.rect(), QColor(T["sidebar_bg"]))
        painter.setPen(QColor(T["line_no"]))
        painter.setFont(self.font())

        block = self.firstVisibleBlock()
        block_num = block.blockNumber()
        top    = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.drawText(0, top,
                                 self._line_area.width() - 4,
                                 self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight,
                                 str(block_num + 1))
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_num += 1

    def set_theme(self, theme):
        self.theme = theme
        self._line_area.update()

    def get_cursor_pos(self):
        c = self.textCursor()
        return c.blockNumber() + 1, c.columnNumber() + 1


# ─────────────────────────────────────────────────────────────────────
# RUN THREAD
# ─────────────────────────────────────────────────────────────────────
class RunThread(QThread):
    output   = pyqtSignal(str, str)
    finished = pyqtSignal(int)

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd

    def run(self):
        try:
            proc = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, encoding="utf-8", errors="replace")
            def rd(stream, tag):
                for line in iter(stream.readline, ""):
                    self.output.emit(line, tag)
                stream.close()
            t1 = threading.Thread(target=rd, args=(proc.stdout, "stdout"), daemon=True)
            t2 = threading.Thread(target=rd, args=(proc.stderr, "stderr"), daemon=True)
            t1.start(); t2.start(); t1.join(); t2.join()
            self.finished.emit(proc.wait())
        except Exception as ex:
            self.output.emit(f"\n[Hata: {ex}]\n", "stderr")
            self.finished.emit(1)


# ─────────────────────────────────────────────────────────────────────
# DOWNLOAD POPUP
# ─────────────────────────────────────────────────────────────────────
class DownloadPopup(QDialog):
    def __init__(self, parent, title, message, btn_text, url, T):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedWidth(440)
        self.setModal(True)
        self.setStyleSheet(f"QDialog {{ background: {T['panel_bg']}; }} QLabel {{ color: {T['fg']}; }}")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Lisans bandı
        bar = QFrame()
        bar.setStyleSheet(f"background: {T['sidebar_bg']};")
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(12, 6, 12, 6)
        lic = QLabel("TSharp ve diğer tüm Artfical ürünlerini kullanarak GNU AGPL v3 lisansını kabul edersiniz.")
        lic.setStyleSheet(f"color: {T['fg_dim']}; font-size: 9px;")
        lic.setWordWrap(True)
        bl.addWidget(lic)
        gnu = QPushButton("GNU AGPL v3")
        gnu.setStyleSheet(f"QPushButton {{ background: transparent; color: {T['accent']}; border: none; font-size: 9px; }}")
        gnu.setCursor(Qt.CursorShape.PointingHandCursor)
        gnu.clicked.connect(lambda: webbrowser.open("https://www.gnu.org/licenses/agpl-3.0.html"))
        bl.addWidget(gnu)
        lay.addWidget(bar)

        # İçerik
        cnt = QWidget()
        cnt.setStyleSheet(f"background: {T['panel_bg']};")
        cl = QVBoxLayout(cnt)
        cl.setContentsMargins(24, 20, 24, 20)
        cl.setSpacing(10)
        tl = QLabel(title)
        tl.setStyleSheet(f"color: {T['fg']}; font-weight: bold; font-size: 11px;")
        cl.addWidget(tl)
        ml = QLabel(message)
        ml.setStyleSheet(f"color: {T['fg']}; font-size: 10px;")
        ml.setWordWrap(True)
        cl.addWidget(ml)
        db = QPushButton(btn_text)
        db.setStyleSheet(f"QPushButton {{ background: {T['run_bg']}; color: #fff; border: none; padding: 6px 14px; border-radius: 4px; font-weight: bold; }} QPushButton:hover {{ background: {T['run_hover']}; }}")
        db.setCursor(Qt.CursorShape.PointingHandCursor)
        db.clicked.connect(lambda: [webbrowser.open(url), self.accept()])
        cl.addWidget(db, alignment=Qt.AlignmentFlag.AlignLeft)
        cb = QPushButton("Kapat")
        cb.setStyleSheet(f"QPushButton {{ background: {T['btn_bg']}; color: {T['btn_fg']}; border: none; padding: 4px 10px; border-radius: 4px; }} QPushButton:hover {{ background: {T['btn_hover']}; }}")
        cb.setCursor(Qt.CursorShape.PointingHandCursor)
        cb.clicked.connect(self.reject)
        cl.addWidget(cb, alignment=Qt.AlignmentFlag.AlignLeft)
        lay.addWidget(cnt)


# ─────────────────────────────────────────────────────────────────────
# ANA IDE
# ─────────────────────────────────────────────────────────────────────
class TSharpGO(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TSharp GO")
        self.resize(1400, 850)
        self.setMinimumSize(900, 600)

        self.current_theme = "dark"
        self.T = THEMES["dark"]
        self.current_file = None
        self.saved = True
        self.diagnostics = []
        self._run_thread = None

        self._hl_timer   = QTimer(self); self._hl_timer.setSingleShot(True)
        self._diag_timer = QTimer(self); self._diag_timer.setSingleShot(True)
        self._hl_timer.timeout.connect(self._highlight_syntax)
        self._diag_timer.timeout.connect(self._run_diagnostics)

        self._build_ui()
        self._build_menu()
        self._apply_theme()
        self._load_sidebar_dir(str(Path.home()))
        self._new_file()

    # ── UI ──────────────────────────────────────────────────────────
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root_lay = QVBoxLayout(central)
        root_lay.setContentsMargins(0, 0, 0, 0)
        root_lay.setSpacing(0)

        # Toolbar
        self._build_toolbar(root_lay)

        # Ana splitter
        self.splitter_main = QSplitter(Qt.Orientation.Horizontal)
        self.splitter_main.setHandleWidth(4)
        root_lay.addWidget(self.splitter_main)

        # Sidebar
        self._build_sidebar()

        # Orta: editör+terminal | diagnostics
        center_sp = QSplitter(Qt.Orientation.Horizontal)
        center_sp.setHandleWidth(4)
        self.splitter_center = center_sp

        edit_sp = QSplitter(Qt.Orientation.Vertical)
        edit_sp.setHandleWidth(4)
        self.splitter_edit = edit_sp

        self._build_editor();   edit_sp.addWidget(self.editor_container)
        self._build_terminal(); edit_sp.addWidget(self.terminal_container)
        edit_sp.setStretchFactor(0, 3)
        edit_sp.setStretchFactor(1, 1)

        center_sp.addWidget(edit_sp)
        center_sp.setStretchFactor(0, 4)

        self._build_diag_panel()
        center_sp.addWidget(self.diag_container)
        center_sp.setStretchFactor(1, 1)

        self.splitter_main.addWidget(center_sp)
        self.splitter_main.setSizes([210, 1190])

        self._build_statusbar()

    def _build_toolbar(self, parent_lay):
        self.toolbar_widget = QFrame()
        self.toolbar_widget.setFixedHeight(44)
        tl = QHBoxLayout(self.toolbar_widget)
        tl.setContentsMargins(8, 6, 8, 6)
        tl.setSpacing(4)

        self.btn_new  = self._mkbtn("Yeni",      self._new_file)
        self.btn_open = self._mkbtn("Aç",        self._open_file)
        self.btn_save = self._mkbtn("Kaydet",    self._save_file)
        for b in [self.btn_new, self.btn_open, self.btn_save]:
            tl.addWidget(b)

        self.title_label = QLabel("adsiz.tsh")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        tl.addWidget(self.title_label)
        tl.addStretch()

        self.btn_theme   = self._mkbtn("Açık Tema",  self._toggle_theme)
        self.sep_frame   = QFrame(); self.sep_frame.setFrameShape(QFrame.Shape.VLine); self.sep_frame.setFixedWidth(1)
        self.btn_compile = self._mkbtn("Derle",      self._compile,  kind="compile")
        self.btn_run     = self._mkbtn("Çalıştır",   self._run,      kind="run")
        for w in [self.btn_theme, self.sep_frame, self.btn_compile, self.btn_run]:
            tl.addWidget(w)

        parent_lay.addWidget(self.toolbar_widget)

    def _mkbtn(self, text, slot, kind="normal"):
        b = QPushButton(text)
        b.setFont(QFont("Segoe UI", 10))
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.setFixedHeight(28)
        b.setProperty("kind", kind)
        b.clicked.connect(slot)
        return b

    def _build_sidebar(self):
        sw = QWidget()
        sw.setMinimumWidth(140); sw.setMaximumWidth(350)
        sl = QVBoxLayout(sw); sl.setContentsMargins(0, 0, 0, 0); sl.setSpacing(0)

        self.sidebar_hdr = QFrame(); self.sidebar_hdr.setFixedHeight(32)
        hl = QHBoxLayout(self.sidebar_hdr); hl.setContentsMargins(10, 0, 0, 0)
        self.sidebar_title = QLabel("DOSYA GEZGİNİ")
        self.sidebar_title.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        hl.addWidget(self.sidebar_title)
        sl.addWidget(self.sidebar_hdr)

        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderHidden(True)
        self.file_tree.setFont(QFont("Segoe UI", 9))
        self.file_tree.itemDoubleClicked.connect(self._sidebar_double_click)
        self.file_tree.itemExpanded.connect(self._on_tree_expand)
        sl.addWidget(self.file_tree)

        self.splitter_main.addWidget(sw)
        self.sidebar_widget = sw

    def _build_editor(self):
        self.editor_container = QWidget()
        el = QVBoxLayout(self.editor_container); el.setContentsMargins(0,0,0,0); el.setSpacing(0)
        self.editor = CodeEditor(self.T)
        self.editor.setFont(QFont("Courier New", 13))
        self.editor.textChanged.connect(self._on_text_changed)
        self.editor.cursorPositionChanged.connect(self._update_cursor_pos)
        self.highlighter = TSharpHighlighter(self.editor.document(), self.T)
        el.addWidget(self.editor)

    def _build_terminal(self):
        self.terminal_container = QWidget()
        tl = QVBoxLayout(self.terminal_container); tl.setContentsMargins(0,0,0,0); tl.setSpacing(0)

        self.term_hdr = QFrame(); self.term_hdr.setFixedHeight(28)
        th = QHBoxLayout(self.term_hdr); th.setContentsMargins(10,0,8,0)
        self.term_title_lbl = QLabel("TERMINAL")
        self.term_title_lbl.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        th.addWidget(self.term_title_lbl); th.addStretch()
        self.btn_clear_term = QPushButton("Temizle")
        self.btn_clear_term.setFont(QFont("Segoe UI", 9))
        self.btn_clear_term.setFixedHeight(22)
        self.btn_clear_term.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_clear_term.clicked.connect(self._clear_terminal)
        th.addWidget(self.btn_clear_term)
        tl.addWidget(self.term_hdr)

        self.terminal = QPlainTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setFont(QFont("Courier New", 11))
        self.terminal.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        tl.addWidget(self.terminal)

    def _build_diag_panel(self):
        self.diag_container = QWidget()
        self.diag_container.setMinimumWidth(180)
        dl = QVBoxLayout(self.diag_container); dl.setContentsMargins(0,0,0,0); dl.setSpacing(0)

        self.diag_hdr = QFrame(); self.diag_hdr.setFixedHeight(32)
        dh = QHBoxLayout(self.diag_hdr); dh.setContentsMargins(10,0,8,0)
        self.diag_title_lbl = QLabel("SORUNLAR")
        self.diag_title_lbl.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        dh.addWidget(self.diag_title_lbl); dh.addStretch()
        self.diag_count_lbl = QLabel("")
        self.diag_count_lbl.setFont(QFont("Segoe UI", 9))
        dh.addWidget(self.diag_count_lbl)
        dl.addWidget(self.diag_hdr)

        self.diag_list = QListWidget()
        self.diag_list.setFont(QFont("Segoe UI", 9))
        self.diag_list.itemClicked.connect(self._diag_goto_line)
        dl.addWidget(self.diag_list)

    def _build_statusbar(self):
        sb = self.statusBar(); sb.setFixedHeight(22)
        self.status_lbl = QLabel("Hazır"); self.status_lbl.setFont(QFont("Segoe UI", 9))
        self.cursor_lbl = QLabel("Satır 1, Sütun 1"); self.cursor_lbl.setFont(QFont("Segoe UI", 9))
        sb.addWidget(self.status_lbl)
        sb.addPermanentWidget(self.cursor_lbl)
        self.status_bar = sb

    def _build_menu(self):
        mb = self.menuBar()

        fm = mb.addMenu("Dosya")
        self._act(fm, "Yeni",          self._new_file,   "Ctrl+N")
        self._act(fm, "Aç",            self._open_file,  "Ctrl+O")
        self._act(fm, "Kaydet",        self._save_file,  "Ctrl+S")
        self._act(fm, "Farklı Kaydet", self._save_as)
        fm.addSeparator()
        self._act(fm, "Çıkış",         self.close)

        em = mb.addMenu("Düzenle")
        self._act(em, "Geri Al", self.editor.undo, "Ctrl+Z")
        self._act(em, "Yinele",  self.editor.redo, "Ctrl+Y")

        vm = mb.addMenu("Görünüm")
        self._act(vm, "Karanlık Tema", lambda: self._switch_theme("dark"))
        self._act(vm, "Açık Tema",     lambda: self._switch_theme("light"))

        hm = mb.addMenu("Yardım")
        self._act(hm, "TSharp Hakkında",
                  lambda: webbrowser.open("https://github.com/Artfical/TSharp"))

    def _act(self, menu, text, slot, shortcut=None):
        a = QAction(text, self)
        if shortcut: a.setShortcut(shortcut)
        a.triggered.connect(slot)
        menu.addAction(a)

    # ── TEMA ────────────────────────────────────────────────────────
    def _apply_theme(self):
        T = self.T

        self.setStyleSheet(f"""
            QMainWindow, QWidget {{ background: {T['bg']}; color: {T['fg']}; }}
            QMenuBar {{ background: {T['panel_bg']}; color: {T['fg']}; border: none; padding: 2px; }}
            QMenuBar::item:selected {{ background: {T['accent']}; color: #ffffff; border-radius: 3px; }}
            QMenu {{ background: {T['panel_bg']}; color: {T['fg']}; border: 1px solid {T['border']}; }}
            QMenu::item:selected {{ background: {T['accent']}; color: #ffffff; }}
            QSplitter::handle {{ background: {T['border']}; }}
            QScrollBar:vertical {{ background: {T['panel_bg']}; width: 10px; border: none; margin: 0; }}
            QScrollBar::handle:vertical {{ background: {T['scrollbar']}; border-radius: 4px; min-height: 20px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; border: none; }}
            QScrollBar:horizontal {{ background: {T['panel_bg']}; height: 10px; border: none; margin: 0; }}
            QScrollBar::handle:horizontal {{ background: {T['scrollbar']}; border-radius: 4px; min-width: 20px; }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; border: none; }}
            QStatusBar {{ background: {T['panel_bg']}; color: {T['fg_dim']}; border-top: 1px solid {T['border']}; }}
            QStatusBar::item {{ border: none; }}
        """)

        # Toolbar
        self.toolbar_widget.setStyleSheet(
            f"background: {T['panel_bg']}; border-bottom: 1px solid {T['border']};")
        self.title_label.setStyleSheet(f"color: {T['fg']}; background: transparent;")
        self.sep_frame.setStyleSheet(f"background: {T['border']};")

        ns = f"QPushButton {{ background: {T['btn_bg']}; color: {T['btn_fg']}; border: none; padding: 3px 10px; border-radius: 4px; }} QPushButton:hover {{ background: {T['btn_hover']}; }}"
        rs = f"QPushButton {{ background: {T['run_bg']}; color: #fff; border: none; padding: 3px 10px; border-radius: 4px; font-weight: bold; }} QPushButton:hover {{ background: {T['run_hover']}; }}"
        cs = f"QPushButton {{ background: {T['compile_bg']}; color: #fff; border: none; padding: 3px 10px; border-radius: 4px; font-weight: bold; }} QPushButton:hover {{ background: {T['compile_hover']}; }}"

        for b in [self.btn_new, self.btn_open, self.btn_save, self.btn_theme]:
            b.setStyleSheet(ns)
        self.btn_run.setStyleSheet(rs)
        self.btn_compile.setStyleSheet(cs)
        self.btn_theme.setText("Açık Tema" if self.current_theme == "dark" else "Karanlık Tema")

        # Sidebar
        self.sidebar_widget.setStyleSheet(f"background: {T['sidebar_bg']};")
        self.sidebar_hdr.setStyleSheet(f"background: {T['sidebar_bg']}; border-bottom: 1px solid {T['border']};")
        self.sidebar_title.setStyleSheet(f"color: {T['fg_dim']}; background: transparent;")
        self.file_tree.setStyleSheet(f"""
            QTreeWidget {{ background: {T['sidebar_bg']}; color: {T['fg']}; border: none; outline: none; }}
            QTreeWidget::item:selected {{ background: {T['sel_bg']}; color: {T['fg']}; }}
            QTreeWidget::item:hover {{ background: {T['btn_hover']}; }}
        """)

        # Editör
        self.editor.setStyleSheet(f"""
            QPlainTextEdit {{ background: {T['editor_bg']}; color: {T['fg']};
                              border: none; selection-background-color: {T['sel_bg']}; }}
        """)
        p = self.editor.palette()
        p.setColor(QPalette.ColorRole.Base, QColor(T["editor_bg"]))
        p.setColor(QPalette.ColorRole.Text, QColor(T["fg"]))
        self.editor.setPalette(p)
        self.editor.setCursorWidth(2)
        self.editor.set_theme(T)

        # Terminal
        self.terminal_container.setStyleSheet(f"background: {T['terminal_bg']};")
        self.term_hdr.setStyleSheet(f"background: {T['panel_bg']}; border-top: 1px solid {T['border']};")
        self.term_title_lbl.setStyleSheet(f"color: {T['fg_dim']}; background: transparent;")
        self.terminal.setStyleSheet(
            f"QPlainTextEdit {{ background: {T['terminal_bg']}; color: {T['fg']}; border: none; }}")
        self.btn_clear_term.setStyleSheet(
            f"QPushButton {{ background: {T['btn_bg']}; color: {T['btn_fg']}; border: none; padding: 2px 8px; border-radius: 3px; }} QPushButton:hover {{ background: {T['btn_hover']}; }}")

        # Diagnostics
        self.diag_container.setStyleSheet(f"background: {T['diag_bg']};")
        self.diag_hdr.setStyleSheet(f"background: {T['panel_bg']}; border-bottom: 1px solid {T['border']};")
        self.diag_title_lbl.setStyleSheet(f"color: {T['fg_dim']}; background: transparent;")
        self.diag_count_lbl.setStyleSheet(f"color: {T['fg_dim']}; background: transparent;")
        self.diag_list.setStyleSheet(f"""
            QListWidget {{ background: {T['diag_bg']}; color: {T['fg']}; border: none; outline: none; }}
            QListWidget::item:selected {{ background: {T['sel_bg']}; }}
            QListWidget::item:hover {{ background: {T['btn_hover']}; }}
        """)

        # Status bar
        self.status_bar.setStyleSheet(
            f"background: {T['panel_bg']}; color: {T['fg_dim']}; border-top: 1px solid {T['border']};")
        self.status_lbl.setStyleSheet(f"color: {T['fg_dim']}; background: transparent;")
        self.cursor_lbl.setStyleSheet(f"color: {T['fg_dim']}; background: transparent;")

        # Highlighter
        self.highlighter.set_theme(T)
        self.highlighter.set_diagnostics(self.diagnostics)

    def _switch_theme(self, name):
        self.current_theme = name
        self.T = THEMES[name]
        self._apply_theme()

    def _toggle_theme(self):
        self._switch_theme("light" if self.current_theme == "dark" else "dark")

    # ── SYNTAX / DIAG ────────────────────────────────────────────────
    def _highlight_syntax(self):
        self.highlighter.set_diagnostics(self.diagnostics)

    def _run_diagnostics(self):
        self.diagnostics = analyze_tsharp(self.editor.toPlainText())
        self._update_diag_panel()
        self.highlighter.set_diagnostics(self.diagnostics)

    def _update_diag_panel(self):
        T = self.T
        self.diag_list.clear()
        errors   = sum(1 for d in self.diagnostics if d[1] == "error")
        warnings = sum(1 for d in self.diagnostics if d[1] == "warning")

        if not self.diagnostics:
            self.diag_count_lbl.setText("Sorun yok")
        else:
            parts = []
            if errors:   parts.append(f"{errors} hata")
            if warnings: parts.append(f"{warnings} uyarı")
            self.diag_count_lbl.setText("  ".join(parts))

        icon_map  = {"error": "E", "warning": "U", "info": "B"}
        color_map = {"error": T["diag_error"], "warning": T["diag_warning"], "info": T["diag_info"]}

        for line_no, severity, msg in self.diagnostics:
            icon = icon_map.get(severity, "?")
            text = f"  [{icon}] Sat.{line_no}: {msg}"
            if len(text) > 52: text = text[:49] + "..."
            item = QListWidgetItem(text)
            item.setForeground(QColor(color_map.get(severity, T["fg"])))
            item.setData(Qt.ItemDataRole.UserRole, line_no)
            self.diag_list.addItem(item)

    def _diag_goto_line(self, item):
        line_no = item.data(Qt.ItemDataRole.UserRole)
        if line_no:
            block = self.editor.document().findBlockByNumber(line_no - 1)
            cur = self.editor.textCursor()
            cur.setPosition(block.position())
            self.editor.setTextCursor(cur)
            self.editor.ensureCursorVisible()
            self.editor.setFocus()

    # ── TEXT EVENTS ──────────────────────────────────────────────────
    def _on_text_changed(self):
        self.saved = False
        self._update_title()
        self._hl_timer.start(120)
        self._diag_timer.start(400)

    def _update_cursor_pos(self):
        ln, col = self.editor.get_cursor_pos()
        self.cursor_lbl.setText(f"Satır {ln}, Sütun {col}")

    # ── SIDEBAR ──────────────────────────────────────────────────────
    def _load_sidebar_dir(self, path):
        self.file_tree.clear()
        self._populate_tree(None, path)

    def _populate_tree(self, parent, path):
        try:
            entries = sorted(os.scandir(path), key=lambda e: (not e.is_dir(), e.name.lower()))
        except PermissionError:
            return
        for entry in entries:
            if entry.name.startswith("."): continue
            is_dir = entry.is_dir()
            is_tsh = entry.name.endswith((".tsh", ".tsharp"))
            if not (is_dir or is_tsh): continue
            prefix = "D " if is_dir else "  "
            item = QTreeWidgetItem([f"{prefix}{entry.name}"])
            item.setData(0, Qt.ItemDataRole.UserRole, entry.path)
            if is_dir:
                item.addChild(QTreeWidgetItem(["__placeholder__"]))
            if parent is None:
                self.file_tree.addTopLevelItem(item)
            else:
                parent.addChild(item)

    def _on_tree_expand(self, item):
        if item.childCount() == 1 and item.child(0).text(0) == "__placeholder__":
            item.removeChild(item.child(0))
            path = item.data(0, Qt.ItemDataRole.UserRole)
            if path: self._populate_tree(item, path)

    def _sidebar_double_click(self, item, col):
        path = item.data(0, Qt.ItemDataRole.UserRole)
        if path and os.path.isfile(path) and path.endswith((".tsh", ".tsharp")):
            self._open_path(path)

    # ── DOSYA İŞLEMLERİ ──────────────────────────────────────────────
    def _new_file(self):
        if not self._confirm_discard(): return
        self.editor.setPlainText("")
        self.current_file = None
        self.saved = True
        self.title_label.setText("adsiz.tsh")
        self.setWindowTitle("TSharp GO - adsiz.tsh")
        self.diagnostics = []
        self._update_diag_panel()
        self.highlighter.set_diagnostics([])

    def _open_file(self):
        if not self._confirm_discard(): return
        path, _ = QFileDialog.getOpenFileName(self, "Dosya Aç", "",
            "T# Dosyaları (*.tsh *.tsharp);;Tüm Dosyalar (*.*)")
        if path: self._open_path(path)

    def _open_path(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.editor.setPlainText(content)
            self.current_file = path; self.saved = True
            name = os.path.basename(path)
            self.title_label.setText(name)
            self.setWindowTitle(f"TSharp GO - {name}")
            self._run_diagnostics()
            self.status_lbl.setText(f"Açıldı: {path}")
        except Exception as ex:
            QMessageBox.critical(self, "Hata", f"Dosya okunamadı:\n{ex}")

    def _save_file(self):
        if self.current_file is None: self._save_as(); return
        self._write_file(self.current_file)

    def _save_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Farklı Kaydet", "",
            "T# Dosyası (*.tsh);;T# Uzun (*.tsharp);;Tüm Dosyalar (*.*)")
        if path: self.current_file = path; self._write_file(path)

    def _write_file(self, path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            self.saved = True
            name = os.path.basename(path)
            self.title_label.setText(name)
            self.setWindowTitle(f"TSharp GO - {name}")
            self.status_lbl.setText(f"Kaydedildi: {path}")
        except Exception as ex:
            QMessageBox.critical(self, "Hata", f"Dosya kaydedilemedi:\n{ex}")

    def _confirm_discard(self):
        if not self.saved:
            ans = QMessageBox.question(self, "Kaydedilmemiş Değişiklikler",
                "Dosyada kaydedilmemiş değişiklikler var. Devam etmek istiyor musunuz?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No |
                QMessageBox.StandardButton.Cancel)
            if ans == QMessageBox.StandardButton.Cancel: return False
            if ans == QMessageBox.StandardButton.Yes: self._save_file()
        return True

    def _update_title(self):
        base   = os.path.basename(self.current_file) if self.current_file else "adsiz.tsh"
        marker = " *" if not self.saved else ""
        self.title_label.setText(base + marker)
        self.setWindowTitle(f"TSharp GO - {base}{marker}")

    # ── TERMINAL ─────────────────────────────────────────────────────
    def _terminal_write(self, text, tag="stdout"):
        T = self.T
        colors = {"stdout": T["fg"], "stderr": T["diag_error"],
                  "info": T["diag_info"], "cmd": T["syn_function"]}
        cur = self.terminal.textCursor()
        cur.movePosition(QTextCursor.MoveOperation.End)
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(colors.get(tag, T["fg"])))
        cur.insertText(text, fmt)
        self.terminal.setTextCursor(cur)
        self.terminal.ensureCursorVisible()

    def _clear_terminal(self):
        self.terminal.clear()

    # ── ÇALIŞTIR / DERLE ─────────────────────────────────────────────
    def _run(self):
        if not self._save_before_run(): return
        cmd = shutil.which("tsharp")
        if cmd is None:
            DownloadPopup(self, "TSharp Bulunamadı",
                "TSharp çalıştırıcısı sisteminizde bulunamadı.\nTSharp'i indirmek için aşağıdaki düğmeye basın:",
                "TSharp İndir", "https://github.com/Artfical/TSharp/releases", self.T).exec()
            return
        self._exec_cmd([cmd, self.current_file])

    def _compile(self):
        if not self._save_before_run(): return
        cmd = shutil.which("tcompile") or shutil.which("derle")
        if cmd is None:
            DownloadPopup(self, "TCompile Bulunamadı",
                "TCompile derleyicisi sisteminizde bulunamadı.\nTCompile'i indirmek için aşağıdaki düğmeye basın:",
                "TCompile İndir", "https://github.com/Artfical/TCompile/releases", self.T).exec()
            return
        self._exec_cmd([cmd, "--tekdosya", self.current_file])

    def _exec_cmd(self, cmd):
        self._clear_terminal()
        self._terminal_write(f"> {' '.join(cmd)}\n", "cmd")
        self.status_lbl.setText("Çalıştırılıyor..." if "tsharp" in cmd[0] else "Derleniyor...")
        self._run_thread = RunThread(cmd)
        self._run_thread.output.connect(self._terminal_write)
        self._run_thread.finished.connect(self._on_run_finished)
        self._run_thread.start()

    def _on_run_finished(self, ret):
        tag = "info" if ret == 0 else "stderr"
        self._terminal_write(f"\n[İşlem tamamlandı, çıkış kodu: {ret}]\n", tag)
        self.status_lbl.setText("Hazır" if ret == 0 else f"Hata (kod {ret})")

    def _save_before_run(self):
        if self.current_file is None:
            path, _ = QFileDialog.getSaveFileName(self, "Önce Dosyayı Kaydedin", "",
                "T# Dosyası (*.tsh);;T# Uzun (*.tsharp)")
            if not path: return False
            self.current_file = path; self._write_file(path)
        elif not self.saved:
            self._save_file()
        return True

    def closeEvent(self, event):
        if self._confirm_discard(): event.accept()
        else: event.ignore()


# ─────────────────────────────────────────────────────────────────────
# BAŞLANGIÇ
# ─────────────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("TSharp GO")
    app.setStyle("Fusion")
    w = TSharpGO()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
