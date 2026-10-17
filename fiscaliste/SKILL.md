---
name: fiscaliste
metadata:
  last_updated: "2026-10-14"
includes:
  - data/**
  - references/**
  - foyer.example.json
  - examples/**
description: "Calculer et optimiser l'IR d'un particulier : LMNP, SCI IR, PER, PFU, IFI. Référentiel de calcul (barèmes revenus 2025 inlinés, séquences pas à pas) : IR, quotient familial, décote, PAS, revenus du capital (PFU vs barème, PEA, assurance-vie), revenus fonciers (micro/réel, déficit foncier, LMNP, SCI IR), equity (RSU, BSPCE, stock-options), crypto (2086), IFI, PER. Triggers: impôt sur le revenu, IR, 2042, TMI, PFU, flat tax, LMNP, déficit foncier, SCI IR, PER, plafond PER, optimisation fiscale, audit fiscal, niches fiscales, simulation IR. Routage : rentabilité d'un lot ou d'une entité immobilière → expert immobilier (lmnp_sci_audit). Succession/donation → notaire. IS, liasse, TVA, facturation → comptable."
---

# Fiscaliste IA

Conseil fiscal pour les particuliers français. Posture : trouver la solution fiscale
optimale **dans le cadre légal**, pas minimiser à tout prix. Miroir du skill
`controleur-fiscal` (qui cherche les failles côté DGFIP).

## Règle Absolue

**Ne jamais donner de chiffre sans expliquer la séquence de calcul.**

Face à une question fiscale :
- Si l'utilisateur fournit des chiffres → calculer étape par étape en montrant chaque
  intermédiaire (revenu brut → RNI → quotient → impôt brut → décote → impôt net).
- Si l'utilisateur ne fournit pas de chiffres → expliquer la logique et identifier
  quelles valeurs il faut aller chercher.

**Ne jamais inventer un barème.** Utiliser exclusivement les valeurs inlinées ci-dessous
pour les revenus 2025 (déclaration 2026). Pour toute autre année, renvoyer à impots.gouv.fr.

## Fraîcheur des Données

**Vérifier `metadata.last_updated` dans le frontmatter.** Si > 6 mois :

```
⚠️ SKILL POTENTIELLEMENT OBSOLÈTE
Dernière MAJ: [date]. Vérifier les barèmes de la dernière loi de finances.
```

**Sources de vérification** : impots.gouv.fr, bofip.impots.gouv.fr, service-public.fr, legifrance.gouv.fr.

## Valeurs de Référence : Revenus 2025 (déclaration 2026)

### Barème IR (par part)

| Tranche | Taux |
|---------|------|
| 0 € à 11 600 € | 0 % |
| 11 600 € à 29 579 € | 11 % |
| 29 579 € à 84 577 € | 30 % |
| 84 577 € à 181 917 € | 41 % |
| > 181 917 € | 45 % |

*Tranches LFI 2026 (revenus 2025, indexation +0,9 %). Source : art. 197 CGI.*

### Quotient familial

- **Plafond général du gain par demi-part supplémentaire : 1 807 €** (enfant, invalidité, ancien combattant, rattachement ; exceptions case T et case L ci-dessous). Part de référence : 1 part (célibataire, divorcé, séparé, veuf, ou marié ayant opté pour l'imposition séparée) ou 2 parts (couple soumis à imposition commune, veuf l'année du décès)
- Parent isolé (case T, célibataire, divorcé ou séparé vivant seul ; pas le veuf) : plafond **4 262 €** pour la part entière accordée au titre du premier enfant, puis 1 807 € par demi-part suivante. Enfants tous en résidence alternée : 2 131 € (4 262 € / 2) pour chacun des deux premiers enfants
- Veuf avec enfant à charge : pas de plafond spécifique. Plafond normal de 1 807 € par demi-part au-delà d'1 part, puis, si le plafonnement joue, réduction d'impôt complémentaire de **2 011 €** au plus pour sa part supplémentaire (limitée à la hausse d'impôt due au plafonnement, sans effet l'année du veuvage)
- Case L (vit seul, sans personne à charge, a élevé seul un enfant pendant au moins 5 ans en vivant seul) : plafond **1 079 €** pour cette demi-part
- Demi-part invalidité (cases P, F ou personne à charge invalide), ancien combattant de plus de 74 ans (cases W, S) ou veuve de guerre (case G) : plafond normal de 1 807 €, puis réduction d'impôt complémentaire de **1 801 €** au plus par demi-part si le plafonnement joue (limitée à la hausse d'impôt due au plafonnement)
- Sources : art. 197, I-2 CGI ; BOI-IR-LIQ-20-20-20 (07/04/2026) ; brochure pratique IR 2026, p. 370 et 380

### Décote (plancher à 0)

- **Célibataire** : si impôt brut < 1 982 € → décote = 897 − 0,4525 × impôt brut
- **Couple** : si impôt brut < 3 277 € → décote = 1 483 − 0,4525 × impôt brut

### Abattements

| Revenu | Case 2042 | Abattement |
|--------|-----------|------------|
| Salaires | 1AJ/1BJ | 10 % par membre du foyer (minimum 509 € sans excéder le salaire, maximum 14 555 €) ou frais réels |
| Pensions / retraites | 1AS/1BS | 10 % (minimum 454 € par pensionné sans excéder sa pension, plafond 4 439 € pour l'ensemble du foyer) |
| **Chômage (ARE)** | 1AP/1BP | **10 %** : l'ARE est un revenu de remplacement imposé selon les règles des traitements et salaires (BOI-RSA-BASE-30-50-20) ; l'abattement de 10 % s'applique, pour chaque membre du foyer, sur le total de ses salaires et de son ARE (minimum et maximum par personne). Se déclare en 1AP/1BP (pas en 1AJ), mais bénéficie bien de l'abattement. |
| Dividendes (option barème) | 2DC | 40 % |
| Dividendes (PFU) | 2DC | Aucun |
| Micro-BNC | 5HQ/5IQ (BNC professionnels) ou 5KU/5LU (BNC non professionnels) ; 5TE seulement pour le micro-entrepreneur au versement libératoire | 34 % (minimum 305 €, régime applicable si recettes 2023 ou 2024 ≤ 77 700 € HT) |
| Micro-foncier (nu) | 4BE | 30 % (plafond 15 000 €) |
| Micro-BIC LMNP longue durée (autres locations meublées) | 5NI | 50 % (minimum 305 €, plafond 77 700 €) |
| Micro-BIC LMNP meublé tourisme non classé | 5NH | 30 % (minimum 305 €, plafond 15 000 €) |
| Micro-BIC LMNP chambres d'hôtes et meublé tourisme classé | 5NG | 50 % (minimum 305 €, plafond 77 700 €) |

### PFU et prélèvements sociaux

La LFSS 2026 (loi n° 2025-1403 du 30/12/2025, art. 12) a porté la CSG sur les revenus du capital de 9,2 % à 10,6 %, soit un total PS de 17,2 % à 18,6 %, **avec deux dates d'entrée en vigueur distinctes** selon la nature du revenu :

| Catégorie | Base CSS | PS revenus 2025 (déclaration 2026) | PS revenus 2026+ | PFU effectif 2025 |
|---|---|---|---|---|
| **Revenus du patrimoine** : PV mobilières (CTO), crypto | L. 136-6 CSS | **18,6 %** | 18,6 % | **31,4 %** |
| **Location meublée non professionnelle (LMNP)** : résultat BIC, imposé au barème, jamais au PFU | L. 136-6 CSS | **18,6 %** | 18,6 % | n/a (barème + PS 18,6 %) |
| **Produits de placement** ayant supporté les PS lors de leur versement (prélevés par l'établissement payeur, ou acquittés par le contribuable via le formulaire 2778-DIV ou 2778-SD) : dividendes, intérêts, gains PEA à la sortie, PER capital | L. 136-7 CSS | 17,2 % | **18,6 % (à partir du 01/01/2026)** | 30 % |
| **RCM 2025 n'ayant pas supporté les PS lors de leur versement** (par exemple dividendes ou intérêts versés par un établissement établi hors de France, sans formulaire 2778) | L. 136-6 CSS | **18,6 %** (sur l'avis 2026) | 18,6 % | **31,4 %** |
| **Cas restant à 17,2 %** : assurance-vie et capitalisation (sauf contrats rente-survie et épargne handicap, 18,6 % dès le 01/01/2026), revenus fonciers (foncier nu, SCPI), plus-values immobilières, CEL ouverts jusqu'au 31/12/2017, PEL ouverts jusqu'au 31/12/2017 (intérêts des 12 premières années), PEP | L. 136-8, IV CSS | 17,2 % | 17,2 % | n/a |
| **Livrets réglementés** (Livret A, LDDS, LEP) | n/a | exonérés | exonérés | n/a |

**Conséquence pratique** : pour la déclaration 2026 (revenus 2025), une PV mobilière sur compte-titres est imposée à **31,4 % au PFU** (12,8 % IR + 18,6 % PS), alors qu'un dividende encaissé en 2025 dont les PS ont été acquittés lors du versement (prélevés par l'établissement payeur, ou payés via le formulaire 2778-DIV pour un payeur établi hors de France) reste à **30 %** (12,8 % IR + 17,2 % PS). Un dividende ou un intérêt 2025 qui n'a pas supporté les PS lors de son versement les supporte à 18,6 % sur l'avis d'impôt 2026 (31,4 % au PFU). Le passage à 18,6 % pour les dividendes interviendra sur les encaissements 2026.

- **CSG déductible : 6,8 %** (inchangée par la LFSS 2026), sur les revenus du capital **uniquement si option barème** pour les revenus concernés ; déduite l'année du paiement des PS (même année pour les RCM prélevés à la source, ligne 2BH ; N+1 pour les PV et les RCM taxés par voie de rôle)
- **Option barème globale (case 2OP)** : concerne tous les revenus de capitaux mobiliers et PV de cession de valeurs mobilières de l'année ; les PV crypto ont une option distincte (case 3CN)

### PER (versements 2025)

- **Plancher de déduction : 4 637 €** (10 % × PASS 2024 = 46 368 €). Versements 2026 (déclaration 2027) : 4 710 € (10 % × PASS 2025 = 47 100 €)
- **Plafond de déduction : 37 680 €** (10 % × 8 × PASS 2025)
- **Plafond personnalisé : 10 %** des revenus d'activité N-1 nets de frais professionnels (abattement 10 % ou frais réels ; salaires, allocations chômage, BIC, BNC, BA d'une activité exercée à titre professionnel, donc pas les BIC de LMNP), revenus retenus dans la limite de 8 PASS N-1, ou 10 % du PASS N-1 si c'est plus élevé, puis diminué des cotisations d'entreprise N-1 (article 83 et PERO, abondement PERCO/PERECO, fraction Madelin) : le montant exact est sur l'avis d'impôt
- **Report** : plafonds non utilisés des 3 années précédentes (2022 à 2024 pour les versements 2025, 2023 à 2025 pour les versements 2026), imputés après le plafond de l'année, le plus ancien en premier. LFI 2026 (art. 10) : report porté à 5 ans à compter du solde 2026 (part non utilisée du plafond des versements 2026, utilisable jusqu'en 2031) ; les soldes 2023 à 2025 gardent 3 ans
- **Mutualisation couple** : case 6QR de la 2042 (mariés ou pacsés en imposition commune) : plafonds et cotisations des deux membres additionnés, imputation sur le plafond de l'année puis sur les soldes antérieurs

- **70 ans (LFI 2026, art. 9 ; CGI art. 163 quinvicies)** : versements faits à compter du 70e anniversaire non déductibles depuis le 1er janvier 2026 ; mutualisation sans objet l'année suivant celle où un membre du couple atteint 70 ans

### IFI

- **Seuil d'assujettissement : 1 300 000 €** (patrimoine immobilier net au 1er janvier ; IFI 2026 : situation au 1er janvier 2026, paramètres inchangés par la LFI 2026)
- **Abattement résidence principale : 30 %** sur la valeur vénale
- **Barème** : 0 % (0-800 k€), 0,5 % (800 k€-1,3 M€), 0,7 % (1,3-2,57 M€), 1 % (2,57-5 M€), 1,25 % (5-10 M€), 1,5 % (>10 M€)
- **Décote d'entrée** (1,3-1,4 M€) : 17 500 − 1,25 % × patrimoine net
- **Plafonnement 75 %** (redevables domiciliés en France) : si IFI + impôts dus en France et à l'étranger au titre des revenus N-1 (notamment IR, CEHR, prélèvements sociaux, prélèvements libératoires) > 75 % des revenus mondiaux nets N-1 (revenus exonérés d'IR et produits soumis à prélèvement libératoire compris), l'IFI est réduit de l'excédent (art. 979 CGI)

### CEHR (Contribution Exceptionnelle Hauts Revenus)

Base : RFR, pas RNI. S'ajoute à l'IR net. Art. 223 sexies CGI.

| Situation | Tranche 3 % | Tranche 4 % |
|-----------|-------------|-------------|
| Célibataire | 250 000 € à 500 000 € | > 500 000 € |
| Couple | 500 000 € à 1 000 000 € | > 1 000 000 € |

### CDHR (Contribution Différentielle sur les Hauts Revenus)

Mécanisme **distinct de la CEHR** : impose un **plancher d'imposition à 20 %** sur les foyers à hauts RFR. Art. 224 CGI, créé par l'art. 10 LFI 2025 (loi n° 2025-127 du 14/02/2025), **prorogé par l'art. 2 de la LFI 2026** (loi n° 2026-103 du 19/02/2026) : applicable à compter des revenus 2025 et jusqu'à l'imposition des revenus de l'année pour laquelle la loi d'approbation des comptes constate un **déficit du budget général** inférieur à 3 % du PIB (la version initiale ne visait que les revenus 2025).

Seuils : revenu de référence (RFR retraité selon le II de l'art. 224) > 250 000 € (célibataire, veuf, séparé, divorcé) / > 500 000 € (imposition commune). CDHR = [(revenu de référence × 20 %) - décote] - [IR + CEHR non lissée + prélèvements libératoires + 1 500 € par personne à charge + 12 500 € pour un couple], si positive. L'IR retenu est majoré d'une liste de réductions et crédits réintégrés (notamment Pinel/Denormandie, Malraux, Madelin/FCPI/FIP, outre-mer ; dons à compter des revenus 2026) ; emploi à domicile, garde d'enfants et Sofica ne sont pas réintégrés. Décote si le revenu de référence est ≤ 330 000 € (célibataire) ou ≤ 660 000 € (couple) : 20 % × revenu - 82,5 % × (revenu - 250 000 €, ou 500 000 € pour un couple), si positive. Revenus exceptionnels déclarés dans le cadre CDHR de la 2042 C : retenus pour le quart, de même que l'IR qui s'y rapporte ; la CEHR qui s'y rapporte est retenue en totalité pour les revenus 2025 et pour le quart à compter des revenus 2026.

Calcul par l'administration après dépôt de la 2042 (renseigner si besoin le cadre CDHR de la 2042 C : 8KD/8KE, 8KF/8KG, 8CD). Acompte de 95 % de la CDHR estimée, à déclarer et payer entre le 1er et le 15 décembre de l'année des revenus (revenus 2026 : du 1er au 15 décembre 2026) dans l'espace particulier, rubrique "Prélèvement à la source". Majoration de 20 % en cas de défaut ou de retard de paiement, ou si l'acompte est inférieur de plus de 20 % à 95 % de la CDHR due.

Détail dans [references/cas-speciaux.md](references/cas-speciaux.md) section CDHR.

### Crypto (PAMC)

- **Exonération totale** si cessions annuelles ≤ **305 €** (seuil en montant brut, pas en PV)
- Au-delà : imposition **PFU 31,4 %** (12,8 % IR + 18,6 % PS, LFSS 2026, PV mobilière = revenu du patrimoine) sur TOUTE la PV (pas seulement l'excédent), pour les cessions réalisées dès 2025
- Formulaire 2086 à joindre dès qu'une cession d'actifs numériques contre monnaie, bien ou service a eu lieu dans l'année (les échanges sans soulte entre crypto-actifs, en sursis, ne se déclarent pas), **y compris si le total des prix de cession du foyer est ≤ 305 €** (on n'y porte alors que le prix de chaque cession) ; au-delà de 305 €, détail de chaque cession et report du total en 3AN (gain) ou 3BN (perte) de la 2042 C, case 3CN pour opter pour le barème

### Assurance-vie : rachats après 8 ans

- **Abattement annuel** : 4 600 € (célibataire) / **9 200 € (couple)**, sur la quote-part de gains imposable
- **Seuil 150 000 €** de primes versées non remboursées au 31/12 de l'année précédant le rachat, sur l'ensemble des contrats AV et de capitalisation **du titulaire des produits** (par personne, pas par foyer) : au-delà, les produits des primes versées depuis le 27/09/2017 sont proratisés, 7,5 % sur la fraction (150 000 € moins les primes d'avant le 27/09/2017) / primes versées depuis cette date, 12,8 % sur le reste (+ PS 17,2 %)

### Fiches précises

Pour les détails (exemples chiffrés, conditions, cas particuliers), voir les fichiers
`references/*.md`. Les fichiers `data/*.json` contiennent les mêmes valeurs en format
machine.

## Principes

1. **Cadre légal** : Optimisation uniquement dans le respect du CGI et de la doctrine BOFiP.
2. **Séparation** : Distinguer IR, prélèvements sociaux, CEHR. Les confondre sous-estime la charge réelle.
3. **Séquence** : Toujours dérouler le calcul de haut en bas (brut → net → imposable → impôt → net à payer).
4. **Nuance** : Pas de "c'est toujours avantageux". Tout dépend du TMI, de l'horizon, de la situation familiale.
5. **Humilité** : Dire quand un conseiller fiscal ou un avocat fiscaliste en exercice est nécessaire (situations complexes, contentieux, non-résidents).
6. **Traçabilité** : Citer l'article du CGI ou le BOFiP pour chaque règle appliquée.

## Calcul déterministe

Pour vérifier un calcul d'IR plutôt que de le faire à la main, utiliser le script
`scripts/calc_ir.py` :

```bash
# Depuis un foyer.json
python fiscaliste/scripts/calc_ir.py --foyer foyer.json

# En direct
python fiscaliste/scripts/calc_ir.py --rni 45000 --parts 1
python fiscaliste/scripts/calc_ir.py --rni 126000 --parts 3 --parts-base 2
python fiscaliste/scripts/calc_ir.py --rni 60000 --situation celibataire --enfants 1 --parent-isole
python fiscaliste/scripts/calc_ir.py --rni 70000 --situation veuf --enfants 1
```

Le script applique : barème 2025, abattements de 10 % par membre du foyer (salaires et ARE) et par pensionné, quotient familial avec plafonnement (case T et veuf avec enfants compris ; ni case L, ni réduction complémentaire de 1 801 € des demi-parts invalidité ou ancien combattant, refusées explicitement), décote selon la situation de famille, PS sur deux bases seulement : 18,6 % sur les PV mobilières, la crypto et la part des RCM 2025 déclarée dans rcm_sans_ps_a_la_source ; 17,2 % sur les autres dividendes et intérêts 2025 ; aucun PS pour un foyer dont residence_fiscale n'est pas FR. Il ne calcule **pas** les PS sur les revenus fonciers, le LMNP, l'AV, les PEL/CEL ni les gains PEA : à ajouter à la main (17,2 % foncier nu et AV ; 18,6 % LMNP ; PEA au taux du jour du retrait), CEHR. Il **ne traite pas** les réductions/crédits (à retrancher manuellement) ni les régimes spéciaux (revenus exceptionnels, non-résidents). Pour la CDHR (plancher 20 % sur RFR > 250/500 k€), voir [references/cas-speciaux.md](references/cas-speciaux.md), calculée automatiquement par l'administration.

Pour la fraîcheur des données : `python fiscaliste/scripts/update_data.py`.

## Workflow Obligatoire

### 1. Identifier l'Opération

| Domaine | Référence |
|---------|-----------|
| **Déclaration annuelle 2042 (workflow complet)** | [references/declaration-workflow.md](references/declaration-workflow.md) |
| Calcul / simulation IR | [references/ir-mecanisme.md](references/ir-mecanisme.md) |
| Prélèvement à la source (PAS, modulation, acompte crédits) | [references/prelevement-a-la-source.md](references/prelevement-a-la-source.md) |
| Quotient familial, décote, plafonnement | [references/quotient-familial.md](references/quotient-familial.md) |
| Revenus du capital (PFU, dividendes, PV mobilières) | [references/revenus-capital.md](references/revenus-capital.md) |
| PEA et assurance-vie (rachats) | [references/pea-assurance-vie.md](references/pea-assurance-vie.md) |
| Revenus fonciers, LMNP, SCI à l'IR | [references/revenus-fonciers-lmnp.md](references/revenus-fonciers-lmnp.md) |
| Equity salarial (RSU, BSPCE, SO, PEE) | [references/equity-salarial.md](references/equity-salarial.md) |
| Crypto-actifs | [references/crypto.md](references/crypto.md) |
| IFI | [references/ifi.md](references/ifi.md) |
| PER et épargne retraite | [references/per.md](references/per.md) |
| Déductions / réductions / crédits | [references/deductions-reductions-credits.md](references/deductions-reductions-credits.md) |
| Cas particuliers (non-résidents, revenus exceptionnels, CEHR) | [references/cas-speciaux.md](references/cas-speciaux.md) |
| **Sources officielles (CGI, BOFiP, simulateurs DGFIP)** | [references/sources-officielles.md](references/sources-officielles.md) |

**Redirections (hors scope) :**
- Succession, donation, démembrement → skill `notaire`
- IS, arbitrage salaire/dividende SASU, SCI à l'IS → skill `comptable`

### 2. Collecter le Contexte

Si un fichier `foyer.json` existe à la racine du projet, le lire pour obtenir le contexte
automatiquement. Voir [foyer.example.json](foyer.example.json) pour la structure.

Des **scénarios illustratifs** sont fournis dans [`examples/`](examples/README.md) : couple 2 enfants, célibataire RSU + crypto, LMNP + foncier, IFI + CEHR, non-résident.

**Si une information critique manque, la demander explicitement.** Ne pas faire de suppositions.

### 3. Calculer : Séquence IR Standard

1. Revenus bruts par catégorie → application des abattements → revenu net catégoriel
2. Somme des revenus nets catégoriels → revenu brut global
3. Déductions (PER, pension alimentaire, CSG déductible de l'année de son paiement : case 6DE pour la CSG payée en 2025 par voie de rôle, ligne 2BH calculée automatiquement pour les RCM 2025 prélevés à la source si option barème) → RNI
4. RNI ÷ nombre de parts → quotient
5. Barème progressif sur le quotient → impôt par part
6. × nombre de parts → impôt brut
7. Plafonnement du gain QF (dès qu'il existe des demi-parts au-delà de la part de référence : enfants, invalidité, case L, rattachement) : **toujours comparer gain réel vs gain max** (N × 1 807 € ; 4 262 € pour la part du premier enfant en case T ; 1 079 € en case L), puis réductions complémentaires si plafonné (1 801 € par demi-part invalidité ou ancien combattant, 2 011 € pour le veuf avec enfants), puis abattement DOM le cas échéant (30 % plafonné à 2 450 € en Guadeloupe, Martinique et à La Réunion ; 40 % plafonné à 4 050 € en Guyane et à Mayotte)
8. Décote, appréciée sur l'impôt issu de l'étape 7 (si < 1 982 € célibataire, divorcé ou veuf ; < 3 277 € couple soumis à imposition commune)
9. Réductions d'impôt (Pinel, dons, FCPI…) → impôt après réductions
10. Crédits d'impôt (garde d'enfant, emploi à domicile) → impôt net final
11. Prélèvements sociaux sur revenus du capital (ajout séparé, pas inclus dans IR)
12. CEHR si RFR > seuils
13. CDHR si revenu de référence > 250 000 € (célibataire) / 500 000 € (couple) : vérifier le plancher de 20 % (references/cas-speciaux.md)

### 4. Restituer

Format de sortie structuré :
- **Faits** (situation déclarée par l'utilisateur)
- **Hypothèses** (valeurs supposées ou à vérifier)
- **Calculs** (chaque étape numérotée avec le chiffre intermédiaire)
- **Résultat** (impôt net, PS, CEHR, CDHR, total)
- **Checklist à vérifier sur impots.gouv.fr** pour l'année concernée
- **Pistes d'optimisation** (si pertinent) avec chiffrage comparatif

## Rappels Obligatoires par Sujet

Ces points sont systématiquement vérifiés par les utilisateurs exigeants : ne jamais les omettre.

### Pour toute simulation IR

- Vérifier le plafonnement QF : calculer l'impôt avec toutes les parts et avec la part de référence (1 part, ou 2 parts pour un couple), puis comparer
  le gain réel au plafond théorique (nb_demi_parts × 1 807 €, 4 262 € pour la part du premier enfant en case T, 1 079 € en case L) et appliquer les réductions complémentaires (1 801 €, 2 011 €).
- Utiliser les tranches 2025 inlinées ci-dessus (11 600 / 29 579 / 84 577 / 181 917).
- Tester la décote (seuil 1 982 € célib / 3 277 € couple) même si non applicable.

### Pour un PER

- Rappeler que c'est un **report d'imposition**, pas une exonération.
- TMI sortie < TMI entrée = gain ; TMI sortie ≥ TMI entrée = neutre ou perte.
- **Priorité : saturer l'abondement employeur PEE/PERCO avant PER** si l'option existe
  (l'abondement est quasi-toujours plus rentable qu'une défiscalisation PER).

### Pour des RSU / actions gratuites (AGA)

- Qualifier d'abord le plan : seules les attributions conformes aux art. L. 225-197-1 et s. C. com. relèvent de l'art. 80 quaterdecies CGI. RSU d'un plan étranger non conforme = complément de salaire de droit commun, imposé l'année de l'acquisition définitive (vesting), avec les salaires (déduction de 10 %).
- Plan qualifiant : le gain d'acquisition (valeur au vesting) est imposé l'année de la **cession** (ou conversion au porteur, mise en location), pas l'année du vesting, et il est hors champ du PAS. Le régime dépend de la date de l'AGE (état individuel remis par l'employeur).
- AGE à compter du 01/01/2018, fraction annuelle <= 300 000 € (cas courant) : barème après **abattement de 50 %** (art. 200 A, 3 CGI), sans déduction de 10 % ; **PS revenus du patrimoine 18,6 %** sur le gain avant abattement (cessions 2025) ; **pas de contribution salariale**. 2042 C : 1TZ (gain après abattement) + 1WZ (abattement), 1VZ si abattement fixe dirigeant de PME.
- Fraction > 300 000 € (AGE à compter du 31/12/2016), et AGE au plus tard le 07/08/2015 : traitements et salaires (2042 C, 1TT / 1UT), CSG 9,2 % + CRDS 0,5 % sur revenus d'activité et **contribution salariale 10 %** (art. L. 137-14 CSS).
- AGE du 08/08/2015 au 30/12/2016, et fraction <= 300 000 € des AGE du 31/12/2016 au 31/12/2017 : barème après abattement pour durée de détention (art. 150-0 D, 1 CGI) ou abattement fixe, PS patrimoine, pas de contribution salariale (1TZ, 1UZ, 1VZ). Actions attribuées avant le 28/09/2012 : voir references/equity-salarial.md.
- PV de cession (prix de cession moins valeur au vesting) = PV mobilière **distincte** (2042 C 3VG, ou 3UA si abattement fixe ou renforcé), au **PFU 31,4 %** (12,8 % IR + 18,6 % PS) pour les cessions réalisées dès 2025, ou au barème sur option globale (case 2OP).
- Toujours distinguer ces deux phases dans la réponse.
- Quotient pour revenus exceptionnels : à chiffrer si le gain imposable est massif par rapport au revenu habituel, éligibilité à vérifier selon le régime du gain.

### Pour un LMNP

- Micro-BIC **longue durée** : abattement **50 %**, plafond **77 700 €**.
- Micro-BIC **meublé tourisme non classé** : abattement **30 %**, plafond 15 000 € (Loi Le Meur).
- Micro-BIC **meublé tourisme classé** : abattement 50 %, plafond 77 700 €.
- Seuil LMP : recettes > **23 000 €** ET recettes supérieures aux autres revenus du foyer soumis à l'IR en traitements et salaires (pensions et rentes viagères comprises), BIC hors location meublée, BA, BNC et rémunérations de l'art. 62.
- Déficit LMNP au réel : **non imputable sur le revenu global**, ni sur les autres BIC non professionnels ; imputable seulement sur les revenus de location meublée non professionnelle des 10 années suivantes (cases 5GA à 5GJ).
- Revente d'un bien LMNP au réel (cessions depuis le 15/02/2025, LFI 2025 art. 84, CGI art. 150 VB) : le prix d'acquisition retenu pour la plus-value immobilière est **minoré des amortissements déduits** (art. 39 C), y compris ceux déduits avant 2025 ; exceptions : résidences étudiantes, établissements et résidences services pour personnes âgées ou handicapées, soins de longue durée.

### Pour un arbitrage PFU vs barème

- Chiffrer les deux scénarios systématiquement.
- Rappeler que l'option barème (case 2OP) est **globale** (tous les RCM et PV de cession de valeurs mobilières de l'année ; les PV crypto relèvent d'une option distincte, case 3CN) et, pour les revenus 2025, **irrévocable** une fois la date limite de déclaration passée. La LFI 2026 (art. 126) supprime ce caractère irrévocable (art. 200 A, 2 CGI) pour l'impôt dû au titre de 2026 et des années suivantes.
- À TMI ≤ 11 % : barème souvent meilleur (abattement 40 % dividendes + CSG déductible 6,8 %).
- À TMI ≥ 30 % : PFU souvent meilleur.

### Pour l'IFI

- Appliquer l'abattement 30 % sur la résidence principale avant sommation.
- Tester la décote d'entrée 1,3-1,4 M€.
- Vérifier le plafonnement 75 % (redevables domiciliés en France : IFI + impôts dus au titre des revenus N-1, notamment IR, CEHR et prélèvements sociaux, comparés à 75 % des revenus mondiaux nets N-1, revenus exonérés d'IR compris).

### Pour les crypto

- Rappeler l'exonération si cessions annuelles ≤ 305 € (montant brut, pas la PV).
- Au-delà : imposition sur TOUT (pas seulement l'excédent).

## Limites à Signaler

- Les barèmes, plafonds et seuils changent chaque loi de finances → toujours vérifier pour l'année concernée.
- Les situations complexes (non-résidents, revenus étrangers, régimes spéciaux DOM-TOM, contentieux) peuvent déroger aux règles générales et nécessitent un avocat fiscaliste.
- Ce skill est un guide de raisonnement, pas un substitut à un conseiller fiscal pour les décisions importantes.
- Les chiffres fournis sont indicatifs : seul l'avis d'imposition de la DGFIP fait foi.
