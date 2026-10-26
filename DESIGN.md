# SE Primer: DESIGN.md

> YZM301 · Ödev 1 · Adım 2 / 6 (Google Stitch)
> Kaynak: [spec.md](spec.md). Bu dosya spec'teki kabul kriterlerini (AK-1…AK-5) ekran ve bileşen düzeyine indirir.

## 1. Tasarım İlkeleri

1. **Telefon önce.** Tek sütun, 390 × 844 px referans çerçeve. Yatay kaydırma yok.
2. **Karar öne çıksın.** Her ekranda tek bir birincil eylem vardır. Seçenekler A/B olarak büyük kartlarda sunulur.
3. **Sonuç her zaman görünür.** Sistem durumu ve veri durumu her ekranın üst şeridinde durur. Oyuncu sonucu tahmin etmek zorunda kalmaz.
4. **Renk tek başına bilgi taşımaz.** Ayakta / çöktü, güvende / ihlal ikonla ve metinle de belirtilir (erişilebilirlik).
5. **Tutor görünür ama baskın değildir.** Tutor balonu karar kartının altında yer alır; cevap değil soru gösterir.

## 2. Görsel Dil

Ödevin kapak görselinden türetilmiştir: lacivert gece, sıcak turuncu aksan, krem zemin, eski kitap estetiği.

### 2.1 Renk tokenları

| Token | Hex | Kullanım |
|---|---|---|
| `--color-ink-navy` | `#13213D` | Üst şerit, birincil yüzey, metin (açık zemin üzerinde) |
| `--color-accent-amber` | `#E08A2E` | Birincil vurgu, karar numarası, ilerleme çubuğu |
| `--color-accent-rust` | `#B5532A` | Kötü son sınırı, uyarı çerçevesi |
| `--color-paper` | `#F7F5F0` | Sayfa zemini |
| `--color-card` | `#FFFDF8` | Kart zemini |
| `--color-line` | `#D9D4C7` | Kart kenarlığı, ayırıcılar |
| `--color-ok-bg` | `#E3EEF9` | İyi son (Son A) zemini |
| `--color-ok-line` | `#2B6CB0` | İyi son çerçevesi ve ikonu |
| `--color-bad-bg` | `#FBE9DC` | Kötü son (Son B) zemini |
| `--color-muted` | `#5B6475` | İkincil metin (en az 4.5:1 kontrast) |

Karanlık tema bu sürümde yoktur. Tek tema, tek karar.

### 2.2 Tipografi

| Rol | Font (Stitch) | Boyut / satır | Ağırlık |
|---|---|---|---|
| Başlık (H1) | Georgia / serif yedek | 30 / 36 px | 700 |
| Alt başlık (H2) | Georgia / serif yedek | 22 / 28 px | 700 |
| Gövde | Inter / sans-serif yedek | 16 / 24 px | 400 |
| Etiket, küçük metin | Inter | 13 / 18 px | 600 |
| Zaman göstergesi | Inter, tabular nums | 40 / 44 px | 700 |

Türkçe karakterler (ğ, ş, ı, İ) test edilmelidir. Font seçiminde Türkçe destek zorunludur.

### 2.3 Boşluk ve şekil

- Yan boşluk: 16 px. Kart iç boşluğu: 16 px. Kartlar arası: 12 px.
- Köşe yarıçapı: kart 16 px, buton 12 px, chip 999 px (tam yuvarlak).
- Dokunma hedefi: en az 44 × 44 px.
- Gölge: yalnızca kararı seçili kartta, `0 4px 12px rgba(19,33,61,0.12)`.

## 3. Ekran 1: Giriş / Onboarding

**Amaç:** Oyuncunun seviyesini, rolünü ve hedefini öğrenmek. Spec §4.1 ve AK-1, AK-2 bu cevaplara dayanır.

### 3.1 Yerleşim (yukarıdan aşağıya)

1. **Kapak alanı (üst %35):** Lacivert zemin. Kitap çizimi veya ödevdeki kapak görselinin sade bir versiyonu. Başlık "SE Primer", altında tek satır: "Dün gece yeni sürüm çıktı. Sen nöbetçisin."
2. **İlerleme göstergesi:** "1 / 3 · Seviye, Rol, Hedef" üç noktalı stepper. Aktif nokta turuncu.
3. **Soru 1: Seviye** (tek seçim, 2 seçenek, yan yana kart)
   - Yeni başladım · "Her kararda ipucu görürsün."
   - Deneyimliyim · "Karar başına 60 saniye. İpucu yok."
