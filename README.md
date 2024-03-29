# Premier League Data Scraper and Formatter

## Data Point Meaning:

1. **full_name** -> the forename and surname of the footballer
2. **club** -> the current club the footballer plays for
3. **nation** -> the nation the footballer plays for
4. **position** -> the position the player plays in
5. **age** -> the age of the footballer
6. **games** -> the number of games played in (start and sub)
7. **games_starts** -> the number of games started in
8. **minutes** -> total number of minutes played
9. **goals** -> number of goals scored
10. **assists** -> number of assists (direct pass to goalscorer)
11. **pens_made** -> number of penalty kicks scored
12. **pens_att** -> number of penalty kicks attempted
13. **cards_yellow** -> number of yellow cards received
14. **cards_red** -> number of red cards received
15. **progressive_carries** -> carries that move the ball towards the opponent's goal line at least 10 yards
16. **progressive_passes** -> completed passes that move the ball towards the opponent's goal line at least 10 yards
17. **progressive_passes_received** -> completed passes received that move the ball towards the opponent's goal line at least 10 yards
18. **shots** -> total number of shots (excluding penalties)
19. **shots_on_target** -> total number of shot on target (excluding penalties)
20. **shots_free_kicks** -> total number of shots coming from free kicks
21. **passes_completed** -> the total number of passes completed
22. **passes** -> the total number of passes attempted
23. **passes_total_distance** -> the total pass distance in yards completed in any direction
24. **passes_progressive_distance** -> the total pass distance in yards completed that traveled towards the opponent's goal line
25. **passes_completed_short** -> the total number of passes completed that traveled between 5 and 15 yards
26. **passes_short** -> the total number of passes attempted that traveled between 5 and 15 yards
27. **passes_completed_medium** -> the total number of passes completed that traveled between 15 and 30 yards
28. **passes_medium** -> the total number of passes attempted that traveled between 15 and 30 yards
29. **passes_completed_long** -> the total number of passes completed that traveled over 30 yards
30. **passes_long** -> the total number of passes attempted that traveled over 30 yards
31. **assisted_shots** -> the total of passes that lead directly to a shot by the receiving player
32. **passes_into_final_third** -> the total number of passes that enter the final third of the pitch (excluding set pieces)
33. **passes_into_penalty_area** -> the total number of passes that enter the opponent's 18 yard box (excluding set pieces)
34. **crosses_into_penalty_area** -> the total number of crosses that enter the opponent's 18 yard box (excluding set pieces)
35. **passes_live** -> live-ball passes (where the game is in play)
36. **passes_dead** -> dead-ball passes (where the game is not in play)
37. **passes_free_kicks** -> passes from free-kicks
38. **through_balls** -> completed passes sent between back defenders into open space
39. **passes_switches** -> passes that travel more than 40 yards across the width of the pitch
40. **crosses** -> crosses from either flank of the 18 yard box
41. **throw_ins** -> throw ins taken to restart play
42. **corner_kicks** -> corner kicks taken
43. **corner_kicks_in** -> corner kicks taken that swing in towards the opponent's goal
44. **corner_kicks_out** -> corner kicks taken that swing out towards the player's own goal
45. **corner_kicks_straight** -> corner kicks taken that went straight
46. **passes_offside** -> passes to a player in an offside position
47. **passes_blocked** -> passes that are blocked by the opponent
48. **tackles** -> number of players tackled
49. **tackles_won** -> number of players tackled that resulted in the players team winning position
50. **tackles_def_3rd** -> number of players tackled in the players defensive 3rd of the pitch
51. **tackles_mid_3rd** -> number of players tackled in the middle 3rd of the pitch
52. **tackles_att_3rd** -> number of players tackled in the opponents defensive 3rd of the pitch
53. **challenge_tackles** -> number of dribblers tackled
54. **challenges** -> number of tackles attempted on dribblers (failed and successful)
55. **challenges_lost** -> number of tackles attempted on dribblers that failed
56. **blocks** -> number of times blocking the ball by standing in its path
57. **blocked_shots** -> number of times blocking a shot by standing in its path
58. **blocked_passes** -> number of times blocking a pass by standing in its path
59. **interceptions** -> number of times intercepting the opponents pass
60. **clearances** -> number of time clearing the ball from the defensive 3rd
61. **errors** -> number of errors leading to an opponent shot
62. **touches** -> number of times the player touched the ball (receiving a pass, then dribbling and sending a pass counts as 1 touch)
63. **touches_def_pen_area** -> number of touches in the defensive penalty area
64. **touches_def_3rd** -> number of touches in the defensive 3rd of the pitch
65. **touches_mid_3rd** -> number of touches in the middle 3rd of the pitch
66. **touches_att_3rd** -> number of touches in the opponents defensive 3rd of the pitch
67. **touches_att_pen_area** -> number of touches in the opponents penalty area
68. **touches_live_ball** -> number of touches during live play
69. **take_ons** -> number of attempts to take on a defender while dribbling
70. **take_ons_won** -> number of attempts to take on a defender that end successfully
71. **take_ons_tackled** -> number of attempts to take on a defender that end unsuccessfully
72. **carries** -> number of times the player carried the ball with their feet in any direction
73. **carries_distance** -> total distance carrying the ball
74. **carries_progressive_distance** -> total distance carrying the ball towards the opponents goal
75. **carries_into_final_third** -> number of times the player carries the ball into the final third
76. **carries_into_penalty_area** -> number of times the player carries the ball into the penalty area
77. **miscontrols** -> number of times the player miscontrols the ball
78. **dispossessed** -> number of times the player lost possession of the ball
79. **passes_received** -> number of passes received by the player
80. **games_subs** -> number of times the player entered the game as a substitute
81. **unused_subs** -> number of times the player was not used as a substitute
82. **on_goals_for** -> number of goals scored by the team while the player is on the pitch
83. **on_goals_against** -> number of goals conceded by the team while the player is on the pitch
84. **fouls** -> number of fouls committed by the player
85. **fouled** -> number of fouls received by the player
86. **offsides** -> number of offside offenses committed by the player
87. **pens_won** -> penalty kicks won for a foul on the player
88. **pens_conceded** -> penalty kicks conceded for committing a foul by the player
89. **own_goals** -> number of times the player has scored a goal against their own team
90. **ball_recoveries** -> number of times the player recovered a loose ball
91. **aerials_won** -> number of headers won by the player against an opponent
92. **aerials_lost** -> number of headers lost by the player against an opponent

