import random

class Tavla:
    def __init__(self):
        # 24 hane (haneler 1-24 arası). Kolaylık için 0'dan 25'e kadar liste tuttuk.
        # Pozitif sayılar Beyaz (B) pulları, negatif sayılar Siyah (S) pulları temsil eder.
        # Klasik başlangıç dizilimi:
        self.tahta = [0] * 26
        self.tahta[1] = 2    # Beyaz pullar
        self.tahta[6] = -5   # Siyah pullar
        self.tahta[8] = -3   # Siyah pullar
        self.tahta[12] = 5   # Beyaz pullar
        self.tahta[13] = -5  # Siyah pullar
        self.tahta[17] = 3   # Beyaz pullar
        self.tahta[19] = 5   # Beyaz pullar
        self.tahta[24] = -2  # Siyah pullar
        
        self.siradaki_oyuncu = "Beyaz" # Oyuna Beyaz başlar

    def tahtayi_yazdir(self):
        print("\n=== TAVLA TAHTASI ===")
        print("Üst Satır (13-24): ", end="")
        for i in range(13, 25):
            print(f"{i}:{self.hucre_format(self.tahta[i])}", end=" | ")
        print("\n" + "-" * 80)
        print("Alt Satır (12-1):  ", end="")
        for i in range(12, 0, -1):
            print(f"{i}:{self.hucre_format(self.tahta[i])}", end=" | ")
        print("\n=====================\n")

    def hucre_format(self, deger):
        if deger > 0:
            return f"{deger}B"
        elif deger < 0:
            return f"{abs(deger)}S"
        else:
            return " ."

    def zar_at(self):
        z1 = random.randint(1, 6)
        z2 = random.randint(1, 6)
        return z1, z2

    def hamle_yap(self, nereden, nereye, oyuncu):
        # Temel sınır kontrolleri
        if nereden < 1 or nereden > 24 or nereye < 1 or nereye > 24:
            print("❌ Geçersiz hane seçimi!")
            return False

        # Seçilen hanede oyuncunun pulu var mı?
        if oyuncu == "Beyaz" and self.tahta[nereden] <= 0:
            print("❌ Orada Beyaz pulunuz yok!")
            return False
        if oyuncu == "Siyah" and self.tahta[nereden] >= 0:
            print("❌ Orada Siyah pulunuz yok!")
            return False

        # Hedef hanede rakip kapı almış mı? (2 veya daha fazla pul)
        if oyuncu == "Beyaz" and self.tahta[nereye] < -1:
            print("❌ Hedef hanede Siyah kapı almış, giremezsiniz!")
            return False
        if oyuncu == "Siyah" and self.tahta[nereye] > 1:
            print("❌ Hedef hanede Beyaz kapı almış, giremezsiniz!")
            return False

        # Hamleyi uygula
        # (Basit sürüm: Kırma mekanizması dahil edilmedi, boş yere geçiş varsayıldı)
        if oyuncu == "Beyaz":
            self.tahta[nereden] -= 1
            self.tahta[nereye] += 1
        else:
            self.tahta[nereden] += 1
            self.tahta[nereye] -= 1
        
        return True

    def oyna(self):
        print("🎲 Python Tavla Oyununa Hoş Geldiniz! 🎲")
        while True:
            self.tahtayi_yazdir()
            print(f"Sıra Oyuncuda: {self.siradaki_oyuncu}")
            
            input("Zar atmak için ENTER'a basın...")
            z1, z2 = self.zar_at()
            print(f"📣 Atılan Zarlar: {z1} ve {z2}")
            
            # 1. Hamle
            while True:
                try:
                    print(f"Kullanabileceğiniz zar adımları: {z1} veya {z2}")
                    nereden = int(input("Hangi hanedeki pulu oynatacaksınız? (1-24): "))
                    nereye = int(input("Hangi haneye taşıyacaksınız? (1-24): "))
                    
                    if self.hamle_yap(nereden, nereye, self.siradaki_oyuncu):
                        break
                except ValueError:
                    print("Lütfen geçerli bir sayı girin.")
            
            # Sırayı değiştir
            self.siradaki_oyuncu = "Siyah" if self.siradaki_oyuncu == "Beyaz" else "Beyaz"

# Oyunu başlat
if __name__ == "__main__":
    oyun = Tavla()
    oyun.oyna()
