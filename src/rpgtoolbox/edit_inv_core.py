#!/usr/bin/env python3
"""!
\file edit_inv_core.py
\package rpgtoolbox.edit_inv_core
EditInventory core logic: carried-weight calculation, container/transport
indexing, and moving items in and out of containers.

\p Bug & todo history: see docs/bug_report_2026-08-26.md.
  BUG-01 (transport_item_to_container, FIXED 2026-08-26) — note is attached
  to that function below; the duplicate edit_inv_core import in
  gui/modules/inventory_gui.py is an open @todo flagged at that import site.
"""


def calc_carried_weight(character):
    """!
    Recalculate the character's carried weight from inventory locations
    and store the result in both character['carried'] and
    character['background']['carr_weight'].
    @param character the character dictionary
    @retval carried the recalculated carried weight
    @see docs/bug_report_2026-08-26.md (no bugs on record for this function)
    """
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
    """!
    Scan the character's gear list and build the container/transport
    indexes (idxcontainer / idxtransport) used by the inventory UI.
    @param character the character dictionary
    @retval result dictionary {'containers': [...], 'transports': [...]}
    @see docs/bug_report_2026-08-26.md (no bugs on record for this function)
    """
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
    """!
    Move the gear item at gear_idx into the named container by marking it
    'unequipped' and updating its 'container' field, then recalculate the
    carried weight.
    @param character the character dictionary
    @param gear_idx index of the item in character['inventory']['gear']
    @param container_name name of the target container
    @retval result {'success': True, 'placed_in': container_name} on success,
                   {'success': False, 'msg': ...} on an invalid index
    @fixes BUG-01 (2026-08-26): the shallow copy
           `item = dict(gear[gear_idx])` was missing (see sibling
           unpack_container_item() below for the pattern) -> every call raised
           NameError: name 'item' is not defined. Fixed + live-tested in
           commit 98e5105; details: docs/bug_report_2026-08-26.md, BUG-01.
    """
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
    """!
    Remove the 'container' assignment of the gear item at gear_idx and
    recalculate the carried weight. Pattern reference for other gear
    item movers (see transport_item_to_container()).
    @param character the character dictionary
    @param gear_idx index of the item in character['inventory']['gear']
    @retval result {'success': True, 'unpacked_into': old_container} on success,
                   {'success': False, 'msg': ...} on an invalid index
    @see docs/bug_report_2026-08-26.md (no bugs on record for this function)
    """
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
    """!
    Calculate the character's carried-weight capacity from strength
    (15 per point, capped at 200).
    @param char the character dictionary
    @retval capacity the max carried weight (rounded, max 200)
    @see docs/bug_report_2026-08-26.md (no bugs on record for this function)
    """
    strength = char.get('str', 10) or 10
    base = float(strength) * 15.0
    return round(base, 2) if base < 200 else 200.0


def calculate_equipment_mmp(character):
    """!
    Derive the movement-penalty (MMP) and the equipment-derived AT /
    missile / agility / max-man-mana modifiers from
    character['equipmentPenalty'] and cache them on the character.
    @param character the character dictionary
    @retval result {'mmp': ..., 'AT': ..., 'misslepen': ...}
    @see docs/bug_report_2026-08-26.md (no bugs on record for this function)
    """
    mmp = 0
    calcpen = character.get('equipmentPenalty', {}) or {}
    if isinstance(calcpen, dict):
        mmp = calcpen.get('weightpenalty', 0)
        character['AT'] = calcpen.get('AT', 0)
        character['misslepen'] = calcpen.get('misatpen', 0)
        character['armquickpen'] = calcpen.get('armqupen', 0)
        character['armmanmod'] = calcpen.get('maxmanmod', 0)

    return {'mmp': mmp, 'AT': character.get('AT'), 'misslepen': character.get('misslepen')}
