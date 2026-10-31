"""Sentetik oturum üreticisi (kural tabanlı + gürültü). Tohum: 13.

Kullanım (proje kökünden):
    .venv\\Scripts\\python scripts\\uret_sentetik.py --oturum 40

Çıktı: data/oturumlar.csv. Yalnızca sentetik satır üretir (kaynak = sentetik).
Dosyada gerçek oturum (kaynak = gercek) varsa üzerine yazmaz; gerçek veriyi korur.

Kuralın tamamı aşağıda. Gizli beceri (0 acemi, 1 usta) veride yer almaz; model onu
doğrudan göremez, yalnızca girdilerden dolaylı olarak tahmin eder.
"""

import argparse
import csv
import math
import random
import sys
from pathlib import Path

for akis in (sys.stdout, sys.stderr):  # Windows konsolunda (cp1254) ✓ ve ✗ karakterleri için
    if hasattr(akis, "reconfigure"):
        akis.reconfigure(encoding="utf-8")

SEED = 13
KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / "data" / "oturumlar.csv"
SUTUNLAR = [
    "oturum", "sahne_no", "seviye", "karar_suresi_sn", "onceki_yanlis_sayisi",
    "ipucu_sayisi", "ilk_tiklama_sn", "onceki_ipucu_gerekti", "ipucu_gerekti", "kaynak",
]


def sigmoid(z):
    return 1.0 / (1.0 + math.exp(-z))


def oturum_uret(rng, kimlik):
    beceri = rng.random()                      # gizli: 0 acemi, 1 usta
    seviye = 1 if rng.random() < 0.4 else 0   # 0 Yeni başladım, 1 Deneyimliyim
    yanlis = 0          # önceki B seçimi sayısı
    ipucu = 0           # önceki "Emin değil misin?" açılış sayısı
    onceki_etiket = 0   # ilk karar için 0
    satirlar = []
    for sahne in (1, 2, 3):
        sure = min(60.0, max(2.0, rng.gauss(10 + 30 * (1 - beceri) + 4 * yanlis, 5)))
        ilk = min(sure, max(0.5, rng.gauss(0.5 * sure, 2)))
        # Etiket kuralı (gürültülü): acemilik, önceki yanlışlar, önceki etiket ve uzun karar süresi
        # etiketi 1 yönünde iter; Deneyimliyim seviyesi tersine çeker.
        z = (-2.6 + 2.5 * (1 - beceri) + 0.6 * yanlis + 0.9 * onceki_etiket
             - 0.5 * seviye + 0.03 * (sure - 15) + rng.gauss(0, 0.5))
        etiket = 1 if rng.random() < sigmoid(z) else 0
        satirlar.append({
            "oturum": kimlik,
            "sahne_no": sahne,
            "seviye": seviye,
            "karar_suresi_sn": round(sure, 1),
            "onceki_yanlis_sayisi": yanlis,
            "ipucu_sayisi": ipucu,
            "ilk_tiklama_sn": round(ilk, 1),
            "onceki_ipucu_gerekti": onceki_etiket,
            "ipucu_gerekti": etiket,
            "kaynak": "sentetik",
        })
        # Bu karardan sonra: ipucu isteme ve B seçme olasılıkları beceriye bağlı
        if rng.random() < 0.05 + 0.35 * (1 - beceri):
            ipucu += 1
        if rng.random() < 0.1 + 0.5 * (1 - beceri):
            yanlis += 1
        onceki_etiket = etiket
    return satirlar


def gercek_var_mi(yol):
    if not yol.exists():
        return False
    with yol.open(encoding="utf-8", newline="") as dosya:
        return any(satir.get("kaynak") == "gercek" for satir in csv.DictReader(dosya))


def main():
    arac = argparse.ArgumentParser(description="SE Primer sentetik oturum üreticisi")
    arac.add_argument("--oturum", type=int, default=40, help="üretilecek oturum sayısı")
    args = arac.parse_args()

    if gercek_var_mi(CIKTI):
        sys.exit("✗ data/oturumlar.csv içinde gerçek oturumlar var; üzerine yazılmadı.")

    rng = random.Random(SEED)
    kimlikler = set()
    satirlar = []
    while len(kimlikler) < args.oturum:
        kimlik = f"{rng.getrandbits(24):06x}"
        if kimlik in kimlikler:
            continue
        kimlikler.add(kimlik)
        satirlar.extend(oturum_uret(rng, kimlik))

    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    with CIKTI.open("w", encoding="utf-8", newline="") as dosya:
        yazar = csv.DictWriter(dosya, fieldnames=SUTUNLAR)
        yazar.writeheader()
        yazar.writerows(satirlar)

    pozitif = sum(s["ipucu_gerekti"] for s in satirlar)
    print(f"✓ {args.oturum} sentetik oturum, {len(satirlar)} satır → {CIKTI}")
    print(f"  ipucu_gerekti: {pozitif} pozitif, {len(satirlar) - pozitif} negatif")


if __name__ == "__main__":
    main()
