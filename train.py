"""SE Primer v2: eğitim ve eval kapısı. Tek komut: python train.py

Akış:
  1. data/oturumlar.csv oku, sütunları ve sınıf sayılarını doğrula.
  2. 5 katlı tabakalı çapraz doğrulama: ortalama ROC-AUC ve dengeli doğruluk.
  3. Eşik altındaysa DUR: model/ klasörüne hiçbir şey yazılmaz (AK-6).
  4. Eşik geçildiyse tüm veriyle eğit, model.onnx yaz, ONNX ile sklearn farkını ölç (≤ 1e-4).
  5. config.json (sözleşme + metrikler) ve model/README.md (model kartı) yaz.

Eşikler spec.md §8.5'te eğitimden önce sabitlendi. Buradaki sayılar oradan alınır.
"""

import hashlib
import json
import shutil
import sys
from pathlib import Path

import numpy as np
import onnxruntime as ort
import pandas as pd
import sklearn
import skl2onnx
from skl2onnx import to_onnx
from skl2onnx.common.data_types import FloatTensorType
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

for akis in (sys.stdout, sys.stderr):  # Windows konsolunda (cp1254) ✓ ve ✗ karakterleri için
    if hasattr(akis, "reconfigure"):
        akis.reconfigure(encoding="utf-8")

SEED = 13
AUC_ESIK = 0.70        # spec §8.5: ortalama ROC-AUC
DENGE_ESIK = 0.50      # spec §8.5: dengeli doğruluk çoğunluk tahmininden (0,50) yüksek olmalı
PARITE_ESIK = 1e-4     # spec §8.5: ONNX ↔ sklearn en büyük olasılık farkı
MIN_SINIF = 10         # spec §8.4: en az 10 pozitif ve 10 negatif satır
GERCEK_HEDEF = 15      # spec §8.4: en az 15 gerçek oturum (yayın kontrolü, RELEASE.md)

KOK = Path(__file__).resolve().parent
VERI = KOK / "data" / "oturumlar.csv"
MODEL_DIR = KOK / "model"
OZELLIKLER = [
    "seviye", "sahne_no", "karar_suresi_sn", "onceki_yanlis_sayisi",
    "ipucu_sayisi", "ilk_tiklama_sn", "onceki_ipucu_gerekti",
]
HEDEF = "ipucu_gerekti"
SINIF_ETIKETLERI = {"0": "ipucu gerekmez", "1": "ipucu gerekir"}


def boru_hatti():
    # Ölçekleme + lojistik regresyon. ONNX'e de bu hâliyle girer (ölçekleme modelin içinde).
    return Pipeline([("olcek", StandardScaler()), ("lr", LogisticRegression(random_state=SEED, max_iter=1000))])


def sha256(yol):
    return hashlib.sha256(yol.read_bytes()).hexdigest()


def veriyi_oku():
    if not VERI.exists():
        sys.exit("✗ data/oturumlar.csv yok. Önce: python scripts/uret_sentetik.py")
    veri = pd.read_csv(VERI)
    eksik = [c for c in OZELLIKLER + [HEDEF, "oturum", "kaynak"] if c not in veri.columns]
    if eksik:
        sys.exit(f"✗ eksik sütun(lar): {eksik}")
    pozitif = int((veri[HEDEF] == 1).sum())
    negatif = int((veri[HEDEF] == 0).sum())
    if min(pozitif, negatif) < MIN_SINIF:
        sys.exit(f"✗ yetersiz veri: {pozitif} pozitif, {negatif} negatif (en az {MIN_SINIF} gerekli). Eğitim durdu.")
    return veri


def eval_kapisi(X, y):
    kat = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    aucler = []
    for egitim, test in kat.split(X, y):
        model = boru_hatti().fit(X.iloc[egitim], y.iloc[egitim])
        aucler.append(roc_auc_score(y.iloc[test], model.predict_proba(X.iloc[test])[:, 1]))
    oof = cross_val_predict(boru_hatti(), X, y, cv=kat, method="predict_proba")[:, 1]
    denge = balanced_accuracy_score(y, (oof >= 0.5).astype(int))
    return float(np.mean(aucler)), [float(a) for a in aucler], float(denge)


