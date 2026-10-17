# Cas particuliers

## Non-résidents fiscaux

### Définition résidence fiscale

Un contribuable est résident fiscal français si l'un de ces critères est rempli (article 4 B CGI) :
- Foyer ou lieu de séjour principal en France
- Exercice d'une activité professionnelle principale en France
- Centre des intérêts économiques en France

**La nationalité n'est pas un critère.**

### Règles applicables aux non-résidents

- Imposés uniquement sur les **revenus de source française** (article 164 A CGI)
- Taux minimum (art. 197 A CGI) : 20 % sur la fraction ≤ 29 579 € et 30 % au-delà (revenus 2025 ; 14,4 % et 20 % pour les revenus de source DOM), sauf option pour le taux moyen si plus favorable
- Pas de quotient familial au-delà de 2 parts
- Pas de décote
- Application des conventions fiscales bilatérales (crédit d'impôt, exonérations)

**Ce skill ne couvre PAS la fiscalité des non-résidents en détail.** Pour les cas complexes, orienter vers un avocat fiscaliste spécialisé en fiscalité internationale.

## Revenus exceptionnels : quotient

### Mécanisme

Lissage fiscal pour éviter qu'un revenu ponctuel ne fasse franchir artificiellement plusieurs tranches.

**Formule** :
```
Impôt_supplémentaire = [IR(revenu_ordinaire + revenu_exceptionnel / coefficient) − IR(revenu_ordinaire)] × coefficient
```

**Coefficient par défaut : 4**. Peut être différent selon la nature du revenu.

### Revenus éligibles

- Prime exceptionnelle (non pérennisable)
- Indemnité de départ volontaire ou licenciement (fraction imposable)
- Gratification de fin d'activité
- Vesting RSU massif (exceptionnellement élevé vs revenus habituels ; éligibilité non établie pour le gain d'un plan qualifiant, art. 200 A, 3)
- Régularisation d'arriérés de salaire
- Plus-value de cession d'entreprise (cas spécifiques)

### Conditions d'application

- Revenu > **moyenne des revenus imposables des 3 années précédentes**
- Caractère exceptionnel avéré (non récurrent)
- Demande expresse du contribuable sur la déclaration

### Nuance critique

**Inutile si foyer déjà au TMI 45%** : le taux marginal ne change pas avec la division par 4.

**Très utile si** :
- TMI habituel 30% et revenu exceptionnel fait passer à 41%
- TMI habituel 11% et revenu exceptionnel fait passer à 30% ou 41%

### Exemple

Foyer célibataire, RNI habituel 40 000 € (TMI 30%), gain RSU 80 000 € imposé comme salaire (plan non qualifiant imposé l'année du vesting, ou plan qualifiant dont l'AGE date au plus tard du 07/08/2015 ; pour un plan qualifiant dont l'AGE date de 2018 ou après, seuls 40 000 € entreraient au barème après abattement de 50 %, l'année de la cession).

**Sans quotient** :
- RNI total : 120 000 €
- Impôt approximatif : ~32 000 €

**Avec quotient (coefficient 4)** :
- Revenu fractionné : 40 000 + 80 000/4 = 60 000 €
- Impôt sur 60 000 € : ~12 000 €
- Impôt sur 40 000 € : ~5 100 €
- Supplément × 4 : (12 000 − 5 100) × 4 = 27 600 €
- Impôt total : 5 100 + 27 600 = ~32 700 €

Dans cet exemple, peu de gain car le revenu ordinaire est déjà en tranche 30%. L'intérêt est marginal.

**Règle** : chiffrer systématiquement les deux scénarios avant de recommander le quotient.

## CEHR (Contribution Exceptionnelle Hauts Revenus)

Voir `data/bareme-ir-2025.json` → `cehr`. Base légale : art. 223 sexies CGI.

### Seuils (revenus 2025)

| Situation | Tranche 3% | Tranche 4% |
|-----------|-----------|-----------|
| Célibataire | 250 000 € à 500 000 € | > 500 000 € |
| Couple | 500 000 € à 1 000 000 € | > 1 000 000 € |

**Base de calcul : RFR** (pas RNI), au sens du 1° du IV de l'article 1417 CGI, **sans application du quotient de l'article 163-0 A** (un revenu exceptionnel imposé au quotient compte pour son montant total) et sans tenir compte des plus-values d'apport-cession (I de l'article 150-0 B ter) dont le report d'imposition expire dans l'année. Le RFR inclut des éléments exonérés ou déduits pour l'IR (certains revenus du capital, abattements réintégrés, versements PER déduits au titre de l'article 163 quatervicies).

