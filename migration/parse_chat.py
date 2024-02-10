import re
from datetime import datetime, timedelta

from dotenv import load_dotenv
from regex import regex

load_dotenv()


class LastDuel:
    challenger = None
    target = None

    def update(self, challenger, target):
        self.challenger = challenger
        self.target = target

    def get_winner(self, loser):
        return self.challenger if self.target == loser else self.target


def clean_line(line):
    line = line.strip()
    if '[singsing]' not in line:
        return
    if '[singsing] [{} 0] null:' in line:
        return
    if '[singsing] [{} 0] nightbot:' in line:
        return
    if '[SUBS] [singsing]' in line:
        return
    if '[singsing] [mods]' in line:
        return
    if '[ONLINE] [singsing]' in line:
        return
    if '[OFFLINE] [singsing]' in line:
        return

    # INFO 2024-01-14 13:46:07,080 [singsing] [{subscriber=27} 27] darth_pantsu: SingSongDinkDonk pepegaStealth double mod EZ
    # INFO 2024-01-22 06:20:09,647 [singsing] [{} 0] skyseskyse: !game
    if match := re.search(
            r'INFO (?P<time>2024-01-\d\d \d\d:\d\d:\d\d,\d\d\d) \[singsing] \[\{.*?} \d+] (?P<message>.*)', line):
        time = match.group('time')
        message = match.group('message')

        # INFO 2024-01-22 06:38:08,122 [singsing] [{subscriber=18} 18] guanyinma: mistermonsieur FAILURE GROUPA
        # 2024-01-21 23:38:07.908000 guanyinma : mistermonsieur FAILURE GROUPA
        input_datetime = datetime.strptime(time, '%Y-%m-%d %H:%M:%S,%f')
        converted_datetime = input_datetime - timedelta(hours=7)
        time = converted_datetime.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]

        return time, message
    else:
        print(line)


def parse_message(line, last_duel):
    author, message = line.split(':', 1)
    author = author.strip().lower()
    message = message.strip()

    if author == 'skwishi':
        if match := re.search(r'singsingRingring (?P<users>([a-zA-Z0-9_]{4,25}\s?)+)', message):
            pinged_users = match.group('users').lower()
            return f'pinged: {pinged_users}'
        elif match := regex.search(r'(?P<loser>\S+) has lost this round', message):
            loser = match.group('loser').lower()
            if loser in [last_duel.challenger, last_duel.target]:
                winner = last_duel.get_winner(loser)
            else:
                winner = 'unknown'
            return f'{loser} lost shootout against {winner}'
        elif match := regex.search(
                r'(?P<display_name>[\p{L}|\p{N}_]+) has snapped their line and got nothing. Try again later', message):
            display_name = match.group('display_name').lower()
            if not re.match(r'[a-z0-9_]{4,25}', display_name):
                return f'{display_name} not in cache, {line=}'
            else:
                fisherman = display_name
            return f'{fisherman} snapped'
        elif match := regex.search(r'(?P<display_name>[\p{L}|\p{N}_]+) has caught a (new species of )?fish '
                                   r'called the (?P<fish>[a-zA-Z0-9_]{4,25}) (for|worth) '
                                   r'(?P<points>[0-9]+) (angler )?points. OOOO', message):
            display_name = match.group('display_name').lower()
            if not re.match(r'[a-z0-9_]{4,25}', display_name):
                return f'{display_name} not in cache, {line=}'
            else:
                fisherman = display_name
            fish = match.group('fish').lower()
            points = int(match.group('points'))
            return f'{fisherman} caught {fish} for {points} points'
    elif re.search('!randomping(.*)', message):
        return f'{author} randompinged'
    elif match := re.search(r'!shootout (?P<target>\S+)( .{4+})?', message):
        challenger = author
        target = match.group('target').lower()
        last_duel.update(challenger, target)
        return f'{challenger} dueled {target}'
    elif re.search(r'!cast(.*)', message):
        return f'{author} tried casting'


def parse():
    last_duel = LastDuel()

    with open('jan_chat_input.txt', 'r', encoding='utf-8') as infile:
        with open('jan_chat_parsed.txt', 'w') as outfile:
            for line in infile:
                result = clean_line(line)
                if result:
                    time, message = result
                    parsed_message = parse_message(message, last_duel)
                    if parsed_message:
                        parsed_message = parsed_message.strip().replace('@', '')
                        # 2024-01-21 23:52:58,983 INFO     bot                       event_message             sandap dueled abc1ndy
                        outfile.write(
                            f'{time} INFO     bot                       event_message             {parsed_message}\n')


def main():
    parse()


if __name__ == '__main__':
    main()
