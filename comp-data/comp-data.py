from bs4 import BeautifulSoup as bs
import requests
import pandas as pd


'''
Valuation data generator (v.0.0.1)
=======================================================================
The valuation_data package provides access ot the comparables data 
provided by Aswath Damodaran on his website. Specifically, the library
generates pandas DataFrames containing a variety of metrics useful when
valuing businesses or individual industries.
=======================================================================
'''


industry_name_list = ['Aerospace/Defense', 'Air Transport', 'Apparel', 
'Auto & Truck', 'Auto Parts', 'Bank (Money Center)',
'Banks (Regional)', 'Beverage (Alcoholic)', 'Beverage (Soft)', 
'Broadcasting', 'Brokerage & Investment Banking', 'Building Materials',
'Business & Consumer Services', 'Cable TV', 'Chemical (Basic)',
'Chemical (Diversified)', 'Chemical (Specialty)', 
'Coal & Related Energy', 'Computer Services', 'Computers/Peripherals', 
'Construction Supplies', 'Diversified', 'Drugs (Biotechnology)', 
'Drugs (Pharmaceutical)', 'Education', 'Electrical Equipment', 
'Electronics (Consumer & Office)', 'Electronics (General)', 
'Engineering/Construction', 'Entertainment', 
'Environmental & Waste Services', 'Farming/Agriculture', 
'Financial Svcs. (Non-bank & Insurance)', 'Food Processing', 
'Food Wholesalers', 'Furn/Home Furnishings', 
'Green & Renewable Energy', 'Healthcare Products', 
'Healthcare Support Services', 'Heathcare Information and Technology', 
'Homebuilding', 'Hospitals/Healthcare Facilities', 'Hotel/Gaming', 
'Household Products', 'Information Services', 'Insurance (General)', 
'Insurance (Life)', 'Insurance (Prop/Cas.)', 
'Investments & Asset Management', 'Machinery', 'Metals & Mining', 
'Office Equipment & Services', 'Oil/Gas (Integrated)', 
'Oil/Gas (Production and Exploration)', 'Oil/Gas Distribution', 
'Oilfield Svcs/Equip.', 'Packaging & Container',
'Paper/Forest Products', 'Power', 'Precious Metals',
'Publishing & Newspapers', 'R.E.I.T.', 'Real Estate (Development)',
'Real Estate (General/Diversified)', 
'Real Estate (Operations & Services)', 'Recreation', 'Reinsurance', 
'Restaurant/Dining', 'Retail (Automotive)', 'Retail (Building Supply)', 
'Retail (Distributors)', 'Retail (General)', 
'Retail (Grocery and Food)', 'Retail (Online)', 
'Retail (Special Lines)', 'Rubber& Tires', 'Semiconductor', 
'Semiconductor Equip', 'Shipbuilding & Marine', 'Shoe', 
'Software (Entertainment)', 'Software (Internet)', 
'Software (System & Application)', 'Steel', 'Telecom (Wireless)', 
'Telecom. Equipment', 'Telecom. Services', 'Tobacco', 'Transportation', 
'Transportation (Railroads)', 'Trucking', 'Utility (General)', 
'Utility (Water)', 'Total Market', 'Total Market (without financials)']


