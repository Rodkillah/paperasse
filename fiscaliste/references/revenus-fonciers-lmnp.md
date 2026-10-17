# Revenus fonciers, LMNP et SCI à l'IR

## Distinction fondamentale

| Type de location | Régime fiscal | Catégorie |
|------------------|---------------|-----------|
| Non meublée (location nue) | Revenus fonciers | Revenus fonciers (micro ou réel) |
| Meublée non professionnelle | **BIC** | LMNP (micro-BIC ou réel) |
| Meublée professionnelle | **BIC** | LMP (réel obligatoire) |
| SCI à l'IR | Revenus fonciers | Transparence fiscale |
| SCI à l'IS | IS | **Hors scope fiscaliste** : voir skill `comptable` |

**Erreur classique** : déclarer une location meublée en revenus fonciers. Non : le meublé relève des BIC. Conséquences fiscales très différentes (amortissements possibles en réel).

## Revenus fonciers (location nue)

### Micro-foncier (régime simplifié)

Voir `data/regimes-fonciers-lmnp.json` → `micro_foncier`.

- **Condition** : revenus fonciers bruts ≤ 15 000 €
- **Abattement** : 30% automatique
- **Exclusions** (le foyer loue, en direct ou via des parts de SCI, un bien relevant d'un régime particulier) : monument historique ou immeuble détenu en nue-propriété ; logement Loc'Avantages (art. 199 tricies) ; logement à amortissement (Périssol, Besson neuf, Robien, Borloo neuf) ; logement à déduction spécifique (conventionnement Anah, Borloo ancien, Cosse, Scellier intermédiaire, Scellier ZRR, Robien ZRR) ; logement ayant ouvert droit à la réduction pour travaux dans les logements touristiques (art. 199 decies EA et 199 decies F). Exclus aussi : les parts de SCPI détenant de tels biens ou à amortissement (Robien SCPI, Borloo SCPI), et le foyer qui ne perçoit que des revenus de parts de sociétés immobilières non soumises à l'IS (SCI à l'IR) ou de FPI, sans aucun bien loué nu en direct. Les réductions Pinel, Duflot, Scellier, Denormandie et Malraux ne font pas obstacle au micro-foncier (brochure pratique IR 2026, p. 157 et 158 ; BOI-RFPI-DECLA-10 § 50 à 70).
- **Avantage** : simplicité. Pas de comptabilité.
- **Inconvénient** : aucun déficit possible. Si vos charges réelles > 30%, vous payez trop d'impôt.

### Régime réel

Obligatoire au-delà de 15 000 € bruts ou sur option irrévocable pour 3 ans.

**Charges déductibles** :
- Intérêts d'emprunt (imputables uniquement sur les revenus fonciers)
- Travaux d'entretien, réparation, amélioration (pas construction, pas agrandissement)
- Taxe foncière (hors TEOM récupérable)
- Primes d'assurance (PNO, GLI)
- Frais de gestion (agence, syndic fraction non récupérable)
- Provisions pour charges de copropriété

**Piège travaux** : les travaux de construction, reconstruction, agrandissement **NE SONT PAS** déductibles des revenus fonciers : ils majorent seulement le prix d'acquisition pour la future plus-value.

### Déficit foncier

Voir `data/regimes-fonciers-lmnp.json` → `regime_reel_foncier.deficit_foncier`.

**Mécanisme** :
- Charges > recettes → déficit
- **Imputable sur le revenu global dans la limite de 10 700 €** par an (limite rehaussée, sans dépasser 21 400 €, du montant des travaux de rénovation énergétique faisant passer le logement d'une classe E, F ou G à A, B, C ou D : devis accepté depuis le 5/11/2022, dépenses payées du 1/01/2023 au 31/12/2025 pour les revenus 2025, dispositif prorogé jusqu'au 31/12/2027 par la LF 2026, art. 47)
- Au-delà : reportable sur les revenus fonciers des **10 années suivantes**
- **Exception critique** : les intérêts d'emprunt **ne sont JAMAIS imputables sur le revenu global**, uniquement sur les revenus fonciers. Mais le revenu brut foncier est réputé compenser **en priorité** les intérêts d'emprunt (BOI-RFPI-BASE-30-20 § 110) : seule la fraction du déficit qui excède le revenu brut diminué des intérêts provient des intérêts. Exemple : loyers 15 000 €, intérêts 6 000 €, autres charges 22 000 € : déficit 13 000 € entièrement issu des autres charges, 10 700 € imputables sur le revenu global, 2 300 € reportables

**Stratégie d'optimisation** :
- Concentrer les travaux importants sur une année → déficit imputable sur revenu global
- Attention à ne pas vendre le bien avant 3 ans après imputation (sinon reprise du déficit)

## LMNP (Location Meublée Non Professionnelle)

### Régime micro-BIC

Voir `data/regimes-fonciers-lmnp.json` → `micro_bic_lmnp`.

**Réforme loi Le Meur (nov. 2024), applicable revenus 2025** : la distinction clé est désormais **classé / non classé**, plus résidence principale.

