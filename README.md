# SE Primer

YZM301 Yazılım Gerçekleme ve Test dersi, Ödev 1.

SE Primer, sağlık sektöründe geçen bir kriz senaryosunu (sabah 08:00'de çöken randevu sistemi) oynanabilir bir uygulamaya dönüştürür. Oyuncu nöbetçi mühendis olarak üç karar verir (mimari, test, KVKK). Her kararın teknik sonucu ve nedeni gösterilir. Arkada çalışan Sokratik AI Tutor cevabı söylemez, soru sorarak düşündürür.

## Bağlantılar

- **Yayınlanan uygulama:** https://se-primer-1-282987152472.europe-west2.run.app/
- **Spesifikasyon:** [spec.md](spec.md)
- **Tasarım:** [DESIGN.md](DESIGN.md), ekran görüntüleri: [tasarim/](tasarim/)
- **Tutor sistem promptu:** [system_prompt.md](system_prompt.md)
- **Tutor değerlendirmesi:** [eval/](eval/)
- **Yayın testi:** [test/yayinlanan_uygulama_testi.md](test/yayinlanan_uygulama_testi.md)
- **Demo videosu (56 sn):** [test/demo.mp4](test/demo.mp4)

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

**Son sonuç:** 3 testten 3'ü geçti (Node 22.23.4, Chrome 156, Cypress 13.17.0). Test süresi yaklaşık 1,5 dakika.

## Yapılmayan üç özellik

1. **Kullanıcı hesabı ve giriş:** Kişisel veri saklama, KVKK yükümlülüğü ve güvenlik sorumluluğu getirdiği için eğitim senaryosu için gerekli değil.
2. **Native mobil uygulama (iOS ve Android):** Tarayıcıda çalışan tek bir sürüm telefonda da açılabiliyor, mağaza yayını ayrı bir süreç ve hesap gerektirdiği için bu ödevin kapsamı dışında.
3. **Kalıcı ilerleme ve liderlik tablosu:** Oyun ilerlemesini saklamak, gerçek kişisel veri tutma riskini artırır ve öğrenme hedefine katkısı yok; her oturum baştan başlar.

## Bilinen sınırlar

- **AI kotası:** Uygulama Gemini modelini kullanıyor. Günlük kota dolarsa tutor yanıt veremez.
- **Tutor testi:** Yayınlanan uygulamada tutora "Hangisi doğru, A mı B mi?" soruldu, cevap sızmadı (ayrıntı: [yayın testi](test/yayinlanan_uygulama_testi.md), bölüm 6). Eval ise AI Studio playground'da yapıldı.
- **Süre 60 saniye:** AI Studio sohbetinde süre sayılamaz, sayaç uygulama arayüzünde tutuluyor.

## Ekip

- Elif Hazar (geliştirme ve teslim)
