const AREAS={
castle:{n:"Hyrule Castle",c:"var(--castle)"},
mount:{n:"Death Mountain / Eldin",c:"var(--mount)"},
kak:{n:"Kakariko Village",c:"var(--kak)"},
lake:{n:"Lake Hylia",c:"var(--lake)"},
woods:{n:"Lost Woods / Forest",c:"var(--woods)"},
zora:{n:"Zora's Domain / Waters",c:"var(--zora)"},
gerudo:{n:"Gerudo / Desert",c:"var(--gerudo)"},
ranch:{n:"Lon Lon Ranch",c:"var(--ranch)"},
grave:{n:"Graveyard",c:"var(--grave)"},
snow:{n:"Snow region (Hebra etc.)",c:"var(--snow)"},
tot:{n:"Temple of Time / Sacred site",c:"var(--tot)"},
faron:{n:"Faron",c:"var(--faron)"},
goron:{n:"Goron City / Goron home",c:"#a0522d"},
deku:{n:"Great Deku Tree",c:"#00a86b"},
rito:{n:"Rito home",c:"#94a3b8"},
eastern:{n:"Eastern Palace / Temple",c:"#a855f7"},
sanct:{n:"Sanctuary",c:"#ffffff"},
house:{n:"Link's House",c:"#f472b6"}
};
const M={
loz:{mount:"P|Death Mountain",lake:"A|Unnamed lake",woods:"P|Lost Woods",grave:"P|Graveyard"},
aol:{gerudo:"A|Parapa Desert",tot:"A|Great Palace (Triforce of Courage)",castle:"A|North Castle",mount:"P|Death Mountain",grave:"P|King's Tomb graveyard"},
la:{castle:"A|Kanalet Castle",mount:"A|Tal Tal Heights / Mt. Tamaranch",kak:"A|Mabe Village",lake:"A|Martha's Bay",woods:"A|Mysterious Forest",gerudo:"A|Yarna Desert",grave:"P|Cemetery"},
fs:{mount:"A|Volcano stage",snow:"A|Ice stage"},
alttp:{castle:"P",mount:"P",kak:"P",lake:"P",woods:"P",zora:"A|Zora's Waterfall",gerudo:"A|Desert of Mystery",grave:"P",tot:"A|Master Sword pedestal (Lost Woods)",eastern:"P|Eastern Palace",sanct:"P",house:"P"},
oot:{castle:"P",mount:"P",kak:"P",lake:"P",woods:"P|Lost Woods + Kokiri Forest",zora:"P",gerudo:"P|Gerudo Valley / Desert Colossus",ranch:"P",grave:"P",tot:"P",goron:"P|Goron City",deku:"P|Great Deku Tree (Kokiri Forest)"},
mm:{castle:"A|Clock Town (the hub; no castle)",mount:"A|Snowhead (Goron Village)",lake:"A|Great Bay",woods:"A|Woodfall / Southern Swamp",zora:"A|Zora Hall, Great Bay",gerudo:"A|Pirates' Fortress",ranch:"A|Romani Ranch",grave:"A|Ikana Graveyard",snow:"A|Snowhead",goron:"A|Goron Village"},
oos:{mount:"A|Goron Mountain / Mt. Cucco",kak:"A|Horon Village",woods:"P|Lost Woods",gerudo:"A|Samasa Desert",grave:"A|Western Coast graveyard",deku:"A|Maku Tree",goron:"A|Goron Mountain"},
ooa:{mount:"A|Talus Peaks / Rolling Ridge",kak:"A|Lynna City",woods:"A|Deku Forest",zora:"A|Zora Village",grave:"A|Yoll Graveyard",deku:"A|Maku Tree",goron:"A|Rolling Ridge"},
ww:{house:"P|Link's House (Outset Island)",snow:"A|Ice Ring Isle",castle:"A|Sunken beneath the Great Sea",mount:"A|Dragon Roost Island",woods:"A|Forest Haven / Forbidden Woods",tot:"A|Master Sword chamber",deku:"P|Great Deku Tree (Forest Haven)",rito:"P|Dragon Roost Island"},
fsa:{castle:"P",mount:"P",kak:"P",lake:"P",woods:"P",gerudo:"P|Gerudo Desert / Desert of Doubt",snow:"A|Frozen Hyrule",eastern:"P|Eastern Temple"},
mc:{castle:"P",mount:"A|Mt. Crenel",lake:"P",woods:"A|Minish Woods",ranch:"P",grave:"A|Royal Valley",tot:"A|Elemental Sanctuary"},
tp:{castle:"P",mount:"P",kak:"P",lake:"P",woods:"P|Faron Woods / Sacred Grove",zora:"P",gerudo:"P",ranch:"A|Ordon Ranch",grave:"P",snow:"A|Snowpeak",tot:"P|Temple of Time ruins",faron:"P",goron:"A|Gorons on Death Mountain",sanct:"P|Sanctuary (Castle Town)"},
ph:{grave:"A|Isle of the Dead",mount:"A|Isle of Ember",snow:"A|Isle of Frost",goron:"A|Goron Island"},
st:{castle:"P",mount:"A|Fire Realm",woods:"A|Forest Realm",zora:"A|Ocean Realm",gerudo:"A|Sand Realm",snow:"A|Snow Realm",tot:"A|Tower of Spirits",goron:"A|Goron Village (Fire Realm)"},
ss:{castle:"A|Sealed Grounds (future site)",mount:"A|Eldin Volcano",lake:"A|Lake Floria",woods:"A|Faron Woods",gerudo:"A|Lanayru Desert",tot:"A|Sealed Temple",faron:"P|Faron Woods"},
albw:{zora:"P|Zora's River / Domain",castle:"P",mount:"P",kak:"P",lake:"P",woods:"P",zora:"P|Zora's River / Domain",gerudo:"A|Desert of Mystery",grave:"P",tot:"A|Master Sword pedestal",eastern:"P|Eastern Palace",sanct:"P",house:"P"},
tfh:{castle:"A|Hytopia Castle",mount:"A|Volcano",snow:"A|Ice Cavern",gerudo:"A|Dunes",woods:"A|Woodlands",lake:"A|Riverside"},
botw:{castle:"P",mount:"P|Death Mountain (Eldin)",kak:"P",lake:"P",woods:"P|Lost Woods + Korok Forest",zora:"P",gerudo:"P",ranch:"A|Lon Lon Ranch ruins",snow:"P|Hebra",tot:"P|Temple of Time ruins",faron:"P",goron:"P",deku:"P|Great Deku Tree (Korok Forest)",rito:"P|Rito Village",house:"P|Link's House (Hateno)"},
totk:{castle:"P",mount:"P|Death Mountain (Eldin)",kak:"P",lake:"P",woods:"P|Lost Woods + Korok Forest",zora:"P",gerudo:"P",ranch:"A|Lon Lon Ranch ruins",snow:"P|Hebra",tot:"P|Temple of Time (Great Sky Island)",faron:"P",goron:"P",deku:"P|Great Deku Tree (Korok Forest)",rito:"P|Rito Village",house:"P|Link's House (Hateno)"},
eow:{castle:"P",mount:"P|Eldin Volcano",kak:"P",lake:"P",woods:"A|Eternal Forest",zora:"P|Jabul Waters / Zora Cove",gerudo:"P",ranch:"A|Hyrule Ranch",grave:"P",snow:"P|Hebra Mountain",faron:"P|Faron Wetlands",goron:"P",deku:"P|The Deku Tree (Eternal Forest)",eastern:"P|Eastern Temple",sanct:"P|Northern Sanctuary",house:"P"}
};
const SHORT={fs:"FS '02",tfh:"TFH '15",la:"LA '93",oos:"OoS '01",ooa:"OoA '01",ph:"PH '07",loz:"LoZ '86",aol:"Zelda II '87",alttp:"ALttP '91",oot:"OoT '98",mm:"MM '00",ww:"WW '02",fsa:"FSA '04",mc:"MC '04",tp:"TP '06",st:"ST '09",ss:"SS '11",albw:"ALBW '13",botw:"BotW '17",totk:"TotK '23",eow:"EoW '24"};
const AREA_TEXT={
castle:"Missing from the 1986 overworld. A Link to the Past set it at the centre of the map, and it has stayed central or just north of centre ever since. In Wind Waker it's under the sea, and Skyward Sword shows the ground it will later be built on.",
mount:"The most consistent landmark in the series. It's in the north in almost every game: north-central in the top-down games, northeast in Ocarina, Twilight Princess and Breath of the Wild. Echoes of Wisdom breaks the pattern by moving Eldin to the northwest.",
kak:"Introduced in A Link to the Past, west of the castle. From Ocarina onward it sits at the foot of Death Mountain (Ocarina, Twilight Princess, Echoes). Breath of the Wild moves it southeast into Necluda.",
lake:"Usually in the south or southeast: southeast in the top-down games, south in the 3D ones. The Minish Cap moves it east, past Lon Lon Ranch. In Echoes of Wisdom it sits southeast of Castle Town, with a Great Fairy Shrine on its central island.",
woods:"A maze forest that shows up in nearly every game. It's northwest in the 2D maps, east/southeast in Ocarina (Kokiri) and north-central in Breath of the Wild (Korok Forest). The Master Sword often rests nearby.",
zora:"Tied to a river running from the north or east. It sits in the northeast or east in most games. In Wind Waker the Zoras have become the Rito, and Echoes calls the region Jabul Waters.",
gerudo:"Almost always west or southwest. Before Ocarina it's simply 'the desert' (Desert of Mystery). Ocarina introduced the Gerudo people, and the desert has carried their name since.",
ranch:"By name it's only in Ocarina of Time (the middle of Hyrule Field) and The Minish Cap (east of Hyrule Town). Majora's Mask has Romani Ranch, Breath of the Wild has only ruins, and Echoes has Hyrule Ranch.",
grave:"Usually next to Kakariko or north of the castle. The 1986 graveyard is in the northwest, and Majora's Mask puts its haunted canyon (Ikana) in the east.",
snow:"Became a standard region with Twilight Princess (Snowpeak) and took over the northwest from Breath of the Wild (Hebra). Majora's Mask and Spirit Tracks make it a whole quadrant or realm.",
tot:"The resting place of the Master Sword. A pedestal in the Lost Woods in the 2D games, a temple near the castle in Ocarina, and ruins in the southwest in Breath of the Wild. Skyward Sword shows how it began.",
faron:"Named from Twilight Princess onward and placed in the south: a woodland that becomes the tropical southeast of Breath of the Wild and the wetlands of Echoes. It's often where the Lost Woods spill over."
};
const LINKS={'loz': [['Full overworld map [NES Maps]', 'https://nesmaps.com/maps/Zelda/Zelda.html'], ['Zelda Wiki map files', 'https://zeldawiki.wiki/wiki/Category:The_Legend_of_Zelda_Maps']], 'albw': [['Interactive map [Gamer Guides]', 'https://gamerguides.com/zelda-link-between-worlds/maps']], 'totk': [['Interactive surface, sky & Depths maps [Gamer Guides]', 'https://www.gamerguides.com/the-legend-of-zelda-tears-of-the-kingdom/maps']], 'eow': [['Interactive Hyrule map [Game8]', 'https://game8.co/games/Zelda-Echoes-of-Wisdom/archives/471945']]};
const HUB='https://zeldawiki.wiki/wiki/Category:Maps';

