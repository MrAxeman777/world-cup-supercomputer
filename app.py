import streamlit as st
import random
import numpy as np


teams = {

    "Argentina":{
        "rating":2050,
        "attack":94,
        "defense":92
    },

    "France":{
        "rating":2035,
        "attack":95,
        "defense":91
    },

    "Spain":{
        "rating":2020,
        "attack":91,
        "defense":93
    },

    "England":{
        "rating":2000,
        "attack":92,
        "defense":91
    },

    "Norway":{
        "rating":1875,
        "attack":87,
        "defense":85
    },

    "Morocco":{
        "rating":1885,
        "attack":83,
        "defense":90
    },

    "Switzerland":{
        "rating":1875,
        "attack":84,
        "defense":87
    },

    "Belgium":{
        "rating":1855,
        "attack":86,
        "defense":84
    }

}


players = {

"Argentina":{
    "Messi":0.24,
    "Julian Alvarez":0.30,
    "Lautaro Martinez":0.28,
    "Mac Allister":0.08,
    "Enzo Fernandez":0.06,
    "Others":0.04
},

"France":{
    "Mbappe":0.36,
    "Dembele":0.20,
    "Olise":0.16,
    "Kolo Muani":0.13,
    "Camavinga":0.08,
    "Others":0.07
},

"Spain":{
    "Lamine Yamal":0.30,
    "Nico Williams":0.19,
    "Pedri":0.16,
    "Olmo":0.12,
    "Ferran Torres":0.15,
    "Others":0.08
},

"England":{
    "Harry Kane":0.34,
    "Bellingham":0.19,
    "Saka":0.18,
    "Palmer":0.15,
    "Foden":0.08,
    "Others":0.06
},

"Norway":{
    "Haaland":0.58,
    "Odegaard":0.18,
    "Sorloth":0.16,
    "Others":0.08
},

"Morocco":{
    "En-Nesyri":0.40,
    "Hakimi":0.20,
    "Others":0.40
},

"Switzerland":{
    "Embolo":0.38,
    "Amdouni":0.22,
    "Others":0.40
},

"Belgium":{
    "Lukaku":0.35,
    "Doku":0.25,
    "De Bruyne":0.22,
    "Others":0.18
}

}


assists = {

"Argentina":{
    "Messi":0.30,
    "Enzo Fernandez":0.18,
    "Mac Allister":0.17,
    "Molina":0.12,
    "Others":0.23
},

"France":{
    "Dembele":0.25,
    "Olise":0.23,
    "Mbappe":0.18,
    "Camavinga":0.10,
    "Others":0.24
},

"Spain":{
    "Pedri":0.25,
    "Lamine Yamal":0.22,
    "Olmo":0.16,
    "Nico Williams":0.15,
    "Others":0.22
},

"England":{
    "Saka":0.24,
    "Palmer":0.20,
    "Bellingham":0.18,
    "Foden":0.16,
    "Rice":0.08,
    "Others":0.14
},

"Norway":{
    "Odegaard":0.42,
    "Haaland":0.15,
    "Others":0.43
},

"Morocco":{
    "Hakimi":0.35,
    "Others":0.65
},

"Switzerland":{
    "Amdouni":0.22,
    "Others":0.78
},

"Belgium":{
    "De Bruyne":0.35,
    "Doku":0.22,
    "Others":0.43
}


}


def pick_scorer(team):

    return random.choices(
        list(players[team].keys()),
        weights=list(players[team].values())
    )[0]


def pick_assist(team):

    return random.choices(
        list(assists[team].keys()),
        weights=list(assists[team].values())
    )[0]


def expected_goals(team1,team2):

    attack1 = teams[team1]["attack"]
    attack2 = teams[team2]["attack"]

    defense1 = teams[team1]["defense"]
    defense2 = teams[team2]["defense"]

    xg1 = 1.35 + ((attack1-defense2)/25)
    xg2 = 1.35 + ((attack2-defense1)/25)

    xg1 = max(0.2,min(3.5,xg1))
    xg2 = max(0.2,min(3.5,xg2))

    return round(xg1,2),round(xg2,2)
