import os
import sys
import platform
import threading
import time
from tkinter import messagebox, ttk
import tkinter as tk

class PCKapaticiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PC Kapatıcı")
        self.root.geometry("400x320")
        self.root.resizable(False, False)
        
        # Tema ve Stil Ayarları
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.is_running = False
        self.remaining_time = 0
        self.os_type = platform.system()
        
        self.create_widgets()

    def create_widgets(self):
        # Başlık Bölümü
        header_label = ttk.Label(self.root, text="PC Otomatik Kapatma Sistemi", font=("Helvetica", 14, "bold"))
        header_label.pack(pady=15)
        
        # İşletim Sistemi Bilgisi
        os_label = ttk.Label(self.root, text=f"Algılanan Sistem: {self.os_type}", font=("Helvetica", 9, "italic"))
        os_label.pack(pady=2)

        # Giriş Alanları Çerçevesi
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=15)

        # Saat, Dakika, Saniye Etiket ve Girişleri
        ttk.Label(input_frame, text="Saat:").grid(row=0, column=0, padx=5)
        self.hour_spin = ttk.Spinbox(input_frame, from_=0, to=23, width=5, wrap=True)
        self.hour_spin.set(0)
        self.hour_spin.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Dakika:").grid(row=0, column=2, padx=5)
        self.min_spin = ttk.Spinbox(input_frame, from_=0, to=59, width=5, wrap=True)
        self.min_spin.set(30) # Varsayılan 30 dk
        self.min_spin.grid(row=0, column=3, padx=5)

        ttk.Label(input_frame, text="Saniye:").grid(row=0, column=4, padx=5)
        self.sec_spin = ttk.Spinbox(input_frame, from_=0, to=59, width=5, wrap=True)
        self.sec_spin.set(0)
        self.sec_spin.grid(row=0, column=5, padx=5)

        # Durum ve Geri Sayım Ekranı
        self.status_label = ttk.Label(self.root, text="Sistem Hazır", font=("Helvetica", 12))
        self.status_label.pack(pady=10)
        
        self.countdown_label = ttk.Label(self.root, text="00:00:00", font=("Helvetica", 20, "bold"), foreground="gray")
        self.countdown_label.pack(pady=5)

        # Butonlar Çerçevesi
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=15)

        self.start_btn = ttk.Button(btn_frame, text="Zamanlayıcıyı Başlat", command=self.start_timer)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.cancel_btn = ttk.Button(btn_frame, text="İptal Et", command=self.cancel_timer, state=tk.DISABLED)
        self.cancel_btn.grid(row=0, column=1, padx=10)

    def start_timer(self):
        try:
            hours = int(self.hour_spin.get())
            minutes = int(self.min_spin.get())
            seconds = int(self.sec_spin.get())
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli sayısal değerler girin.")
            return

        self.remaining_time = (hours * 3600) + (minutes * 60) + seconds

        if self.remaining_time <= 0:
            messagebox.showwarning("Uyarı", "Lütfen 0'dan büyük bir süre girin.")
            return

        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Geri sayım başlatıldı...", foreground="green")
        self.countdown_label.config(foreground="black")
        
        # Arayüzün donmaması için geri sayımı arka planda (Thread) çalıştırıyoruz
        self.timer_thread = threading.Thread(target=self.countdown)
        self.timer_thread.daemon = True
        self.timer_thread.start()

    def countdown(self):
        while self.remaining_time > 0 and self.is_running:
            mins, secs = divmod(self.remaining_time, 60)
            hours, mins = divmod(mins, 60)
            time_format = f"{hours:02d}:{mins:02d}:{secs:02d}"
            
            self.countdown_label.config(text=time_format)
            self.root.update()
            time.sleep(1)
            self.remaining_time -= 1

        if self.is_running:
            self.countdown_label.config(text="00:00:00")
            self.status_label.config(text="Bilgisayar kapatılıyor!", foreground="red")
            self.execute_shutdown()

    def cancel_timer(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Zamanlayıcı iptal edildi.", foreground="orange")
        self.countdown_label.config(text="00:00:00", foreground="gray")
        
        # Eğer işletim sistemi seviyesinde bir kapatma emri verildiyse onu da iptal et
        try:
            if self.os_type == "Windows":
                os.system("shutdown -a")
            elif self.os_type in ["Linux", "Darwin"]:
                os.system("sudo shutdown -c")
        except Exception:
            pass

    def execute_shutdown(self):
        # İşletim sistemine göre kapatma komutunu tetikler
        if self.os_type == "Windows":
            os.system("shutdown /s /t 1")
        elif self.os_type == "Linux":
            os.system("poweroff")
        elif self.os_type == "Darwin": # macOS
            os.system("osascript -e 'tell app \"System Events\" to shut down'")
        else:
            messagebox.showerror("Hata", "Bilinmeyen işletim sistemi! Kapatma komutu çalıştırılamadı.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PCKapaticiApp(root)
    root.mainloop()
