import tkinter as tk
from tkinter import messagebox
import random

# ------------------------------
# Dungeon Generator
# ------------------------------

def generate_dungeon():
    """Generate a random dungeon layout with 4–7 rooms."""
    room_count = random.randint(4, 7)
    base_names = [
        "Dusty Room", "Dark Chamber", "Hall of Echoes", "Stone Passage",
        "Hidden Vault", "Old Armory", "Cursed Hall", "Twisting Hall", "Forgotten Nook"
    ]
    random.shuffle(base_names)

    # Fixed start and exit rooms
    start = "Cell"
    exit_room = "Exit"

    # Choose random extra rooms
    room_names = base_names[:room_count - 2]

    # Assign random positions on a 3x3 grid (excluding start top middle and exit bottom middle)
    coords = [(x, y) for x in range(3) for y in range(3) if (x, y) not in [(1,0), (1,2)]]
    random.shuffle(coords)

    rooms = {start: {"pos": (1, 0)}}  # Start always top middle
    rooms[exit_room] = {"pos": (1, 2)}  # Exit bottom middle

    # Fill in random rooms
    for name in room_names:
        rooms[name] = {"pos": coords.pop()}

    # Assign items
    available_rooms = [r for r in room_names if r not in (start, exit_room)]

    if available_rooms:
        sword_room = random.choice(available_rooms)
        rooms[sword_room]["item"] = "sword"

    possible_key_rooms = [r for r in available_rooms if "item" not in rooms[r]]
    if possible_key_rooms:
        key_room = random.choice(possible_key_rooms)
        rooms[key_room]["item"] = "key"

    # Place monster in a different random room
    monster_candidates = [r for r in available_rooms if "item" not in rooms[r]]
    if monster_candidates:
        monster_room = random.choice(monster_candidates)
        rooms[monster_room]["monster"] = True

    return rooms, start, exit_room

# ------------------------------
# Game Setup
# ------------------------------

rooms, start_room, exit_room = generate_dungeon()
current_room = start_room
inventory = []
discovered = {current_room}

# Map from coordinates to room names for coordinate-based movement
coord_to_room = {data['pos']: room for room, data in rooms.items()}

# ------------------------------
# Game Logic
# ------------------------------

def update_status():
    """Update room info, inventory, and map."""
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, f"You are in the {current_room}\n")

    if "item" in rooms[current_room]:
        text_area.insert(tk.END, f"You see a {rooms[current_room]['item']} here.\n")

    text_area.insert(tk.END, "Where do you want to go?\n")
    inventory_label.config(text=f"Inventory: {', '.join(inventory) or 'empty'}")

    draw_map()

def move(direction):
    """Move between rooms using coordinate-based logic."""
    global current_room
    x, y = rooms[current_room]['pos']

    if direction == "north":
        target_coord = (x, y-1)
    elif direction == "south":
        target_coord = (x, y+1)
    elif direction == "east":
        target_coord = (x+1, y)
    elif direction == "west":
        target_coord = (x-1, y)
    else:
        return

    if target_coord in coord_to_room:
        current_room = coord_to_room[target_coord]
        discovered.add(current_room)

        # Monster encounter
        if "monster" in rooms[current_room]:
            if "sword" in inventory:
                messagebox.showinfo("Battle!", "You fought bravely and defeated the monster! 🗡️")
                del rooms[current_room]["monster"]
            else:
                messagebox.showerror("Game Over", "💀 A monster attacks! You died. Try again.")
                window.destroy()
                return

        update_status()
        check_win()
    else:
        messagebox.showinfo("Blocked", "You can't go that way!")

def get_item():
    """Pick up items."""
    if "item" in rooms[current_room]:
        item = rooms[current_room]["item"]
        inventory.append(item)
        messagebox.showinfo("Item Collected", f"You picked up the {item}!")
        del rooms[current_room]["item"]
        update_status()
    else:
        messagebox.showinfo("Nothing Here", "There is nothing to pick up here.")

def check_win():
    """Check for win condition."""
    if current_room == exit_room:
        if "key" in inventory:
            messagebox.showinfo("Victory", "You unlocked the door and escaped the dungeon! 🎉")
            window.destroy()
        else:
            messagebox.showwarning("Locked Door", "The door is locked! You need a key.")

# ------------------------------
# Map Drawing
# ------------------------------

def draw_map():
    """Draw map with hidden unexplored names."""
    map_canvas.delete("all")
    cell_size = 80

    for room, data in rooms.items():
        x, y = data['pos']
        color = "#888"  # unexplored
        label = ""      # hide names

        if room in discovered:
            if "monster" in data:
                color = "#ff6961"
            elif "item" in data:
                color = "#ffd700"
            else:
                color = "#90ee90"
            label = room  # show name after discovering

        outline = "red" if room == current_room else "black"

        map_canvas.create_rectangle(
            x * cell_size, y * cell_size,
            x * cell_size + cell_size, y * cell_size + cell_size,
            fill=color, outline=outline, width=2
        )

        if label:
            map_canvas.create_text(
                x * cell_size + cell_size / 2,
                y * cell_size + cell_size / 2,
                text=label,
                font=("Arial", 8)
            )

# ------------------------------
# GUI Setup
# ------------------------------

window = tk.Tk()
window.title("Escape the Dungeon 🏰 — Random Adventure")
window.geometry("600x550")

title_label = tk.Label(window, text="Escape the Dungeon: Random Adventure", font=("Arial", 16, "bold"))
title_label.pack(pady=5)

text_area = tk.Text(window, height=8, width=60, wrap="word", bg="#f0f0f0")
text_area.pack(padx=10, pady=5)

# Movement buttons
button_frame = tk.Frame(window)
button_frame.pack()

btn_north = tk.Button(button_frame, text="Go North", command=lambda: move("north"), width=10)
btn_south = tk.Button(button_frame, text="Go South", command=lambda: move("south"), width=10)
btn_east = tk.Button(button_frame, text="Go East", command=lambda: move("east"), width=10)
btn_west = tk.Button(button_frame, text="Go West", command=lambda: move("west"), width=10)

btn_north.grid(row=0, column=1, padx=5, pady=5)
btn_west.grid(row=1, column=0, padx=5, pady=5)
btn_east.grid(row=1, column=2, padx=5, pady=5)
btn_south.grid(row=2, column=1, padx=5, pady=5)

# Pick up item button
get_button = tk.Button(window, text="Pick Up Item", command=get_item, bg="#d4ed91", width=20)
get_button.pack(pady=5)

# Inventory label
inventory_label = tk.Label(window, text="Inventory: empty", font=("Arial", 10))
inventory_label.pack(pady=5)

# Map
map_canvas = tk.Canvas(window, width=400, height=250, bg="#ddd")
map_canvas.pack(pady=10)

# Start game
update_status()
window.mainloop()
