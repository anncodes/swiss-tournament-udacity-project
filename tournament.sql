-- tournament.sql is the SQL database which contains the database schema
-- and views of the tournament project.  In this file, we create tables 
-- and views


-- To import tournament.sql using the psql command line interface.
-- 
-- \i tournament.sql

/* Deletes the database if it exists */
DROP DATABASE IF EXISTS tournament;

/*Creates the database tournament */
CREATE DATABASE tournament;

/* Connects to the database tournament*/
\c tournament;


/* Creates the players table which contains the player's id and name */
CREATE TABLE players(
	playerid SERIAL PRIMARY KEY,
	name VARCHAR NOT NULL,
	);

/* Creates the matches table which contains match id, tournament, winner and the loser */
CREATE TABLE matches(
	matchid SERIAL PRIMARY KEY,
	winner INTEGER REFERENCES players(playerid),
	loser INTEGER REFERENCES players(playerid)
	);

/* Creates a view of players and the total number of wins

playerid |       name       | wins
----------+------------------+------
      172 | Fluttershy       |    1
      171 | Twilight Sparkle |    1
      173 | Applejack        |    0
      174 | Pinkie Pie       |    0
(4 rows)
      
 */

CREATE VIEW playerwins AS
SELECT players.playerid, players.name, COUNT(matches.winner) AS wins
FROM players
LEFT JOIN matches
ON players.playerid = matches.winner
GROUP BY players.playerid
ORDER BY wins DESC;

/* Creates a view of players and the total number of matches they played on

 playerid |       name       | matchesplayed
----------+------------------+---------------
      172 | Fluttershy       |             1
      173 | Applejack        |             1
      171 | Twilight Sparkle |             1
      174 | Pinkie Pie       |             1
(4 rows)

      
 */
CREATE VIEW totalmatches AS
SELECT players.playerid, players.name, COUNT(matches.winner) AS matchesplayed
FROM players
LEFT JOIN matches
ON players.playerid = matches.winner OR players.playerid = matches.loser
GROUP BY players.playerid
ORDER BY matchesplayed DESC;


/* Creates a view of players and their win records

 playerid |       name       | wins | matches
----------+------------------+------+---------
      172 | Fluttershy       |    1 |       1
      171 | Twilight Sparkle |    1 |       1
      173 | Applejack        |    0 |       1
      174 | Pinkie Pie       |    0 |       1

(4 rows)
  
 */
CREATE VIEW playerstandings AS
SELECT players.playerid, players.name, playerwins.wins as wins, 
       totalmatches.matchesplayed as matches
FROM players, playerwins, totalmatches
WHERE players.playerid = playerwins.playerid AND playerwins.playerid = totalmatches.playerid
ORDER BY wins DESC;

