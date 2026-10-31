"""İkinci tüketici: Python referans betiği (parite testinin "doğru cevap" kaynağı).

model/model.onnx ve model/config.json'u okur, 5 referans girdi için olasılığı hesaplar ve
tests/parite.json dosyasına yazar. Cypress testi (cypress/e2e/parite.cy.js) aynı girdileri
tarayıcıdaki Primer uygulamasına verir ve iki sayının farkını ≤ 1e-4 diye kontrol eder.

Kullanım (proje kökünden):
    .venv\\Scripts\\python tests\\parite.py
"""

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import onnxruntime as ort

if hasattr(sys.stdout, "reconfigure"):  # Windows konsolu (cp1254) için
    sys.stdout.reconfigure(encoding="utf-8")

KOK = Path(__file__).resolve().parent.parent
MODEL_DIR = KOK / "model"
CIKTI = KOK / "tests" / "parite.json"
TOLERANS = 1e-4

# 5 referans girdi. Değerler sabit ve elle seçildi; kapsam: acemi/usta, iki seviye, farklı sahneler.
REFERANS_GIRDILER = [
    {"seviye": 0, "sahne_no": 1, "karar_suresi_sn": 5.0, "onceki_yanlis_sayisi": 0,
     "ipucu_sayisi": 0, "ilk_tiklama_sn": 2.0, "onceki_ipucu_gerekti": 0},
    {"seviye": 0, "sahne_no": 2, "karar_suresi_sn": 45.0, "onceki_yanlis_sayisi": 2,
     "ipucu_sayisi": 1, "ilk_tiklama_sn": 20.0, "onceki_ipucu_gerekti": 1},
    {"seviye": 1, "sahne_no": 3, "karar_suresi_sn": 30.0, "onceki_yanlis_sayisi": 1,
     "ipucu_sayisi": 0, "ilk_tiklama_sn": 12.0, "onceki_ipucu_gerekti": 0},
    {"seviye": 0, "sahne_no": 3, "karar_suresi_sn": 58.0, "onceki_yanlis_sayisi": 3,
     "ipucu_sayisi": 2, "ilk_tiklama_sn": 30.0, "onceki_ipucu_gerekti": 1},
    {"seviye": 1, "sahne_no": 1, "karar_suresi_sn": 9.5, "onceki_yanlis_sayisi": 0,
     "ipucu_sayisi": 0, "ilk_tiklama_sn": 4.5, "onceki_ipucu_gerekti": 0},
]


def main():
    config = json.loads((MODEL_DIR / "config.json").read_text(encoding="utf-8"))
    ozellik_sirasi = [o["name"] for o in config["features"]]
    onnx_yolu = MODEL_DIR / "model.onnx"
    oturum = ort.InferenceSession(str(onnx_yolu))

    girdiler = []
    for i, girdi in enumerate(REFERANS_GIRDILER, start=1):
        x = np.array([[girdi[ad] for ad in ozellik_sirasi]], dtype=np.float32)
        p = float(oturum.run(["probabilities"], {"input": x})[0][0][1])
        girdiler.append({"id": i, "girdi": girdi, "p": round(p, 8)})
        print(f"  {i}. p(ipucu_gerekti) = {p:.6f}  {girdi}")

    cikti = {
        "model_surumu": config["surum"],
        "onnx_sha256": hashlib.sha256(onnx_yolu.read_bytes()).hexdigest(),
        "ozellik_sirasi": ozellik_sirasi,
        "tolerans": TOLERANS,
        "girdiler": girdiler,
    }
    CIKTI.write_text(json.dumps(cikti, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"✓ {len(girdiler)} referans olasılık yazıldı → {CIKTI}")


if __name__ == "__main__":
    main()
