import random
import time

TEAM_NAMES = [
    "Lew Kraków",
    "Wisła Płock",
    "Legia Warszawa",
    "Piast Gliwice",
    "Cracovia",
    "Lech Poznań",
    "Zagłębie Lubin",
    "Korona Kielce",
    "Śląsk Wrocław",
    "Pogoń Szczecin",
    "Jagiellonia Białystok",
    "Widzew Łódź"
]


class Team:
    """Klasa reprezentująca drużynę w turnieju"""
    
    def __init__(self, name: str):
        self.name = name
        self.matches = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
    
    @property
    def goal_difference(self) -> int:
        """Zwraca różnicę bramek"""
        return self.goals_for - self.goals_against
    
    def add_match_result(self, goals_for: int, goals_against: int):
        """Dodaje wynik meczu do statystyk drużyny"""
        self.matches += 1
        self.goals_for += goals_for
        self.goals_against += goals_against
        
        if goals_for > goals_against:
            self.wins += 1
            self.points += 3
        elif goals_for < goals_against:
            self.losses += 1
        else:
            self.draws += 1
            self.points += 1
    
    def to_dict(self) -> dict:
        """Zwraca słownik ze statystykami drużyny"""
        return {
            "team": self.name,
            "matches": self.matches,
            "wins": self.wins,
            "draws": self.draws,
            "losses": self.losses,
            "goals_for": self.goals_for,
            "goals_against": self.goals_against,
            "goal_difference": self.goal_difference,
            "points": self.points
        }
    
    def __repr__(self):
        return f"Team('{self.name}')"


class Match:
    """Klasa reprezentująca pojedynczy mecz"""
    
    def __init__(self, team1: Team, team2: Team, score1: int = None, score2: int = None):
        self.team1 = team1
        self.team2 = team2
        self.score1 = score1
        self.score2 = score2
    
    def play(self):
        """Rozgrywa mecz - generuje losowy wynik"""
        self.score1 = self._generate_random_score()
        self.score2 = self._generate_random_score()
        
        # Aktualizacja statystyk drużyn
        self.team1.add_match_result(self.score1, self.score2)
        self.team2.add_match_result(self.score2, self.score1)
        
        return (self.team1.name, self.team2.name, self.score1, self.score2)
    
    @staticmethod
    def _generate_random_score() -> int:
        """Generuje losowy wynik meczu (bramki)"""
        weights = [0.20, 0.25, 0.20, 0.15, 0.10, 0.05, 0.03, 0.02]
        return random.choices(range(8), weights=weights)[0]
    
    def get_result(self) -> tuple:
        """Zwraca wynik meczu jako krotkę"""
        return (self.team1.name, self.team2.name, self.score1, self.score2)
    
    def get_winner(self) -> Team | None:
        """Zwraca zwycięzcę meczu lub None w przypadku remisu"""
        if self.score1 > self.score2:
            return self.team1
        elif self.score2 > self.score1:
            return self.team2
        return None
    
    def is_draw(self) -> bool:
        """Sprawdza czy mecz zakończył się remisiem"""
        return self.score1 == self.score2
    
    def __repr__(self):
        return f"Match({self.team1.name} {self.score1}-{self.score2} {self.team2.name})"


