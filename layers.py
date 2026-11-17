import json
b=open('build.py').read()
SKY=[
{"id":"sky_ss","t":"Skyward Sword: The Sky","y":2011,"img":"ss_sky.webp","w":1200,"h":675,
 "mk":[["castle",52,58,"Skyloft (the hub)"],["snow",24,28,"The Thunderhead (Isle of Songs inside)"],["mount",53,34,"Red column of light: drop to Eldin"],["faron",55,70,"Column of light: drop to Faron"],["gerudo",37,77,"Yellow column of light: drop to Lanayru"]],
 "note":"One sea of clouds with Skyloft in the middle. You reach the Surface by diving through coloured columns of light into each province. The Thunderhead storm covers the northwest."},
{"id":"sky_totk","t":"Tears of the Kingdom: The Sky","y":2023,"img":"totk_sky.webp","w":1500,"h":1500,
 "mk":[["tot",53,60,"Great Sky Island (tutorial, Temple of Time)"],["snow",25,24,"Hebra Sky (Wind Temple area)"],["zora",79,45,"Wellspring Island (Water Temple)"],["faron",60,76,"Thunderhead Isles, Faron Sky (approximate)"]],
 "note":"Archipelagos float above specific surface regions instead of around one hub. You can dive off any island and land on the ground directly below. Its Thunderhead Isles echo Skyward Sword's Thunderhead."}
]
STACKS=[
["Tears of the Kingdom: three stacked layers",[["totk_sky.webp","Sky"],["botw.webp","Surface"],["totk_depths.webp","Depths"]],"The same footprint three times. The Depths roughly invert the surface: mountains become chasms and Lightroots sit under shrines."],
["Skyward Sword: sky over surface",[["ss_sky.webp","The Sky"],["ss_surface.webp","The Surface (Faron, Eldin, Lanayru)"]],"The sky is a single connected space, and the surface is three separate provinces you reach by diving."],
["A Link to the Past: Light and Dark World",[["alttp_light.webp","Light World"],["alttp_dark.webp","Dark World"]],"The same grid in two moods. Every landmark has a twin in the same spot."],
["Oracle of Ages: present and past",[["ooa_present.webp","Present"],["ooa_past.webp","Past"]],"Labrynna in two eras. Changing something in the past changes the present."],
["Oracle of Seasons: four seasons",[["oos_spring.webp","Spring"],["oos_summer.webp","Summer"],["oos_autumn.webp","Autumn"],["oos_winter.webp","Winter"]],"One map, four states. Water freezes, vines grow and paths open or close with the season."],
["Wind Waker and Phantom Hourglass: two seas",[["ww.webp","The Great Sea"],["ph.webp","World of the Ocean King"]],"In Wind Waker the sea is a layer over drowned Hyrule. Phantom Hourglass is its sequel, set in a different ocean."]
]
LT=[
["Sky above","Skyward Sword (the Sky); Tears of the Kingdom (Sky Islands); Twilight Princess (City in the Sky, one dungeon area); Four Swords Adventures (Tower of Winds stage)"],
["Underground","Tears of the Kingdom (the Depths); Oracle of Seasons (Subrosia); Majora's Mask (under Ikana); Echoes of Wisdom (Hyrule Castle Underground)"],
["Mirror / parallel world","A Link to the Past (Dark World); A Link Between Worlds (Lorule); Twilight Princess (Twilight Realm, covering provinces); Echoes of Wisdom (Still World rifts)"],
["Time","Ocarina of Time (child and adult Hyrule, seven years apart); Oracle of Ages (present and past); Majora's Mask (the three-day cycle)"],
["Season","Oracle of Seasons (four seasons on one map)"],
["Water over land","Wind Waker (the Great Sea over sunken Hyrule)"],
]
data="const SKY="+json.dumps(SKY)+";const STACKS="+json.dumps(STACKS)+";const LT="+json.dumps(LT)+";\n"
section='''<section id="layers"><h2>World layers: sky, below and alternate worlds</h2>
<div class="sub">Many Zelda maps have a second layer stacked on the first. This section starts with the two sky maps, then puts each game's layers side by side.</div>
<h3 style="margin:18px 0 4px">The two skies</h3><div class="compare" id="skies"></div>
<div class="tablewrap" style="margin-top:12px"><table style="min-width:700px" id="skytable"></table></div>
<h3 style="margin:22px 0 4px">Layer stacks</h3><div id="stacks"></div>
<h3 style="margin:22px 0 4px">Layer types across the series</h3><div class="tablewrap"><table style="min-width:700px" id="lt"></table></div>
</section>
'''
b=b.replace('<section><h2>Every map</h2>',section+'<section><h2>Every map</h2>')
js=r'''
SKY.forEach(g=>$('#skies').appendChild(card(g)));
const ST=[["","Skyward Sword","Tears of the Kingdom"],["Structure","One cloud sea with scattered islands","Separate archipelagos, each above a surface region"],["Hub","Skyloft, in the centre","None. The Great Sky Island is the starting area, south of centre"],["Way down","Dive through 3 columns of light (Faron, Eldin, Lanayru)","Dive anywhere and land on the ground directly below"],["Storm zone","The Thunderhead (northwest), hiding the Isle of Songs","The Thunderhead Isles (Faron Sky), fog-covered until a quest clears it"],["Temples in the sky","Sky Keep (endgame)","The Wind and Water Temples, plus the Temple of Time on the Great Sky Island"],["Relation to the surface","The surface is cut off by the Cloud Barrier","The same footprint as the surface and the Depths"]];
$('#skytable').innerHTML=ST.map((r,i)=>'<tr>'+r.map((c,j)=>i===0?`<th style="writing-mode:horizontal-tb;transform:none;height:auto;background:var(--panel2)">${c}</th>`:(j===0?`<th>${c}</th>`:`<td style="text-align:left">${c}</td>`)).join('')+'</tr>').join('');
STACKS.forEach(([t,imgs,n])=>{const c=document.createElement('div');c.className='card';c.style.marginTop='12px';c.innerHTML=`<h3>${t}</h3><div class="note" style="margin:4px 0 8px">${n}</div><div style="display:grid;grid-template-columns:repeat(${imgs.length},1fr);gap:8px">${imgs.map(([f,cap])=>`<figure style="margin:0;cursor:zoom-in" data-f="${f}" data-c="${t}: ${cap}"><img src="maps/${f}" loading="lazy" style="width:100%;border-radius:6px;background:#000;aspect-ratio:1/1;object-fit:contain"><figcaption style="font-size:12px;color:var(--mute);text-align:center">${cap}</figcaption></figure>`).join('')}</div>`;
c.querySelectorAll('figure').forEach(fg=>fg.onclick=()=>openLB(null,fg.dataset.f,fg.dataset.c));$('#stacks').appendChild(c)});
$('#lt').innerHTML='<tr><th style="writing-mode:horizontal-tb;transform:none;height:auto;background:var(--panel2)">Layer type</th><th style="writing-mode:horizontal-tb;transform:none;height:auto;background:var(--panel2);text-align:left">Where it appears</th></tr>'+LT.map(r=>`<tr><th>${r[0]}</th><td style="text-align:left">${r[1]}</td></tr>`).join('');
apply();
'''
b=b.replace("drawCmp();\n// matrix","drawCmp();\n"+js+"// matrix")
b=b.replace("<script>\n'''+reuse+data+r'''","<script>\n'''+reuse+data+LAYERDATA+r'''")
b=b.replace("data=\"const GAMES=\"","LAYERDATA=open('layerdata.js').read()\ndata=\"const GAMES=\"")
open('build.py','w').write(b); open('layerdata.js','w').write(data)
