from flask import Flask, session, redirect, url_for, render_template, request
import random

app = Flask(__name__)
app.secret_key = 'replace-with-a-secure-random-key'

RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['♠', '♥', '♦', '♣']

def build_deck(shuffle=True):
    deck = [(rank, suit) for suit in SUITS for rank in RANKS]
    if shuffle:
        random.shuffle(deck)
    return deck

def card_value(rank):
    if rank in ('J', 'Q', 'K'):
        return 10
    if rank == 'A':
        return 11
    return int(rank)

def hand_value(hand):
    value = 0
    aces = 0
    for rank, _ in hand:
        v = card_value(rank)
        value += v
        if rank == 'A':
            aces += 1
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1
    return value

def format_card(card):
    rank, suit = card
    return f"{rank}{suit}"

def format_hand(hand):
    return ' '.join(format_card(c) for c in hand)

def deal_initial_hands(deck):
    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]
    return player, dealer

def dealer_turn(deck, hand):
    while hand_value(hand) <= 16:
        hand.append(deck.pop())
    return hand

def determine_winner(player, dealer):
    p_val = hand_value(player)
    d_val = hand_value(dealer)
    if p_val > 21:
        return 'dealer'
    if d_val > 21:
        return 'player'
    if p_val > d_val:
        return 'player'
    return 'dealer'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    deck = build_deck()
    player, dealer = deal_initial_hands(deck)
    session['deck'] = deck
    session['player'] = player
    session['dealer'] = dealer
    session['state'] = 'playing'
    return redirect(url_for('game'))

@app.route('/game', methods=['GET', 'POST'])
def game():
    deck = session.get('deck')
    player = session.get('player')
    dealer = session.get('dealer')
    state = session.get('state', 'playing')
    message = ''

    if request.method == 'POST' and state == 'playing':
        action = request.form.get('action')
        if action == 'hit':
            player.append(deck.pop())
            if hand_value(player) > 21:
                state = 'done'
                message = 'You busted! Dealer wins.'
        elif action == 'stand':
            state = 'dealer'
            session['state'] = state

    if state == 'dealer':
        dealer = dealer_turn(deck, dealer)
        winner = determine_winner(player, dealer)
        state = 'done'
        if winner == 'player':
            message = 'You win!'
        else:
            message = 'Dealer wins! (Dealer wins ties)'
        session['dealer'] = dealer
        session['state'] = state

    session['player'] = player
    session['dealer'] = dealer
    session['deck'] = deck
    session['state'] = state

    return render_template('game.html',
        player_hand=format_hand(player),
        player_value=hand_value(player),
        dealer_hand=format_hand([dealer[0]]) + ' [hidden]' if state == 'playing' else format_hand(dealer),
        dealer_value=hand_value([dealer[0]]) if state == 'playing' else hand_value(dealer),
        state=state,
        message=message
    )

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)