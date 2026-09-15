"""
Dairenin Yarıçapını ve Alanını Hesaplayan program
"""

yari_cap = int(input("Dairenin yarıçapını giriniz :"))
pi = 3.14

cevre = 2*pi*yari_cap # cevre hesapladık
alan = pi*(yari_cap**2) # alan hesapladık

print("Dairenin Çevre Uzunluğu :",cevre)
print("Dairenin alanı :",alan)