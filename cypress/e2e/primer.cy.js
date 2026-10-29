// SE Primer: uçtan uca testler (yayınlanan Build uygulaması)
// Çalıştırma: npx cypress run  (BASE_URL ortam değişkeniyle değiştirilebilir)

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

describe('SE Primer: iyi son (A, A, A)', () => {
  it('Yeni başladım seviyesinde üç kararla iyi sona ulaşır', () => {
    GIRIS();
    cy.contains('Yeni başladım').click();
    KRIZE_GEC();

    cy.contains('Eski sürüme geri dön').should('be.visible'); // Karar 1
    SECIM_YAP('Eski sürüme geri dön');
    cy.contains('button', 'Sonraki Karara Geç').click();

    cy.contains('Önce kısa test koş').should('be.visible'); // Karar 2
    SECIM_YAP('Önce kısa test koş');
    cy.contains('button', 'Sonraki Karara Geç').click();

    cy.contains('Hasta adlarını maskele').should('be.visible'); // Karar 3
    SECIM_YAP('Hasta adlarını maskele', 'Kriz Sonuç Raporunu Gör');
    cy.contains('button', 'Kriz Sonuç Raporunu Gör').click();

    cy.contains('Kusursuz Müdahale: Sistem Ayakta').should('be.visible');
    cy.contains('Yeniden Oyna').should('be.visible');
  });
});

describe('SE Primer: kötü son (A, A, B)', () => {
  it('KVKK ihlali ile kötü sona ulaşır', () => {
    GIRIS();
    cy.contains('Yeni başladım').click();
    KRIZE_GEC();

    SECIM_YAP('Eski sürüme geri dön');
    cy.contains('button', 'Sonraki Karara Geç').click();

    SECIM_YAP('Önce kısa test koş');
    cy.contains('button', 'Sonraki Karara Geç').click();

    SECIM_YAP('Logu ekibe olduğu gibi at', 'Kriz Sonuç Raporunu Gör');
    cy.contains('button', 'Kriz Sonuç Raporunu Gör').click();

    cy.contains('Sistem Ayakta Ama KVKK İhlali').should('be.visible');
  });
});

describe('SE Primer: Deneyimliyim (süre yolu)', () => {
  it('60 saniye dolunca B otomatik uygulanır', () => {
    cy.visit('/');
    cy.contains('Deneyimliyim').click();
    KRIZE_GEC();

    cy.contains('Karar Sayacı').should('be.visible');
    cy.contains('Nöbetçi İpucu').should('not.exist');

    // Cevap vermeden süre dolmasını bekle; süre dolunca B otomatik uygulanır
    cy.contains('Sonraki Karara Geç', { timeout: 75000 }).should('be.visible');
    cy.contains('Canlıda yama yap').should('be.visible');
    cy.contains('Sistem Askıda').should('be.visible');

    // AK-2: "Süre doldu" mesajı Build'de eklendi ama canlıya henüz yansımadı (Republish gerekli)
    cy.contains('Süre doldu').should('be.visible');
  });
});