def get_table(url, columns_position = 0, index = 'industry name'):
    
    '''Takes the url to a dataset provided on Aswath Damodaran's 
    website and returns a pandas dataframe storing the data

    Args:
        url(str): Value providing url
        columns_position(int): Value indicating top of the table
            (default is 0)
        index(str): Value indicating column to be turned into index
            (default is Industry Name)

    Returns:
        table_df: DataFrame object containing data
    '''

    html = requests.get(url)
    soup = bs(html.text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    
    column_list = rows[columns_position].find_all('td')
    columns = []
    for i in column_list:
        text = i.text
        text = text.replace('\n\t\t\t\t        ', ' ')
        text = text.replace('\n\t\t\t        ', ' ')
        text = text.replace('\n\t\t        ', ' ')
        text = text.replace('\n\t\t', ' ')
        text = text.replace('\n\t', ' ')
        text = text.replace('\n        ', ' ')
        text = text.replace('\n      ', ' ')
        text = text.replace('\t', ' ')
        text = text.replace('       ',' ')
        text = text.replace('    ', '')
        text = text.replace('   ', '')
        columns.append(text.lower())

    table_df = pd.DataFrame(columns = columns)
    rows = rows[columns_position + 1:]
    for row in rows:
        entries = row.find_all('td')
        lst = []
        for i in entries:
            text = i.text
            text = text.replace('\n\t\t\t\t        ', ' ')
            text = text.replace('\n\t\t\t        ', ' ')
            text = text.replace('\n\t\t        ', ' ')
            text = text.replace('\n\t\t', ' ')
            text = text.replace('\n\t', ' ')
            text = text.replace('\n        ', ' ')
            text = text.replace('\n      ', ' ')
            text = text.replace('\t', ' ')
            text = text.replace('       ',' ')
            text = text.replace('    ', '')
            text = text.replace('   ', '')
            lst.append(text.lower())
        table_df.loc[len(table_df)] = lst
    table_df = table_df.iloc[columns_position + 1:]
    table_df = table_df.set_index(index.lower())
    return table_df


class Market:
    '''
    A class used to represent the overall market, providing market-
    related measures

    Args:

    Attributes:
        main_url(str): String providing the basic url to Damodaran's 
        website
        returns_url(str): String providing the url addition to the 
        returns dataset
        ...
        country_multiples_url(str): String providing url addition to 
        the country multiples dataset

    Methods:
        get_returns(): Calls get_table() to create returns DataFrame
        object
        ...
        get_country_multiples(): Calls get_table() to create country 
        multiples DataFrame object
    '''

    main_url = 'http://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/'

    # Discount rate estimation
    returns_url = 'histretSP.html'
    risk_premiums_US_url = 'histimpl.html'
    risk_premiums_other_url = 'ctryprem.html'
    country_tax_rates_url = 'countrytaxrate.html'
    risk_measures_url = 'mktcaprisk.html'
 
    # Capital structure
    macro_url = 'macro.html'

    # Multiples
    market_cap_multiples_url = 'mktcapmult.html'
    country_multiples_url = 'countrystats.html'

    def __init__(self):
        pass

    def get_returns(self):
        url = self.main_url + self.returns_url
        returns = get_table(url, 1, 'year')
        return returns # Check

    def get_risk_premiums_US(self):
        url = self.main_url + self.risk_premiums_US_url
        risk_premiums_US = get_table(url, index = 'year')
        return risk_premiums_US # Check

    def get_risk_premiums_other(self):
        url = self.main_url + self.risk_premiums_other_url
        risk_premiums_other = get_table(url, index = 'country')
        return risk_premiums_other # Check

    def get_country_tax_rates(self):
        url = self.main_url + self.country_tax_rates_url
        country_tax_rates = get_table(url, index = 'country')
        return country_tax_rates # Check

    def get_risk_measures(self):
        url = self.main_url + self.risk_measures_url
        risk_measures = get_table(url, index = 'market capitalization (decile)')
        return risk_measures # Check

    def get_macro(self):
        url = self.main_url + self.macro_url
        macro = get_table(url, index = 'date')
        return macro # Check

    def get_market_cap_multiples(self):
        url = self.main_url + self.market_cap_multiples_url
        market_cap_multiples = get_table(url, index = 'market cap decile')
        return market_cap_multiples # Check

    def get_country_multiples(self):
        url = self.main_url + self.country_multiples_url
        country_multiples = get_table(url, index = 'country')
        return country_multiples # Check


class Industry:
    '''
    A class used to represent individual industries, providing 
    industry-related measures

    Args:
        industry_name(str): Value indicating name of the industry

    Attributes:
        main_url(str): String providing the basic url to Damodaran's 
        website
        holdings_url(str): String providing the url addition to 
        holdings dataset
        ...
        standard_deviation_url(str): String providing the url addition
        to standard deviaiton dataset

    Methods:
        get_holdings(): Calls get_table() to create industry holdings 
        Series object
        ...
        get_standard_deviation(): Calls get_table() to create 
        industry standard deviation Series object
    '''

    main_url = 'http://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/'

    # Corporate governance
    holdings_url = 'inshold.html' 

    # Discount rate estimation
    betas_url = 'Betas.html'
    total_betas_url = 'totalbeta.html' 
    cost_of_capital_url = 'wacc.html'
    industry_tax_rates_url = 'taxrate.html' 

    # Dollar value measures
    dollar_values_url = 'DollarUS.html'

    # COVID effects
    covid_effects_url = 'COVIDeffects.html'

    # Return measures
    eva_url = 'EVA.html'

    # Capital structure
    debt_details_url = 'debtdetails.html'
    debt_fundamentals_url = 'dbtfund.html'
    leases_url = 'leaseeffect.html'

    # Dividend policy
    dividends_fcfe_url = 'divfcfe.html'
    dividend_fundamentals_url = 'divfund.html'

    # Cash flow estimation
    capital_expenditures_url = 'capex.html'
    margins_url = 'margin.html'
    working_capital_url = 'wcdata.html'

    # Growth rate estimation
    roe_url = 'roe.html'
    eps_growth_url = 'fundgr.html'
    historical_growth_url = 'histgr.html'
    ebit_growth_url = 'fundgrEB.html'

    # Multiples
    price_earnings_url = 'pedata.html'
    price_book_url = 'pbvdata.html'
    revenue_multiples_url = 'psdata.html'
    ev_multiples_url = 'vebitda.html'

    # Option pricing models
    standard_deviation_url = 'optvar.html'

    def __init__(self, industry_name):
        self.industry = industry_name.lower()

    def get_holdings(self):
        url = self.main_url + self.holdings_url
        holdings = get_table(url).loc[self.industry]
        return holdings # Check

    def get_betas(self):
        url = self.main_url + self.betas_url
        betas = get_table(url).loc[self.industry]
        return betas # Check

    def get_total_betas(self):
        url = self.main_url + self.total_betas_url
        total_betas = get_table(url).loc[self.industry]
        return total_betas # Check

    def get_cost_of_capital(self):
        url = self.main_url + self.cost_of_capital_url
        cost_of_capital = get_table(url).loc[self.industry]
        return cost_of_capital # Check

    def get_industry_tax_rates(self):
        url = self.main_url + self.industry_tax_rates_url
        industry_tax_rates = get_table(url, 1).loc[self.industry]
        return industry_tax_rates # Check

    def get_eva(self):
        url = self.main_url + self.eva_url
        eva = get_table(url).loc[self.industry]
        return eva # Check

    def get_debt_details(self):
        url = self.main_url + self.debt_details_url
        debt_details = get_table(url).loc[self.industry]
        return debt_details # Check

    def get_debt_fundamentals(self):
        url = self.main_url + self.debt_fundamentals_url
        debt_fundamentals = get_table(url).loc[self.industry]
        return debt_fundamentals # Check

    def get_leases(self):
        url = self.main_url + self.leases_url
        leases = get_table(url).loc[self.industry]
        return leases # Check

    def get_dividends_fcfe(self):
        url = self.main_url + self.dividends_fcfe_url
        dividends_fcfe = get_table(url).loc[self.industry]
        return dividends_fcfe # Check

    def get_capital_expenditures(self):
        url = self.main_url + self.capital_expenditures_url
        capital_expenditures = get_table(url).loc[self.industry]
        return capital_expenditures # Check

    def get_margins(self):
        url = self.main_url + self.margins_url
        margins = get_table(url, 1).loc[self.industry]
        return margins # Check

    def get_working_capital(self):
        url = self.main_url + self.working_capital_url
        working_capital = get_table(url).loc[self.industry]
        return working_capital # Check

    def get_roe(self):
        url = self.main_url + self.roe_url
        roe = get_table(url).loc[self.industry]
        return roe # Check

    def get_eps_growth(self):
        url = self.main_url + self.eps_growth_url
        eps_growth = get_table(url).loc[self.industry]
        return eps_growth # Check

    def get_historical_growth(self):
        url = self.main_url + self.historical_growth_url
        historical_growth = get_table(url).loc[self.industry]
        return historical_growth # Check

    def get_ebit_growth(self):
        url = self.main_url + self.ebit_growth_url
        ebit_growth = get_table(url).loc[self.industry]
        return ebit_growth # Check

    def get_price_earnings(self):
        url = self.main_url + self.price_earnings_url
        price_earnings = get_table(url).loc[self.industry]
        return price_earnings # Check

    def get_price_book(self):
        url = self.main_url + self.price_book_url
        price_book = get_table(url).loc[self.industry]
        return price_book # Check

    def get_revenue_multiples(self):
        url = self.main_url + self.revenue_multiples_url
        revenue_multiples = get_table(url).loc[self.industry]
        return revenue_multiples # Check

    def get_ev_multiples(self):
        url = self.main_url + self.ev_multiples_url
        ev_multiples = get_table(url, 1).loc[self.industry]
        return ev_multiples # Check

    def get_standard_deviation(self):
        url = self.main_url + self.standard_deviation_url
        standard_deviation = get_table(url).loc[self.industry]
        return standard_deviation # Check
