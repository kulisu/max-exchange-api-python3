#!/usr/bin/env python3

import base64
import hashlib
import hmac
import json

from urllib.parse import urlencode
from urllib.request import Request
from urllib.request import urlopen

from .constants import *
from .helpers import *


class Client(object):
    def __init__(self, key, secret, timeout=30):
        self._api_key = key
        self._api_secret = secret

        self._api_timeout = int(timeout)

    def _build_body(self, endpoint, query=None):
        if query is None:
            query = {}

        # TODO: duplicated nonce may occurred in high frequency trading
        # fix it by yourself, hard code last two characters is a quick solution
        # {"error":{"code":2006,"message":"The nonce has already been used by access key."}}
        body = {
            'path': f"/api/{PRIVATE_API_VERSION}/{endpoint}.json",
            'nonce': get_current_timestamp(),
        }

        body.update(query)

        return body

    def _build_headers(self, scope, body=None):
        if body is None:
            body = {}

        headers = {
            'Accept': 'application/json',
            'User-Agent': 'pyCryptoTrader/1.0.3',
        }

        if scope.lower() == 'private':
            payload = self._build_payload(body)
            sign = hmac.new(bytes(self._api_secret, 'utf-8'), bytes(payload, 'utf-8'), hashlib.sha256).hexdigest()

            headers.update({
                # This header is REQUIRED to send JSON data.
                # or you have to send PLAIN form data instead.
                'Content-Type': 'application/json',
                'X-MAX-ACCESSKEY': self._api_key,
                'X-MAX-PAYLOAD': payload,
                'X-MAX-SIGNATURE': sign
            })

        return headers

    def _build_payload(self, body):
        return base64.urlsafe_b64encode(json.dumps(body).encode('utf-8')).decode('utf-8')

    def _build_url(self, scope, endpoint, body=None, query=None):
        if query is None:
            query = {}

        if body is None:
            body = {}

        # 2020-03-03 Updated
        # All query parameters must equal to payload
        query.update(body)

        if scope.lower() == 'private':
            url = f"{PRIVATE_API_URL}/{PRIVATE_API_VERSION}/{endpoint}.json"
        else:
            url = f"{PUBLIC_API_URL}/{PUBLIC_API_VERSION}/{endpoint}.json"

        return f"{url}?{urlencode(query, True, '/[]')}" if len(query) > 0 else url

    def _send_request(self, scope, method, endpoint, query=None, form=None):
        if form is None:
            form = {}

        if query is None:
            query = {}

        body = self._build_body(endpoint, query)
        data = None

        if len(form) > 0:
            body.update(form)
            data = json.dumps(body).encode('utf-8')

        # Build X-MAX-PAYLOAD header first
        headers = self._build_headers(scope, body)

        # Fix "401 Payload is not consistent .."
        # state[]=cancel&state[]=wait&state[]=done
        # {"path": "/api/v2/orders.json", "state": ["cancel", "wait", "done"]}
        for key in body:
            if type(body[key]) is list and not key[-2:] == '[]':
                body[f"{key}[]"] = body.pop(key)

                if key in query:
                    query.pop(key)

        # Build final url here
        url = self._build_url(scope, endpoint, body, query)

        request = Request(headers=headers, method=method.upper(), url=url.lower())

        # Start: Debugging with BurpSuite only
        # import ssl
        # ssl._create_default_https_context = ssl._create_unverified_context

        """
        root@kali:/tmp/max-exchange-api-python3# export HTTPS_PROXY=https://127.0.0.1:8080
        root@kali:/tmp/max-exchange-api-python3# /usr/bin/python3 all_api_endpoints.py
        """
        # End: Debugging with BurpSuite only

        response = urlopen(request, data=data, timeout=self._api_timeout)

        return json.loads(response.read())

    # Public API
    def get_public_all_currencies(self):
        """
        https://max.maicoin.com/documents/api_list#!/public/getApiV2Currencies

        :return: a list contains all available currencies
        """

        return self._send_request('public', 'GET', 'currencies')

    def get_public_all_markets(self):
        """ma
        https://max.maicoin.com/documents/api_list#!/public/getApiV2Markets

        :return: a list contains all available markets
        """

        return self._send_request('public', 'GET', 'markets')

    def get_public_all_tickers(self, pair=None):
        """
        https://max.maicoin.com/documents/api_list#!/public/getApiV2Tickers

        :param pair: the specific trading pair to query (optional)
        :return: a list contains all pair tickers
        """

        if pair is not None and len(pair) > 0:
            return self._send_request('public', 'GET', f"tickers/{pair.lower()}")
        else:
            return self._send_request('public', 'GET', 'tickers')

    def get_public_k_line(self, pair, limit=30, period=1, timestamp=''):
        """
        https://max.maicoin.com/documents/api_list#!/public/getApiV2K

        :param pair: the trading pair to query
        :param limit: the data points limit to query
        :param period: the time period of K line in minute
        :param timestamp: the Unix epoch seconds set to return trades executed before the time only
        :return: a list contains all OHLC prices in exchange
        """

        query = {
            'market': pair.lower(),
            'limit': limit,
            'period': period,
            'timestamp': timestamp
        }

        return self._send_request('public', 'GET', 'k', query)

    def get_public_markets_summary(self):
        """
        https://max.maicoin.com/documents/api_list#!/public/getApiV2Summary

        :return: a dict contains overview of market data for all tickers
        """

        return self._send_request('public', 'GET', 'summary')

    # TODO: this is a deprecated endpoint
    def get_public_order_book(self, pair, asks=20, bids=20):
        """
        https://max.maicoin.com/documents/api_list#!/public/getApiV2OrderBook

        :param pair: the trading pair to query
        :param asks: the sell orders limit to query
        :param bids: the buy orders limit to query
        :return: a dict contains asks and bids data
        """

        raise DeprecationWarning('this route will be removed since 2021/5/30, please use api/v2/depth to instead.')

        query = {
            'market': pair.lower(),
            'asks_limit': asks,
            'bids_limit': bids
        }

        return self._send_request('public', 'GET', 'order_book', query)

    def get_public_pair_depth(self, pair, limit=300):
        """
        https://max.maicoin.com/documents/api_list#!/public/getApiV2Depth

        :param pair: the trading pair to query
        :param limit: the price levels limit to query
        :return: a dict contains asks and bids data
        """

        query = {
            'market': pair.lower(),
            'limit': limit
        }

        return self._send_request('public', 'GET', 'depth', query)

    def get_public_recent_trades(self, pair, timestamp='', _from='',
                                 to='', sort='desc', pagination=True,
                                 page=1, limit=50, offset=0):
        """
        https://max.maicoin.com/documents/api_list#!/public/getApiV2Trades

        :param pair: the trading pair to query
        :param timestamp: the Unix epoch seconds set to return trades executed before the time only
        :param _from: the order id set to return trades created after the trade
        :param to: the order id set to return trades created before the trade
        :param sort: sort the trades by created time, default is 'desc'
        :param pagination: do pagination and return metadata in header
        :param page: the page number applied for pagination
        :param limit: the records limit to query
        :param offset: the records to skip, not applied for pagination
        :return: a list contains all completed orders in exchange
        """

        query = {
            'market': pair.lower(),
            'timestamp': timestamp,
            'from': _from,
            'to': to,
            'order_by': sort,
            'pagination': pagination,
            'page': page,
            'limit': limit,
            'offset': offset
        }

        return self._send_request('public', 'GET', 'trades', query)

    def get_public_server_time(self):
        """
        https://max.maicoin.com/documents/api_list#!/public/getApiV2Timestamp

        :return: an integer in seconds since Unix epoch of server's current time
        """

        return self._send_request('public', 'GET', 'timestamp')

    def get_public_withdrawal_constraints(self):
        """
        https://max.maicoin.com/documents/api_list#!/public/getApiV2WithdrawalConstraint

        :return: a list contains all withdrawal constraints
        """

        return self._send_request('public', 'GET', 'withdrawal/constraint')

    def get_public_vip_levels(self, level=None):
        """
        https://max.maicoin.com/documents/api_list#!/public/getApiV2VipLevels

        :param level: the specific VIP level to query (optional)
        :return: a list contains all VIP level fees
        """

        if level is not None and type(level) is int:
            return self._send_request('public', 'GET', f"vip_levels/{level}")
        else:
            return self._send_request('public', 'GET', 'vip_levels')

    # Private API (Read)
    def get_private_account_balance(self, currency):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2MembersAccountsCurrency

        :param currency: the specific coin to query
        :return: a dict contains all balance information
        """

        return self._send_request('private', 'GET', f"members/accounts/{currency.lower()}")

    def get_private_account_balances(self):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2MembersAccounts

        :return: a list contains all coins balance
        """

        return self._send_request('private', 'GET', 'members/accounts')

    # TODO: this is a deprecated endpoint
    def get_private_deposit_address(self, currency=''):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2DepositAddress

        :param currency: the specific coin to query
        :return: a list contains all deposit addresses
        """

        query = {}

        if currency is not None and len(currency) > 0:
            query['currency'] = currency.lower()

        return self._send_request('private', 'GET', 'deposit_address', query)

    def get_private_deposit_addresses(self, currency=''):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2DepositAddresses

        :param currency: the specific coin to query
        :return: a list contains all deposit addresses
        """

        query = {}

        if currency is not None and len(currency) > 0:
            query['currency'] = currency.lower()

        return self._send_request('private', 'GET', 'deposit_addresses', query)

    def get_private_deposit_detail(self, _id):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2Deposit

        :param _id: the specific tx ID to query
        :return: a dict contains all deposit information
        """

        return self._send_request('private', 'GET', 'deposit', {'txid': _id})

    def get_private_deposit_history(self, currency='', _from='', to='', state='',
                                    pagination=False, page=1, limit=50, offset=0):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2Deposits

        :param currency: the specific coin to query
        :param _from: the target period after Epoch time in seconds
        :param to: the target period before Epoch time in seconds
        :param state: the deposits status to query
        :param pagination: do pagination and return metadata in header
        :param page: the page number applied for pagination
        :param limit: the records limit to query
        :param offset: the records to skip, not applied for pagination
        :return: a list contains all completed deposits in exchange
        """

        query = {
            'from': _from,
            'to': to,
            'pagination': pagination,
            'page': page,
            'limit': limit,
            'offset': offset
        }

        if currency is not None and len(currency) > 0:
            query['currency'] = currency.lower()
        if state is not None and len(state) > 0:
            query['state'] = state.lower()

        return self._send_request('private', 'GET', 'deposits', query)

    def get_private_executed_trades(self, _id):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2TradesMyOfOrder

        :param _id: the id of the order
        :return: a list contains all trades in an order
        """

        return self._send_request('private', 'GET', 'trades/my/of_order', {'id': _id})

    def get_private_max_rewards(self):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2MaxRewardsYesterday

        :return: a dict contains all MAX rewards in yesterday
        """

        return self._send_request('private', 'GET', 'max_rewards/yesterday')

    def get_private_member_me(self):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2MembersMe

        :return: a dict contains all personal profile and balances information
        """

        return self._send_request('private', 'GET', 'members/me')

    def get_private_member_profile(self):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2MembersProfile

        :return: a dict contains all personal profile information
        """

        return self._send_request('private', 'GET', 'members/profile')

    def get_private_vip_level(self):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2MembersVipLevel

        :return: a dict contains VIP level info
        """

        return self._send_request('private', 'GET', 'members/vip_level')

    def get_private_order_detail(self, _id, client_id=''):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2Order

        :param _id: the id of the order
        :param client_id: a unique order id specified by user, must less or equal to 36
        :return: a dict contains all order information
        """

        if client_id is not None and len(client_id) > 0:
            return self._send_request('private', 'GET', 'order', {'client_oid': client_id})
        else:
            return self._send_request('private', 'GET', 'order', {'id': _id})

    def get_private_order_history(self, pair, state=None, sort='asc', pagination=True,
                                  page=1, limit=100, offset=0, group_id=''):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2Orders

        :param pair: the trading pair to query
        :param state: the states to be filtered, default is 'wait' and 'convert'
        :param sort: sort the orders by created time, default is 'asc'
        :param pagination: do pagination and return metadata in header
        :param page: the page number applied for pagination
        :param limit: the orders limit to query
        :param offset: the records to skip, not applied for pagination
        :param group_id: a integer group id for orders
        :return: a list contains all placed orders
        """

        if state is None:
            state = ['wait', 'convert']

        query = {
            'market': pair.lower(),
            'order_by': sort.lower(),
            'pagination': pagination,
            'page': page,
            'limit': limit,
            'offset': offset

        }

        if state is not None and len(state) > 0:
            query['state'] = state

        if group_id is not None and type(group_id) is int:
            query['group_id'] = group_id

        return self._send_request('private', 'GET', 'orders', query)

    def get_private_reward_history(self, currency='', _from='', to='', _type='',
                                   pagination=False, page=1, limit=50, offset=0):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2Rewards

        :param currency: the specific coin to query
        :param _from: the target period after Epoch time in seconds
        :param to: the target period before Epoch time in seconds
        :param _type: the rewards type, should be 'airdrop' or 'holding', 'mining' or 'trading'
        :param pagination: do pagination and return metadata in header
        :param page: the page number applied for pagination
        :param limit: the records limit to query
        :param offset: the records to skip, not applied for pagination
        :return: a list contains all rewards information
        """

        query = {
            'from': _from,
            'to': to,
            'pagination': pagination,
            'page': page,
            'limit': limit,
            'offset': offset
        }

        if currency is not None and len(currency) > 0:
            query['currency'] = currency.lower()

        if _type is not None and len(_type) > 0:
            return self._send_request('private', 'GET', f"rewards/{_type}_reward", query)
        else:
            return self._send_request('private', 'GET', 'rewards', query)

    def get_private_trade_history(self, pair, timestamp='', _from='',
                                  to='', sort='desc', pagination=True,
                                  page=1, limit=50, offset=0):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2TradesMy

        :param pair: the trading pair to query
        :param timestamp: the Unix epoch seconds set to return trades executed before the time only
        :param _from: the order id set to return trades created after the trade
        :param to: the order id set to return trades created before the trade
        :param sort: sort the trades by created time, default is 'desc'
        :param pagination: do pagination and return metadata in header
        :param page: the page number applied for pagination
        :param limit: the records limit to query
        :param offset: the records to skip, not applied for pagination
        :return: a list contains all completed trades
        """

        query = {
            'market': pair.lower(),
            'timestamp': timestamp,
            'from': _from,
            'to': to,
            'order_by': sort,
            'pagination': pagination,
            'page': page,
            'limit': limit,
            'offset': offset
        }

        return self._send_request('private', 'GET', 'trades/my', query)

    def get_private_transfer_detail(self, _id):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2InternalTransfer

        :param _id: the internal transfer id to query
        :return: a dict contains all transfer information
        """

        return self._send_request('private', 'GET', 'internal_transfer', {'uuid': _id})

    def get_private_transfer_history(self, currency='', _from='', to='', side='',
                                     pagination=False, page=1, limit=50, offset=0):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2InternalTransfers

        :param currency: the specific coin to query
        :param _from: the target period after Epoch time in seconds
        :param to: the target period before Epoch time in seconds
        :param side: the transfer side, should be 'in' or 'out'
        :param pagination: do pagination and return metadata in header
        :param page: the page number applied for pagination
        :param limit: the records limit to query
        :param offset: the records to skip, not applied for pagination
        :return: a list contains all transferred information
        """

        query = {
            'from': _from,
            'to': to,
            'pagination': pagination,
            'page': page,
            'limit': limit,
            'offset': offset
        }

        if currency is not None and len(currency) > 0:
            query['currency'] = currency.lower()
        if side is not None and len(side) > 0:
            query['side'] = side.lower()

        return self._send_request('private', 'GET', 'internal_transfers', query)

    def get_private_withdrawal_addresses(self, currency, pagination=True, page=1, limit=100, offset=0):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2WithdrawAddresses

        :param currency: the specific coin to query
        :param pagination: do pagination and return metadata in header
        :param page: the page number applied for pagination
        :param limit: the records limit to query
        :param offset: the records to skip, not applied for pagination
        :return: a list contains all withdraw addresses
        """

        query = {
            'currency': currency.lower(),
            'pagination': pagination,
            'page': page,
            'limit': limit,
            'offset': offset
        }

        return self._send_request('private', 'GET', 'withdraw_addresses', query)

    def get_private_withdrawal_detail(self, _id):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2Withdrawal

        :param _id: the specific withdrawal UUID to query
        :return: a dict contains all withdrawal information
        """

        return self._send_request('private', 'GET', 'withdrawal', {'uuid': _id})

    def get_private_withdrawal_history(self, currency='', _from='', to='', state='',
                                       pagination=False, page=1, limit=50, offset=0):
        """
        https://max.maicoin.com/documents/api_list#!/private/getApiV2Withdrawals

        :param currency: the specific coin to query
        :param _from: the target period after Epoch time in seconds
        :param to: the target period before Epoch time in seconds
        :param state: the withdrawals status to query
        :param pagination: do pagination and return metadata in header
        :param page: the page number applied for pagination
        :param limit: the records limit to query
        :param offset: the records to skip, not applied for pagination
        :return: a list contains all completed withdrawals in exchange
        """

        query = {
            'from': _from,
            'to': to,
            'pagination': pagination,
            'page': page,
            'limit': limit,
            'offset': offset
        }

        if currency is not None and len(currency) > 0:
            query['currency'] = currency.lower()
        if state is not None and len(state) > 0:
            query['state'] = state.lower()

        return self._send_request('private', 'GET', 'withdrawals', query)

    # Private API (Write)
    def set_private_cancel_order(self, _id, client_id=''):
        """
        https://max.maicoin.com/documents/api_list#!/private/postApiV2OrderDelete

        :param _id: the id of the order
        :param client_id: a unique order id specified by user, must less or equal to 36
        :return: a dict contains cancelled order information
        """

        if client_id is not None and len(client_id) > 0:
            return self._send_request('private', 'POST', 'order/delete', {'client_oid': client_id})
        else:
            return self._send_request('private', 'POST', 'order/delete', {}, {'id': _id})

    def set_private_cancel_orders(self, pair='', side='', group_id=''):
        """
        https://max.maicoin.com/documents/api_list#!/private/postApiV2OrdersClear

        :param pair: the trading pair to clear all orders
        :param side: the trading side to clear all orders
        :param group_id: a integer group id for orders
        :return: a list contains all cleared orders
        """

        form = {}

        if pair is not None and len(pair) > 0:
            form['market'] = pair.lower()

        if side is not None and len(side) > 0:
            form['side'] = side.lower()

        if group_id is not None and type(group_id) is int:
            form['group_id'] = group_id

        return self._send_request('private', 'POST', 'orders/clear', {}, form)

    def set_private_create_order(self, pair, side, amount, price, stop='', _type='limit', client_id='', group_id=''):
        """
        https://max.maicoin.com/documents/api_list#!/private/postApiV2Orders

        :param pair: the trading pair to create
        :param side: the trading side, should only be buy or sell
        :param amount: the amount of the order for the trading pair
        :param price: the price of the order for the trading pair
        :param stop; the price to trigger a stop order
        :param _type: the order type, should only be limit, market, stop_limit or stop_market
        :param client_id: a unique order id specified by user, must less or equal to 36
        :param group_id: a integer group id for orders
        :return: a dict contains created order information
        """

        form = {
            'market': pair.lower(),
            'side': side.lower(),
            'volume': str(amount),
            'price': str(price),
            'ord_type': _type.lower()
        }

        if stop is not None and len(stop) > 0:
            form['stop_price'] = str(stop)

        if client_id is not None and len(client_id) > 0:
            form['client_oid'] = client_id

        if group_id is not None and type(group_id) is int:
            form['group_id'] = group_id

        return self._send_request('private', 'POST', 'orders', {}, form)

    def set_private_create_orders(self, pair, sides=None, amounts=None, prices=None, stops=None, _types=None):
        """
        https://max.maicoin.com/documents/api_list#!/private/postApiV2OrdersMulti

        :param pair: the trading pair to create
        :param sides: the trading side, should only be buy or sell
        :param amounts: the amount of the order for the trading pair
        :param prices: the price of the order for the trading pair
        :param stops; the price to trigger a stop order
        :param _types: the order type, should only be limit, market, stop_limit or stop_market
        :return: a list contains created orders information
        """

        raise DeprecationWarning('this route will be removed since 2021/4/30')

        if _types is None:
            _types = []

        if stops is None:
            stops = []

        if prices is None:
            prices = []

        if amounts is None:
            amounts = []

        if sides is None:
            sides = []

        orders = []

        if type(sides) is not list or type(amounts) is not list or type(prices) is not list:
            raise ValueError
        if type(stops) is not list or type(_types) is not list or len(_types) == 0:
            raise ValueError

        for i in range(0, len(sides)):
            orders.append({
                'side': sides[i].lower(),
                'volume': str(amounts[i]),
                'price': str(prices[i]),
                'ord_type': _types[i].lower()
            })

        return self._send_request('private', 'POST', 'orders/multi', {}, {'market': pair.lower(), 'orders': orders})

    def set_private_create_withdrawal(self, currency, amount, address):
        form = {
            'currency': currency.lower(),
            'withdraw_address_uuid': address,
            'amount': str(amount),
        }

        return self._send_request('private', 'POST', 'withdrawal', {}, form)
    
    def set_private_deposit_address(self, currency):
        """
        https://max.maicoin.com/documents/api_list#!/private/postApiV2DepositAddresses

        :param currency: the specific coin to create
        :return: a list contains created deposit address
        """

        return self._send_request('private', 'POST', 'deposit_addresses', {}, {'currency': currency.lower()})
