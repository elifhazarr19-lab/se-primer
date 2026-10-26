# Stitch Düzeltme İstemleri (spec'e uyum)

Her istemi Stitch'te ilgili ekran seçiliyken ayrı ayrı gönder. Önce 1. ekran, sonra 2 ve 3.

## 1. Giriş ekranı

> Edit the onboarding screen to match this spec exactly. Keep the navy hero, title "SE Primer" and subtitle "Dün gece yeni sürüm çıktı. Sen nöbetçisin." Remove all extra descriptions and icons. Question groups with exactly these options: "Seviye": "Yeni başladım" (subtitle: "Her kararda ipucu görürsün."), "Deneyimliyim" (subtitle: "Karar başına 60 saniye. İpucu yok."). "Rol": "Geliştirici", "Test mühendisi", "Proje yöneticisi" (no subtitles). "Hedef": "Mimari", "Test", "KVKK" (no subtitles). Bottom button "Krize başla". All UI text in Turkish.

## 2. Karar sahnesi

> Edit the decision screen to match this spec exactly. Remove time estimates ("Tahmini süre"), risk badges ("Yüksek Risk"), the "Vaka Danışmanı" label and any extra metrics or text not listed here. Top bar: clock "08:07", stepper "Karar 1 / 3", chips "Sistem: ayakta" and "Veri: güvende". Scenario card: "Dün gece yeni sürüm çıktı. 300 hasta bekliyor." Amber label "KARAR 1 · MİMARİ", question "Canlı sistem çöktü. Ne yaparsın?". Two option cards with exactly these labels and no extra text: "A) Eski sürüme geri dön" and "B) Canlıda yama yap". Tutor card titled "Tutor", with the message "Geri dönmeden önce veritabanı şemasının değişip değişmediğini nasıl anlarsın?" and input "Tutora bir soru sor…". Bottom snackbar "Geri al" with a 3-second countdown bar. All UI text in Turkish.

## 3a. Sonuç: iyi son

> Edit the good ending screen to match this spec exactly. Remove points (+40, +50), the "Kazanılan Yetkinlik" card, all metrics (erişilebilirlik, veri kaybı, KVKK uyumu), the simulation evaluation, incident codes and timelines. Keep only: light blue banner (#E3EEF9) with blue border (#2B6CB0), large amber clock "08:25", text "Sistem ayakta, veri güvende", three summary chips "Mimari: Geri dönüldü", "Test: Kısa test koşuldu", "KVKK: Maskelendi", reflection text "Kararların birbirini nasıl etkilediğini düşün.", buttons "Yeniden oyna" and "Kararları gözden geçir", small note "Bu oturumda kayıt tutulmaz." All UI text in Turkish.

## 3b. Sonuç: kötü son

> Edit the bad ending screen to match this spec exactly. Remove points, metrics, the simulation evaluation, learning cards, timelines and incident codes. Keep only: rust-tinted banner (#FBE9DC) with rust border (#B5532A), label "Oyun bitti", text "Sistem ayakta ama KVKK ihlali", a short 2-3 sentence explanation of which rule caused the ending, the three decision chips with the violating decision outlined in red, buttons "Yeniden oyna" and "Kararları gözden geçir", small note "Bu oturumda kayıt tutulmaz." All UI text in Turkish.
