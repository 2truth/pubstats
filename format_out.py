#!/usr/bin/python3

import pickle
import csv

from pubs import Pub, CustomedAuthor, CONFERENCES, CONFERENCES_SHORT, AREA_TITLES, PUB_SHORT

OUT_FILENAME = 'output/stat04.txt'

def FormatOut(authors_:dict, do_save_=True):
    '''
    in:
        authors: {
            'name1': Class Author1,
            ...
        }
    output: str
        "name\tuniversity\thomepage\ttotal_all_2017_2022\ttotal_conf_2017_2022\ttotal_journal_2017_2022\tieeesp_2017_\tacm_ccs\tusenix_sec\tndss\ttdsc\ttifs\t\n"   
    '''
    out_1 = 'name\tuniversity\thomepage\ttotal_all_2017_2022\ttotal_conf_2017_2022\ttotal_journal_2017_2022\tieeesp_2017_\tacm_ccs_2017_\tusenix_sec_2017_\tndss_2017_\ttdsc_2017_\ttifs_2017_\t\n'

    for name_2, author_2 in authors_.items():

        tifs_num_2 = 0 if 'TIFS' not in author_2.year_filter_venues_num else author_2.year_filter_venues_num['TIFS']
        tdsc_num_2 = 0 if 'TDSC' not in author_2.year_filter_venues_num else author_2.year_filter_venues_num['TDSC']
        sp_num_2 = 0 if 'IEEE S&P' not in author_2.year_filter_venues_num else author_2.year_filter_venues_num['IEEE S&P']
        ccs_num_2 = 0 if 'ACM CCS' not in author_2.year_filter_venues_num else author_2.year_filter_venues_num['ACM CCS']
        usenix_sec_num_2 = 0 if 'USENIX Security' not in author_2.year_filter_venues_num else author_2.year_filter_venues_num['USENIX Security']
        ndss_num_2 = 0 if 'NDSS' not in author_2.year_filter_venues_num else author_2.year_filter_venues_num['NDSS']
        
        # ndss_in_five_num_2 = 0
        # if CONFERENCES['sys_sec'][-2] in author_2.venues_num:
        #     ndss_num_2 = author_2.venues_num[CONFERENCES['sys_sec'][-2]]
        #     ndss_in_five_num_2 = author_2.year_filter_venues_num[CONFERENCES['sys_sec'][-2]]
        
        total_in_five_num_2 = 0
        for venue_3 in author_2.year_filter_venues_num:
            total_in_five_num_2 += author_2.year_filter_venues_num[venue_3]
            
        out_1 += f"{author_2.name}\t{author_2.university}\t{author_2.homepage}\t\
                    {total_in_five_num_2}\t\
                    {total_in_five_num_2-tifs_num_2-tdsc_num_2}\t\
                    {tifs_num_2+tdsc_num_2}\t\
                    {sp_num_2}\t\
                    {ccs_num_2}\t\
                    {usenix_sec_num_2}\t\
                    {ndss_num_2}\t\
                    {tdsc_num_2}\t\
                    {tifs_num_2}\n"

    if(do_save_):
        with open(OUT_FILENAME, 'w') as f:
            f.write(out_1)
        
    return out_1

def ParseAuthors(pubs_:list):
    ''' break publications into per-author statistics
    in: 
        pubs: [ Pub class { .authors:list, .year:str, .short_venue:str, .title:str }, ... ]
    output:
        authors: {
            'name1': Class Author1,
            ...
        }
    '''

    authors_1 = {}

    # Load aux data from cs rankings first
    aux_data_csrankings_1 = {}
    with open('csrankings.csv', 'r') as f:
        csvaliases = csv.reader(f)
        for row in csvaliases:
            if row[0] == 'alias':
                continue
            if row[0].find('[') != -1:
                name = row[0][0:row[0].find('[')-1]
            else:
                name = row[0]
            aux_data_csrankings_1[name] = (row[1], row[2], row[3])

    # Load aux data as parsed from DBLP (as fallback)
    with open('pickle/affiliations.pickle', 'rb') as f:
        aux_data_dblp_1 = pickle.load(f)
    
    # v = set()
    # parse pubs and split into authors
    for pub_2 in pubs_:
        # break up into authors
        for name_3 in pub_2.authors:
            if name_3 not in authors_1:
                if name_3 in aux_data_csrankings_1:
                    authors_1[name_3] = CustomedAuthor(name_3, aux_data_csrankings_1[name_3])
                elif name_3 in aux_data_dblp_1:
                    authors_1[name_3] = CustomedAuthor(name_3, aux_data_dblp_1[name_3])
                else:
                    authors_1[name_3] = CustomedAuthor(name_3, ('', '', ''))
            authors_1[name_3].AddPublication(pub_2.authors, pub_2.title, pub_2.venue, pub_2.year)
        # v.add(pub_2.venue)
    # print(v)

    return authors_1

def LoadPubs(do_save_=True)->dict:
    '''
    out: {
        'sys_sec': [ Pub class { .authors:list, .year:str, .short_venue:str, .title:str }, ... ],
        ...
    }

    '''

    all_pubs_1 = {}

    for area_2 in ['sys_sec']:
        if area_2 not in all_pubs_1:
            all_pubs_1[area_2] = []
        
        # Load pickeled data
        with open('pickle/pubs-{}.pickle'.format(area_2), 'rb') as f_2:
            pubs_2 = pickle.load(f_2)
            all_pubs_1[area_2] += pubs_2

        # import LocalData
        # all_pubs_1[area_2] += LocalData.LoadLocalData()
        
        # Normalize venue
        for pub_2 in all_pubs_1[area_2]:
            pub_2.venue = pub_2.venue if pub_2.venue not in PUB_SHORT else PUB_SHORT[pub_2.venue]
        # old_v = set()
        # short_v = set()
        if(do_save_):
            f_txt_2 = open('output/pubs-{}.txt'.format(area_2), 'w')
            out_2 = 'authors\ttitle\tvenue\tyear\n'
            for pub_3 in pubs_2:
                authors_3 = ','.join(pub_3.authors)
                short_venue_3 = pub_3.venue if pub_3.venue not in PUB_SHORT else PUB_SHORT[pub_3.venue]
                out_3 = f'{authors_3}\t{pub_3.title}\t{short_venue_3}\t{pub_3.year}\n'
                out_2 += out_3
                # old_v.add(pub_3.venue)
                # short_v.add(short_venue_3)
            f_txt_2.write(out_2)
            f_txt_2.close()
    # print(old_v)
    # print('end line')
    # print(short_v)

    return all_pubs_1


if __name__ == '__main__':
    # Load pickeled data
    all_pubs = LoadPubs()

    # Prepare per-author information
    for area in ['sys_sec']:
        authors = ParseAuthors(all_pubs[area])

    t = 'Shouling Ji'
    print('pubs:{}, years_num:{}, venues_num:{}, uni:{}, home:{}, google:{}'.format(len(authors[t].pubs), authors[t].years_num,
                                    authors[t].venues_num, authors[t].university, authors[t].homepage, authors[t].google_scholar))

    FormatOut(authors)

    