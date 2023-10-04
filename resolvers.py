# importações
import local
import asyncio
import csv
import aiodns
import signal
from ipaddress import ip_network
import uvloop
import curses
import logging

logging.basicConfig(filename="recursive.log", level=getattr(logging, local.LOG_LEVEL))

# Inicialização
#uvloop.install()
resolver = aiodns.DNSResolver()
loop = asyncio.get_event_loop()
sem = asyncio.Semaphore(local.semaphore_limit)

total_tested = 0
open_dns_count = 0

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()

async def test_dns(ip):
    global total_tested, open_dns_count
    async with sem:
        try:
            answers = await resolver.query(f"{ip}", "A")
            open_dns_count += 1
        except Exception as e:  
            logging.error(f"Erro ao resolver {ip}: {e}")
            return

    total_tested += 1
    try:
        stdscr.clear()  # Limpar a tela antes de atualizar
        stdscr.addstr(0, 0, f"Testados: {total_tested}/4096, Abertos: {open_dns_count}")
        stdscr.refresh()
        await asyncio.sleep(0.1)  # Dar tempo para atualizar a tela
    except Exception as e:
        logging.error(f"Erro ao atualizar a tela: {e}")


async def main():
    tasks = []
    for network in local.networks:
        for ip in ip_network(network):
            tasks.append(test_dns(ip))

    await asyncio.gather(*tasks)

    stdscr.addstr(0, 0, f"Testados: {total_tested}/4096, Abertos: {open_dns_count}")
    stdscr.refresh()


def shutdown(signum, frame):
    curses.endwin()
    logging.info("Operação interrompida pelo usuário.")
    exit(0)


def main_curses(stdscr):
    global total_tested, open_dns_count  # definições globais

    stdscr.clear()

    try:
        loop.run_until_complete(main())
    except Exception as e:
        logging.error(f"Erro: {e}")

    finally:
        curses.endwin()



if __name__ == "__main__":
    try:
        signal.signal(signal.SIGINT, shutdown)
        with open("open_dns_servers.csv", "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Timestamp", "IP Address", "Status"])
        loop.run_until_complete(main())
    except Exception as e:
        stdscr.addstr(2, 0, f"Erro: {e}")
        logging.error(f"Erro: {e}")
    finally:
        curses.endwin()

