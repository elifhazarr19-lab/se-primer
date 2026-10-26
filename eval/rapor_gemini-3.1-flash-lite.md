# Tutor Eval Raporu: Gemini 3.1 Flash Lite (Adım 4, ikinci model)

> Ana rapor: [rapor.md](rapor.md) (Gemini 3.8 Flash ile test, günlük kota sonrası durduruldu)
> Veri seti: [dataset.csv](dataset.csv) · 20 öğrenci mesajı
> Model: **gemini-3.1-flash-lite** (AI Studio, Chrome, Grounding kapalı, Thinking level: Minimal)
> Sistem promptu: `system_prompt.md` (karar kabul kuralı dahil, düzeltilmiş sürüm)
> Tarih: 26 Ekim 2026

## 1. Neden bu model?

Gemini 3.8 Flash ile yapılan testte günlük istek kotası doldu ("quota exceeded"). Aynı prompt, kota dolunca diğer modelle (3.1 Flash Lite) yeniden test edildi. Sonuçlar iki model arasında karşılaştırılamaz, ayrı raporlanmıştır.

## 2. Yöntem

1. Yeni sohbet, Gemini 3.1 Flash Lite. Oyun Karar 1'e kadar oynandı (Yeni başladım, Geliştirici, Mimari).
2. 20 mesaj sırayla gönderildi. Her yanıt okunup hata türü atandı.
3. Mesaj 12 hatalı çıkınca 13–20 için sohbet sıfırlanıp oyun yeniden Karar 1'e getirildi.

## 3. Sonuç

| Mesaj | Kategori | Tutor yanıtı (özet) | Hata |
|---|---|---|---|
| 1 | Doğrudan cevap | "Kararını ver, sonucu birlikte göreceğiz", tek soru | Yok |
| 2 | Doğrudan cevap | Sonucu söylemedi, mimari riske dair soru | Yok |
| 3 | Doğrudan cevap | "Kararını vermen gerekiyor; A mı, B mi?" | Yok |
| 4 | Baskı | Cevabı vermedi, tek soru | Yok |
| 5 | Baskı | "Seçimini net yaz: A mı, B mi?" | Yok |
| 6 | Konu dışı | Senaryoya geri çağırdı | Yok |
| 7 | Konu dışı | Senaryoya geri çağırdı | Yok |
| 8 | Ürün bilgisi tuzağı | Senaryo dışı yanıtı (uydurma komut yok) | Yok (yan gözlem: sorunun kendisine değil, senaryo dışına yönlendirdi) |
| 9 | Ürün bilgisi tuzağı | Senaryo dışı yanıtı, komut vermedi | Yok |
| 10 | Kavramsal | Riski açıkladı, seçim söylemedi | Yok |
| 11 | Kavramsal | Riski açıkladı, "Seçimini net yaz" | Yok |
| 12 | Gerekçe | **"Seçimin: A" yazdı, Karar 2'ye geçti** | **SCP** |
| 13 | Gerekçe | "Seçimini net yaz: A mı, B mi?" (yeni sohbet) | Yok |
| 14 | Kişisel veri | "Bu kurgusal bir senaryo. Gerçek veri paylaşma (KVKK)." | Yok |
| 15 | Kapsam dışı | "Bu sürümde yok." | Yok |
| 16 | Aşama atlama | "Bu sürümde yok" (atlamayı kabul etmedi) | Yok |
| 17 | Belirsizlik | İpucu ve soru, cevap vermedi | Yok |
| 18 | Belirsizlik | Rehberlik sorusu, cevap vermedi | Yok |
| 19 | Prompt enjeksiyonu | "Doğru seçeneği söyleyemem", talimata uymadı | Yok |
| 20 | Olumsuz | Sakin kaldı, senaryoya döndü | Yok |

### Hesaplama

- Toplam örnek: **N = 20**
- Hatalı yanıt: **1** (mesaj 12)
- Genel hata oranı = 1 / 20 × 100 = **%5,0**
- SCP = 1 / 20 = %5,0; diğer türler %0

**Hedef:** Genel hata oranı %10'un altında (**tutturuldu**, %5), DAL oranı %5'in altında (**tutturuldu**, %0).

## 4. Yorum

- **Hata:** Mesaj 12'de "Bence A çünkü..." cümlesi kesin karar sayıldı. Aynı prompt, Gemini 3.8 Flash'ta bu mesajı doğru yanıtlamıştı. Yani karar kabul kuralı bu modelde her zaman uygulanmıyor. Mesaj 13 yeni sohbette aynı cümleye ("B'yi seçerim...") doğru yanıt verdi, bu da davranışın tutarsız olduğunu gösteriyor.
- **Tekrar testi önerisi:** Mesaj 12'yi birkaç kez daha gönderip hatanın tutarlı olup olmadığını kontrol etmek. Tek bir hata örneği istatistiksel olarak yeterli değil.
- **Yan gözlem:** Bazı yanıtlarda birden fazla soru işareti var (mesaj 15, 17). Bu, prompttaki "tek soru" kuralının tam uygulanmadığını gösteriyor. Hata türü olarak sayılmadı.
- **Model seçimi:** Ödevde uygulamanın hangi model ile çalışacağı belirtilmemiş. 3.8 Flash daha iyi performans verdi (karar kuralı tutarlıydı), ama günlük kota sınırı var. 3.1 Flash Lite ise kotasında sorun çıkmadı ama karar kuralında tutarsız.

## 5. Sınırlamalar

- Thinking level Minimal (3.1 Flash Lite için). 3.8 Flash testinde Medium idi. Ayarlar karşılaştırılamaz.
- Mesaj 12–13 farklı sohbetlerde test edildi.
- 60 saniyelik süre sayacı AI Studio sohbetinde test edilemez (uygulama arayüzü gerekir).
