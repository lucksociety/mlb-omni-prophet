import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path: sys.path.append(ROOT_DIR)
for folder in ['models', 'utils', 'recording', 'ingestion', 'models/K Prophet', 'models/HR']:
    path = os.path.join(ROOT_DIR, folder)
    if path not in sys.path: sys.path.append(path)
#!/usr/bin/env python3
"""
MLB QUANT-ELITE V9.0 PROTOCOL: HOU @ BOS
Date: May 2, 2026
Task: Forensic Deep-Research Audit & 100,000-Iteration Monte Carlo Simulation
"""

from quant_elite_v9 import run_v9_protocol

# ── 1. DEEP RESEARCH AUDIT ──────────────────────────────────────
# Roster Verification:
# HOU SP: Spencer Arrighetti (R) | 2026: 3-0, 2.00 ERA, 1.15 WHIP, 26.9% K%
# BOS SP: Connelly Early (L) | 2026: 2-1, 2.84 ERA, 21.4% K%
#
# Environmental Physics:
# Venue: Fenway Park (PF: 105)
# Weather: 54°F, 2mph SSE Wind, 66% Humidity, Showers (Rain Intensity: 1)
# 
# Logistics Audit:
# Travel: HOU (Away) from CST to EST (+1 hr). 
# Fatigue: HOU Bullpen high fatigue (Abreu, Alexander, De Los Santos high usage d2).
#          BOS Bullpen medium fatigue (Chapman, Whitlock, Kelly used yesterday).
#
# The Human Element:
# Umpire: Neutral Zone assumed.
# Catcher: Yainer Diaz (HOU) vs Connor Wong (BOS).
# ────────────────────────────────────────────────────────────────

# LINEUPS (Confirmed)
hou_lineup = [
    ('Carlos Correa', 'R'),
    ('Yordan Alvarez', 'L'),
    ('Isaac Paredes', 'R'),
    ('Christian Walker', 'R'),
    ('Jose Altuve', 'R'),
    ('Yainer Diaz', 'R'),
    ('Brice Matthews', 'R'),
    ('Cam Smith', 'R'),
    ('Dustin Harris', 'L')
]

bos_lineup = [
    ('Jarren Duran', 'L'),
    ('Willson Contreras', 'R'),
    ('Roman Anthony', 'L'),
    ('Wilyer Abreu', 'L'),
    ('Trevor Story', 'R'),
    ('Marcelo Mayer', 'L'),
    ('Ceddanne Rafaela', 'R'),
    ('Connor Wong', 'R'),
    ('Caleb Durbin', 'R')
]

if __name__ == '__main__':
    # EXECUTE QUANT-ELITE V9.0 PROTOCOL
    run_v9_protocol(
        away_team='HOU',
        home_team='BOS',
        away_sp_name='Spencer Arrighetti',
        home_sp_name='Connelly Early',
        away_sp_hand='R',
        home_sp_hand='L',
        away_era=2.00,
        home_era=2.84,
        away_lineup=hou_lineup,
        home_lineup=bos_lineup,
        park_factor=105,
        is_dome=False,
        temp_f=54,
        wind_mph=2,
        wind_ang=110, # SSE wind at Fenway (slight in/across)
        humidity=66,
        altitude=20,
        rain_intensity=1,
        away_drs=-3,
        home_drs=4,
        away_manager_hook=-0.2,
        home_manager_hook=0.1,
        away_bp_pitches_d1=14, # King, Sousa
        away_bp_pitches_d2=83, # Alexander, Abreu, De Los Santos
        home_bp_pitches_d1=51, # Kelly, Whitlock, Chapman
        home_bp_pitches_d2=0,
        umpire_zone='neutral',
        away_catcher='Yainer Diaz',
        home_catcher='Connor Wong',
        game_time='16:10',
        is_game_1=False
    )