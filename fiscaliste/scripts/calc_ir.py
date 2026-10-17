#!/usr/bin/env python3
"""
Calculateur IR déterministe pour revenus 2025 (déclaration 2026).

Usage:
    # Calcul direct, personne seule sans personne à charge
    python fiscaliste/scripts/calc_ir.py --parts 1 --rni 45000

    # Calcul direct selon la situation de famille (parts calculées par le script)
    python fiscaliste/scripts/calc_ir.py --rni 60000 --situation celibataire --enfants 1 --parent-isole
    python fiscaliste/scripts/calc_ir.py --rni 70000 --situation veuf --enfants 1
    python fiscaliste/scripts/calc_ir.py --rni 90000 --situation marie --enfants 1 --enfants-alternee 2

    # Parts fournies (mode historique) : --parts-base obligatoire dès que --parts > 1
    # (2 = imposition commune ; 1 = célibataire ou divorcé sans case T)
    python fiscaliste/scripts/calc_ir.py --parts 3 --parts-base 2 --rni 126000

    # Via fichier foyer.json
    python fiscaliste/scripts/calc_ir.py --foyer foyer.example.json

    # Sortie JSON
    python fiscaliste/scripts/calc_ir.py --parts 2 --parts-base 2 --rni 90000 --json

Situations (--situation ou champ foyer.situation) : celibataire, divorce, separe,
marie, pacse, veuf (conjoint décédé avant le 1er janvier 2025), veuf_annee_deces
(déclaration individuelle du survivant, pour la période postérieure au décès
survenu en 2025). L'année du décès, il y a deux déclarations : la déclaration
commune (du 1er janvier au décès) se calcule avec marie ou pacse. Époux imposés
séparément (option l'année du mariage, cas de l'art. 6-4 CGI) : une déclaration
par personne, avec separe (1 part de base, décote des personnes seules).

Couvre :
    - Déduction de 10 % sur traitements, salaires et allocations chômage calculée
      pour chaque membre du foyer sur le total de SES salaires et de SON ARE
      (minimum et maximum par personne, minimum borné au montant brut : jamais de
      revenu net négatif) ; abattement de 10 % sur pensions par pensionné
      (minimum par pensionné borné à sa pension), somme plafonnée pour le foyer
    - Barème progressif tranche par tranche
    - Quotient familial avec plafonnement selon la situation de famille, jamais
      selon le nombre de parts : impôt de référence sur 1 part (célibataire,
      divorcé, séparé, veuf) ou 2 parts (mariés, pacsés, survivant l'année du
      décès) ; case T parent isolé (plafond propre pour la part du premier
      enfant) ; veuf avec enfants à charge (2 parts de base, plafonnement par
      rapport à 1 part puis réduction complémentaire plafonnée) ; enfants en
      résidence alternée classés après les enfants à charge exclusive ou principale
    - Décote selon la situation de famille : barème des couples pour la seule
      imposition commune (marie, pacse, ou --parts-base 2), barème des personnes
      seules pour tous les autres, survivant l'année du décès compris
    - Arrondi à l'euro le plus proche (Decimal, ROUND_HALF_UP : 0,50 € compté
      pour 1 €) ; champ informatif sous_seuil_recouvrement_61 (impôt sous le seuil
      de mise en recouvrement, laissé tel quel)
    - PS différenciés LFSS 2026 : 18,6 % revenus du patrimoine (PV mobilières,
      crypto, RCM 2025 sans PS lors du versement) / 17,2 % produits de placement
      2025 ayant supporté les PS lors du versement (dividendes, intérêts).
      Aucun PS pour un foyer dont residence_fiscale n'est pas FR.
      Les PS sur le résultat LMNP ne sont PAS calculés (le champ
      lmnp_reel_resultat du foyer.json n'alimente pas la base PS)
    - CEHR selon la situation de famille (seuils des couples pour la seule
      imposition commune)

Refus explicites (ValueError ; en ligne de commande, code de sortie 2) :
    - situation hors de la liste ci-dessus (concubin, etc.)
    - case T (parent_isole / --parent-isole) hors célibataire, divorcé ou séparé,
      ou sans enfant
    - revenus_chomage (champ historique) non nul pour un couple marié ou pacsé,
      ou renseigné avec revenus_chomage_declarant1/2 : ventiler l'ARE par déclarant
    - CEHR du survivant l'année du décès dès que le RFR dépasse le premier seuil
      des personnes seules (assiette scindée avant et après décès)
    - cas non gérés (« cas non géré par calc_ir.py ») : nb_enfants_invalides > 0,
      champs booléens case_p, case_f, case_w, case_s, case_g (demi-parts
      invalidité, ancien combattant, veuve de guerre et leur réduction
      complémentaire), case_l (demi-part à plafond propre), veuf ou survivant
      l'année du décès (veuf_annee_deces) ayant au moins un enfant en résidence
      alternée, quel que soit le nombre d'enfants à charge exclusive

Ne couvre PAS :
    - Réductions / crédits d'impôt (à retrancher manuellement après)
    - Régimes spéciaux (revenus exceptionnels, non-résidents, DOM-TOM) : pour un
      non-résident, seul le retrait des PS sur revenus du capital est appliqué
    - IFI (script distinct à créer si besoin)
    - Situations familiales particulières refusées ci-dessus : les calculer avec
      la fiche 2041 ou le simulateur impots.gouv.fr

Les valeurs viennent de data/bareme-ir-2025.json. Pour une autre année,
exposer --bareme data/bareme-ir-XXXX.json.
"""

