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



idy, idb = 'youtube/k0PCNQS6OQY','export/Metaprednaska_3/EXPORT/Metaprednáška 3'
idy, idb = 'youtube/O027XaoSaTc','export/Metaprednaska_2/EXPORT/meta2'
idy, idb = 'youtube/iSoyfaMPvnE','export/4/EXPORT/Metaprednaska_4_oprava'
idy, idb = 'youtube/jmg02wCJD5M','export/Metaprednaska_1/EXPORT/Prokrastinácia_meta_prednaska_oprava'
idy, idb = 'youtube/BrawnBoqeqM','export/1838/EXPORT/In-House/D2 E451b_04-Porter'
idy, idb = 'youtube/qkOMs4VPcYw','export/Kriticke_mysleni/EXPORT/01'
idy, idb = 'youtube/_MLwgyCpFI4','export/1672/EXPORT/D2_Sall2_Angelika_Inglsperger_v1'
idy, idb = 'youtube/KmuV4I1D6xQ','export/1877/EXPORT/D2-D6_Seaside_Ballroom/D6_Andrej'
idy, idb = 'youtube/Ovw_rA9DaSk','export/1732/EXPORT/PIP/top_5_data_trends_of-brad_want'
idy, idb = 'youtube/_PyR1Ml70Rg','export/Webexpo/EXPORT/Cennydd Bowles'
idy, idb = 'youtube/9KkelKEunJo','export/ZeroWaste/EXPORT/1'
idy, idb = 'youtube/WZFYwjoGjOk','export/1007/EXPORT/Day 2 + 3 - Seattle 1 - Jakub/01 - seal'
idy, idb = 'youtube/SkZoUo2zYEI','export/1045/EXPORT/DeWolf_v03'
idy, idb = 'youtube/OJiXVnsF1ks','export/1086/EXPORT/LMC_01'
idy, idb = 'youtube/MSAcrpxvvqw','export/832/EXPORT/day 3/Day3_TopCongressHall_1515_Chris_Bache_v02'
idy, idb = 'youtube/FBnp9HPNHuM','export/Kriticke_mysleni/EXPORT/06'
idy, idb = 'youtube/K9lR_9fBb5c','export/1258/EXPORT/D2-Auditorium-Keynotes/07-arima'
idy, idb = 'youtube/bszNdUq8Rh8','export/ZeroWaste/EXPORT/234_v2'
idy, idb = 'youtube/hrrPsnGc9Rg','export/1010/EXPORT/fireside_chat'
idy, idb = 'youtube/AVMJe0fReAM','export/1913/EXPORT/D2/07.Interview'
idy, idb = 'youtube/PPEgY50n4Yc','export/ZeroWaste/EXPORT/6'
idy, idb = 'youtube/qKX94hMTrQA','export/582/EXPORT/D2-3Huyen_v2'
idy, idb = 'youtube/fQ2-wl25_1A','export/Science_Cafe/EXPORT/sc'
idy, idb = 'youtube/dpe-IrmhfPY','export/Kriticke_mysleni/EXPORT/05'
idy, idb = 'youtube/UAA3f7IUDsM','export/BB/EXPORT/BB_09'
idy, idb = 'youtube/wqQ-2vf4Ffw','export/832/EXPORT/day 2/D2_Hall3_007_Javier-Charme-Marticorena'
idy, idb = 'youtube/4Sg8PYbMzKQ','export/Klic_k_rozvoji_talentu/EXPORT/09'
idy, idb = 'youtube/c1ApDVmrr10','export/791/EXPORT/Future_Port_Prague_7.9.2017-klip_v1-1080p'