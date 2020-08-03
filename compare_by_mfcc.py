import os, time
from api.tools import Tools as t
from file_to_mfcc import FileToMFCC
from file_to_video_vector import FileToVideoVector
from api.offset_calc import OffsetCalc
from tqdm import tqdm
# from match_by_duration import MatchByDuration
import random
import shutil

MIN_CORR_SCORE = 0
a_filename = 'distances.npy'
v_filename = 'video_vector.npy'

OVERWRITE_A = False
OVERWRITE_V = False

DISCS = ['ongoing', 'incoming', 'data-1', 'data-2', 'data-3']


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
        self.file2mfcc = FileToMFCC(workdir)
        # self.file2video_vector = FileToVideoVector(workdir)
        process_list = []
        for ida, match in self.matches.items():
            for idb, match_item in match.idb_items.items():
                process_list.append((ida, idb))
        random.shuffle(process_list)

        for idx in tqdm(range(len(process_list)), ascii=True, desc='process {} lines'.format(len(process_list))):
            idy, ide = process_list[idx]
            y_info = t.load_json(os.path.join(workdir, idy, 'info.json'))
            e_info = t.load_json(os.path.join(workdir, ide, 'info.json'))
            if None in [y_info, e_info]:
                print('ERR', idy, ide)
                continue
            y_a_path, y_v_path = self.get_vectors(idy, y_info)
            e_a_path, e_v_path = self.get_vectors(ide, e_info)


            # offset = self.get_offset(idy=idy, ide=ide)
            # self.matches[ida].idb_items[idb].offset = offset
        # t.save_pickle(self.out_matches_path, self.matches)

    # def get_offset(self, idy, ide, y_info=None, e_info=None):
    #     y_info = y_info if y_info is not None else self.get_info(idy)
    #     e_info = e_info if e_info is not None else self.get_info(ide)
    #
    #     if None in [y_info, e_info]:
    #         return None
    #
    #     print(ide, idy)
    #     file2mfcc = FileToMFCC(workdir)
    #     # file2video_vector = FileToVideoVector(workdir)
    #
    #     t0 = time.time()
    #     print('y_a_path')
    #
    #
    #     y_a_path = file2mfcc.run(y_info['src'], idy)
    #     t1 = time.time()
    #     print('... {:0.2f}', t1 - t0)
    #     print('e_a_path')
    #     e_a_path = file2mfcc.run(e_info['src'], ide)
    #     t2 = time.time()
    #     print('... {:0.2f}', t2 - t1)
    #
    #     print('y_v_path')
    #     # y_v_path = file2video_vector.run(y_info['src'], idy)
    #     t3 = time.time()
    #     print('... {:0.2f}', t3 - t2)
    #     print('e_v_path')
    #     # e_v_path = file2video_vector.run(e_info['src'], ide)
    #     t4 = time.time()
    #     print('... {:0.2f}', t4 - t3)
    #     if None in [y_a_path, e_a_path]:
    #         return None
    #     offset, score = self._correlate(y_a_path, e_a_path, y_info['duration'], e_info['duration'])
    #
    #     # print(y_v_path, e_v_path)
    #     if None in [score, offset]:
    #         return None
    #     if score > MIN_CORR_SCORE:
    #         return offset
    #     else:
    #         return None
    #
    #
    #     #TODO: vytvorit video vektor stejne jakko audio a pripravit do __init__
    #     # pak fce na porovnani vektoru - asi bude stejna pro audio i pro video jen s preskalovanim casu. Audio vektor podvzorkovat na 25fps?
    #     # ve finalne projet kratkym oknem a sledovat odchylku mezi vektory. Pokud nekde velky rozdil -> video neni shodne.
    #     # bylo by fajn pred porovnavanim udelat dynamic time wrapping obou vektoru a spravne je na sebe napasovat

    @staticmethod
    def get_src_path(src):
        if not os.path.isfile(src):
            for disc in DISCS:
                src_split = src.split('/')
                if src_split[2] == disc:
                    continue
                src_split[2] = disc
                new_src = '/'.join(src_split)
                if os.path.isfile(new_src):
                    print('{} -> {}'.format(src, new_src))
                    src = new_src
                    break
        
        return src

    @staticmethod
    def get_tmp_src(id_key, src):

        tmp_path = os.path.join(workdir, id_key, os.path.basename(src))

        return tmp_path

    def get_vectors(self, id_key, info):
        # print(id_key)
        src_tmp = self.get_tmp_src(id_key, info['src'])
        a_path = os.path.join(workdir, id_key, a_filename)
        run_audio = not os.path.isfile(a_path) or OVERWRITE_A

        v_path = os.path.join(workdir, id_key, v_filename)
        # run_video = not os.path.isfile(v_path) or OVERWRITE_V

        if run_audio:
            t_copy = time.time()
            print('copy', info['src'])
            shutil.copyfile(info['src'], src_tmp)
            print('... {:0.2f}', time.time() - t_copy)

        if run_audio:
            print('a_path')
            t_a = time.time()
            a_path = self.file2mfcc.run(src_tmp, a_path)
            t2 = time.time()
            print('... {:0.2f}', time.time() - t_a)

        # if run_video:
        #     print('v_path')
        #     t_v = time.time()
        #     v_path = self.file2video_vector.run(src_tmp, v_path)
        #     t3 = time.time()
        #     print('... {:0.2f}', time.time() - t_v)

        if os.path.isfile(src_tmp):
            if 'jabba' not in src_tmp:
                print('remove', src_tmp)
                os.remove(src_tmp)
            else:
                raise('ERROR - jabba in src_tmp')
        return a_path, v_path

    def get_info(self, id):
        info_path = os.path.join(self.workdir, id, 'info.json')
        info = t.load_json(info_path)
        if info is None:
            print('cannot read ', info_path)
        return info
         
    def _correlate(self, y_path, e_path, y_dur, e_dur):
        '''
        korelace dvou mfcc prubehu - ziskat maximalni moznou presnost (overit jestli to delam v autosyncu dobre)
        '''


        # print(y_info['src'], e_info['src'], y_dur, e_dur)
        return self.offset_calc.calculate(y_path, y_dur, e_path, e_dur)


    
