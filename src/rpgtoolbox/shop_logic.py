#!/usr/bin/env python3
"""
Shop-Logik: buy_item(), sell_item(), calc_MMP(), calc_carried_weight()
Pure Business Logic - keine Tkinter-Abhängigkeiten.
"""

from rpgToolDefinitions.inventory import coins


def buy_item(purse, price_str, shoptype="armor"):
    """
    Buy an item. Returns updated purse or None if not enough money.
    
    Args:
        purse: dict with coin types ['MP','PP','GP','SP','BP','CP','TP','IP']
        price_str: price like '10GP' (final 2 chars = coin type)
        shoptype: type of shop item
    
    Returns:
        dict: updated purse if successful, None if can't afford
    """
    worth_val = int(price_str[:-2])
    coin_type = price_str[-2:]
    
    # Convert to IP (smallest unit)
    mymoney = purse["IP"]
    cu = coins["short"].index(coin_type)
    multiplier = 10 ** (len(coins["short"]) - cu - 1)
    price = worth_val * multiplier
    
    if mymoney < price:
        return None  # Can't afford
    
    # Convert all purse coins to IP first, subtract price, then reconvert
    total_in_ip = 0
    for coin in coins["short"]:
        upper = coin.upper()
        cu_idx = coins["short"].index(coin)
        multiplier_p = 10 ** (len(coins["short"]) - cu_idx - 1)
        total_in_ip += purse.get(upper, 0) * multiplier_p
    
    result_ip = total_in_ip - price
    if result_ip < 0:
        return None
    
    # Reconvert back to coin types
    new_purse = purse.copy()
    remaining = result_ip
    for i, coin in enumerate(reversed(coins["short"])):
        upper_coin = coin.upper()
        unit_val = 10 ** (len(coins["short"]) - (len(coins["short"]) - 1 - i) - 1)
        
        # For IP (last element), unit_val = 1
        if coins["short"][i] == "ip":
            new_purse[upper_coin] = remaining
            remaining = 0
        else:
            count = remaining // unit_val
            new_purse[upper_coin] = count
            remaining -= count * unit_val
    
    return new_purse


def sell_item(inv_item, worth_field, shoptype):
    """
    Calculate sell price (typically buy_price / 2).
    
    Args:
        inv_item: dict representation of inventory item
        worth_field: key for worth in inv_item
        shoptype: type of shop
    
    Returns:
        tuple: (price_int, coin_type) or None if no worth
    """
    worth_val = inv_item.get(worth_field)
    if not worth_val or not isinstance(worth_val, str):
        return None
    
    try:
        price = int(worth_val[:-2]) // 2  # Sell for half the buy price
        coin_type = worth_val[-2:]
        return (price, coin_type)
    except (ValueError, IndexError):
        return None


def calc_mmp(character, shoptype="armor"):
    """
    Calculate Maximum Market Power based on character level and profession.
    
    Args:
        character: dict with 'lvl', 'prof', etc.
        shoptype: type of shop
    
    Returns:
        float: MMP value
    """
    lvl = character.get('lvl', 1)
    prof = character.get('prof', 'Ranger')
    
    # Base MMP from level
    base_mmp = lvl * 50.0
    
    # Profession multiplier
    prof_multipliers = {
        'Ranger': 1.2,
        'Fighter': 1.1,
        'Mage': 1.3,
        'Cleric': 1.0,
        'Thief': 0.9,
    }
    
    multiplier = prof_multipliers.get(prof, 1.0)
    
    # Equipment bonus based on shoptype
    equip_bonus = {'armor': 0.25, 'weapon': 0.20, 'gear': 0.15, 'gems': 0.10}
    bonus = equip_bonus.get(shoptype, 0.1)
    
    return base_mmp * multiplier * (1 + bonus)


def calc_carried_weight(char_inventory):
    """
    Calculate total carried weight from inventory.
    
    Args:
        char_inventory: dict with lists of items per category
    
    Returns:
        float: total weight
    """
    total_weight = 0.0
    
    for shoptype, item_list in char_inventory.items():
        if not isinstance(item_list, list):
            continue
        
        for item in item_list:
            if not isinstance(item, dict):
                continue
            
            # Weight column typically stored as float
            weight = item.get('weight')
            if weight is not None:
                try:
                    total_weight += float(weight)
                except (ValueError, TypeError):
                    pass
    
    return total_weight


def idx_container_transport(char_inventory, shoptype="armor"):
    """
    Calculate container transport capacity usage.
    
    Args:
        char_inventory: dict with item lists
        shoptype: type of container
    
    Returns:
        tuple: (used_capacity, max_capacity) or None
    """
    used = 0.0
    cap = 100.0  # Default max capacity
    
    for key, items in char_inventory.items():
        if not isinstance(items, list):
            continue
        
        for item in items:
            if not isinstance(item, dict):
                continue
            
            # Check if item is a container type (e.g., backpack)
            item_type = item.get('type', '')
            weight = item.get('weight')
            
            try:
                if item_type == 'container':
                    cap += float(item.get('capacity', 50.0))
                elif weight:
                    used += float(weight)
            except (ValueError, TypeError):
                pass
    
    return (used, cap)


def add_shop_item(source_data, shoptype, price=None):
    """
    Create a shop item from source template data.
    
    Args:
        source_data: template dict for the item type
        shoptype: category of shop
        price: optional price override
    
    Returns:
        dict: new shop item or None if no template
    """
    if not source_data:
        return None
    
    new_item = source_data.copy()
    
    if price:
        price_str = f"{price}GP"
        new_item['worth'] = price_str
    else:
        # Default worth calculation
        base_cost = 10  # Base cost in GP
        new_item['worth'] = f"{base_cost}GP"
    
    return new_item


def get_selected(items, search_params):
    """
    Find a selected item matching search parameters.
    
    Args:
        items: list of item dicts
        search_params: dict with fields to match
    
    Returns:
        dict: matched item or None
    """
    for item in items:
        if not isinstance(item, dict):
            continue
        
        match = True
        for key, val in search_params.items():
            if item.get(key) != val:
                match = False
                break
        
        if match:
            return item
    
    return None
