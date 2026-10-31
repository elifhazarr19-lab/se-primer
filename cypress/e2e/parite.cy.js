// SE Primer v2: model paritesi (tarayıcı ↔ Python).
// Kaynak: tests/parite.json (tests/parite.py üretir). Uygulama ?parite= parametresiyle verilen
// tek bir karar girdisi için olasılığı data-cy="p" alanında gösterir (6 ondalık, nokta ayraçlı).
// Kabul: her girdi için |tarayıcı − Python| < tolerans (1e-4). Spec §8.5 ve AK-8.

describe('Model paritesi: tarayıcı (onnxruntime-web) ↔ Python referansı', () => {
  it('5 referans girdinin hepsinde olasılık farkı tolerans içinde', () => {
    cy.readFile('tests/parite.json').then((referans) => {
      referans.girdiler.forEach(({ id, girdi, p }) => {
        cy.visit(`/?parite=${encodeURIComponent(JSON.stringify(girdi))}`);
        cy.get('[data-cy="p"]', { timeout: 20000 })
          .should('be.visible')
          .invoke('text')
          .then((metin) => {
            const tarayici = parseFloat(metin.trim());
            expect(Number.isNaN(tarayici), `girdi ${id}: p okunamadı ("${metin}")`).to.equal(false);
            expect(
              Math.abs(tarayici - p),
              `girdi ${id}: tarayıcı ${tarayici}, Python ${p}`
            ).to.be.lessThan(referans.tolerans);
          });
      });
    });
  });
});
