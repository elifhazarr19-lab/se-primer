# Tutor Değerlendirmesi: Özet

Bu dosya iki ayrı değerlendirmeyi tek yerde toplar. Ayrıntılar kendi raporlarında.

| Model | Tarih | Mesaj | Hatalı | Oran | Ana hata | Rapor |
|---|---|---|---|---|---|---|
| Gemini 3.8 Flash (düzeltme öncesi prompt) | 26 Ekim 2026 | 20 | 2 | %10 | Gerekçe cümlesi kesin karar sayıldı (SCP) | [rapor.md](rapor.md) |
| Gemini 3.8 Flash (düzeltilmiş prompt, 12 ve 13) | 26 Ekim 2026 | 2 | 0 | %0 (2 mesaj) | — | [rapor.md](rapor.md), bölüm 6 |
| Gemini 3.1 Flash Lite (düzeltilmiş prompt) | 26 Ekim 2026 | 20 | 1 | %5 | Mesaj 12 kesin karar sayıldı (SCP) | [rapor_gemini-3.1-flash-lite.md](rapor_gemini-3.1-flash-lite.md) |
| Gemini 3.8 Flash (düzeltilmiş prompt, tam tekrar) | 29 Ekim 2026 | 20 | 1 | %5 | Seçeneklerin artı ve eksisini yazdı (mesaj 18, kural 1) | [rapor.md](rapor.md), bölüm 6.2 |
| Gemini 3.8 Flash (kural 1 genişletildi, yalnızca mesaj 18 yeniden test) | 29 Ekim 2026 | 1 | 0 | %0 | Mesaj 18 düzeldi | [rapor.md](rapor.md), bölüm 6.3 |

## Sonuç

- **DAL (cevap sızıntısı):** Tüm testlerde 0. Hedef (%5'in altı) tutturuldu.
- **En sık hata:** Gerekçe cümlesinin karar sayılması (SCP). Düzeltilmiş prompt 3.8 Flash'ta bu hatayı giderdi (12 ve 13 numaralı mesajlar), ama Flash Lite'ta mesaj 12 yine hatalı çıktı.
- **Genel hedef (%10'un altı):** Flash Lite'ta %5 ile tutturuldu. 3.8 Flash'ta düzeltilmiş prompt ile yapılan kısmi testte de 0 hata.

## Açık konular

- 3.8 Flash'ta düzeltilmiş prompt ile 20 mesajın tamamı 29 Ekim 2026'da test edildi (bkz. rapor.md, bölüm 6.2). Sonuç: sızıntı 0, kural ihlali 1 (mesaj 18), sınırda 2.
- Mesaj 18 için kural genişletildi ve yalnızca bu mesaj yeniden test edildi, düzeldi. Diğer 19 mesaj yeni promptla tekrar test edilmedi.
- Flash Lite'ta mesaj 12 hatası tekrarlanabilir. Üç kez denemek gerekirse ayrıca test edilebilir.
- Hangi modelin uygulamada kullanılacağı henüz kesinleşmedi. Yayınlanan uygulama Gemini 3.8 Flash kullanıyor.
