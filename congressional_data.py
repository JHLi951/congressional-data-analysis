from congress import Congress
import credentials
import pprint
import requests
import matplotlib.pyplot as plt


PPC_BASE_URL = 'https://api.propublica.org/congress'
FEC_BASE_URL = 'https://api.open.fec.gov'
VERSION = '/v1'
CONGRESS_NO = 116
congress = Congress(credentials.API_KEY)

def get(end):

    url = PPC_BASE_URL + VERSION + end
    headers = {'X-API-Key': credentials.PPC_API_KEY}
    response = requests.get(url, headers=headers)

    return response

def get_member_list(congress, chamber):

    response = get(f'/{congress}/{chamber}/members.json')
    mem_list = response.json()
    mem_list = mem_list['results'][0]

    return mem_list


def get_senator_list():
    senators = congress.members.filter('senate', congress=CONGRESS_NO)
    senator_list = []
    for senator in senators[0]['members']:
        first_name = senator['first_name']
        last_name = senator['last_name']
        party_affiliation = senator['party']
        member_id = senator['id']
        if senator['in_office'] == True:
            senator_list.append((first_name + " " + last_name, party_affiliation, member_id))
    return senator_list


def get_representative_list():
    representatives = congress.members.filter('house', congress=CONGRESS_NO)
    representative_list = []
    for representative in representatives[0]['members']:
        first_name = representative['first_name']
        last_name = representative['last_name']
        party_affiliation = representative['party']
        member_id = representative['id']
        if representative['in_office'] == True:
            representative_list.append((first_name + " " + last_name, party_affiliation, member_id))
    return representative_list


def get_member_id(name):
    senators = get_senator_list()
    reps = get_representative_list()

    for n, p, i in senators:
        if name == n:
            return i
    for n, p, i in reps:
        if name == n:
            return i
    return 0


def get_specific_member(name):
    
    member_id = get_member_id(name)
    response = get(f'/members/{member_id}.json')
    mem_info = response.json()
    mem_info = mem_info['results'][0]

    return mem_info


# Takes a single name or a list of names and returns a dictionary
# of names mapped to their yearly office spending.
# Currently only works for House members due to the limitations of ProPublica
def get_yearly_expense(name):
    spending = {}

    if isinstance(name, list):
        for person in name:

            mem_id = get_member_id(person)
            response = get(f'/members/{mem_id}/office_expenses/2018/4.json')
            spending_info = response.json()

            for category in spending_info['results']:
                if category['category_slug'] == "total":
                    spending[person] = category['year_to_date']
    else:
        
        mem_id = get_member_id(name)
        response = get(f'/members/{mem_id}/office_expenses/2018/4.json')
        spending_info = response.json()

        for category in spending_info['results']:
            if category['category_slug'] == "total":
                spending[name] = category['year_to_date']

    return spending


def bargraph(dictionary, xlabel, ylabel, title):

    x = dictionary.keys()
    y = dictionary.values()

    plt.bar(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def get_perfect_voters():
    perfects = congress.votes.perfect('senate', congress=CONGRESS_NO)
    perfect_voters = []
    for perfect_voter in perfects['members']:
        name = perfect_voter['name']
        party_affiliation = perfect_voter['party']
        mem_id = perfect_voter['id']
        perfect_voters.append((name, party_affiliation, mem_id))
    return perfect_voters


def get_Democrats():

    senators = get_senator_list()
    representatives = get_representative_list()
    senate_democrats = [senator for senator in senators if senator[1] == "D"]
    house_democrats = [rep for rep in representatives if rep[1] == "D"]
    congress_democrats = senate_democrats + house_democrats

    return congress_democrats


def get_vote_history(name):

    mem_id = get_member_id(name)
    response = get(f'/members/{mem_id}/votes.json')

    pprint.pprint(response.json())


def get_committees(name):

    mem_id = get_member_id(name)
    response = get(f'/members/{mem_id}.json')
    mem_hist = response.json()

    committees = []
    sub_committees = []

    for i in mem_hist['results'][0]['roles']:
        for c in i['committees']:
            committees.append(c['name'])
        for sc in i['subcommittees']:
            sub_committees.append(sc['name'])

    print("Committee List")
    print("~~~~~~~~~~~~~~")
    print(committees)
    print()
    print("Sub-committee List")
    print("~~~~~~~~~~~~~~")
    print(sub_committees)

