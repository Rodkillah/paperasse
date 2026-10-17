# Quotient familial et plafonnement

## Calcul des parts

Le quotient familial réduit le revenu taxable en augmentant le nombre de parts.

### Parts de base selon situation

| Situation | Parts de base |
|-----------|--------------|
| Célibataire, divorcé, séparé | 1 |
| Marié, pacsé (imposition commune) | 2 |
| Veuf sans enfant | 1 |
| Veuf avec enfant(s) à charge | 2 (+ parts enfants : 2,5 avec un enfant) ; plafonnement calculé par rapport à 1 part, puis réduction complémentaire de 2 011 € au plus (revenus 2025) |
| Veuf dont le conjoint est décédé en 2025 | Deux déclarations : commune jusqu'au décès (2 parts + enfants), puis individuelle du survivant avec les mêmes parts ; sur celle-ci, plafonnement par rapport à 2 parts, sans réduction complémentaire, et décote des personnes seules (897 €) |

### Majoration pour enfants à charge

| Rang de l'enfant | Parts ajoutées |
|------------------|----------------|
| 1er enfant | +0,5 |
| 2ème enfant | +0,5 |
| 3ème enfant et suivants | +1 chacun |

**Cas particuliers** :
- Enfant en résidence alternée : moitié de la majoration de son rang, les enfants à charge exclusive ou principale étant comptés en premier (art. 194 I CGI) : 0,25 / 0,25 / 0,5 sans enfant à charge exclusive ; 0,25 puis 0,5 avec un enfant à charge exclusive ; 0,5 par enfant avec au moins deux enfants à charge exclusive. Exemple : couple avec 2 enfants à charge exclusive et 1 en résidence alternée = 3,5 parts (brochure pratique IR 2026, tableaux 2 et 3)
- Enfant ou personne à charge invalide (carte d'invalidité ou CMI-invalidité) : +0,5 part supplémentaire
- Déclarant ou conjoint invalide (cases P, F), ancien combattant de plus de 74 ans titulaire de la carte du combattant (cases W, S), veuve de guerre (case G) : +0,5 part (+1 part pour un couple dont chacun est invalide). Si le plafonnement joue, réduction d'impôt complémentaire de 1 801 € au plus par demi-part (revenus 2025)
- Parent isolé (case T, célibataire, divorcé ou séparé vivant seul au 1er janvier, hors concubinage, assumant à titre exclusif ou principal la charge d'au moins un enfant) : +0,5 part, soit 1 part entière pour le premier enfant. Enfants uniquement en résidence alternée : +0,25 part pour un enfant, +0,5 part à partir de deux. Le veuf avec enfants n'est pas concerné : il a déjà le nombre de parts d'un couple (art. 194, I CGI)

### Exemples

| Foyer | Parts |
|-------|-------|
| Célibataire sans enfant | 1 |
| Célibataire, 1 enfant | 1,5 (ou 2 si parent isolé) |
| Marié, 0 enfant | 2 |
| Marié, 2 enfants | 3 (2 + 0,5 + 0,5) |
| Marié, 3 enfants | 4 (2 + 0,5 + 0,5 + 1) |
| Marié, 1 enfant + 1 en résidence alternée | 2,75 (2 + 0,5 + 0,25) |

## Plafonnement du gain QF

**Mécanisme critique souvent oublié.** Le gain d'impôt lié aux demi-parts supplémentaires (enfants, mais aussi invalidité, ancien combattant, case L, rattachement) est plafonné.

### Algorithme de vérification

```
impôt_avec_parts_pleines = calcul normal avec toutes les parts
impôt_sans_enfants       = calcul avec la part de référence : 1 part (célibataire, divorcé, séparé, veuf, même avec enfants) ou 2 parts (couple soumis à imposition commune, veuf l'année du décès)
gain_réel = impôt_sans_enfants − impôt_avec_parts_pleines

plafond_par_demi_part = 1 807 €  (revenus 2025, voir data/bareme-ir-2025.json)
nb_demi_parts_supp = (nb_parts − parts_de_base) × 2
gain_max = plafond_par_demi_part × nb_demi_parts_supp
# case T : les 2 premières demi-parts au-delà d'1 part valent 4 262 € au total (au lieu de 2 × 1 807 €)
# case L : la demi-part vaut 1 079 € (au lieu de 1 807 €)

impôt_final = impôt_sans_enfants − min(gain_réel, gain_max)
# si gain_réel > gain_max : retrancher en plus les réductions complémentaires
# (1 801 € par demi-part invalidité, ancien combattant ou veuve de guerre ; 2 011 € pour la part
# supplémentaire du veuf avec enfants), dans la limite de gain_réel − gain_max
```

### Conséquence pratique

Au-delà d'un certain seuil de revenu, **l'avantage fiscal stagne** même si le revenu augmente. Les enfants cessent de réduire l'impôt proportionnellement.

**Exemple (marié, 2 enfants, 2025)** :
- Parts pleines : 3 parts
- Demi-parts supplémentaires : (3 − 2) × 2 = 2 demi-parts
- Gain maximum : 2 × 1 807 € = **3 614 €**

Le plafond devient actif à partir de 71 466 € de revenu net imposable (brochure pratique IR 2026, tableau 4) : au-delà, le gain QF stagne à 3 614 €.

### Pièges fréquents

1. **Oublier le plafonnement** : calculer l'IR avec 3 parts sans comparer au calcul à 2 parts + plafond.
2. **Appliquer le plafonnement sur 1 part** : non, il s'applique sur les demi-parts **supplémentaires** à la situation de base.
3. **Parent isolé (case T)** : les deux premières demi-parts au-delà de 1 part (part entière du premier enfant) sont plafonnées ensemble à 4 262 € (revenus 2025), au lieu de 2 × 1 807 € = 3 614 €, puis 1 807 € par demi-part suivante. **Veuf avec enfants** : référence 1 part, plafond normal de 1 807 € par demi-part, puis réduction complémentaire de 2 011 € au plus.

## Décote

Mécanisme distinct du QF, appliqué **après** le plafonnement.

### Formules (revenus 2025)

Voir `data/bareme-ir-2025.json` → champ `decote`.

- **Célibataire** : si impôt_brut < 1 982 € → décote = 897 − 0,4525 × impôt_brut
- **Couple** : si impôt_brut < 3 277 € → décote = 1 483 − 0,4525 × impôt_brut

### Ordre d'application

```
Impôt brut (après barème)
  ↓ plafonnement QF, puis réductions complémentaires si plafonné (1 801 €, 2 011 €), puis abattement DOM le cas échéant (30 % ou 40 %, art. 197, I-3 CGI)
Impôt après QF
  ↓ décote (si applicable)
Impôt après décote
  ↓ réductions puis crédits
Impôt net
```

### Particularité : taux marginal effectif élevé

Dans la zone de décote, chaque euro supplémentaire de revenu :
- Augmente l'impôt au taux du barème
- Diminue la décote de 0,4525 × ce supplément

Taux marginal effectif ≈ (taux_barème × 1,4525). Un foyer à la tranche 11% peut subir un taux marginal effectif proche de 16% dans la zone de décote.

## Personnes rattachées (enfants majeurs)

C'est l'**enfant** qui demande son rattachement (art. 6-3° CGI) : le parent ne fait qu'accepter
en le déclarant. La décision appartient donc à l'enfant, qui doit arbitrer entre rattachement
et autonomie fiscale (RFR propre, accès aux aides). Les deux parties doivent se coordonner
chaque année.

### Régime selon la situation de l'enfant

Deux régimes distincts selon la situation de l'enfant rattaché :

| Situation de l'enfant rattaché | Case 2042 | Effet fiscal |
|-------------------------------|-----------|--------------|
| Célibataire, sans enfant à charge | **J** | Mêmes majorations qu'un enfant mineur : +0,5 part pour chacun des deux premiers enfants à charge, +1 part à partir du troisième (BOI-IR-LIQ-10-10-10-20, § 160) |
| Marié, pacsé, ou avec enfant à charge | **N** | Abattement **6 855 €** sur le RNI par personne rattachée (art. 196 B CGI), pas de demi-part |

**Plafonnement (case J)** : le même plafond par demi-part s'applique.
Voir `data/bareme-ir-2025.json` → `quotient_familial.plafond_gain_par_demi_part`.

**Abattement (case N)** : 6 855 € par personne rattachée (conjoint + enfants éventuels).
Voir `data/bareme-ir-2025.json` → `rattachement_majeur_marie.abattement_par_personne`.

### Conditions

- Enfant célibataire de **moins de 21 ans**, ou de **moins de 25 ans** s'il poursuit des études
- Enfant **infirme** : rattachable **sans condition d'âge** (art. 196 CGI)
- Rattachement **annuel** (option à renouveler chaque année, normalement irrévocable pour l'année concernée : BOI-IR-LIQ-10-10-10-20, § 140) : à recalculer chaque année selon la situation du foyer

**Contrepartie** : les revenus de l'enfant sont en principe intégrés dans le RNI du foyer,
sous réserve des exonérations applicables aux apprentis et jobs étudiants
(voir `references/ir-mecanisme.md` → section "Revenus partiellement exonérés").

**À chiffrer au cas par cas** : si les revenus de l'enfant dépassent les seuils d'exonération,
l'impôt supplémentaire peut annuler le gain QF lié au rattachement.

### Alternative : pension alimentaire (art. 156-II-2° CGI)

L'enfant majeur peut **ne pas être rattaché** : le parent déduit alors une pension alimentaire
de son revenu imposable.

**Accès aux aides sous conditions de ressources** : pour certaines aides basées sur le RFR
propre de l'enfant (tarifs réduits transports, aides à l'achat d'un véhicule, certaines aides
locales…), le non-rattachement peut être une condition nécessaire : en cas de rattachement,
l'enfant n'a pas de RFR propre utilisable. Pour les bourses sur critères sociaux (CROUS),
le revenu des parents est pris en compte sauf exceptions (émancipation, rupture familiale
déclarée…). En revanche, l'APL et l'accès aux logements sociaux ne dépendent pas du
rattachement fiscal : le revenu des parents n'y est pas pris en compte.

Plafonds de déduction (revenus 2025), voir `data/bareme-ir-2025.json` → `pension_alimentaire` :

| Situation de l'enfant | Plafond |
|-----------------------|---------|
| Célibataire, non domicilié chez le parent | **6 855 €** |
| Marié/pacsé ou chargé de famille, si vous assurez seul son entretien (6 855 € si les beaux-parents participent aussi) | **13 710 €** |
| Domicilié chez le parent, sans ressources (forfait) | **4 075 €** (célibataire) / **8 150 €** (marié/pacsé) |

La pension peut être versée **en espèces ou en nature** (loyer, frais d'inscription, frais médicaux
payés directement à l'établissement) : les deux entrent dans le même plafond, sur justificatifs.

**Preuve requise** : relevés bancaires pour les versements en numéraire (virement, chèque) ;
factures ou reçus de l'établissement pour les paiements directs à des tiers (loyer, école…).
Les versements en espèces (cash) sont à proscrire, quasi-impossibles à justifier.
L'administration peut également demander à justifier le besoin de l'enfant.

**Impact fiscal pour l'enfant** : la pension est imposable chez l'enfant à hauteur du montant
déduit par le parent (art. 79 CGI), y compris les paiements en nature. Si l'enfant est apprenti,
son salaire peut être exonéré (voir `references/ir-mecanisme.md` → "Revenus partiellement
exonérés"), mais la pension reçue s'ajoute au-dessus et est imposable en totalité :
l'exonération ne couvre pas la pension.

**Arbitrage à faire chaque année** :
- **Rattachement (case J)** : gain parent ≤ `plafond_gain_par_demi_part` × demi-parts ajoutées
  (voir `data/bareme-ir-2025.json` → `quotient_familial`) : c'est un maximum, le gain réel
  dépend du revenu du parent
- **Pension alimentaire** : gain net = (pension × TMI parent) − (pension × TMI enfant)
- Si l'enfant n'était pas imposable, la pension peut le faire basculer dans l'imposition
- La pension augmente le RFR de l'enfant (peut réduire l'accès aux aides ci-dessus)

**Break-even** (enfant non imposable) : si le plafonnement QF est actif (ce qui est probable
dès lors qu'on envisage cet arbitrage), le gain rattachement est fixe à 1 807 € pour un enfant de rang 1 ou 2 (3 614 € s'il est le troisième enfant à charge ou plus, une part entière ; 4 262 € s'il ouvre la case T d'un parent isolé).
Le break-even vaut alors **1 807 € ÷ TMI**, soit environ :
- TMI 30 % → 1 807 ÷ 0,30 → ~6 000 €
- TMI 41 % → 1 807 ÷ 0,41 → ~4 400 €
- TMI 11 % → rattachement gagne toujours (break-even théorique > plafond de déduction)

**Attention franchissement de tranche** : si la déduction de pension fait descendre le RNI
sous la frontière de tranche (29 579 € × nombre de parts), une partie ne vaut que 11 % au lieu
de 30 %. Le gain réel de la pension est alors inférieur à pension × 30 %, ce qui remonte le
break-even effectif. À chiffrer tranche par tranche : le rattachement reste compétitif
bien au-delà du break-even apparent.

Pour un foyer en **TMI 11 %**, le rattachement gagne presque toujours (break-even > 16 000 €,
hors plafond de déduction).

**Exclusif** : impossible de cumuler rattachement et déduction de pension alimentaire pour
le même enfant.

**Articulation avec les donations** : la pension alimentaire peut constituer un vecteur de
transfert patrimonial fiscalement efficace, là où une donation classique n'est pas déductible.
Sur 10 ans à TMI 30%, le parent transfère 6 855 € × 10 = 68 550 € avec une économie fiscale
d'environ 20 565 €. La donation classique (abattement 100 000 € par parent, renouvelable
tous les 15 ans) reste complémentaire mais sans avantage IR pour le parent.

**Condition impérative** : la pension doit être justifiée par l'état de besoin de l'enfant
(art. 208 Code civil). Si l'enfant dispose de revenus ou d'un patrimoine suffisants,
l'administration peut requalifier les versements et redresser (abus de droit). La stratégie
est légitime tant que le besoin est réel et démontrable : étudiant, apprenti, début de
carrière avec revenus modestes.

## Parent isolé (case T)

Majoration de 0,5 part pour les contribuables vivant seuls et élevant des enfants.

**Conditions** :
- Célibataire, divorcé ou séparé au 1er janvier
- Assume la charge exclusive ou principale d'au moins un enfant
- N'est pas en concubinage

**Plafonnement spécifique** : l'avantage procuré par la part entière accordée au titre du premier enfant (les deux premières demi-parts au-delà d'1 part) est limité à **4 262 €** (revenus 2025), puis 1 807 € par demi-part suivante. Enfants tous en résidence alternée : 2 131 € pour la demi-part de chacun des deux premiers enfants. Le plafonnement joue dès 45 298 € de revenu net imposable pour un parent isolé avec un enfant (2 parts). Sources : art. 197, I-2 CGI ; BOI-IR-LIQ-20-20-20, § 70 ; brochure pratique IR 2026, p. 370.

## Ancien parent isolé (case L)

Majoration de 0,5 part (art. 195, 1-a, b et e CGI) pour la personne célibataire, divorcée, séparée ou veuve qui vit seule au 1er janvier, sans personne à charge, et qui a assumé seule la charge exclusive ou principale d'un enfant (majeur ou imposé séparément, ou décédé après 16 ans ou par suite de faits de guerre) pendant au moins 5 années au cours desquelles elle vivait seule.

**Plafonnement spécifique** : l'avantage de cette demi-part est limité à **1 079 €** (revenus 2025), au lieu de 1 807 €. Le plafonnement joue dès 31 906 € de revenu net imposable (1,5 part). Sources : art. 197, I-2 CGI ; BOI-IR-LIQ-20-20-20, § 100 ; brochure pratique IR 2026, p. 370.

## Références CGI / BOFiP

- Parts : art. 194 à 195 CGI
- Plafonnement QF : art. 197, I-2 CGI
- Décote : art. 197, I-4-a CGI
- Parent isolé : art. 194-II CGI
- Rattachement enfant infirme : art. 196 CGI
- Rattachement majeur marié/pacsé : art. 196 B CGI
- Pension alimentaire enfant majeur : art. 156-II-2° CGI
- BOFiP : BOI-IR-LIQ-10-20-20 (majorations de parts), BOI-IR-LIQ-20-20-20 (plafonnement, 07/04/2026) et BOI-IR-LIQ-20-20-30 (décote, 07/04/2026)
- BOFiP pension alimentaire : BOI-IR-BASE-20-30-20-20
