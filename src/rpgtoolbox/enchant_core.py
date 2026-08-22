#!/usr/bin/env python3
"""Enchantment-Logik: Zauber-Berechnung, Gewichtsmultiplikatoren, Kosten."""
from rpgToolDefinitions.inventory import coins

BONUS_MULT = {0:1, 5:10, 10:50, 15:250, 20:1000, 25:5000}

def calc_bonus_multiplier(bonus_choice):
    return BONUS_MULT.get(int(bonus_choice), 1)

def calc_weight_mult(weight_choice):
    if not isinstance(weight_choice, (int, float)):
        return 1
    w = int(weight_choice)
    if 79 < w < 100: return 10
    elif 59 < w < 80: return 50
    elif 39 < w < 60: return 100
    return 1

def calc_enchant_cost(base_worth, bonus_choice=0, weight_choice=100):
    bm = calc_bonus_multiplier(bonus_choice)
    wm = calc_weight_mult(weight_choice)
    return {k: v * bm * wm for k,v in base_worth.items()}

def worth_to_string(worth_dict):
    r = ""
    for key in coins["long"]:
        val = worth_dict.get(key, 0)
        if isinstance(val, (int,float)) and val > 0:
            r += f"{val}{key[0]}p "
    return r.strip()

def process_enchantment(char_inv, shoptype, elem_idx, item_dict, purse, bonus_pct, weight_pct, enchant_type="charged magic item", spell=None, description=""):
    """Core-Funktion: Zauberei + Zahlung (ersetzt payEnchantment+getBonusItem)."""
    # Schritt 1: Kosten berechnen
    original_worth = char_inv[shoptype][elem_idx]["worth"]
    bonus_mult = calc_bonus_multiplier(bonus_pct)
    weight_mult = calc_weight_mult(weight_pct)
    enchanted_worth = {k: v * bonus_mult * weight_mult for k,v in original_worth.items()}
    
    # Schritt 2: Zahlung verarbeiten (buyStuff-Äquivalent)
    clong = list(coins["long"])
    cshort = [c.upper() for c in coins["short"]]
    
    purse_total = sum(purse[c.upper()] * (10**i) for i,c in enumerate(cshort))
    worth_total = sum(enchanted_worth.get(k,0) * (10**i) for i,k in enumerate(clong))
    
    if worth_total > purse_total:
        return {"success": False, "msg": "Nicht genug Geld"}
    
    # Schritt 3: Zauber-Effekte anwenden
    new_item = item_dict.copy()
    new_item["magic"] = True
    new_item["worth"] = enchanted_worth
    
    if enchant_type == "magic bonus item":
        new_item["bonus"] = int(new_item.get("bonus",0)) + int(bonus_pct)
        new_item["skill"] = description
        desc = f"; magic bonus (+{int(bonus_pct)})"
        if weight_mult > 1:
            desc += f"; magic weight reduced ({int(weight_pct)}%)"
        new_item["description"] = item_dict.get("description","") + desc
        # Gewicht anpassen
        old_wt = float(new_item.get("weight",0))
        new_item["weight"] = round(old_wt * 100.0 / weight_mult, 2) if weight_mult > 1 else old_wt
    
    elif enchant_type == "charged magic item":
        parts = spell.split("|") if isinstance(spell, str) and "|" in spell else [spell or "", str(new_item.get("spell_lvl",1))]
        new_item["type"] = parts[0] if len(parts) > 1 else (parts[0].strip() if parts else new_item.get("type",""))
        new_item["spell"] = parts[-1] if len(parts) > 1 else spell or new_item.get("spell", "")
        new_item["realm"] = new_item.get("realm", "charged")
    
    elif enchant_type == "daily item":
        new_item["daily"] = int(float(bonus_pct))
        parts = spell.split("|") if isinstance(spell, str) and "|" in spell else [spell or "", "1"]
        new_item["spell"] = parts[0]
        new_item["lvl"] = int(parts[-1]) if parts[-1].isdigit() else 1
        new_item["realm"] = new_item.get("realm", "daily")
    
    elif enchant_type == "permanent magic item":
        # pp_mult aus Zauber-Typ extrahieren (vereinfacht)
        new_item["pp mult"] = int(float(spell or 0)) if spell and spell.replace('.','').isdigit() else 1
        new_item["realm"] = "per"
    
    # Schritt 4: Geld abziehen
    remaining_gold = purse_total - worth_total
    for i in range(len(clong)):
        key_short = cshort[i].upper()
        unit_val = 10 ** (len(clong) - 1 - i) + 1
        count = remaining_gold // unit_val if unit_val != 0 else remaining_gold
        new_purse = purse.copy()
        new_purse[key_short] = max(0, purse.get(key_short,0) - count)
        remaining_gold -= count * unit_val
    
    # Schritt 5: Ergebnis zuruckgeben
    return {
        "success": True,
        "new_item": new_item,
        "enchanted_worth": enchanted_worth,
        "new_purse": new_purse,
        "display_costs": worth_to_string(enchanted_worth),
        "bonus_mult": bonus_mult,
        "weight_mult": weight_mult,
    }
