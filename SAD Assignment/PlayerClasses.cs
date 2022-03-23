using System;
using System.Collections.Generic;
using System.Linq;

/*
Thijmen Bouwsema 1008331
*/

namespace SAD_Assignment
{
    /// <summary>
    /// Class <c>PlayerContainer</c> contains 2 static player classes for easy access
    /// </summary>
    public class PlayerContainer {
        public static Player Player1 { get; set; }
        public static Player Player2 { get; set; }
        public PlayerContainer(int playerHP) {
            Player1 = new Player(1, playerHP);
            Player2 = new Player(2, playerHP);
        }
    }
    /// <summary>
    /// Class <c>Player</c> defines a player of the game
    /// </summary>
    public class Player {
        public static Random rnd = new Random();
        public int ID { get; }
        public List<Card> Deck { get; set; }
        public List<Card> Hand { get; set; }
        public Stack<Card> DiscardPile { get; set; }
        public int HP { get; set; }
        public int Energy { get; set; }
        public Player(int id, int hp) {
            this.ID = id;
            this.Energy = 0;
            this.HP = hp;
            this.Deck = null;
            this.Hand = new List<Card>();
            this.DiscardPile = new Stack<Card>();
        }
        /// <summary>
        /// Method <c>AddDeck</c> adds a deck to the player class
        /// </summary>
        public void AddDeck(List<Card> deck) {
            this.Deck = deck;
        }
        /// <summary>
        /// Method <c>FillHand</c> fills player's hand untill it contains 7 cards
        /// </summary>
        public void FillHand() {
            // will take any non-Irrelevant cards and put them in hand
            for (int i = 0; i < this.Deck.Count; i++) {
                if (this.Deck[i].Type != Type.Irrelevant) {
                    Card addCard = this.Deck[i];
                    this.Deck.RemoveAt(i);
                    this.Hand.Add(addCard);
                }
            }
            // fills this.hand until there's 7 cards; moves cards from deck to hand
            while (this.Hand.Count < 7 && this.Deck.Count > 0) {
                Card addCard = this.Deck.First();
                this.Deck.RemoveAt(0);
                this.Hand.Add(addCard);
            }
        }
        /// <summary>
        /// Method <c>FillHand</c> fills player's hand by specified amount
        /// </summary>
        public void FillHand(int amount) {
            // fills this.hand with specified amount of cards; moves cards from deck to hand
            while (amount > 0 && this.Deck.Count > 0) {
                Card addCard = this.Deck.First();
                this.Deck.RemoveAt(0);
                this.Hand.Add(addCard);
                amount--;
            }
        }
        /// <summary>
        /// Method <c>DiscardHand</c> removes specified amount of cards from player's hand and adds them to player's discard pile
        /// </summary>
        public void DiscardHand(int amount) {
            // take cards from Hand to DiscardPile (equal to amount)
            // selects random cards to move from hand to discard pile;
            while (amount > 0 && this.Hand.Count > 0) {
                int handIndex = rnd.Next(this.Hand.Count);
                this.DiscardPile.Push(this.Hand[handIndex]);
                this.Hand.RemoveAt(handIndex);
                amount--;
            }
        }
        /// <summary>
        /// Method <c>DiscardHand</c> removes specified card from player's hand and adds it to player's discard pile
        /// </summary>
        public void DiscardHand(Card specificCard) {
            // discards specific card from hand
            if (this.Hand.Count < 1) {
                return;
            }
            for (int i = 0; i < this.Hand.Count; i++) {
                if (specificCard.CardName == this.Hand[i].CardName && specificCard.State == this.Hand[i].State) {
                    this.DiscardPile.Push(this.Hand[i]);
                    this.Hand.RemoveAt(i);
                    return;
                }
            }
        }
        /// <summary>
        /// Method <c>ChangeHP</c> alters player's HP by specified amount
        /// </summary>
        public void ChangeHP(int amount) {
            // (amount > 0) = damage; (amount < 0) = healing
            int newHP = this.HP - amount;
            if (newHP < 0) {
                this.HP = 0;
            }
            else {
                this.HP = newHP;
            }
        }
        /// <summary>
        /// Method <c>ChangeEnergy</c> alters player's energy by specified amount
        /// </summary>
        public void ChangeEnergy(int amount) {
            // adds {amount} energy of specified color to energy reserve (if < 0 it subtracts)
            this.Energy = this.Energy + amount;
        }

        // 1 unused method

        /// <summary>
        /// Method <c>ShuffleDeck</c> randomises the order of player's deck
        /// </summary>
        public void ShuffleDeck() {
            // not implemented; deliverable case does not require it's implementation (decks have specific cards; shuffling would randomise their order in the deck)
        }
    }
}