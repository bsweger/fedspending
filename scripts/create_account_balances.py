"""
Create a .csv file of U.S. federal account balances

TODO:
    Parameterize inputs such as environment and output file location
"""
import click
import json
import logging
import urllib.parse

import pandas as pd
from pandas.io.json import json_normalize
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def request_data(uri, data=None, headers=None):
    """Post a specified request to the USAspending API.

    Args:
        uri: endpoint for the POST request
        data: information to send as the request payload
        headers: request headers

    Returns:
        Response object

    """
    r = requests.post(uri, data=data, headers=headers)
    if r.status_code == requests.codes.ok:
        return r
    else:
        r.raise_for_status()


def process_data(usa_response, df):
    """Process a USAspending API response.

    Args:
        usa_response: a Response object returned by the USAspending API call
        df: the DataFrame object used to store data returned by the API call

    Returns:
        DataFrame that contains the flattened results of the API call

    TODO:
        Reconsider the recursive approach to paginating through the API results
        (to avoid hitting the recursion limit)

    """
    json_data = usa_response.json()
    # results contain nested objects: flatten everything so we can put it
    # into a dataframe
    flat_data = json_normalize(json_data['results'])
    # add data from the API call to the dataframe
    df = pd.concat([df, pd.DataFrame(flat_data)])
    # process the next page of data, if applicable
    if json_data['page_metadata']['has_next_page']:
        logger.info('Calling {}. Current df size = {}'.format(
            json_data['page_metadata']['next'], len(df.index)))
        r = request_data(uri=json_data['page_metadata']['next'])
        df = process_data(r, df)
    return df


@click.command()
@click.option('--path', default='./data/data_act_account_balances.csv', help='file path of resulting .csv')
def create_balances_csv(path):
    """Create a .csv of tas-based account balances

    Args:
        path: path where the resulting .csv should be saved

    """
    # specify the endpoint and request body for the initial API call
    df = pd.DataFrame()
    env = 'https://api.usaspending.gov/api/v1/'
    endpoint = 'tas/balances/'
    headers = {'content-type': 'application/json'}
    payload = {
        "limit": 250,
        "fields": [
            "treasury_account_identifier",
            "submission",
            "federal_account",
            "funding_toptier_agency",
            "gross_outlay_amount_by_tas_cpe",
            "adjustments_to_unobligated_balance_brought_forward_cpe",
            "budget_authority_appropriated_amount_cpe",
            "budget_authority_available_amount_total_cpe",
            "budget_authority_unobligated_balance_brought_forward_fyb",
            "obligations_incurred_total_by_tas_cpe",
            "other_budgetary_resources_amount_cpe",
            "unobligated_balance_cpe",
        ]
    }
    # Make the first request
    r = request_data(
        uri=urllib.parse.urljoin(env, endpoint),
        data=json.dumps(payload),
        headers=headers
    )
    # process the results of the API call (and any subsequent pages, if applicable)
    df = process_data(r, df)

    # write the dataframe of results to a .csv file
    df.to_csv(path, index=False)


if __name__ == '__main__':
    create_balances_csv()