## Goalkeeper Specific Statistics:

1. **gk_shots_on_target_against** -> number of shots from the opponent that were on target
2. **gk_saves** -> number of times the player saved a shot from being scored
3. **gk_clean_sheets** -> number of times the player finished a match without conceding a goal
4. **gk_pens_att** -> number of penalty kicks attempted by the opponent
5. **gk_pens_allowed** -> number of penalty kicks against that were scored
6. **gk_pens_saved** -> number of penalty kicks against that were saved by the player
7. **gk_pens_missed** -> number of penalty kicks against that went off target
8. **gk_free_kick_goals_against** -> number of goals against that came direct from a free kick
9. **gk_corner_kick_goals_against** -> number of goals against that came from a corner kick
10. **gk_own_goals_against** -> number of goals against that were scored by the players own team
11. **gk_passes_completed_launched** -> number of passes over 40 yards completed
12. **gk_passes_launched** -> number of passes over 40 yards attempted
13. **gk_passes** -> number of passes attempted (excluding goal kicks)
14. **gk_passes_throws** -> number of passes from hand attempted
15. **gk_passes_length_avg** -> average length of the players passes
16. **gk_goal_kicks** -> number of goal kicks taken to restart play
17. **gk_goal_kicks_length_avg** -> average length of the players goal kicks
18. **gk_crosses** -> the number of times an opponent has crossed the ball in the players 18 yard box
19. **gk_crosses_stopped** -> the number of times the player stopped the crossed ball from an opponent into the 18 yard box
20. **gk_def_actions_outside_pen_area** -> the number of defensive actions completed by the player outside their 18 yard box