import random


rooms = {
    'hall': {'south': 'kitchen', 'east': 'dining room', 'item': None},
    'kitchen': {'north': 'hall', 'item': 'monster'},
    'dining room': {'west': 'hall', 'south': 'garden', 'item': 'key'},
    'garden': {'north': 'dining room', 'item': 'treasure'}
}


current_room = 'hall'
inventory = []


def show_state():
    print(f"\nyou are in the {current_room}")
    if 'item' in rooms[current_room] and rooms[current_room]['item']:
        print(f"you see a {rooms[current_room]['item']}")
    print(f"inventory: {inventory}")


def move(direction):
    global current_room
    if direction in rooms[current_room]:
        current_room = rooms[current_room][direction]
    else:
        print("you can't go that way")


def get_item():
    global inventory
    item = rooms[current_room].get('item')
    if item:
        if item == 'monster':
            print("a monster caught you. game over.")
            return False
        else:
            inventory.append(item)
            print(f"you picked up a {item}")
            rooms[current_room]['item'] = None
    else:
        print("there's nothing here to pick up")
    return True


def main():
    print("welcome to the adventure game")
    print("move commands: go north, go south, go east, go west")
    print("add to inventory: get 'item name'")
    print("reach the garden with the key to win the game")
    
    while True:
        show_state()
        move_valid = True
        command = input("\n>").strip().lower()
        
        if command.startswith('go '):
            move(command.split()[1])
        elif command == 'get':
            move_valid = get_item()
        else:
            print("invalid command.")
        
        if not move_valid:
            break
        
        if current_room == 'garden' and 'key' in inventory:
            print("you have reached the garden and found the treasure. you win.")
            break


if __name__ == "__main__":
    main()
