from congress import Congress
import credentials
import pprint
import requests


PPC_BASE_URL = 'https://api.propublica.org/congress'
FEC_BASE_URL = 'https://api.open.fec.gov'
VERSION = '/v1'
CONGRESS_NO = 116
congress = Congress(credentials.API_KEY)


def get_senator_list():
    senators = congress.members.filter('senate', congress=CONGRESS_NO)
    senator_list = []
    for senator in senators[0]['members']:
        first_name = senator['first_name']
        last_name = senator['last_name']
        party_affiliation = senator['party']
        member_id = senator['id']
        # print(f'{first_name} {last_name}, {party_affiliation}, {member_id}')
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
        # print(f'{first_name} {last_name}, {party_affiliation}, {member_id}')
        if representative['in_office'] == True:
            representative_list.append((first_name + " " + last_name, party_affiliation, member_id))
    return representative_list

def get_perfect_voters():
    perfects = congress.votes.perfect('senate', congress=CONGRESS_NO)

    for perfect_voter in perfects['members']:
        name = perfect_voter['name']
        party_affiliation = perfect_voter['party']
        print(f'{name}, {party_affiliation}')

# def get_member_info():

def get_Democrats():
    

    senators = get_senator_list()
    representatives = get_representative_list()
    senate_democrats = [senator for senator in senators if senator[1] == "D"]
    house_democrats = [rep for rep in representatives if rep[1] == "D"]
    congress_democrats = senate_democrats + house_democrats

    print("Senate democrats: " + str(len(senate_democrats)))
    print("House democrats: " + str(len(house_democrats)))

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

def get_vote_history(mem_id):
    url = PPC_BASE_URL + VERSION + f'/members/{mem_id}/votes.json'
    headers = {'X-API-Key': credentials.PPC_API_KEY}
    response = requests.get(url, headers=headers)

    pprint.pprint(response.json())

def get_committee_history(mem_id):
    url = PPC_BASE_URL + VERSION + f'/members/{mem_id}.json'
    headers = {'X-API-Key': credentials.PPC_API_KEY}
    response = requests.get(url, headers=headers)
    mem_hist = response.json()
    mem_hist = trim_response(mem_hist)

    committees = []
    sub_committees = []

    for i in mem_hist['roles']:
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

def trim_response(response):
    return response['results'][0]


# print(get_member_id("Nancy Pelosi"))
get_committee_history(get_member_id("Alexandria Ocasio-Cortez"))