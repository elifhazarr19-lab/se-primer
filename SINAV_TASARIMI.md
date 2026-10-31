# Vize sınav tasarımı

## Bu sınavı ben olsam nasıl tasarlardım

The Primer'daki oyuncu, anlatının kurallarıyla değil yaptığı seçimlerin sonucuyla öğrenir. Ben de
sınavda ezber yerine bu tür bir düşünmeyi ölçerdim. Öğrenci bir sistemin neden öyle davrandığını
açıklayabilmeli ve yeni bir durumda tahmin yürütebilmeli. Üç ilke yönetirdi:

1. **Gerekçe, cevaptan önce gelir.** Her soru "ne" yerine "neden" ve "ne olmazdı" diye sorar.
   Doğru cevap bir kelime değil, bir karşılaştırmadır.
2. **Çeldiriciler yanlış değil, eksiktir.** Yanlış seçenek ya da yarım bilgi, öğrencinin
   sık yaptığı hatayı temsil eder: "yüksek doğruluk her zaman yeterlidir" gibi.
3. **Uygulama, tanımın yerini tutar.** Kavram bir senaryoda kullanılmadan ölçülmüş sayılmaz.

## Özgün sınav sorusu (1 sayfa, 40 dk)

**Senaryo.** Bir ekip, oyuncunun karar süresi ve seçim geçmişinden "bu oyuncuya ipucu gerekir mi"
sorusunu yanıtlayan bir sınıflandırıcı eğitti. Test sonucu: ROC-AUC = 0,91. Ekip modeli hemen
yayınlamak istiyor. Ama test verisi, eğitim verisiyle aynı oyuncu oturumlarından alınmış.
Eşik (0,70) ise sonuç açıklandıktan sonra belirlendi.

**(a) [25 puan]** Test verisinin neden ayrı oturumlardan alınması gerektiğini açıklayın.
Hangi sızıntı türü bu durumda ortaya çıkar? Sonucu güvenilir kılmak için hangi değişiklik gerekir?

**(b) [25 puan]** Eşiğin sonuç açıklandıktan sonra seçilmesi neden bir sorundur? Bu sorunu önlemek
için eğitimden önce hangi üç değer sabitlenmelidir? Her biri için kısa bir gerekçe yazın.

**(c) [25 puan]** Aynı model iki ortamda çalışıyor: Python sunucusu ve tarayıcıdaki JavaScript.
Olasılıklar 0,4512 ve 0,4519 çıkıyor. Bu fark kabul edilebilir mi? Hangi test bu durumu yakalar,
tolerans neye göre seçilir ve neden sıfır değil?

**(d) [25 puan]** Ekip, modeli bir commit hash'i yerine `main` dalı üzerinden yayınlamayı
planlıyor. Bu planın iki sakıncasını yazın. Yayın sonrası bir hata bulunursa geri alma adımlarını
sırasıyla sıralayın.

## Beklenen kavramlar ve çeldiriciler

| Kavram | Doğru cevapta olması gereken | Sık yapılan hata (çeldirici) |
|---|---|---|
| Sızıntı | Test ve eğitim aynı oturumdan, bilgi iki tarafa sızar | "Veri çok olduğu için sorun olmaz" |
| Eşik sabitleme | Eşik, sonuçtan önce tanımlanır; aksi halde seçim veriye uydurulur | "Eşiği en iyi sonuç veren değere çekmek doğaldır" |
| Parite toleransı | Float32 yuvarlaması için küçük bir tolerans; eşik, ölçülen hataya ve karar sınırına göre seçilir | "Olasılık tam eşitse yayınlanabilir" |
| Yayın sürümü | Commit hash'i değişmez; `main` değişebilir | "Dosya adı aynıysa sürüm aynıdır" |

## Puanlama notu

Tam puan için (a) ve (b) "neden" sorusuna yanıt vermeli. (c) için tolerans sayısı tek başına
yeterli değil, toleransın nereden geldiği yazılmalı. (d) için en az iki sakınca ve sırayla geri
alma adımı beklenir.
