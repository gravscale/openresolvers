import argparse
import asyncio
import csv
import aiodns
import signal
from ipaddress import ip_network
import logging
import curses

# Default Configurations
semaphore_limit = 100
LOG_LEVEL = "ERROR"


# Global Variables
total_tested = 0
open_dns_count = 0
error_count = 0
completed_networks = 0
sem = asyncio.Semaphore(semaphore_limit)

resolver = aiodns.DNSResolver()
loop = asyncio.get_event_loop()

async def test_dns(ip, network, stdscr, total_networks, csvwriter=None, show_option="so"):
    global total_tested, open_dns_count, error_count
    status = "Closed"
    async with sem:
        try:
            answers = await resolver.query(f"{ip}", "A")
            open_dns_count += 1
            status = "Open"
        except Exception as e:
            logging.error(f"Error resolving {ip}: {e}")
            error_count += 1
            status = "Error"

    total_tested += 1

    if stdscr and show_option in ["so", "se", "sc"]:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Networks ({completed_networks}/{total_networks}) Tested IPs ({total_tested}) Open Resolvers ({open_dns_count}) Errors ({error_count})")
        stdscr.refresh()

    if csvwriter and show_option in [status[:2].lower()]:
        csvwriter.writerow([network, ip, status])

async def main(stdscr, args):
    global completed_networks
    total_networks = len(args.networks)
    csvwriter = None
    if args.output:
        csvfile = open(args.output, "w", newline="")
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Network", "IP", "Status"])

    tasks = []
    for network in args.networks:
        for ip in ip_network(network):
            tasks.append(test_dns(str(ip), network, stdscr, total_networks, csvwriter, args.show_option))
        completed_networks += 1
    await asyncio.gather(*tasks)

    if args.output:
        csvfile.close()

    if stdscr:
        stdscr.addstr(1, 0, "Press any key to close.")
        stdscr.getch()

def setup_logging(logfile, level):
    logging.basicConfig(filename=logfile, level=level)

def shutdown(signum, frame):
    curses.endwin()
    logging.info("Operation interrupted by the user.")
    exit(0)

def main_curses(stdscr, args):
    stdscr.clear()
    signal.signal(signal.SIGINT, shutdown)
    loop.run_until_complete(main(stdscr, args))
    curses.endwin()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find open resolvers')
    parser.add_argument('networks', nargs='+', help='Network blocks in CIDR format')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-o', '--output', help='Output CSV file', default=None)
    parser.add_argument('-l', '--logfile', default='openresolvers.log')    
    parser.add_argument('-a', '--auto_close', action='store_true', help='Auto close curses')
    parser.add_argument('-q', '--quiet', action='store_true', help='No curses display')
    parser.add_argument('-se', '--show_errors', dest='show_option', action='store_const', const='se')
    parser.add_argument('-so', '--show_open', dest='show_option', action='store_const', const='so', default='so')
    parser.add_argument('-sc', '--show_closed', dest='show_option', action='store_const', const='sc')
    parser.add_argument('--version', action='version', version='1.0')
    args = parser.parse_args()

    if args.verbose >= 2:
        LOG_LEVEL = "DEBUG"
    elif args.verbose == 1:
        LOG_LEVEL = "INFO"

    setup_logging(args.logfile, LOG_LEVEL)

    if args.quiet:
        loop.run_until_complete(main(None, args))
    else:
        curses.wrapper(main_curses, args)
