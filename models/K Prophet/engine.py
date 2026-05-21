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
#!/usr/bin/env python3
import math
import random
from typing import Dict, List, Tuple

class KProphetEngine:
    """
    K PROPHET V11.2 — THE STOCHASTIC SINGULARITY (Overdispersed)
    Deterministic Reality Engine (DRE) - Ultimate Precision State.
    ===================================================================
    V11.2 Patch: Introduced Stochastic Volatility & Chaos Injection.
    Widened K-distributions to reflect real-world variance and prevent 
    artificially tight probability clustering (The "Insane Probability" Fix).
    """
    def __init__(self, settings=None):
        self.settings = settings or {}
        self.MLB_AVG_K_PCT = 22.7
        self.MLB_AVG_SWSTR = 11.0
        self.MLB_AVG_CSW = 27.0
        
        # 2026 League Benchmarks (Induced Movement)
        self.BENCHMARKS = {
            '4-Seam': {'IVB': 16.0, 'HB': 7.5},
            'Sinker': {'IVB': 9.0, 'HB': 15.0},
            'Sweeper': {'IVB': 1.0, 'HB': 17.5},
            'Curveball': {'IVB': -11.0, 'HB': 10.0},
        }

        # Bible Constants & 2026 Performance Leaders
        self.ARCHETYPES = {
            'Ryne Nelson': {'type': 'North-South', 'mult': 1.15, 'vol': 1.2, 'IVB': 18.9, 'floor_adj': 0.0},
            'Dylan Cease': {'type': 'Unicorn', 'mult': 1.18, 'vol': 1.1, 'HB': 15.5, 'floor_adj': 0.0},
            'Andrew Painter': {'type': 'North-South', 'mult': 1.12, 'vol': 1.1, 'IVB': 17.5, 'floor_adj': 0.0},
            'Carlos Lagrange': {'type': 'North-South', 'mult': 1.25, 'vol': 1.3, 'IVB': 18.5, 'floor_adj': 0.0},
            'Framber Valdez': {'type': 'Unicorn', 'mult': 1.12, 'vol': 1.1, 'floor_adj': 0.0}, 
        }
        
        self.CATCHER_TIERS = {
            'Patrick Bailey': 1.15,
            'Travis d\'Arnaud': 1.08,
            'Sean Murphy': 1.10,
            'Alejandro Kirk': 1.10,
            'Austin Wells': 1.10,
            'Cal Raleigh': 1.08,
            'Will Smith': 1.05,
            'Francisco Alvarez': 1.05,
            'Henry Davis': 0.95,
            'Edgar Quero': 0.85,
        }

    def calculate_platoon_mod(self, p_hand: str, b_hand: str, pitcher_name: str, pitcher_data: Dict = None) -> float:
        """Vision Geometry: Handedness Advantage."""
        arch_data = self.ARCHETYPES.get(pitcher_name)
        if not arch_data and pitcher_data:
            arch_data = self.detect_archetype(pitcher_data)
        else:
            arch_data = arch_data or {'type': 'Standard', 'mult': 1.0}
            
        arch = arch_data['type']
        
        if b_hand == 'S': return 1.0
        
        if p_hand == b_hand:
            if arch == 'East-West': return 1.15 
            if arch == 'Unicorn': return 1.10
            return 1.08
        else:
            if arch == 'East-West': return 0.88
            if arch == 'Unicorn': return 1.05 
            return 0.95

    def calculate_synergy_score(self, p: Dict, catcher: Dict) -> float:
        """V20: Strategic alignment between pitcher arsenal and catcher framing style."""
        arch_data = self.detect_archetype(p)
        arch = arch_data['type']
        
        c_name = catcher.get('Name', 'Unknown')
        
        # High-End Framers (North-South specialists)
        ns_framers = ['Patrick Bailey', 'Dillon Dingler', 'Austin Wells']
        # Low-Ball specialists
        ew_framers = ['Alejandro Kirk', 'Cal Raleigh']
        
        synergy = 1.0
        if arch == 'North-South' and c_name in ns_framers:
            synergy = 1.06 
        elif arch == 'East-West' and c_name in ew_framers:
            synergy = 1.04 
            
        return synergy

    def detect_archetype(self, p: Dict) -> Dict:
        """Dynamically detect pitcher archetype from Statcast/Movement metrics."""
        ivb = p.get('IVB', 16.0)
        hb = p.get('HB', 7.5)
        fa_stuff = p.get('Pit+ FA', 100)
        si_stuff = p.get('Pit+ SI', 100)
        sl_stuff = p.get('Pit+ SL', 100)
        vaa = p.get('VAA', -4.5)
        
        if ivb > 18.0 or vaa > -4.1 or fa_stuff > 115:
            return {'type': 'North-South', 'mult': 1.15, 'vol': 1.2, 'IVB': ivb, 'floor_adj': 0.0}
            
        if hb > 14.0 or (si_stuff > 110 and p.get('Hand') == 'R'):
            return {'type': 'East-West', 'mult': 1.05, 'vol': 0.9, 'HB': hb, 'floor_adj': 0.0}

        if si_stuff > 110 and sl_stuff > 115:
            return {'type': 'Unicorn', 'mult': 1.10, 'vol': 1.1, 'floor_adj': 0.0}
        
        return {'type': 'Standard', 'mult': 1.0, 'vol': 1.0, 'floor_adj': 0.0}

    def solve_physics_pk(self, p: Dict, b: Dict, env: Dict) -> float:
        """Calculates core strikeout probability per plate appearance."""
        # V20.1 Fix: Anchor physics to the pitcher's actual K% instead of league average
        base_k = p.get('K_pct', self.MLB_AVG_K_PCT) / 100.0
        
        stuff = p.get('Stuff', 100)
        
        velo_delta = p.get('Velo_Delta', 0.0)
        spin_delta = p.get('Spin_Delta', 0.0)
        if velo_delta > 1.0 or spin_delta > 100:
            stuff += (velo_delta * 5.0) + (spin_delta / 50.0)
            
        if stuff > 110:
            stuff_factor = (stuff / 100.0) ** 1.5 
        elif stuff > 105:
            stuff_factor = (stuff / 100.0) ** 1.0
        else:
            stuff_factor = (stuff / 100.0) ** 0.5
            
        vaa_boost = 1.10 if p.get('VAA', -4.0) > -4.0 else 1.0
        
        swstr = p.get('SwStr%')
        if swstr is None:
            est_swstr = (self.MLB_AVG_K_PCT * 0.48) + ((p.get('Stuff', 100) - 100) * 0.25)
            swstr = max(7.0, est_swstr)
            
        csw = p.get('CSW%')
        if csw is None:
            est_csw = (self.MLB_AVG_K_PCT * 1.1) + ((p.get('Stuff', 100) - 100) * 0.35)
            csw = max(22.0, est_csw)

        whiff_mod = ((swstr / self.MLB_AVG_SWSTR) * 0.7) + ((csw / self.MLB_AVG_CSW) * 0.3)
        
        # Biomechanics: Tunneling SD (Release Point Consistency)
        tunnel_sd = p.get('Tunneling_SD', 1.0)
        if tunnel_sd > 2.5:
            whiff_mod *= 0.92 # TUNNEL_BROKEN_SEVERE
        elif tunnel_sd > 1.5:
            whiff_mod *= 0.96 # TUNNEL_BROKEN

        # Plate Discipline Synergy
        chase_factor = max(0.80, (b.get('O_Swing', 30.0) / 30.0))
        miss_factor = max(0.75, (100.0 - b.get('Z_Contact', 85.0)) / 15.0)
        
        physics_pk = base_k * stuff_factor * vaa_boost * whiff_mod * chase_factor * miss_factor
        
        synergy_mod = self.calculate_synergy_score(p, env.get('Catcher', {}))
        physics_pk *= synergy_mod
        
        # Atmospheric Physics
        weather = env.get('Weather', {})
        temp = weather.get('temp', 72)
        temp_mod = 1.0 + (temp - 72) * 0.0020 # Increased from 0.0012
        
        dew_point = weather.get('dew_point', 50)
        if dew_point < 45 and not weather.get('dome'):
            physics_pk *= 0.97 # GRIP_RISK (Simplified for all pitches)
            
        pressure = weather.get('pressure', 29.92)
        if pressure > 30.1:
            physics_pk *= 1.02 # Break Boost
        elif pressure < 29.5:
            physics_pk *= 0.98 # Reduced Movement
            
        location = env.get('Location', '')
        if location in ['SF', 'SD', 'SEA'] and temp < 65:
             temp_mod *= 1.04 
             
        game_time = env.get('GameTime', 19.0) 
        is_west_coast = location in ['LAD', 'SF', 'SD', 'SEA', 'LAA', 'OAK']
        if is_west_coast and 16.0 <= game_time <= 18.0:
            physics_pk *= 1.08 
            
        ump_zone = env['Umpire'].get('zone_type', 'neutral')
        arch_type = p.get('Archetype', 'Standard')
        
        if arch_type == 'East-West' and ump_zone == 'wide':
             physics_pk *= 1.05
        elif arch_type == 'North-South' and ump_zone == 'tall':
             physics_pk *= 1.05
             
        hb = p.get('HB', 7.5)
        if hb > 15.0 or p.get('Pit+ SI', 100) > 115:
             physics_pk *= 1.04 
            
        ump_mod = env['Umpire'].get('CS_pct', 16.5) / 16.5
        park_mod = env.get('ParkFactor', 1.0)
        
        if env.get('is_1st_inning'):
            physics_pk *= 1.05

        return physics_pk * temp_mod * ump_mod * park_mod

    def hyper_dimensional_monte_carlo(self, p: Dict, lineup: List[Dict], env: Dict, overrides: Dict = None) -> Tuple[int, float, Dict]:
        """V10.1 Monte Carlo Loop."""
        overrides = overrides or {}
        n_sims = 100000
        results = []
        
        p_name = p.get('Name', 'Unknown')
        arch_data = self.ARCHETYPES.get(p_name)
        if not arch_data:
            arch_data = self.detect_archetype(p)
            
        arch_mod = arch_data['mult']
        volatility = arch_data['vol']
        p['Archetype'] = arch_data['type'] 
        
        c_name = env.get('Catcher', {}).get('Name', 'Unknown')
        catcher_mod = self.CATCHER_TIERS.get(c_name, 1.0)

        # ── BATTERS FACED (BF) COMPUTATION (v2) ──
        # Anchor = Mean(Pitch Count last 5 starts) × BF_Multiplier
        bf_mult = overrides.get('BF_Multiplier', 1.0)
        pitch_counts = p.get('Last_5_Pitches', [92]*5)
        mean_pc = sum(pitch_counts) / len(pitch_counts)
        anchor_pc = mean_pc * bf_mult
        
        # Denominator shift for opponent P/PA
        opp_ppa = env.get('Opponent_PPA', 3.9) # League avg
        ppa_adj = 0.0
        if opp_ppa > 4.1: ppa_adj = 0.10 # Top 5 rank
        
        # Manager / Bullpen / Moneyline Scripts
        script_bf_adj = 0.0
        if p.get('ShortLeash'): script_bf_adj -= 1.5
        if env.get('Bullpen_Unavailable'): script_bf_adj += 1.2
        
        ml = env.get('Moneyline', 0)
        if ml > 180: script_bf_adj -= 1.0
        elif ml < -250: script_bf_adj -= 0.8
        
        # Disaster Start Rate (DSR)
        dsr = p.get('DSR', 0.10)
        if dsr >= 0.25: script_bf_adj -= 1.5
        elif dsr >= 0.15: script_bf_adj -= 0.8
        
        # ── K/BF RATE SYNTHESIS (v2) ──
        # Categorical Hitter Shifts
        k_suppressors = sum(1 for b in lineup if b.get('Z_Contact', 85) > 90)
        k_amplifiers = sum(1 for b in lineup if b.get('O_Swing', 30) > 35 and p.get('SwStr', 11) > 14)
        
        lineup_k_mod = 1.0
        if k_suppressors >= 3: lineup_k_mod *= 0.96 # Increased suppression
        if k_amplifiers >= 3: lineup_k_mod *= 1.04 # Added amplification for high O-Swing lineups
        
        # Plan B Check
        has_plan_b = p.get('PlanB', False)
        
        # Dynamic Credibility Weighting (DCW)
        anchor_weight = 0.60 
        if p.get('Stuff', 100) >= 110: anchor_weight = 0.35 # Allow stuff to shine more
        if p.get('BreakoutCandidate', False): anchor_weight = 0.25 # Young arms need less anchoring
        
        anchored_k_base = p.get('K_pct', self.MLB_AVG_K_PCT) / 100.0
        experience_factor = min(1.0, p.get('IP', 100) / 100.0)

        total_bf = 0
        for _ in range(n_sims):
            k_count = 0
            pitch_count = 0
            bf_sim = 0
            times_through = 1
            
            game_form_mod = random.gauss(1.0, 0.22)
            if random.random() < 0.05:
                 game_form_mod *= random.uniform(0.6, 1.5)
            
            # Final Projected BF for this sim
            sim_ppa = random.gauss(p.get('PPA', 3.9) + ppa_adj, 0.3)
            projected_bf = (anchor_pc / sim_ppa) + script_bf_adj
            
            # Hard Ceiling
            career_max_bf = p.get('Career_Max_BF', 27)
            projected_bf = min(projected_bf, career_max_bf * 1.05)
            
            b_idx = 0
            while bf_sim < projected_bf:
                b = lineup[b_idx % 9]
                bf_sim += 1
                if bf_sim % 9 == 1 and bf_sim > 1:
                    times_through += 1
                b_idx += 1
                
                ttt_penalty = 1.0
                if times_through == 2: ttt_penalty = 0.95
                if times_through == 3: 
                    ttt_penalty = 0.92 if experience_factor > 0.5 else (0.85 if experience_factor > 0.3 else 0.75)
                
                # Plan B Missing Penalty
                if times_through >= 2 and not has_plan_b:
                    ttt_penalty *= 0.90 # PLAN_B_MISSING
                
                p_platoon = self.calculate_platoon_mod(p.get('Hand', 'R'), b.get('Hand', 'R'), p_name, p)
                physics_pk = self.solve_physics_pk(p, b, env)
                
                b_k_pct = b.get('K_pct', self.MLB_AVG_K_PCT) / 100.0
                anchored_pk = anchored_k_base * (b_k_pct / (self.MLB_AVG_K_PCT / 100.0))
                
                base_pk = (anchored_pk * anchor_weight) + (physics_pk * (1.0 - anchor_weight))
                current_pk = base_pk * p_platoon * arch_mod * catcher_mod * lineup_k_mod
                
                current_pk *= ttt_penalty
                current_pk *= game_form_mod 
                current_pk *= overrides.get('Hot_Streak', 1.0)
                current_pk *= overrides.get('density_mod', 1.0) 
                
                if p.get('Hand') == 'L':
                    rhb_count = sum(1 for b in lineup if b.get('Hand') == 'R')
                    if rhb_count >= 7:
                        current_pk *= 0.96 
                
                if random.random() < current_pk:
                    k_count += 1
                
            results.append(k_count)
            total_bf += bf_sim
            
        mean_k = sum(results) / n_sims
        dist = {k: results.count(k) / n_sims for k in set(results)}
        exact_k = max(dist, key=dist.get)
        
        return exact_k, dist[exact_k], {
            'mean_k': mean_k,
            'distribution': dist,
            'expected_bf': total_bf / n_sims,
            'Archetype': arch_data['type']
        }

    def calculate_lineup_density_mod(self, lineup: List[Dict]) -> float:
        """V13.3 Lineup Density Cluster Logic (Chapter 4)."""
        bottom_three = lineup[6:9]
        avg_k = sum(b.get('K_pct', 22.7) for b in bottom_three) / 3.0
        
        if avg_k > 28.0:
            return 1.06 
        if avg_k < 18.0:
            return 0.98 
        return 1.0

    def project(self, pitcher_data: Dict, lineup_data: List[Dict], env: Dict, overrides: Dict = None) -> Dict:
        """Unified Projection Interface."""
        density_mod = self.calculate_lineup_density_mod(lineup_data)
        overrides = overrides or {}
        overrides['density_mod'] = density_mod
        
        exact_k, confidence, metrics = self.hyper_dimensional_monte_carlo(pitcher_data, lineup_data, env, overrides)
        
        # ── SENSITIVITY CHECK (v2) ──
        # Re-run at μ - 0.75 and μ + 0.75 to check fragility
        # For efficiency, we can simulate this by shifting the distribution
        def get_prob_at_mu(target_mu, original_metrics, line):
            shift = target_mu - original_metrics['mean_k']
            dist = original_metrics['distribution']
            over_prob = sum(prob for k, prob in dist.items() if (k + shift) > line)
            return over_prob

        probs = {}
        dist = metrics['distribution']
        is_fragile = False
        
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over_prob = sum(prob for k, prob in dist.items() if k > line)
            
            # Sensitivity check for each line
            p_minus = get_prob_at_mu(metrics['mean_k'] - 0.75, metrics, line)
            p_plus = get_prob_at_mu(metrics['mean_k'] + 0.75, metrics, line)
            
            if abs(p_plus - over_prob) > 0.10 or abs(over_prob - p_minus) > 0.10:
                is_fragile = True
                
            probs[line] = {'Over': over_prob, 'Under': 1.0 - over_prob}
            
        # ── DISTRIBUTION (v2) ──
        # Calculate 'r' (dispersion parameter)
        # r = μ² ÷ (variance − μ)
        mean_k = metrics['mean_k']
        variance = sum((k - mean_k)**2 * prob for k, prob in dist.items())
        r = (mean_k**2) / (variance - mean_k) if (variance - mean_k) > 0 else 6.0
        r = max(3.5, min(10.0, r)) # Cap per Step 5.4

        return {
            'exact_k': exact_k,
            'mean_k': mean_k,
            'distribution': dist,
            'confidence': confidence,
            'probabilities': probs,
            'r': r,
            'is_fragile': is_fragile,
            'telemetry': {
                'ExpectedBF': metrics['expected_bf'],
                'Final_pK': (metrics['mean_k'] / metrics['expected_bf']) if metrics['expected_bf'] > 0 else 0,
                'Archetype': metrics['Archetype']
            },
            'status': 'DETERMINED'
        }