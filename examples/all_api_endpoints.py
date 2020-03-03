#!/usr/bin/env python3

from max.client import Client

if __name__ == '__main__':
    client = Client('PUY_MY_API_KEY_HERE', 'PUY_MY_API_SECRET_HERE')

    try:
        ''' Public (Read) '''
        result = client.get_public_all_currencies()
        print(f"[I] Invoked get_public_all_currencies() API Result: \n    {result}\n")

        result = client.get_public_k_line('maxtwd', 2, 60)
        print(f"[I] Invoked get_public_k_line('maxtwd', 2, 60) API Result: \n    {result}\n")

        result = client.get_public_pair_depth('maxtwd', 2)
        print(f"[I] Invoked get_public_pair_depth('maxtwd', 2) API Result: \n    {result}\n")

        result = client.get_public_server_time()
        print(f"[I] Invoked get_public_server_time() API Result: \n    {result}\n")

        result = client.get_public_withdrawal_constraints()
        print(f"[I] Invoked get_public_withdrawal_constraints() API Result: \n    {result}\n")

        # result = client.get_public_all_markets()
        # print(f"[I] Invoked get_public_all_markets() API Result: \n    {result}\n")

        # result = client.get_public_all_tickers()
        # print(f"[I] Invoked get_public_all_tickers() API Result: \n    {result}\n")

        # result = client.get_public_all_tickers('maxtwd')
        # print(f"[I] Invoked get_public_all_tickers('maxtwd') API Result: \n    {result}\n")

        # result = client.get_public_k_line('maxtwd')
        # print(f"[I] Invoked get_public_k_line('maxtwd') API Result: \n    {result}\n")

        # result = client.get_public_k_line('maxtwd', 1)
        # print(f"[I] Invoked get_public_k_line('maxtwd', 1) API Result: \n    {result}\n")

        # result = client.get_public_k_line('maxtwd', 2, 60, 1560502801)
        # print(f"[I] Invoked get_public_k_line('maxtwd', 2, 60, 1560502801) API Result: \n    {result}\n")

        # result = client.get_public_order_book('maxtwd')
        # print(f"[I] Invoked get_public_order_book('maxtwd') API Result: \n    {result}\n")

        # result = client.get_public_order_book('maxtwd', 1, 2)
        # print(f"[I] Invoked get_public_order_book('maxtwd', 1, 2) API Result: \n    {result}\n")

        # result = client.get_public_pair_depth('maxtwd')
        # print(f"[I] Invoked get_public_pair_depth('maxtwd') API Result: \n    {result}\n")

        # result = client.get_public_recent_trades('maxtwd')
        # print(f"[I] Invoked get_public_recent_trades('maxtwd') API Result: \n    {result}\n")

        # result = client.get_public_recent_trades('maxtwd', 1560509180)
        # print(f"[I] Invoked get_public_recent_trades('maxtwd', 1560509180) API Result: \n    {result}\n")

        ''' Private (Read) '''
        result = client.get_private_account_balances()
        print(f"[I] Invoked get_private_account_balances() API Result: \n    {result}\n")

        result = client.get_private_deposit_history()
        print(f"[I] Invoked get_private_deposit_history() API Result: \n    {result}\n")

        result = client.get_private_max_rewards()
        print(f"[I] Invoked get_private_max_rewards() API Result: \n    {result}\n")

        result = client.get_private_member_profile()
        print(f"[I] Invoked get_private_member_profile() API Result: \n    {result}\n")

        result = client.get_private_order_history('maxtwd', ['cancel', 'wait', 'done'])
        print(f"[I] Invoked get_private_order_history('maxtwd', ['cancel', .., 'done']) API Result: \n    {result}\n")

        result = client.get_private_reward_history()
        print(f"[I] Invoked get_private_reward_history() API Result: \n    {result}\n")

        result = client.get_private_trade_history('maxtwd')
        print(f"[I] Invoked get_private_trade_history('maxtwd') API Result: \n    {result}\n")

        result = client.get_private_transfer_history(side='out')
        print(f"[I] Invoked get_private_transfer_history(side='out') API Result: \n    {result}\n")

        result = client.get_private_withdrawal_history()
        print(f"[I] Invoked get_private_withdrawal_history() API Result: \n    {result}\n")

        # result = client.get_private_account_balance('max')
        # print(f"[I] Invoked get_private_account_balance('max') API Result: \n    {result}\n")

        # result = client.get_private_deposit_address()
        # print(f"[I] Invoked get_private_deposit_address() API Result: \n    {result}\n")

        # result = client.get_private_deposit_address('max')
        # print(f"[I] Invoked get_private_deposit_address('max') API Result: \n    {result}\n")

        # result = client.get_private_deposit_addresses()
        # print(f"[I] Invoked get_private_deposit_addresses() API Result: \n    {result}\n")

        # result = client.get_private_deposit_addresses('max')
        # print(f"[I] Invoked get_private_deposit_addresses('max') API Result: \n    {result}\n")

        # result = client.get_private_deposit_detail('0x0123456789abcdef..')
        # print(f"[I] Invoked get_private_deposit_detail('0x0123456789abcdef..') API Result: \n    {result}\n")

        # result = client.get_private_deposit_history('usdt')
        # print(f"[I] Invoked get_private_deposit_history('usdt') API Result: \n    {result}\n")

        # result = client.get_private_deposit_history('usdt', state='accepted')
        # print(f"[I] Invoked get_private_deposit_history('usdt', state='accepted') API Result: \n    {result}\n")

        # result = client.get_private_executed_trades(12345678)
        # print(f"[I] Invoked get_private_executed_trades(12345678) API Result: \n    {result}\n")

        # result = client.get_private_member_me()
        # print(f"[I] Invoked get_private_member_me() API Result: \n    {result}\n")

        # result = client.get_private_order_detail(12345678)
        # print(f"[I] Invoked get_private_order_detail(12345678) API Result: \n    {result}\n")

        # result = client.get_private_order_history('maxtwd')
        # print(f"[I] Invoked get_private_order_history('maxtwd') API Result: \n    {result}\n")

        # result = client.get_private_reward_history('max', _type='holding')
        # print(f"[I] Invoked get_private_reward_history('max', _type='holding') API Result: \n    {result}\n")

        # result = client.get_private_transfer_detail(12345678901234567)
        # print(f"[I] Invoked get_private_transfer_detail(12345678901234567) API Result: \n    {result}\n")

        # result = client.get_private_transfer_history('max', side='out')
        # print(f"[I] Invoked get_private_transfer_history('max', side='out') API Result: \n    {result}\n")

        # result = client.get_private_withdrawal_addresses('usdt')
        # print(f"[I] Invoked get_private_withdrawal_addresses('usdt') API Result: \n    {result}\n")

        # result = client.get_private_withdrawal_detail(1234567890123456)
        # print(f"[I] Invoked get_private_withdrawal_detail(1234567890123456) API Result: \n    {result}\n")

        ''' Private (Write) '''
        # result = client.set_private_cancel_order(12345678)
        # print(f"[I] Invoked set_private_cancel_order(12345678) API Result: \n    {result}\n")

        # result = client.set_private_cancel_orders('maxtwd', 'sell')
        # print(f"[I] Invoked set_private_cancel_orders('maxtwd', 'sell') API Result: \n    {result}\n")

        # result = client.set_private_create_order('maxtwd', 'sell', 100, 123456)
        # print(f"[I] Invoked set_private_create_order('maxtwd', 'sell', 100, 123456) API Result: \n    {result}\n")

        """
        result = client.set_private_create_orders(
            'maxtwd', ['sell', 'sell'], [100, 100], [999, 999], _types=['limit', 'limit']
        )
        print(f"[I] Invoked set_private_create_orders('maxtwd', ['sell', 'sell'], ..) API Result: \n    {result}\n")
        """

        # result = client.set_private_deposit_address('xrp')
        # print(f"[I] Invoked set_private_deposit_address('xrp') API Result: \n    {result}\n")
    except Exception as error:
        print(f"[X] Exception: {str(error)}")

        # Networking errors occurred here
        response = getattr(error, 'read', None)
        if callable(response):
            print(f"[X] Reason: {response().decode('utf-8')}")
