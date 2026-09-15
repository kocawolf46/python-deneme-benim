import customtkinter as ctk
import math

class GelismisHesapMakinesi(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pencere Ayarları
        self.title("Gelişmiş Hesap Makinesi")
        self.geometry("400x600")
        
        # Varsayılan Tema (Arka Plan Rengi Kontrolü)
        # ctk.set_appearance_mode("dark") -> Arka planı koyu gri yapar
        # ctk.set_appearance_mode("light") -> Arka planı açık gri/beyaz yapar
        self.current_theme = "dark"
        ctk.set_appearance_mode(self.current_theme)
        ctk.set_default_color_theme("blue")

        # Giriş Ekranı (Display)
        self.ekran = ctk.CTkEntry(
            self, 
            width=360, 
            height=70, 
            font=("Arial", 24), 
            justify="right",
            fg_color="#2b2b2b",  # Ekranın kendi iç arka plan rengi
            text_color="white"
        )
        self.ekran.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

        # Buton Düzeni (Gelişmiş Fonksiyonlar Dahil)
        butonlar = [
            ('C', 1, 0), ('√', 1, 1), ('^', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('log', 5, 0), ('0', 5, 1), ('.', 5, 2), ('=', 5, 3)
        ]

        # Butonları Ekrana Yerleştirme
        for (metin, satir, sutun) in butonlar:
            # Operatörler ve sayılar için farklı renk tonları ayarlama
            if metin in ['C', '=', '/', '*', '-', '+', '√', '^', 'log']:
                bg_renk = "#ff9500" if metin == '=' else "#505050"
                yazi_renk = "white"
            else:
                bg_renk = "#333333"
                yazi_renk = "white"

            btn = ctk.CTkButton(
                self, 
                text=metin, 
                width=80, 
                height=60, 
                font=("Arial", 20),
                fg_color=bg_renk,
                text_color=yazi_renk,
                command=lambda m=metin: self.buton_tiklama(m)
            )
            btn.grid(row=satir, column=sutun, padx=5, pady=5)

        # Temayı/Arka Plan Rengini Değiştirme Butonu
        self.tema_btn = ctk.CTkButton(
            self, 
            text="Tema Değiştir (Arka Plan)", 
            width=360, 
            height=40,
            fg_color="#1f6aa5",
            command=self.arka_plan_degistir
        )
        self.tema_btn.grid(row=6, column=0, columnspan=4, padx=20, pady=15)

    def buton_tiklama(self, karakter):
        mevcut = self.ekran.get()

        if karakter == 'C':
            self.ekran.delete(0, ctk.END)
        elif karakter == '=':
            try:
                # Gelişmiş ifadeleri Python diline çevirme
                if '^' in mevcut:
                    mevcut = mevcut.replace('^', '**')
                
                sonuc = eval(mevcut)
                self.ekran.delete(0, ctk.END)
                self.ekran.insert(ctk.END, str(sonuc))
            except:
                self.ekran.delete(0, ctk.END)
                self.ekran.insert(ctk.END, "Hata")
        elif karakter == '√':
            try:
                sonuc = math.sqrt(float(mevcut))
                self.ekran.delete(0, ctk.END)
                self.ekran.insert(ctk.END, str(sonuc))
            except:
                self.ekran.delete(0, ctk.END)
                self.ekran.insert(ctk.END, "Hata")
        elif karakter == 'log':
            try:
                sonuc = math.log10(float(mevcut))
                self.ekran.delete(0, ctk.END)
                self.ekran.insert(ctk.END, str(sonuc))
            except:
                self.ekran.delete(0, ctk.END)
                self.ekran.insert(ctk.END, "Hata")
        else:
            self.ekran.insert(ctk.END, karakter)

    # 🎨 Arka Plan Rengini Dinamik Değiştiren Fonksiyon
    def arka_plan_degistir(self):
        if self.current_theme == "dark":
            ctk.set_appearance_mode("light")  # Genel arka planı beyaz/açık yapar
            self.ekran.configure(fg_color="#e0e0e0", text_color="black") # Ekran rengini günceller
            self.current_theme = "light"
        else:
            ctk.set_appearance_mode("dark")   # Genel arka planı siyah/koyu yapar
            self.ekran.configure(fg_color="#2b2b2b", text_color="white") # Ekran rengini günceller
            self.current_theme = "dark"

if __name__ == "__main__":
    uygulama = GelismisHesapMakinesi()
    uygulama.mainloop()
