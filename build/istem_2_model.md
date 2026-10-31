# Build istemi 2: Model entegrasyonu (HF yayınından sonra)

**Önkoşul:** Model Hugging Face'e yüklendi ve `<COMMIT>` yerine gerçek commit hash'i yazıldı
(bkz. RELEASE.md, 3. adım). Bu istem istem 1'in üzerine uygulanır. Yapıştırmadan önce
`<COMMIT>` alanını değiştir.

---

Mevcut uygulamayı koru. Veri toplama modu (istem 1) ve mevcut tüm davranışlar aynı kalsın.
Aşağıdaki modeli ekle.

## Model

- ONNX Runtime Web'i yükle: `https://cdn.jsdelivr.net/npm/onnxruntime-web@1.22.0/dist/ort.min.js`
- Modeli bu adresten yükle (commit'e sabit):
  `https://huggingface.co/elifhazarr06/se-primer-takilma/resolve/<COMMIT>/model.onnx`
- Girdi tensörü: ad `input`, tip `float32`, şekil `[1, 7]`. Özellik sırası tam olarak:
  `seviye, sahne_no, karar_suresi_sn, onceki_yanlis_sayisi, ipucu_sayisi, ilk_tiklama_sn, onceki_ipucu_gerekti`
- Çıktı: ad `probabilities`, şekil `[1, 2]`. Olasılık = `probabilities.data[1]`.
- Model yüklenemezse uygulama çökmesin: olasılık gösterme ve oyunu bugünkü gibi oynat.

## Özelliklerin hesabı

Her karar kesinleşince (istem 1'deki satır yazılırken) aynı tanımlarla özellikleri hesapla:
seviye, sahne_no, karar_suresi_sn, onceki_yanlis_sayisi (B seçilme sayısı), ipucu_sayisi
("Emin değil misin?" açılış sayısı), ilk_tiklama_sn, onceki_ipucu_gerekti (önceki karar etiketi).
Modeli çalıştır ve olasılığı `p` olarak sakla.

## Oyunu değiştirme (AK-7)

- Kod başında `MODEL_ACIK = true` sabiti olsun. `false` ise model hiç yüklenmez ve oyun v1
  davranışında çalışır (geri alma adımı, bkz. RELEASE.md §5).
- `p >= 0.5` ise **bir sonraki karar ekranında** "Yardım modu" açılır:
  - Ekranda "Nöbetçi İpucu" kutusu görünsün ve kısa somut bir ipucu yazsın. Sokratik ton koru,
    cevabı söyleme. Karara göre metinler:
    - Karar 1: "Canlı sistemde doğrulanmamış bir yama geri dönüşü zorlaştırır. Hangi seçenek sistemi bilinen bir duruma geri götürür?"
    - Karar 2: "Testsiz yayın hatayı kullanıcıya taşır. Hangi seçenek hatayı yayından önce yakalamaya yardım eder?"
    - Karar 3: "Logda kişisel veri kalırsa KVKK sorumluluğu doğar. Ekibe giden logda kişisel veri var mı, bunu nasıl ayırırsın?"
  - Deneyimliyim modundaysa 60 saniyelik "Karar Sayacı" bu ekranda **görünmesin** ve süre dolumu
    olmasın (kullanıcı süresiz karar verebilir).
  - Ekranın üstünde küçük bir rozet göster: "Yardım modu açık".
- `p < 0.5` ise bugünkü davranış: Yeni başladım'da ipucu kutusu mevcut tutor kuralına göre çalışır,
  Deneyimliyim'de sayaç ve süre dolumu aynen işler.
- İlk karar ekranında henüz tahmin yoktur. Bu ekran bugünkü gibi çalışır.

## Parite test kancası (Cypress için)

- URL'de `?parite=<JSON>` parametresi varsa uygulama oyunu oynatmaz. Yalnızca şu JSON'u alır:
  `{"seviye":0,"sahne_no":1,"karar_suresi_sn":5.0,"onceki_yanlis_sayisi":0,"ipucu_sayisi":0,"ilk_tiklama_sn":2.0,"onceki_ipucu_gerekti":0}`
  Modeli bu özelliklerle çalıştırır ve sonucu, metin olarak yalnızca sayı içeren bir
  `<div data-cy="p">` içinde 6 ondalıkla gösterir. Ondalık ayraç nokta olsun (örnek: `0.035877`).
- Bu kanca normal oyuncuya görünmesin. Sayfada başka bir şey gösterme.

## Kontrol

Değişiklikten sonra şunları doğrula ve bana özetle:
1. `?parite=` ile bir girdi verildiğinde `data-cy="p"` alanında sayı görünüyor mu?
2. Yardım modu, Deneyimliyim'de sayaç kaldırma ve "Yardım modu açık" rozetini bir oyunda gördün mü?
3. Model dosyası yüklenemezse (ör. yanlış commit adresi) uygulama çalışmaya devam ediyor mu?
