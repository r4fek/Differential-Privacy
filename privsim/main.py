import sys
import click
from collections import Counter
from string import digits, letters, punctuation
import random

random = random.SystemRandom()
ascii = digits + letters + punctuation


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


def simulate(url, privacy):
    assert 0 < privacy < 1
    counters = [Counter() for _ in xrange(len(url))]
    num_generated = 0

    while True:
        num_generated += 1
        masked = generate_masked_url(url, privacy)
        for i, letter in enumerate(masked):
            counters[i][letter] += 1

        sys.stdout.write('\rrecov: {} | gen: {}'.format(
            ''.join([counters[i].most_common(1)[0][0] for i in xrange(len(url))]), masked))
        sys.stdout.flush()

        if check_reports(url, counters):
            click.echo(
                click.style('\n\n{} reports required to recover the original URL {} with privacy level {}%'
                            .format(num_generated, url, privacy*100.0), fg='green'))
            return


@click.command()
@click.argument('url', default='http://stackoverflow.com/questions/5290994/python-remove-and-replace-printed-items')
@click.option('-p', '--privacy', default=90.0, help='Level of privacy <100. Higher == better user privacy')
def main(url, privacy):
    simulate(url, privacy/100.0)


if __name__ == '__main__':
    main()
