#!/usr/bin/env python3
"""
Blackjack (21) - Console Version
--------------------------------
Rules implemented:
- You (player) vs. dealer (computer).
- Player gets two cards face-up; dealer gets two cards (one face-up, one face-down).
- Player may Hit (take a card) or Stand (stop).
- Dealer must hit on 16 or less, and stand on 17 or more.
- Aces count as 1 or 11 to best benefit the hand.
- Face cards J, Q, K are worth 10.
- Dealer wins all ties.
"""

import random
from typing import List, Tuple

# Card representation:
# Each card is a tuple: (rank, suit)
# rank: '2'..'10', 'J', 'Q', 'K', 'A'
# suit: '♠', '♥', '♦', '♣'


RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['♠', '♥', '♦', '♣']


def build_deck(shuffle: bool = True) -> List[Tuple[str, str]]:
    """Create a standard 52-card deck; optionally shuffle it."""
    deck = [(rank, suit) for suit in SUITS for rank in RANKS]
    if shuffle:
        random.shuffle(deck)
    return deck


def card_value(rank: str) -> int:
    """Return the base value of a single card rank (Ace treated as 11 here; we adjust later)."""
    if rank in ('J', 'Q', 'K'):
        return 10
    if rank == 'A':
        return 11  # we'll adjust for aces later
    return int(rank)


def hand_value(hand: List[Tuple[str, str]]) -> int:
    """
    Compute the best value of a Blackjack hand.
    Aces are initially counted as 11; we lower them to 1 as needed to avoid busting.
    """
    value = 0
    aces = 0
    for rank, _ in hand:
        v = card_value(rank)
        value += v
        if rank == 'A':
            aces += 1

    # If we're over 21 and have aces counted as 11, convert them (11 -> 1) one by one
    while value > 21 and aces > 0:
        value -= 10  # change one Ace from 11 to 1
        aces -= 1

    return value


def format_card(card: Tuple[str, str]) -> str:
    """Return a user-friendly string for a single card, e.g., 'A♠' or '10♥'."""
    rank, suit = card
    return f"{rank}{suit}"


def format_hand(hand: List[Tuple[str, str]]) -> str:
    """Return a user-friendly string for a list of cards."""
    return ' '.join(format_card(c) for c in hand)


def deal_initial_hands(deck: List[Tuple[str, str]]):
    """Deal two cards to player and dealer (dealer's second card is 'hidden')."""
    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]
    return player, dealer


def player_turn(deck: List[Tuple[str, str]], hand: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """
    Player chooses to Hit or Stand.
    Returns the final player hand.
    """
    while True:
        print(f"\nYour hand: {format_hand(hand)} (value: {hand_value(hand)})")
        choice = input("Hit or Stand? [H/S]: ").strip().lower()
        if choice in ('h', 'hit'):
            hand.append(deck.pop())
            value = hand_value(hand)
            print(f"You drew: {format_card(hand[-1])}. Hand value is now {value}.")
            if value > 21:
                print("You busted!")
                break
        elif choice in ('s', 'stand'):
            break
        else:
            print("Please type 'H' to Hit or 'S' to Stand.")
    return hand


def dealer_turn(deck: List[Tuple[str, str]], hand: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """
    Dealer must hit on 16 or less, stand on 17+.
    Returns the final dealer hand.
    """
    print(f"\nDealer reveals hole card: {format_card(hand[1])}")
    print(f"Dealer's hand: {format_hand(hand)} (value: {hand_value(hand)})")

    while hand_value(hand) <= 16:
        drawn = deck.pop()
        hand.append(drawn)
        print(f"Dealer hits and draws: {format_card(drawn)}")
        print(f"Dealer's hand: {format_hand(hand)} (value: {hand_value(hand)})")

    if hand_value(hand) > 21:
        print("Dealer busts!")
    else:
        print("Dealer stands.")
    return hand


def determine_winner(player: List[Tuple[str, str]], dealer: List[Tuple[str, str]]) -> str:
    """
    Determine the outcome according to rules:
    - Dealer wins all ties.
    Returns 'player', 'dealer', or 'push' (push will not occur due to 'dealer wins ties' rule).
    """
    p_val = hand_value(player)
    d_val = hand_value(dealer)

    if p_val > 21:
        return 'dealer'
    if d_val > 21:
        return 'player'
    if p_val > d_val:
        return 'player'
    # dealer wins ties and when d_val > p_val
    return 'dealer'


def play_round() -> None:
    """Play a single round of Blackjack."""
    deck = build_deck(shuffle=True)
    player, dealer = deal_initial_hands(deck)

    # Show initial hands (dealer shows only one card)
    print("\n=== New Round ===")
    print(f"Dealer shows: {format_card(dealer[0])} and [hidden]")
    print(f"Your hand: {format_hand(player)} (value: {hand_value(player)})")

    # Player turn
    player = player_turn(deck, player)

    # If player busts, dealer wins immediately
    if hand_value(player) > 21:
        print("\nDealer wins!")
        print(f"Dealer hand was: {format_hand(dealer)} (value: {hand_value(dealer)})")
        return

    # Dealer turn
    dealer = dealer_turn(deck, dealer)

    # Determine outcome
    result = determine_winner(player, dealer)

    print("\n=== Results ===")
    print(f"Your hand:   {format_hand(player)} (value: {hand_value(player)})")
    print(f"Dealer hand: {format_hand(dealer)} (value: {hand_value(dealer)})")

    if result == 'player':
        print("You win!")
    elif result == 'dealer':
        print("Dealer wins! (Dealer wins ties)")
    else:
        print("Push (tie).")  # Should not occur with 'dealer wins ties', kept for completeness.


def main():
    print("Welcome to Blackjack! (Dealer wins ties)")
    while True:
        play_round()
        again = input("\nPlay again? [Y/N]: ").strip().lower()
        if again not in ('y', 'yes'):
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
