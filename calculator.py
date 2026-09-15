def topla(a, b):
    return a + b

def cikar(a, b):
    return a - b

def carp(a, b):
    return a * b

def bol(a, b):
    if b == 0:
        return "Hata: Sıfıra bölme yapılamaz!"
    return a / b

def us_al(a, b):
    return a ** b

def karekok(a):
    if a < 0:
        return "Hata: Negatif sayıların karekökü alınamaz!"
    return a ** 0.5

def menu():
    print("\n--- Gelişmiş Hesap Makinesi ---")
    print("1. Toplama (+)")
    print("2. Çıkarma (-)")
    print("3. Çarpma (*)")
    print("4. Bölme (/)")
    print("5. Üs Alma (^)")
    print("6. Karekök Alma (√)")
    print("q. Çıkış")

while True:
    menu()
    secim = input("İşlem seçiniz: ").lower()
    
    if secim == 'q':
        print("Programdan çıkılıyor...")
        break
        
    if secim in ['1', '2', '3', '4', '5']:
        try:
            sayi1 = float(input("1. sayıyı giriniz: "))
            sayi2 = float(input("2. sayıyı giriniz: "))
        except ValueError:
            print("Geçersiz giriş! Lütfen bir sayı girin.")
            continue
            
        if secim == '1':
            print(f"Sonuç: {topla(sayi1, sayi2)}")
        elif secim == '2':
            print(f"Sonuç: {cikar(sayi1, sayi2)}")
        elif secim == '3':
            print(f"Sonuç: {carp(sayi1, sayi2)}")
        elif secim == '4':
            print(f"Sonuç: {bol(sayi1, sayi2)}")
        elif secim == '5':
            print(f"Sonuç: {us_al(sayi1, sayi2)}")
            
    elif secim == '6':
        try:
            sayi1 = float(input("Karekökü alınacak sayıyı giriniz: "))
        except ValueError:
            print("Geçersiz giriş! Lütfen bir sayı girin.")
            continue
        print(f"Sonuç: {karekok(sayi1)}")
    else:
        print("Geçersiz seçim! Lütfen menüden bir işlem seçin.")
