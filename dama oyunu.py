import tkinter as tk
from tkinter import messagebox

class GorselDama:
    def __init__(self, root):
        self.root = root
        self.root.title("Türk Daması - Dama Kuralı Dahil")
        self.root.resizable(False, False)
        
        # Oyun Durumu (State)
        self.sira = 'Beyaz'
        self.secili_tas = None  # (satir, sutun)
        
        # 'B': Beyaz, 'S': Siyah, 'DB': Dama Beyaz, 'DS': Dama Siyah, '.': Boş
        self.tahta = [
            ['S'] * 8,
            ['S'] * 8,
            ['.'] * 8,
            ['.'] * 8,
            ['.'] * 8,
            ['.'] * 8,
            ['B'] * 8,
            ['B'] * 8
        ]
        
        self.kare_boyutu = 70
        self.tuval_boyutu = 8 * self.kare_boyutu
        
        self.bilgi_etiketi = tk.Label(root, text=f"Sıra: {self.sira} Oyuncuda", font=("Arial", 14, "bold"), pady=10)
        self.bilgi_etiketi.pack()
        
        self.canvas = tk.Canvas(root, width=self.tuval_boyutu, height=self.tuval_boyutu, bg="#f0d9b5")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.tiklama_olayi)
        
        self.ekrani_guncelle()

    def ekrani_guncelle(self):
        self.canvas.delete("all")
        
        # Kareleri Çiz
        for satir in range(8):
            for sutun in range(8):
                x1, y1 = sutun * self.kare_boyutu, satir * self.kare_boyutu
                x2, y2 = x1 + self.kare_boyutu, y1 + self.kare_boyutu
                renk = "#b58863" if (satir + sutun) % 2 == 1 else "#f0d9b5"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=renk, outline="")
                
                if self.secili_tas == (satir, sutun):
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="#2ebd59", width=4)

        # Taşları Çiz
        for satir in range(8):
            for sutun in range(8):
                tas = self.tahta[satir][sutun]
                if tas != '.':
                    x = (sutun * self.kare_boyutu) + (self.kare_boyutu // 2)
                    y = (satir * self.kare_boyutu) + (self.kare_boyutu // 2)
                    r = self.kare_boyutu // 2 - 10
                    
                    tas_rengi = "#ffffff" if 'B' in tas else "#222222"
                    kenar_rengi = "#cccccc" if 'B' in tas else "#000000"
                    
                    self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=tas_rengi, outline=kenar_rengi, width=2)
                    self.canvas.create_oval(x - (r-6), y - (r-6), x + (r-6), y + (r-6), outline=kenar_rengi, width=1)
                    
                    # Dama Taşı İkonu (Yıldız)
                    if tas.startswith('D'):
                        self.canvas.create_text(x, y + 2, text="★", fill="#ffcc00", font=("Arial", 18, "bold"))

    def hamle_gecerli_mi(self, y1, x1, y2, x2):
        tas = self.tahta[y1][x1]
        hedef = self.tahta[y2][x2]
        
        if hedef != '.': return False, None
        
        dy, dx = y2 - y1, x2 - x1
        if dy != 0 and dx != 0: return False, None  # Çapraz yasak
        
        adim_y = 1 if dy > 0 else (-1 if dy < 0 else 0)
        adim_x = 1 if dx > 0 else (-1 if dx < 0 else 0)
        
        # --- NORMAL TAŞ KURALLARI ---
        if not tas.startswith('D'):
            # Yön kontrolü (Normal taş geri gidemez)
            if self.sira == 'Beyaz' and dy > 0: return False, None
            if self.sira == 'Siyah' and dy < 0: return False, None
            
            # 1 Adım İlerleme
            if abs(dy) + abs(dx) == 1:
                return True, "normal"
                
            # 2 Adım Taş Yeme
            if abs(dy) == 2 or abs(dx) == 2:
                ara_y, ara_x = y1 + adim_y, x1 + adim_x
                ara_tas = self.tahta[ara_y][ara_x]
                rakip_mi = ('S' in ara_tas) if self.sira == 'Beyaz' else ('B' in ara_tas)
                if rakip_mi:
                    return True, (ara_y, ara_x)
            return False, None

        # --- DAMA TAŞI KURALLARI ---
        else:
            yol_boyu_taslar = []
            gecerli_y, gecerli_x = y1 + adim_y, x1 + adim_x
            
            # Yol üzerindeki tüm kareleri tara
            while gecerli_y != y2 or gecerli_x != x2:
                t = self.tahta[gecerli_y][gecerli_x]
                if t != '.':
                    yol_boyu_taslar.append(((gecerli_y, gecerli_x), t))
                gecerli_y += adim_y
                gecerli_x += adim_x
                
            # Yol temizse sadece ilerlemedir
            if len(yol_boyu_taslar) == 0:
                return True, "normal"
                
            # Yolda sadece 1 taş varsa ve o da rakipse onu yer
            if len(yol_boyu_taslar) == 1:
                (t_y, t_x), t_tip = yol_boyu_taslar[0]
                rakip_mi = ('S' in t_tip) if self.sira == 'Beyaz' else ('B' in t_tip)
                if rakip_mi:
                    return True, (t_y, t_x)
                    
            return False, None

    def tiklama_olayi(self, event):
        sutun, satir = event.x // self.kare_boyutu, event.y // self.kare_boyutu
        
        if self.secili_tas is None:
            tas = self.tahta[satir][sutun]
            dogru_renk = ('B' in tas) if self.sira == 'Beyaz' else ('S' in tas)
            if tas != '.' and dogru_renk:
                self.secili_tas = (satir, sutun)
                self.ekrani_guncelle()
        else:
            if self.secili_tas == (satir, sutun):
                self.secili_tas = None
                self.ekrani_guncelle()
                return
                
            y1, x1 = self.secili_tas
            gecerli, yenen_tas = self.hamle_gecerli_mi(y1, x1, satir, sutun)
            
            if gecerli:
                # Taşı Taşı
                self.tahta[satir][sutun] = self.tahta[y1][x1]
                self.tahta[y1][x1] = '.'
                
                # Taş yeme işleme
                if yenen_tas and yenen_tas != "normal":
                    ara_y, ara_x = yenen_tas
                    self.tahta[ara_y][ara_x] = '.'
                
                # Dama Olma Kontrolü
                if self.tahta[satir][sutun] == 'B' and satir == 0:
                    self.tahta[satir][sutun] = 'DB'
                    messagebox.showinfo("Tebrikler!", "Beyaz taş DAMA oldu!")
                elif self.tahta[satir][sutun] == 'S' and satir == 7:
                    self.tahta[satir][sutun] = 'DS'
                    messagebox.showinfo("Tebrikler!", "Siyah taş DAMA oldu!")
                
                self.secili_tas = None
                self.sira = 'Siyah' if self.sira == 'Beyaz' else 'Beyaz'
                self.bilgi_etiketi.config(text=f"Sıra: {self.sira} Oyuncuda")
                self.ekrani_guncelle()
                self.oyun_bitti_mi_kontrol_et()
            else:
                tas = self.tahta[satir][sutun]
                dogru_renk = ('B' in tas) if self.sira == 'Beyaz' else ('S' in tas)
                if tas != '.' and dogru_renk:
                    self.secili_tas = (satir, sutun)
                    self.ekrani_guncelle()

    def oyun_bitti_mi_kontrol_et(self):
        beyaz_var = any(('B' in t) for satir in self.tahta for t in satir)
        siyah_var = any(('S' in t) for satir in self.tahta for t in satir)
        
        if not beyaz_var:
            messagebox.showinfo("Oyun Bitti", "Siyah oyuncu kazandı!")
            self.root.quit()
        elif not siyah_var:
            messagebox.showinfo("Oyun Bitti", "Beyaz oyuncu kazandı!")
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    oyun = GorselDama(root)
    root.mainloop()
