#!/usr/bin/env python3
"""EditInventory-Core-Logik: carried_weight, container/transport."""


def calc_carried_weight(character):
    shoptypes = ['weapon', 'gear', 'gems', 'services', 'herbs']
    unequipped = ['', 'unequipped', 'transport']
    carried = 0.0

    for elem in character.get('idxtransport') or []:
        n = elem.get('name') if isinstance(elem, dict) else None
        if n and n not in unequipped:
            unequipped.append(n)

    gear_inv = character.get('inventory', {}).get('gear', [])
    for elem in character.get('idxcontainer') or []:
        eidx = elem.get('index', -1) if isinstance(elem, dict) else -1
        if 0 <= eidx < len(gear_inv):
            loc = gear_inv[eidx].get('location', '')
            if loc in unequipped:
                n = elem.get('name')
                if n and n not in unequipped:
                    unequipped.append(n)

    for cat in shoptypes:
        for item in character.get('inventory', {}).get(cat, []):
            loc = item.get('location', '')
            if loc not in unequipped:
                if cat == 'gear':
                    if item.get('type') == 'clothes' and loc != 'equipped':
                        carried += float(item.get('weight', 0))
                else:
                    carried += float(item.get('weight', 0))

    carried = round(carried, 2)
    character['carried'] = carried
    bg = character.get('background')
    if isinstance(bg, dict):
        bg['carr_weight'] = carried
    return carried


def build_container_index(character):
    containers = []
    transports = []
    gear = character.get('inventory', {}).get('gear', []) or []

    for idx, item in enumerate(gear):
        i_type = str(item.get('type', '')).lower()
        entry = {'name': item.get('name', ''), 'index': idx, 'type': i_type}
        if i_type in ('container', 'sack'):
            containers.append(entry)
        elif i_type in ('transport', 'cart', 'mount'):
            transports.append(entry)

    character['idxcontainer'] = containers
    character['idxtransport'] = transports
    return {'containers': containers, 'transports': transports}


def transport_item_to_container(character, gear_idx, container_name):
    gear = character.get('inventory', {}).get('gear', []) or []
    if gear_idx < 0 or gear_idx >= len(gear):
        return {'success': False, 'msg': 'Ungultiger Container-Index'}

    item = dict(gear[gear_idx])
    item['location'] = 'unequipped'
    item['container'] = container_name

    gear[gear_idx] = item
    character['inventory']['gear'][gear_idx] = item
    calc_carried_weight(character)
    return {'success': True, 'placed_in': container_name}


def unpack_container_item(character, gear_idx):
    gear = character.get('inventory', {}).get('gear', []) or []
    if gear_idx < 0 or gear_idx >= len(gear):
        return {'success': False, 'msg': 'Container nicht gefunden'}

    item = dict(gear[gear_idx])
    old_container = item.get('container')
    item['container'] = None
    gear[gear_idx] = item
    character['inventory']['gear'][gear_idx] = item
    calc_carried_weight(character)
    return {'success': True, 'unpacked_into': old_container}


def get_carried_capacity(char):
    strength = char.get('str', 10) or 10
    base = float(strength) * 15.0
    return round(base, 2) if base < 200 else 200.0


def calculate_equipment_mmp(character):
    mmp = 0
    calcpen = character.get('equipmentPenalty', {}) or {}
    if isinstance(calcpen, dict):
        mmp = calcpen.get('weightpenalty', 0)
        character['AT'] = calcpen.get('AT', 0)
        character['misslepen'] = calcpen.get('misatpen', 0)
        character['armquickpen'] = calcpen.get('armqupen', 0)
        character['armmanmod'] = calcpen.get('maxmanmod', 0)

    return {'mmp': mmp, 'AT': character.get('AT'), 'misslepen': character.get('misslepen')}
