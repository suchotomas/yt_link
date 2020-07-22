import os, time
from api.tools import Tools as t
from file_to_mfcc import FileToMFCC
from file_to_video_vector import FileToVideoVector
from api.offset_calc import OffsetCalc
from tqdm import tqdm
import random

MIN_CORR_SCORE = 0


class CompareByMFCC:
    '''
    - podmineny vstupy dva klice (idy, ide)
    - nepodmineny vstupy: y_info, e_info,  
    '''
    def __init__(self, workdir):
        self.workdir = workdir    
        self.offset_calc = OffsetCalc()


    def run(self, matches_path, out_matches_path):
        self.matches = t.load_pickle(matches_path)
        self.out_matches_path = out_matches_path
        process_list = []
        for ida, match in self.matches.items():
            for idb, match_item in match.idb_items.items():
                process_list.append((ida, idb))
        random.shuffle(process_list)
        for idx in tqdm(range(len(process_list)), ascii=True, desc='process {} lines'.format(len(process_list))):
            ida, idb = process_list[idx]
            offset = self.get_offset(idy=ida, ide=idb)
            self.matches[ida].idb_items[idb].offset = offset
        t.save_pickle(self.out_matches_path, self.matches)

    def get_offset(self, idy, ide, y_info=None, e_info=None):
        y_info = y_info if y_info is not None else self.get_info(idy)
        e_info = e_info if e_info is not None else self.get_info(ide)



        file2mfcc = FileToMFCC(workdir)
        # file2video_vector = FileToVideoVector(workdir)

        t0 = time.time()
        # print('y_a_path')
        y_a_path = file2mfcc.run(y_info['src'], idy)
        t1 = time.time()
        # print('... {:0.2f}', t1 - t0)
        # print('e_a_path')
        e_a_path = file2mfcc.run(e_info['src'], ide)
        t2 = time.time()
        # print('... {:0.2f}', t2 - t1)


        # print('y_v_path')
        # self.y_v_path = self.file2video_vector.run(y_info['src'], idy)
        # t3 = time.time()
        # print('... {:0.2f}', t3 - t2)
        # print('e_v_path')
        # self.e_v_path = self.file2video_vector.run(e_info['src'], ide)
        # t4 = time.time()
        # print('... {:0.2f}', t4 - t3)
        if None in [y_a_path, e_a_path, y_info, e_info]:
            return None
        offset, score = self._correlate(y_a_path, e_a_path, y_info, e_info)
        if None in [score, offset]:
            return None
        if score > MIN_CORR_SCORE:
            return offset
        else:
            return None

        #TODO: vytvorit video vektor stejne jakko audio a pripravit do __init__
        # pak fce na porovnani vektoru - asi bude stejna pro audio i pro video jen s preskalovanim casu. Audio vektor podvzorkovat na 25fps?
        # ve finalne projet kratkym oknem a sledovat odchylku mezi vektory. Pokud nekde velky rozdil -> video neni shodne.
        # bylo by fajn pred porovnavanim udelat dynamic time wrapping obou vektoru a spravne je na sebe napasovat

    def get_info(self, id):
        info_path = os.path.join(self.workdir, id, 'info.json')
        info = t.load_json(info_path)
        if info is None:
            print('cannot read ', info_path)
        return info
         
    def _correlate(self, y_path, e_path, y_info, e_info):
        '''
        korelace dvou mfcc prubehu - ziskat maximalni moznou presnost (overit jestli to delam v autosyncu dobre)
        '''

        y_dur, e_dur = y_info['duration'], e_info['duration']

        # print(y_info['src'], e_info['src'], y_dur, e_dur)
        return self.offset_calc.calculate(y_path, y_dur, e_path, e_dur)


    

workdir = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir'
matches_path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/matches_100.pickle'
out_matches_path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/matches_100_offsets.pickle'

idy, idb = 'youtube/k0PCNQS6OQY','export/Metaprednaska_3/EXPORT/Metaprednáška 3'
idy, idb = 'youtube/O027XaoSaTc','export/Metaprednaska_2/EXPORT/meta2'
idy, idb = 'youtube/iSoyfaMPvnE','export/4/EXPORT/Metaprednaska_4_oprava'
idy, idb = 'youtube/jmg02wCJD5M','export/Metaprednaska_1/EXPORT/Prokrastinácia_meta_prednaska_oprava'
# idy, idb = 'youtube/BrawnBoqeqM','export/1838/EXPORT/In-House/D2 E451b_04-Porter'
# idy, idb = 'youtube/qkOMs4VPcYw','export/Kriticke_mysleni/EXPORT/01'
# idy, idb = 'youtube/_MLwgyCpFI4','export/1672/EXPORT/D2_Sall2_Angelika_Inglsperger_v1'
# idy, idb = 'youtube/KmuV4I1D6xQ','export/1877/EXPORT/D2-D6_Seaside_Ballroom/D6_Andrej'
# idy, idb = 'youtube/Ovw_rA9DaSk','export/1732/EXPORT/PIP/top_5_data_trends_of-brad_want'
# idy, idb = 'youtube/_PyR1Ml70Rg','export/Webexpo/EXPORT/Cennydd Bowles'
# idy, idb = 'youtube/9KkelKEunJo','export/ZeroWaste/EXPORT/1'
# idy, idb = 'youtube/WZFYwjoGjOk','export/1007/EXPORT/Day 2 + 3 - Seattle 1 - Jakub/01 - seal'
# idy, idb = 'youtube/SkZoUo2zYEI','export/1045/EXPORT/DeWolf_v03'
# idy, idb = 'youtube/OJiXVnsF1ks','export/1086/EXPORT/LMC_01'
# idy, idb = 'youtube/MSAcrpxvvqw','export/832/EXPORT/day 3/Day3_TopCongressHall_1515_Chris_Bache_v02'
# idy, idb = 'youtube/FBnp9HPNHuM','export/Kriticke_mysleni/EXPORT/06'
# idy, idb = 'youtube/K9lR_9fBb5c','export/1258/EXPORT/D2-Auditorium-Keynotes/07-arima'
# idy, idb = 'youtube/bszNdUq8Rh8','export/ZeroWaste/EXPORT/234_v2'
# idy, idb = 'youtube/hrrPsnGc9Rg','export/1010/EXPORT/fireside_chat'
# idy, idb = 'youtube/AVMJe0fReAM','export/1913/EXPORT/D2/07.Interview'
# idy, idb = 'youtube/PPEgY50n4Yc','export/ZeroWaste/EXPORT/6'
# idy, idb = 'youtube/qKX94hMTrQA','export/582/EXPORT/D2-3Huyen_v2'
# idy, idb = 'youtube/UAA3f7IUDsM','export/BB/EXPORT/BB_09'
# idy, idb = 'youtube/4Sg8PYbMzKQ','export/Klic_k_rozvoji_talentu/EXPORT/09'

# idy, idb = 'youtube/dpe-IrmhfPY','export/Kriticke_mysleni/EXPORT/05'


compare = CompareByMFCC(workdir)
compare.run(matches_path, out_matches_path)
# print(compare.get_offset(idy, idb))
# print()