### À ne pas oublier

- S'ajoute à l'IR net (ne se déduit pas)
- Lissage (art. 223 sexies, II, 1 CGI) : si le RFR de l'année est au moins égal à 1,5 fois la moyenne des RFR des deux années précédentes, la fraction du RFR qui excède cette moyenne est divisée par deux puis ajoutée à la moyenne, et la contribution ainsi calculée est multipliée par deux. Conditions : RFR de chacune des deux années précédentes au plus égal à 250 000 € (célibataire, veuf, séparé, divorcé) ou 500 000 € (imposition commune), et foyer passible de l'IR ces deux années pour plus de la moitié de ses revenus de même nature. Mise en oeuvre : la 2042 C (revenus 2025) ne prévoit pas de case de demande, seulement la case 8TD à cocher si les revenus non passibles de l'IR en France ont excédé 50 % des revenus mondiaux en 2023 ou 2024 ; en cas de changement de situation de famille sur la période, le bénéfice est subordonné à une réclamation ; contrôler l'avis d'imposition et, si le lissage n'a pas été appliqué, adresser la demande au centre des finances publiques. La CEHR retenue pour calculer la CDHR est toujours la CEHR non lissée.

## CDHR (Contribution Différentielle sur les Hauts Revenus)

Voir `data/bareme-ir-2025.json` → `cdhr`.

Mécanisme **distinct de la CEHR** : impose un **plancher d'imposition à 20 %** sur les foyers à hauts RFR. À ne jamais confondre avec la CEHR (les deux peuvent s'appliquer simultanément sur un même foyer).

### Base légale

- Art. 224 CGI, créé par l'**art. 10 de la LFI 2025** (loi n° 2025-127 du 14/02/2025)
- **Prorogée par l'art. 2 de la LFI 2026** (loi n° 2026-103 du 19/02/2026) : applicable à compter de l'imposition des revenus 2025 et jusqu'à l'imposition des revenus de l'année au titre de laquelle le projet de loi d'approbation des comptes constate un **déficit du budget général** inférieur à 3 % du PIB (version initiale : revenus 2025 seulement). Acompte et pénalités reconduits.

### Seuils RFR

| Situation | Seuil de déclenchement |
|---|---|
| Célibataire, veuf, séparé, divorcé | RFR > 250 000 € |
| Couple marié ou pacsé (imposition commune) | RFR > 500 000 € |

### Mécanisme

