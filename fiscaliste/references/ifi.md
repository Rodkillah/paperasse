# IFI (Impôt sur la Fortune Immobilière)

Voir `data/ifi-bareme.json` pour les tranches et paramètres.

**IFI 2026 (patrimoine au 1er janvier 2026)** : seuil, barème, décote, abattement RP et plafonnement inchangés par la loi de finances pour 2026 (loi n° 2026-103 du 19 février 2026). Seule modification : nouvel art. 975 VII CGI, qui exonère la fraction des parts ou actions de sociétés représentative d'immeubles (art. 965, 2°) lorsque ces actifs ont été soumis à la taxe sur les holdings patrimoniales (art. 235 ter C) au titre de l'exercice clos l'année précédente. Cette taxe n'étant due qu'au titre des exercices clos à compter du 31 décembre 2026, l'exonération ne joue pas avant l'IFI 2027.

## Principe

Impôt annuel sur le patrimoine **immobilier net** du foyer fiscal au **1er janvier**.

**Condition d'assujettissement** : patrimoine immobilier net > 1 300 000 €.

**Particularité** : une fois le seuil franchi, le barème s'applique à partir de **800 000 €** (pas à partir de 1 300 000 €). Mécanisme de décote entre 1 300 000 € et 1 400 000 € pour lisser l'entrée.

## Assiette taxable

### Actif immobilier (à inclure)

- Biens immobiliers détenus directement (résidences, locatifs, terrains)
- Parts de sociétés civiles (SCI, SCPI) à hauteur de la fraction immobilière
- Parts de SCPI en direct ou via assurance-vie (fraction immobilière)
- Immeubles affectés à l'activité professionnelle **du foyer** s'ils ne constituent pas l'outil de travail
- Droits démembrés (usufruit ou pleine propriété, selon le cas)

### Exonérations principales

| Bien | Régime |
|------|--------|
| Résidence principale | **Abattement 30%** sur la valeur vénale |
| Biens professionnels | Exonération totale si outil de travail (conditions strictes) |
| Bois, forêts, parts de groupements forestiers | Exonération des 3/4 (25 % imposable) sous engagement de gestion durable de 30 ans (art. 976 I et II CGI) |
| LMP | Exonéré comme bien professionnel si recettes annuelles > 23 000 €, si les revenus de cette location représentent plus de 50 % des revenus professionnels du foyer IFI (traitements et salaires, BIC, BA, BNC, art. 62) et si elle constitue l'activité principale (art. 975 I et V CGI) |
| Biens ruraux loués par bail à long terme (18 ans au moins) ou bail cessible, parts de GFA et GAF | Exonération des 3/4 jusqu'à 101 897 € de valeur totale, de 1/2 au-delà (limite appréciée séparément pour les biens ruraux et pour les parts) ; totale si le bail est consenti à un proche qui y exerce sa profession principale (art. 976 III et IV CGI) |

**Conditions "biens professionnels"** pour des titres de société à l'IS (article 975 III CGI ; l'article 885 O bis visait l'ISF, abrogé depuis 2018) :
- Fonction de direction effective
- Rémunération normale ayant procuré au redevable plus de 50 % de ses revenus professionnels soumis à l'IR (traitements et salaires, BIC, BA, BNC, revenus de l'article 62)
- Détention d'au moins 25 % des droits de vote, groupe familial et un niveau de société interposée compris (non exigée des gérants et associés visés à l'article 62 CGI) ; à défaut, exonération possible si les titres détenus directement représentent plus de 50 % de la valeur brute du patrimoine total

## Passif déductible

### Dettes déductibles

- Emprunts immobiliers (capital restant dû au 1er janvier)
- Dettes liées à travaux sur immeubles taxables
- Impôts afférents à l'immobilier : taxe foncière (hors taxe d'enlèvement des ordures ménagères), IFI théorique dû au 1er janvier de l'année d'imposition (ligne 9GH de la 2042-IFI, calcul selon BOI-PAT-IFI-20-40-10 § 80), droits de mutation à titre gratuit afférents à des actifs imposables. L'IR et les prélèvements sociaux sur les revenus des biens ne sont pas déductibles.

### Dettes NON déductibles

- Dettes personnelles non liées à l'immobilier
- Emprunts in fine contractés pour l'achat d'un actif imposable (dette à imputation spéciale) : fraction non déductible = capital emprunté x années écoulées depuis le versement / durée totale du prêt ; prêt sans terme : 1/20 du capital par année écoulée (art. 974 II CGI)
- Prêts consentis par un membre du foyer fiscal IFI (jamais déductibles), ou par un ascendant, un descendant hors foyer, un frère ou une sœur (y compris du conjoint, partenaire de Pacs ou concubin) ou une société contrôlée par le foyer ou sa famille : non déductibles sauf preuve du caractère normal des conditions du prêt (terme, montant, remboursements effectifs). Article 974 III CGI (l'article 885 T bis visait l'ISF)

### Plafonnement du passif

Si la valeur vénale du patrimoine immobilier taxable dépasse 5 M€ et que les dettes déductibles excèdent 60 % de cette valeur, la fraction des dettes au-delà de 60 % n'est déductible qu'à hauteur de 50 % (art. 974 IV CGI), sauf pour les dettes dont le redevable justifie qu'elles n'ont pas été contractées dans un objectif principalement fiscal.

## Calcul du barème

Voir `data/ifi-bareme.json` → `tranches`.

| Tranche patrimoine net | Taux |
|------------------------|------|
| 0 à 800 000 € | 0% |
| 800 000 à 1 300 000 € | 0,5% |
| 1 300 000 à 2 570 000 € | 0,7% |
| 2 570 000 à 5 000 000 € | 1,0% |
| 5 000 000 à 10 000 000 € | 1,25% |
| > 10 000 000 € | 1,5% |

