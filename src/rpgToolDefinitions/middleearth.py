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
        "Angmar" :["Cam Dum", "Gundaband", "Ettenmoors"],
        "Anor" : ["Nenuial", "Hills of Evendim", "North Downs", "Rhudaur", "Shire", \
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
        "Harad" :["Far Harad", "Near Harad"],
        "Eriador" :["Arnor"],
        "Amon Sul" : ["Weathertop"],
        "Eregion" :[],
        "Moria" : ["Khazaddum"],
        "Imladris" :["Rivendell", "Bruinen", "Misty Mountains"],
        "Bruinen" : ["Loudwater"],
        "Mitheithel" :["Hoarwell"],
        "Rhovanion":["Wilderland", "Mirkwood", "Sea of Rhun", "Celduin", "Laketown", "Dale", "Erebor", \
                     "Iron Hills", "Dol Guldur", "Woodland"],
        "northwestern Endor" : ["Rhovanion", "Arnor", "Angmar", "Calenardhon", "Eriador", \
                                 "Moria"],
        "northeastern Endor":[],
        "northern Endor" :["northwestern Endor", "northeastern Endor"],
        "middle Endor" :["Misty Mountains", "Rohan", "Rhovanion"],
        "southwestern Endor" :[],
        "southeastern Endor" :[],
        "southern Endor" : ["southwestern Endor", "southeastern Endor"],
        "Ered Nimrais" :["White Mountains"],
        "Rohan":["Gap of Rohan", "West Emnet", "East Emnet", "Entwash", "Eastfold", "Westfold", \
                 "Folde", "West March", "Folde", "Isen", "Edoras", "Aldburg", "Hornburg", "Helms Deep", \
                 "Anduin", "Fangorn"],
        "Isengard" :["Isen", "Misty Mountains"],
        "Misty Mountains": ["Hitheaglir", "Imladris", "Moria", "Caradhras", "Danuidhol", "Celebdil", \
                            "Gobblintown", "Dunland", "Eregion", "Agnmar"],
        "Lothlorien" : ["Lorien"],
        "Fangorn" : ["Entwash"],
        "Forodwaith" :[],
        "Dunland" :["Enedhwaith"],
        "Enedhwaith":["Tharbad", "Lond Daer"],
        }
