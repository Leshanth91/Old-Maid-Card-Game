import random

def wait_for_player():
    '''() -> None
    Pauses the program until the user presses enter.
    '''
    try:
         input("\nPress enter to continue. ")
         print()
    except SyntaxError:
         pass


def make_deck():
    '''() -> list of str
    Returns a deck of playing cards with one queen missing.
    '''
    deck=[]
    # Define standard suits and ranks using unicode for card symbols
    suits = ['\u2660', '\u2661', '\u2662', '\u2663']
    ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    
    # Nested loop to pair every rank with every suit
    for suit in suits:
        for rank in ranks:
            deck.append(rank+suit)
            
    deck.remove('Q\u2663') # Remove one queen to setup the Old Maid dynamic
    return deck

def shuffle_deck(deck):
    '''(list of str) -> None
    Randomly shuffles the given list of cards.
    '''
    random.shuffle(deck)

#####################################

def deal_cards(deck):
     '''(list of str) -> tuple of (list of str, list of str)
     Splits the deck into two lists for the dealer and the player.
     '''
     dealer=[]
     other=[]

     # Alternates dealing cards between the dealer and the player using modulo
     for i in range(len(deck)):
         if i%2==0:
            dealer.append(deck[i])
         else:
            other.append(deck[i])

     return (dealer, other)
 


def remove_pairs(l):
    '''(list of str) -> list of str
    Returns a shuffled copy of the list with all matching pairs removed.
    
    Precondition: Elements of l must be valid card strings.
    '''

    no_pairs=[]
    unique_ranks=[]

    # Step 1: Isolate and collect all unique card ranks present in the hand
    for card in l:
        rank=card[:-1] # Slices off the suit character at the end to get the rank
        if rank not in unique_ranks:
            unique_ranks.append(rank)
    
    # Step 2: Group cards by rank and discard matches
    for rank in unique_ranks:
        cards_of_this_rank=[]
    
        # Gather all matching cards of this specific rank
        for card in l:
            if card[:-1]==rank:
                cards_of_this_rank.append(card)

        # Pairs cancel out; if an odd number exists, exactly 1 card stays
        if len(cards_of_this_rank)%2 != 0: 
            no_pairs.append(cards_of_this_rank[0])

    random.shuffle(no_pairs) # Shuffle the remaining cards as required
    return no_pairs


def print_deck(deck):
    '''(list of str) -> None
    Prints elements of the deck separated by spaces.
    '''

    output = ""
    for card in deck:
        output += card + " "
    
    print(output.strip())

    
def get_valid_input(n):
     '''(int) -> int
     Asks the user for an integer between 1 and n until a valid one is given.
     
     Precondition: n must be greater than or equal to 1.
     '''

     valid = False
     user_choice = 0
     
     # Input validation loop to force a safe choice within deck boundaries
     while not valid:
          user_choice = int(input("Give me an integer between 1 and " + str(n) + ": "))
          if user_choice >= 1 and user_choice <= n:
               valid = True
          else:
               print("Invalid number. Please enter integer between 1 and " + str(n) + ": ", end="")
               
     return user_choice

def play_game():
     '''() -> None
     Starts and runs the full card game loop.
     '''
    
     deck=make_deck()
     shuffle_deck(deck)
     tmp=deal_cards(deck)

     dealer=tmp[0]
     human=tmp[1]

     print("Hello. My name is Robot and I am the dealer.")
     print("Welcome to my card game!")
     print("Your current deck of cards is:")
     print_deck(human)
     print("Do not worry. I cannot see the order of your cards")

     print("Now discard all the pairs from your deck. I will do the same.")
     wait_for_player()
     
     # Initial pair discarding phase before main gameplay turns begin
     dealer=remove_pairs(dealer)
     human=remove_pairs(human)

     turn = 1

     # Main Core Game Loop: Runs until either the dealer or human runs out of cards
     while len(dealer) > 0 and len(human) > 0:
          print("***********************************************************")
          
          if turn == 1:
               print("Your turn.")
               print("Your current deck of cards is:")
               print_deck(human)
               
               print("I have " + str(len(dealer)) + " cards. If 1 stands for my first card and")
               print(str(len(dealer)) + " for my last card, which of my cards would you like?")
               
               # Process player picking a card from the dealer
               choice = get_valid_input(len(dealer))
               chosen_card = dealer.pop(choice - 1) # Subtract 1 to match 0-indexed list
               
               print("You asked for my " + str(choice) + "th card.")
               print("Here it is. It is " + chosen_card)
               
               # Add the stolen card to player's hand and instantly clean up pairs
               human.append(chosen_card)
               print("With " + chosen_card + " added, your current deck of cards is:")
               print_deck(human)
               
               human = remove_pairs(human)
               print("And after discarding pairs and shuffling, your deck is:")
               print_deck(human)
               
               wait_for_player()
               turn = 0 # Hand over the turn to the robot
               
          else:
               print("My turn.")
               # Robot selects a random index from the human's hand
               robot_choice = random.randint(0, len(human) - 1)
               chosen_card = human.pop(robot_choice)
               
               print("I took your " + str(robot_choice + 1) + "th card.")
               
               # Add stolen card to dealer's hand and discard matching pairs
               dealer.append(chosen_card)
               dealer = remove_pairs(dealer)
               
               wait_for_player()
               turn = 1 # Hand over the turn back to the human

     # Game Win/Loss Evaluation Phase
     if len(human) == 0:
          print("Oops. You do not have any more cards")
          print("Congratulations! You, Human, win")
          
     else:
          print("Oops. I do not have any more cards")
          print("You lost! I, Robot, win")

	 

# main
play_game()
