# Build istemi 1: Veri Toplama Modu (şimdi)

Bu metni SE Primer AI Studio Build sohbetine olduğu gibi yapıştır. Ardından uygulamayı yeniden
yayınla (Republish).

---

Mevcut uygulamayı koru. Tüm metinler, düğmeler, karar seçenekleri, sonuç ekranları, Deneyimliyim
60 saniyelik sayaç ve "Süre doldu" mesajı aynı kalsın. Yalnızca aşağıdaki eklemeleri yap:

1. **Giriş ekranına onay kutusu ekle.** Metin: "Veri toplama modu (araştırma)". Altına küçük
   bir açıklama yaz: "Oturumun anonim kaydedilir: ad, e-posta veya cihaz kimliği toplanmaz.
   Katılım isteğe bağlıdır." Kutu işaretli değilse uygulama bugünkü gibi çalışsın.

2. **Her karar için bir satır kaydet.** Satır, kararın kesinleştiği anda yazılır. Bu an, seçimden
   sonra 3 saniyelik "Geri al" bandının bittiği ya da "Geri al" düğmesine basıldığı andır.
   Satır sütunları tam olarak şu sırada olsun:
   `oturum,sahne_no,seviye,karar_suresi_sn,onceki_yanlis_sayisi,ipucu_sayisi,ilk_tiklama_sn,onceki_ipucu_gerekti,ipucu_gerekti,kaynak`

   - `oturum`: oyun başında bir kez, 6 haneli rastgele hex üret (örnek: `a7f3c1`). Ad, e-posta
     veya cihaz bilgisi kullanma.
   - `sahne_no`: karar sırası, 1, 2 veya 3.
   - `seviye`: "Yeni başladım" için 0, "Deneyimliyim" için 1.
   - `karar_suresi_sn`: karar ekranı açıldıktan sonra seçime kadar geçen süre (saniye, 1 ondalık).
   - `onceki_yanlis_sayisi`: bu karardan önce seçilen **B seçeneği** sayısı. Karar 1, 2 ve 3'te
     B seçeneği kötü seçenektir ("Canlıda yama yap", "Hemen yayına al", "Logu ekibe olduğu gibi at").
   - `ipucu_sayisi`: bu karardan önce "Emin değil misin?" düğmesinin açılış sayısı.
   - `ilk_tiklama_sn`: karar ekranı açıldıktan sonra ilk seçime kadar geçen süre (saniye, 1 ondalık).
   - `onceki_ipucu_gerekti`: bir önceki satırın `ipucu_gerekti` değeri. İlk karar için 0.
   - `ipucu_gerekti`: bu kararda "Geri al" kullanıldıysa **veya** tutora soru yazıldıysa 1, aksi halde 0.
   - `kaynak`: her zaman `gercek`.

   Her oturum üç satır üretir. Sayılar nokta ondalık ayraçlı yazılsın.

3. **Sonuç ekranına "Veri dosyasını indir (CSV)" düğmesi ekle.** Düğme yalnızca veri toplama
   kutusu işaretliyse görünsün. Dosya adı `oturumlar_<oturum>.csv` olsun. İçerik: başlık satırı ve
   o oturumun üç satırı. Tarayıcıda dosya olarak indir.

4. Kişisel veri (ad, e-posta, cihaz kimliği, konum) hiçbir yerde toplanmasın ya da yazılmasın.

Değişiklikten sonra uygulamayı baştan sona bir kez oyna (Yeni başladım, A-A-A yolu), CSV'de üç
satır olduğunu ve sütun sırasının yukarıdaki gibi olduğunu doğrula. Sonra bana kısa bir özet ver.
