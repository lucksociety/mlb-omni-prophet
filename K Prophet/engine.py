#!/usr/bin/env python3
import math
import random
from typing import Dict, List, Tuple

class KProphetEngine:
    """
    K PROPHET V11.0 — THE DETERMINISTIC SINGULARITY
    Deterministic Reality Engine (DRE) - Ultimate Precision State.
    ===================================================================
    Integrating Command-Adjusted Efficiency, Shelling Early-Exits,
    Dynamic TTT Penalties, and Platoon Concentration Weighting.
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
            'Ryne Nelson': {'type': 'North-South', 'mult': 1.15, 'vol': 1.2, 'IVB': 18.9, 'floor_adj': 1.5},
            'Dylan Cease': {'type': 'Unicorn', 'mult': 1.18, 'vol': 1.1, 'HB': 15.5, 'floor_adj': 0.5},
            'Andrew Painter': {'type': 'North-South', 'mult': 1.12, 'vol': 1.1, 'IVB': 17.5, 'floor_adj': 1.2},
            'Carlos Lagrange': {'type': 'North-South', 'mult': 1.25, 'vol': 1.3, 'IVB': 18.5, 'floor_adj': 1.5},
            'Framber Valdez': {'type': 'Unicorn', 'mult': 1.12, 'vol': 1.1, 'floor_adj': 0.5}, 
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
            if arch == 'East-West': return 1.15 # Upgraded from 1.12
            if arch == 'Unicorn': return 1.10
            return 1.08
        else:
            if arch == 'East-West': return 0.88
            if arch == 'Unicorn': return 1.05 # Unicorns gain vs opposite
            return 0.95

    def detect_archetype(self, p: Dict) -> Dict:
        """Dynamically detect pitcher archetype from Statcast/Movement metrics."""
        # V12.5: PHYSICS-BASED DETECTION (Bible Chapter 1 & 3)
        ivb = p.get('IVB', 16.0)
        hb = p.get('HB', 7.5)
        fa_stuff = p.get('Pit+ FA', 100)
        si_stuff = p.get('Pit+ SI', 100)
        sl_stuff = p.get('Pit+ SL', 100)
        vaa = p.get('VAA', -4.5)
        
        # North-South: High IVB or Flat VAA
        if ivb > 18.0 or vaa > -4.1 or fa_stuff > 115:
            # Bible: "If a pitcher has elite IVB, his K-Floor rises by 1.5"
            return {'type': 'North-South', 'mult': 1.15, 'vol': 1.2, 'IVB': ivb, 'floor_adj': 1.5}
            
        # East-West: High Horizontal Movement (Sweepers)
        if hb > 14.0 or (si_stuff > 110 and p.get('Hand') == 'R'):
            return {'type': 'East-West', 'mult': 1.05, 'vol': 0.9, 'HB': hb, 'floor_adj': 0.0}

        # Unicorn: Hybrid/Splinker/High-Movement Sliders
        if si_stuff > 110 and sl_stuff > 115:
            return {'type': 'Unicorn', 'mult': 1.10, 'vol': 1.1, 'floor_adj': 0.5}
        
        return {'type': 'Standard', 'mult': 1.0, 'vol': 1.0, 'floor_adj': 0.0}

    def solve_physics_pk(self, p: Dict, b: Dict, env: Dict) -> float:
        """Calculates core strikeout probability per plate appearance."""
        # V12.5: DECOUPLED PHYSICS + WHIFF SYNERGY
        # Use League Average K% as the base for physics
        base_k = (self.MLB_AVG_K_PCT / 100.0) 
        
        # Stuff+ Scaling
        stuff = p.get('Stuff', 100)
        
        # V12.6: Recent Form (14-day Velo/Spin Delta)
        # Bible: "Stuff+ Gainers: Who has increased spin or velocity in the last 14 days?"
        velo_delta = p.get('Velo_Delta', 0.0)
        spin_delta = p.get('Spin_Delta', 0.0)
        if velo_delta > 1.0 or spin_delta > 100:
            stuff += (velo_delta * 5.0) + (spin_delta / 50.0)
            
        if stuff > 120:
            stuff_factor = (stuff / 100.0) ** 1.5 
        else:
            stuff_factor = (stuff / 100.0) ** 0.5
            
        vaa_boost = 1.10 if p.get('VAA', -4.0) > -4.0 else 1.0
        
        # V12.0: Pitcher Whiff Context — Dynamic Fallbacks
        swstr = p.get('SwStr%')
        if swstr is None:
            est_swstr = (p.get('K_pct', self.MLB_AVG_K_PCT) * 0.48) + ((p.get('Stuff', 100) - 100) * 0.15)
            swstr = max(7.0, est_swstr)
            
        csw = p.get('CSW%')
        if csw is None:
            est_csw = (p.get('K_pct', self.MLB_AVG_K_PCT) * 1.1) + ((p.get('Stuff', 100) - 100) * 0.2)
            csw = max(22.0, est_csw)

        whiff_mod = ((swstr / self.MLB_AVG_SWSTR) * 0.7) + ((csw / self.MLB_AVG_CSW) * 0.3)
        
        # Plate Discipline Synergy
        chase_factor = (b.get('O_Swing', 30.0) / 30.0)
        miss_factor = (100.0 - b.get('Z_Contact', 85.0)) / 15.0
        
        # Physics Blend
        physics_pk = base_k * stuff_factor * vaa_boost * whiff_mod * chase_factor * miss_factor
        
        # Environment (Chapter 8)
        temp = env['Weather'].get('temp', 72)
        temp_mod = 1.0 + (temp - 72) * 0.0012 
        
        # V12.7: Marine Layer (Coastal Boost)
        # Bible: "Dense, cool evening air maximizes Magnus Force. Over becomes more probable."
        location = env.get('Location', '')
        if location in ['SF', 'SD', 'SEA'] and temp < 65:
             temp_mod *= 1.04 # Extra density boost for spin
             
        # V12.8: Shadow Play (Shadow Transition)
        # Bible: "Late afternoon games in the West Coast are a goldmine for the Over."
        game_time = env.get('GameTime', 19.0) # Decimal hours
        is_west_coast = location in ['LAD', 'SF', 'SD', 'SEA', 'LAA', 'OAK']
        if is_west_coast and 16.0 <= game_time <= 18.0:
            physics_pk *= 1.08 # Shadow blindness modifier
            
        # V13.0: Umpire-Pitcher Synergy (Chapter 7)
        # Bible: "East-West pitchers thrive with wide-zone umpires. North-South with high zones."
        ump_zone = env['Umpire'].get('zone_type', 'neutral')
        arch_type = p.get('Archetype', 'Standard')
        
        if arch_type == 'East-West' and ump_zone == 'wide':
             physics_pk *= 1.05
        elif arch_type == 'North-South' and ump_zone == 'tall':
             physics_pk *= 1.05
             
        # V13.1: Seam-Shifted Wake (SSW) Coefficient (Layer 7)
        # Bible: "Late movement that defies spin-axis logic."
        hb = p.get('HB', 7.5)
        if hb > 15.0 or p.get('Pit+ SI', 100) > 115:
             physics_pk *= 1.04 
            
        ump_mod = env['Umpire'].get('CS_pct', 16.5) / 16.5
        park_mod = env.get('ParkFactor', 1.0)
        
        return physics_pk * temp_mod * ump_mod * park_mod

    def hyper_dimensional_monte_carlo(self, p: Dict, lineup: List[Dict], env: Dict, overrides: Dict = None) -> Tuple[int, float, Dict]:
        """V10.1 Monte Carlo Loop."""
        overrides = overrides or {}
        n_sims = 10000
        results = []
        
        p_name = p.get('Name', 'Unknown')
        arch_data = self.ARCHETYPES.get(p_name)
        if not arch_data:
            arch_data = self.detect_archetype(p)
            
        arch_mod = arch_data['mult']
        volatility = arch_data['vol']
        p['Archetype'] = arch_data['type'] # Inject for synergy check
        
        c_name = env.get('Catcher', {}).get('Name', 'Unknown')
        catcher_mod = self.CATCHER_TIERS.get(c_name, 1.0)

        # Dynamic Credibility Weighting (DCW)
        # V11.1: STABILIZATION LOGIC (Month-by-Month Framework)
        # The baseline K% is now pre-blended across 2026/2025/Career based on the current month.
        # We only need to shift weight away from the anchor if there is a massive Stuff breakout.
        anchor_weight = 0.65 # Default stabilization weight (increased since baseline is now fully stable)
        
        if p.get('Stuff', 100) > 112: 
            anchor_weight = 0.45
        elif p.get('Stuff', 100) > 120: 
            anchor_weight = 0.30
        
        # Hot Streak Detection Override
        if overrides.get('Hot_Streak', 1.0) > 1.0:
            anchor_weight -= 0.15 # Trust physics/recent form more
        
        anchor_weight = max(0.20, min(0.80, anchor_weight))

        anchored_k_base = p.get('K_pct', self.MLB_AVG_K_PCT) / 100.0

        total_bf = 0
        for _ in range(n_sims):
            k_count = 0
            pitch_count = 0
            bf_sim = 0
            times_through = 1
            # V12.9: The Shadow Hook (Bullpen Correlation)
            # Bible: "Mediocre pitcher forced to throw 105 pitches because there is no one left in the pen."
            max_pitches = overrides.get('PitchLimit', 92)
            bp_burn = env.get('Bullpen_Burn', 0.0) # 0.0 to 1.0 scale
            
            # V13.2: Manager Desperation Logic (Layer 7)
            # If Bullpen is fried AND Starter has Elite Ride, extend leash significantly.
            if bp_burn > 0.8 and arch_data['type'] == 'North-South':
                max_pitches += 12
            elif bp_burn > 0.7:
                max_pitches += 6
            
            if p.get('ShortLeash'): max_pitches -= 15
            
            # V11.0: Command-Adjusted Efficiency
            # High BB% increases Pitches/PA dramatically for young arms.
            bb_pct = p.get('BB_pct', 8.5)
            experience_factor = min(1.0, p.get('IP', 100) / 100.0)
            efficiency_mod = 1.0 + (bb_pct - 8.5) * (0.025 if experience_factor < 0.5 else 0.015)
            
            # V11.0: Shelling Risk (Early Exit Probability)
            # High xERA or bad matchup can end simulation early.
            xera = p.get('xERA', 4.0)
            base_shell_risk = (xera * 0.006)
            if experience_factor < 0.4: base_shell_risk *= 1.25 # Rookies get pulled faster
            
            b_idx = 0
            while pitch_count < max_pitches:
                # Early Exit Check (Shelling)
                # Roll for exit based on xERA and current BF
                # V12.0: Reduced hazard rate to check per "segment" (3 batters) instead of every batter
                if bf_sim > 10 and bf_sim % 3 == 0: 
                    shell_roll = random.random()
                    if shell_roll < base_shell_risk * 1.5: # Slightly higher per-check but fewer checks
                        break
                b = lineup[b_idx % 9]
                bf_sim += 1
                if bf_sim % 9 == 1 and bf_sim > 1:
                    times_through += 1
                b_idx += 1
                
                # V11.0: Dynamic TTT Penalty
                # Young pitchers (low IP) take a harder hit 3rd time through.
                ttt_penalty = 1.0
                experience_factor = min(1.0, p.get('IP', 100) / 100.0)
                if times_through == 2: ttt_penalty = 0.95
                if times_through == 3: 
                    ttt_penalty = 0.82 if experience_factor > 0.5 else 0.72
                
                # Platoon and Physics
                p_platoon = self.calculate_platoon_mod(p.get('Hand', 'R'), b.get('Hand', 'R'), p_name, p)
                physics_pk = self.solve_physics_pk(p, b, env)
                
                # Anchor Adjustment for specific batter
                b_k_pct = b.get('K_pct', self.MLB_AVG_K_PCT) / 100.0
                anchored_pk = anchored_k_base * (b_k_pct / (self.MLB_AVG_K_PCT / 100.0))
                
                # V12.0: Global Multiplier Logic (Bible Fix)
                # Blend the base probabilities first, then apply external multipliers (Catcher, Platoon, Archetype)
                # This ensures modifiers aren't muted by the anchor_weight.
                base_pk = (anchored_pk * anchor_weight) + (physics_pk * (1.0 - anchor_weight))
                current_pk = base_pk * p_platoon * arch_mod * catcher_mod
                
                # Momentum, TTT, and Density
                current_pk *= ttt_penalty
                current_pk *= overrides.get('Hot_Streak', 1.0)
                current_pk *= overrides.get('density_mod', 1.0) # V13.3
                
                # V11.0: Platoon Concentration Penalty
                # LHP facing Righty-Heavy lineups (7+ RHB)
                if p.get('Hand') == 'L':
                    rhb_count = sum(1 for b in lineup if b.get('Hand') == 'R')
                    if rhb_count >= 7:
                        current_pk *= 0.96 # Extra suppression
                
                roll = random.random()
                if roll < current_pk:
                    k_count += 1
                
                # V12.0: Plate Discipline Tax (Ptax)
                # High BB% and Low O_Swing increase pitches/PA for the pitcher.
                b_bb_pct = b.get('BB_pct', 8.5)
                b_oswing = b.get('O_Swing', 30.0)
                b_pitches_mod = 1.0 + (b_bb_pct - 8.5) * 0.02 + (30.0 - b_oswing) * 0.01
                pa_pitches = random.gauss(3.9 * efficiency_mod * b_pitches_mod, 1.1 * volatility)
                pitch_count += max(1, pa_pitches)
                
            results.append(k_count)
            total_bf += bf_sim
            
        mean_k = sum(results) / n_sims
        
        # Apply Bible Floor Adjustment (Chapter 1)
        mean_k += arch_data.get('floor_adj', 0.0)
        
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
        # Bible: "If the 7-8-9 hitters are a 'Strikeout Cluster' (>28% K-rate), the starter thrives."
        bottom_three = lineup[6:9]
        avg_k = sum(b.get('K_pct', 22.7) for b in bottom_three) / 3.0
        
        if avg_k > 28.0:
            return 1.06 # "Cluster Boost"
        if avg_k < 18.0:
            return 0.94 # "Grinder Cluster"
        return 1.0

    def project(self, pitcher_data: Dict, lineup_data: List[Dict], env: Dict, overrides: Dict = None) -> Dict:
        """Unified Projection Interface."""
        # Inject lineup density mod into overrides for the sim
        density_mod = self.calculate_lineup_density_mod(lineup_data)
        overrides = overrides or {}
        overrides['density_mod'] = density_mod
        
        exact_k, confidence, metrics = self.hyper_dimensional_monte_carlo(pitcher_data, lineup_data, env, overrides)
        
        probs = {}
        dist = metrics['distribution']
        for line in [3.5, 4.5, 5.5, 6.5, 7.5]:
            over_prob = sum(prob for k, prob in dist.items() if k > line)
            probs[line] = {'Over': over_prob, 'Under': 1.0 - over_prob}
            
        return {
            'exact_k': exact_k,
            'mean_k': metrics['mean_k'],
            'confidence': confidence,
            'probabilities': probs,
            'telemetry': {
                'ExpectedBF': metrics['expected_bf'],
                'Final_pK': (metrics['mean_k'] / metrics['expected_bf']) if metrics['expected_bf'] > 0 else 0,
                'Archetype': metrics['Archetype']
            },
            'status': 'DETERMINED'
        }
