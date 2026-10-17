# Equity salarial (RSU, BSPCE, stock-options, PEE/PERCO)

Voir `data/equity-salarial.json` pour les taux et seuils.

## RSU / AGA (Restricted Stock Units / Actions Gratuites)

**Terminologie** : "RSU" (Restricted Stock Units) est le terme anglo-saxon ; "AGA" (attribution gratuite d'actions) désigne le dispositif français (art. L. 225-197-1 et s. C. com., art. 80 quaterdecies CGI). Ils ne se confondent pas : des RSU ne relèvent du régime de l'art. 80 quaterdecies que si le plan respecte les conditions du Code de commerce (plan dit qualifiant, BOI-RSA-ES-20-20-20 § 10) ; sinon, le gain est un complément de salaire de droit commun. Dans les deux cas : période d'acquisition (vesting) puis détention éventuelle.

### Deux événements fiscaux distincts, imposés la même année (celle de la cession)

Source : BOI-RSA-ES-20-20-20, version du 21/05/2026 (https://bofip.impots.gouv.fr/bofip/5654-PGP.html/identifiant=BOI-RSA-ES-20-20-20-20260521). Le régime dépend de la **date de la décision d'AGE** qui a autorisé l'attribution et du caractère **qualifiant** du plan (art. L. 225-197-1 et s. C. com.).

**1. Gain d'acquisition** = valeur des actions à la date d'acquisition définitive (vesting)
- Valeur retenue : premier cours coté du jour de l'attribution définitive (§ 120)
- **Fait générateur : la cession** (ou disposition, conversion au porteur, mise en location), pas le vesting (art. 80 quaterdecies CGI ; § 150)
- Une moins-value de cession (vente sous la valeur d'acquisition) s'impute sur le gain d'acquisition correspondant, avant application des abattements, dans la limite de ce montant (§ 190) ; la limite annuelle de 300 000 € s'apprécie après cette imputation ; les moins-values de cession d'autres valeurs mobilières ne s'imputent pas sur un gain d'acquisition

**2. Plus-value de cession** = prix de cession − valeur à la date d'acquisition définitive
- **PV mobilière** (§ 170) : PFU à **31,4 % pour les cessions réalisées dès 2025** (12,8 % IR + 18,6 % PS, LFSS 2026), ou barème sur option globale
- Les PV mobilières sont des "revenus du patrimoine" (art. L. 136-6 CSS), donc soumises au taux PS 18,6 % dès les revenus 2025

### Régime du gain d'acquisition selon la date de l'AGE

| Décision d'AGE | Fraction annuelle ≤ 300 000 € | Fraction > 300 000 € |
|---|---|---|
| **Après le 31/12/2017** (LF 2018 art. 28, régime courant) | Barème **après abattement de 50 %** (art. 200 A, 3 CGI), le cas échéant abattement fixe 150-0 D ter ; **PS revenus du patrimoine** sans abattement (L. 136-6, I-e CSS) ; **pas de contribution salariale** (§ 45 et 50) | Traitements et salaires : barème sans abattement, PS sur revenus d'activité, **contribution salariale 10 %** (L. 137-14 CSS) |
| Du 31/12/2016 au 31/12/2017 | Régime de la ligne « 08/08/2015 au 30/12/2016 » : abattement pour durée de détention ou abattement fixe, PS revenus du patrimoine, pas de contribution salariale (§ 44 et 49). 2042 C : 1TZ, 1UZ, 1VZ | Traitements et salaires, CSG 9,2 % + CRDS 0,5 % sur revenus d'activité, contribution salariale 10 % (§ 44 et 49). 2042 C : 1TT / 1UT |
| Du 08/08/2015 au 30/12/2016 (loi Macron) | Pas de plafond : barème après abattement pour durée de détention des PV mobilières (art. 150-0 D, 1 CGI, droit commun 50 % de 2 à 8 ans et 65 % au-delà, ou renforcé, durée décomptée depuis l'acquisition définitive) ou abattement fixe 150-0 D ter, sans déduction de 10 % ; PS revenus du patrimoine ; contribution salariale supprimée (§ 43 et 48). 2042 C : 1TZ, 1UZ, 1VZ | sans objet |
| Au plus tard le 07/08/2015 (actions attribuées depuis le 28/09/2012) | Traitements et salaires de droit commun, CSG 9,2 % + CRDS 0,5 % sur revenus d'activité, contribution salariale 10 % (§ 40 et 47). 2042 C : 1TT / 1UT | sans objet |
| Actions attribuées avant le 28/09/2012 | Taux de 30 % (2042 C 3VI) ou, sur option, traitements et salaires (3VJ / 3VK) ; PS revenus du patrimoine (§ 46) ; contribution salariale 10 % si attribution depuis le 16/10/2007 (3VN) | sans objet |

La limite de 300 000 € est annuelle, non reportable, et s'apprécie en faisant masse des gains d'acquisition des actions cédées la même année. CSG déductible : quand le gain bénéficie de l'abattement de 50 %, de l'abattement pour durée de détention (droit commun ou renforcé) ou de l'abattement fixe, la CSG déductible (6,8 %, taux inchangé par la LFSS 2026) n'est retenue qu'au prorata du gain après abattement sur le gain avant abattement.

**Plans non qualifiants** (dont des RSU de plans étrangers qui ne respectent pas les art. L. 225-197-1 et s. C. com.) : le gain d'acquisition est un complément de salaire de droit commun, imposé l'année de l'acquisition définitive (BOI-RSA-ES-20-20-20 § 10), à déclarer avec les salaires et non en 1TT ou 1TZ.

### Pièges classiques

Deux erreurs symétriques :
1. **Traiter le gain d'acquisition d'un plan qualifiant comme un salaire** (CSG d'activité, contribution 10 %) : faux sous 300 000 € pour une AGE postérieure à 2017.
2. **Le traiter comme une simple PV mobilière au PFU** : faux, il est au barème après abattement de 50 %, avec PS patrimoine, l'année de la cession.

Seule la plus-value ultérieure (valeur au vesting → cession) est une PV mobilière.

### Stratégie : quotient pour revenus exceptionnels

Une cession massive d'actions gratuites (ex: 150 000 € de gain d'acquisition imposable la même année) fait franchir plusieurs tranches. Le **quotient pour revenus exceptionnels** (coefficient 4) peut lisser l'imposition, sous réserve d'éligibilité : aucune source officielle consultée (BOFiP actions gratuites, brochure IR 2026) ne dit si le gain d'acquisition d'un plan qualifiant (art. 200 A, 3) en relève. Ne pas le promettre avant lecture de BOI-IR-LIQ-20-30-20 ; pour un plan qualifiant, l'événement imposable est la cession, pas le vesting.

Mécanisme : impôt = [IR(RNI_hors_RSU + vesting/4) − IR(RNI_hors_RSU)] × 4. Utile si le vesting seul fait franchir une tranche. **Nuance** : inutile si le foyer est déjà au TMI 45% : le taux marginal ne change pas avec la division. Détail et exemples chiffrés dans la section cas-speciaux listée depuis SKILL.md.

## Stock-options

### Rabais excédentaire

Différence entre prix du marché à l'attribution et prix d'exercice, au-delà de 5%.
→ **Imposé comme salaire l'année de la levée de l'option** (2042 C, 1TP / 1UP).

### Gain de levée

Selon date d'attribution :

| Plan | Régime |
|------|--------|
| Attribuées avant le 28/09/2012 | Taux proportionnels 18 %, 30 % ou 41 % (2042 C 3VD, 3VI, 3VF) ou, sur option, salaires (3VJ / 3VK) ; contribution salariale 10 % si attribution depuis le 16/10/2007 (3VN) |
| Attribuées à compter du 28/09/2012 | Gain de levée imposé en traitements et salaires l'année de la cession des actions (2042 C 1TT / 1UT), CSG 9,2 % + CRDS 0,5 % sur revenus d'activité, contribution salariale 10 % (art. L. 137-14 CSS) |

Toujours consulter le plan pour déterminer le régime applicable.

## BSPCE (Bons de Souscription de Parts de Créateur d'Entreprise)

**Différence clé vs RSU** : l'imposition intervient l'année de la **cession des titres** (ou conversion au porteur, mise en location). Pour les titres souscrits depuis le 01/01/2025 (LF 2025, art. 92), on distingue le **gain d'exercice** (valeur des titres au jour de l'exercice moins prix fixé à l'attribution), taxé à 12,8 % (2042 C 3PC) ou, sur option, au barème selon les règles des traitements et salaires (1AY / 1BY), et à 30 % sans option si l'activité dans la société a duré moins de 3 ans (3PE), et le **gain de cession** (prix de cession moins valeur au jour de l'exercice), imposé comme une PV mobilière de droit commun (3TL). Les deux supportent les PS des revenus du patrimoine (BOI-RSA-ES-20-40-40, version du 28/05/2026, § 60 à 150). Titres souscrits jusqu'au 31/12/2024 : un gain unique (3SJ, 3TJ, 3SK).

### Imposition du gain de cession

Voir `data/equity-salarial.json` → `bspce.gain_cession`.

| Ancienneté dans la société à la date de cession | Taux global pour cessions 2025 |
|--------------------------------------------------|-------------|
| **≥ 3 ans** | **31,4 %** (12,8 % IR + 18,6 % PS) : PV mobilière |
| **< 3 ans** | 50 % (30 % IR + 20 % PS, contribution salariale spécifique) |

Note : pour les cessions ≥ 3 ans, le PS suit le taux applicable aux PV mobilières (revenus du patrimoine, L. 136-6 CSS), soit 18,6 % dès 2025. Pour les cessions < 3 ans, la part PS reste à 20 % (contribution salariale spécifique, distincte du PS de droit commun).

La pénalité pour départ précoce (< 3 ans) est forte. À intégrer dans les décisions de départ.

### Conditions d'éligibilité de la société

À vérifier avant attribution :
- Société par actions passible de l'IS : française ou, depuis le 01/01/2020, dont le siège est dans l'UE ou un État de l'EEE conventionné (impôt équivalent à l'IS)
- Immatriculée depuis moins de 15 ans
- Non cotée, ou cotée (marché réglementé ou organisé de l'EEE) avec une capitalisation boursière inférieure à 150 M€ ; attribution encore possible 3 ans après le franchissement
- Soumise à l'IS
- Capital détenu à 25 % au moins, de manière continue, par des personnes physiques ou par des personnes morales elles-mêmes détenues à 75 % au moins par des personnes physiques
- Pour les BSPCE attribués avant le 08/08/2015 seulement : ne pas avoir été créée dans le cadre d'une concentration, restructuration, extension ou reprise d'activités préexistantes
- Conditions modifiées pour les bons attribués depuis le 01/01/2026 (LF 2026, art. 25) : à vérifier

**Si conditions non remplies** : requalification en salaires → barème IR + cotisations sociales → traitement beaucoup plus défavorable.

### Vérification préalable recommandée

Demander à la société :
- Date d'immatriculation au RCS
- Capital social et répartition (tableau des associés)
- Régime fiscal (IS obligatoire)
- Historique des restructurations éventuelles

## Épargne salariale (PEE / PERCO / PERO)

### PEE (Plan d'Épargne Entreprise)

Enveloppe collective distincte du PER individuel.

- **Abondement employeur** : exonéré d'IR dans la limite du plafond, mais soumis à CSG et CRDS : **AVANTAGE MAJEUR**
- **Plafond abondement** : 8 % du PASS par bénéficiaire (art. R. 3332-8 C. trav.), soit 3 768 € pour 2025 (PASS 47 100 €) et 3 844,80 € pour 2026 (PASS 48 060 €), sans dépasser le triple du versement du salarié ; plafond porté à 6 920,64 € pour 2026 quand le versement sert à acquérir des titres de l'entreprise
- **Blocage** : 5 ans sauf cas de déblocage anticipé (mariage, naissance 3e enfant, achat RP, divorce avec enfant, fin contrat travail, surendettement, invalidité, décès, violences conjugales)
- **Sortie après 5 ans** : exonération IR, seuls les PS restent dus sur les gains (produits de placement, art. L. 136-7 CSS : 17,2 % pour une sortie en 2025 ; 18,6 % à compter du 01/01/2026, sous réserve de l'exception de la LFSS 2026, art. 12, II, 2° pour les produits acquis ou constatés avant le 01/01/2026 relevant des taux historiques : à vérifier pour les gains de PEE)
- **Dividendes réinvestis** : exonérés IR tant qu'ils restent dans l'enveloppe

### PERCO / PERO (PER d'entreprise)

- **Sortie à la retraite** : rente ou capital
- **Fiscalité sortie** : même que PER individuel (versements à barème, gains au PFU)
- **Abondement employeur** : exonéré d'IR dans les plafonds, CSG et CRDS dues comme pour l'abondement PEE (16 % du PASS, soit 7 536 € pour 2025 et 7 689,60 € pour 2026, distinct du plafond PEE, sans dépasser le triple du versement du salarié)

### Arbitrage PEE/PERCO vs PER individuel

| Enveloppe | Avantage unique | Quand privilégier |
|-----------|----------------|-------------------|
| PEE | Abondement employeur (levier +30% à +300%) | D'abord, toujours, tant qu'il y a abondement |
| PERCO / PERO | Abondement employeur sur épargne retraite | En second après PEE max |
| PER individuel | Déduction RNI (pas de plafond d'abondement) | En complément, après saturation PEE/PERCO |

**Règle d'or** : ne jamais abonder un PER individuel avant d'avoir saturé l'abondement employeur PEE + PERCO. L'abondement est de l'argent gratuit.

## Quotient pour revenus exceptionnels

Vesting massif, cession d'entreprise, indemnité de départ → à étudier (pour un gain d'actions gratuites, éligibilité à vérifier selon le régime du gain, voir la stratégie ci-dessus).

**Mécanisme** :
1. Revenu exceptionnel ÷ coefficient (généralement 4)
2. Ajouter au revenu ordinaire
3. Calculer l'impôt supplémentaire
4. × coefficient

**À mentionner systématiquement** pour :
- Vesting RSU > 1,5 × salaire annuel
- Cession de parts de société
- Indemnité de départ importante
- Prime exceptionnelle massive

**Inutile si** : foyer déjà à TMI 45% (taux marginal identique quelle que soit la division).

## Formulaires

| Revenu | Formulaire / case |
|--------|-------------------|
| Gain acquisition RSU (salaire) | 2042 case 1TT / 1UT |
| Plus-value cession RSU | 2042 C case 3VG (PFU) ou 2074 (détail) |
| Gain BSPCE | 2042 C : titres souscrits jusqu'au 31/12/2024 : 3SJ (19 %), 3TJ (12,8 % ou barème), 3SK (30 %) ; titres souscrits depuis le 01/01/2025 : gain d'exercice 3PC (12,8 %) ou 3PE (30 %), option salaires 1AY / 1BY, gain de cession 3TL |
| Abondement PEE (information) | Déclaration employeur, exonéré |
| Stock-options | Variable selon plan, consulter le plan |

## Références CGI / BOFiP

- RSU : art. 80 quaterdecies CGI
- Stock-options : art. 80 bis CGI
- BSPCE : art. 163 bis G CGI
- PEE : art. L. 3332-1 et s. Code du travail
- PER : art. 163 quatervicies CGI
- BOFiP : BOI-RSA-ES (actionnariat salarié)
