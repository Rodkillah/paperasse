# PEA et Assurance-Vie (fiscalité des rachats)

Voir `data/pea-assurance-vie.json` pour les taux et seuils.

> **Note** : la fiscalité de la transmission de l'assurance-vie (au décès) est couverte par le skill `notaire`. Ce document ne couvre que la fiscalité des rachats de vivant.

## PEA (Plan d'Épargne en Actions)

### Plafonds de versement

| Plan | Plafond |
|------|---------|
| PEA classique | 150 000 € |
| PEA-PME | Variable (à vérifier), plafond combiné avec PEA ≤ 225 000 € |
| PEA jeune (enfant majeur rattaché) | 20 000 € |

Les plafonds concernent les **versements**, pas la valeur du plan. Un plan peut dépasser 150 000 € de valorisation grâce aux gains.

### Fiscalité selon ancienneté du plan

#### Avant 5 ans

- **Tout retrait entraîne la clôture** du plan
- Imposition des gains : 12,8 % IR (ou barème sur option globale) + PS produits de placement, 17,2 % pour un retrait en 2025 puis **18,6 % à compter du 01/01/2026** (LFSS 2026), soit PFU 31,4 %

**Exceptions** (retrait partiel avant 5 ans **sans clôture** du plan ; les PS restent dus) :
- Licenciement, invalidité ou mise à la retraite anticipée du titulaire ou de son époux ou partenaire de Pacs
- Retrait de titres d'une société en liquidation judiciaire
- Création ou reprise d'entreprise (réinvestissement dans les 3 mois) : gain exonéré d'IR, mais plus aucun versement possible ensuite

#### Après 5 ans