| Type de location | Seuil | Abattement |
|------------------|-------|-----------|
| LMNP longue durée | 77 700 € | 50% |
| Meublé de tourisme classé | 77 700 € | 50% |
| **Meublé de tourisme non classé** | **15 000 €** | **30%** |

Le micro-BIC s'applique si les recettes de l'année précédente ou de l'avant-dernière année ne dépassent pas le seuil : le régime réel devient obligatoire après deux années consécutives de dépassement (N-2 et N-1). Abattement minimum : 305 €. Pour les revenus 2026, le seuil de 77 700 € passe à 83 600 € (BOFiP ACTU-2025-00127) ; le seuil de 15 000 € et le taux de 30 % des meublés de tourisme non classés sont maintenus.

### Régime réel LMNP

**Principe** : résultat BIC = recettes − charges − **amortissements**.

**Amortissements** :
- Bien immobilier : 2-3%/an sur 25-40 ans (hors terrain, terrain non amortissable)
- Mobilier : 10-20%/an sur 5-10 ans
- Gros travaux : amortissables sur leur durée d'usage

**Résultat fiscal** : souvent nul ou déficitaire grâce aux amortissements → pas d'IR sur les loyers pendant des années.

**Déficit LMNP** : NON imputable sur le revenu global (contrairement au LMP), ni sur les autres BIC non professionnels. Imputable uniquement sur les revenus de location meublée non professionnelle des **10 années suivantes** (cases 5GA à 5GJ).

**Revente : réintégration des amortissements** (LFI 2025, art. 84 ; CGI, art. 150 VB, III) : pour les cessions réalisées depuis le 15/02/2025, le prix d'acquisition retenu pour la plus-value immobilière des particuliers est minoré des amortissements déduits en application de l'article 39 C, y compris ceux déduits avant 2025, quelle que soit la date de mise en location (réponse ministérielle n° 10097, JO AN du 24/03/2026). Exceptions : résidences pour étudiants ou jeunes de moins de 30 ans en formation, établissements et résidences services pour personnes âgées ou handicapées, établissements de soins de longue durée. Les abattements pour durée de détention s'appliquent ensuite.

### Bascule LMP vs LMNP

Voir `data/regimes-fonciers-lmnp.json` → `lmp_vs_lmnp`.

**Conditions LMP (cumulatives)** :
1. Recettes meublées > 23 000 €
2. ET recettes meublées > revenus du foyer soumis à l'IR en traitements et salaires (y compris pensions et rentes viagères, rémunérations de l'art. 62), BIC hors location meublée, BA et BNC (art. 155, IV CGI)

**Conséquences LMP** :
- Déficits imputables sur le revenu global
- Plus-values professionnelles (exonération possible après 5 ans sous conditions de recettes)
- Cotisations sociales TNS sur le bénéfice (SSI), charge significative
- Biens exonérés d'IFI comme biens professionnels (sous conditions)

**Attention bascule involontaire** : une baisse des autres revenus du foyer pris en compte (traitements et salaires, pensions comprises, BIC, BA, BNC), par exemple une pension inférieure à l'ancien salaire, peut faire basculer en LMP malgré des loyers inchangés. À surveiller.

## SCI à l'IR

Voir `data/regimes-fonciers-lmnp.json` → `sci_ir`.

**Régime par défaut** : transparence fiscale.

- Les revenus et charges remontent directement dans la déclaration de chaque associé au prorata des parts
- Nature fiscale : revenus fonciers classiques (micro ou réel selon le total fonciers du foyer)
- Cession des parts ou du bien : régime des plus-values immobilières des particuliers
- L'amortissement **n'est PAS possible** (contrairement à la SCI à l'IS)

**Quand choisir SCI IR** :
- Transmission patrimoniale (démembrement, donation de parts)
- Location nue (meublé en SCI = risque de requalification IS)
- Détention longue (exonération PV immo à 22 ans IR / 30 ans PS)

**Quand choisir SCI IS (hors scope)** :
- Fort rendement locatif et réinvestissement
- Possibilité d'amortir le bien
- Piège : à la cession, PV calculée sur valeur nette comptable (après amortissements) → imposition forte

→ Pour SCI à l'IS, voir skill `comptable`.

## Formulaires

| Régime | Formulaire |
|--------|-----------|
| Micro-foncier | 2042 case 4BE |
| Régime réel foncier | 2044 (ou 2044 spéciale) |
| Micro-BIC LMNP | 2042 C-PRO : 5NG (chambres d'hôtes et meublés de tourisme classés), 5NH (meublés de tourisme non classés), 5NI (autres locations meublées) ; 5NJ, 5NK, 5NL si les revenus sont soumis aux cotisations sociales |
| Réel LMNP / LMP | 2031 + 2033 (liasse BIC) + 2042 C-PRO |
| SCI IR | Déclaration 2072 (SCI) + report sur 2044 (associés) |

## Références CGI / BOFiP

- Revenus fonciers : art. 14 à 33 quater CGI
- Déficit foncier : art. 156-I-3° CGI
- LMNP : art. 35-I-5° bis CGI
- LMP : art. 155-IV CGI
- SCI : art. 8 CGI (transparence)
- BOFiP : BOI-RFPI (fonciers) et BOI-BIC-CHAMP-40 (meublés)
