import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)
GAMES = [
    {
        "away": {"team": "Cardinals", "pitcher": "Hunter Dobbins", "lineup": ["JJ Wetherholt", "Iván Herrera", "Alec Burleson", "Jordan Walker", "Nolan Gorman", "Masyn Winn", "Nathan Church", "Pedro Pagés", "Victor Scott II"]},
        "home": {"team": "Pirates", "pitcher": "Paul Skenes", "lineup": ["Oneil Cruz", "Brandon Lowe", "Bryan Reynolds", "Ryan O'Hearn", "Marcell Ozuna", "Nick Gonzales", "Spencer Horwitz", "Konnor Griffin", "Henry Davis"]},
        "umpire": "MISSING"
    },
    {
        "away": {"team": "Phillies", "pitcher": "Andrew Painter", "lineup": ["Trea Turner", "Kyle Schwarber", "Bryce Harper", "Adolis García", "Brandon Marsh", "Bryson Stott", "Alec Bohm", "Justin Crawford", "Rafael Marchán"]},
        "home": {"team": "Giants", "pitcher": "Adrian Houser", "lineup": ["Jung Hoo Lee", "Matt Chapman", "Luis Arraez", "Casey Schmitt", "Rafael Devers", "Willy Adames", "Heliot Ramos", "Drew Gilbert", "Patrick Bailey"]},
        "umpire": "MISSING"
    },
    {
        "away": {"team": "Rockies", "pitcher": "Michael Lorenzen", "lineup": ["Edouard Julien", "Mickey Moniak", "Hunter Goodman", "TJ Rumfield", "Tyler Freeman", "Troy Johnston", "Kyle Karros", "Ezequiel Tovar", "Jake McCarthy"]},
        "home": {"team": "Reds", "pitcher": "Andrew Abbott", "lineup": ["Dane Myers", "Matt McLain", "Elly De La Cruz", "Sal Stewart", "Spencer Steer", "Nathaniel Lowe", "Tyler Stephenson", "Rece Hinds", "Ke'Bryan Hayes"]},
        "umpire": "MISSING"
    },
    {
        "away": {"team": "Astros", "pitcher": "Lance McCullers Jr.", "lineup": ["Carlos Correa", "Yordan Alvarez", "Isaac Paredes", "Jose Altuve", "Christian Walker", "Yainer Diaz", "Dustin Harris", "Cam Smith", "Brice Matthews"]},
        "home": {"team": "Orioles", "pitcher": "Brandon Young", "lineup": ["Gunnar Henderson", "Taylor Ward", "Adley Rutschman", "Pete Alonso", "Samuel Basallo", "Leody Taveras", "Dylan Beavers", "Coby Mayo", "Jeremiah Jackson"]},
        "umpire": "MISSING"
    },
    {
        "away": {"team": "Tigers", "pitcher": "Framber Valdez", "lineup": ["Jahmai Jones", "Gleyber Torres", "Kevin McGonigle", "Matt Vierling", "Dillon Dingler", "Riley Greene", "Spencer Torkelson", "Hao-Yu Lee", "Javier Báez"]},
        "home": {"team": "Braves", "pitcher": "Bryce Elder", "lineup": ["Ronald Acuña Jr.", "Drake Baldwin", "Matt Olson", "Ozzie Albies", "Michael Harris II", "Austin Riley", "Dominic Smith", "Mauricio Dubón", "Mike Yastrzemski"]},
        "umpire": "MISSING"
    },
    {
        "away": {"team": "Nationals", "pitcher": "Miles Mikolas", "lineup": ["James Wood", "Luis García Jr.", "Brady House", "CJ Abrams", "Daylen Lile", "Jacob Young", "Nasim Nuñez", "José Tena", "Keibert Ruiz"]},
        "home": {"team": "Mets", "pitcher": "Freddy Peralta", "lineup": ["Bo Bichette", "Juan Soto", "Francisco Alvarez", "MJ Melendez", "Mark Vientos", "Brett Baty", "Marcus Semien", "Carson Benge", "Ronny Mauricio"]},
        "umpire": "MISSING"
    },
    {
        "away": {"team": "Blue Jays", "pitcher": "Kevin Gausman", "lineup": ["Myles Straw", "Ernie Clement", "Vladimir Guerrero Jr.", "Kazuma Okamoto", "Daulton Varsho", "Eloy Jiménez", "Davis Schneider", "Tyler Heineman", "Andrés Giménez"]},
        "home": {"team": "Twins", "pitcher": "Bailey Ober", "lineup": ["Byron Buxton", "Trevor Larnach", "Austin Martin", "Josh Bell", "Kody Clemens", "Victor Caratini", "Luke Keaschall", "Tristan Gray", "Royce Lewis"]},
        "umpire": "MISSING"
    },
    {
        "away": {"team": "Angels", "pitcher": "José Soriano", "lineup": ["Zach Neto", "Mike Trout", "Yoán Moncada", "Jorge Soler", "Nolan Schanuel", "Jo Adell", "Josh Lowe", "Travis d'Arnaud", "Adam Frazier"]},
        "home": {"team": "White Sox", "pitcher": "Davis Martin", "lineup": ["Andrew Benintendi", "Munetaka Murakami", "Miguel Vargas", "Colson Montgomery", "Everson Pereira", "Sam Antonacci", "Chase Meidroth", "Tristan Peters", "Drew Romo"]},
        "umpire": "MISSING"
    },
    {
        "away": {"team": "Diamondbacks", "pitcher": "Michael Soroka", "lineup": ["Ildemaro Vargas", "Ketel Marte", "Corbin Carroll", "Lourdes Gurriel Jr.", "Adrian Del Castillo", "Jose Fernandez", "Nolan Arenado", "Alek Thomas", "James McCann"]},
        "home": {"team": "Brewers", "pitcher": "Brandon Woodruff", "lineup": ["Brice Turang", "William Contreras", "Jake Bauers", "Gary Sánchez", "Garrett Mitchell", "Sal Frelick", "Luis Rengifo", "David Hamilton", "Brandon Lockridge"]},
        "umpire": "MISSING"
    },
    {
        "away": {"team": "Royals", "pitcher": "Noah Cameron", "lineup": ["Maikel Garcia", "Bobby Witt Jr.", "Vinnie Pasquantino", "Salvador Perez", "Carter Jensen", "Michael Massey", "Jac Caglianone", "Isaac Collins", "Kyle Isbel"]},
        "home": {"team": "Athletics", "pitcher": "Jeffrey Springs", "lineup": ["Shea Langeliers", "Nick Kurtz", "Brent Rooker", "Tyler Soderstrom", "Colby Thomas", "Jacob Wilson", "Max Muncy", "Darell Hernaiz", "Zack Gelof"]},
        "umpire": "MISSING"
    }
]