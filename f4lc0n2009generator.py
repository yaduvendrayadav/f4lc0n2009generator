import ipaddress
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend
import os
from datetime import datetime, timedelta
import random
from bitcoinaddress import Wallet
from concurrent.futures import ProcessPoolExecutor
import time
import multiprocessing

def generate_key():
    ip_ranges = [
        ipaddress.IPv4Network("192.168.1.0/28"),
    ]
    start_timestamp = int(datetime(2009, 1, 1).timestamp())
    end_timestamp = int(datetime(2010, 1, 1).timestamp())
    random_timestamp = random.randint(start_timestamp, end_timestamp)
    random_datetime = datetime.fromtimestamp(random_timestamp)
    entropy = str(random_timestamp).encode('utf-8')
    total_ram = random.choice([1, 2, 4]) * 1024 * 1024 * 1024
    memory_usage = random.randint(1000000, 500000000)
    entropy += memory_usage.to_bytes((memory_usage.bit_length() + 7) // 8, 'big')
    cpu_load = random.uniform(0.0, 100.0)
    entropy += str(cpu_load).encode('utf-8')
    process_id = random.randint(1000, 9999)
    process_memory_usage = random.randint(1000000, 500000000)
    entropy += str(process_id).encode('utf-8')
    entropy += process_memory_usage.to_bytes((process_memory_usage.bit_length() + 7) // 8, 'big')
    ip_range = random.choice(ip_ranges)
    ip = str(random.choice(list(ip_range.hosts())))
    entropy += ip.encode('utf-8')
    entropy += os.urandom(32)
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(entropy)
    hashed_entropy = digest.finalize()
    private_key = ec.derive_private_key(int.from_bytes(hashed_entropy, "big"), ec.SECP256K1(), default_backend())
    private_key_hex = private_key.private_numbers().private_value.to_bytes(32, 'big').hex()
    wallet = Wallet(private_key_hex)
    addresses = {
        "Uncompressed Bitcoin address": wallet.address.mainnet.pubaddr1,
        "Compressed Bitcoin address": wallet.address.mainnet.pubaddr1c,
        "P2SH-Segwit Bitcoin address": wallet.address.mainnet.pubaddr3,
        "Bech32 Bitcoin address P2WPKH": wallet.address.mainnet.pubaddrbc1_P2WPKH    }
    wif = wallet.key.mainnet.wif
    wifc = wallet.key.mainnet.wifc

    return {
        "Random date and time in 2009 for entropy": random_datetime,
        "Total RAM in 2009 (in bytes)": total_ram,
        "Simulated memory usage by Bitcoin Core (in bytes)": memory_usage,
        "Simulated CPU load in 2009 (in percentage)": cpu_load,
        "Simulated process ID in 2009": process_id,
        "Simulated process memory usage in 2009 (in bytes)": process_memory_usage,
        "Simulated IP address in 2009": ip,
        "Private key in 64-character hexadecimal format": private_key_hex,
        "Privatekey Uncompressed": wif,
        "Privatekey compressed": wifc,
        **addresses
    }

"""
#for test 12M4p2tizp12ryx93BTso8yxbPPPnCNA87 1NprETPuXnDFELfxL6trvk1AFsDxYuKgze 3HT3LeupKE8DgjkiyBwt9R2vg1xmJSacKR bc1qaan5nkprqgxkjz20znlwzcvyk7ze6v9zp45w7j
def generate_key():
    private_key_hex = "8ec7083bb445b1414d540fa0c07d0ef3db98bd95c64b51e4cc3e2eec8dcb86c5"
    wallet = Wallet(private_key_hex)
    addresses = {
        "Uncompressed Bitcoin address": wallet.address.mainnet.pubaddr1,
        "Compressed Bitcoin address": wallet.address.mainnet.pubaddr1c,
        "P2SH-Segwit Bitcoin address": wallet.address.mainnet.pubaddr3,
        "Bech32 Bitcoin address P2WPKH": wallet.address.mainnet.pubaddrbc1_P2WPKH
    }
    wif = wallet.key.mainnet.wif
    wifc = wallet.key.mainnet.wifc

    return {
        "Private key in 64-character hexadecimal format": private_key_hex,
        "Privatekey Uncompressed": wif,
        "Privatekey compressed": wifc,
        **addresses
    }
"""


if __name__ == '__main__':
    print(".########.##........##........######....#####...##....##\n.##.......##....##..##.......##....##..##...##..###...##\n.##.......##....##..##.......##.......##.....##.####..##\n.######...##....##..##.......##.......##.....##.##.##.##\n.##.......#########.##.......##.......##.....##.##..####\n.##.............##..##.......##....##..##...##..##...###\n.##.............##..########..######....#####...##....##")
    print("Donate: 1FALCoN194bPQELKGxz2vdZyrPRoSVxGmR" )
    print("simulator configurations 2009 GENERATION BTC V1" )
    print("http://f4lc0n.com" )
    multiprocessing.freeze_support()
    num_processors = multiprocessing.cpu_count()
    executor = ProcessPoolExecutor(max_workers=num_processors)
    print("Loading puzzle.txt ... One moment Please")
    with open("puzzle.txt", "r") as file:
        puzzle_addresses = set()
        for line in file:
            address = line.strip().split('\t')[0]
            puzzle_addresses.add(address)
    num_puzzle_addresses = len(puzzle_addresses)
    print("Number of addresses loaded from puzzle.txt:", num_puzzle_addresses)
    count = 0
    while True:
        futures = [executor.submit(generate_key) for _ in range(num_processors)]
        count += len(futures)
        for future in futures:
            result = future.result()
            for key, value in result.items():
                print(key + ":", value)
            print()
            if any(result[address] in puzzle_addresses for address in ["Compressed Bitcoin address", "Uncompressed Bitcoin address", "P2SH-Segwit Bitcoin address", "Bech32 Bitcoin address P2WPKH"]):
                with open("WINNER.TXT", "a") as file:
                    file.write("Matching address found:\n")
                    for key, value in result.items():
                        file.write(key + ": " + str(value) + "\n")
                    file.write("\n")
    generation_rate = count / (time.time() - start_time)
    print("Total keys generated:", count)
    print("Generation rate per second:", generation_rate)
