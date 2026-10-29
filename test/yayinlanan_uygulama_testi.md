# Yayınlanan Uygulama Testi (manuel, tarayıcı)

> Link: https://se-primer-1-282987152472.europe-west2.run.app/
> Tarih: 26 Ekim 2026 · Güncellendi: 29 Ekim 2026 (Süre doldu mesajı ve Cypress sonucu) · Ekran: masaüstü tarayıcı, telefon genişliğinde pencere
> Kapsam: Spec §4 ve §5 (AK-1 … AK-5)

## 1. Seviye: Yeni başladım (iyi son yolu)

| Adım | Seçim | Sonuç | Durum |
|---|---|---|---|
| Giriş | Yeni başladım, Geliştirici, Mimari | Kriz ekranına geçildi | Geçti |
| Karar 1 | A (Eski sürüme geri dön) | Sistem ayakta, veri güvende; "Geri Al" bandı 3 sn | Geçti |
| Karar 2 | A (Önce kısa test koş) | Sistem ayakta, veri güvende | Geçti |
| Karar 3 | A (Hasta adlarını maskele) | Sistem ayakta, veri güvende; KVKK gerekçesi | Geçti |
| Son | — | "Kusursuz Müdahale: Sistem Ayakta, Veri Güvende!" | Geçti |

İpucu kutusu her karar ekranında göründü (AK-1).

## 2. Seviye: Yeni başladım (kötü son yolu)

| Adım | Seçim | Sonuç | Durum |
|---|---|---|---|
| Karar 1 | A | Sistem ayakta | Geçti |
| Karar 2 | A | Sistem ayakta | Geçti |
| Karar 3 | B (Logu ekibe olduğu gibi at) | Sistem ayakta, KVKK ihlali | Geçti |
| Son | — | "Sistem Ayakta Ama KVKK İhlali!" (K1: A, K2: A, K3: B) | Geçti |

## 3. Seviye: Deneyimliyim (süre yolu)

| Kontrol | Sonuç | Durum |
|---|---|---|
| 60 saniyelik sayaç görünüyor mu (AK-2) | "Karar Sayacı (Deneyimli)" 60 sn'den geri sayıyor | Geçti |
| İpucu kapalı mı | Karar ekranında ipucu kutusu yok | Geçti |
| Süre dolunca B uygulanıyor mu | Karar 1'e cevap verilmedi; B ("Canlıda yama yap") otomatik uygulandı, sonuç ekranı açıldı | Geçti |
| "Süre doldu" mesajı gösteriliyor mu (AK-2) | Republish sonrası görünüyor: "Süre doldu. Ekip B seçeneğini uyguladı." | Geçti |
| Süre içinde verilen seçimler | Karar 2 (A), Karar 3 (A) | Geçti |
| Son | K1: B, K2: A, K3: A → "Kusursuz Müdahale: Sistem Ayakta, Veri Güvende!" | Geçti (spec kuralıyla uyumlu) |

## 4. Test edilmeyenler

- Kayıtlı yeniden oynama davranışı: "Yeniden Oyna" düğmesine basıldığında oyunun sıfırlanıp sıfırlanmadığı ayrıca test edilmedi. Cypress yalnızca son ekranda düğmenin göründüğünü kontrol ediyor.

Not: Tutor (bölüm 6, 6.1) ve "Sistem çöktü" yolları (Cypress: K1=B, K2=B) artık test edildi.

## 5. Bilinen sorunlar

1. **"Süre doldu" mesajı (AK-2): çözüldü.** Build'e eklendi, Republish sonrası canlı sürümde görünüyor ve Cypress testi bunu doğruluyor.
2. **AI kotası:** Uygulama Gemini 3.8 Flash kullanıyor. Kota dolarsa tutor çalışmaz.

## 6. AI Tutor (yayınlanan uygulama, 26 Ekim 2026)

| Kontrol | Sonuç | Durum |
|---|---|---|
| Tutor açılıyor mu (Karar 1, "Emin değil misin?" düğmesi) | Açıldı, ilk mesaj geldi | Geçti |
| "Hangisi doğru, A mı B mi?" sorusu | Cevap söylenmedi, ipucu + tek soru ("Seçimini net yaz: A mı, B mi?") | Geçti |
| Model | Gemini 3.8 Flash (uygulamanın kullandığı model) | — |

### 6.1 Republish sonrası tekrar (29 Ekim 2026, canlı)

Tutor kuralı güncellendi (AI TUTOR KURALLARI 1 ve 12: seçenekleri karşılaştırma yasağı, tek soru) ve Build'de Republish yapıldı. Aynı iki mesaj canlı sitede yeniden gönderildi.

| Mesaj | Republish öncesi | Republish sonrası | Durum |
|---|---|---|---|
| "Hiçbir fikrim yok, yardım et" | "Daha az risk taşır" diyerek iki seçeneğin riskini karşılaştırdı. İki soru işareti var | "Kriz anında bir kesintiye müdahale ederken zaman kısıtı ile sistem kararlılığı arasındaki dengeyi nasıl kurarsın?" Karşılaştırma yok, tek soru | Geçti |
| "Bilmiyorum" | Aynı ipucu metnini verdi | Mesaj 18 ile birebir aynı yanıt. Seçenek karşılaştırması yok, tek soru | Kısmen: kural geçti, yanıt mesaja özgü değil |

**Not:** Mesaj 17'de canlı tutor her iki belirsiz mesaja aynı yanıtı verdi. Kural açısından sorun yok, ama yanıtın mesaja bağlı üretilip üretilmediği bu testle ayrılamadı. Ayrıntılı kontrol için farklı bir belirsiz ifade denenebilir.

## 7. Güncel durum (29 Ekim 2026)

- **"Süre doldu" mesajı:** Yayında. Canlı sitenin kodunda metin var ve Deneyimliyim sonuç kartında görünüyor.
- **Cypress (Node 22.23.4, Chrome 156, Cypress 13.17.0):** 9 testten 9'u geçiyor. Test dosyası: `cypress/e2e/primer.cy.js`.
  - Üç kararın 8 kombinasyonu (K1, K2, K3): hepsi geçti. Dört farklı son: iyi son, sistem ayakta ama KVKK ihlali, sistem çöktü, sistem çöktü ve KVKK ihlali
  - Deneyimliyim, süre dolumu ve "Süre doldu" uyarısı: geçti (yaklaşık 65 sn)
- **Demo videosu:** [test/demo.mp4](demo.mp4), 56 sn. Akış [demo_senaryosu.md](demo_senaryosu.md) ile aynı. Kayıt Cypress ile 390x844 ekranda alındı, telefon kaydı değil.
