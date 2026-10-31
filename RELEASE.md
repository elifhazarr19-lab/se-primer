# RELEASE: SE Primer model v2.0 (takılma tahmini)

| Alan | Değer |
|---|---|
| Model | `ipucu_gerekti` olasılığı (tabular, `Pipeline(StandardScaler → LogisticRegression)`) |
| Sürüm | 2.0 |
| HF reposu | `elifhazarr06/se-primer-takilma` (model, herkese açık) |
| Commit'e sabit URL | `https://huggingface.co/elifhazarr06/se-primer-takilma/resolve/<COMMIT>/model.onnx` |
| Durum | **Yayın hazır değil.** Aşağıdaki kontrol listesinde açık maddeler var. |

## 1. Ne değişti (v1 → v2)

- **v1:** Tutor kuralları elle yazılmış (AI Studio sistem talimatı). Tek tüketici: AI Studio uygulaması.
- **v2:** Oyuncunun davranışından `ipucu_gerekti` olasılığı tahmin edilir. Olasılık ≥ 0,50 ise bir sonraki karar ekranında somut ipucu gösterilir ve Deneyimliyim'de sayaç kalkar (spec §8.1, AK-7).
- Model artefaktı: `model.onnx` + `config.json` (sözleşme) + `model/README.md` (model kartı).
- İki tüketici: Primer uygulaması (tarayıcıda `onnxruntime-web`) ve Python referansı (`tests/parite.py`). Aynı girdilerde aynı olasılığı vermeleri (fark ≤ 1e-4) test edilir.

## 2. Yayın kontrol listesi

Her madde kanıtla işaretlenir. İşaretlenmemiş madde yayını durdurur.

| # | Kontrol | Kanıt | Durum |
|---|---|---|---|
| 1 | Eval kapısı: ortalama ROC-AUC ≥ 0,70 ve dengeli doğruluk > 0,50 | `train.py` çıktısı, `model/config.json` `metrics` | ☑ geçti (sentetik veri; gerçek veriyle yeniden ölçülmeli, madde 3) |
| 2 | ONNX ↔ sklearn en büyük olasılık farkı ≤ 1e-4 | `config.json` `onnx_sklearn_fark` | ☑ 7,5e-08 |
| 3 | En az 15 **gerçek** oturum ve kaynağı `gercek` olan satırlar | `config.json` `veri.gercek_oturum` | ☐ **0 / 15**. Arkadaşlardan veri toplanacak. |
| 4 | Gerçek veriyle yeniden eğitim ve eval kapısı | `python train.py` (gerçek veri dahil) | ☐ 3. maddeye bağlı |
| 5 | Tarayıcı paritesi ≤ 1e-4 (5 referans girdi) | `cypress/e2e/parite.cy.js` | ☐ Build istem 2'den sonra |
| 6 | Model kartı (sınırlar, veri, eşik, gizlilik) | `model/README.md` | ☑ üretildi (4. maddeden sonra yeniden üretilecek) |
| 7 | Commit'e sabit URL, `<COMMIT>` alanı doldurulmuş | Bu dosya, Build istem 2 | ☐ HF yüklemesinden sonra |

Yayın kararı: 3, 4, 5 ve 7 işaretlenmeden model "yayınlandı" sayılmaz.

## 3. Yayın adımları (kullanıcı)

Bu adımlar hesap girişi ve token gerektirir. Token repoya ya da bu dosyaya yazılmaz.

```bash
hf auth login
hf auth whoami
hf repos create elifhazarr06/se-primer-takilma --type model --public --exist-ok
hf upload elifhazarr06/se-primer-takilma model . --repo-type model --commit-message "SE Primer v2.0: takılma tahmini"
```

`hf upload` çıktısındaki `https://huggingface.co/.../commit/<HASH>` bağlantısındaki `<HASH>` değerini
al. Bu, `<COMMIT>` değeridir. Bu dosyanın üstündeki URL'de ve Build istem 2'de `<COMMIT>` yerine yaz.

Yükleme bittikten sonra kontrol:

```bash
curl -sI https://huggingface.co/elifhazarr06/se-primer-takilma/resolve/<COMMIT>/model.onnx
```

Yanıtta `200` görmelisin. Tarayıcıda giriş yapmadan da açılmalı (gizli pencere).

## 4. Commit'e sabitleme neden önemli

`resolve/main/` adresi zamanla değişebilir. Bu yüzden tüketiciler her zaman `resolve/<COMMIT>/`
kullanır. Yeni model yüklenirse eski commit'e giden tüketiciler hiç etkilenmez. Yeni sürümü
kullanmak için tüketici kodundaki `<COMMIT>` değeri değiştirilir ve yeniden yayınlanır.

## 5. Geri alma (rollback) planı

