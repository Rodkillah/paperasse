# Revenus du capital (RCM, dividendes, plus-values mobilières)

## PFU vs barème : l'arbitrage fondamental

Les revenus mobiliers (dividendes, intérêts, plus-values de titres) sont soumis au choix :

| Régime | Taux 2025 | Caractéristiques |
|--------|-----------|------------------|
| **PFU (flat tax)** | **30 % pour dividendes / intérêts ; 31,4 % pour PV mobilières et crypto** (voir tableau ci-dessous) | Par défaut. Pas d'abattement. Pas de CSG déductible. |
| **Barème progressif** | Selon TMI | Sur option **globale** (case 2OP : tous les RCM et PV mobilières de l'année ; les PV crypto relèvent d'une option distincte, case 3CN). Abattement 40% sur dividendes. CSG déductible 6,8 % l'année du paiement des PS (même année pour les RCM prélevés à la source, ligne 2BH ; N+1 pour les PV et les RCM taxés par voie de rôle). |

### Taux PS différenciés (LFSS 2026)

La LFSS 2026 (loi n° 2025-1403 du 30/12/2025, art. 12) modifie le taux de CSG (9,2 % → 10,6 %, soit total PS 17,2 % → 18,6 %) avec **deux dates d'entrée en vigueur distinctes** :

| Catégorie | PS revenus 2025 | PS revenus 2026+ | Base CSS |
|---|---|---|---|
| Revenus du patrimoine (PV mobilières, crypto, LMNP) | **18,6 %** | 18,6 % | L. 136-6 |
| Produits de placement ayant supporté les PS lors du versement (dividendes, intérêts, PEA à la sortie, PER) | 17,2 % | **18,6 % à partir du 01/01/2026** | L. 136-7 |
| RCM 2025 n'ayant pas supporté les PS lors du versement (payeur établi hors de France, sans formulaire 2778) | **18,6 %** (avis 2026) | 18,6 % | L. 136-6 |
| AV et capitalisation (sauf rente-survie et épargne handicap : 18,6 % dès le 01/01/2026), foncier nu, SCPI (revenus fonciers), plus-values immobilières, CEL ouverts jusqu'au 31/12/2017, PEL ouverts jusqu'au 31/12/2017 (12 premières années), PEP | 17,2 % | 17,2 % (inchangé) | L. 136-8, IV |
| Livrets réglementés (Livret A, LDDS, LEP) | exonérés | exonérés | n/a |

Voir `data/pfu-prelevements-sociaux.json` pour les taux exacts.

### Règles d'orientation rapide