La CDHR s'applique lorsque l'imposition retenue reste **inférieure à 20 % du revenu de référence** (RFR retraité selon le II de l'art. 224 : notamment revenus exceptionnels retenus pour le quart, revenus exonérés par convention et revenus de brevets taxés à 10 % exclus). Formule (BOI-IR-CDHR-10 § 240) : CDHR = [(revenu de référence × 20 %) - décote] - [IR + CEHR non lissée + prélèvements libératoires + 1 500 € par personne à charge + 12 500 € pour un couple soumis à imposition commune], si positive. L'IR retenu est l'IR après réductions et crédits, **majoré** d'une liste de réductions et crédits réintégrés (Pinel/Denormandie, Malraux, Madelin/FCPI/FIP, outre-mer, etc. ; dons de l'art. 200 à compter des revenus 2026) ; emploi à domicile, garde d'enfants et Sofica ne sont pas réintégrés. L'IR afférent aux revenus exceptionnels est lui aussi retenu pour le quart ; la CEHR afférente est retenue en totalité pour les revenus 2025 et pour le quart à compter des revenus 2026 (art. 2 LFI 2026). Décote si le revenu de référence est ≤ 330 000 € (célibataire) ou ≤ 660 000 € (couple) : décote = revenu × 20 % - (revenu - 250 000 €) × 82,5 % (500 000 € pour un couple), si positive.

Calcul par l'administration après dépôt de la 2042. La 2042 C (revenus 2025) comporte un cadre « Précisions pour le calcul de la CDHR » à remplir le cas échéant : revenus exceptionnels non taxés au quotient et leur taux proportionnel d'imposition (8KD/8KE, 8KF/8KG ; déclarer le montant total, seul le quart est retenu), revenus exonérés par convention (8CD). Les produits soumis à prélèvement libératoire y sont ventilés selon qu'ils ont été perçus du 1er janvier au 14 février 2025 ou du 15 février au 31 décembre 2025 (2DK/2DL, 2XY/2XZ, 2VJ/2VK, 2EF/2EG).

### Distinction CEHR vs CDHR

| Critère | CEHR (art. 223 sexies CGI) | CDHR (art. 224 CGI) |
|---|---|---|
| Nature | Surtaxe additionnelle | Plancher d'imposition |
| Taux | 3 % à 4 % selon tranche RFR | 0 à 20 % selon écart au plancher |
| Mode de calcul | Direct sur le RFR | Différentiel : 20 % du revenu de référence, moins la décote, moins (IR majoré + CEHR non lissée + prélèvements libératoires + 1 500 € par personne à charge + 12 500 € par couple) |
| Application | Tous les foyers > seuils | Uniquement si l'imposition retenue reste sous 20 % du revenu de référence |

Les deux peuvent s'appliquer simultanément : la CEHR est toujours due au-delà des seuils, la CDHR se déclenche surtout en cas de fort poids des revenus au PFU (imposés à 12,8 % d'IR), mais aussi en présence de réductions d'impôt non réintégrées ou de revenus soumis à prélèvement libératoire.

### Calendrier

- **Acompte** : 95 % du montant estimé à verser entre le **1er et le 15 décembre** de l'année des revenus, via le service "Prélèvement à la source" sur impots.gouv.fr
- **Solde** : calculé automatiquement par l'administration après dépôt de la 2042 au printemps suivant ; l'acompte s'impute sur la CDHR due et l'excédent est restitué
- **Pénalité** : majoration de 20 % en cas de défaut ou de retard de paiement de l'acompte (assiette : 95 % de la CDHR due), ou si l'acompte versé est inférieur de plus de 20 % à 95 % de la CDHR due (assiette : 95 % de la CDHR due moins l'acompte versé)

### Cas typiques touchés

- Dirigeants à fort revenu PFU dividendes (TMI effectif IR ~12,8 % alors que RFR > 250 k€)
- Business angels avec PV mobilières importantes
- Cadres exécutifs à fort RSU/BSPCE l'année de vesting/cession (à nuancer : un revenu exceptionnel déclaré dans le cadre CDHR de la 2042 C n'est retenu que pour le quart, avec l'IR qui s'y rapporte)

### Source officielle

[impots.gouv.fr : Contribution Différentielle sur les Hauts Revenus](https://www.impots.gouv.fr/actualite/contribution-differentielle-sur-les-hauts-revenus-cdhr)

## Revenus étrangers et conventions fiscales

### Principes

- France applique le principe de **mondialité** pour les résidents : imposition sur l'ensemble des revenus (y compris étrangers)
- **Conventions fiscales bilatérales** peuvent prévoir :
  - Exonération en France (méthode de l'exemption)
  - Imposition en France avec crédit d'impôt pour l'impôt payé à l'étranger (méthode de l'imputation)

### Méthodes courantes

| Méthode | Effet |
|---------|-------|
| Exemption totale | Revenu non imposé en France |
| Exemption avec taux effectif | Revenu inclus pour le calcul du taux, mais non imposé |
| Imputation | Revenu imposé en France, crédit d'impôt = impôt payé à l'étranger (limité à l'impôt français correspondant) |

### À vérifier

- La convention fiscale **entre la France et le pays de source** du revenu
- Formulaire 2047 pour déclarer les revenus étrangers (annexe à la 2042)
- Crédits d'impôt étrangers : reports, limitations

**Zone complexe** : renvoyer vers un avocat fiscaliste pour les cas significatifs (expatriation partielle, revenus locatifs étrangers, retraites étrangères).

## Expatriation et retour en France

### Exit tax

Article 167 bis CGI : imposition immédiate des plus-values latentes sur titres détenus lors du départ à l'étranger, si :
- Résidence fiscale française pendant au moins 6 ans sur les 10 dernières années
- Détention de titres > seuils (plusieurs catégories de seuils)

Sursis de paiement possible dans certains cas. Régime complexe.

### Retour en France

Régime d'**impatriation** (article 155 B CGI) : exonération partielle de l'impôt pour les impatriés sous conditions strictes. Durée 8 ans max.

**Hors scope ce skill** : renvoyer vers un avocat fiscaliste spécialisé.

## DOM-TOM

Régimes spéciaux :
- Réduction d'impôt de 30% à 40% dans les DOM (plafonnée)
- Revenus de source DOM : régime spécifique
- Investissement Girardin : mécanismes distincts

**Hors scope ce skill** pour le détail. Signaler la spécificité et renvoyer vers la documentation locale / BOFiP dédié.

## Allocations chômage et revenus de remplacement

Déclarées case **1AP / 1BP** (pas 1AJ). Bien vérifier le pré-rempli France Travail.

**Points critiques** :
- **Abattement 10 % applicable** : l'ARE est un revenu de remplacement imposé selon les règles des traitements et salaires (BOI-RSA-BASE-30-50-20). La déduction forfaitaire de 10 % s'applique, pour chaque membre du foyer, sur le total de ses salaires et de son ARE (minimum 509 € et maximum 14 555 € par personne, revenus 2025). La déclarer en 1AP au lieu de 1AJ ne supprime PAS l'abattement.
- CSG prélevée à taux réduit à la source
- La fraction de CSG prélevée à taux réduit n'est pas déductible du revenu imposable

**Pourquoi 1AP et pas 1AJ ?** L'ARE n'est pas un revenu d'*activité* mais de *remplacement* : la distinction compte pour certaines prestations sociales, pas pour l'abattement de 10 %. Elle ne joue pas non plus pour le plafond de déduction PER : la brochure IR 2026 range expressément les allocations de chômage parmi les revenus salariaux retenus pour ce plafond.

## Professions médicales conventionnées secteur 1

Deux déductions forfaitaires spécifiques aux médecins conventionnés secteur 1
en déclaration contrôlée (BOI-BNC-SECT-40) :

- **Déduction Groupe III (2 %)** : forfait de 2 % des recettes brutes couvrant
  représentation, réception, prospection, cadeaux professionnels, travaux de
  recherche, blanchissage et petits déplacements (§ 120). Alternative au réel :
  non cumulable avec la déduction des frais réels de ces mêmes catégories.
- **Déduction complémentaire (3 %)** : 3 % calculés sur les recettes
  conventionnelles (§ 160).

Depuis la disparition du régime AGA/OGA (majoration supprimée depuis les
revenus 2023, réduction frais de comptabilité abrogée par la LF 2025), ces
forfaits constituent le principal avantage catégoriel restant pour les
médecins secteur 1. Vérifier les conditions à jour dans BOI-BNC-SECT-40 avant
application.

## Situations matrimoniales particulières

### Année du mariage / PACS

- **Imposition commune** pour l'année entière (depuis 2011)
- Ou imposition séparée sur option (cases dédiées)
- À chiffrer : selon situation des conjoints, l'une peut être plus favorable

### Année de séparation / divorce

- **Imposition séparée** pour l'année entière depuis la séparation (principe)
- Enfants à charge : attribution selon accord ou garde principale
- Case T (parent isolé) possible pour celui qui assume seul les enfants

### Année du décès d'un conjoint

- Imposition commune jusqu'au décès (du 1er janvier à la date de décès)
- Imposition individuelle du conjoint survivant pour la fin de l'année
- Deux déclarations séparées à faire

## Droit de reprise DGFIP

Délai pendant lequel la DGFIP peut redresser :

| Impôt | Délai standard |
|-------|----------------|
| IR | 3 ans (jusqu'au 31 décembre de la 3e année suivant celle de l'imposition) |
| IFI | 3 ans si la déclaration révèle suffisamment l'exigibilité (LPF L. 180), 6 ans sinon ou à défaut de déclaration (LPF L. 186) |
| Tous impôts | **10 ans** en cas d'activité occulte ou fraude |
| TVA | 3 ans |

**Conservation des documents** : minimum 6 ans (conseil : 10 ans pour couvrir tous les cas).

## PUMA (Protection universelle maladie) : cotisation subsidiaire maladie

Concerne les personnes **affiliées à l'assurance maladie française** qui tirent peu ou pas de revenus d'activité professionnelle mais disposent d'un **patrimoine générateur de revenus du capital significatifs**.

### Conditions d'assujettissement cumulatives

- Rattachement à un régime d'assurance maladie français
- Revenus d'activité professionnelle **< 20 % du PASS** (≈ 9 420 € pour 2025)
- Revenus du capital (RCM, PV, revenus fonciers) > **50 % du PASS** (≈ 23 550 € pour 2025)

### Calcul

Assiette = revenus du patrimoine − abattement (50 % du PASS).
Taux : **6,5 %** appliqué à l'assiette (taux plafonné à 8 × PASS = ~376 k€ de base pour 2025).

Recouvrement : URSSAF, pas DGFIP. Avis distinct de l'avis IR.

### À vérifier systématiquement

- Retraités avec patrimoine significatif (dividendes, loyers) → potentiellement concernés
- Rentiers avant retraite → souvent concernés
- Personnes en congé sabbatique avec revenus du capital → vérifier

### Nuance

- **Non déductible** de l'IR (contrairement à la CSG sur revenus d'activité)
- Cumul avec les prélèvements sociaux 17,2 % sur les mêmes revenus du capital (pas de double comptage, mais additionne à la pression fiscale globale)

**Piège fréquent** : oublier la PUMA dans la simulation globale d'un FIRE / rentier → sous-estimation de ~6,5 % sur les revenus du capital hors seuil.

## Régularisation spontanée

**Intérêt** : réduction des pénalités si le contribuable rectifie avant contrôle.

- Intérêts de retard : 0,2%/mois
- Pas de majoration si régularisation spontanée et bonne foi

**Quand envisager** : oubli de déclaration (crypto, revenus étrangers, plus-values). Orienter vers un avocat fiscaliste pour les cas significatifs (régularisation structurée).

## Références CGI / BOFiP

- Résidence fiscale : art. 4 B CGI
- Non-résidents : art. 164 A à 165 CGI
- Revenus exceptionnels : art. 163-0 A CGI
- CEHR : art. 223 sexies CGI
- Exit tax : art. 167 bis CGI
- Impatriation : art. 155 B CGI
- Droit de reprise : LPF (Livre des Procédures Fiscales)
- PUMA / cotisation subsidiaire maladie : art. L. 380-2 CSS
- BOFiP : BOI-INT (conventions internationales), BOI-IR-LIQ
