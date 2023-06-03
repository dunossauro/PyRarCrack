"""
Bruteforce attack for .rar using unrar.

V: 0.0.2.4

Based on:
http://stackoverflow.com/questions/11747254/python-brute-force-algorithm
http://www.enigmagroup.org/code/view/python/168-Rar-password-cracker
http://rarcrack.sourceforge.net/
"""
from argparse import ArgumentParser
from itertools import chain, product
import os
from os.path import exists
from string import printable
from subprocess import PIPE, Popen
from time import time
import threading


chars = printable + "ÁáÂâàÀÃãÅåÄäÆæÉéÊêÈèËëÐðÍíÎîÌìÏïÓóÒòÔôØøÕõÖöÚúÛûÙùÜüÇçÑñÝý®©Þþß"
special_chars = "();<>`|~\"&'}]"

parser = ArgumentParser(description="Python combination generator to unrar")
parser.add_argument(
    "--start",
    help='Number of characters of the initial string [1 -> "a", 2 -> "aa"]',
    default=1,
    type=int,
)

parser.add_argument(
    "--stop",
    help='Number of characters of the final string [3 -> "ßßß"]',
    default=3,
    type=int,
)
parser.add_argument(
    "--threads", type=int, default=os.cpu_count(), help="Number of threads to use"
)

parser.add_argument(
    "--verbose", help="Show combinations", default=False, required=False
)

parser.add_argument(
    "--alphabet",
    help="alternative chars to combinations",
    default=chars,
    required=False,
)

parser.add_argument("--file", help=".rar file [file.rar]", type=str)

args = parser.parse_args()


def generate_combinations(alphabet, length, start=1):
    """Generate combinations using alphabet."""
    yield from (
        "".join(string)
        for string in chain.from_iterable(
            product(alphabet, repeat=x) for x in range(start, length + 1)
        )
    )


def format(string):
    """Format chars to write them in shell."""
    formated = map(
        lambda char: char if char not in special_chars else f"\\{char}", string
    )
    return "".join(formated)


def worker(start, stop):
    for combination in generate_combinations(args.alphabet, stop, start):
        formated_combination = format(combination)
        if args.verbose:
            print(f"Trying: {combination}")
        cmd = Popen(
            f"unrar t -p{formated_combination} {args.file}".split(),
            stdout=PIPE,
            stderr=PIPE,
        )
        out, err = cmd.communicate()
        if "All OK" in out.decode():
            print(f"Password found: {combination}")
            print(f"Time: {time() - start_time}")
            exit()


if __name__ == "__main__":
    if not exists(args.file):
        raise FileNotFoundError(args.file)
    if args.stop < args.start:
        args.start, args.stop = args.stop, args.start  # switch the numbers
    start_time = time()
    threads = []
    print(f"Threads: {args.threads}")
    for i in range(args.threads):
        start = i * (args.stop - args.start) // args.threads + args.start
        stop = (i + 1) * (args.stop - args.start) // args.threads + args.start
        t = threading.Thread(target=worker, args=(start, stop))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