### Décote d'entrée

Entre 1 300 000 € et 1 400 000 € : formule `17 500 − 1,25% × valeur_patrimoine_net`.

Évite un effet de seuil brutal à 1 300 000 €.

## Plafonnement de l'IFI en fonction des revenus (art. 979 CGI)

**Règle des 75 %** (redevables ayant leur domicile fiscal en France) : si le total de l'IFI et des impôts dus en France et à l'étranger au titre des revenus et produits de l'année N-1 (notamment IR, CEHR, prélèvements sociaux, prélèvements libératoires) dépasse 75 % des revenus mondiaux nets de frais professionnels de N-1, l'IFI est réduit de l'excédent. Les revenus retenus incluent les revenus exonérés d'IR et les produits soumis à prélèvement libératoire, déterminés sans tenir compte des exonérations, seuils, réductions et abattements. Déclaration : annexe 5, lignes 9PR et 9PX de la 2042-IFI (ne pas ajouter l'IFI de l'année en ligne 9PR).

L'excédent réduit uniquement l'IFI : il n'est ni imputable sur d'autres impôts ni restituable.

**Attention** : les revenus exonérés d'IR et les produits soumis à prélèvement libératoire comptent dans les revenus retenus, sans application des exonérations et abattements. Clause anti-abus (art. 979 II CGI, BOI-PAT-IFI-40-30-20) : les revenus distribués à une société passible de l'IS contrôlée par le foyer sont réintégrés, pour la part correspondant à une diminution artificielle des revenus, lorsque l'existence de la société et le choix d'y recourir ont pour objet principal d'éluder tout ou partie de l'IFI.

## Évaluation des biens

### Résidence principale

Valeur vénale au 1er janvier, **moins abattement 30%**.

### Biens locatifs

Valeur vénale : possible décote pour location en cours, à justifier au cas par cas par des comparaisons de marché. Aucun taux n'est fixé par le CGI ni par le BOFiP : les 10 à 20 % souvent cités ne sont qu'un ordre de grandeur de pratique, jamais une règle à appliquer.

### Parts de SCI / SCPI

Valeur des parts × fraction immobilière. Possible décote pour illiquidité.

### Biens démembrés

- **Usufruit** : l'usufruitier déclare le bien pour sa valeur en **pleine propriété** (art. 968 CGI), y compris en cas de donation avec réserve d'usufruit
- **Nue-propriété** : rien à déclarer en principe, et les dettes afférentes au bien ne sont pas déductibles pour le nu-propriétaire

**Exceptions limitatives (art. 968 CGI)** : imposition répartie entre usufruitier et nu-propriétaire selon le barème de l'art. 669 CGI dans trois cas seulement : usufruit légal du conjoint survivant (issu de la loi civile, pas d'un testament ni d'une donation au dernier vivant) ; vente de la nue-propriété à un tiers autre qu'un héritier présomptif, un donataire ou une personne interposée ; don de la nue-propriété à l'État, une collectivité, un établissement public ou une association ou fondation reconnue d'utilité publique.

## Déclaration

- Déclaration 2042-IFI jointe à la 2042
- Annexes 1 à 6 intégrées à la 2042-IFI (biens professionnels, biens détenus directement, biens détenus indirectement, passif, plafonnement, impôts payés à l'étranger), sans justificatif à joindre ; 2042-IFI-COV si aucune déclaration de revenus n'est déposée ; cocher la case ØIF de la 2042
- Date limite : même que la déclaration IR

### Documents à préparer

- Évaluation de chaque bien (expertise, estimation, comparables DVF)
- Relevés bancaires emprunts au 1er janvier
- Attestations SCPI / SCI
- Tableau d'amortissement des emprunts in fine

## Pièges fréquents

1. **Oublier l'abattement 30 % RP** : perte directe
2. **Inclure un LMP en patrimoine taxable** alors qu'il peut être exonéré comme bien professionnel
3. **Emprunt in fine déduit pour son capital total** au lieu de la déduction dégressive : redressement probable
4. **Évaluer la RP au prix d'achat** au lieu de la valeur vénale actuelle : source de sous-déclaration
5. **Omettre les SCPI en assurance-vie** : la fraction immobilière des unités de compte est imposable
6. **Oublier le plafonnement 75 %** : l'IFI peut être réduit si les revenus sont faibles par rapport au patrimoine (redevables domiciliés en France)

## Sanctions

- Défaut ou retard de déclaration : intérêt de retard de 0,20 %/mois (art. 1727 CGI) + majoration de 10 % (art. 1728 CGI), portée à 40 % si la déclaration n'est pas déposée dans les 30 jours d'une mise en demeure
- Insuffisance ou sous-évaluation de bonne foi : rappel d'impôt et intérêt de retard seul, sans majoration
- Manquement délibéré : majoration 40%
- Manœuvres frauduleuses ou abus de droit : majoration 80 % (art. 1729 CGI)

**Délai de reprise** : 3 ans (jusqu'au 31 décembre de la 3e année suivant la déclaration, LPF art. L. 180) lorsque l'exigibilité de l'impôt est suffisamment révélée par la déclaration et ses annexes ; 6 ans (LPF art. L. 186) en cas de défaut de déclaration ou si d'autres recherches sont nécessaires (BOI-PAT-IFI-60-10).

## Références CGI / BOFiP

- Champ IFI : art. 964 à 983 CGI
- Résidence principale : art. 973-I CGI
- Biens professionnels : art. 975 CGI
- Passif déductible : art. 974 CGI
- Plafonnement : art. 979 CGI
- Barème : art. 977 CGI
- BOFiP : BOI-PAT-IFI
