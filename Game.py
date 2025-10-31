import tkinter as tk
from tkinter import messagebox
import random

# ------------------------------
# Generate Random Room Names
# ------------------------------

def generate_room_names():
    """Generate random room names for each location except Cell and Exit."""
    base_names = ["Room 1", "Room 2", "Room 3", "Room 4", "Dark Hall", "Shadow Room", "Ancient Chamber"]
    random.shuffle(base_names)

    return {
        "cell": "Cell",
        "hallway": base_names[0],
        "armory": base_names[1],
        "sword_room": base_names[2],
        "monster_room": base_names[3],
        "exit": "Exit"
    }

room_names = generate_room_names()

# ------------------------------
# Game Data
# ------------------------------

rooms = {
    room_names['cell']: {'south': room_names['hallway'], 'pos': (1, 0)},
    room_names['hallway']: {
        'north': room_names['cell'],
        'east': room_names['armory'],
        'south': room_names['exit'],
        'west': room_names['monster_room'],
        'pos': (1, 1)
    },
    room_names['armory']: {
        'west': room_names['hallway'],
        'east': room_names['sword_room'],
        'item': 'key',
        'pos': (2, 1)
    },
    room_names['sword_room']: {'west': room_names['armory'], 'item': 'sword', 'pos': (3, 1)},
    room_names['monster_room']: {'east': room_names['hallway'], 'monster': True, 'pos': (0, 1)},
    room_names['exit']: {'north': room_names['hallway'], 'pos': (1, 2)}
}

current_room = room_names['cell']
inventory = []
discovered = {current_room}

# ------------------------------
# Game Logic
# ------------------------------

def update_status():
    """Update game description, inventory, and map."""
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, f"You are in the {current_room}\n")

    if "item" in rooms[current_room]:
        text_area.insert(tk.END, f"You see a {rooms[current_room]['item']} here.\n")

    text_area.insert(tk.END, "Where do you want to go?\n")
    inventory_label.config(text=f"Inventory: {', '.join(inventory) or 'empty'}")
    draw_map()


def move(direction):
    """Handle moving between rooms."""
    global current_room
    if direction in rooms[current_room]:
        next_room = rooms[current_room][direction]
        current_room = next_room
        discovered.add(current_room)

        # Check for monster encounter
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
    """Pick up item if in room."""
    if "item" in rooms[current_room]:
        item = rooms[current_room]["item"]
        inventory.append(item)
        messagebox.showinfo("Item Collected", f"You picked up the {item}!")
        del rooms[current_room]["item"]
        update_status()
    else:
        messagebox.showinfo("Nothing Here", "There is nothing to pick up here.")


def check_win():
    """Check win condition."""
    if current_room == room_names['exit']:
        if "key" in inventory:
            messagebox.showinfo("Victory", "You unlocked the door and escaped the dungeon! 🎉")
            window.destroy()
        else:
            messagebox.showwarning("Locked Door", "The door is locked! You need a key.")


# ------------------------------
# Map Drawing
# ------------------------------

def draw_map():
    """Draw discovered rooms on the map canvas."""
    map_canvas.delete("all")
    cell_size = 80

    for room, data in rooms.items():
        x, y = data['pos']
        # Color code rooms
        if room not in discovered:
            color = "#888"
        elif "monster" in data:
            color = "#ff6961"
        elif "item" in data:
            color = "#ffd700"
        else:
            color = "#90ee90"

        outline = "red" if room == current_room else "black"

        map_canvas.create_rectangle(
            x * cell_size, y * cell_size,
            x * cell_size + cell_size, y * cell_size + cell_size,
            fill=color, outline=outline, width=2
        )
        map_canvas.create_text(
            x * cell_size + cell_size / 2,
            y * cell_size + cell_size / 2,
            text=room, font=("Arial", 8)
        )


# ------------------------------
# GUI Setup
# ------------------------------

window = tk.Tk()
window.title("Escape the Dungeon 🏰 — Random Adventure")
window.geometry("550x550")

title_label = tk.Label(window, text="Escape the Dungeon: Random Adventure", font=("Arial", 16, "bold"))
title_label.pack(pady=5)

text_area = tk.Text(window, height=8, width=55, wrap="word", bg="#f0f0f0")
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

# Item button
get_button = tk.Button(window, text="Pick Up Item", command=get_item, bg="#d4ed91", width=20)
get_button.pack(pady=5)

# Inventory label
inventory_label = tk.Label(window, text="Inventory: empty", font=("Arial", 10))
inventory_label.pack(pady=5)

# Map canvas
map_canvas = tk.Canvas(window, width=400, height=250, bg="#ddd")
map_canvas.pack(pady=10)

# Start game
update_status()
window.mainloop()