def goal_times(goals):

    if goals == 0:
        return []

    return sorted(
        random.sample(range(1,91), goals)
    )



def generate_stats(team1,team2,xg1,xg2):

    difference = (
        teams[team1]["rating"]
        -
        teams[team2]["rating"]
    )

    possession1 = round(
        50 + difference/12 + random.randint(-4,4)
    )

    possession1 = max(35,min(65,possession1))

    possession2 = 100-possession1


    shots1 = max(5,int(np.random.normal(xg1*7,2)))
    shots2 = max(5,int(np.random.normal(xg2*7,2)))


    sot1 = max(
        1,
        min(shots1,int(shots1*random.uniform(.3,.5)))
    )

    sot2 = max(
        1,
        min(shots2,int(shots2*random.uniform(.3,.5)))
    )


    return {
        "possession":(possession1,possession2),
        "shots":(shots1,shots2),
        "shots_on_target":(sot1,sot2)
    }




def penalties(team1,team2):

    winner = random.choices(
        [team1,team2],
        weights=[
            teams[team1]["rating"],
            teams[team2]["rating"]
        ]
    )[0]


    loser = team2 if winner == team1 else team1


    winner_score = random.randint(4,5)
    loser_score = random.randint(2,3)


    st.write(
        f"🥅 Penalty Shootout: {winner} {winner_score}-{loser_score} {loser}"
    )


    return winner




def simulate_match(team1,team2):

    xg1,xg2 = expected_goals(team1,team2)


    goals1 = np.random.poisson(xg1)
    goals2 = np.random.poisson(xg2)


    events=[]


    for minute in goal_times(goals1):

        scorer = pick_scorer(team1)
        assist = pick_assist(team1)

        events.append(
            f"{minute}' {team1}: {scorer} ({assist})"
        )


    for minute in goal_times(goals2):

        scorer = pick_scorer(team2)
        assist = pick_assist(team2)

        events.append(
            f"{minute}' {team2}: {scorer} ({assist})"
        )


    st.write("------------------------")
    st.write(f"### {team1} {goals1}-{goals2} {team2}")


    for event in sorted(events):
        st.write(event)


    stats = generate_stats(team1,team2,xg1,xg2)

    st.write("Possession:",stats["possession"])
    st.write("Shots:",stats["shots"])
    st.write("Shots on Target:",stats["shots_on_target"])
    st.write("xG:",xg1,"-",xg2)



    if goals1 == goals2:

        st.write("⏱ Extra Time!")

        et1=np.random.poisson(xg1*0.3)
        et2=np.random.poisson(xg2*0.3)

        goals1 += et1
        goals2 += et2



    if goals1 == goals2:

        return penalties(team1,team2)


    if goals1 > goals2:
        return team1

    return team2




def get_loser(team1,team2,winner):

    if winner == team1:
        return team2

    return team1




def simulate_world_cup():

    st.header("🏆 Quarterfinals")

    qf1 = simulate_match("Argentina","Switzerland")
    qf2 = simulate_match("Spain","Belgium")
    qf3 = simulate_match("France","Morocco")
    qf4 = simulate_match("Norway","England")



    st.header("🔥 Semifinals")

    sf1 = simulate_match(qf1,qf2)
    sf2 = simulate_match(qf3,qf4)



    sf1_loser = get_loser(qf1,qf2,sf1)
    sf2_loser = get_loser(qf3,qf4,sf2)



    st.header("🥉 Third Place Match")

    third = simulate_match(sf1_loser,sf2_loser)



    st.header("🏆 Final")

    champion = simulate_match(sf1,sf2)

    runner_up = get_loser(sf1,sf2,champion)



    st.header("🌎 Tournament Results")

    st.success(
        f"🥇 Champion: {champion}"
    )

    st.write(
        f"🥈 Runner-up: {runner_up}"
    )

    st.write(
        f"🥉 Third Place: {third}"
    )




# =========================
# WEBSITE
# =========================


st.title("🌎 World Cup Supercomputer")

st.write(
    "AI-style World Cup predictor using ratings, xG, goals, scorers, and assists."
)


if st.button("⚽ Simulate World Cup"):

    simulate_world_cup()
