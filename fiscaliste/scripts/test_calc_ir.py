#!/usr/bin/env python3
"""
Tests de calc_ir.py (revenus 2025, déclaration 2026).

Lancement, depuis fiscaliste/scripts :
    python3 -m unittest
    python3 -m unittest -v test_calc_ir

Le module testé se choisit par la variable d'environnement CALC_IR_CHEMIN
(défaut : calc_ir.py du même dossier). Exemple, pour la preuve d'échec sur une
copie de l'ancien script :
    CALC_IR_CHEMIN=/chemin/vers/calc_ir.orig.py python3 -m unittest -v

Les barèmes sont toujours passés explicitement (--bareme, --pfu, et en argument
des fonctions) : une copie du script placée ailleurs ne retrouverait pas data/.

Les identifiants T1-a ... T8-c renvoient à la spécification (spec-calc_ir.txt).
Les montants d'impôt attendus sont arrondis à l'euro (ROUND_HALF_UP).
"""

import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE_SKILL = ICI.parent
DATA = RACINE_SKILL / "data"
EXEMPLES = RACINE_SKILL / "examples"
FOYER_EXEMPLE = RACINE_SKILL / "foyer.example.json"
BAREME_CHEMIN = DATA / "bareme-ir-2025.json"
PFU_CHEMIN = DATA / "pfu-prelevements-sociaux.json"
CHEMIN = Path(os.environ.get("CALC_IR_CHEMIN", str(ICI / "calc_ir.py"))).resolve()


def _charger_module(chemin):
    spec = importlib.util.spec_from_file_location("calc_ir_sous_test", str(chemin))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


calc_ir = _charger_module(CHEMIN)
BAREME = json.loads(BAREME_CHEMIN.read_text(encoding="utf-8"))
PFU = json.loads(PFU_CHEMIN.read_text(encoding="utf-8"))

MSG_CHOMAGE_COUPLE = (
    "revenus_chomage non ventilé : pour un couple, renseigner "
    "revenus_chomage_declarant1 (case 1AP) et/ou revenus_chomage_declarant2 "
    "(case 1BP). La déduction de 10 % se calcule par bénéficiaire "
    "(BOI-RSA-BASE-30-50-20, § 80 et § 210)."
)
MSG_CASE_T = (
    "case T réservée aux célibataires, divorcés ou séparés vivant seuls avec au "
    "moins un enfant à charge (art. 194 II CGI)"
)
MSG_CEHR_DECES = (
    "CEHR de l'année du décès non calculée : assiette scindée avant et après "
    "décès (BOI-IR-CHR § 100)"
)
MSG_NON_GERE = "cas non géré par calc_ir.py"
MSG_AVERTISSEMENT_BASE_1 = (
    "mode --parts-base 1 : ni case T ni veuf pris en compte, utiliser --situation"
)


def foyer(situation, revenus=None, deductions=None, **champs_foyer):
    """Construit un foyer.json minimal."""
    f = {"situation": situation}
    f.update(champs_foyer)
    return {"foyer": f, "revenus": dict(revenus or {}), "deductions": dict(deductions or {})}


def calcul_foyer(f):
    return calc_ir.from_foyer(f, BAREME, PFU)


