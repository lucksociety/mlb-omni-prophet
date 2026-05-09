import subprocess
import json

games = [
    ("BOS", "DET", "Brayan Bello", "Framber Valdez", 
     "Jarren Duran,W. Contreras,Wilyer Abreu,Trevor Story,C. Rafaela,A. Monasterio,Caleb Durbin,Connor Wong,I. Kiner-Falefa", 
     "M. Vierling,K. McGonigle,Jahmai Jones,D. Dingler,Riley Greene,W. Perez,S. Torkelson,Z. McKinstry,Hao-Yu Lee"),
    
    ("OAK", "PHI", "Luis Severino", "C. Sanchez",
     "Jacob Wilson,Brent Rooker,Nick Kurtz,Colby Thomas,Zack Gelof,T. Soderstrom,Austin Wynns,D. Hernaiz,Brett Harris",
     "Trea Turner,K. Schwarber,Bryce Harper,A. Garcia,B. Marsh,J. Realmuto,Bryson Stott,Alec Bohm,J. Crawford"),
     
    ("BAL", "MIA", "Chris Bassitt", "Sandy Alcantara",
     "G. Henderson,Taylor Ward,D. Beavers,Pete Alonso,S. Basallo,L. Taveras,C. Cowser,Coby Mayo,B. Alexander",
     "X. Edwards,Liam Hicks,Otto Lopez,Kyle Stowers,Jakob Marsee,Connor Norby,Joe Mack,Owen Caissie,G. Pauley"),
     
    ("TOR", "TB", "Kevin Gausman", "Drew Rasmussen",
     "G. Springer,Y. Pinango,K. Okamoto,J. Sanchez,Lenyn Sosa,D. Varsho,E. Clement,A. Gimenez,B. Valenzuela",
     "C. Simpson,J. Caminero,J. Aranda,Yandy Diaz,Jake Fraley,B. Williamson,C. Mullins,H. Feduccia,R. Palacios"),
     
    ("MIN", "WSH", "Taj Bradley", "Cade Cavalli",
     "Byron Buxton,T. Larnach,Ryan Jeffers,Josh Bell,A. Martin,Kody Clemens,L. Keaschall,Brooks Lee,Royce Lewis",
     "James Wood,Daylen Lile,Curtis Mead,CJ Abrams,Jacob Young,Jorbit Vivas,Nasim Nunez,Jose Tena,Keibert Ruiz"),
     
    ("TEX", "NYY", "Jacob deGrom", "Elmer Rodriguez",
     "Evan Carter,Corey Seager,Josh Jung,Joc Pederson,E. Duran,Jake Burger,A. Osuna,Danny Jansen,A. McCutchen",
     "T. Grisham,Aaron Judge,C. Bellinger,J. Dominguez,J. Chisholm,P. Goldschmidt,Austin Wells,Ryan McMahon,J. Caballero"),
     
    ("CLE", "KC", "Gavin Williams", "Stephen Kolek",
     "Steven Kwan,C. DeLauter,Jose Ramirez,K. Manzardo,Rhys Hoskins,D. Schneemann,T. Bazzana,A. Martinez,Bo Naylor",
     "M. Garcia,Bobby Witt,V. Pasquantino,S. Perez,C. Jensen,J. Caglianone,I. Collins,M. Massey,Kyle Isbel"),
     
    ("CIN", "CHC", "Andrew Abbott", "Jameson Taillon",
     "TJ Friedl,JJ Bleday,E. De La Cruz,Sal Stewart,N. Lowe,S. Steer,T. Stephenson,Matt McLain,K. Hayes",
     "Nico Hoerner,Alex Bregman,Ian Happ,Seiya Suzuki,Carson Kelly,M. Busch,D. Swanson,P. Crow-Armstrong,Matt Shaw"),
     
    ("MIL", "STL", "Brandon Sproat", "Andre Pallante",
     "G. Mitchell,J. Chourio,Brice Turang,W. Contreras,Jake Bauers,A. Vaughn,Sal Frelick,Luis Rengifo,D. Hamilton",
     "J. Wetherholt,Ivan Herrera,A. Burleson,J. Walker,Nolan Gorman,Masyn Winn,N. Church,Pedro Pages,Victor Scott"),
     
    ("LAD", "HOU", "Shohei Ohtani", "Peter Lambert",
     "D. Rushing,F. Freeman,Will Smith,Kyle Tucker,T. Hernandez,Max Muncy,Andy Pages,A. Freeland,Miguel Rojas",
     "C. Correa,Y. Alvarez,I. Paredes,C. Walker,Jose Altuve,Cam Smith,Zach Cole,C. Vazquez,Nick Allen"),
     
    ("CWS", "LAA", "Erick Fedde", "Sam Aldegheri",
     "C. Meidroth,M. Vargas,M. Murakami,R. Grichuk,C. Montgomery,Edgar Quero,Derek Hill,Drew Romo,L. Acuna",
     "Zach Neto,Mike Trout,Yoan Moncada,Jorge Soler,N. Schanuel,Jo Adell,Josh Lowe,V. Grissom,T. d'Arnaud"),
     
    ("ATL", "SEA", "Bryce Elder", "George Kirby",
     "M. Harris,D. Baldwin,Matt Olson,Ozzie Albies,Austin Riley,Sean Murphy,M. Dubon,M. Yastrzemski,Eli White",
     "J. Crawford,Cal Raleigh,J. Rodriguez,Josh Naylor,R. Arozarena,Luke Raley,D. Canzone,Cole Young,Leo Rivas"),
     
    ("PIT", "ARI", "Bubba Chandler", "E. Rodriguez",
     "Jake Mangum,N. Gonzales,B. Reynolds,M. Ozuna,Oneil Cruz,Jared Triolo,K. Griffin,Joey Bart,Billy Cook",
     "G. Perdomo,Ketel Marte,C. Carroll,G. Moreno,I. Vargas,L. Gurriel,N. Arenado,J. Fernandez,Alek Thomas"),
     
    ("SD", "SF", "Walker Buehler", "Logan Webb",
     "R. Laureano,F. Tatis,J. Merrill,M. Machado,X. Bogaerts,Gavin Sheets,M. Andujar,L. Campusano,J. Cronenworth",
     "Jung Hoo Lee,Luis Arraez,Matt Chapman,R. Devers,Willy Adames,B. Eldridge,Heliot Ramos,Drew Gilbert,P. Bailey")
]

missing_pitchers = set()
missing_batters = set()

for g in games:
    away, home, away_sp, home_sp, away_l, home_l = g
    cmd = [
        "python3", "/Users/danielreiss/Desktop/Antigravity/MLB/auto_sim_v16.py",
        "--away", away, "--home", home,
        "--away_sp", away_sp, "--home_sp", home_sp,
        "--away_lineup", away_l,
        "--home_lineup", home_l,
        "--check_data"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        data = json.loads(res.stdout)
        for p in data.get("missing_pitchers", []): missing_pitchers.add(p)
        for b in data.get("missing_batters", []): missing_batters.add(b)
    except:
        pass

print("--- PITCHERS ---")
for p in sorted(list(missing_pitchers)): print(p)
print("\n--- BATTERS ---")
for b in sorted(list(missing_batters)): print(b)