4. **Soru 2: Rol** (tek seçim, 3 seçenek, dikey liste)
   - Geliştirici / Test mühendisi / Proje yöneticisi
5. **Soru 3: Hedef** (tek seçim, 3 seçenek, dikey liste)
   - Mimari / Test / KVKK
6. **Birincil buton (sabit alt):** "Krize başla". Üç soru cevaplanana kadar pasif (`disabled`, %40 opaklık). Pasif iken altında "Üç soruyu da yanıtla" yazar.

### 3.2 Davranış

- Seçim yapıldığında kart amber çerçeve alır ve ilerleme noktası dolar.
- Soru 1'de "Deneyimliyim" seçilince kart altında küçük uyarı: "Süre baskısı açık."
- Soruları geri almak için üstte "‹ Geri" bulunur. Son soruda aktif değildir.
- Geçişler yatay kaydırmalı, 250 ms.

### 3.3 Bileşenler

`OnboardingStepper`, `ChoiceCard` (tek / dikey varyant), `PrimaryButton`, `HelperText`

## 4. Ekran 2: Oyun Sahnesi / Karar

**Amaç:** Her üç karar için aynı yapı. Oyuncu durumu okur, seçer, sonucu görür, tutora soru sorar. Spec §4.2 ve §4.4, AK-1 ila AK-4 buraya bağlanır.

### 4.1 Yerleşim (yukarıdan aşağıya)

1. **Durum şeridi (lacivert, sabit üst, 56 px):**
   - Sol: saat "08:00" (yukarı sayar, ör. 08:07)
   - Orta: "Karar 1 / 3" ve üç noktalı stepper
   - Sağ: iki chip: "Sistem: ayakta" (yeşil ikon) ve "Veri: güvende" (mavi kilit ikonu). Olumsuz durumda chip kırmızımsı `--color-bad-bg` zemine geçer ve metin "Sistem: çöktü" olur.
2. **Kriz kartı (yalnızca Karar 1'de, sonra daralır):** Kısa senaryo metni. "Dün gece yeni sürüm çıktı. 300 hasta bekliyor." Karar 2 ve 3'te tek satıra iner, "Önceki durumu göster" ile açılır.
3. **Sayaç (yalnızca Deneyimliyim):** Sağ üstte dairesel 60 saniye sayacı (`TimerRing`). Son 10 saniyede halka kızıl renge döner ve titreşir. Süre dolunca karar kartları kilitlenir ve "Süre doldu, ekip B'yi uyguladı" bildirimi çıkar.
4. **Karar kartı (ana alan):**
   - Başlık: "KARAR 1 · MİMARİ" (amber etiket)
   - Soru cümlesi: "Canlı sistem çöktü. Ne yaparsın?"
   - İki büyük seçenek kartı, dikey: **A)** Eski sürüme geri dön / **B)** Canlıda yama yap. Her kartta bir satırlık alt metin: "Bilinen son çalışan sürüm." / "Hızlı ama test edilmemiş."
   - Alt metin, spec'teki seçenek etiketlerine birebir uyar. Ek bilgi cümleleri oyuncuyu yönlendirmemelidir.
5. **İpucu balonu (yalnızca Yeni başladım):** Karar kartının hemen altında, otomatik açık. Tutor avatarı ve kısa metin, en fazla bir soru. Örnek: "Geri dönmeden önce veritabanı şemasının değişip değişmediğini nasıl anlarsın?"
   - Deneyimliyim modunda bu balon hiç gösterilmez (ipucu yok, spec §4.1). Tutora soru sorma alanı (aşağıdaki 6. madde) iki modda da açıktır; Deneyimliyim'de sayaç çalışırken de kullanılabilir. Tutor yanıtı kısa olur (spec §4.5).
