#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression test: monstercreatorWin — BUG-2251 (Bild zeigt immer Eintrag 0)
+ BUG-2252 (Missile/Magic "add"-Button schreibt nur "0xx") + Default-Werte
(LoadGMTable-Datenvorlage).

Befunde (vor Fix):
- updateWindow() liest das Bild aus ``self.GMcontent[0]`` statt
  ``self.GMcontent[self.__index]`` → beim Wechsel/Neuanlage wird das Bild des
  ERSTEN Eintrags angezeigt, obwohl der aktuelle Eintrag das richtige
  ``piclink`` hat.
- __getOBm() / __getOBmag() rufen ``updateCurrentSet()`` NACH dem Setzen von
  ``currDataSet["OB missile"|"OB magic"]`` auf → ``updateCurrentSet``
  überschreibt den Wert mit dem (leeren) Widget-Variablen-Wert und ersetzt
  diesen bei "" durch den Dummy "0xx".
- loadGMTable() legt die Datenvorlage für neue NSC/Monster komplett leer an;
  die Standardwerte (Level 1, Hits 10, AT 4, Size M, Qu 0, DB mis 0, DB 0,
  enc 1-1) fehlen.

Testet die unbound Methods mit Fake-``StringVar``-Substituten (keine
``tk.Tk()``-Root); PIL/ImageTk werden nur bei updateWindow gemodded, damit
die Bild-Pfad-Auswahl observable bleibt.

