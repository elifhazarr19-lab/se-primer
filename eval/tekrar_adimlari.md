# Tutor Eval Tekrarı: 20 Mesajın Tamamı (Gemini 3.8 Flash)

Amaç: Düzeltilmiş sistem promptu ile 20 mesajın tamamını yeniden test etmek. Önceki turda 1–7 ve 12–13 doğrulanmıştı, 8–11 ve 14–20 kalmıştı.

## Hazırlık

1. Google AI Studio'yu aç, modeli **Gemini 3.8 Flash** olarak seç.
2. Sağ paneldeki **System instructions** alanına [system_prompt.md](../system_prompt.md) dosyasının tamamını yapıştır.
3. **Grounding** kapalı olsun.
4. Geçici sohbet (Temporary chat) aç.

## Oyunu Karar 1'e getir

Her sohbette şu sırayla ilerle:

1. Seviye: **Yeni başladım**
2. Rol: **Geliştirici**
3. Hedef: **Mimari**
4. **Kriz Masasına Geç**, sonra **Müdahaleyi Başlat**

Oyun Karar 1'de olmalı. Tutor bu bağlamda cevap vermeli.

## Mesajları gönder

1. [tekrar_etiket_formu.csv](tekrar_etiket_formu.csv) dosyasındaki mesajları **1'den 20'ye** sırayla gönder. Her mesajdan sonra tutorun yanıtını kopyala.
2. Oyun Karar 2'ye geçerse (tutor yerine oyun ilerlerse), sohbeti sıfırla ve yukarıdaki adımlarla Karar 1'e geri getir. Önceki turda da böyle yapıldı.
3. Mesajları yazarken seçim kelimesi (sadece "A" ya da "B") gönderme. Bu oyunu ilerletir.

## Yanıtları kaydet

Her mesajın tutor yanıtını bana yapıştır, ya da `tutor_yaniti` sütununa kendin yapıştır. Yanıtlar gelince her biri için şunları işaretleyeceğim:

- Cevabı söyledi mi (sızıntı)?
- Tam olarak bir soru işareti var mı?
- Beklenen davranışla uyumlu mu?

Sonuçlar `eval/rapor.md` içinde yeni bir bölüm olarak yazılacak ve `RAPOR_OZET.md` güncellenecek.

## Not

Bu tekrar için AI Studio'nun günlük kotası yeterli olmalı. Kota dolarsa kaldığın mesajın numarasını söyle, kalanları ertesi gün devam ettiririz.
