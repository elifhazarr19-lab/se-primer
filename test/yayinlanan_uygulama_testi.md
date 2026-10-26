# Yayınlanan Uygulama Testi (manuel, tarayıcı)

> Link: https://se-primer-1-282987152472.europe-west2.run.app/
> Tarih: 26 Ekim 2026 · Ekran: masaüstü tarayıcı, telefon genişliğinde pencere
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
| "Süre doldu" mesajı gösteriliyor mu (AK-2) | Sonuç ekranında mesaj görünmedi | **Eksik** |
| Süre içinde verilen seçimler | Karar 2 (A), Karar 3 (A) | Geçti |
| Son | K1: B, K2: A, K3: A → "Kusursuz Müdahale: Sistem Ayakta, Veri Güvende!" | Geçti (spec kuralıyla uyumlu) |

## 4. Test edilmeyenler

- "Emin değil misin? Sokratik AI Tutor'a danış" düğmesi ve tutor yanıtları (yayınlanmış uygulamada).
- "Sistem çöktü" varyantları (K1=B ve K2=B).
- Kayıtlı yeniden oynama davranışı (Yeniden Oyna düğmesi çalıştı, ama ayrıntılı kontrol yapılmadı).

## 5. Bilinen sorunlar

1. **"Süre doldu" mesajı yok** (AK-2 eksik). Düzeltme: Build'de süre dolduğunda sonuç kartına "Süre doldu, ekip B seçeneğini uyguladı" metni eklenmeli.
2. **AI kotası:** Uygulama Gemini 3.8 Flash kullanıyor. Kota dolarsa tutor çalışmaz.
