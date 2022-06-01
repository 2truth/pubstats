#!/usr/bin/python3

# Security conference abbreviations
# booktitle: AsiaCCS
# booktitle: CCS
# booktitle: CODASPY
# booktitle: WOOT
# booktitle: USENIX Security Symposium
# booktitle: NDSS
# booktitle: EuroS&amp;P
# booktitle: USENIX Annual Technical Conference
# booktitle: RTSS
# booktitle: DIMVA
# booktitle: OSDI
# booktitle: ESORICS
# booktitle: IEEE Symposium on Security and Privacy

# check out https://github.com/emeryberger/CSrankings/blob/gh-pages/filter.xq for conference names

CONFERENCES = {
    'sys_arch': ['ASPLOS', 'ISCA', 'MICRO', 'HPCA'],
    'sys_net': ['SIGCOMM', 'NSDI'],
    'sys_sec': ['CCS', 'ACM Conference on Computer and Communications Security', 'USENIX Security', 'USENIX Security Symposium', 'NDSS', 'IEEE Symposium on Security and Privacy'],
    'sys_db': ['SIGMOD Conference', 'VLDB', 'PVLDB', 'Proc. VLDB Endow.', 'ICDE', 'PODS'],
    'sys_design': ['DAC', 'ICCAD'],
    'sys_embed': ['EMSOFT', 'RTAS', 'RTSS'],
    'sys_hpc': ['HPDC', 'ICS', 'SC'],
    'sys_mob': ['MobiSys', 'MobiCom', 'MOBICOM', 'SenSys'],
    'sys_mes': ['IMC', 'Internet Measurement Conference', 'Proc. ACM Meas. Anal. Comput. Syst.'],
    'sys_os': ['SOSP', 'OSDI', 'EuroSys', 'USENIX Annual Technical Conference', 'USENIX Annual Technical Conference, General Track', 'FAST'],
    'sys_pl': ['PLDI', 'POPL', 'ICFP', 'OOPSLA', 'OOPSLA/ECOOP'],
    'sys_se': ['SIGSOFT FSE', 'ESEC/SIGSOFT FSE', 'ICSE', 'ICSE (1)', 'ICSE (2)', 'ASE', 'ISSTA'],
}

CONFERENCES_NUMBER = {
    'sys_arch': {},
    'sys_net': {},
    'sys_sec': {'IEEE Trans. Dependable Secur. Comput.', 'IEEE Trans. Inf. Forensics Secur.'},
    'sys_db': {},
    'sys_design': {},
    'sys_embed': {},
    'sys_hpc': {},
    'sys_mob': {},
    'sys_mes': {},
    'sys_os': {},
    'sys_pl': {'Proc. ACM Program. Lang.' : ['POPL', 'OOPSLA', 'ICFP']},
    'sys_se': {}
}

CONFERENCES_SHORT = {
    'sys_arch': ['ASPLOS', 'ISCA', 'MICRO', 'HPCA'],
    'sys_net': ['SIGCOMM', 'NSDI'],
    'sys_sec': ['CCS', 'USENIX Security', 'NDSS', 'Oakland'],
    'sys_db': ['SIGMOD', 'VLDB', 'ICDE', 'PODS'],
    'sys_design': ['DAC', 'ICCAD'],
    'sys_embed': ['EMSOFT', 'RTAS', 'RTSS'],
    'sys_hpc': ['HPDC', 'ICS', 'SC'],
    'sys_mob': ['MobiSys', 'MobiCom', 'SenSys'],
    'sys_mes': ['IMC', 'SIGMETRICS'],
    'sys_os': ['SOSP', 'OSDI', 'EuroSys', 'USENIX ATC', 'FAST'],
    'sys_pl': ['PLDI', 'POPL', 'ICFP', 'OOPSLA'],
    'sys_se': ['FSE', 'ICSE', 'ASE', 'ISSTA'],
}

PUB_SHORT = {
    'CCS': 'ACM CCS', 
    'ACM Conference on Computer and Communications Security': 'ACM CCS', 
    'USENIX Security Symposium': 'USENIX Security', 
    'IEEE Symposium on Security and Privacy': 'IEEE S&P',
    'IEEE Trans. Dependable Secur. Comput.': 'TDSC',
    'IEEE Trans. Inf. Forensics Secur.': 'TIFS'
}

AREA_TITLES = {
    'sys_arch': 'Systems: Architecture',
    'sys_net': 'Systems: Networks',
    'sys_sec': 'Systems: Security',
    'sys_db': 'Systems: Databases',
    'sys_design': 'Systems: Design',
    'sys_embed': 'Embedded Systems',
    'sys_hpc': 'Systems: HPC',
    'sys_mob': 'Mobile Systems',
    'sys_mes': 'Systems: Measurements',
    'sys_os': 'Systems: OS',
    'sys_pl': 'Systems: Programming Languages',
    'sys_se': 'Systems: Software Engineering',
    'sys': 'All Areas'
}

class Pub():
    def __init__(self, authors_, title_, venue_, year_):
        self.venue = venue_
        self.title = title_
        self.authors = authors_
        self.year = year_
        #print('{} {} {} {}\n'.format(authors, year, venue, title))

class Author():
    def __init__(self, name, aux_data):
        self.name = name
        self.years = {}
        self.nr_authors_year = {}
        self.venues = []
        self.normalized_pubs = {}
        self.affiliation, self.homepage, self.scholar = aux_data

    def add_norm_area(self, year, fraction):
        if not year in self.normalized_pubs:
            self.normalized_pubs[year] = 0
        self.normalized_pubs[year] += fraction

    def add_publication(self, venue, year, title, authors):
        if not year in self.years:
            self.years[year] = 0
            self.nr_authors_year[year] = []
        self.years[year] += 1
        self.nr_authors_year[year].append(len(authors))

        if not venue in self.venues:
            self.venues.append(venue)

    def get_total(self):
        return sum(self.years.values())

class CustomedAuthor():
    def __init__(self, name_:str, aux_data_, bottom_year_=2017):
        self.name = name_
        self.pubs = []
        self.pubs_set = set()
        self.total = 0
        self.years_num = {} # { 'year1': num, ... }
        self.venues_num = {} # { 'venue1': num, ... }
        self.year_filter_venues_num = {} # {'venue1': num }
        self.university, self.homepage, self.google_scholar = aux_data_
        self.filter_year = bottom_year_
    
    def SetBottomYear(year_:int):
        self.filter_year = year_

    def AddPublication(self, authors_:list, title_:str, venue_:str, year_:str):
        if title_ in self.pubs_set: return
        self.pubs_set.add(title_)

        self.total += 1
        
        if year_ not in self.years_num:
            self.years_num[year_] = 0
        self.years_num[year_] += 1
        
        self.pubs.append(Pub(authors_, title_, venue_, year_))

        if venue_ not in self.venues_num:
            self.venues_num[venue_] = 0
            self.year_filter_venues_num[venue_] = 0
        self.venues_num[venue_] += 1
        if year_ >= self.filter_year:
            self.year_filter_venues_num[venue_] += 1



if __name__ == '__main__':
    print('Nothing to see here, move along...')