def onnx_yaz_ve_olc(model, X, yol):
    onx = to_onnx(
        model,
        initial_types=[("input", FloatTensorType([None, X.shape[1]]))],
        options={id(model): {"zipmap": False}},
        target_opset=17,
    )
    yol.write_bytes(onx.SerializeToString())
    oturum = ort.InferenceSession(str(yol))
    p_onnx = oturum.run(["probabilities"], {"input": X.to_numpy(np.float32)})[0]
    fark = float(np.abs(p_onnx - model.predict_proba(X)).max())
    return fark


def model_karti(config):
    metrik_satirlari = "\n".join(f"| {k} | {v} |" for k, v in config["metrics"].items())
    veri = config["veri"]
    uyari = (
        "> **Yayın uyarısı:** Bu eğitimde gerçek oturum sayısı "
        f"{veri['gercek_oturum']} (hedef {GERCEK_HEDEF}). Gerçek oturum hedefin altındaysa model "
        "yalnızca eğitim hattını doğrular; RELEASE.md'deki yayın kontrol listesi bunu engeller."
        if not config["yayin_hazir"] else
        f"Gerçek oturum sayısı {veri['gercek_oturum']} (hedef {GERCEK_HEDEF} ve üstü)."
    )
    return f"""# SE Primer model kartı: {config['title']}

Sürüm: **{config['surum']}** · Seed: {config['seed']} · Eşik olasılığı: {config['esik']}

## Amaç

{config['aciklama']}

Model girdi olarak bir oyuncunun karar ekranındaki davranış özetini alır ve `ipucu_gerekti`
olasılığını döndürür. Olasılık {config['esik']} ve üzerindeyse oyunda "Yardım modu" açılır.

## Girdiler (sütun sırası = config.json `features` sırası)

| Sıra | Özellik | Tanım |
|---|---|---|
{chr(10).join(f"| {i + 1} | `{o['name']}` | {o['aciklama']} |" for i, o in enumerate(config['features']))}

## Çıktı

`probabilities[1]` = `ipucu_gerekti = 1` olasılığı. Sınıf sırası: {config['classes']}.

## Veri

- Satır: {veri['satir']} · Oturum: {veri['oturum']} · Pozitif: {veri['pozitif']} · Negatif: {veri['negatif']}
- Gerçek satır: {veri['gercek_satir']} · Sentetik satır: {veri['sentetik_satir']}
- {uyari}
- Sentetik üretici kuralı ve tohumu: [data/SOZLUK.md](../data/SOZLUK.md)
- Veri dosyası sha256: `{config['veri_sha256']}`

## Eval (5 katlı tabakalı çapraz doğrulama, seed {config['seed']})

| Metrik | Değer |
|---|---|
{metrik_satirlari}

Kabul eşikleri (spec §8.5): ortalama ROC-AUC ≥ {AUC_ESIK}, dengeli doğruluk > {DENGE_ESIK}.
ONNX ↔ sklearn en büyük fark: {config['onnx_sklearn_fark']:.2e} (eşik {PARITE_ESIK}).

## Sınırlar ve kullanım

- Bu model karar vermez; oyunun zorluğunu ayarlamak için bir sinyal üretir.
- Eğitim verisi küçük ve (kısmen) sentetik. Sonuçlar genellenebilir değildir.
- Gerçek kişisel veri, ad, e-posta veya cihaz kimliği yoktur. Oturum kimlikleri rastgele üretilir.
- Tarayıcıda çalışan model herkes tarafından indirilebilir. Gizli veriyle eğitilmiş değildir.

## Sürüm bilgisi

- scikit-learn {config['sklearn_version']}, skl2onnx {config['skl2onnx_version']},
  onnxruntime {config['onnxruntime_version']}, Python {config['python_version']}
- model.onnx sha256: `{config['onnx_sha256']}`
"""


