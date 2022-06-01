
from pubs import Pub, CustomedAuthor, CONFERENCES, CONFERENCES_SHORT, AREA_TITLES, PUB_SHORT


local_data = '''
Changjiang Li, Li Wang, Shouling Ji, Xuhong Zhang, Zhaohan Xi, Shanqing Guo, and Ting Wang	Seeing is Living? Rethinking the Security of Facial Liveness Verification in the Deepfake Era	USENIX Security 2022
Ren Pang, Zhaohan Xi, Shouling Ji, Xiapu Luo, and Ting Wang	On the Security Risks of AutoML	USENIX Security 2022
Chong Fu, Xuhong Zhang, Shouling Ji, Jinyin Chen, Jingzheng Wu, Shanqing Guo, Jun Zhou, Alex X. Liu, and Ting Wang	Label Inference Attacks Against Vertical Federated Learning	USENIX Security 2022
Yuhao Mao, Chong Fu, Saizhuo Wang, Shouling Ji, Xuhong Zhang, Zhenguang Liu, Jun Zhou, Alex X. Liu, Raheem Beyah, and Ting Wang	Transfer Attacks Revisited: A Large-Scale Empirical Study in Real Computer Vision Settings	IEEE S&P 2022
Jialuo Chen, Jingyi Wang, Tinglan Peng, Youcheng Sun, Peng Cheng, Shouling Ji, Xingjun Ma, Bo Li, and Dawn Song	Copy, Right? A Testing Framework for Copyright Protection of Deep Learning Models	IEEE S&P 2022
Chenyang Lyu, Shouling Ji, Xuhong Zhang, Hong Liang, Binbin Zhao, Kangjie Lu, and Reheem Beyah	EMS: History-Driven Mutation for Coverage-based Fuzzing	NDSS 2022
Yiming Wu, Zhiyuan Xie, Shouling Ji, Zhenguang Liu, Xuhong Zhang, Changting Lin, Shuiguang Deng, Jun Zhou, Ting Wang, and Raheem Beyah	Fraud-agents Detection in Online Microfinance: A Large-scale Empirical Study	IEEE Transactions on Dependable and Secure Computing (TDSC)
Yiming Wu, Qianjun Liu, Xiaojing Liao, Shouling Ji, Peng Wang, Xiaofeng Wang, Chunming Wu, and Zhao Li	Price TAG: Towards Semi-Automatically Discovery Tactics, Techniques and Procedures OF E-Commerce Cyber Threat Intelligence	IEEE Transactions on Dependable and Secure Computing (TDSC)
'''


def LoadLocalData():
    '''
    out:
        [ Pub class { .authors:list, .year:str, .venue:str, .title:str }, ... ]
    '''
    out_1 = []

    for l_2 in local_data.split('\n'):
        if(not l_2): continue
        pre_result_2 = l_2.split('\t')
        authors_2 = pre_result_2[0]
        title_2 = pre_result_2[1]
        venue_2 = pre_result_2[2]
        
        authors_list_2 = [ i.strip() for i in authors_2.split(',') ]
        authors_list_2[-1] = authors_list_2[-1][4:]


        for v_3 in list(PUB_SHORT.values()) + ['NDSS']:
            if v_3 in venue_2:
                venue_2 = v_3

        out_1.append(Pub(authors_list_2, title_2, venue_2, 2022))
    return out_1

if __name__ == '__main__':
    LoadLocalData()
