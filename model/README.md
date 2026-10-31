# SE Primer model kartı: takılma tahmini (ipucu_gerekti)

Sürüm: **2.0** · Seed: 13 · Eşik olasılığı: 0.5

## Amaç

Oyuncunun karar ekranındaki davranışından, bir sonraki kararda ipucu gerekip gerekmediğini tahmin eder.

Model girdi olarak bir oyuncunun karar ekranındaki davranış özetini alır ve `ipucu_gerekti`
olasılığını döndürür. Olasılık 0.5 ve üzerindeyse oyunda "Yardım modu" açılır.

## Girdiler (sütun sırası = config.json `features` sırası)

| Sıra | Özellik | Tanım |
|---|---|---|
| 1 | `seviye` | 0 Yeni başladım, 1 Deneyimliyim |
| 2 | `sahne_no` | karar sırası: 1, 2, 3 |
| 3 | `karar_suresi_sn` | ekran açılışından seçime kadar geçen süre (sn) |
| 4 | `onceki_yanlis_sayisi` | önceki kararlarda B seçeneği sayısı (adet) |
| 5 | `ipucu_sayisi` | önceki kararlarda "Emin değil misin?" açılış sayısı (adet) |
| 6 | `ilk_tiklama_sn` | ekran açılışından ilk seçime kadar geçen süre (sn) |
| 7 | `onceki_ipucu_gerekti` | önceki karar için etiket (ilk karar için 0) |

## Çıktı

`probabilities[1]` = `ipucu_gerekti = 1` olasılığı. Sınıf sırası: [0, 1].

## Veri

- Satır: 120 · Oturum: 40 · Pozitif: 45 · Negatif: 75
- Gerçek satır: 0 · Sentetik satır: 120
- > **Yayın uyarısı:** Bu eğitimde gerçek oturum sayısı 0 (hedef 15). Gerçek oturum hedefin altındaysa model yalnızca eğitim hattını doğrular; RELEASE.md'deki yayın kontrol listesi bunu engeller.
- Sentetik üretici kuralı ve tohumu: [data/SOZLUK.md](../data/SOZLUK.md)
- Veri dosyası sha256: `e8021cc7f95dbbe362e1c70d090f37ae43298943f76c0d3a065aef4d5c540212`

## Eval (5 katlı tabakalı çapraz doğrulama, seed 13)

| Metrik | Değer |
|---|---|
| cv_roc_auc_ortalama | 0.8252 |
| cv_roc_auc_katlar | [0.837, 0.7556, 0.8963, 0.7926, 0.8444] |
| cv_dengeli_dogruluk | 0.7133 |
| esik_roc_auc | 0.7 |
| esik_dengeli_dogruluk | 0.5 |

Kabul eşikleri (spec §8.5): ortalama ROC-AUC ≥ 0.7, dengeli doğruluk > 0.5.
ONNX ↔ sklearn en büyük fark: 7.51e-08 (eşik 0.0001).

## Sınırlar ve kullanım

- Bu model karar vermez; oyunun zorluğunu ayarlamak için bir sinyal üretir.
- Eğitim verisi küçük ve (kısmen) sentetik. Sonuçlar genellenebilir değildir.
- Gerçek kişisel veri, ad, e-posta veya cihaz kimliği yoktur. Oturum kimlikleri rastgele üretilir.
- Tarayıcıda çalışan model herkes tarafından indirilebilir. Gizli veriyle eğitilmiş değildir.

## Sürüm bilgisi

- scikit-learn 1.9.1, skl2onnx 1.20.0,
  onnxruntime 1.31.1, Python 3.14
- model.onnx sha256: `fce332014a54534f250c65d1b80c8ae9566c943f5033eb61ebddd72f725d8f1a`
