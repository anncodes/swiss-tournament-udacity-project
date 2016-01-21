#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
# This file is used to provide access to the database via a library of 
# functions which can add, delete or query data in the tournament.sql database  
#
#

# Connects to the tournament database
import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""

    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    conn = DB.cursor()
    conn.execute("DELETE FROM matches;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    conn = DB.cursor()
    conn.execute("DELETE FROM players;")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    conn = DB.cursor()
    conn.execute("SELECT count(*) FROM players;")
    rows = conn.fetchall()
    DB.close()
    return rows[0][0]




def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    conn = DB.cursor()
    conn.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    DB.commit()
    DB.close()
    
    

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    conn = DB.cursor()
    conn.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)", (winner, loser,))
    DB.commit()
    DB.close()



def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    conn = DB.cursor()
    conn.execute("SELECT players.playerid, players.name, playerwins.wins as wins, totalmatches.matchesplayed as matches FROM players, playerwins, totalmatches WHERE players.playerid = playerwins.playerid AND playerwins.playerid = totalmatches.playerid ORDER BY wins;")
    standings = conn.fetchall()
    DB.close()
    return standings
   	
 	

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    
    pairings = []
    standings = playerStandings()
    for i in range(1, len(standings), 2):
       pair = (standings[i-1][0], standings[i-1][1], standings[i][0], standings[i][1])
       pairings.append(pair)
    return pairings
    