| TMI | Recommandation | Raison |
|-----|---------------|--------|
| 0% ou 11% | Barème | Tranche basse + abattement 40% dividendes + CSG déductible |
| 30% | À chiffrer | Selon composition : dividendes (abattement 40%) vs intérêts/PV (pas d'abattement) |
| 41% ou 45% | PFU | Flat tax 12,8% < TMI 41%/45% |

**Règle absolue** : l'option barème (case 2OP) est **globale** : elle engage tous les RCM et PV de cession de valeurs mobilières du foyer de l'année (les PV crypto ont leur propre option, case 3CN). Pour les revenus 2025, elle est **irrévocable** une fois la date limite de déclaration passée ; la LFI 2026 (art. 126) supprime ce caractère irrévocable pour l'impôt dû au titre de 2026 et des années suivantes. Ne jamais recommander sans avoir vérifié la composition complète.

### Exemple de calcul comparatif

Foyer célibataire, TMI 30%, **dividendes 10 000 € encaissés en 2025** :

**Sous PFU** (dividende = produit de placement, PS 17,2 % en 2025) :
- IR : 10 000 × 12,8% = 1 280 €
- PS : 10 000 × 17,2% = 1 720 €
- Total : 3 000 €

**Sous barème** :
- Assiette IR : 10 000 × (1 − 0,40) = 6 000 €
- IR : 6 000 × 30% = 1 800 €
- PS : 10 000 × 17,2% = 1 720 €
- CSG déductible : 10 000 × 6,8 % = 680 €, déduite du revenu global 2025 (PS prélevés à la source en 2025, ligne 2BH), économie 680 × 30 % = 204 €
- Total net : 3 520 − 204 = **3 316 €**

→ Ici, PFU avantageux (3 000 € < 3 316 €) malgré l'abattement 40%.

Mais si le même foyer a aussi **5 000 € de PV mobilière réalisée en 2025** (revenu du patrimoine, PS 18,6 %) :
- PFU : 5 000 × 31,4 % = 1 570 €
- Barème : 5 000 × 30 % IR + 5 000 × 18,6 % PS = 2 430 €, moins la CSG déductible en 2026 (5 000 × 6,8 % × 30 % = 102 €), soit 2 328 €
- PFU plus favorable et l'écart s'élargit (758 € contre 316 € sur les dividendes) : sans abattement de 40 %, le barème à TMI 30 % coûte 17,2 points d'IR de plus que le PFU. L'option étant globale, comparer les totaux : PFU 4 570 € contre barème 5 644 €.

**Attention** : à partir des revenus 2026, le dividende passera aussi à 18,6 % PS (PFU effectif 31,4 %).

## Types de revenus du capital

### Dividendes (case 2DC)

- Par défaut : PFU 30 % pour les dividendes 2025 dont les PS ont été acquittés lors du versement (12,8 % IR + 17,2 % PS) ; 31,4 % pour les dividendes 2025 qui n'ont pas supporté les PS lors du versement (PS 18,6 % sur l'avis 2026) et pour tous les dividendes encaissés à compter du 01/01/2026
- Option barème : abattement 40 % puis IR barème + PS (17,2 % en 2025, 18,6 % à partir de 2026)
- **Dividendes étrangers** : peuvent avoir été soumis à une retenue à la source dans le pays d'origine, crédit d'impôt possible sous convention fiscale

### Intérêts, RCM (case 2TR)

- Obligations, crowdfunding immobilier (intérêts), livrets fiscalisés, comptes à terme
- Soumis au PFU par défaut ou barème sur option
- **Pas d'abattement** : contrairement aux dividendes
- **Crowdfunding immobilier** : imposé comme RCM, pas comme revenus fonciers, même si sous-jacent immobilier
- **Livrets réglementés** (Livret A, LDDS, LEP) : exonérés d'IR et de PS → à ne pas confondre

### Plus-values mobilières (case 3VG)

- Gain net de cession de titres (actions, parts sociales, OPC)
- PFU par défaut ou barème sur option
- Voir `data/plus-values-mobilieres-crypto.json` pour détails
- **Abattements durée de détention** : uniquement pour titres acquis **avant 2018** ET option barème
- **Abattement dirigeant retraite** : 500 000 € (600 000 € pour une cession à de jeunes agriculteurs) sous conditions strictes (cession de titres de PME, départ en retraite), pour les cessions jusqu'au 31/12/2031 (art. 150-0 D ter CGI ; LF 2025, art. 70), au PFU comme au barème, sans effet sur les prélèvements sociaux

### Crypto-actifs

Régime distinct : méthode PAMC (prix acquisition moyen pondéré) sur l'ensemble du portefeuille, formulaire 2086 (à joindre même en cas d'exonération), exonération si le total des prix de cession du foyer n'excède pas 305 €/an. Détail dans la section crypto listée depuis SKILL.md.

## Prélèvements sociaux : couche distincte de l'IR

**À ne jamais confondre avec l'IR.** Les PS sont prélevés en plus sur la quasi-totalité des revenus du capital.