- **Retraits libres** sans clôture du plan
- **EXONÉRATION TOTALE d'IR** sur les gains
- **Prélèvements sociaux** dus sur les gains à chaque retrait, au taux applicable à la date du retrait :
  - **Retraits avant le 01/01/2026** : 17,2 %
  - **Retraits à partir du 01/01/2026** : **18,6 %** (LFSS 2026, art. 12, qui modifie l'art. L. 136-8 CSS). Pour la DGFiP, ce taux s'applique à tout le gain acquis depuis le 01/01/2018, y compris la part acquise avant 2026 ; seules les fractions historiques des PEA ouverts avant 2018 gardent leurs anciens taux (voir « Taux historiques PS »). L'art. 12, II, 2° de la LFSS 2026 exclut de la hausse les produits mentionnés aux C et D du V de l'art. 8 de la LFSS 2018 « acquis ou constatés avant le 1er janvier 2026 » : sur un retrait important, contrôler le taux appliqué sur le relevé de l'établissement.
- Référence : les gains PEA sont qualifiés de "produits de placement" (PS prélevés à la source au moment du retrait), pas de "revenus du patrimoine"

### Taux historiques PS

Seuls les PEA ouverts avant le 01/01/2018 gardent des taux historiques : la fraction des gains acquise ou constatée avant le 01/01/2018 (et, pour un plan détenu depuis moins de 5 ans à cette date, pendant ses 5 premières années) reste taxée aux taux en vigueur lors de son acquisition (LFSS 2018, art. 8, V, C, 3°). Tous les autres gains supportent le taux en vigueur au jour du retrait : 17,2 % en 2025, 18,6 % à compter du 01/01/2026. L'établissement applique ce calcul et le fait figurer sur le relevé de retrait ou de clôture.

### Composition éligible

- Actions européennes (UE + EEE)
- OPCVM investis à 75% minimum en actions européennes
- Certaines ETF européens (vérifier l'éligibilité)

**Non éligibles** : actions américaines, asiatiques, obligations, or, crypto.

### Arbitrage PEA vs assurance-vie

| Critère | PEA | AV |
|---------|-----|-----|
| Exonération IR | **Oui** après 5 ans | Non (abattement seulement) |
| PS sur gains | 17,2 % puis 18,6 % à partir du 01/01/2026, à chaque retrait | 17,2 % inchangé (cas exclu de la hausse LFSS 2026, sauf contrats rente-survie et épargne handicap : 18,6 % dès le 01/01/2026) |
| Composition | Actions EUR uniquement | Libre (actions, obligations, fonds €) |
| Retrait avant échéance | Clôture avant 5 ans | Libre à tout moment |
| Transmission | Dans succession classique | Régime spécifique (voir notaire) |
| Plafond | 150 000 € | Aucun |

**Stratégie de cumul** :
- PEA pour la performance actions européennes (fiscalité imbattable après 5 ans)
- AV pour la diversification (fonds €, UC mondiales) et la transmission

## Assurance-Vie : fiscalité des rachats

### Principe de proportionnalité

**Un rachat partiel NE retire PAS que du capital non imposable.** Il retire une fraction **proportionnelle** de gains et de capital.

**Formule** :
```
quote_part_gains_imposable = (gains_totaux / valeur_totale_contrat) × montant_racheté
```

**Exemple** :
- Contrat : versements 80 000 € + gains 20 000 € = valeur totale 100 000 €
- Rachat de 10 000 €
- Quote-part gains imposable = (20 000 / 100 000) × 10 000 = **2 000 €**
- 8 000 € sont du capital (non imposable), 2 000 € sont du gain (imposable)

**Piège classique** : croire qu'un rachat de 10 000 € sur un contrat avec 20 000 € de gains retire d'abord du capital (0 imposable). Non.

### Abattement annuel après 8 ans

Voir `data/pea-assurance-vie.json` → `assurance_vie_rachats.abattement_annuel_apres_8_ans`.

| Situation | Abattement annuel |
|-----------|-------------------|
| Célibataire, veuf, divorcé | 4 600 € |
| Couple (imposition commune) | 9 200 € |

**Condition** : 8 ans d'ancienneté du **contrat** (pas des versements).

**Mécanique** : l'abattement s'applique sur la quote-part de gains imposable, pas sur le montant racheté.

**Renouvelable** : chaque année civile (pas glissant sur 12 mois).

### Taux d'imposition selon date des versements

#### Versements avant le 27 septembre 2017

Taux dégressif selon ancienneté du contrat. Prélèvement libératoire (PFL) optionnel :

| Ancienneté du contrat | PFL | Barème (option) |
|-----------------------|-----|-----------------|
| < 4 ans | 35% | Barème |
| 4-8 ans | 15% | Barème |
| 8 ans et plus (6 ans pour un contrat souscrit avant le 01/01/1990) | 7,5 % prélevé sans abattement, l'abattement étant restitué par crédit d'impôt (ligne 2DH) | Barème après abattement (ligne 2CH) |

#### Versements après le 27 septembre 2017

**Règle** : PFU 30 % sur les gains, avec modulation selon les primes versées non remboursées et l'ancienneté du contrat.

| Situation | Taux |
|-----------|------|
| Contrat < 8 ans | PFU 30% (12,8% IR + 17,2% PS) |
| Contrat ≥ 8 ans, primes non remboursées ≤ 150 000 € (tous contrats du titulaire, au 31/12 N-1) | 24,7 % (7,5 % IR + 17,2 % PS), après abattement |
| Contrat ≥ 8 ans, primes non remboursées > 150 000 € | Produits proratisés : 7,5 % IR sur la part (150 000 € moins primes d'avant le 27/09/2017) / primes versées depuis le 27/09/2017, 12,8 % IR sur le reste, + PS 17,2 % (lignes 2VV et 2WW) |

**Seuil 150 000 €** : s'apprécie sur les primes versées et non remboursées au 31 décembre de l'année précédant le rachat, sur l'ensemble des contrats d'assurance-vie et de capitalisation dont est titulaire la personne bénéficiaire des produits (par personne, pas par foyer).

### Option barème

**Contrat de 8 ans et plus (taux de 7,5 %)** : au-delà de l'abattement, le barème perd dès la TMI de 11 % (environ 10,25 % après effet de la CSG déductible, contre 7,5 %) et ne gagne qu'à TMI 0 %. Dans la limite de l'abattement (4 600 / 9 200 €, appliqué quel que soit le mode d'imposition), l'IR est nul dans les deux cas, mais l'option barème ouvre droit à la CSG déductible (6,8 %) sur les produits déclarés ligne 2BH (pas sur les produits des fonds en euros des années antérieures, ligne 2CG). Produits taxés à 12,8 % (contrat de moins de 8 ans, primes au-delà de 150 000 €) : le barème gagne à TMI 0 % et 11 %. L'option étant globale, l'arbitrage se fait sur l'ensemble des revenus du capital.

Option **globale** (case 2OP), irrévocable pour les revenus 2025 une fois la date limite de déclaration passée (révocable à compter des revenus 2026, LFI 2026 art. 126).

### Contrats très anciens (avant 1983)

Régime de faveur pour les contrats souscrits **avant le 1er janvier 1983** : exonération d'IR sur les gains (les PS restent dus), sauf pour les produits perçus depuis le 01/01/2020 et attachés à des primes versées depuis le 10/10/2019, imposés comme ceux d'un contrat de plus de 8 ans à primes postérieures au 27/09/2017 (LF 2021, art. 9 ; CGI, art. 125-0 A, I quater A).

Extrêmement rare, à vérifier si le contrat est très ancien.

## Stratégies courantes

### 1. Rachats après 8 ans optimisés

Fractionner les rachats pour rester dans l'abattement annuel (9 200 € couple).

Exemple : besoin de 50 000 € sur 5 ans → 10 000 € par an optimise l'abattement (si gains ≤ abattement par rachat).

### 2. Arbitrage UC vs fonds €

- Fonds € : rendement faible mais sécurité + PS au fil de l'eau (CSG/CRDS en année N sur les intérêts crédités)
- UC : rendement potentiel + PS uniquement au rachat (pas au fil de l'eau)

### 3. Ouvrir un contrat tôt pour prendre date

L'ancienneté compte. Un contrat ouvert avec 100 € prend date → 8 ans plus tard, l'abattement est disponible.

## Déclaration

### Rachats PEA

- Pas de déclaration spécifique tant que le plan n'est pas clôturé
- À la clôture : 2042 case 3VT (gains PEA imposables)
- PS prélevés par l'établissement

### Rachats AV

- Contrat de 8 ans et plus : 2CH (primes du 26/09/1997 au 26/09/2017, barème), 2DH (prélèvement libératoire de 7,5 % déjà acquitté), 2UU réparti en 2VV (primes jusqu'à 150 000 €, 7,5 %) et 2WW (au-delà, 12,8 %)
- Contrat de moins de 8 ans : 2XX (prélèvement libératoire), 2YY (autres produits des primes d'avant le 27/09/2017), 2ZZ (primes depuis le 27/09/2017). Les lignes 2BH et 2CG servent seulement à exclure de la base des PS les produits qui les ont déjà supportés (2BH avec CSG déductible si option barème, 2CG sans)
- Attestation annuelle de l'assureur requise

## Pièges fréquents

1. **Oublier la proportionnalité** → surévaluer ce qu'on peut retirer "sans impôt"
2. **8 ans du versement** au lieu du contrat → mauvais calcul
3. **Seuil 150 000 €** apprécié par titulaire, tous contrats AV et capitalisation confondus (ni par contrat, ni par foyer), au 31/12 de l'année précédente
4. **Option barème irrévocable** pour les revenus 2025 (révocable à compter des revenus 2026, LFI 2026 art. 126)
5. **Retrait PEA avant 5 ans** pour un petit besoin → clôture automatique
6. **PEA composé d'actions non éligibles** → régularisation DGFIP possible

## Références CGI / BOFiP

- PEA : art. 163 quinquies D CGI, art. L. 221-30 Code monétaire et financier
- Assurance-vie fiscalité rachats : art. 125-0 A CGI
- Abattement annuel AV : art. 125-0 A-I-2° CGI
- Seuil 150 000 € : art. 125-0 A-I-2° bis CGI
- BOFiP : BOI-RPPM-RCM-40-50 (PEA) et BOI-RPPM-RCM-20-10-20-50 (AV)
