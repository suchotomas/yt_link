import os, time
from api.tools import Tools as t
from file_to_mfcc import FileToMFCC
from file_to_video_vector import FileToVideoVector
from api.offset_calc import OffsetCalc
class ComparePair:
    '''
    - podmineny vstupy dva klice (idy, ide)
    - nepodmineny vstupy: y_info, e_info,  
    '''
    def __init__(self, workdir):
        self.workdir = workdir    
        self.offset_calc = OffsetCalc()

    def init_pair(self, idy, ide, y_info=None, e_info=None):
        y_info = y_info if y_info is not None else self.get_info(idy)
        e_info = e_info if e_info is not None else self.get_info(ide)

        file2mfcc = FileToMFCC(workdir)
        file2video_vector = FileToVideoVector(workdir)

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
        self.find_offset(y_a_path, e_a_path, y_info, e_info)
        

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
         
    def find_offset(self, y_path, e_path, y_info, e_info):
        '''
        korelace dvou mfcc prubehu - ziskat maximalni moznou presnost (overit jestli to delam v autosyncu dobre)
        '''

        y_dur, e_dur = y_info['duration'], e_info['duration']

        print(y_path, e_path, y_dur, e_dur)
        print(self.offset_calc.calculate(y_path, y_dur, e_path, e_dur))


    
idy, ide = 'youtube/--hV89Eu4UM','export/1300/EXPORT/2018_06_01-katedra_aplikovane_matematiky_den_pro_zdenka_hedrlina._V3_1300mp4'
idy, ide = 'youtube/9KkelKEunJo','export/ZeroWaste/EXPORT/1'
workdir = '/mnt/data/palpatine/DATASETS/YT_LINK/workdir'

ye_list = [
    ['youtube/k0PCNQS6OQY','export/Metaprednaska_3/EXPORT/Metaprednáška 3'],
['youtube/O027XaoSaTc','export/Metaprednaska_2/EXPORT/meta2'],
['youtube/iSoyfaMPvnE','export/4/EXPORT/Metaprednaska_4_oprava'],
['youtube/jmg02wCJD5M','export/Metaprednaska_1/EXPORT/Prokrastinácia_meta_prednaska_oprava'],
['youtube/BrawnBoqeqM','export/1838/EXPORT/In-House/D2 E451b_04-Porter'],
['youtube/qkOMs4VPcYw','export/Kriticke_mysleni/EXPORT/01'],
['youtube/_MLwgyCpFI4','export/1672/EXPORT/D2_Sall2_Angelika_Inglsperger_v1'],
['youtube/KmuV4I1D6xQ','export/1877/EXPORT/D2-D6_Seaside_Ballroom/D6_Andrej'],
['youtube/Ovw_rA9DaSk','export/1732/EXPORT/PIP/top_5_data_trends_of-brad_want'],
['youtube/_PyR1Ml70Rg','export/Webexpo/EXPORT/Cennydd Bowles'],
['youtube/9KkelKEunJo','export/ZeroWaste/EXPORT/1'],
['youtube/WZFYwjoGjOk','export/1007/EXPORT/Day 2 + 3 - Seattle 1 - Jakub/01 - seal'],
['youtube/SkZoUo2zYEI','export/1045/EXPORT/DeWolf_v03'],
['youtube/OJiXVnsF1ks','export/1086/EXPORT/LMC_01'],
['youtube/MSAcrpxvvqw','export/832/EXPORT/day 3/Day3_TopCongressHall_1515_Chris_Bache_v02'],
['youtube/FBnp9HPNHuM','export/Kriticke_mysleni/EXPORT/06'],
['youtube/K9lR_9fBb5c','export/1258/EXPORT/D2-Auditorium-Keynotes/07-arima'],
['youtube/bszNdUq8Rh8','export/ZeroWaste/EXPORT/234_v2'],
['youtube/hrrPsnGc9Rg','export/1010/EXPORT/fireside_chat'],
['youtube/AVMJe0fReAM','export/1913/EXPORT/D2/07.Interview'],
['youtube/PPEgY50n4Yc','export/ZeroWaste/EXPORT/6'],
['youtube/qKX94hMTrQA','export/582/EXPORT/D2-3Huyen_v2'],
['youtube/fQ2-wl25_1A','export/Science_Cafe/EXPORT/sc'],
['youtube/dpe-IrmhfPY','export/Kriticke_mysleni/EXPORT/05'],
['youtube/UAA3f7IUDsM','export/BB/EXPORT/BB_09'],
['youtube/wqQ-2vf4Ffw','export/832/EXPORT/day 2/D2_Hall3_007_Javier-Charme-Marticorena'],
['youtube/4Sg8PYbMzKQ','export/Klic_k_rozvoji_talentu/EXPORT/09'],
['youtube/c1ApDVmrr10','export/791/EXPORT/Future_Port_Prague_7.9.2017-klip_v1-1080p'],
]
cp = ComparePair(workdir)
for idx, (idy, ide) in enumerate(ye_list):
    cp.init_pair(idy, ide)