| Durum | Ne yapılır | Süre |
|---|---|---|
| Model yanlış karar veriyor (ör. tutor gereksiz ipucu veriyor) | Build'de `MODEL_ACIK = false` yapılıp Republish edilir. Yardım modu kapanır, oyun v1 davranışına döner. | Dakikalar |
| Yeni commit kötü çıktı | Tüketici `<COMMIT>` değerini bir önceki commit'e çevirir ve Republish eder. | Dakikalar |
| Model dosyası yüklenmiyor | İstem 2, model yüklenemediğinde olasılık göstermeden oyunu sürdürür (kendiliğinden geri döner). | Otomatik |
| Parite testi kırıldı | Yayın durur. Hata kaynağı bulunmadan yeni commit yayınlanmaz. | — |

Geri alma için HF reposundaki dosyalar silinmez. Eski commit'ler kalıcıdır.

## 6. Shadow / Canary / aşamalı yayın planı

Bu ödevde gerçek trafik yoktur. Aşağıdaki plan uygulanacak adımları tanımlar. Hangisinin
yapıldığı işaretlidir.

1. **Gölge (shadow), ☑ uygulanabilir:** Modeli, karar etkilemeden yeni gerçek oturumların
   üzerinde çalıştır. Model olasılığı ile gerçek etiket (`ipucu_gerekti`) karşılaştırılır.
   Eşikler (ROC-AUC ≥ 0,70) bu yeni veride de sağlanmalı. Bu adım, eğitim verisi dışında bir
   doğrulama verir.
2. **Canary, ☐ yapılmadı:** Yardım modu yalnızca oturum kimliğine göre seçilen bir alt kümede
   açılır (ör. kimliğin son hanesi 0–1, yani yaklaşık %20). Bu alt kümede ipucu sayısı, süre
   dolumu ve "Geri al" oranı, kontrol grubuyla karşılaştırılır.
3. **Aşamalı (progressive), ☐ yapılmadı:** %20 → %50 → %100. Her aşamada ROC-AUC ve
   "Geri al" oranı önceden tanımlı bir eşiği geçmelidir. Geçmezse 5. adımdaki geri alma çalışır.

## 7. Ödünleşim matrisi: nerede çıkarım yapılacak

| Kriter | Tarayıcı (`onnxruntime-web`, bu sürüm) | Mobil (`onnxruntime-react-native`, gömülü) | Sunucu (Rails `onnxruntime` gem / FastAPI, bonus) |
|---|---|---|---|
| Gizlilik | Girdi cihazda kalır. Model herkes tarafından indirilebilir. | Girdi cihazda kalır. Model uygulama paketinin içindedir. | Girdi sunucuya gider. Loglama KVKK kapsamına girer. |
| Gecikme | Yerel, ağ gerekmez. İlk yüklemede model indirilir. | Yerel, ağ gerekmez. | Ağ gecikmesi var. Ücretsiz katmanda uyku gecikmesi olabilir. |
| Model güncelleme | Commit değiştirilip Republish ile anında. | Mağaza ya da APK güncellemesi gerekir. | Sunucu değiştirilince anında. |
| Parite riski | Orta. Tarayıcı float32 hesabı. | Orta-yüksek. Native sürüm yaması gerekti (AGENTS.md §2). | Düşük. Aynı ONNX ailesi, ayrı runtime. |
| Maliyet | Ücretsiz (GitHub Pages / Cloud Run). | Ücretsiz (yerel). | Ücretsiz katman, sınırlı. |
| Bu ödevde | **Seçildi.** Yayınlanan uygulamada kullanılıyor. | Kapsam dışı. | Bonus, henüz yapılmadı. |

Seçim gerekçesi: model herkese açık, eğitim verisi kişisel değil, güncelleme ve yayın tek bir
yerden yapılabiliyor. Gizli veriyle eğitilseydi sunucu seçeneği zorunlu olurdu (AGENTS.md §1).

## 8. Kaynaklar

- Mitchell vd. (2019), *Model Cards for Model Reporting*: model kartı yapısı (`model/README.md`).
- Breck vd. (2017), *The ML Test Score*: parite ve yayın kontrol listesi fikri.
- Shankar vd. (2022), *Operationalizing Machine Learning*: 3V sorunu (Velocity, Validation, Versioning).
- Sommerville, *Software Engineering* (10. baskı), Bl. 8: doğrulama ve geçerleme (V&V). Parite testi bunun bir örneğidir.
- Hugging Face Hub belgeleri: `revision` ve `resolve` URL'leri (commit'e sabitleme).
- ONNX Runtime Web ve `skl2onnx` belgeleri: girdi/çıktı adları ve `zipmap` seçeneği.
- Cypress belgeleri: `cy.readFile`, `data-cy` seçicileri.