6. **Tutor girişi (alt):** Metin alanı "Tutora bir soru sor…" + gönder ikonu. Tutor yanıtı balon olarak gelir; cevap yerine soru içerir.
7. **Sonuç paneli (karar verildikten sonra, alttan kayarak açılır):** Spec §4.4'teki dört bilgi, dört satır:
   - Seçtiğin: **A · Eski sürüme geri dön**
   - Sistem: ayakta / çöktü (ikon + metin)
   - Veri: güvende / ihlal (ikon + metin)
   - Neden: 1-2 cümle
   - Birincil buton: "Sonraki karar" (Karar 3'te "Sonucu gör")

### 4.2 Durumlar

| Durum | Görünüm |
|---|---|
| Karar bekliyor | Her iki seçenek aktif. Sonuç paneli gizli. |
| Seçim yapıldı, geri sayım | Seçilen kart amber çerçeveli, diğeri %50 opak. Alt kısımda "Geri al" bandı ve 3 sn'lik çubuk. |
| Geri alındı | Band kapanır, kartlar yeniden aktif olur. Karar aynı şekilde yeniden sorulur. |
| Seçim kesinleşti | Band kapanır, sonuç paneli alttan açılır. |
| Süre doldu (Deneyimliyim) | Kartlar kilitli, B vurgulanır, "Süre doldu" bandı. |
| Tutor yükleniyor | Üç nokta animasyonu, en fazla 3 sn. Sonra "Bir daha dene" metni. |
| Tutor cevap vermeye zorlandı | Yanıt ipucunu bir adım somutlaştırır. UI değişmez. |

### 4.3 Bileşenler

`StatusBar`, `StatusChip`, `ScenarioCard` (genişlemeli), `TimerRing`, `DecisionCard` (A/B varyantı), `UndoBanner` (3 sn geri sayım), `HintBubble`, `TutorChatInput`, `TutorMessage`, `ResultPanel`, `ProgressStepper`, `Banner` (süre doldu)

### 4.4 Etkileşim kuralları

- Karar seçimi onay ister mi? **Hayır.** Tek dokunuşla seçim yapılır, ama kesinleşmez. Seçimden sonra ekranın altında 3 saniyelik "Geri al" bandı belirir (geri sayım çubuğuyla). Band dolmadan dokunulursa seçim iptal edilir ve karar yeniden açılır. Band dolunca seçim kesinleşir ve sonuç paneli açılır. Bu kural üç kararın hepsinde geçerlidir (spec §4.4).
- Geri sayım sırasında da sayaç (Deneyimliyim) çalışmaya devam eder.
- Karar sonrası kart geçişi: kart sola kayar, bir sonraki kart sağdan girer, 250 ms.
- Sayaç ekranda görünürken oyuncu tutora yazabilir; süre durmaz.

## 5. Ekran 3: Sonuç / Final

**Amaç:** İki sondan birini göstermek ve kararların zincirini özetlemek. Spec §4.3 ve AK-5.

### 5.1 Son A · İyi

- Üst banner, mavi (`--color-ok-bg`, `--color-ok-line`): "08:25 · Sistem ayakta, veri güvende."
- Büyük saat: "08:25" (amber, tabular nums)
- Üç karar özeti, her biri bir satır chip: "Mimari: Geri dönüldü", "Test: Kısa test koşuldu", "KVKK: Maskelendi"
- Kısa değerlendirme: "Kararların birbirini nasıl etkilediğini düşün." (Tutor'dan değil, sabit metin. Yargı içermez.)

### 5.2 Son B · Kötü

- Üst banner, kırmızımsı (`--color-bad-bg`, `--color-accent-rust`): "Oyun bitti · Sistem ayakta ama KVKK ihlali" veya "Sistem çöktü" veya "Sistem çöktü ve KVKK ihlali" (spec §4.3 tablosuna göre metin değişir, ama her varyant "KVKK" veya "çöküş" içerir, AK-5 gereği KVKK ihlali varsa mutlaka belirtilir)
- Ne oldu paragrafı: en fazla 3 cümle, hangi kuralın ihlal edildiği.
- Üç karar özeti aynı chip yapısında, ihlal eden karar kırmızı çerçeveli.

### 5.3 Ortak alt bölüm

- Birincil buton: "Yeniden oyna" (oturumu sıfırlar, Ekran 1'e döner)
- İkincil buton: "Kararları gözden geçir" (Ekran 2'ye geçmeden önce sonuç panellerini salt okunur gösterir)
- Metin: "Bu oturumda kayıt tutulmaz." (KVKK ve kapsam gereği, spec §3.1)

### 5.4 Bileşenler

`EndingBanner` (A/B varyantı), `BigClock`, `DecisionSummaryChip`, `ReflectionText`, `PrimaryButton`, `SecondaryButton`, `PrivacyNote`

## 6. Erişilebilirlik ve Teknik Notlar

- Tüm metin kontrastı WCAG AA (en az 4.5:1). `--color-muted` üzerinde kontrol edilmelidir.
- Her kart `role="button"` ve `aria-pressed` ile işaretlenir. Süre sayacı `aria-live="polite"` ile yalnızca son 10 saniyede duyurulur.
- Tutor balonu `aria-live="polite"` alanına yazılır.
- Hareket azaltma tercihi (`prefers-reduced-motion`) açıksa kayma animasyonları kaldırılır.
- Sayaç: Deneyimliyim'de yalnızca 60 sn; diğer modda DOM'da hiç yer almaz.

## 7. Stitch İçin Üretim İstemleri (İngilizce)

Stitch'e her ekranı ayrı ayrı vermek için. Çıktıyı Stitch'te düzenledikten sonra bu dosyadaki kararlarla çelişiyorsa dosya esas alınır.

**Ekran 1: Onboarding**
> Mobile app onboarding screen, 390×844. Dark navy (#13213D) hero at the top with a serif title "SE Primer" and a short subtitle in Turkish: "Dün gece yeni sürüm çıktı. Sen nöbetçisin." Below, a three-dot step indicator labeled "1 / 3". Three single-select question groups: "Seviye" (two side-by-side cards: "Yeni başladım", "Deneyimliyim"), "Rol" (three stacked cards), "Hedef" (three stacked cards). Warm off-white background (#F7F5F0), cards in #FFFDF8 with #D9D4C7 borders, amber accent (#E08A2E) for selected state. Sticky bottom primary button "Krize başla", disabled state at 40% opacity. Sans-serif body (Inter), serif headings. 16px side margins, 44px minimum touch targets.

**Ekran 2: Karar sahnesi**
> Mobile game decision screen, 390×844. Top status bar in navy (#13213D) with clock "08:07", a stepper "Karar 1 / 3", and two status chips: "Sistem: ayakta" with a green check icon and "Veri: güvende" with a blue lock icon. Below, a scenario card: "Dün gece yeni sürüm çıktı. 300 hasta bekliyor." Main decision card with amber label "KARAR 1 · MİMARİ" and question "Canlı sistem çöktü. Ne yaparsın?" Two large stacked option cards: "A) Eski sürüme geri dön" with subtitle "Bilinen son çalışan sürüm." and "B) Canlıda yama yap" with subtitle "Hızlı ama test edilmemiş." Below, a tutor chat bubble with a small avatar and text "Geri dönmeden önce veritabanı şemasının değişip değişmediğini nasıl anlarsın?" and a bottom text input "Tutora bir soru sor…". Warm off-white background, card style with 16px radius, subtle shadow on selected card only. Turkish UI text. After a choice is made, show a bottom snackbar with the text "Geri al" and a thin 3-second countdown bar. Include a variant with a circular 60-second timer in the top right corner, and a variant showing a bottom sheet "Ne oldu / Neden oldu" with four rows: decision, system status, data status, reason.

**Ekran 3: Sonuç**
> Mobile game ending screen, 390×844, two variants. Variant A (good): light blue banner (#E3EEF9) with blue border (#2B6CB0), large amber clock "08:25", text "Sistem ayakta, veri güvende", three summary chips, short reflection text, primary button "Yeniden oyna" and secondary button "Kararları gözden geçir", small privacy note "Bu oturumda kayıt tutulmaz." Variant B (bad): rust-tinted banner (#FBE9DC) with rust border (#B5532A), text "Sistem ayakta ama KVKK ihlali", the violating decision chip with a red outline, same buttons. Warm off-white background, serif headline, sans body, 16px margins.

## 8. Onaylanan Kararlar

- **Geri al bandı (3 sn):** Onaylandı. Üç karar için de geçerli (bkz. §4.4).
- **Tutora sorma alanı:** Onaylandı. İki seviyede de açık (bkz. §4.1 ve spec §4.5).
- **Son B metni:** Spec §4.3'e göre Son B tek son, metni üç duruma göre değişir (KVKK / çöküş / ikisi). Tek ekran, üç metin varyantı.
