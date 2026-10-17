# PER (Plan d'Épargne Retraite) individuel

Voir `data/per-plafonds.json` pour les plafonds et paramètres.

## Mécanisme de déduction

Le versement PER **réduit le RNI** de l'année de versement.

```
RNI avant PER
  − versement PER (dans la limite du plafond)
= RNI après PER
  ÷ nombre de parts
= Quotient → barème → impôt brut réduit
```

**Économie d'impôt immédiate** = versement × TMI.

Exemple : versement 5 000 €, TMI 30% → économie IR = 1 500 €.

## Plafond de déduction

### Formule

**Plafond = 10 % des revenus d'activité professionnelle** de l'année N-1, nets de frais professionnels (salaires après abattement de 10 % ou frais réels, allocations chômage, gains d'acquisition d'actions gratuites, BIC, BNC, BA d'une activité exercée à titre professionnel ; pas les BIC de location meublée non professionnelle, ni les revenus fonciers ou du capital), ces revenus étant retenus dans la limite de 8 PASS N-1 ; ou 10 % du PASS N-1 si ce montant est plus élevé. Ce plafond est ensuite **diminué des cotisations d'entreprise versées en N-1** : article 83 et PERO (parts déductibles), abondement PERCO/PERECO/PERO dans la limite exonérée, fraction Madelin déduite du résultat, jours de congé affectés (10 jours au plus).

### Bornes (versements 2025, déclaration 2026 ; PASS de l'année précédant le versement)

| Borne | Valeur | Base |
|-------|--------|------|
| Plancher | 4 637 € (versements 2026 : 4 710 €) | 10 % × PASS 2024 = 46 368 € (versements 2026 : 10 % × PASS 2025) |
| Plafond absolu | 37 680 € | 10% × 8 × PASS 2025 |

**Plancher** : même sans revenus professionnels, le plafond vaut au minimum 10 % du PASS N-1 (4 637 € pour les versements 2025, 4 710 € pour les versements 2026), mais il est ensuite diminué des cotisations d'entreprise N-1 (article 83, abondement PERCO/PERECO/PERO, Madelin) : exemple officiel, 4 637 € moins 3 000 € d'article 83 = 1 637 €. Depuis 2026, il ne joue plus pour les versements faits à partir de 70 ans.

### Report des plafonds non utilisés

Les plafonds non utilisés des **3 années précédentes** sont mobilisables. Ordre : plafond de l'année en cours d'abord, puis plafonds N-3, N-2, N-1 (ordre FIFO : le plus ancien en premier).

**Exemple** :
- Plafond N : 5 000 €, utilisé 3 000 € → reste 2 000 € reportables sur N+1 à N+3
- Au-delà de N+3, le plafond non utilisé est **perdu**

### Mutualisation couple

Les époux/pacsés soumis à imposition commune peuvent **mutualiser leurs plafonds** en cochant la **case 6QR** de la 2042. Plafonds et cotisations des deux membres sont additionnés en un plafond unique du foyer, imputé d'abord sur le plafond de l'année puis sur les soldes non utilisés des années antérieures. Un conjoint sans revenu pro peut ainsi bénéficier du plafond inemployé de l'autre. Hors mutualisation, le report des soldes reste individuel.

### Versements à partir de 70 ans (LFI 2026)

Depuis le 1er janvier 2026 (loi n° 2026-103, art. 9 ; CGI art. 163 quinvicies), les versements faits par le titulaire à compter du jour de son 70e anniversaire ne sont plus déductibles (versements volontaires et obligatoires ; l'exonération des versements d'épargne salariale tombe aussi). À la sortie, la part de capital correspondant à ces versements est exonérée d'IR, comme un versement non déduit. La mutualisation des plafonds devient sans objet au titre de l'année suivant celle où l'un des membres du couple atteint 70 ans (BOI-IR-BASE-20-50-30).

## Arbitrage : le PER est-il vraiment utile ?

**Le PER est un REPORT d'imposition, pas une exonération.**

À la sortie, les versements sont imposés comme revenu (barème). Les gains sont imposés au PFU.

### Gagnant / perdant

| Situation | Résultat |
|-----------|----------|
| TMI entrée > TMI sortie | **Gain net** : économie à l'entrée > imposition sortie |
| TMI entrée = TMI sortie | **Neutre fiscalement** : seul l'effet capitalisation sur l'économie initiale joue |
| TMI entrée < TMI sortie | **Perte nette** : rare mais possible (carrière ascendante, sortie capital massif) |

### Cas typiques favorables

- **Actif TMI 30-41% avec retraite estimée TMI 11-30%** : gain net substantiel
- **Année de revenus exceptionnels** : versement pour écraser l'IR de l'année, sortie étalée plus tard
- **Quotient pour revenus exceptionnels + PER** : combinaison puissante pour un vesting RSU important

### Cas défavorables ou neutres

- **TMI 11% stable** : intérêt marginal, seul l'effet capitalisation compte
- **TMI 45% stable (hauts revenus à la retraite)** : pas d'avantage, imposition identique entrée/sortie
- **Horizon court (< 10 ans avant retraite)** : peu d'effet de capitalisation

## Sortie du PER

### Sortie à la retraite

**Deux options au choix** :

1. **Sortie en rente viagère**
   - Imposition comme pension (barème + abattement 10% plafonné)
   - Prélèvements sociaux sur une fraction seulement de la rente (selon l'âge au premier versement : 70 % avant 50 ans, 50 % de 50 à 59 ans, 40 % de 60 à 69 ans, 30 % après 69 ans), au taux de 17,2 % pour les rentes versées en 2025 et de 18,6 % pour celles versées à partir du 1er janvier 2026
   - Protection en cas de longévité

2. **Sortie en capital**
   - **Versements déduits à l'entrée** : imposés au barème comme une pension, sans abattement de 10 % et sans prélèvements sociaux (part capital) ; revenu exceptionnel éligible au quotient quel que soit son montant (BOI-RSA-PENS-30-10-20)
   - **Gains** : imposés séparément au PFU (12,8 % IR + PS), les gains PER étant qualifiés de "produits de placement" (L. 136-7 CSS) :
     - **Sortie avant le 01/01/2026** : PFU 30 % (PS 17,2 %) si l'établissement a prélevé les PS lors de la sortie (à vérifier sur l'IFU 2025) ; à défaut, PS 18,6 % sur l'avis 2026 (brochure IR 2026, ligne 2TZ)
     - **Sortie à partir du 01/01/2026** : PFU 31,4 % (PS 18,6 %, LFSS 2026)
   - Possibilité de fractionner la sortie sur plusieurs années (à demander à l'assureur)

**Piège sortie capital** : ne pas confondre le régime du capital (barème, écrase la tranche) et celui des gains (PFU fixe). Bien distinguer.

### Versements non déduits (cas rare)

Si l'on a choisi de ne pas déduire les versements (option exercée lors de chaque versement auprès du gestionnaire, et non une fois pour toutes à la souscription) :
- Sortie partiellement exonérée
- Seuls les gains sont imposés au PFU (30 % avant 01/01/2026, 31,4 % à partir du 01/01/2026, voir taux PS PER ci-dessus)
- Utile si on anticipe un TMI sortie > TMI entrée, rare

### Sortie anticipée autorisée

Cas de déblocage avant la retraite (fiscalité selon le cas : accidents de la vie, part versements exonérée d'IR et de PS et gains soumis aux seuls PS ; achat de la résidence principale, part versements déduits imposée au barème sans abattement de 10 % et gains au PFU) :
- Achat de la résidence principale
- Décès du conjoint / partenaire PACS
- Invalidité
- Surendettement
- Fin des droits au chômage
- Cessation d'activité non salariée après jugement de liquidation

Hors ces cas : déblocage impossible (capital bloqué jusqu'à la retraite).

## Priorité absolue : abondement employeur avant PER individuel

**Avant tout versement PER individuel, vérifier que l'abondement PEE / PERCO de l'employeur est saturé.**

L'abondement est un complément versé par l'entreprise pour chaque euro versé par le salarié sur son PEE ou son PERCO, typiquement 50 à 300 % du versement salarié, dans une limite annuelle (8 % du PASS pour le PEE, 16 % du PASS pour le PERCO).

| Dispositif | Avantage |
|------------|----------|
| **PEE + abondement** | Prime gratuite de l'employeur + exonération IR sur l'abondement + PFU 17,2 % à la sortie (pas 30 %) |
| **PERCO + abondement** | Idem + blocage jusqu'à la retraite |
| **PER individuel** | Uniquement économie d'impôt immédiate × TMI, pas de match employeur |

**Règle** : un abondement employeur de 100 % représente un rendement immédiat de 100 %. Aucune défiscalisation PER n'égale ce rendement. Toujours saturer PEE/PERCO en premier si l'option existe.

## Mécanique pratique

### Déclaration

- Versements PER déductibles du revenu global : cases 6NS (déclarant 1), 6NT (déclarant 2), 6NU (personne à charge) ; PERP, Préfon et assimilés : 6RS, 6RT, 6RU ; mutualisation : case 6QR ; plafond imprimé erroné : 6PS, 6PT, 6PU ; nouvel arrivant en France : case 6QW
- Plafond calculé automatiquement par la DGFIP (figure sur l'avis d'imposition N-1, rubrique "Plafond pour l'épargne retraite")

## Différence PER individuel vs PERCO / PERO

- **PER individuel** (présent doc) : versements volontaires, déductibles dans la limite du plafond, sortie imposée au barème.
- **PERCO / PEE** (plans d'épargne entreprise) : alimenté par intéressement, participation, abondement employeur. Voir la section Equity salarial listée depuis SKILL.md pour le détail.

**Règle d'or** : toujours saturer l'abondement employeur (PEE + PERCO) AVANT d'abonder un PER individuel. L'abondement est de l'argent gratuit : aucun rendement PER individuel n'égale un match à 50-300%.

## Pièges fréquents

1. **Oublier le plafond** : versement > plafond disponible (plafond de l'année + soldes reportables) : l'excédent n'est ni déductible ni reportable sur une année suivante (brochure IR 2026, exemple p. 233), il reste bloqué dans le PER et, faute d'option pour la non-déduction exercée lors du versement, la part de capital correspondante sera quand même imposée au barème à la sortie (BOI-RSA-PENS-30-10-20 § 110). Pour la fraction qui dépasse le plafond, exercer l'option pour la non-déduction au moment du versement.
2. **Sortie en capital sur un TMI 45%** : imposition quasi équivalente à un revenu normal, intérêt limité
3. **Mutualisation couple oubliée** : un conjoint sans revenu laisse 4 637 € de plafond inemployé sur les versements 2025 (4 710 € sur les versements 2026), faute d'avoir coché la case 6QR
4. **Assurer le plafond N-1 sur l'avis** : ne pas se fier aux calculs manuels, utiliser le plafond officiel DGFIP
5. **PER individuel avant PEE/PERCO** : manque l'abondement employeur

## Références CGI / BOFiP

- PER individuel : art. 163 quatervicies CGI
- Plafond de déduction : art. 163 quatervicies-I-2 CGI
- Sortie en capital : art. 158, 5, b quinquies CGI (1° part versements, 2° part produits) ; BOI-RSA-PENS-30-10-20
- Mutualisation couple : art. 163 quatervicies-I-2° CGI
- BOFiP : BOI-IR-BASE-20-50-20
