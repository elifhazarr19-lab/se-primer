# SE Primer

YZM301 Yazılım Gerçekleme ve Test dersi, Ödev 1.

SE Primer, sağlık sektöründe geçen bir kriz senaryosunu (sabah 08:00'de çöken randevu sistemi) oynanabilir bir uygulamaya dönüştürür. Oyuncu nöbetçi mühendis olarak üç karar verir (mimari, test, KVKK). Her kararın teknik sonucu ve nedeni gösterilir. Arkada çalışan Sokratik AI Tutor cevabı söylemez, soru sorarak düşündürür.

## Bağlantılar

- **AI Studio uygulaması (Build):** https://aistudio.google.com/apps/f8ae9c9b-27e3-4ffc-b823-dfeee1b09a30
- **Yayınlanan uygulama (telefonda açılan link):** https://se-primer-1-282987152472.europe-west2.run.app/
- **Spesifikasyon:** [spec.md](spec.md)
- **Tasarım:** [DESIGN.md](DESIGN.md), ekran görüntüleri: [tasarim/](tasarim/)
- **Tutor sistem promptu:** [system_prompt.md](system_prompt.md)
- **Tutor değerlendirmesi:** [eval/](eval/)
- **Yayın testi:** [test/yayinlanan_uygulama_testi.md](test/yayinlanan_uygulama_testi.md)
- **Demo videosu (56 sn):** [test/demo.mp4](test/demo.mp4)
- **Model (v2) HF reposu:** `elifhazarr06/se-primer-takilma` (yayınlanınca bağlantı buraya eklenecek, commit'li adres [RELEASE.md](RELEASE.md) içinde)
- **Veri sözlüğü:** [data/SOZLUK.md](data/SOZLUK.md) · **Sınav tasarımı:** [SINAV_TASARIMI.md](SINAV_TASARIMI.md)

## Mimari

Üç katmanlı bir yapı var:

1. **Tasarım (Google Stitch):** Üç ana ekran (giriş, karar, son) ve bileşen kuralları. Kararlar [DESIGN.md](DESIGN.md) dosyasında.
2. **Oyun ve tutor (Google AI Studio):** [system_prompt.md](system_prompt.md) içinde, oyun akışını, sonuç kurallarını ve Sokratik tutor davranışını tanımlar. Oyun kurallarını bir model yönetir.
3. **Uygulama (Google AI Studio Build):** Tasarım ve sistem talimatını birleştirip telefonda açılan bir web uygulaması üretir. Yayınlanan link bu katmandan gelir.

Testler [Cypress](https://www.cypress.io/) ile yazıldı: [cypress/e2e/primer.cy.js](cypress/e2e/primer.cy.js).

### Oyun kuralları (özet)

- **Sistem ayakta:** (K1 = A) veya (K1 = B ve K2 = A)
- **KVKK ihlali:** K3 = B
- **İyi son:** Sistem ayakta ve KVKK ihlali yok.
- **Kötü son:** Diğer tüm durumlar. Metin duruma göre değişir.
- **Deneyimliyim modu:** Her karar için 60 saniye. Süre dolarsa B uygulanır.

## Çalıştırma

Testler için Node.js 22 kullanıldı (Node 24 ile Cypress çalışma sırasında takılıyor).

```bash
npm install
npm test
```

Farklı bir adres üzerinde test etmek için:

```bash
BASE_URL=https://se-primer-1-282987152472.europe-west2.run.app npm test
```

Videolar `cypress/videos/` klasörüne kaydedilir.

**Windows notu:** Proje yolunda ASCII olmayan karakter (ör. `İ`) varsa Cypress takılabiliyor. Bu durumda projeyi `C:\se-primer` gibi ASCII bir yola kopyalayıp orada çalıştırın. Testler Chrome ile çalıştırıldığında `npm test -- --browser chrome` kullanılabilir.

**Son sonuç:** 9 testten 9'u geçti (Node 22.23.4, Chrome 156, Cypress 13.17.0). Testler üç kararın 8 kombinasyonunu (4 farklı son) ve Deneyimliyim süre yolunu kapsar. Süre yaklaşık 2,5 dakika.

## Model (v2): takılma tahmini

Oyuncunun karar davranışından `ipucu_gerekti` olasılığını tahmin eden küçük bir model. Olasılık
0,50 ve üzerindeyse bir sonraki karar ekranında somut ipucu gösterilir (spec §8).

**Kurulum ve eğitim (3 komut, Python 3.14):**

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python train.py
```

macOS/Linux için `.venv/bin/pip` ve `.venv/bin/python` kullanın.

`train.py` tek komutla şunları yapar: 5 katlı çapraz doğrulama, eval kapısı, ONNX dışa aktarımı
ve ONNX ↔ sklearn eşdeğerlik kontrolü. Eşik altında kalan model `model/` klasörüne yazılmaz.

| Dosya | Ne |
|---|---|
| [data/oturumlar.csv](data/oturumlar.csv) | Karar satırları (`kaynak`: `gercek` veya `sentetik`) |
| [data/SOZLUK.md](data/SOZLUK.md) | Her sütunun tanımı ve sentetik üreticinin kuralı |
| [scripts/uret_sentetik.py](scripts/uret_sentetik.py) | Sentetik oturum üretici (tohum 13) |
| [train.py](train.py) | Eğitim ve eval kapısı |
| [model/](model/) | `model.onnx`, `config.json` (sözleşme), `README.md` (model kartı) |
| [tests/parite.py](tests/parite.py) → [tests/parite.json](tests/parite.json) | Python referans olasılıkları (5 girdi) |
| [cypress/e2e/parite.cy.js](cypress/e2e/parite.cy.js) | Tarayıcı ↔ Python parite testi (tolerans 1e-4) |
| [RELEASE.md](RELEASE.md) | Yayın kontrol listesi, commit'e sabit URL, geri alma, ödünleşim matrisi |

**Durum:** Eğitim hattı çalışıyor. Model yayında değil: gerçek oturum sayısı kontrol listesindeki
hedefin (15) altında. Şu ana kadar veri sentetik; bu sayılar yalnızca eğitim hattının çalıştığını
gösterir.

**Parite referansı (Python):** `.venv\Scripts\python tests\parite.py`

## Yapay zekâ araçlarının kullanımı

- **Google AI Studio (Gemini):** Oyunun akışı ve Sokratik tutor ([system_prompt.md](system_prompt.md)); Build uygulaması.
- **Claude Code (Anthropic):** `train.py`, `scripts/uret_sentetik.py`, `tests/parite.py`, Cypress testleri ve bu dokümanların ilk taslakları. `train.py`, `scripts/uret_sentetik.py` ve `tests/parite.py` çalıştırılarak doğrulandı. Parite testi (`cypress/e2e/parite.cy.js`) henüz uygulamanın yeni sürümünde çalıştırılmadı.
- **Elle düzeltilenler:** Cypress'teki hatalı varsayımlar (son düğme sırası ve Deneyimliyim doğrulaması) yeniden yazıldı. Tutor kuralına "seçenekleri karşılaştırma yok" maddesi elle eklendi.
- **Elle belirlenenler:** Eşikler (ROC-AUC 0,70; parite 1e-4), "yanlış seçim" tanımı (B seçeneği) ve sentetik üretici kuralı. Bunlar eğitimden önce spec'te sabitlendi.

## Yapılmayan üç özellik

1. **Kullanıcı hesabı ve giriş:** Kişisel veri saklama, KVKK yükümlülüğü ve güvenlik sorumluluğu getirdiği için eğitim senaryosu için gerekli değil.
2. **Native mobil uygulama (iOS ve Android):** Tarayıcıda çalışan tek bir sürüm telefonda da açılabiliyor, mağaza yayını ayrı bir süreç ve hesap gerektirdiği için bu ödevin kapsamı dışında.
3. **Kalıcı ilerleme ve liderlik tablosu:** Oyun ilerlemesini saklamak, gerçek kişisel veri tutma riskini artırır ve öğrenme hedefine katkısı yok; her oturum baştan başlar.

## Bilinen sınırlar

- **AI kotası:** Uygulama Gemini modelini kullanıyor. Günlük kota dolarsa tutor yanıt veremez.
- **Tutor testi:** Yayınlanan uygulamada tutora "Hangisi doğru, A mı B mi?" soruldu, cevap sızmadı (ayrıntı: [yayın testi](test/yayinlanan_uygulama_testi.md), bölüm 6). Eval ise AI Studio playground'da yapıldı.
- **Süre 60 saniye:** AI Studio sohbetinde süre sayılamaz, sayaç uygulama arayüzünde tutuluyor.
- **Tutor yanıt çeşitliliği:** Belirsiz mesajlara ("Bilmiyorum" ve "Hiçbir fikrim yok, yardım et") canlı tutor aynı yanıtı verebiliyor. Kural açısından sorun yok, ama yanıtın mesaja özgü olup olmadığı tam kontrol edilemedi (bkz. [yayın testi](test/yayinlanan_uygulama_testi.md), bölüm 6.1).

## Ekip

- Elif Hazar (geliştirme ve teslim)
