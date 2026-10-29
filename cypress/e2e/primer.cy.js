// SE Primer: uçtan uca testler (yayınlanan Build uygulaması)
// Çalıştırma: npx cypress run  (BASE_URL ortam değişkeniyle değiştirilebilir)
// Kapsam: Yeni başladım seviyesinde 3 kararın 8 kombinasyonunun tamamı (4 farklı son) + Deneyimliyim süre yolu

const GIRIS = () => {
  cy.visit('/');
  cy.contains('Mühendislik Deneyimin').should('be.visible');
};

const KRIZE_GEC = () => {
  // Giriş: seviye (varsayılan), rol (varsayılan), hedef (varsayılan) → Devam
  cy.contains('button', 'Devam Et').click();
  cy.contains('button', 'Devam Et').click();
  cy.contains('button', 'Kriz Masasına Geç').click();
  cy.contains('button', 'Müdahaleyi Başlat').click();
};

const SECIM_YAP = (metin, sonrakiButon = 'Sonraki Karara Geç') => {
  cy.contains(metin).click();
  // 3 saniyelik "Geri Al" bandı dolana kadar bekle (son karardan sonra buton farklı)
  cy.contains(sonrakiButon, { timeout: 10000 }).should('be.visible');
};

// Karar metinleri (A ve B seçenekleri)
const KARAR = {
  1: { A: 'Eski sürüme geri dön', B: 'Canlıda yama yap' },
  2: { A: 'Önce kısa test koş', B: 'Hemen yayına al' },
  3: { A: 'Hasta adlarını maskele', B: 'Logu ekibe olduğu gibi at' },
};

// Son ekran başlıkları (uygulamadaki tam metin)
const SON = {
  iyi: 'Kusursuz Müdahale: Sistem Ayakta, Veri Güvende!',
  kvkk: 'Sistem Ayakta Ama KVKK İhlali!',
  coktu: 'Sistem Çöktü!',
  cifte: 'Sistem Çöktü ve KVKK İhlali!',
};

// Oyun kuralı: sistem ayakta = (K1 = A) veya (K1 = B ve K2 = A); KVKK ihlali = K3 = B
const beklenenSon = (k1, k2, k3) => {
  const sistemAyakta = k1 === 'A' || (k1 === 'B' && k2 === 'A');
  const kvkkIhlali = k3 === 'B';
  if (sistemAyakta && !kvkkIhlali) return SON.iyi;
  if (sistemAyakta && kvkkIhlali) return SON.kvkk;
  if (!sistemAyakta && !kvkkIhlali) return SON.coktu;
  return SON.cifte;
};

describe('SE Primer: tüm yollar (K1, K2, K3)', () => {
  ['A', 'B'].forEach((k1) =>
    ['A', 'B'].forEach((k2) =>
      ['A', 'B'].forEach((k3) => {
        it(`K1=${k1}, K2=${k2}, K3=${k3} → ${beklenenSon(k1, k2, k3)}`, () => {
          GIRIS();
          cy.contains('Yeni başladım').click();
          KRIZE_GEC();

          cy.contains(KARAR[1][k1]).should('be.visible'); // Karar 1
          SECIM_YAP(KARAR[1][k1]);
          cy.contains('button', 'Sonraki Karara Geç').click();

          cy.contains(KARAR[2][k2]).should('be.visible'); // Karar 2
          SECIM_YAP(KARAR[2][k2]);
          cy.contains('button', 'Sonraki Karara Geç').click();

          cy.contains(KARAR[3][k3]).should('be.visible'); // Karar 3
          SECIM_YAP(KARAR[3][k3], 'Kriz Sonuç Raporunu Gör');
          cy.contains('button', 'Kriz Sonuç Raporunu Gör').click();

          cy.contains(beklenenSon(k1, k2, k3)).should('be.visible');
          cy.contains('Yeniden Oyna').should('be.visible');
        });
      })
    )
  );
});

describe('SE Primer: Deneyimliyim (süre yolu)', () => {
  it('60 saniye dolunca B otomatik uygulanır ve "Süre doldu" mesajı gösterilir', () => {
    cy.visit('/');
    cy.contains('Deneyimliyim').click();
    KRIZE_GEC();

    cy.contains('Karar Sayacı').should('be.visible');
    cy.contains('Nöbetçi İpucu').should('not.exist');

    // Cevap vermeden süre dolmasını bekle; süre dolunca B otomatik uygulanır
    cy.contains('Sonraki Karara Geç', { timeout: 75000 }).should('be.visible');
    cy.contains('Canlıda yama yap').should('be.visible');
    cy.contains('Sistem Askıda').should('be.visible');

    // AK-2: süre dolduğunda sonuç kartında uyarı görünür
    cy.contains('Süre doldu. Ekip B seçeneğini uyguladı.').should('be.visible');
  });
});