def cli(*args):
    """Lance le script testé en sous-processus avec les barèmes explicites."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(
        [sys.executable, str(CHEMIN), "--bareme", str(BAREME_CHEMIN),
         "--pfu", str(PFU_CHEMIN), *[str(a) for a in args]],
        capture_output=True, text=True, encoding="utf-8", env=env, timeout=60,
    )


class CasCli(unittest.TestCase):
    def cli_json(self, *args):
        res = cli(*args, "--json")
        self.assertEqual(res.returncode, 0,
                         "code %s, stderr : %s" % (res.returncode, res.stderr.strip()))
        return json.loads(res.stdout)

    def cli_refus(self, message, *args):
        res = cli(*args)
        self.assertEqual(res.returncode, 2,
                         "code %s attendu 2, stdout : %s" % (res.returncode, res.stdout.strip()))
        self.assertIn(message, res.stderr)
        return res


# ─────────────────────────────────────────────────────
# calc-ir-code-1 : déduction de 10 % par membre du foyer
# ─────────────────────────────────────────────────────

class TestT1AbattementSalairesParMembre(unittest.TestCase):

    def test_T1a_marie_200000_100000(self):
        r = calcul_foyer(foyer("marie", {"salaires_declarant1": 200000,
                                         "salaires_declarant2": 100000}))
        self.assertEqual(r["rni"], 275445)
        self.assertEqual(r["impot_apres_decote"], 80533)

    def test_T1b_marie_50000_3000_decote_couple(self):
        r = calcul_foyer(foyer("marie", {"salaires_declarant1": 50000,
                                         "salaires_declarant2": 3000}))
        self.assertEqual(r["rni"], 47491)
        self.assertEqual(r["impot_brut_apres_qf"], 2672)
        self.assertEqual(r["impot_apres_decote"], 2398)

    def test_T1c_marie_are_ventilee_declarant2(self):
        r = calcul_foyer(foyer("marie", {"salaires_declarant1": 150000,
                                         "revenus_chomage_declarant2": 20000}))
        self.assertEqual(r["rni"], 153445)
        self.assertEqual(r["impot_apres_decote"], 32241)

    def test_T1c_marie_are_non_ventilee_refusee(self):
        for situation in ("marie", "pacse"):
            with self.subTest(situation=situation):
                f = foyer(situation, {"salaires_declarant1": 150000,
                                      "revenus_chomage": 20000})
                with self.assertRaises(ValueError) as ctx:
                    calcul_foyer(f)
                self.assertEqual(str(ctx.exception), MSG_CHOMAGE_COUPLE)

    def test_T1d_nominal_celibataire(self):
        r = calcul_foyer(foyer("celibataire", {"salaires_declarant1": 30000}))
        self.assertEqual(r["rni"], 27000)
        r = calcul_foyer(foyer("celibataire", {"revenus_chomage": 18000}))
        self.assertEqual(r["rni"], 16200)
        self.assertEqual(r["impot_apres_decote"], 0)

    def test_T1e_exemple_foyer_ifi_cehr(self):
        f = json.loads((EXEMPLES / "foyer-ifi-cehr.json").read_text(encoding="utf-8"))
        r = calcul_foyer(f)
        self.assertEqual(r["rni"], 435890)
        self.assertEqual(r["impot_apres_decote"], 149198)
        self.assertEqual(r["cehr"], 267)

    def test_nominal_couple_revenus_chomage_historique_nul_accepte(self):
        # Précision (a) de la contre-vérification : un foyer.json de couple copié
        # de l'ancien modèle ("revenus_chomage": 0) reste utilisable.
        r = calcul_foyer(foyer("marie", {"salaires_declarant1": 30000,
                                         "revenus_chomage": 0}))
        self.assertEqual(r["rni"], 27000)

    def test_nominal_revenus_chomage_historique_survivant_annee_deces(self):
        # Précision (b) : un seul déclarant, champ historique rattaché au déclarant 1.
        r = calcul_foyer(foyer("veuf_annee_deces", {"revenus_chomage": 18000}))
        self.assertEqual(r["rni"], 16200)

    def test_revenus_chomage_historique_et_ventile_refuses(self):
        f = foyer("celibataire", {"revenus_chomage": 1000,
                                  "revenus_chomage_declarant1": 1000})
        with self.assertRaisesRegex(ValueError, "^revenus_chomage non ventilé"):
            calcul_foyer(f)


# ─────────────────────────────────────────────────────
# calc-ir-code-2 et 2v : abattements bornés au brut, pensions par pensionné
# ─────────────────────────────────────────────────────

class TestT2AbattementsBornesEtPensions(unittest.TestCase):

    def test_T2a_salaire_300_net_nul(self):
        self.assertEqual(calc_ir.abattement_salaires(300, BAREME), 0)
        r = calcul_foyer(foyer("celibataire", {"salaires_declarant1": 300,
                                               "revenus_fonciers_micro": 30000}))
        self.assertEqual(r["rni"], 30000)
        self.assertEqual(r["impot_apres_decote"], 2104)

    def test_T2b_pension_300_net_nulle(self):
        r = calcul_foyer(foyer("celibataire", {"pensions_declarant1": 300,
                                               "revenus_fonciers_micro": 30000}))
        self.assertEqual(r["rni"], 30000)
        self.assertEqual(r["impot_apres_decote"], 2104)

    def test_T2c_minimum_par_pensionne(self):
        r = calcul_foyer(foyer("marie", {"pensions_declarant1": 30000,
                                         "pensions_declarant2": 3000,
                                         "revenus_fonciers_micro": 30000}))
        self.assertEqual(r["rni"], 59546)
        self.assertEqual(r["impot_apres_decote"], 4072)

    def test_T2d_nominal_plafond_foyer(self):
        r = calcul_foyer(foyer("marie", {"pensions_declarant1": 40000,
                                         "pensions_declarant2": 40000}))
        self.assertEqual(r["rni"], 75561)
        self.assertEqual(r["impot_apres_decote"], 8876)


# ─────────────────────────────────────────────────────
# calc-ir-code-3 : CLI, parts de base selon la situation
# ─────────────────────────────────────────────────────

class TestT3SituationCli(CasCli):

    def test_T3a_parts_2_sans_situation_ambigu(self):
        self.cli_refus("situation ambiguë", "--rni", 60000, "--parts", 2)

    def test_T3b_case_t_1_enfant(self):
        r = self.cli_json("--rni", 60000, "--situation", "celibataire",
                          "--enfants", 1, "--parent-isole")
        self.assertEqual(r["parts"], 2)
        self.assertEqual(r["qf_details"]["gain_qf_max"], 4262)
        self.assertEqual(r["impot_apres_decote"], 6842)

    def test_T3c_case_t_2_enfants(self):
        r = self.cli_json("--rni", 80000, "--situation", "celibataire",
                          "--enfants", 2, "--parent-isole")
        self.assertEqual(r["parts"], 2.5)
        self.assertEqual(r["qf_details"]["gain_qf_max"], 6069)
        self.assertEqual(r["impot_apres_decote"], 11035)

    def test_T3d_nominal_mode_historique(self):
        r = self.cli_json("--rni", 40000, "--parts", 1.5, "--parts-base", 1)
        self.assertEqual(r["impot_apres_decote"], 3297)
        r = self.cli_json("--rni", 126000, "--parts", 3, "--parts-base", 2)
        self.assertEqual(r["impot_apres_decote"], 20394)
        r = self.cli_json("--rni", 45000, "--parts", 1)
        self.assertEqual(r["impot_apres_decote"], 6604)

    def test_parts_incoherentes(self):
        self.cli_refus("parts incohérentes : 2 calculées pour la situation, 1.5 fournies",
                       "--rni", 60000, "--situation", "celibataire", "--enfants", 1,
                       "--parent-isole", "--parts", 1.5)

    def test_parts_coherentes_acceptees(self):
        r = self.cli_json("--rni", 60000, "--situation", "celibataire", "--enfants", 1,
                          "--parent-isole", "--parts", 2)
        self.assertEqual(r["impot_apres_decote"], 6842)

    def test_avertissement_parts_base_1(self):
        res = cli("--rni", 40000, "--parts", 1.5, "--parts-base", 1)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn(MSG_AVERTISSEMENT_BASE_1, res.stderr)

    def test_options_famille_sans_situation_refusees(self):
        self.cli_refus("exigent --situation",
                       "--rni", 60000, "--parts", 2, "--parts-base", 1, "--parent-isole")

    def test_case_t_hors_situation_refusee_en_cli(self):
        self.cli_refus(MSG_CASE_T, "--rni", 60000, "--situation", "marie",
                       "--enfants", 1, "--parent-isole")


# ─────────────────────────────────────────────────────
# calc-ir-code-4a : case T
# ─────────────────────────────────────────────────────

class TestT4aCaseT(unittest.TestCase):

    def test_T4a1_case_t_1_enfant(self):
        r = calcul_foyer(foyer("celibataire", {"revenus_fonciers_micro": 60000},
                               parent_isole=True, nb_enfants_charge=1))
        self.assertEqual(r["parts"], 2)
        self.assertEqual(r["impot_apres_decote"], 6842)

    def test_T4a2_case_t_2_enfants(self):
        r = calcul_foyer(foyer("celibataire", {"revenus_fonciers_micro": 80000},
                               parent_isole=True, nb_enfants_charge=2))
        self.assertEqual(r["parts"], 2.5)
        self.assertEqual(r["qf_details"]["gain_qf_max"], 6069)
        self.assertEqual(r["impot_apres_decote"], 11035)

    def test_T4a3_case_t_2_enfants_alternance_seule(self):
        r = calcul_foyer(foyer("celibataire", {"revenus_fonciers_micro": 60000},
                               parent_isole=True, nb_enfants_alternee=2))
        self.assertEqual(r["parts"], 2)
        self.assertEqual(r["qf_details"]["gain_qf_max"], 4262)
        self.assertEqual(r["impot_apres_decote"], 6842)

    def test_case_t_un_seul_enfant_alterne_plafond_2131(self):
        # Contre-vérification de calc-ir-code-3 : case T avec un seul enfant en
        # alternance, 1,5 part, B = 2 131 (et non 1 807).
        r = calcul_foyer(foyer("celibataire", {"revenus_fonciers_micro": 60000},
                               parent_isole=True, nb_enfants_alternee=1))
        self.assertEqual(r["parts"], 1.5)
        self.assertEqual(r["qf_details"]["gain_qf_max"], 2131)

    def test_T4a4_nominal_sans_case_t(self):
        r = calcul_foyer(foyer("celibataire", {"revenus_fonciers_micro": 40000},
                               parent_isole=False, nb_enfants_charge=1))
        self.assertEqual(r["parts"], 1.5)
        self.assertEqual(r["impot_apres_decote"], 3297)


# ─────────────────────────────────────────────────────
# calc-ir-code-4b : veuf, année du décès, situations inconnues
# ─────────────────────────────────────────────────────

class TestT4bVeuf(unittest.TestCase):

    def test_T4b1_veuf_1_enfant(self):
        r = calcul_foyer(foyer("veuf", {"revenus_fonciers_micro": 70000},
                               nb_enfants_charge=1))
        self.assertEqual(r["parts"], 2.5)
        self.assertEqual(r["qf_details"]["gain_qf_max"], 5421)
        self.assertEqual(r["qf_details"]["reduction_complementaire_veuf"], 2011)
        self.assertEqual(r["impot_apres_decote"], 6672)

    def test_T4b2_veuf_2_enfants(self):
        r = calcul_foyer(foyer("veuf", {"revenus_fonciers_micro": 90000},
                               nb_enfants_charge=2))
        self.assertEqual(r["parts"], 3)
        self.assertEqual(r["qf_details"]["gain_qf_max"], 7228)
        self.assertEqual(r["qf_details"]["reduction_complementaire_veuf"], 2011)
        self.assertEqual(r["impot_apres_decote"], 11462)

    def test_T4b3_survivant_annee_deces_60000(self):
        r = calcul_foyer(foyer("veuf_annee_deces", {"revenus_fonciers_micro": 60000}))
        self.assertEqual(r["parts"], 2)
        self.assertEqual(r["qf_details"]["reduction_complementaire_veuf"], 0)
        self.assertEqual(r["impot_apres_decote"], 4208)

    def test_T4b4_enfant_invalide_refuse(self):
        f = foyer("marie", {"revenus_fonciers_micro": 60000},
                  nb_enfants_charge=1, nb_enfants_invalides=1)
        with self.assertRaisesRegex(ValueError, MSG_NON_GERE):
            calcul_foyer(f)

    def test_T4b4_situation_concubin_refusee(self):
        f = foyer("concubin", {"revenus_fonciers_micro": 60000})
        with self.assertRaisesRegex(ValueError, "situation inconnue : concubin"):
            calcul_foyer(f)

    def test_T4b5_nominal_veuf_sans_enfant(self):
        r = calcul_foyer(foyer("veuf", {"revenus_fonciers_micro": 40000}))
        self.assertEqual(r["parts"], 1)
        self.assertEqual(r["impot_apres_decote"], 5104)

    def test_survivant_annee_deces_sans_reduction_complementaire(self):
        # Contre-vérification de calc-ir-code-4b : survivant l'année du décès, A sur
        # 2 parts, B = 1 807 € par demi-part au-delà de 2 parts, H = 0. Aucun témoin
        # chiffré de la spec : contrôle structurel quand le plafonnement joue.
        r = calcul_foyer(foyer("veuf_annee_deces", {"revenus_fonciers_micro": 100000},
                               nb_enfants_charge=1))
        qf = r["qf_details"]
        self.assertEqual(r["parts"], 2.5)
        self.assertTrue(qf["plafonne"])
        self.assertEqual(qf["gain_qf_max"], 1807)
        self.assertEqual(qf["reduction_complementaire_veuf"], 0)
        self.assertEqual(r["impot_brut_apres_qf"],
                         qf["impot_reference_parts_base"] - qf["gain_qf_max"])

    def test_T4b6_survivant_annee_deces_decote_personne_seule(self):
        r = calcul_foyer(foyer("veuf_annee_deces", {"revenus_fonciers_micro": 30000}))
        self.assertEqual(r["parts"], 2)
        self.assertEqual(r["impot_apres_decote"], 189)


# ─────────────────────────────────────────────────────
# calc-ir-code-5 : décote selon la situation
# ─────────────────────────────────────────────────────

class TestT5Decote(CasCli):

    def test_T5a_case_t_decote_personne_seule(self):
        r = self.cli_json("--rni", 30000, "--situation", "celibataire",
                          "--enfants", 1, "--parent-isole")
        self.assertEqual(r["impot_apres_decote"], 189)

    def test_T5b_veuf_decote_personne_seule(self):
        r = self.cli_json("--rni", 45000, "--situation", "veuf", "--enfants", 1)
        self.assertEqual(r["parts"], 2.5)
        self.assertEqual(r["impot_apres_decote"], 1659)

    def test_T5c_nominal_couple_mode_historique(self):
        r = self.cli_json("--rni", 30000, "--parts", 2, "--parts-base", 2)
        self.assertEqual(r["impot_apres_decote"], 0)

    def test_T5c_couple_par_situation(self):
        r = self.cli_json("--rni", 30000, "--situation", "marie")
        self.assertEqual(r["impot_apres_decote"], 0)

    def test_T5d_survivant_annee_deces_cli(self):
        r = self.cli_json("--rni", 30000, "--situation", "veuf_annee_deces")
        self.assertEqual(r["parts"], 2)
        self.assertEqual(r["impot_apres_decote"], 189)


# ─────────────────────────────────────────────────────
# calc-ir-code-6 : CEHR selon la situation
# ─────────────────────────────────────────────────────

class TestT6Cehr(CasCli):

    def test_T6a_case_t_seuils_personne_seule(self):
        r = self.cli_json("--rni", 300000, "--rfr", 300000, "--situation", "celibataire",
                          "--enfants", 1, "--parent-isole")
        self.assertEqual(r["cehr"], 1500)
        self.assertEqual(r["impot_apres_decote"], 107262)
        self.assertEqual(r["total_a_payer"], 108762)

    def test_T6b_garde_fou_veuf_cli(self):
        r = self.cli_json("--rni", 300000, "--rfr", 300000, "--situation", "veuf",
                          "--enfants", 1)
        self.assertEqual(r["cehr"], 1500)
        self.assertEqual(r["qf_details"]["reduction_complementaire_veuf"], 2011)
        self.assertEqual(r["impot_apres_decote"], 104092)

    def test_T6b_garde_fou_veuf_foyer_cehr(self):
        # Juste par accident sur l'ancien code (parts_base 1 pour le veuf) : doit le
        # rester quand le veuf reçoit 2,5 parts.
        r = calcul_foyer(foyer("veuf", {"revenus_fonciers_micro": 300000},
                               nb_enfants_charge=1))
        self.assertEqual(r["cehr"], 1500)

    def test_T6b_garde_fou_veuf_foyer_impot(self):
        r = calcul_foyer(foyer("veuf", {"revenus_fonciers_micro": 300000},
                               nb_enfants_charge=1))
        self.assertEqual(r["impot_apres_decote"], 104092)

    def test_T6c_nominal_couple_mode_historique(self):
        r = self.cli_json("--rni", 600000, "--rfr", 600000, "--parts", 2, "--parts-base", 2)
        self.assertEqual(r["cehr"], 3000)
        self.assertEqual(r["impot_apres_decote"], 223048)

    def test_T6c_couple_par_situation(self):
        r = self.cli_json("--rni", 600000, "--rfr", 600000, "--situation", "marie")
        self.assertEqual(r["cehr"], 3000)
        self.assertEqual(r["impot_apres_decote"], 223048)

    def test_cehr_annee_deces_refusee_cli(self):
        self.cli_refus(MSG_CEHR_DECES, "--rni", 300000, "--rfr", 300000,
                       "--situation", "veuf_annee_deces")

    def test_cehr_annee_deces_refusee_foyer(self):
        f = foyer("veuf_annee_deces", {"revenus_fonciers_micro": 300000})
        with self.assertRaises(ValueError) as ctx:
            calcul_foyer(f)
        self.assertEqual(str(ctx.exception), MSG_CEHR_DECES)


# ─────────────────────────────────────────────────────
# calc-ir-code-7 : rang des enfants en résidence alternée
# ─────────────────────────────────────────────────────

class TestT7ResidenceAlternee(unittest.TestCase):

    def _couple(self, enfants, alternee):
        return calcul_foyer(foyer("marie", {"salaires_declarant1": 100000},
                                  nb_enfants_charge=enfants, nb_enfants_alternee=alternee))

    def test_T7a_2_exclusifs_1_alterne(self):
        r = self._couple(2, 1)
        self.assertEqual(r["rni"], 90000)
        self.assertEqual(r["parts"], 3.5)
        self.assertEqual(r["qf_details"]["gain_qf_max"], 5421)
        self.assertEqual(r["impot_apres_decote"], 7787)

    def test_T7b_1_exclusif_2_alternes(self):
        r = self._couple(1, 2)
        self.assertEqual(r["parts"], 3.25)
        self.assertEqual(r["qf_details"]["gain_qf_max"], 4517.5)
        self.assertEqual(r["impot_apres_decote"], 8690)

    def test_T7c_nominal_0_exclusif_2_alternes(self):
        r = self._couple(0, 2)
        self.assertEqual(r["parts"], 2.5)
        self.assertEqual(r["impot_apres_decote"], 11401)


# ─────────────────────────────────────────────────────
# calc-ir-code-8 : arrondi à l'euro, seuil de recouvrement
# ─────────────────────────────────────────────────────

class TestT8Arrondi(CasCli):

    def test_T8a_impot_arrondi_a_l_euro(self):
        r = self.cli_json("--rni", 27000, "--parts", 1)
        self.assertEqual(r["impot_apres_decote"], 1564)

    def test_T8b_demi_euro_compte_pour_un(self):
        self.assertEqual(calc_ir.arrondi_euro(1596.5), 1597)

    def test_T8c_nominal_exemples_brochure(self):
        self.assertEqual(calc_ir.arrondi_euro(1597.30), 1597)
        self.assertEqual(calc_ir.arrondi_euro(1597.50), 1598)
        self.assertEqual(calc_ir.arrondi_euro(1597.75), 1598)

    def test_champ_sous_seuil_recouvrement_61(self):
        r = self.cli_json("--rni", 17418, "--parts", 1)
        self.assertTrue(0 < r["impot_apres_decote"] < 61, r["impot_apres_decote"])
        self.assertIs(r["sous_seuil_recouvrement_61"], True)
        r = self.cli_json("--rni", 27000, "--parts", 1)
        self.assertIs(r["sous_seuil_recouvrement_61"], False)
        r = self.cli_json("--rni", 13000, "--parts", 1)
        self.assertEqual(r["impot_apres_decote"], 0)
        self.assertIs(r["sous_seuil_recouvrement_61"], False)


# ─────────────────────────────────────────────────────
# Refus explicites des cas non gérés
# ─────────────────────────────────────────────────────

class TestRefusExplicites(unittest.TestCase):

    def test_cases_non_gerees(self):
        for case in ("case_l", "case_p", "case_f", "case_w", "case_s", "case_g"):
            with self.subTest(case=case):
                f = foyer("celibataire", {"revenus_fonciers_micro": 40000}, **{case: True})
                with self.assertRaisesRegex(ValueError, MSG_NON_GERE):
                    calcul_foyer(f)

    def test_case_t_hors_celibataire_divorce_separe(self):
        for situation in ("marie", "pacse", "veuf", "veuf_annee_deces"):
            with self.subTest(situation=situation):
                f = foyer(situation, {"revenus_fonciers_micro": 40000},
                          parent_isole=True, nb_enfants_charge=1)
                with self.assertRaises(ValueError) as ctx:
                    calcul_foyer(f)
                self.assertEqual(str(ctx.exception), MSG_CASE_T)

    def test_case_t_sans_enfant(self):
        f = foyer("divorce", {"revenus_fonciers_micro": 40000}, parent_isole=True)
        with self.assertRaises(ValueError) as ctx:
            calcul_foyer(f)
        self.assertEqual(str(ctx.exception), MSG_CASE_T)

    def test_case_t_acceptee_pour_divorce_et_separe(self):
        for situation in ("divorce", "separe"):
            with self.subTest(situation=situation):
                r = calcul_foyer(foyer(situation, {"revenus_fonciers_micro": 60000},
                                       parent_isole=True, nb_enfants_charge=1))
                self.assertEqual(r["impot_apres_decote"], 6842)

    def test_veuf_enfants_uniquement_en_alternance(self):
        f = foyer("veuf", {"revenus_fonciers_micro": 40000}, nb_enfants_alternee=1)
        with self.assertRaisesRegex(ValueError, MSG_NON_GERE):
            calcul_foyer(f)

    def test_veuf_avec_enfant_en_alternance_refuse_foyer(self):
        # Refusé quel que soit le nombre d'enfants à charge exclusive (règle non vérifiée).
        for enfants in (0, 1, 2):
            with self.subTest(nb_enfants_charge=enfants):
                f = foyer("veuf", {"revenus_fonciers_micro": 70000},
                          nb_enfants_charge=enfants, nb_enfants_alternee=1)
                with self.assertRaisesRegex(ValueError, "^" + MSG_NON_GERE + " : veuf .*"
                                            "; calculer avec la fiche 2041 ou le simulateur "
                                            "impots.gouv.fr$"):
                    calcul_foyer(f)

    def test_veuf_avec_enfant_en_alternance_refuse_cli(self):
        res = cli("--rni", 70000, "--situation", "veuf", "--enfants", 1,
                  "--enfants-alternee", 1)
        self.assertEqual(res.returncode, 2, res.stdout)
        self.assertIn(MSG_NON_GERE + " : veuf", res.stderr)

    def test_survivant_annee_deces_avec_enfant_en_alternance_refuse_foyer(self):
        for enfants in (0, 1):
            with self.subTest(nb_enfants_charge=enfants):
                f = foyer("veuf_annee_deces", {"revenus_fonciers_micro": 60000},
                          nb_enfants_charge=enfants, nb_enfants_alternee=1)
                with self.assertRaisesRegex(ValueError, "^" + MSG_NON_GERE + " : .*veuf_annee_deces"
                                            ".*; calculer avec la fiche 2041 ou le simulateur "
                                            "impots.gouv.fr$"):
                    calcul_foyer(f)

    def test_survivant_annee_deces_avec_enfant_en_alternance_refuse_cli(self):
        res = cli("--rni", 60000, "--situation", "veuf_annee_deces", "--enfants-alternee", 1)
        self.assertEqual(res.returncode, 2, res.stdout)
        self.assertIn(MSG_NON_GERE, res.stderr)
        self.assertIn("veuf_annee_deces", res.stderr)

    def test_revenus_chomage_non_ventile_cli(self):
        f = foyer("pacse", {"salaires_declarant1": 30000, "revenus_chomage": 5000})
        with tempfile.TemporaryDirectory() as dossier:
            chemin = Path(dossier) / "foyer.json"
            chemin.write_text(json.dumps(f, ensure_ascii=False), encoding="utf-8")
            res = cli("--foyer", chemin)
        self.assertEqual(res.returncode, 2, res.stdout)
        self.assertIn("revenus_chomage non ventilé", res.stderr)


# ─────────────────────────────────────────────────────
# Lots associés intégrés au script (items-calc_ir.txt)
# ─────────────────────────────────────────────────────

def _arrondi(x):
    return int(Decimal(str(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


class TestLotsAssocies(unittest.TestCase):

    def test_non_resident_sans_ps(self):
        # pfu-calc-non-resident-1 : pas de PS sur dividendes, intérêts, PV, crypto.
        f = json.loads((EXEMPLES / "foyer-expatrie-non-resident.json").read_text(encoding="utf-8"))
        r = calcul_foyer(f)
        self.assertEqual(r["prelevements_sociaux"], 0)

    def test_resident_ps_produits_de_placement(self):
        f = json.loads((EXEMPLES / "foyer-expatrie-non-resident.json").read_text(encoding="utf-8"))
        f = copy.deepcopy(f)
        f["foyer"]["residence_fiscale"] = "FR"
        r = calcul_foyer(f)
        taux = PFU["prelevements_sociaux"]["taux_produits_de_placement_2025"]["valeur"]
        self.assertEqual(r["prelevements_sociaux"], _arrondi(Decimal("12000") * Decimal(str(taux))))

    def test_rcm_sans_ps_a_la_source_base_patrimoine(self):
        # pfu-ps-rcm-2025-1 : la part des RCM sans PS au versement passe à 18,6 %.
        r = calcul_foyer(foyer("celibataire", {"salaires_declarant1": 30000,
                                               "dividendes_bruts": 1000,
                                               "rcm_sans_ps_a_la_source": 400}))
        self.assertEqual(r["ps_details"]["placement"]["base"], 600)
        self.assertEqual(r["ps_details"]["patrimoine"]["base"], 400)


# ─────────────────────────────────────────────────────
# Exemples livrés : exécution sans erreur
# ─────────────────────────────────────────────────────

class TestExemples(unittest.TestCase):

    def test_foyers_livres_s_executent(self):
        fichiers = [FOYER_EXEMPLE] + sorted(EXEMPLES.glob("*.json"))
        self.assertGreater(len(fichiers), 1)
        for chemin in fichiers:
            contenu = json.loads(chemin.read_text(encoding="utf-8"))
            if "foyer" not in contenu or "revenus" not in contenu:
                continue
            with self.subTest(fichier=chemin.name):
                res = cli("--foyer", chemin, "--json")
                self.assertEqual(res.returncode, 0, res.stderr)
                json.loads(res.stdout)
                res = cli("--foyer", chemin)
                self.assertEqual(res.returncode, 0, res.stderr)


if __name__ == "__main__":
    unittest.main()
