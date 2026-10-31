# Veri sözlüğü: `data/oturumlar.csv`

Her satır bir **karar ekranı**dır. Bir oturumda üç karar vardır, yani bir oturum üç satır eder.
Uygulamanın Veri Toplama Modu bu dosyayı oluşturur. Sentetik satırlar `scripts/uret_sentetik.py`
ile üretilir.

## Sütunlar

| Sütun | Tanım | Birim / değer | Model girdisi mi |
|---|---|---|---|
| `oturum` | Rastgele oturum kimliği (6 hane hex). Ad, e-posta veya cihaz kimliği yoktur. | metin | hayır |
| `sahne_no` | Karar sırası | 1, 2, 3 | evet |
| `seviye` | Oyuncunun seçtiği seviye | 0 = Yeni başladım, 1 = Deneyimliyim | evet |
| `karar_suresi_sn` | Karar ekranı açıldıktan sonra kararın kesinleşmesine kadar geçen süre | saniye (0,1 hassasiyet) | evet |
| `onceki_yanlis_sayisi` | Bu karardan önce verilen **B seçeneği** sayısı (karar 1, 2, 3 için B = kötü seçenek) | adet, 0–2 | evet |
| `ipucu_sayisi` | Bu karardan önce "Emin değil misin?" (tutor) düğmesinin açılış sayısı | adet | evet |
| `ilk_tiklama_sn` | Karar ekranı açıldıktan sonra ilk seçime kadar geçen süre | saniye (0,1 hassasiyet) | evet |
| `onceki_ipucu_gerekti` | Bir önceki kararın `ipucu_gerekti` etiketi. İlk karar için 0. | 0/1 | evet |
| `ipucu_gerekti` | **Hedef etiket.** Bu karar için oyuncunun yardıma ihtiyacı olup olmadığı. | 0/1 | hayır (hedef) |
| `kaynak` | Satırın kökeni | `gercek` veya `sentetik` | hayır |

### Etiket kuralı (`ipucu_gerekti`)

- `1`: Oyuncu o kararda **"Geri al"** kullandı **veya** tutora soru yazdı.
- `0`: Aksi halde.

Etiket, girdilerle sızıntı oluşmasın diye hiçbir girdi sütununa yansımaz. "Geri al" ve tutora
yazılan soru girdi olarak kullanılmaz.

### Model girdisi

`seviye, sahne_no, karar_suresi_sn, onceki_yanlis_sayisi, ipucu_sayisi, ilk_tiklama_sn, onceki_ipucu_gerekti`
(bu sıra `model/config.json` içindeki `features` sırasıdır).

## Kaynak sütunu

- `gercek`: arkadaşların uygulamada oynadığı oturumlar. Veri Toplama Modu bu değeri yazar.
- `sentetik`: `scripts/uret_sentetik.py` tarafından üretilir.

Yayın kontrolü için en az **15 gerçek oturum** gerekir (`model/config.json` içinde `gercek_oturum`).

## Gizlilik (KVKK)

- Ad, e-posta, cihaz kimliği, IP, konum ve hasta verisi toplanmaz.
- Oturum kimliği rastgele üretilir ve kişiyle eşleştirilmez.
- Gerçek veri paylaşılırken yalnızca bu CSV gönderilir. Ekran görüntüsü veya ses kaydı eklenmez.

## Sentetik üretici: kural ve tohum

Dosya: [scripts/uret_sentetik.py](../scripts/uret_sentetik.py). Tohum: **13**.

Her sentetik oturum için:

1. Gizli beceri `b ~ U(0, 1)`. Bu değer veride yer almaz.
2. Seviye: `P(Deneyimliyim) = 0,4`.
3. Her karar için (sahne 1, 2, 3):
   - `karar_suresi_sn ~ N(10 + 30·(1−b) + 4·yanlis, 5)`, [2, 60] aralığına kırpılır.
   - `ilk_tiklama_sn ~ N(0,5·süre, 2)`, [0,5, süre] aralığına kırpılır.
   - Etiket: `z = −2,6 + 2,5·(1−b) + 0,6·yanlis + 0,9·önceki_etiket − 0,5·seviye + 0,03·(süre−15) + N(0; 0,5)`;
     `ipucu_gerekti ~ Bernoulli(σ(z))`.
   - Karardan sonra: `P(ipucu) = 0,05 + 0,35·(1−b)`, `P(B) = 0,1 + 0,5·(1−b)`.

Çalıştırma (proje kökünden): `.venv\Scripts\python scripts\uret_sentetik.py --oturum 40`.
Üretici gerçek oturum içeren bir dosyanın üzerine yazmaz.

**Sınır:** Kural ve modelin girdileri aynı kaynaktan geldiği için sentetik veride ROC-AUC
yapay olarak yüksek çıkar. Bu sayı yalnızca eğitim hattının çalıştığını gösterir. Model
kararının kanıtı gerçek oturumlardır.
