# Historical teaching fixture from class/lecture02.qmd; reference: 2019-09-30.
import pandas as pd

players = ["Novak Djokovic", "Rafael Nadal", "Roger Federer",
           "Daniil Medvedev", "Dominic Thiem"]
tennis = pd.DataFrame({
    "date_of_birth": ["1987-05-22", "1986-06-03", "1981-08-08",
                      "1996-02-11", "1993-09-03"],
    "grand_slam_win": [16, 19, 20, 0, 0]
}, index=players)