Run:  xvfb-run -a python3 gui/test_monstercreator_fixes.py
Exits 0 after fix (GREEN); 1 while the bugs are present (RED).
"""
import os
import sys
from copy import deepcopy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "gui"))

import modules.attackcheck_gui as ac            # noqa: E402  (aus gui/ ein)

W = ac.monstercreatorWin
unbound_obm    = W._monstercreatorWin__getOBm
unbound_obmag  = W._monstercreatorWin__getOBmag
unbound_upwin  = W.updateWindow
unbound_loadgm = W.loadGMTable

# echte GM-Tabelle als FixturesQuelle
GMCSV = os.path.join(ROOT, "data", "default", "nscs", "gamemaster.csv")
PIC_NSC = os.path.join(ROOT, "data", "default", "pics_nsc")


def full_ds(**over):
    """Kompletter NSC-Datensatz (Schema von gamemaster.csv) + Overrides."""
    ds = {
        "category": "Test", "name": "", "lvl": "", "Qu": "", "speed code": "",
        "AT": "", "hits": "", "PP": "", "size": "",
        "OB melee": "", "OB missile": "", "OB magic": "",
        "Primary Attack": "", "Secondary Attack": "", "Tertiary Attack": "",
        "DB": "", "DBm": "", "comment": "", "Notes": "", "enc": "",
        "immune": "", "weakness": "", "piclink": "", "spells": "",
        "climate code": "", "habitat code": "", "frequency of encounter code": "",
        "measurement": "",
    }
    ds.update(over)
    return ds


class Var:
    """Substituiert tk-Var-Widgets: nur .set()/.get()."""

    def __init__(self, value=""):
        self.value = value

    def set(self, v):
        self.value = v

    def get(self):
        return self.value


class FakeComment:
    def get(self, a, b):
        return ""


class FakeLabel:
    def __init__(self):
        self.image = None

    def configure(self, image=None):
        self.image = image


class FakePILImg:
    def resize(self, *a, **k):
        return self


class FakePIL:
    opened = []
    UnidentifiedImageError = type("UnidentifiedImageError", (Exception,), {})

    class Resampling:
        LANCZOS = 1

    @staticmethod
    def open(path):
        FakePIL.opened.append(path)
        return FakePILImg()


class FakeImageTk:
    made = []

    class PhotoImage:
        def __init__(self, img=None):
            FakeImageTk.made.append(img)


class FakeSelf(object):
    """Leere Träger-Klasse: erlaubt freie Set/Read-Attribute (object.__new__
    würde unter Py3.12 setattr blockieren)."""
    pass


def make_obm_self():
    """Fake-self für __getOBm/__getOBmag: Widgets + Datensatz + GMcontent."""
    f = FakeSelf()
    f.currDataSet = full_ds(**{})
    f.GMcontent = [deepcopy(f.currDataSet)]
    f._monstercreatorWin__index = 0          # = self.__index
    f._monstercreatorWin__selectCat = Var("Test")
    f._monstercreatorWin__name = Var("")
    f._monstercreatorWin__lvl = Var("")
    f._monstercreatorWin__hits = Var("")
    f._monstercreatorWin__at = Var("")
    f._monstercreatorWin__size = Var("")
    f._monstercreatorWin__pp = Var("")
    f._monstercreatorWin__qu = Var("")
    f._monstercreatorWin__dbm = Var("")
    f._monstercreatorWin__db = Var("")
    f._monstercreatorWin__obstring = Var("")
    f._monstercreatorWin__magicstring = Var("")
    f._monstercreatorWin__displayComment = FakeComment()
    # Melee-Widgets brauche ich nur, damit updateCurrentSet läuft
    f._monstercreatorWin__obstringmis = Var("")     # leeres Missile-Widget (Neuanlage)
    f._monstercreatorWin__obmval = Var("10")
    f._monstercreatorWin__selectOBmis = Var("Warping")
    f._monstercreatorWin__obstringmagic = Var("")   # leeres Magic-Widget
    f._monstercreatorWin__obmagval = Var("15")
    f._monstercreatorWin__selectOBmagic = Var("Fire Bolt")
    f._monstercreatorWin__attacks = {"Warping": "Wp", "Fire Bolt": "FB"}
    # updateWindow wird im OBm/OBmag-Test nicht gebraucht → No-Op-Recorder
    f._monstercreatorWin__updateWindow_calls = 0
    f.updateWindow = lambda event=None: setattr(
        f, "_monstercreatorWin__updateWindow_calls",
        f._monstercreatorWin__updateWindow_calls + 1)
    # die echte updateCurrentSet braucht diese Extras (rohes object-fake)
    f._monstercreatorWin__enc = Var("")
    f._monstercreatorWin__getComment = lambda event=None: None
    f.updateCurrentSet = lambda event=None: W.updateCurrentSet(f)
    return f


def test_obm_add_button():
    """BUG-2252 (Missile): 'add' muss value+Abkürzung eintragen, nicht '0xx'."""
    f = make_obm_self()
    unbound_obm(f)
    got = f.currDataSet["OB missile"]
    assert got == "10 Wp", (
        f"BUG-2252 MISSILE: erwartet '10 Wp' (value + Abkürzung), got {got!r} — "
        f"Dummy '0xx' kommt von updateCurrentSet() nach dem Setzen")
    # ... und in GMcontent[0] (updateCurrentSet schreibt dorthin) ...
    print("PASS test_obm_add_button: OB missile =", repr(got))


def test_obmag_add_button():
    """BUG-2252 (Magic): gleicher Reihenfolge-Fehler wie Missile-Zeile."""
    f = make_obm_self()
    unbound_obmag(f)
    got = f.currDataSet["OB magic"]
    assert got == "15 FB", (
        f"BUG-2252 MAGIC: erwartet '15 FB' (value + Abkürzung), got {got!r}")
    print("PASS test_obmag_add_button: OB magic =", repr(got))


def make_pic_self():
    """Fake-self für updateWindow() mit zwei Einträgen, index=1."""
    f = FakeSelf()
    pic0 = os.path.join(PIC_NSC, "first.jpg")
    pic1 = os.path.join(PIC_NSC, "second.jpg")
    f.GMcontent = [full_ds(name="Eins", piclink=pic0),
                   full_ds(name="Zwei", piclink=pic1)]
    f.currDataSet = deepcopy(f.GMcontent[1])
    f._monstercreatorWin__index = 1           # = self.__index (zweiter Eintrag)
    f.NPCcat = ["Test"]
    f.selectedPic = None
    f.picLabel = FakeLabel()
    for attr, key in [
        ("selectCat", "category"), ("name", "name"), ("lvl", "lvl"),
        ("hits", "hits"), ("at", "AT"), ("size", "size"), ("pp", "PP"),
        ("qu", "Qu"), ("dbm", "DBm"), ("db", "DB"),
        ("obstring", "OB melee"), ("obstringmis", "OB missile"),
        ("obstringmagic", "OB magic"), ("magicstring", "spells"), ("enc", "enc"),
    ]:
        setattr(f, f"_monstercreatorWin__{attr}", Var())
    f._monstercreatorWin__LabelImunities = type("L", (), {"config": lambda s, **k: None})()
    f._monstercreatorWin__LabelWeaknesses = f._monstercreatorWin__LabelImunities
    f._monstercreatorWin__displayComment = FakeComment()
    f._monstercreatorWin__insertComment = lambda event=None: None
    return f, pic0, pic1


def test_update_window_pic_index():
    """BUG-2251: updateWindow muss das Bild des AKTUELLEN Eintrags laden."""
    f, pic0, pic1 = make_pic_self()
    # PIL/ImageTk modden, damit die Pfad-Auswahl observable bleibt
    real_pil, real_tk = ac._pilimg, ac.ImageTk
    FakePIL.opened.clear()
    FakeImageTk.made.clear()
    ac._pilimg, ac.ImageTk = FakePIL, FakeImageTk
    try:
        unbound_upwin(f)
    finally:
        ac._pilimg, ac.ImageTk = real_pil, real_tk
    assert FakePIL.opened, "updateWindow hat kein Bild geöffnet"
    got = FakePIL.opened[-1]
    assert got == pic1, (
        f"BUG-2251: erwartet Bild des aktuellen Eintrags {pic1!r}, "
        f"geöffnet wurde {got!r} (immer der erste GMcontent[0])")
    print("PASS test_update_window_pic_index: geöffnet =", got)


def test_new_element_defaults():
    """Verbesserung 2253: Datenvorlage trägt die User-Standardwerte."""
    f = FakeSelf()
    f.GMtable = GMCSV
    f.nscpicpath = PIC_NSC + "/"
    unbound_loadgm(f)
    tpl = f._monstercreatorWin__datatemplate
    expect = {"lvl": "1", "hits": "10", "AT": "4", "size": "M",
              "Qu": "0", "DBm": "0", "DB": "0", "enc": "1-1"}
    bad = {k: (tpl.get(k), v) for k, v in expect.items() if tpl.get(k) != v}
    assert not bad, f"BUG/2253: Template-Standardwerte fehlen/abweichend: {bad}"
    assert tpl.get("piclink", "").endswith("default.jpg"), (
        f"piclink-Default fehlt: {tpl.get('piclink')!r}")
    print("PASS test_new_element_defaults: Standardwerte im Template gesetzt")


def main():
    tests = [test_obm_add_button, test_obmag_add_button,
             test_update_window_pic_index, test_new_element_defaults]
    failures = 0
    for t in tests:
        try:
            t()
        except AssertionError as e:
            failures += 1
            print("FAIL", t.__name__, "::", e)
        except Exception as e:           # noqa: BLE001 — Test-Meldung, kein Stopp
            failures += 1
            print("ERROR", t.__name__, "::", type(e).__name__, e)
    if failures:
        print(f"RESULT: {failures}/{len(tests)} FEHLGESCHLAGEN (RED)")
        return 1
    print(f"RESULT: {len(tests)}/{len(tests)} PASS (GREEN)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
