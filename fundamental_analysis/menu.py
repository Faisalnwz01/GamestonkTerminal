import FundamentalAnalysis as fa
from alpha_vantage.fundamentaldata import FundamentalData
import config_bot as cfg
import argparse
import datetime
from datetime import datetime
from stock_market_helper_funcs import *
import pandas as pd
import json
import requests
from pandas.io.json import json_normalize

from fundamental_analysis import alpha_vantage_api as av_api
from fundamental_analysis import financial_modeling_prep_api as fmp_api


# -----------------------------------------------------------------------------------------------------------------------
def print_fundamental_analysis(s_ticker, s_start, s_interval):
    """ Print help """

    s_intraday = (f'Intraday {s_interval}', 'Daily')[s_interval == "1440min"]

    if s_start:
        print(f"\n{s_intraday} Stock: {s_ticker} (from {s_start.strftime('%Y-%m-%d')})")
    else:
        print(f"\n{s_intraday} Stock: {s_ticker}")

    print("\nFundamental Analysis:") # https://github.com/JerBouma/FundamentalAnalysis
    print("   info        provides information on main key metrics of company")
    print("   help        show this fundamental analysis menu again")
    print("   q           quit this menu, and shows back to main menu")
    print("   quit        quit to abandon program")
    print("\nAlpha Vantage API")
    print("   overview    overview of the company")
    print("   key         main key metrics of the company")
    print("   income      income statements of the company")
    print("   balance     balance sheet of the company")
    print("   cash        cash flow of the company")
    print("   earnings    earnings dates and reported EPS")
    print("\nFinancial Modeling Prep API")
    print("   profile     profile of the company")
    print("   rating      rating of the company from strong sell to strong buy")
    print("   quote       quote of the company")
    print("   enterprise  enterprise value of the company over time")
    print("   dcf         discounted cash flow of the company over time")
    print("   income      income statements of the company")
    print("   balance     balance sheet of the company")
    print("   cash        cash flow of the company")
    print("   metrics     key metrics of the company")
    print("   ratios      financial ratios of the company")
    print("   growth      financial statement growth of the company")
    print("")
    

# ---------------------------------------------------- INFO ----------------------------------------------------
def info(l_args, s_ticker):
    parser = argparse.ArgumentParser(prog='info', 
                                     description="""Provides information about main key metrics. Namely: EBITDA,
                                     EPS, P/E, PEG, FCF, P/B, ROE, DPR, P/S, Dividend Yield Ratio, D/E, and Beta.""")
        
    try:
        (ns_parser, l_unknown_args) = parser.parse_known_args(l_args)

        if l_unknown_args:
            print(f"The following args couldn't be interpreted: {l_unknown_args}")

        filepath = 'fundamental_analysis/key_metrics_explained.txt'
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                print("{}".format(line.strip()))
                line = fp.readline()
            print("")

    except:
        print("ERROR!\n")
        return
    

# ---------------------------------------------------- MENU ----------------------------------------------------
def fa_menu(fa_parser, s_ticker, s_start, s_interval):

    print_fundamental_analysis(s_ticker, s_start, s_interval)

    # Loop forever and ever
    while True:
        # Get input command from user
        as_input = input('> ')
        
        # Parse fundamental analysis command of the list of possible commands
        try:
            (ns_known_args, l_args) = fa_parser.parse_known_args(as_input.split())

        except SystemExit:
            print("The command selected doesn't exist\n")
            continue

        if ns_known_args.fa == 'info':
            info(l_args, s_ticker)

        elif ns_known_args.fa == 'help':
            print_fundamental_analysis(s_ticker, s_start, s_interval)

        elif ns_known_args.fa == 'q':
            # Just leave the FA menu
            return False

        elif ns_known_args.fa == 'quit':
            # Abandon the program
            return True
        
        # ----------------------------------------------- ALPHA VANTAGE ----------------------------------------------
        elif ns_known_args.fa == 'overview':
            av_api.overview(l_args, s_ticker)

        elif ns_known_args.fa == 'key':
            av_api.key(l_args, s_ticker)

        elif ns_known_args.fa == 'income':
            av_api.income_statement(l_args, s_ticker)

        elif ns_known_args.fa == 'balance':
            av_api.balance_sheet(l_args, s_ticker)

        elif ns_known_args.fa == 'cash':
            av_api.cash_flow(l_args, s_ticker)

        elif ns_known_args.fa == 'earnings':
            av_api.earnings(l_args, s_ticker)

        # -------------------------------------------- FINANCIAL MODELING PREP -----------------------------------------
        # Details:
        elif ns_known_args.fa == 'profile':
            fmp_api.profile(l_args, s_ticker)

        elif ns_known_args.fa == 'rating':
            fmp_api.rating(l_args, s_ticker)

        elif ns_known_args.fa == 'quote':
            fmp_api.quote(l_args, s_ticker)
        
        elif ns_known_args.fa == 'enterprise':
            fmp_api.enterprise(l_args, s_ticker)

        elif ns_known_args.fa == 'dcf':
            fmp_api.discounted_cash_flow(l_args, s_ticker)

        # Financial statement:
        elif ns_known_args.fa == 'income':
            fmp_api.income_statement(l_args, s_ticker)

        elif ns_known_args.fa == 'balance':
            fmp_api.balance_sheet(l_args, s_ticker)

        elif ns_known_args.fa == 'cash':
            fmp_api.cash_flow(l_args, s_ticker)

        # Ratios:
        elif ns_known_args.fa == 'metrics':
            fmp_api.key_metrics(l_args, s_ticker)

        elif ns_known_args.fa == 'ratios':
            fmp_api.financial_ratios(l_args, s_ticker)

        elif ns_known_args.fa == 'growth':
            fmp_api.financial_statement_growth(l_args, s_ticker)

        # ------------------------------------------------------------------------------------------------------------
        else:
            print("Command not recognized!")