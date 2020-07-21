- vstupem pro skript budou dva listy EXPORTS_LIST a YOUTUBE_LIST
- CreateProcessPool v preprocess.py -> exports_to_process a youtube_to_process s durations
- MatchByDuration -> matches.pickle (skupiny podle shodnych delek)

-- Audio: vektor MFCC distances (podivat se na cuSignal)
-- Video: vektor rozdilovych snimku

#Video vektor:
- jak vytvorit?? videa muzou mit posun par framu, pokud vezmu vektor s rozlisenim x sekund, nedokazu videa posunuta o frame zmergovat - video bude v kazdym samplujiny
- vektor pres diference nemusi byt stabilni, napr. u staticych snimku bude sama nula, 1 pri skoku a jinakk nic - nenese to informaci o obsahu, jen o casovym prubehu. Nedostatecny. Resil by to mozna vektor poctu pixelu v hodnoach od 180 do 220..? Neco takovyho 
Nezustavaji pri konverzi intra framy?

Stava se casto, ze by vypadnul frame uprostred? Poud ne tak:
1. pres MFCC detekovat offset - syncnout

    - zjistit jaka je presnost..? Jak pripadne zvysit?
2. pres 3x3 zkusit prvni match
3. pokud shodne, kontrola pres vektor videa 
    - prvnich a podslednich 20 framu frame by frame, stred po 3,5 sec
    

plan pristi tyden:
otestovat MFCC sync + zpresnit s presnosti na frame pro zjisteni offsetu
-- zkusit segmentovany check? Pro otestovani vypadku signalu a zkraceni  (sync na zacatku, sync na konci)
- dal viz predchozi



- pristup do fronty a na starillera?