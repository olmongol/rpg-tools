#!/usr/bin/env python
'''
\file middleearth.py
\package rpgToolDefinitions.middleearth
\brief definition of landscapes in Middle-Earth


\date (C) 2020
\author Marcus Schwamberger
\email marcus@lederzeug.de
\version 1.0
'''
__version__ = "1.0"
__updated__ = "05.09.2020"

areas = {"Shire" : ["Old Forrest", "Bockland", "Westmarch", "Baranduin", "Hobbiton", "Baranduin"],
        "Breeland" : ["Weather Hills", "Weather Top", "Barrow Downs", "Old Forest", "Bree", "Midgewater"],
        "Angmar" :["Cam Dum", "Gundaband", "Ettenmoors", "Misty Mountains"],
        "Arnor" : ["Nenuial", "Hills of Evendim", "North Downs", "Rhudaur", "Shire", \
                  "Breeland", "Arthedain", "Cardolan", "Minhirath", \
                  "Hoarwell", "Lune", "Tyrn Gorthad"],
        "Cardolan" :["Breeland", "South Downs", "Minhiriath", "Tharbad", "Eryn Vorn", "Gwathlo", \
                     "Mitheithel", "Gwathlo", "Lond Daer", "Bruinen"],
        "Rhudaur" :["Mitheithel", "Bruinen", "Tollshaws", "Angle", "Coldfells", "Egladil", "Carmeth Brin", \
                    "Misty Mountains", "Elnost", "Daenost"],
        "Arthedain" : ["Shire", "Breeland", "Annuminas", "Amon Sul", "Fornost", "Elostirion", \
                       "North Downs"],
        'Beleriand' : ["Arvenien", "Forest of Brethil", "Dimbar", "Doriath", "Estolad", \
                       "Falas", "Himlad", "Nan-tathren", "Talath Dirnen", "Taur-en Faroth", \
                       "Taur-im-Dulnath", "Thargelion", "Ossirand", "Lindon", "Belegost", \
                       "Nogrod", "Brithombar", "Eglarest", "Gondolin", "Menegroth", "Nargothrond" \
                       "Himring", "Vinyamar", "Ered Luin", "Blue Mountains", "Forlindon", \
                       "Harlindon", "River Lhun"],
        "Doriath" : ["Thingol", "Mellan"],
        "Minhiriath" : ["Eryn Vorn", "Gwathlo", "Baranduin"],
        "Gondor" :["Osgiliath", "Minas Tirith", "Anórien", "Ered Nimrais", 'Anduin', \
                   "Lossarnach", "Lebennin", "Belfalas", "Dol Amroth", "Dor-en-Ernil", \
                   "Lamedon", "Ringlo", "Anfalas", "Andrast", "Pinnath Gelin", "Harondor", \
                   "Poros", "Harnen", "Calenardhon", "Isen", "Limlight", "Rhovanion", "Ephel Duath", \
                   "Durthang", "Cair Andros", "Calembel", "Dol Amroth", "Henneth Annun", "Linhir", \
                   "Pelagir", "Tarnost", "Dunland"],
        "Calenardhon":["Rohan"],
        "Ered Nimrais" :["White Mouintains"],
        "Gwathlo" :["Greyflood"],
        "Baranduin" :["Brandywine"],
        "Harad" :["Far Harad", "Near Harad", "Khand", "Haradwaith"],
        "Far Harad":[],
        "Near Harad":["Harnen"],
        "Haradwaith" :["Sutherland"],
        "Khand" :[],
        "Eriador" :["Arnor", "Imladris", "Agnmar", "Eregion"],
        "Amon Sul" : ["Weathertop"],
        "Eregion" :["Bruinen", "Glanduin", "Ost-in-Edhil", "Nin-in-Eilph", "Misty Mountains"],
        "Moria" : ["Khazaddum", "Misty Mountains"],
        "Imladris" :["Rivendell", "Bruinen", "Misty Mountains"],
        "Bruinen" : ["Loudwater"],
        "Mitheithel" :["Hoarwell"],
        "Rhovanion":["Wilderland", "Mirkwood", "Sea of Rhun", "Celduin", "Esgaroth", "Dale", "Erebor", \
                     "Iron Hills", "Dol Guldur", "Woodland", "Anduin", "Brown Lands", "Emyn Muil", \
                     "Dagorlad"],
        "northwestern Endor" : [ "Arnor", "Angmar", "Calenardhon", "Eriador", \
                                 "Moria", "Forodwaith", "Beleriand"],
        "northeastern Endor":["Rhovanion", "Rhun", "Dorwinion", "Iron Hills", "Ered Mithrin"],
        "northern Endor" :["northwestern Endor", "northeastern Endor"],
        "middle Endor" :["Misty Mountains", "Rohan", "Rhovanion", "Mordor", "Rhun", "Lorien", "Fangorn"],
        "southwestern Endor" :["Gondor", ],
        "southeastern Endor" :["Harad", "Khand", "Umbar"],
        "southern Endor" : ["southwestern Endor", "southeastern Endor"],
        "Ered Nimrais" :["White Mountains"],
        "Rohan":["Gap of Rohan", "West Emnet", "East Emnet", "Entwash", "Eastfold", "Westfold", \
                 "Folde", "West March", "Folde", "Isen", "Edoras", "Aldburg", "Hornburg", "Helms Deep", \
                 "Anduin", "Fangorn"],
        "Isengard" :["Isen", "Misty Mountains"],
        "Misty Mountains": ["Hitheaglir", "Caradhras", "Danuidhol", "Celebdil"],
        "Goblintown" :["Misty Mountains"],
        "Lothlorien" : ["Lorien"],
        "Fangorn" : ["Entwash"],
        "Forodwaith" :[],
        "Dunland" :["Enedhwaith", "Misty Mountains"],
        "Enedhwaith":["Tharbad", "Lond Daer"],
        "Belfalas":["Dol Amroth", " Bay of Belfalas"],
        "Mordor":["Gorgoroth", "Udun", "Minas Morgul", "Nurn", "Sea of Nurnen", "Ered Lithui", "Baraddur", \
                  "Ephel Duath", "Mor Annon"],
        "Ered Lithui":["Ash Mountains"],
        "Ephel Duath" : ["Mountains of Shadow"],
        "Umbar" : [],
        }



def getAllRegions(region = "everywhere"):
    """
    This function delivers a list of all included regions in ME for the herb hunt.
    @param region region to generate the list of.
    @retval result list of all included regions.
    """
    global areas
    result = [region]
    checked = []

    if region in areas.keys() and region not in checked:
        result += areas[region]
        result = list(set(result))
        checked.append(region)
        result.sort()
        checked.sort()
        checked = list(set(checked))

        while checked != result:

            for r in result:

                if r in areas.keys() and r not in checked:
                    result += areas[r]

                result = list(set(result))
                checked.append(r)
                checked = list(set(checked))
                result.sort()
                checked.sort()

    return result
