#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import hashlib
import random
import sys
import argparse

from CTFd import create_app
from CTFd.models import Users, Teams, Challenges, Flags, Awards, ChallengeFiles, Fails, Solves

parser = argparse.ArgumentParser()

parser.add_argument("--mode", help="Set user mode", default="teams")
parser.add_argument("--users", help="Amount of users to generate", default=50, type=int)
parser.add_argument("--teams", help="Amount of teams to generate", default=10, type=int)
parser.add_argument("--challenges", help="Amount of challenges to generate", default=20, type=int)
parser.add_argument("--awards", help="Amount of awards to generate", default=5, type=int)

args = parser.parse_args()

app = create_app()

mode = args.mode
USER_AMOUNT = args.users
TEAM_AMOUNT = args.teams if args.mode == 'teams' else 0
CHAL_AMOUNT = args.challenges
AWARDS_AMOUNT = args.awards

categories = [
    'Exploitation',
    'Reversing',
    'Web',
    'Forensics',
    'Scripting',
    'Cryptography',
    'Networking',
]
lorems = [
    'Lorem', 'ipsum', 'dolor', 'sit', 'amet,', 'consectetur', 'adipiscing', 'elit.',
    'Proin', 'fringilla', 'elit', 'velit,', 'sed', 'scelerisque', 'tellus', 'dapibus',
    'vel.', 'Aenean', 'at', 'urna', 'porta,', 'fringilla', 'erat', 'eget,',
    'lobortis', 'quam.', 'Praesent', 'luctus,', 'quam', 'at', 'consequat', 'luctus,',
    'mauris', 'sem', 'pretium', 'metus,', 'eu', 'viverra', 'dui', 'leo',
    'in', 'tortor.', 'Cras', 'iaculis', 'enim', 'erat,', 'sed', 'gravida',
    'velit', 'consectetur', 'a.', 'Duis', 'eget', 'fermentum', 'elit.', 'Vivamus',
    'laoreet', 'elementum', 'massa,', 'ut', 'sodales', 'mi', 'gravida', 'at.',
    'Vivamus', 'dignissim', 'in', 'eros', 'non', 'iaculis.', 'Vivamus', 'nec',
    'sem', 'fringilla,', 'semper', 'lectus', 'in,', 'malesuada', 'tellus.', 'Vestibulum',
    'mattis', 'commodo', 'enim', 'sit', 'amet', 'scelerisque.', 'Proin', 'at',
    'condimentum', 'nisi,', 'nec', 'fringilla', 'ante.', 'Vestibulum', 'sit', 'amet',
    'neque', 'sit', 'amet', 'elit', 'placerat', 'interdum', 'egestas', 'ac',
    'malesuada', 'quis', 'arcu', 'ac', 'blandit.', 'Vivamus', 'in', 'massa',
    'a', 'purus', 'bibendum', 'sagittis.', 'Nunc', 'venenatis', 'lacus', 'sed',
    'nulla', 'dapibus,', 'consequat', 'laoreet', 'nisi', 'faucibus.', 'Nam', 'consequat',
    'viverra', 'nibh', 'a', 'cursus.', 'Phasellus', 'tristique', 'justo', 'vitae',
    'rutrum', 'pharetra.', 'Sed', 'sed', 'porttitor', 'lacus.', 'Nam', 'ornare',
    'sit', 'amet', 'nisi', 'imperdiet', 'vulputate.', 'Maecenas', 'hendrerit', 'ullamcorper',
    'elit,', 'sed', 'pellentesque', 'lacus', 'bibendum', 'sit', 'amet.', 'Aliquam',
    'consectetur', 'odio', 'quis', 'tellus', 'ornare,', 'id', 'malesuada', 'dui',
    'rhoncus.', 'Quisque', 'fringilla', 'pellentesque', 'nulla', 'id', 'congue.', 'Nulla',
    'ultricies', 'dolor', 'tristique', 'facilisis', 'at', 'accumsan', 'nisi.', 'Praesent',
    'commodo,', 'mauris', 'sit', 'amet', 'placerat', 'condimentum,', 'nibh', 'leo',
    'pulvinar', 'justo,', 'vel', 'dignissim', 'mi', 'dolor', 'et', 'est.',
    'Nulla', 'facilisi.', 'Sed', 'nunc', 'est,', 'lobortis', 'id', 'diam',
    'nec,', 'vulputate', 'varius', 'orci.', 'Maecenas', 'iaculis', 'vehicula', 'eros',
    'eu', 'congue.', 'Nam', 'tempor', 'commodo', 'lobortis.', 'Donec', 'eget',
    'posuere', 'dolor,', 'ut', 'rhoncus', 'tortor.', 'Donec', 'et', 'quam',
    'quis', 'urna', 'rhoncus', 'fermentum', 'et', 'ut', 'tellus.', 'Aliquam',
    'erat', 'volutpat.', 'Morbi', 'porttitor', 'ante', 'nec', 'porta', 'mollis.',
    'Ut', 'sodales', 'pellentesque', 'rutrum.', 'Nullam', 'elit', 'eros,', 'sollicitudin',
    'ac', 'rutrum', 'sit', 'amet,', 'eleifend', 'vel', 'nulla.', 'Morbi',
    'quis', 'lacinia', 'nisi.', 'Integer', 'at', 'neque', 'vel', 'velit',
    'tincidunt', 'elementum', 'lobortis', 'sit', 'amet', 'tellus.', 'Nunc', 'volutpat',
    'diam', 'ac', 'diam', 'lacinia,', 'id', 'molestie', 'quam', 'eu',
    'ultricies', 'ligula.', 'Duis', 'iaculis', 'massa', 'massa,', 'eget', 'venenatis',
    'dolor', 'fermentum', 'laoreet.', 'Nam', 'posuere,', 'erat', 'quis', 'tempor',
    'consequat,', 'purus', 'erat', 'hendrerit', 'arcu,', 'nec', 'aliquam', 'ligula',
    'augue', 'vitae', 'felis.', 'Vestibulum', 'tincidunt', 'ipsum', 'vel', 'pharetra',
    'lacinia.', 'Quisque', 'dignissim,', 'arcu', 'non', 'feugiat', 'semper,', 'felis',
    'est', 'commodo', 'lorem,', 'malesuada', 'elementum', 'nibh', 'lectus', 'porttitor',
    'nisi.', 'Duis', 'non', 'lacinia', 'nisl.', 'Etiam', 'ante', 'nisl,',
    'mattis', 'eget', 'convallis', 'vel,', 'ullamcorper', 'ac', 'nisl.', 'Duis',
    'eu', 'massa', 'at', 'urna', 'laoreet', 'convallis.', 'Donec', 'tincidunt',
    'sapien', 'sit', 'amet', 'varius', 'eu', 'dignissim', 'tortor,', 'elementum',
    'gravida', 'eros.', 'Cras', 'viverra', 'accumsan', 'erat,', 'et', 'euismod',
    'dui', 'placerat', 'ac.', 'Ut', 'tortor', 'arcu,', 'euismod', 'vitae',
    'aliquam', 'in,', 'interdum', 'vitae', 'magna.', 'Vestibulum', 'leo', 'ante,',
    'posuere', 'eget', 'est', 'non,', 'adipiscing', 'ultrices', 'erat.', 'Donec',
    'suscipit', 'felis', 'molestie,', 'ultricies', 'dui', 'a,', 'facilisis', 'magna.',
    'Cum', 'sociis', 'natoque', 'penatibus', 'et', 'magnis', 'dis', 'parturient',
    'montes,', 'nascetur', 'ridiculus', 'mus.', 'Nulla', 'quis', 'odio', 'sit',
    'amet', 'ante', 'tristique', 'accumsan', 'ut', 'iaculis', 'neque.', 'Vivamus',
    'in', 'venenatis', 'enim.', 'Nunc', 'dignissim', 'justo', 'neque,', 'sed',
    'ultricies', 'justo', 'dictum', 'in.', 'Nulla', 'eget', 'nunc', 'ac',
    'arcu', 'vestibulum', 'bibendum', 'vitae', 'quis', 'tellus.', 'Morbi', 'bibendum,',
    'quam', 'ac', 'cursus', 'posuere,', 'purus', 'lectus', 'tempor', 'est,',
    'eu', 'iaculis', 'quam', 'enim', 'a', 'nibh.', 'Etiam', 'consequat',
]
hipsters = [
    'Ethnic', 'narwhal', 'pickled', 'Odd', 'Future', 'cliche', 'VHS', 'whatever',
    'Etsy', 'American', 'Apparel', 'kitsch', 'wolf', 'mlkshk', 'fashion', 'axe',
    'ethnic', 'banh', 'mi', 'cornhole', 'scenester', 'Echo', 'Park', 'Dreamcatcher',
    'tofu', 'selvage', 'authentic', 'cliche', 'High', 'Life', 'brunch',
    'pork', 'belly', 'viral', 'XOXO', 'drinking', 'vinegar', 'bitters', 'Wayfarers',
    'gastropub', 'dreamcatcher', 'chillwave', 'Shoreditch', 'kale', 'chips', 'swag', 'street',
    'art', 'put', 'a', 'bird', 'on', 'it', 'Vice', 'synth',
    'cliche', 'retro', 'Master', 'cleanse', 'ugh', 'Austin', 'slow-carb', 'small',
    'batch', 'Hashtag', 'food', 'truck', 'deep', 'v', 'semiotics', 'chia',
    'normcore', 'bicycle', 'rights', 'Austin', 'drinking', 'vinegar', 'hella', 'readymade',
    'farm-to-table', 'Wes', 'Anderson', 'put', 'a', 'bird', 'on', 'it',
    'freegan', 'Synth', 'lo-fi', 'food', 'truck', 'chambray', 'Shoreditch', 'cliche',
    'kogiSynth', 'lo-fi', 'single-origin', 'coffee', 'brunch', 'butcher', 'Pickled',
    'Etsy', 'locavore', 'forage', 'pug', 'stumptown', 'occupy', 'PBR&B', 'actually',
    'shabby', 'chic', 'church-key', 'disrupt', 'lomo', 'hoodie', 'Tumblr', 'biodiesel',
    'Pinterest', 'butcher', 'Hella', 'Carles', 'pour-over', 'YOLO', 'VHS', 'literally',
    'Selvage', 'narwhal', 'flexitarian', 'wayfarers', 'kitsch', 'bespoke', 'sriracha', 'Banh',
    'mi', '8-bit', 'cornhole', 'viral', 'Tonx', 'keytar', 'gastropub', 'YOLO',
    'hashtag', 'food', 'truck', '3', 'wolf', 'moonFingerstache', 'flexitarian', 'craft',
    'beer', 'shabby', 'chic', '8-bit', 'try-hard', 'semiotics', 'Helvetica', 'keytar',
    'PBR', 'four', 'loko', 'scenester', 'keytar', '3', 'wolf', 'moon',
    'sriracha', 'gluten-free', 'literally', 'try-hard', 'put', 'a', 'bird', 'on',
    'it', 'cornhole', 'blog', 'fanny', 'pack', 'Mumblecore', 'pickled', 'distillery',
    'butcher', 'Ennui', 'tote', 'bag', 'letterpress', 'disrupt', 'keffiyeh', 'art',
    'party', 'aesthetic', 'Helvetica', 'stumptown', 'Wes', 'Anderson', 'next', 'level',
    "McSweeney's", 'cornhole', 'Schlitz', 'skateboard', 'pop-up', 'Chillwave', 'biodiesel', 'semiotics',
    'seitan', 'authentic', 'bicycle', 'rights', 'wolf', 'pork', 'belly', 'letterpress',
    'locavore', 'whatever', 'fixie', 'viral', 'mustache', 'beard', 'Hashtag', 'sustainable',
    'lomo', 'cardigan', 'lo-fiWilliamsburg', 'craft', 'beer', 'bitters', 'iPhone', 'gastropub',
    'messenger', 'bag', 'Organic', 'post-ironic', 'fingerstache', 'ennui', 'banh', 'mi',
    'Art', 'party', 'bitters', 'twee', 'bespoke', 'church-key', 'Intelligentsia', 'sriracha',
    'Echo', 'Park', 'Tofu', 'locavore', 'street', 'art', 'freegan', 'farm-to-table',
    'distillery', 'hoodie', 'swag', 'ugh', 'YOLO', 'VHS', 'Cred', 'hella',
    'readymade', 'distillery', 'Banh', 'mi', 'Echo', 'Park', "McSweeney's,", 'mlkshk',
    'photo', 'booth', 'swag', 'Odd', 'Future', 'squid', 'Tonx', 'craft',
    'beer', 'High', 'Life', 'tousled', 'PBR', 'you', 'probably', "haven't",
    'heard', 'of', 'them', 'locavore', 'PBR&B', 'street', 'art', 'pop-up',
]
names = [
    'James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph',
    'Charles', 'Thomas', 'Christopher', 'Daniel', 'Matthew', 'Donald', 'Anthony', 'Paul',
    'Mark', 'George', 'Steven', 'Kenneth', 'Andrew', 'Edward', 'Brian', 'Joshua',
    'Kevin', 'Ronald', 'Timothy', 'Jason', 'Jeffrey', 'Gary', 'Ryan', 'Nicholas',
    'Eric', 'Stephen', 'Jacob', 'Larry', 'Frank', 'Jonathan', 'Scott', 'Justin',
    'Raymond', 'Brandon', 'Gregory', 'Samuel', 'Patrick', 'Benjamin', 'Jack', 'Dennis',
    'Jerry', 'Alexander', 'Tyler', 'Douglas', 'Henry', 'Peter', 'Walter', 'Aaron',
    'Jose', 'Adam', 'Harold', 'Zachary', 'Nathan', 'Carl', 'Kyle', 'Arthur',
    'Gerald', 'Lawrence', 'Roger', 'Albert', 'Keith', 'Jeremy', 'Terry', 'Joe',
    'Sean', 'Willie', 'Jesse', 'Ralph', 'Billy', 'Austin', 'Bruce', 'Christian',
    'Roy', 'Bryan', 'Eugene', 'Louis', 'Harry', 'Wayne', 'Ethan', 'Jordan',
    'Russell', 'Alan', 'Philip', 'Randy', 'Juan', 'Howard', 'Vincent', 'Bobby',
    'Dylan', 'Johnny', 'Phillip', 'Craig', 'Mary', 'Patricia', 'Elizabeth', 'Jennifer',
    'Linda', 'Barbara', 'Susan', 'Margaret', 'Jessica', 'Dorothy', 'Sarah', 'Karen',
    'Nancy', 'Betty', 'Lisa', 'Sandra', 'Helen', 'Donna', 'Ashley', 'Kimberly',
    'Carol', 'Michelle', 'Amanda', 'Emily', 'Melissa', 'Laura', 'Deborah', 'Stephanie',
    'Rebecca', 'Sharon', 'Cynthia', 'Ruth', 'Kathleen', 'Anna', 'Shirley', 'Amy',
    'Angela', 'Virginia', 'Brenda', 'Pamela', 'Catherine', 'Katherine', 'Nicole', 'Christine',
    'Janet', 'Debra', 'Carolyn', 'Samantha', 'Rachel', 'Heather', 'Maria', 'Diane',
    'Frances', 'Joyce', 'Julie', 'Martha', 'Joan', 'Evelyn', 'Kelly', 'Christina',
    'Emma', 'Lauren', 'Alice', 'Judith', 'Marie', 'Doris', 'Ann', 'Jean',
    'Victoria', 'Cheryl', 'Megan', 'Kathryn', 'Andrea', 'Jacqueline', 'Gloria', 'Teresa',
    'Janice', 'Sara', 'Rose', 'Julia', 'Hannah', 'Theresa', 'Judy', 'Mildred',
    'Grace', 'Beverly', 'Denise', 'Marilyn', 'Amber', 'Danielle', 'Brittany', 'Diana',
    'Jane', 'Lori', 'Olivia', 'Tiffany', 'Kathy', 'Tammy', 'Crystal', 'Madison',
]
emails = [
    '@gmail.com',
    '@yahoo.com',
    '@outlook.com',
    '@hotmail.com',
    '@mailinator.com',
    '@poly.edu',
    '@nyu.edu'
]
extensions = [
    '.doc', '.log', '.msg', '.rtf', '.txt', '.wpd', '.wps', '.123',
    '.csv', '.dat', '.db', '.dll', '.mdb', '.pps', '.ppt', '.sql',
    '.wks', '.xls', '.xml', '.mng', '.pct', '.bmp', '.gif', '.jpe',
    '.jpg', '.png', '.psd', '.psp', '.tif', '.ai', '.drw', '.dxf',
    '.eps', '.ps', '.svg', '.3dm', '.3dm', '.ind', '.pdf', '.qxd',
    '.qxp', '.aac', '.aif', '.iff', '.m3u', '.mid', '.mid', '.mp3',
    '.mpa', '.ra', '.ram', '.wav', '.wma', '.3gp', '.asf', '.asx',
    '.avi', '.mov', '.mp4', '.mpg', '.qt', '.rm', '.swf', '.wmv',
    '.asp', '.css', '.htm', '.htm', '.js', '.jsp', '.php', '.xht',
    '.fnt', '.fon', '.otf', '.ttf', '.8bi', '.plu', '.xll', '.cab',
    '.cpl', '.cur', '.dmp', '.drv', '.key', '.lnk', '.sys', '.cfg',
    '.ini', '.reg', '.app', '.bat', '.cgi', '.com', '.exe', '.pif',
    '.vb', '.ws', '.deb', '.gz', '.pkg', '.rar', '.sea', '.sit',
    '.sit', '.zip', '.bin', '.hqx', '.0 E', '.mim', '.uue', '.cpp',
    '.jav', '.pl', '.bak', '.gho', '.old', '.ori', '.tmp', '.dmg',
    '.iso', '.toa', '.vcd', '.gam', '.nes', '.rom', '.sav', '.msi',
]
companies = [
    'Corp',
    'Inc.',
    'Squad',
    'Team',
]


