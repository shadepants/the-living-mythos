# Q9b bracket options. Rates per season. Targets: P(child reaches young adult) = 0.57 (l15, Gurven & Kaplan 2007);
# completed fertility ~5.7 (their forager average, range 4.5-6 in the log); adult mortality ~1%/yr to 40,
# Gompertz rise after (shape from G&K; per-bracket values are my averages, not from the paper).
A_CHILD = 0.43/0.57/60                         # exponential exit at 1/60: a/(a+m) = 0.57
s = 0.57**(1/3); B_CHILD = (3/60)*(1-s)/s       # 3 Erlang stages, each survived with prob s
MODES = {
    # name: (spans in seasons for children/young adults/adults, stages, mortality x4, birth, fertile brackets)
    'R': ((60, 40, 100), (1, 1, 1), [0.0093, 0.003, 0.004, 0.02], 0.045, [1, 2]),     # rev 30 prototype values
    'A': ((60, 40, 100), (1, 1, 1), [A_CHILD, 0.0025, 0.003, 0.0156], 5.7/140, [1, 2]),  # draft cuts 0-14/15-24/25-49/50+
    'B': ((60, 40, 100), (3, 3, 3), [B_CHILD, 0.0025, 0.003, 0.0156], 5.7/140, [1, 2]),  # same cuts, 3 hidden stages each
    'C': ((60, 20, 100), (1, 1, 1), [A_CHILD, 0.0025, 0.0028, 0.0125], 5.7/120, [1, 2]),  # role cuts 0-14/15-19/20-44/45+
    'D': ((60, 20, 100), (1, 1, 1), [A_CHILD, 0.0025, 0.0028, 0.0125], 5.7/100, [2]),     # role cuts, only adults (20-44) fertile
}
