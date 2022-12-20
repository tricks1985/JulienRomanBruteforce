
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

url = "https://api.thegraph.com/subgraphs/id/QmfUK2Adp2bDcfwrc3joUVtfBHxKbz6hBa1MqGYSuD3zFR"

session = requests.Session()
retries = Retry(
    total = 5,
    backoff_factor = 0.5,
    status_forcelist = [413, 429, 495, 500, 502, 503, 504]
)
session.mount('https://', HTTPAdapter(max_retries=retries))

# get addr which:

# - received between 5 and 500 LINK
# - received LINK 3 times or less
# - sent LINK 3 times or less

query = """
query($lastID: String) {
    exampleEntities(
        first: 1000,
        where :{
            id_gt: $lastID,
            valueReceived_gte:   "5000000000000000000",
            valueReceived_lte: "500000000000000000000",
            countInitiatedTx_lte: 3,
            countReceivedTx_lte: 3,
        }
    )
    {
        id
    }
}
"""

def runQuery(lastId):

    response = session.request(
        'POST',
        url,
        json={
            'query': query,
            'variables': {'lastID':lastId},
        }
    )

    return response.json()


lastId=''

while True:

    # query the API with the lastId
    result = runQuery(lastId)

    # if no results, end the loop
    if not len(result['data']['exampleEntities']):
        break

    lastId = result['data']['exampleEntities'][-1]['id']

    with open("1_theGraphAddr.txt", "a") as file:
        for addr in result['data']['exampleEntities']:
            file.write(addr['id']+"\n")
