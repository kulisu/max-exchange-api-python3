# max-exchange-api-python3

## Warning

This is an UNOFFICIAL wrapper for MAX exchange [HTTP API v2](https://max.maicoin.com/documents/api) written in Python 3.6

And this wrapper does not receive active maintainance, plaese consider using [CCXT](https://github.com/TaopaiC/ccxt/blob/max-191223/python/ccxt/max.py)

**USE THIS WRAPPER AT YOUR OWN RISK, I WILL NOT CORRESPOND TO ANY LOSES**

## Features

- Implementation of all [public](https://max.maicoin.com/documents/api_list#/public) and [private](https://max.maicoin.com/documents/api_list#/private) endpoints
- Simple handling of [authentication](https://max.maicoin.com/documents/api_v2#sign) with API key and secret
- All HTTP raw requests and responses can be found [here](https://gist.github.com/kulisu/8e519e2746a394401272a5f1f779c257)

## Usage

1. [Register an account](https://max.maicoin.com/signup?r=ecc3b0ab) with MAX exchange _(referral link)_
2. [Generate API key and secret](https://max.maicoin.com/api_tokens), assign relevant permissions to it
3. Clone this repository, and run `examples/all_api_endpoints.py`
4. Write your own trading policies and get profits ! 

### Linux

```bash
cd ~/ && git clone https://github.com/kulisu/max-exchange-api-python3
cd ~/max-exchange-api-python3 && cp examples/all_api_endpoints.py .

# update API key and secret
# vim all_api_endpoints.py

python3 all_api_endpoints.py
```

### Windows

```batch
cd %USERPROFILE%\Downloads
git clone https://github.com/kulisu/max-exchange-api-python3

cd max-exchange-api-python3 && copy examples\all_api_endpoints.py .

# update API key and secret
# notepad all_api_endpoints.py

python3 all_api_endpoints.py
```

### Example

```python
#!/usr/bin/env python3

from max.client import Client

if __name__ == '__main__':
    client = Client('PUY_MY_API_KEY_HERE', 'PUY_MY_API_SECRET_HERE')

    try:
        # Public (Read)
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

        # Private (Read)
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

        result = client.get_private_transfer_history()
        print(f"[I] Invoked get_private_transfer_history() API Result: \n    {result}\n")

        result = client.get_private_withdrawal_history()
        print(f"[I] Invoked get_private_withdrawal_history() API Result: \n    {result}\n")
    except Exception as error:
        print(f"[X] {str(error)}")

        # Networking errors occurred here
        response = getattr(error, 'read', None)
        if callable(response):
            print(f"[X] {response().decode('utf-8')}")
```

## Donation

If you feel this wrapper saved your times, buy me a coffee ?

- BTC: 32awSDjEY8V3KYS3bazLjSsu6SB3JiQcDi
- ETH: 0xAC2a7571EBA8986e4Ec9bA1A81Cde323c959c614
- LTC: MJNSuSSPYQRTknAMJw2BggocaMt9Lb7xFv
- MAX: 0xAC2a7571EBA8986e4Ec9bA1A81Cde323c959c614
- USDT: 34yVszuBhejsbSfnULK187srAhGkoeWgL6
