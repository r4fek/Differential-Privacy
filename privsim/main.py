import sys
import base64

import click
from collections import Counter
from string import digits, ascii_letters, punctuation
import random

random = random.SystemRandom()
ascii = digits + ascii_letters + punctuation


def get_random_char():
    return random.choice(ascii)


def generate_masked_url(url, privacy):
    letters = []
    for i, letter in enumerate(url):
        if random.random() < privacy:
            letters.append(get_random_char())
        else:
            letters.append(url[i])
    return ''.join(letters)


def check_reports(url, counters):
    for i, letter in enumerate(url):
        if counters[i].most_common(1)[0][0] == letter:
            continue
        else:
            return False
    return True


def _simulate(url, privacy):
    assert 0 < privacy < 1
    counters = [Counter() for _ in range(len(url))]
    num_generated = 0

    while True:
        num_generated += 1
        masked = generate_masked_url(url, privacy)
        for i, letter in enumerate(masked):
            counters[i][letter] += 1

        sys.stdout.write('\rrecov: {} | gen: {}'.format(
            ''.join([counters[i].most_common(1)[0][0] for i in range(len(url))]), masked))
        sys.stdout.flush()

        if check_reports(url, counters):
            click.echo(
                click.style('\n\n{} reports required to recover the original URL {} with privacy level {}%'
                            .format(num_generated, url, privacy*100.0), fg='green'))
            return


@click.command()
@click.argument('url', default='http://stackoverflow.com/questions/5290994/python-remove-and-replace-printed-items')
@click.option('-p', '--privacy', default=90.0, help='Level of privacy <100. Higher == better user privacy')
def simulate(url, privacy):
    _simulate(url, privacy/100.0)


@click.command()
@click.argument('path', default='reports.txt')
def recover(path):
    with open(path, 'r') as f:
        reports = f.readlines()

    reports = [base64.urlsafe_b64decode(r) for r in reports if r]

    num_chars = len(reports[0])
    counters = [Counter() for _ in range(num_chars)]
    recovered = b''
    recovered_reports = []

    for report in reports:
        for i, letter in enumerate(report):
            counters[i][letter] += 1
        recovered = bytes([counters[l].most_common(1)[0][0] for l in range(num_chars)])
        print('recov: {}'.format(recovered))
        recovered_reports.append(recovered)
    try:
        click.echo(
            click.style('\nRecovered! {}'.format(recovered.decode('utf-8')),
                        fg='green'))
        reports_needed = len([r for r in recovered_reports if r != recovered])
        click.echo(
            click.style('Reports needed: {}'.format(reports_needed),
                        fg='green'))
    except UnicodeDecodeError:
        click.echo(
            click.style('\nUnable to recover full URL :(', fg='red'))


@click.group()
def cli():
    pass

cli.add_command(simulate)
cli.add_command(recover)