import argparse
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / "data"
DEFAULT_BAREME = DATA_DIR / "bareme-ir-2025.json"
DEFAULT_PFU = DATA_DIR / "pfu-prelevements-sociaux.json"

SITUATIONS = ("celibataire", "divorce", "separe", "marie", "pacse", "veuf", "veuf_annee_deces")
# Imposition commune : décote et seuils CEHR des couples. Jamais veuf_annee_deces
# (BOI-IR-LIQ-20-20-30 § 70 : décote des personnes seules après le décès).
SITUATIONS_IMPOSITION_COMMUNE = ("marie", "pacse")
# Case T (art. 194 II et 197 I-2 CGI) : le veuf n'y figure pas.
SITUATIONS_CASE_T = ("celibataire", "divorce", "separe")

MSG_CASE_T = ("case T réservée aux célibataires, divorcés ou séparés vivant seuls avec au "
              "moins un enfant à charge (art. 194 II CGI)")
MSG_CHOMAGE_NON_VENTILE = (
    "revenus_chomage non ventilé : pour un couple, renseigner revenus_chomage_declarant1 "
    "(case 1AP) et/ou revenus_chomage_declarant2 (case 1BP). La déduction de 10 % se "
    "calcule par bénéficiaire (BOI-RSA-BASE-30-50-20, § 80 et § 210).")
MSG_CHOMAGE_DOUBLE = (
    "revenus_chomage non ventilé : le champ historique revenus_chomage est renseigné en même "
    "temps que revenus_chomage_declarant1/2 ; ne garder que revenus_chomage_declarant1 "
    "(case 1AP) et/ou revenus_chomage_declarant2 (case 1BP). La déduction de 10 % se "
    "calcule par bénéficiaire (BOI-RSA-BASE-30-50-20, § 80 et § 210).")
MSG_CEHR_ANNEE_DECES = ("CEHR de l'année du décès non calculée : assiette scindée avant et "
                        "après décès (BOI-IR-CHR § 100)")
AVERTISSEMENT_PARTS_BASE_1 = ("mode --parts-base 1 : ni case T ni veuf pris en compte, "
                              "utiliser --situation")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def cas_non_gere(description):
    return ValueError(f"cas non géré par calc_ir.py : {description} ; calculer avec la "
                      f"fiche 2041 ou le simulateur impots.gouv.fr")


def _euros(montant):
    """Montant entier en texte, séparateur de milliers français (1 801)."""
    return f"{montant:,}".replace(",", " ")


# ─────────────────────────────────────────────────────
# Arrondi
# ─────────────────────────────────────────────────────

def _dec(x):
    """Decimal sans bruit binaire : un float passe par sa représentation décimale."""
    return x if isinstance(x, Decimal) else Decimal(str(x))


