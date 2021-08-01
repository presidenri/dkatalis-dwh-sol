import pandas as pd
from functools import reduce
from tabulate import tabulate

from task_1 import get_hist_data


if __name__ == "__main__":
    print("==== TASK 2 HAS STARTED ====")

    data_accounts = get_hist_data(r'./data/accounts/').rename(
        columns={"id": "account_global_id",
                 "card_id": "account_card_id",
                 "savings_account_id": "account_savings_account_id"})
    data_cards = get_hist_data(r'./data/cards/').rename(
        columns={"id": "card_global_id",
                 "status": "card_status"})
    data_savings_accounts = get_hist_data('./data/savings_accounts/').rename(
        columns={"id": "savings_account_global_id",
                 "status": "savings_account_status"})

    # Get Cards data with their respective account_id
    df_ca = pd.merge(data_cards,
                     data_accounts[['account_global_id', 'account_card_id']],
                     left_on=['card_id'],
                     right_on=['account_card_id'], how='left').drop_duplicates()

    # Get Savings Account data with their respective account_id
    df_sa = pd.merge(data_savings_accounts,
                     data_accounts[['account_global_id', 'account_savings_account_id']],
                     left_on=['savings_account_id'],
                     right_on=['account_savings_account_id'], how='left').drop_duplicates()

    # Forward fill all timestamps with the events respective to their Account ID
    data_frames = [data_accounts,
                   df_ca.drop(['account_card_id'], axis=1),
                   df_sa.drop(['account_savings_account_id'], axis=1)]
    df_ts = reduce(
        lambda left, right: pd.merge(left, right, on=['ts', 'account_global_id'], how='outer'),
        data_frames).sort_values(['account_global_id', 'ts']).groupby(['account_global_id']).fillna(method='ffill')

    # Add Account Global ID field to Account TS
    df_gaccount = pd.merge(df_ts[['ts', 'account_id']],
                           data_accounts[['ts', 'account_id', 'account_global_id']],
                           left_on=['ts', 'account_id'],
                           right_on=['ts', 'account_id'], how='outer').fillna(method='ffill')

    # Fill every timestamps with the other Account information
    df_ts_accounts = pd.merge(df_ts,
                              df_gaccount,
                              left_on=['ts', 'account_id'],
                              right_on=['ts', 'account_id'], how='outer')

    # Create a clean Card DF respective to the Account TS events
    df_clean_cards = pd.merge(df_ts_accounts,
                              df_ca[['ts', 'account_global_id']],
                              left_on=['ts', 'account_global_id'],
                              right_on=['ts', 'account_global_id'], how='left').loc[
        df_ts_accounts['account_card_id'].str.len() > 0]

    # Join Account TS history DF with the cleaned Cards DF
    df_acc_cards = pd.merge(df_ts_accounts.drop(['card_global_id',
                                                 'card_id',
                                                 'card_number',
                                                 'credit_used',
                                                 'monthly_limit',
                                                 'card_status'], axis=1),
                            df_clean_cards[['ts',
                                            'account_global_id',
                                            'card_global_id',
                                            'card_id',
                                            'card_number',
                                            'credit_used',
                                            'monthly_limit',
                                            'card_status']],
                            left_on=['ts', 'account_global_id'],
                            right_on=['ts', 'account_global_id'], how='left').sort_values('ts')

    # Join Account TS DF + cleaned Cards DF + Savings Account DF
    df_acc_savings = pd.merge(df_acc_cards,
                              df_sa[['ts', 'account_global_id']],
                              left_on=['ts', 'account_global_id'],
                              right_on=['ts', 'account_global_id'], how='left').sort_values('ts')

    # Choose the fields to show
    df_dwh = df_acc_savings[['ts',
                             'account_global_id',
                             'account_id',
                             'name',
                             'address',
                             'phone_number',
                             'email',
                             'account_card_id',
                             'card_global_id',
                             'card_id',
                             'card_number',
                             'credit_used',
                             'monthly_limit',
                             'card_status',
                             'savings_account_global_id',
                             'account_savings_account_id',
                             'balance',
                             'interest_rate_percent',
                             'savings_account_status'
                             ]].rename(columns={"account_card_id": "card_id",
                                                "account_savings_account_id": "savings_account_id"})
    print(tabulate(df_dwh, headers='keys', tablefmt='psql'))

    print("==== TASK 2 HAS FINISHED ====")