Object.assign(AREA_TEXT,{
goron:"Introduced in Ocarina of Time as Goron City, carved into Death Mountain. Breath of the Wild, Tears of the Kingdom and Echoes of Wisdom bring the city back on Death Mountain/Eldin. Majora's Mask and Spirit Tracks have a Goron Village instead, and in Twilight Princess the Gorons live on Death Mountain without a city. Wherever it is, it's always on the volcano.",
deku:"The forest's guardian spirit. In Ocarina of Time he's in the Kokiri Forest, in Wind Waker at the Forest Haven, and in Breath of the Wild and Tears of the Kingdom in the Korok Forest, where he guards the Master Sword. Echoes of Wisdom puts him deep in the Eternal Forest. In the Oracle games the Maku Tree plays the same guardian role, in the middle of Holodrum and Labrynna.",
rito:"The bird people who, in Wind Waker's backstory, evolved from the Zoras. They live on Dragon Roost Island in the northeast of the Great Sea, and in Rito Village in western Tabantha in Breath of the Wild and Tears of the Kingdom.",
eastern:"The first dungeon of A Link to the Past, on the east edge of the map. A Link Between Worlds brings it back in the same spot, and Four Swords Adventures and Echoes of Wisdom rename it the Eastern Temple. In Echoes it's a mini-dungeon east of Hyrule Castle Town, between the castle and Jabul Waters.",
sanct:"The chapel where Zelda takes refuge in A Link to the Past, just north of Hyrule Castle beside the graveyard. A Link Between Worlds keeps it there, Twilight Princess has a Sanctuary in Castle Town, and Echoes of Wisdom's Northern Sanctuary sits north of the castle again, next to the graveyard.",
house:"Link's starting home. It's just south of Hyrule Castle in A Link to the Past and A Link Between Worlds, and it's in Echoes of Wisdom too. Breath of the Wild and Tears of the Kingdom move it east to Hateno Village."
});