class Tournament:
    """Klasa reprezentująca turniej/ligę"""
    
    def __init__(self, team_names: list):
        self.teams = [Team(name) for name in team_names]
        self.matches: list[Match] = []
        self.is_played = False
    
    @classmethod
    def create_random(cls, num_teams: int = 8) -> "Tournament":
        """Tworzy turniej z losowymi drużynami"""
        selected_names = random.sample(TEAM_NAMES, num_teams)
        return cls(selected_names)
    
    def generate_matches(self):
        """Generuje wszystkie mecze (każdy z każdym)"""
        self.matches = []
        num_teams = len(self.teams)
        
        for i in range(num_teams):
            for j in range(i + 1, num_teams):
                match = Match(self.teams[i], self.teams[j])
                self.matches.append(match)
    
    def play_all(self):
        """Rozgrywa wszystkie mecze turnieju"""
        if not self.matches:
            self.generate_matches()
        
        for match in self.matches:
            match.play()
        
        self.is_played = True
    
    def get_standings(self) -> list:
        """Zwraca posortowaną tabelę wyników"""
        if not self.is_played:
            self.play_all()
        
        table = [team.to_dict() for team in self.teams]
        # Sortowanie: punkty -> różnica bramek -> bramki strzelone
        table.sort(key=lambda x: (x["points"], x["goal_difference"], x["goals_for"]), reverse=True)
        return table
    
    def get_winner(self) -> Team:
        """Zwraca zwycięzcę turnieju"""
        if not self.is_played:
            self.play_all()
        
        standings = self.get_standings()
        winner_name = standings[0]["team"]
        return next(team for team in self.teams if team.name == winner_name)
    
    def get_team_by_name(self, name: str) -> Team | None:
        """Zwraca drużynę po nazwie"""
        for team in self.teams:
            if team.name == name:
                return team
        return None
    
    def print_matches(self):
        """Wyświetla wyniki wszystkich meczów"""
        if not self.matches:
            print("Brak rozegranych meczów.")
            return
        
        print("\n" + "=" * 60)
        print("WYNIKI MECZÓW")
        print("=" * 60)
        
        for i, match in enumerate(self.matches, 1):
            result = match.get_result()
            team1, team2, score1, score2 = result
            print(f"{i:2}. {team1:20s} {score1} - {score2} {team2:>20s}")
    
    def print_standings(self):
        """Wyświetla tabelę wyników"""
        if not self.is_played:
            self.play_all()
        
        table = self.get_standings()
        
        print("\n" + "=" * 70)
        print("TABELA WYNIKÓW TURNIEJU")
        print("=" * 70)
        print(f"{'Lp.':<4} {'Drużyna':<20} {'M':>3} {'Z':>3} {'R':>3} {'P':>3} {'B+/B-':>10} {'RMB':>6} {'Pkt':>4}")
        print("-" * 70)
        
        for i, row in enumerate(table, 1):
            goal_diff = f"{row['goals_for']}/{row['goals_against']}"
            rm_diff = f"{row['goal_difference']:+d}"
            print(f"{i:<4} {row['team']:<20} {row['matches']:>3} {row['wins']:>3} {row['draws']:>3} {row['losses']:>3} {goal_diff:>10} {rm_diff:>6} {row['points']:>4}")
        
        print("=" * 70)
        print("\nLegenda: M - mecze, Z - zwycięstwa, R - remisy, P - porażki")
        print("        B+/B- - bramki strzelone/stracone, RMB - różnica bramek, Pkt - punkty")
    
    def __repr__(self):
        return f"Tournament({len(self.teams)} drużyn, {len(self.matches)} meczów)"


# ========== Funkcje pomocnicze (dla kompatybilności wstecznej) ==========

def generate_teams(num_teams=8):
    """Generuje losowe drużyny z listy dostępnych nazw"""
    all_teams = random.sample(TEAM_NAMES, num_teams)
    return all_teams

def generate_random_score():
    """Generuje losowy wynik meczu (bramki)"""
    weights = [0.20, 0.25, 0.20, 0.15, 0.10, 0.05, 0.03, 0.02]
    goals = random.choices(range(8), weights=weights)[0]
    return goals

def generate_match_result(team1, team2):
    """Generuje losowy wynik meczu między dwiema drużynami"""
    score1 = generate_random_score()
    score2 = generate_random_score()
    return (team1, team2, score1, score2)

def simulate_league(teams):
    """Symuluje ligę - każdy z każdym (każda drużyna gra z każdą)"""
    matches = []
    num_teams = len(teams)
    
    for i in range(num_teams):
        for j in range(i + 1, num_teams):
            team1 = teams[i]
            team2 = teams[j]
            result = generate_match_result(team1, team2)
            matches.append(result)
    
    return matches