- Composition : CSG + CRDS + prélèvement de solidarité
- Taux différencié depuis la LFSS 2026 (voir table en haut du document) : 18,6 % pour les revenus du patrimoine dès 2025, 17,2 % puis 18,6 % au 01/01/2026 pour les produits de placement, 17,2 % inchangé pour l'AV (hors rente-survie et épargne handicap), le foncier nu, les SCPI, les plus-values immobilières, les CEL et PEL ouverts jusqu'au 31/12/2017 (PEL : 12 premières années) et les PEP
- **Sous PFU** : PS inclus dans le taux global (30 % ou 31,4 % selon la nature du revenu)
- **Sous barème** : PS séparés de l'IR (mais CSG 6,8 % déductible l'année du paiement des PS : même année pour les RCM prélevés à la source, N+1 pour les PV et les RCM taxés par voie de rôle)

**Cas restant à 17,2 %** (CSG maintenue à 9,2 % par l'art. L. 136-8, IV CSS, rétabli par la LFSS 2026) :
- Assurance-vie et contrats de capitalisation (sauf contrats rente-survie et épargne handicap : 18,6 % dès le 01/01/2026)
- Revenus fonciers (foncier nu, SCPI)
- CEL ouverts jusqu'au 31/12/2017 ; PEL ouverts jusqu'au 31/12/2017, pour les intérêts des 12 premières années (PEL et CEL ouverts depuis le 01/01/2018 : 18,6 % au 01/01/2026)
- PEP
- Plus-values immobilières

Les livrets réglementés (Livret A, LDDS, LEP) ne figurent pas dans cette liste : ils sont exonérés d'IR et de PS.

### CSG déductible

- Montant : 6,8% de la base
- **Condition** : uniquement sous option barème progressif
- **Zéro déductible sous PFU**
- Déduite du revenu global de l'année de paiement des PS : même année pour les dividendes et intérêts prélevés à la source (ligne 2BH, déduction automatique), N+1 pour les PV mobilières et les RCM taxés par voie de rôle (case 6DE préremplie) ; économie = CSG déductible × TMI de cette année-là

## Enveloppes fiscales spécifiques

**PEA** : exonération IR après 5 ans. PS dus à chaque retrait : **17,2 % pour les retraits effectués avant le 01/01/2026**, **18,6 % à partir du 01/01/2026** (sur tout le gain acquis depuis le 01/01/2018, y compris la part acquise avant le 01/01/2026, selon la DGFiP ; les fractions historiques des PEA ouverts avant 2018 gardent leurs anciens taux). Cf. art. L. 136-7 CSS (assiette) et L. 136-8 CSS (taux).

**AV** : abattement annuel après 8 ans, fiscalité selon date des versements. PS **17,2 % inchangés** (cas exclu de la hausse LFSS 2026), sauf contrats rente-survie et épargne handicap, passés à 18,6 % au 01/01/2026.

Règles complètes (retrait avant/après 5 ans PEA, abattements AV par tranche de versement, 152 500 € succession AV) dans la section PEA/AV listée depuis SKILL.md.

## Pièges fréquents

1. **Confondre IR et PS** dans une simulation : conduit à sous-estimer la charge de 17,2 à 18,6 points selon la nature du revenu.
2. **Oublier l'option barème globale** : choisir le barème pour les dividendes implique le barème aussi pour les intérêts et PV mobilières.
3. **CSG déductible sous PFU** : elle n'existe pas.
4. **Abattement 40% sous PFU** : n'existe que sous barème.
5. **Retenue à la source étrangère** : créditer contre l'IR français (conventions fiscales), à ne pas oublier.

## Références CGI / BOFiP / CSS

- PFU : art. 200 A CGI
- Option barème : art. 200 A-2 CGI
- Abattement dividendes 40% : art. 158-3° CGI
- Plus-values mobilières : art. 150-0 A à 150-0 D CGI
- Prélèvements sociaux : art. L. 136-1 et s. CSS
- Différenciation revenus du patrimoine vs produits de placement : art. L. 136-6 et L. 136-7 CSS
- LFSS 2026 (hausse CSG) : loi n° 2025-1403 du 30/12/2025, art. 12 (modifie L. 136-8 CSS)
- BOFiP : BOI-RPPM-RCM (dividendes/RCM) et BOI-RPPM-PVBMI (PV mobilières)
