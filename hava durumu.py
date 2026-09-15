import tkinter as tk
from tkinter import messagebox
import requests

# Hava durumu verisini çeken ana fonksiyon
def hava_durumu_al():
    sehir = sehir_giris.get().strip()
    if not sehir:
        messagebox.showwarning("Uyarı", "Lütfen bir şehir adı girin!")
        return
    
    # ⚠️ BURAYA KENDİ OPENWEATHERMAP API ANAHTARINI YAPIŞTIRMALISIN
    API_KEY = "BURAYA_API_ANAHTARINI_YAZIN"
    url = f"http://openweathermap.org{sehir}&appid={API_KEY}&units=metric&lang=tr"
    
    try:
        cevap = requests.get(url)
        veri = cevap.json()
        
        if veri["cod"] == "404":
            messagebox.showerror("Hata", f"'{sehir}' isimli şehir bulunamadı!")
            return

        # Bilgileri çekiyoruz
        sehir_adi = veri["name"]
        ulke = veri["sys"]["country"]
        sicaklik = veri["main"]["temp"]
        hissedilen = veri["main"]["feels_like"]
        nem = veri["main"]["humidity"]
        aciklama = veri["weather"]["description"].capitalize()

        # Etiketleri güncelliyoruz
        sehir_etiket.config(text=f"📍 {sehir_adi}, {ulke}")
        durum_etiket.config(text=f"☁️ {aciklama}")
        derece_etiket.config(text=f"🌡️ Sıcaklık: {sicaklik}°C")
        hissedilen_etiket.config(text=f"🤔 Hissedilen: {hissedilen}°C")
        nem_etiket.config(text=f"💧 Nem: %{nem}")
        
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Bağlantı Hatası", "İnternet bağlantısı kurulamadı!")
    except Exception as e:
        messagebox.showerror("Hata", f"Bir sorun oluştu: {e}")

# Pencere Tasarımı
pencere = tk.Tk()
pencere.title("Hava Durumu Raporu")
pencere.geometry("350x450")
pencere.configure(bg="#f0f4f8")

# Giriş Alanı ve Başlık
baslik = tk.Label(pencere, text="Hava Durumu", font=("Arial", 18, "bold"), bg="#f0f4f8", fg="#333333")
baslik.pack(pady=15)

sehir_giris = tk.Entry(pencere, font=("Arial", 14), width=20, justify="center")
sehir_giris.pack(pady=5)
sehir_giris.focus() # İmleç direkt burada başlasın

# Sorgula Butonu
sorgula_buton = tk.Button(pencere, text="Hava Durumunu Gör", font=("Arial", 12, "bold"), 
                          bg="#4a90e2", fg="white", bd=0, padx=10, pady=5, command=hava_durumu_al)
sorgula_buton.pack(pady=15)

# Sonuç Kartı Alanı
sonuc_cercevesi = tk.Frame(pencere, bg="white", bd=1, relief="solid", padx=20, pady=20)
sonuc_cercevesi.pack(pady=10, fill="x", padx=20)

sehir_etiket = tk.Label(sonuc_cercevesi, text="📍 Şehir Seçilmedi", font=("Arial", 14, "bold"), bg="white", fg="#2c3e50")
sehir_etiket.pack(pady=5)

durum_etiket = tk.Label(sonuc_cercevesi, text="☁️ --", font=("Arial", 12), bg="white", fg="#7f8c8d")
durum_etiket.pack(pady=3)

derece_etiket = tk.Label(sonuc_cercevesi, text="🌡️ Sıcaklık: --", font=("Arial", 12), bg="white", fg="#c0392b")
derece_etiket.pack(pady=3)

hissedilen_etiket = tk.Label(sonuc_cercevesi, text="🤔 Hissedilen: --", font=("Arial", 11), bg="white", fg="#d35400")
hissedilen_etiket.pack(pady=3)

nem_etiket = tk.Label(sonuc_cercevesi, text="💧 Nem: --", font=("Arial", 11), bg="white", fg="#2980b9")
nem_etiket.pack(pady=3)

# Klavyeden Enter'a basınca da çalışması için
pencere.bind('<Return>', lambda event: hava_durumu_al())

pencere.mainloop()