def arrondi_euro(x):
    """Arrondi à l'euro le plus proche (CGI, art. 193 et 1657-1).

    Fractions inférieures à 0,50 € négligées, fractions de 0,50 € et plus comptées
    pour 1 € (1 597,50 donne 1 598). round() de Python arrondit les demis au pair
    (round(1596.5) == 1596) : ne pas l'utiliser pour un montant fiscal.
    """
    return int(_dec(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


# ─────────────────────────────────────────────────────
# Abattement salaires / pensions
# ─────────────────────────────────────────────────────

def abattement_salaires(brut_1aj, bareme):
    """Revenu net après la déduction de 10 % pour UN membre du foyer (salaires + ARE).

    Minimum et maximum s'appliquent distinctement à chaque membre du foyer
    (art. 83, 3° CGI ; BOI-RSA-BASE-30-50-20 § 80 et § 210) et la déduction ne
    peut excéder le montant brut (§ 100) : jamais de revenu net négatif. Appeler
    une fois par membre, jamais sur la somme du foyer.
    """
    if brut_1aj <= 0:
        return 0
    cfg = bareme["abattement_salaires_10pct"]
    brut = _dec(brut_1aj)
    abatt = min(brut, max(_dec(cfg["minimum"]), min(_dec(cfg["maximum"]), brut * _dec(cfg["taux"]))))
    return arrondi_euro(brut - abatt)


def abattement_pensions_foyer(pensions, bareme):
    """Revenu net des pensions du foyer après l'abattement de 10 % (art. 158, 5-a CGI).

    pensions : liste des pensions brutes, une valeur par pensionné. 10 % par
    pensionné avec un minimum par pensionné sans excéder sa pension, puis somme
    des abattements plafonnée pour l'ensemble du foyer (BOI-RSA-PENS-30-10-10
    § 160 à 180).
    """
    cfg = bareme["abattement_pensions_10pct"]
    montants = [_dec(p) for p in pensions if p > 0]
    if not montants:
        return 0
    minimum, taux = _dec(cfg["minimum"]), _dec(cfg["taux"])
    abatt = sum(min(p, max(minimum, p * taux)) for p in montants)
    abatt = min(abatt, _dec(cfg["maximum"]))
    return arrondi_euro(sum(montants) - abatt)


# ─────────────────────────────────────────────────────
# Barème progressif (tranche par tranche)
# ─────────────────────────────────────────────────────

def _bornes(tranche):
    if "jusqu_a" in tranche and "de" not in tranche:
        return 0, tranche["jusqu_a"]
    if "au_dela" in tranche:
        return tranche["au_dela"], None
    return tranche["de"], tranche["a"]


def impot_bareme(rni, parts, tranches):
    """Impôt (impôt sur rni / parts) x parts, en Decimal.

    Calculé sans division, bornes des tranches multipliées par le nombre de parts :
    même résultat que le calcul sur 1 part, mais exact au centime, ce qui garde
    l'arrondi à l'euro fiable sur une fraction de 0,50 €.
    """
    revenu = _dec(rni)
    n = _dec(parts)
    impot = Decimal(0)
    for t in tranches:
        bas, haut = _bornes(t)
        bas_n = _dec(bas) * n
        if revenu <= bas_n:
            break
        haut_n = revenu if haut is None else min(revenu, _dec(haut) * n)
        impot += (haut_n - bas_n) * _dec(t["taux"])
    return impot


def impot_par_part(quotient, tranches):
    """Calcule l'impôt sur un quotient (1 part) en appliquant les tranches."""
    return float(impot_bareme(quotient, 1, tranches))


# ─────────────────────────────────────────────────────
# Parts de quotient familial
# ─────────────────────────────────────────────────────

def parts_enfants(n_excl, n_alt):
    """Majoration de parts au titre des enfants (art. 194 I CGI).

    Rangs 1 et 2 : 0,5 part ; à partir du rang 3 : 1 part. Les enfants à charge
    exclusive ou principale occupent les premiers rangs ; un enfant en résidence
    alternée reçoit la moitié de la majoration de son rang (brochure IR 2026,
    tableau 3) : 1 exclusif + 2 alternés = 0,5 + 0,25 + 0,5.
    """
    total = 0.0
    for rang in range(1, n_excl + n_alt + 1):
        majoration = 0.5 if rang <= 2 else 1.0
        total += majoration if rang <= n_excl else majoration / 2
    return total


def calcul_parts(situation, enfants=0, enfants_alternee=0, parent_isole=False):
    """Parts et régime de calcul selon la situation de famille.

    Retourne le dict des paramètres de régime de calc() : parts, parts_base
    (parts de l'impôt de référence A de la fiche 2041, rubrique 6),
    imposition_commune (décote et CEHR des couples), case_t, veuf_avec_charge,
    survivant_annee_deces, enfants, enfants_alternee, situation.
    Lève ValueError pour une situation inconnue, une case T impossible ou un cas
    non géré.
    """
    if situation not in SITUATIONS:
        raise ValueError(f"situation inconnue : {situation}")
    for nom, n in (("enfants à charge", enfants), ("enfants en résidence alternée", enfants_alternee)):
        if isinstance(n, bool) or not isinstance(n, int) or n < 0:
            raise ValueError(f"nombre d'{nom} invalide : {n!r}")
    if not isinstance(parent_isole, bool):
        raise ValueError(f"parent_isole doit valoir true ou false : {parent_isole!r}")
    if parent_isole and (situation not in SITUATIONS_CASE_T or enfants + enfants_alternee == 0):
        raise ValueError(MSG_CASE_T)
    # Parts et plafonnement d'un enfant en résidence alternée non vérifiés pour le veuf
    # et pour le survivant l'année du décès : refus, quel que soit le nombre d'enfants
    # à charge exclusive ou principale.
    if situation == "veuf" and enfants_alternee > 0:
        raise cas_non_gere("veuf avec au moins un enfant en résidence alternée "
                           "(règle non vérifiée)")
    if situation == "veuf_annee_deces" and enfants_alternee > 0:
        raise cas_non_gere("survivant l'année du décès (veuf_annee_deces) avec au moins un "
                           "enfant en résidence alternée (règle non vérifiée)")

    majoration = parts_enfants(enfants, enfants_alternee)
    veuf_avec_charge = situation == "veuf" and enfants > 0
    if situation in SITUATIONS_IMPOSITION_COMMUNE or situation == "veuf_annee_deces":
        # Survivant l'année du décès : mêmes parts que le couple, impôt A sur 2 parts.
        parts, parts_base = 2 + majoration, 2
    elif veuf_avec_charge:
        # Veuf avec enfant à charge : parts du couple (art. 194 I), mais impôt A sur 1 part.
        parts, parts_base = 2 + majoration, 1
    else:
        parts, parts_base = 1 + majoration, 1
    if parent_isole:
        # Case T : +0,5 part ; +0,25 seulement si un unique enfant, en résidence alternée.
        if enfants > 0 or enfants_alternee >= 2:
            parts += 0.5
        else:
            parts += 0.25
    return {
        "situation": situation,
        "parts": parts,
        "parts_base": parts_base,
        "imposition_commune": situation in SITUATIONS_IMPOSITION_COMMUNE,
        "case_t": parent_isole,
        "veuf_avec_charge": veuf_avec_charge,
        "survivant_annee_deces": situation == "veuf_annee_deces",
        "enfants": enfants,
        "enfants_alternee": enfants_alternee,
    }


# ─────────────────────────────────────────────────────
# Décote
# ─────────────────────────────────────────────────────

def decote(impot, imposition_commune, bareme):
    """Montant de la décote (Decimal), limité à l'impôt.

    Barème des couples pour l'imposition commune seulement, barème des personnes
    seules sinon, quel que soit le nombre de parts. S'applique à l'impôt après
    plafonnement du quotient familial et réduction complémentaire du veuf.
    """
    cfg = bareme["decote"]
    regime = "couple" if imposition_commune else "celibataire"
    seuil = _dec(cfg[f"seuil_{regime}"])
    plafond = _dec(cfg[f"plafond_{regime}"])
    impot = _dec(impot)
    if impot >= seuil:
        return Decimal(0)
    return min(impot, max(Decimal(0), plafond - _dec(cfg["taux"]) * impot))


# ─────────────────────────────────────────────────────
# Quotient familial avec plafonnement (fiche 2041, rubrique 6)
# ─────────────────────────────────────────────────────

def plafond_avantage_qf(parts, parts_base, case_t, enfants, enfants_alternee, bareme):
    """Montant B : avantage maximal des parts au-delà des parts de base (Decimal).

    - Cas général (veuf compris, base 1 part) : plafond par demi-part, soit la
      moitié par quart de part.
    - Case T avec au moins un enfant à charge exclusive ou principale : plafond
      propre pour les deux premières demi-parts au-delà de 1 part (part du premier
      enfant), puis plafond général.
    - Case T avec enfants en résidence alternée seulement : moitié du plafond
      propre pour chacun des deux premiers enfants (deux quarts chacun), puis
      moitié du plafond général par quart suivant.
    """
    qf = bareme["quotient_familial"]
    plafond_demi_part = _dec(qf["plafond_gain_par_demi_part"])
    quarts = (_dec(parts) - _dec(parts_base)) * 4
    if not case_t:
        return plafond_demi_part / 2 * quarts
    plafond_case_t = _dec(qf["plafond_parent_isole_premier_enfant"])
    if enfants > 0:
        return plafond_case_t + plafond_demi_part / 2 * (quarts - 4)
    k = min(enfants_alternee, 2)
    return plafond_case_t / 2 * k + plafond_demi_part / 2 * (quarts - 2 * k)


def impot_avec_qf(rni, parts, parts_base, bareme, case_t=False, veuf_avec_charge=False,
                  enfants=0, enfants_alternee=0):
    """
    Applique le QF avec plafonnement (fiche 2041, rubrique 6).
    - I : impôt avec toutes les parts
    - A : impôt de référence sur parts_base (1 ou 2 selon la situation)
    - B : plafond de l'avantage (plafond_avantage_qf)
    - I1 = max(I, A - B) ; veuf avec enfant à charge, si le plafonnement joue :
      réduction complémentaire H = min(plafond, A - I - B), impôt I2 = I1 - H.
    """
    tranches = bareme["bareme_ir"]["tranches"]
    impot_total = impot_bareme(rni, parts, tranches)
    impot_reference = impot_bareme(rni, parts_base, tranches)
    gain_max = plafond_avantage_qf(parts, parts_base, case_t, enfants, enfants_alternee, bareme)

    impot_plafonne = max(impot_total, impot_reference - gain_max)
    qf_plafonne = impot_plafonne > impot_total
    reduction = Decimal(0)
    if qf_plafonne and veuf_avec_charge:
        plafond_reduction = _dec(bareme["quotient_familial"]["reduction_complementaire_veuf_avec_enfants"])
        reduction = min(plafond_reduction, impot_reference - impot_total - gain_max)
    impot_brut = impot_plafonne - reduction

    return {
        "impot_brut": arrondi_euro(impot_brut),
        "impot_total_parts": arrondi_euro(impot_total),
        "impot_base_parts": arrondi_euro(impot_reference),
        "gain_qf_reel": arrondi_euro(impot_reference - impot_total),
        # Plafond B exact : il peut finir en 0,50 € (903,50 € par quart de part).
        "gain_qf_max": int(gain_max) if gain_max == gain_max.to_integral_value() else float(gain_max),
        "qf_plafonne": qf_plafonne,
        "reduction_complementaire_veuf": arrondi_euro(reduction),
    }


# ─────────────────────────────────────────────────────
# CEHR
# ─────────────────────────────────────────────────────

def cehr(rfr, imposition_commune, bareme):
    """CEHR (art. 223 sexies CGI) : seuils des couples pour l'imposition commune
    seulement, seuils des personnes seules sinon, quel que soit le nombre de parts."""
    cfg = bareme["cehr"]
    seuils = cfg["seuils_couple"] if imposition_commune else cfg["seuils_celibataire"]
    rfr = _dec(rfr)
    total = Decimal(0)
    for t in seuils:
        taux = _dec(t["taux"])
        if "au_dela" in t:
            if rfr > _dec(t["au_dela"]):
                total += (rfr - _dec(t["au_dela"])) * taux
        elif rfr > _dec(t["de"]):
            total += (min(rfr, _dec(t["a"])) - _dec(t["de"])) * taux
    return arrondi_euro(total)


# ─────────────────────────────────────────────────────
# PS sur revenus du capital
# ─────────────────────────────────────────────────────

def ps_capital(base_patrimoine, base_placement, pfu_data):
    """PS différenciés LFSS 2026 (revenus 2025).

    - Revenus du patrimoine (PV mobilières CTO, crypto, LMNP, RCM 2025 n'ayant pas
      supporté les PS lors du versement) : 18,6 % dès 2025.
    - Produits de placement (dividendes, intérêts, RCM) ayant supporté les PS lors
      du versement : 17,2 % pour les encaissements 2025 (18,6 % à partir du
      01/01/2026).
    """
    ps = pfu_data["prelevements_sociaux"]
    taux_patrimoine = ps["taux_revenus_du_patrimoine_2025"]["valeur"]
    taux_placement = ps["taux_produits_de_placement_2025"]["valeur"]
    montant_patrimoine = arrondi_euro(_dec(base_patrimoine) * _dec(taux_patrimoine))
    montant_placement = arrondi_euro(_dec(base_placement) * _dec(taux_placement))
    return {
        "patrimoine": {"base": base_patrimoine, "taux": taux_patrimoine,
                       "montant": montant_patrimoine},
        "placement": {"base": base_placement, "taux": taux_placement,
                      "montant": montant_placement},
        "total": montant_patrimoine + montant_placement,
    }


# ─────────────────────────────────────────────────────
# Orchestration
# ─────────────────────────────────────────────────────

def calc(rni, parts, parts_base, bareme, rfr=None, base_ps_patrimoine=0,
         base_ps_placement=0, pfu_data=None, *, imposition_commune, case_t=False,
         veuf_avec_charge=False, survivant_annee_deces=False, enfants=0,
         enfants_alternee=0, situation=None):
    """Calcul de l'impôt. Le régime (imposition_commune, case_t, veuf_avec_charge,
    survivant_annee_deces) est explicite : il ne se déduit jamais de parts_base.
    Les paramètres de régime sortent de calcul_parts() (ou du mode --parts-base)."""
    if parts_base not in (1, 2):
        raise ValueError(f"parts de base invalides : {parts_base} (1 ou 2)")
    if parts < parts_base:
        raise ValueError(f"parts ({parts:g}) inférieures aux parts de base ({parts_base:g})")
    seuil_cehr_personne_seule = _dec(bareme["cehr"]["seuils_celibataire"][0]["de"])
    if survivant_annee_deces and rfr and _dec(rfr) > seuil_cehr_personne_seule:
        raise ValueError(MSG_CEHR_ANNEE_DECES)

    qf = impot_avec_qf(rni, parts, parts_base, bareme, case_t=case_t,
                       veuf_avec_charge=veuf_avec_charge, enfants=enfants,
                       enfants_alternee=enfants_alternee)
    dec = decote(qf["impot_brut"], imposition_commune, bareme)
    impot_apres_decote = arrondi_euro(max(Decimal(0), _dec(qf["impot_brut"]) - dec))
    seuil_recouvrement = bareme["recouvrement"]["seuil_mise_en_recouvrement"]

    if (base_ps_patrimoine or base_ps_placement) and pfu_data:
        ps_detail = ps_capital(base_ps_patrimoine, base_ps_placement, pfu_data)
    else:
        ps_detail = None
    ps = ps_detail["total"] if ps_detail else 0
    cehr_montant = cehr(rfr, imposition_commune, bareme) if rfr else 0

    return {
        "situation": situation,
        "rni": rni,
        "parts": parts,
        "parts_base": parts_base,
        "imposition_commune": imposition_commune,
        "case_t": case_t,
        "quotient_par_part": arrondi_euro(_dec(rni) / _dec(parts)),
        "impot_brut_apres_qf": qf["impot_brut"],
        "qf_details": {
            "impot_reference_parts_base": qf["impot_base_parts"],
            "gain_qf_reel": qf["gain_qf_reel"],
            "gain_qf_max": qf["gain_qf_max"],
            "plafonne": qf["qf_plafonne"],
            "reduction_complementaire_veuf": qf["reduction_complementaire_veuf"],
        },
        "decote": arrondi_euro(dec),
        "impot_apres_decote": impot_apres_decote,
        "sous_seuil_recouvrement_61": 0 < impot_apres_decote < seuil_recouvrement,
        "prelevements_sociaux": ps,
        "ps_details": ps_detail,
        "cehr": cehr_montant,
        "total_a_payer": impot_apres_decote + ps + cehr_montant,
        "_note": ("Avant réductions et crédits d'impôt. Les additionner manuellement. "
                  "sous_seuil_recouvrement_61 est informatif : l'impôt n'est pas mis à 0."),
    }


def verifier_cas_non_geres(f, bareme):
    """Refuse les situations que le script ne sait pas calculer (ValueError)."""
    qf = bareme["quotient_familial"]
    if f.get("nb_enfants_invalides", 0):
        raise cas_non_gere("nb_enfants_invalides > 0 (demi-parts pour enfant invalide)")
    for champ in ("case_p", "case_f", "case_w", "case_s", "case_g"):
        if f.get(champ):
            reduction = _euros(qf["reduction_complementaire_invalidite_ancien_combattant"])
            raise cas_non_gere(f"{champ} (demi-part invalidité, ancien combattant ou veuve de "
                               f"guerre, réduction complémentaire de {reduction} € au plus)")
    if f.get("case_l"):
        plafond = _euros(qf["plafond_demi_part_case_l"])
        raise cas_non_gere(f"case_l (demi-part plafonnée à {plafond} €)")


def from_foyer(foyer, bareme, pfu_data):
    """Déduit les paramètres à partir d'un foyer.json."""
    f = foyer["foyer"]
    r = foyer["revenus"]
    d = foyer.get("deductions", {})

    # Situation et parts
    situation = f.get("situation", "celibataire")
    if situation not in SITUATIONS:
        raise ValueError(f"situation inconnue : {situation}")
    verifier_cas_non_geres(f, bareme)
    regime = calcul_parts(situation, f.get("nb_enfants_charge", 0),
                          f.get("nb_enfants_alternee", 0), f.get("parent_isole", False))

    # Revenu net catégoriel salaires + ARE (déduction de 10 %), calculé PAR MEMBRE
    # du foyer : minimum et plafond s'appliquent distinctement à chaque déclarant
    # (BOI-RSA-BASE-30-50-20 § 80 et § 210 ; fiche de calcul n° 2041 FDC, une
    # colonne par déclarant). L'ARE (cases 1AP/1BP) suit les règles des traitements
    # et salaires (§ 10) : elle s'ajoute à la base du membre qui la perçoit. Le
    # champ historique revenus_chomage n'est accepté que pour une déclaration à un
    # seul déclarant (rattaché au déclarant 1) : pour un couple, on ne sait pas à
    # qui le rattacher.
    chomage_d1 = r.get("revenus_chomage_declarant1", 0)
    chomage_d2 = r.get("revenus_chomage_declarant2", 0)
    chomage_historique = r.get("revenus_chomage", 0)
    if chomage_historique:
        if situation in SITUATIONS_IMPOSITION_COMMUNE:
            raise ValueError(MSG_CHOMAGE_NON_VENTILE)
        if chomage_d1 or chomage_d2:
            raise ValueError(MSG_CHOMAGE_DOUBLE)
        chomage_d1 = chomage_historique
    base_d1 = r.get("salaires_declarant1", 0) + chomage_d1
    base_d2 = r.get("salaires_declarant2", 0) + chomage_d2
    net_salaires = abattement_salaires(base_d1, bareme) + abattement_salaires(base_d2, bareme)

    # Pensions : minimum par pensionné, plafond pour le foyer (art. 158, 5-a CGI).
    net_pensions = abattement_pensions_foyer(
        [r.get("pensions_declarant1", 0), r.get("pensions_declarant2", 0)], bareme)

    # Revenus fonciers : déjà au net (micro post-abattement / réel post-charges).
    fonciers = r.get("revenus_fonciers_reels", 0) + r.get("revenus_fonciers_micro", 0)

    # Revenus imposables au barème (hors revenus du capital si PFU)
    revenu_global = net_salaires + net_pensions + fonciers

    # Déductions (PER + pension alimentaire + CSG déductible)
    # PER : per_declarant1/2 doivent être les montants DÉDUCTIBLES, déjà plafonnés
    # (plafond de l'avis, soldes reportés, mutualisation 6QR) ; rien n'est plafonné ici.
    per = d.get("per_declarant1", 0) + d.get("per_declarant2", 0)
    pension_alim = d.get("pension_alimentaire_enfant_majeur", 0)
    csg_ded = d.get("csg_deductible_n1", 0)
    rni = arrondi_euro(max(0, revenu_global - per - pension_alim - csg_ded))

    # Base PS sur revenus du capital, séparée par nature (LFSS 2026) :
    # - produits de placement (dividendes, intérêts) ayant supporté les PS lors du
    #   versement : 17,2 % sur les encaissements 2025
    # - revenus du patrimoine (PV mobilières, crypto) : 18,6 % dès les revenus 2025
    # RCM 2025 n'ayant pas supporté les PS lors de leur versement (ni par l'établissement
    # payeur, ni via un formulaire 2778-DIV ou 2778-SD) : PS mis en recouvrement sur l'avis
    # au titre des revenus du patrimoine (L. 136-6), donc 18,6 % dès 2025 (brochure IR 2026, p. 124).
    # Le champ rcm_sans_ps_a_la_source est une partie de dividendes_bruts + interets_rcm.
    rcm_total = r.get("dividendes_bruts", 0) + r.get("interets_rcm", 0)
    rcm_sans_ps = max(0, min(r.get("rcm_sans_ps_a_la_source", 0), rcm_total))
    base_ps_placement = rcm_total - rcm_sans_ps
    base_ps_patrimoine = (r.get("plus_values_mobilieres", 0) + r.get("crypto_plus_values", 0)
                          + rcm_sans_ps)

    # RFR approximatif : RNI + revenus du capital taxés au PFU + abattements réintégrés
    # Simplification : RNI + bases PS
    rfr_approx = rni + base_ps_placement + base_ps_patrimoine
    # Non-résident : pas de PS sur dividendes, intérêts, PV mobilières ni PV crypto
    # (service-public F2329). Les PS sur revenus fonciers ne sont pas calculés par ce script.
    resident = f.get("residence_fiscale", "FR") == "FR"

    return calc(
        rni=rni,
        bareme=bareme,
        rfr=rfr_approx,
        base_ps_patrimoine=base_ps_patrimoine if resident else 0,
        base_ps_placement=base_ps_placement if resident else 0,
        pfu_data=pfu_data,
        **regime,
    )


def _regime_cli(p, args):
    """Régime de calcul en ligne de commande (sans --foyer). Erreurs : p.error (code 2)."""
    options_famille = args.enfants or args.enfants_alternee or args.parent_isole
    if args.situation:
        if args.parts_base is not None:
            p.error("--parts-base et --situation s'excluent : avec --situation, les parts "
                    "de base se déduisent de la situation")
        try:
            regime = calcul_parts(args.situation, args.enfants or 0,
                                  args.enfants_alternee or 0, args.parent_isole)
        except ValueError as e:
            p.error(str(e))
        if args.parts is not None and abs(args.parts - regime["parts"]) > 1e-9:
            p.error(f"parts incohérentes : {regime['parts']:g} calculées pour la situation, "
                    f"{args.parts:g} fournies")
        return regime

    if options_famille:
        p.error("--enfants, --enfants-alternee et --parent-isole exigent --situation")
    if args.parts is None:
        p.error("--rni et --situation (ou --parts) requis sauf si --foyer est utilisé")
    if args.parts < 1:
        p.error(f"--parts doit valoir au moins 1 : {args.parts:g} fourni")
    if args.parts_base is None:
        if args.parts != 1:
            p.error(f"situation ambiguë : --parts {args.parts:g} sans --situation ni "
                    f"--parts-base. Préciser --situation (et --parent-isole pour la case T, "
                    f"--situation veuf pour un veuf).")
        parts_base = 1
    else:
        if args.parts_base not in (1, 2):
            p.error(f"--parts-base doit valoir 1 (personne seule) ou 2 (imposition commune) : "
                    f"{args.parts_base:g} fourni")
        if args.parts < args.parts_base:
            p.error(f"--parts ({args.parts:g}) inférieur à --parts-base ({args.parts_base:g})")
        parts_base = int(args.parts_base)
        if parts_base == 1:
            print(AVERTISSEMENT_PARTS_BASE_1, file=sys.stderr)
    return {
        "situation": None,
        "parts": args.parts,
        "parts_base": parts_base,
        "imposition_commune": parts_base == 2,
        "case_t": False,
        "veuf_avec_charge": False,
        "survivant_annee_deces": False,
        "enfants": 0,
        "enfants_alternee": 0,
    }


def main():
    p = argparse.ArgumentParser(description="Calculateur IR déterministe : revenus 2025")
    p.add_argument("--rni", type=float, help="Revenu net imposable (après abattements et déductions)")
    p.add_argument("--situation", choices=SITUATIONS,
                   help="Situation de famille : les parts, le plafonnement, la décote et la "
                        "CEHR en découlent (veuf : conjoint décédé avant 2025 ; "
                        "veuf_annee_deces : déclaration du survivant après le décès)")
    p.add_argument("--enfants", type=int, default=None,
                   help="Enfants à charge exclusive ou principale (avec --situation)")
    p.add_argument("--enfants-alternee", type=int, default=None,
                   help="Enfants en résidence alternée (avec --situation)")
    p.add_argument("--parent-isole", action="store_true",
                   help="Case T : célibataire, divorcé ou séparé vivant seul avec enfant à charge")
    p.add_argument("--parts", type=float,
                   help="Nombre de parts fiscales (avec --situation : contrôle de cohérence)")
    p.add_argument("--parts-base", type=float,
                   help="Mode historique sans --situation : 1 (célibataire ou divorcé sans "
                        "case T) ou 2 (imposition commune) ; obligatoire si --parts > 1")
    p.add_argument("--rfr", type=float, help="RFR pour CEHR (optionnel)")
    p.add_argument("--base-ps-patrimoine", type=float, default=0,
                   help="Base PS revenus du patrimoine (PV mobilières, crypto, RCM 2025 sans PS "
                        "lors du versement) : 18,6 %% dès 2025")
    p.add_argument("--base-ps-placement", type=float, default=0,
                   help="Base PS produits de placement ayant supporté les PS lors du versement "
                        "(dividendes, intérêts) : 17,2 %% en 2025. RCM 2025 sans PS lors du "
                        "versement : --base-ps-patrimoine")
    p.add_argument("--base-ps", type=float, default=0,
                   help="(déprécié) alias de --base-ps-placement, comportement 17,2 %% historique")
    p.add_argument("--foyer", type=str, help="Chemin vers un foyer.json")
    p.add_argument("--bareme", type=str, default=str(DEFAULT_BAREME))
    p.add_argument("--pfu", type=str, default=str(DEFAULT_PFU))
    p.add_argument("--json", action="store_true", help="Sortie JSON")
    args = p.parse_args()

    bareme = load_json(args.bareme)
    pfu_data = load_json(args.pfu) if Path(args.pfu).exists() else None

    if args.foyer:
        if args.situation or args.enfants or args.enfants_alternee or args.parent_isole:
            p.error("--situation, --enfants, --enfants-alternee et --parent-isole ne "
                    "s'emploient pas avec --foyer : la situation se lit dans le fichier")
        foyer = load_json(args.foyer)
        try:
            result = from_foyer(foyer, bareme, pfu_data)
        except ValueError as e:
            p.error(str(e))
    else:
        if args.rni is None:
            p.error("--rni requis sauf si --foyer est utilisé")
        regime = _regime_cli(p, args)
        try:
            result = calc(
                rni=args.rni,
                bareme=bareme,
                rfr=args.rfr,
                base_ps_patrimoine=args.base_ps_patrimoine,
                base_ps_placement=args.base_ps_placement + args.base_ps,
                pfu_data=pfu_data,
                **regime,
            )
        except ValueError as e:
            p.error(str(e))

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        situation = result["situation"] or f"non précisée (parts de base : {result['parts_base']})"
        if result["case_t"]:
            situation += ", case T"
        print()
        print(f"  Situation ....................... {situation}")
        print(f"  RNI ............................. {result['rni']:>10} €")
        print(f"  Parts ........................... {result['parts']:>10}")
        print(f"  Quotient par part ............... {result['quotient_par_part']:>10} €")
        print(f"  Impôt brut (après QF) ........... {result['impot_brut_apres_qf']:>10} €")
        qf = result["qf_details"]
        if qf["gain_qf_reel"]:
            status = "PLAFONNE" if qf["plafonne"] else "non plafonné"
            print(f"    └ gain QF réel / max .......... {qf['gain_qf_reel']:>6} / {qf['gain_qf_max']} € ({status})")
        if qf["reduction_complementaire_veuf"]:
            print(f"    └ réduction complémentaire veuf {-qf['reduction_complementaire_veuf']:>8} € (incluse)")
        print(f"  Décote .......................... {-result['decote']:>10} €")
        print(f"  Impôt après décote .............. {result['impot_apres_decote']:>10} €")
        if result["sous_seuil_recouvrement_61"]:
            seuil = bareme["recouvrement"]["seuil_mise_en_recouvrement"]
            print(f"    └ sous le seuil de mise en recouvrement ({seuil} €) : vérifier après "
                  f"réductions et crédits")
        if result["prelevements_sociaux"]:
            det = result.get("ps_details") or {}
            pat = det.get("patrimoine", {})
            pla = det.get("placement", {})
            if pat.get("base"):
                print(f"  PS {pat['taux']*100:.1f}% revenus patrimoine ...... {pat['montant']:>10} €")
            if pla.get("base"):
                print(f"  PS {pla['taux']*100:.1f}% produits placement ...... {pla['montant']:>10} €")
            print(f"  PS total revenus capital ........ {result['prelevements_sociaux']:>10} €")
        if result["cehr"]:
            print(f"  CEHR ............................ {result['cehr']:>10} €")
        print(f"  ─────────────────────────────────────────────────")
        print(f"  TOTAL (avant réductions/crédits)  {result['total_a_payer']:>10} €")
        print()


if __name__ == "__main__":
    main()
