import random

print("Sayı Tahmin Oyununa Hoş Geldiniz!")
rastgele_sayi = random.randint(1, 100)
tahmin_sayisi = 0

while True:
    tahmin = int(input("1 ile 100 arasında bir sayı girin: "))
    tahmin_sayisi += 1
    
    if tahmin < rastgele_sayi:
        print("Daha büyük bir sayı söyleyin.")
    elif tahmin > rastgele_sayi:
        print("Daha küçük bir sayı söyleyin.")
    else:
        print(f"Tebrikler! {tahmin_sayisi}. denemede bildiniz.")
        break