def update_standings(standings, match):
    """Aktualizuje tabelę wyników po meczu"""
    team1, team2, score1, score2 = match
    
    # Inicjalizacja drużyn jeśli nie istnieją
    if team1 not in standings:
        standings[team1] = {"matches": 0, "wins": 0, "draws": 0, "losses": 0, "goals_for": 0, "goals_against": 0, "points": 0}
    if team2 not in standings:
        standings[team2] = {"matches": 0, "wins": 0, "draws": 0, "losses": 0, "goals_for": 0, "goals_against": 0, "points": 0}
    
    # Aktualizacja statystyk
    standings[team1]["matches"] += 1
    standings[team2]["matches"] += 1
    
    standings[team1]["goals_for"] += score1
    standings[team1]["goals_against"] += score2
    standings[team2]["goals_for"] += score2
    standings[team2]["goals_against"] += score1
    
    # Wynik meczu
    if score1 > score2:
        standings[team1]["wins"] += 1
        standings[team1]["points"] += 3
        standings[team2]["losses"] += 1
    elif score1 < score2:
        standings[team2]["wins"] += 1
        standings[team2]["points"] += 3
        standings[team1]["losses"] += 1
    else:
        standings[team1]["draws"] += 1
        standings[team2]["draws"] += 1
        standings[team1]["points"] += 1
        standings[team2]["points"] += 1

def get_standings_sorted(standings):
    """Sortuje tabelę wyników: punkty, różnica bramek, bramki strzelone"""
    table = []
    for team, stats in standings.items():
        goal_diff = stats["goals_for"] - stats["goals_against"]
        table.append({
            "team": team,
            "matches": stats["matches"],
            "wins": stats["wins"],
            "draws": stats["draws"],
            "losses": stats["losses"],
            "goals_for": stats["goals_for"],
            "goals_against": stats["goals_against"],
            "goal_difference": goal_diff,
            "points": stats["points"]
        })
    
    # Sortowanie: punkty -> różnica bramek -> bramki strzelone
    table.sort(key=lambda x: (x["points"], x["goal_difference"], x["goals_for"]), reverse=True)
    return table

def print_matches(matches):
    """Wyświetla wyniki wszystkich meczów"""
    print("\n" + "=" * 60)
    print("WYNIKI MECZÓW")
    print("=" * 60)
    
    for i, match in enumerate(matches, 1):
        team1, team2, score1, score2 = match
        print(f"{i:2}. {team1:20s} {score1} - {score2} {team2:>20s}")

def print_standings(table):
    """Wyświetla tabelę wyników"""
    print("\n" + "=" * 70)
    print("TABELA WYNIKÓW TURNIEJU")
    print("=" * 70)
    print(f"{'Lp.':<4} {'Drużyna':<20} {'M':>3} {'Z':>3} {'R':>3} {'P':>3} {'B+/B-':>10} {'RMB':>6} {'Pkt':>4}")
    print("-" * 70)
    
    for i, row in enumerate(table, 1):
        goal_diff = f"{row['goals_for']}/{row['goals_against']}"
        rm_diff = f"{row['goal_difference']:+d}"
        print(f"{i:<4} {row['team']:<20} {row['matches']:>3} {row['wins']:>3} {row['draws']:>3} {row['losses']:>3} {goal_diff:>10} {rm_diff:>6} {row['points']:>4}")
    
    print("=" * 70)
    print("\nLegenda: M - mecze, Z - zwycięstwa, R - remisy, P - porażki")
    print("        B+/B- - bramki strzelone/stracone, RMB - różnica bramek, Pkt - punkty")

def main():
    print("\n" + "#" * 60)
    print("#" + " " * 18 + "TURNIEJ PIŁKI NOŻNEJ" + " " * 18 + "#")
    print("#" * 60)
    
    # Generowanie losowych drużyn
    num_teams = 8
    teams = generate_teams(num_teams)
    
    print(f"\nUczestniczące drużyny ({num_teams}):")
    for i, team in enumerate(teams, 1):
        print(f"  {i}. {team}")
    
    # Symulacja ligi
    matches = simulate_league(teams)
    
    # Obliczanie wyników
    standings = {}
    for match in matches:
        update_standings(standings, match)
    
    # Wyświetlanie wyników
    print_matches(matches)
    
    # Sortowanie i wyświetlanie tabeli
    table = get_standings_sorted(standings)
    print_standings(table)
    
    # Ogłoszenie zwycięzcy
    print(f"\n🏆 ZWYCIĘZCA TURNIEJU: {table[0]['team']} 🏆")
    print(f"   Zdobyte punkty: {table[0]['points']}")
    print(f"   Bilans bramkowy: {table[0]['goals_for']}-{table[0]['goals_against']} ({table[0]['goal_difference']:+d})")

if __name__ == "__main__":
    main()