#
# workdir = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir'
# matches_path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/matches_100.pickle'
# out_matches_path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/matches_100_offsets.pickle'
#
# idy, idb = 'youtube/k0PCNQS6OQY','export/Metaprednaska_3/EXPORT/Metaprednáška 3'
# idy, idb = 'youtube/O027XaoSaTc','export/Metaprednaska_2/EXPORT/meta2'
# idy, idb = 'youtube/iSoyfaMPvnE','export/4/EXPORT/Metaprednaska_4_oprava'
# idy, idb = 'youtube/jmg02wCJD5M','export/Metaprednaska_1/EXPORT/Prokrastinácia_meta_prednaska_oprava'
# # idy, idb = 'youtube/BrawnBoqeqM','export/1838/EXPORT/In-House/D2 E451b_04-Porter'
# idy, idb = 'youtube/qkOMs4VPcYw','export/Kriticke_mysleni/EXPORT/01'
# idy, idb = 'youtube/_MLwgyCpFI4','export/1672/EXPORT/D2_Sall2_Angelika_Inglsperger_v1'
# idy, idb = 'youtube/KmuV4I1D6xQ','export/1877/EXPORT/D2-D6_Seaside_Ballroom/D6_Andrej'
# # idy, idb = 'youtube/Ovw_rA9DaSk','export/1732/EXPORT/PIP/top_5_data_trends_of-brad_want'
# # idy, idb = 'youtube/_PyR1Ml70Rg','export/Webexpo/EXPORT/Cennydd Bowles'
# # idy, idb = 'youtube/9KkelKEunJo','export/ZeroWaste/EXPORT/1'
# # idy, idb = 'youtube/WZFYwjoGjOk','export/1007/EXPORT/Day 2 + 3 - Seattle 1 - Jakub/01 - seal'
# # idy, idb = 'youtube/SkZoUo2zYEI','export/1045/EXPORT/DeWolf_v03'
# # idy, idb = 'youtube/OJiXVnsF1ks','export/1086/EXPORT/LMC_01'
# # idy, idb = 'youtube/MSAcrpxvvqw','export/832/EXPORT/day 3/Day3_TopCongressHall_1515_Chris_Bache_v02'
# # idy, idb = 'youtube/FBnp9HPNHuM','export/Kriticke_mysleni/EXPORT/06'
# # idy, idb = 'youtube/K9lR_9fBb5c','export/1258/EXPORT/D2-Auditorium-Keynotes/07-arima'
# # idy, idb = 'youtube/bszNdUq8Rh8','export/ZeroWaste/EXPORT/234_v2'
# # idy, idb = 'youtube/hrrPsnGc9Rg','export/1010/EXPORT/fireside_chat'
# # idy, idb = 'youtube/AVMJe0fReAM','export/1913/EXPORT/D2/07.Interview'
# # idy, idb = 'youtube/PPEgY50n4Yc','export/ZeroWaste/EXPORT/6'
# # idy, idb = 'youtube/qKX94hMTrQA','export/582/EXPORT/D2-3Huyen_v2'
# # idy, idb = 'youtube/UAA3f7IUDsM','export/BB/EXPORT/BB_09'
# # idy, idb = 'youtube/4Sg8PYbMzKQ','export/Klic_k_rozvoji_talentu/EXPORT/09'
#
# idy, idb = 'youtube/dpe-IrmhfPY','export/Kriticke_mysleni/EXPORT/05'




# export_path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/export_to_process.json'
# youtube_path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/youtube_to_process.json'
workdir = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir'
matches_path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/matches_popular_from2017.pickle'
out_matches_path = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir/matches_popular_from2017_offsets.pickle'

compare = CompareByMFCC(workdir)
compare.run(matches_path, out_matches_path)
# print(compare.get_offset(idy, idb))
# print()