def gen_sentence():
    return ' '.join(random.sample(lorems, 50))


def gen_name():
    return random.choice(names)


def gen_team_name():
    return random.choice(hipsters).capitalize() + str(random.randint(1, 1000))


def gen_email():
    return random.choice(emails)


def gen_category():
    return random.choice(categories)


def gen_affiliation():
    return (random.choice(hipsters) + " " + random.choice(companies)).title()


def gen_value():
    return random.choice(range(100, 500, 50))


def gen_word():
    return random.choice(hipsters)


def gen_file():
    return gen_word() + random.choice(extensions)


def random_date(start, end):
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))


def random_chance():
    return random.random() > 0.5


if __name__ == '__main__':
    with app.app_context():
        db = app.db

        # Generating Challenges
        print("GENERATING CHALLENGES")
        for x in range(CHAL_AMOUNT):
            word = gen_word()
            chal = Challenges(
                name=word,
                description=gen_sentence(),
                value=gen_value(),
                category=gen_category()
            )
            db.session.add(chal)
            db.session.commit()
            f = Flags(
                challenge_id=x + 1,
                content=word,
                type='static'
            )
            db.session.add(f)
            db.session.commit()

        # Generating Files
        print("GENERATING FILES")
        AMT_CHALS_WITH_FILES = int(CHAL_AMOUNT * (3.0 / 4.0))
        for x in range(AMT_CHALS_WITH_FILES):
            chal = random.randint(1, CHAL_AMOUNT)
            filename = gen_file()
            md5hash = hashlib.md5(filename.encode('utf-8')).hexdigest()
            chal_file = ChallengeFiles(
                challenge_id=chal,
                location=md5hash + '/' + filename
            )
            db.session.add(chal_file)

        db.session.commit()

        # Generating Teams
        print("GENERATING TEAMS")
        used = []
        used_oauth_ids = []
        count = 0
        while count < TEAM_AMOUNT:
            name = gen_team_name()
            if name not in used:
                used.append(name)
                team = Teams(
                    name=name,
                    password="password"
                )
                if random_chance():
                    team.affiliation = gen_affiliation()
                if random_chance():
                    oauth_id = random.randint(1, 1000)
                    while oauth_id in used_oauth_ids:
                        oauth_id = random.randint(1, 1000)
                    used_oauth_ids.append(oauth_id)
                    team.oauth_id = oauth_id
                db.session.add(team)
                count += 1

        db.session.commit()

        # Generating Users
        print("GENERATING USERS")
        used = []
        used_oauth_ids = []
        count = 0
        while count < USER_AMOUNT:
            name = gen_name()
            if name not in used:
                used.append(name)
                try:
                    user = Users(
                        name=name,
                        email=name + gen_email(),
                        password='password'
                    )
                    user.verified = True
                    if random_chance():
                        user.affiliation = gen_affiliation()
                    if random_chance():
                        oauth_id = random.randint(1, 1000)
                        while oauth_id in used_oauth_ids:
                            oauth_id = random.randint(1, 1000)
                        used_oauth_ids.append(oauth_id)
                        user.oauth_id = oauth_id
                    if mode == 'teams':
                        user.team_id = random.randint(1, TEAM_AMOUNT)
                    db.session.add(user)
                    count += 1
                except Exception:
                    pass

        db.session.commit()

        if mode == 'teams':
            # Assign Team Captains
            print("GENERATING TEAM CAPTAINS")
            teams = Teams.query.all()
            for team in teams:
                captain = Users.query.filter_by(team_id=team.id).order_by(Users.id).limit(1).first()
                if captain:
                    team.captain_id = captain.id
            db.session.commit()

        # Generating Solves
        print("GENERATING SOLVES")
        if mode == 'users':
            for x in range(USER_AMOUNT):
                used = []
                base_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=-10000)
                for y in range(random.randint(1, CHAL_AMOUNT)):
                    chalid = random.randint(1, CHAL_AMOUNT)
                    if chalid not in used:
                        used.append(chalid)
                        user = Users.query.filter_by(id=x + 1).first()
                        solve = Solves(
                            user_id=user.id,
                            team_id=user.team_id,
                            challenge_id=chalid,
                            ip='127.0.0.1',
                            provided=gen_word()
                        )

                        new_base = random_date(base_time, base_time + datetime.timedelta(minutes=random.randint(30, 60)))
                        solve.date = new_base
                        base_time = new_base

                        db.session.add(solve)
                        db.session.commit()
        elif mode == 'teams':
            for x in range(1, TEAM_AMOUNT):
                used_teams = []
                used_users = []
                base_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=-10000)
                team = Teams.query.filter_by(id=x).first()
                members_ids = [member.id for member in team.members]
                for y in range(random.randint(1, CHAL_AMOUNT)):
                    chalid = random.randint(1, CHAL_AMOUNT)
                    user_id = random.choice(members_ids)
                    if (chalid, team.id) not in used_teams:
                        if (chalid, user_id) not in used_users:
                            solve = Solves(
                                user_id=user_id,
                                team_id=team.id,
                                challenge_id=chalid,
                                ip='127.0.0.1',
                                provided=gen_word()
                            )
                            new_base = random_date(
                                base_time,
                                base_time + datetime.timedelta(minutes=random.randint(30, 60))
                            )
                            solve.date = new_base
                            base_time = new_base
                            db.session.add(solve)
                            db.session.commit()
                            used_teams.append((chalid, team.id))
                            used_users.append((chalid, user_id))

        db.session.commit()

        # Generating Awards
        print("GENERATING AWARDS")
        for x in range(USER_AMOUNT):
            base_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=-10000)
            for _ in range(random.randint(0, AWARDS_AMOUNT)):
                user = Users.query.filter_by(id=x + 1).first()
                award = Awards(
                    user_id=user.id,
                    team_id=user.team_id,
                    name=gen_word(),
                    value=random.randint(-10, 10)
                )
                new_base = random_date(base_time, base_time + datetime.timedelta(minutes=random.randint(30, 60)))
                award.date = new_base
                base_time = new_base

                db.session.add(award)

        db.session.commit()

        # Generating Wrong Flags
        print("GENERATING WRONG FLAGS")
        for x in range(USER_AMOUNT):
            used = []
            base_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=-10000)
            for y in range(random.randint(1, CHAL_AMOUNT * 20)):
                chalid = random.randint(1, CHAL_AMOUNT)
                if chalid not in used:
                    used.append(chalid)
                    user = Users.query.filter_by(id=x + 1).first()
                    wrong = Fails(
                        user_id=user.id,
                        team_id=user.team_id,
                        challenge_id=chalid,
                        ip='127.0.0.1',
                        provided=gen_word()
                    )

                    new_base = random_date(base_time, base_time + datetime.timedelta(minutes=random.randint(30, 60)))
                    wrong.date = new_base
                    base_time = new_base

                    db.session.add(wrong)
                    db.session.commit()

        db.session.commit()
        db.session.close()