def main():
    veri = veriyi_oku()
    X = veri[OZELLIKLER].astype(float)
    y = veri[HEDEF].astype(int)

    auc, auc_katlar, denge = eval_kapisi(X, y)
    print(f"eval: ortalama ROC-AUC = {auc:.4f} (eşik {AUC_ESIK}), dengeli doğruluk = {denge:.4f} (eşik > {DENGE_ESIK})")
    if auc < AUC_ESIK or denge <= DENGE_ESIK:
        sys.exit(
            "✗ EVAL KAPISI BAŞARISIZ: model yayınlanamaz. model/ klasörüne hiçbir şey yazılmadı (AK-6)."
        )
    print("✓ eval kapısı geçildi")

    son_model = boru_hatti().fit(X, y)
    if MODEL_DIR.exists():
        shutil.rmtree(MODEL_DIR)
    MODEL_DIR.mkdir(parents=True)

    fark = onnx_yaz_ve_olc(son_model, X, MODEL_DIR / "model.onnx")
    if fark > PARITE_ESIK:
        shutil.rmtree(MODEL_DIR)
        sys.exit(f"✗ ONNX çıktısı sklearn'den sapıyor (maks fark {fark:.2e} > {PARITE_ESIK}). Model silindi.")
    print(f"✓ model.onnx üretildi (sklearn ile maks fark {fark:.1e})")

    gercek_satir = int((veri["kaynak"] == "gercek").sum())
    sentetik_satir = int((veri["kaynak"] == "sentetik").sum())
    gercek_oturum = int(veri.loc[veri["kaynak"] == "gercek", "oturum"].nunique())
    ornek = X.iloc[0]
    config = {
        "title": "takılma tahmini (ipucu_gerekti)",
        "surum": "2.0",
        "aciklama": (
            "Oyuncunun karar ekranındaki davranışından, bir sonraki kararda ipucu gerekip "
            "gerekmediğini tahmin eder."
        ),
        "target": HEDEF,
        "class_labels": SINIF_ETIKETLERI,
        "classes": [int(c) for c in son_model.classes_],
        "esik": 0.5,
        "features": [
            {"name": c, "aciklama": aciklama, "example": float(ornek[c])}
            for c, aciklama in [
                ("seviye", "0 Yeni başladım, 1 Deneyimliyim"),
                ("sahne_no", "karar sırası: 1, 2, 3"),
                ("karar_suresi_sn", "ekran açılışından seçime kadar geçen süre (sn)"),
                ("onceki_yanlis_sayisi", "önceki kararlarda B seçeneği sayısı (adet)"),
                ("ipucu_sayisi", "önceki kararlarda \"Emin değil misin?\" açılış sayısı (adet)"),
                ("ilk_tiklama_sn", "ekran açılışından ilk seçime kadar geçen süre (sn)"),
                ("onceki_ipucu_gerekti", "önceki karar için etiket (ilk karar için 0)"),
            ]
        ],
        "metrics": {
            "cv_roc_auc_ortalama": round(auc, 4),
            "cv_roc_auc_katlar": [round(a, 4) for a in auc_katlar],
            "cv_dengeli_dogruluk": round(denge, 4),
            "esik_roc_auc": AUC_ESIK,
            "esik_dengeli_dogruluk": DENGE_ESIK,
        },
        "veri": {
            "satir": int(len(veri)),
            "oturum": int(veri["oturum"].nunique()),
            "pozitif": int((y == 1).sum()),
            "negatif": int((y == 0).sum()),
            "gercek_satir": gercek_satir,
            "sentetik_satir": sentetik_satir,
            "gercek_oturum": gercek_oturum,
        },
        "veri_sha256": sha256(VERI),
        "yayin_hazir": bool(gercek_oturum >= GERCEK_HEDEF),
        "onnx_sklearn_fark": fark,
        "onnx_sha256": sha256(MODEL_DIR / "model.onnx"),
        "seed": SEED,
        "sklearn_version": sklearn.__version__,
        "skl2onnx_version": skl2onnx.__version__,
        "onnxruntime_version": ort.__version__,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
    }
    (MODEL_DIR / "config.json").write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    (MODEL_DIR / "README.md").write_text(model_karti(config), encoding="utf-8")

    print(f"✓ config.json ve model/README.md yazıldı → {MODEL_DIR}")
    print(f"  gerçek oturum: {gercek_oturum} (yayın için hedef {GERCEK_HEDEF})")
    if not config["yayin_hazir"]:
        print("  ! yayın hazır değil: gerçek oturum hedefin altında. RELEASE.md kontrol listesine bakın.")


if __name__ == "__main__":
    main()
