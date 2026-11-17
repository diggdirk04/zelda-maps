import json
# [source game, name in BotW/TotK, what it references, which game(s), kind]
B='BotW + TotK'; W='BotW'; T='TotK'
R=[
["The Legend of Zelda (1986)","Gleeok Bridge","Gleeok, the multi-headed dragon boss",B,"Place"],
["The Legend of Zelda (1986)","Aquame Bridge","Aquamentus, the horned dragon boss",B,"Place"],
["The Legend of Zelda (1986)","Manhala Bridge","Manhandla, the plant boss",B,"Place"],
["The Legend of Zelda (1986)","Digdogg Suspension Bridge","Digdogger, the urchin boss",B,"Place"],
["The Legend of Zelda (1986)","Gleeok as an enemy","The boss returns as a field and sky enemy",T,"Enemy"],
["The Legend of Zelda (1986)","Oaki the Korok's line","A take on the original game's famous 'dangerous to go alone' line",T,"Dialogue"],
["Zelda II: The Adventure of Link","Carok Bridge","Carock, guardian of the Maze Island palace",B,"Place"],
["Zelda II: The Adventure of Link","Helmhead Bridge","Helmethead, guardian of Midoro Palace",B,"Place"],
["Zelda II: The Adventure of Link","Orsedd Bridge","Horsehead, guardian of Parapa Palace",B,"Place"],
["Zelda II: The Adventure of Link","Rebonae Bridge","Rebonack, the Island Palace boss",B,"Place"],
["Zelda II: The Adventure of Link","Rauru (the first King of Hyrule)","Rauru is a Zelda II town before he's Ocarina's Sage of Light",T,"Character"],
["A Link to the Past","Sahasra Slope","Sahasrahla, the village elder",B,"Place"],
["A Link to the Past","Flowers around the Master Sword pedestal","Placed like the flowers around the pedestal in A Link to the Past",B,"Detail"],
["Link's Awakening","Tal Tal Peak","Tal Tal Heights",B,"Place"],
["Link's Awakening","Peak of Awakening","The game's own title",B,"Place"],
["Link's Awakening","Koholit Rock","Koholint Island",B,"Place"],
["Link's Awakening","Toronbo Beach","Toronbo Shores",B,"Place"],
["Link's Awakening","Mabe Village Ruins","Mabe Village",B,"Place"],
["Link's Awakening","Martha's Landing","Martha's Bay",B,"Place"],
["Link's Awakening","Malin Bay","Marin",B,"Place"],
["Link's Awakening","Torin Wetland, Mount Taran, Taran Pass","Tarin, Marin's father",B,"Place"],
["Link's Awakening","Kanalet Ridge","Kanalet Castle",B,"Place"],
["Link's Awakening","Ukuku Plains","Ukuku Prairie",B,"Place"],
["Link's Awakening","Goponga Island and Goponga Village Ruins","Goponga Swamp",B,"Place"],
["Link's Awakening","Ulria Grotto","Ulrira, the telephone hint man",B,"Place"],
["Link's Awakening","Tabahl Woods","Tabahl Wasteland",B,"Place"],
["Link's Awakening","Rok Woods","Roc's Feather",B,"Place"],
["Link's Awakening","Bananas as a reward","Bananas are part of the trading quest",W,"Item"],
["Ocarina of Time","Temple of Time","The temple itself, ruined on the Great Plateau (and in the sky in TotK)",B,"Place"],
["Ocarina of Time","Ranch Ruins","Lon Lon Ranch, southeast of Hyrule Castle",B,"Place"],
["Ocarina of Time","Fresh Milk bottle logo","The Lon Lon Ranch logo",T,"Item"],
["Ocarina of Time","Divine Beasts Vah Ruta, Vah Rudania, Vah Naboris","The sages Ruto, Darunia and Nabooru",W,"Name"],
["Ocarina of Time","Lake Saria","Saria, Sage of the Forest",B,"Place"],
["Ocarina of Time","Mido Swamp","Mido, the Kokiri bully",B,"Place"],
["Ocarina of Time","Mount Nabooru","Nabooru, Sage of Spirit",B,"Place"],
["Ocarina of Time","Darunia Lake","Darunia, Sage of Fire",B,"Place"],
["Ocarina of Time","Ruto Mountain, Ruto Lake, Ruto Precipice","Princess Ruto, Sage of Water",B,"Place"],
["Ocarina of Time","Rauru Hillside, Rauru Settlement Ruins","Rauru, Sage of Light",B,"Place"],
["Ocarina of Time","Ja'Abu Ridge","Lord Jabu-Jabu (and Wind Waker's Jabun)",B,"Place"],
["Ocarina of Time","Inogo Bridge","Ingo, the ranch hand",B,"Place"],
["Ocarina of Time","Kaepora Pass","Kaepora Gaebora, the owl",B,"Place"],
["Ocarina of Time","Bonooru's Stand, Pierre Plateau","Bonooru and Pierre, the two scarecrows",B,"Place"],
["Ocarina of Time","'A Song of Storms' shrine quest","The Song of Storms",W,"Quest"],
["Ocarina of Time","Twinrova at Ganondorf's side","The Gerudo witches",T,"Character"],
["Ocarina of Time","Link humming while cooking","Tunes from Ocarina of Time and other classic games",T,"Music"],
["Majora's Mask","Majora's Mask headgear","The mask itself. It's from the Master Trials DLC in BotW and also appears in TotK; monsters ignore you while wearing it",B,"Armor"],
["Majora's Mask","Fierce Deity armor","The Fierce Deity Mask transformation",T,"Armor"],
["Majora's Mask","Mikau Lake, Lulu Lake, Toto Lake","Members of the Indigo-Go's band",B,"Place"],
["Majora's Mask","Lake Darman","Darmani, the Goron hero",B,"Place"],
["Majora's Mask","Romani Plains","Romani of Romani Ranch",B,"Place"],
["Majora's Mask","Gero Pond","Don Gero, the frog conductor",B,"Place"],
["Majora's Mask","Tingel Island","Tingle, who debuted in Majora's Mask",B,"Place"],
["Oracle of Seasons","Horon Lagoon","Horon Village",B,"Place"],
["Oracle of Seasons","Tarm Point","Tarm Ruins",B,"Place"],
["Oracle of Seasons","Lodrum Headland","Holodrum, the game's world",B,"Place"],
["Oracle of Ages","Talus Plateau","Talus Peaks",B,"Place"],
["Oracle of Ages","Brynna Plain","Labrynna, the game's world",B,"Place"],
["Four Swords","Glowing 'eyeball' enemies","Vaati's sprite form",W,"Enemy"],
["The Wind Waker","Mekar Island, Lake Mekar","Makar, Sage of Wind",B,"Place"],
["The Wind Waker","Ankel, Knuckel and Davdi Islands","Tingle's brothers Ankle and Knuckle, and David Jr.",B,"Place"],
["The Wind Waker","Mount Daphnes","King Daphnes, the King of Red Lions",B,"Place"],
["The Wind Waker","Divine Beast Vah Medoh","Usually linked to Medli, the Rito Sage of Earth",W,"Name"],
["The Wind Waker","Rock Salt description","Salt 'from the ancient sea', a nod to the Great Sea",W,"Item"],
["The Wind Waker","Wind Temple","The dungeon of the same name",T,"Dungeon"],
["The Minish Cap","Minshi Woods","The Minish",B,"Place"],
["The Minish Cap","Pico Pond","The Picori, the Hylian name for the Minish",B,"Place"],
["The Minish Cap","Crenel Hills","Mount Crenel",B,"Place"],
["Twilight Princess","Arbiter's Grounds","The Gerudo Desert dungeon",B,"Place"],
["Twilight Princess","Faron Woods","The forest province",B,"Place"],
["Twilight Princess","Bridge of Eldin","The bridge of the same name",B,"Place"],
["Twilight Princess","Rutala Dam","Queen Rutela",B,"Place"],
["Twilight Princess","Ralis Pond","Prince Ralis",B,"Place"],
["Phantom Hourglass","Linebeck Island","Captain Linebeck",B,"Place"],
["Phantom Hourglass","Mercay Island, Bannan Island, Molida Island","Islands of the World of the Ocean King",B,"Place"],
["Phantom Hourglass","Zauz Island","Zauz the blacksmith",B,"Place"],
["Phantom Hourglass","Lake Siela","Ciela, Link's fairy companion",B,"Place"],
["Skyward Sword","Gorko Lake, Gortram Cliff","Gorko the Goron archaeologist",B,"Place"],
["Skyward Sword","Pillars of Levia","Levias, the sky spirit",B,"Place"],
["Skyward Sword","Eagus, Horwell and Owlan Bridges","Instructors at Skyloft's Knight Academy",B,"Place"],
["Skyward Sword","Thunderhead Isles","The Thunderhead storm in the sky",T,"Place"],
["Skyward Sword","Goddess statues and the White Sword of the Sky","Hylia's statues and the Goddess Sword",T,"Item"],
["A Link Between Worlds","Oren Bridge","Queen Oren, Sage of Water",B,"Place"],
["Tri Force Heroes","Tuft Mountain","King Tuft of Hytopia",B,"Place"],
]
open('refs.js','w').write('const REFS='+json.dumps(R)+';\n')
b=open('build.py').read()
sec='''<section id="callbacks"><h2>Callbacks in Breath of the Wild &amp; Tears of the Kingdom</h2>
<div class="sub">Both games are full of nods to earlier Zelda games: place names, bridges, armor, music and characters. Many names are slightly misspelled on purpose, as if worn down by history. TotK reuses BotW's map, so almost every place name appears in both games.</div>
<div class="ctl" style="margin-top:10px"><input id="rq" placeholder="Search callbacks..." style="background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:6px 10px;min-width:220px">
<select id="rg"><option value="">Both games</option><option value="BotW">Breath of the Wild</option><option value="TotK">Tears of the Kingdom</option></select>
<select id="rk"><option value="">All types</option></select><span id="rc"></span></div>
<div id="refs" class="areas"></div></section>
'''
b=b.replace('<section><h2>How each area changes over time</h2><div class="areas" id="areas"></div></section>','<section><h2>How each area changes over time</h2><div class="areas" id="areas"></div></section>\n'+sec)
b=b.replace("LAYERDATA=open('layerdata.js').read()","LAYERDATA=open('layerdata.js').read()+open('refs.js').read()")
js=r'''
(function(){const kinds=[...new Set(REFS.map(r=>r[4]))].sort();$('#rk').innerHTML+=kinds.map(k=>`<option>${k}</option>`).join('');
const tag=g=>`<span style="font-size:11px;border:1px solid var(--line);border-radius:999px;padding:1px 7px;color:var(--mute);white-space:nowrap">${g}</span>`;
function draw(){const q=$('#rq').value.toLowerCase(),gm=$('#rg').value,k=$('#rk').value;
 const rows=REFS.filter(r=>(!q||r.join(' ').toLowerCase().includes(q))&&(!gm||r[3].includes(gm))&&(!k||r[4]===k));
 const by={};rows.forEach(r=>(by[r[0]]=by[r[0]]||[]).push(r));
 $('#refs').innerHTML=Object.entries(by).map(([g,rs])=>`<div class="area" style="border-left-color:var(--gold)"><h3>${g} <span style="color:var(--mute);font-weight:400;font-size:13px">(${rs.length})</span></h3>${rs.map(r=>`<p style="display:flex;gap:8px;justify-content:space-between;align-items:baseline"><span><b>${r[1]}</b>: ${r[2]}</span><span style="display:flex;gap:4px">${tag(r[4])}${tag(r[3])}</span></p>`).join('')}</div>`).join('')||'<p class="sub">No matches.</p>';
 $('#rc').textContent=`${rows.length} callbacks across ${Object.keys(by).length} games`}
['#rq','#rg','#rk'].forEach(s=>$(s).addEventListener('input',draw));draw()})();
'''
b=b.replace("// matrix",js+"// matrix",1)
b=b.replace('<div class="sub">The real overworld maps','<div class="sub"><a href="#callbacks">Jump to the Breath of the Wild &amp; Tears of the Kingdom callbacks list</a> · The real overworld maps')
open('build.py','w').write(b)
