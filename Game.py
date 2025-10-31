import tkinter as tk
from tkinter import messagebox
import random

# ------------------------------
# Dungeon Generator
# ------------------------------

def generate_dungeon():
    """Generate a 3x3 grid dungeon with random special rooms."""
    grid_size = 3
    positions = [(x, y) for x in range(grid_size) for y in range(grid_size)]
    random.shuffle(positions)

    # Assign rooms to coordinates
    rooms = {}
    for idx, pos in enumerate(positions):
        rooms[pos] = {"name": f"Room {idx+1}"}

    # Randomly assign special rooms
    special_rooms = random.sample(list(positions), 4)
    cell_pos, exit_pos, sword_pos, monster_pos = special_rooms

    rooms[cell_pos]["name"] = "Cell"
    rooms[cell_pos]["discovered"] = True  # start discovered

    rooms[exit_pos]["name"] = "Exit"
    rooms[sword_pos]["item"] = "sword"
    rooms[monster_pos]["monster"] = True

    return rooms, cell_pos, exit_pos

# ------------------------------
# Game Setup
# ------------------------------

rooms, current_pos, exit_pos = generate_dungeon()
inventory = []
discovered = {current_pos}

grid_size = 3

# ------------------------------
# Game Logic
# ------------------------------

def update_status():
    """Update room info, inventory, and map."""
    room_data = rooms[current_pos]
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, f"You are in the {room_data['name']}\n")

    if "item" in room_data:
        text_area.insert(tk.END, f"You see a {room_data['item']} here.\n")

    text_area.insert(tk.END, "Where do you want to go?\n")
    inventory_label.config(text=f"Inventory: {', '.join(inventory) or 'empty'}")
    draw_map()

def move(direction):
    """Move between rooms using grid coordinates."""
    global current_pos
    x, y = current_pos

    if direction == "north":
        target = (x, y-1)
    elif direction == "south":
        target = (x, y+1)
    elif direction == "east":
        target = (x+1, y)
    elif direction == "west":
        target = (x-1, y)
    else:
        return

    if target in rooms:
        current_pos = target
        discovered.add(current_pos)
        room_data = rooms[current_pos]

        # Monster encounter
        if "monster" in room_data:
            if "sword" in inventory:
                messagebox.showinfo("Battle!", "You fought bravely and defeated the monster! 🗡️")
                del rooms[current_pos]["monster"]
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
    room_data = rooms[current_pos]
    if "item" in room_data:
        item = room_data["item"]
        inventory.append(item)
        messagebox.showinfo("Item Collected", f"You picked up the {item}!")
        del room_data["item"]
        update_status()
    else:
        messagebox.showinfo("Nothing Here", "There is nothing to pick up here.")

def check_win():
    """Check for win condition."""
    room_data = rooms[current_pos]
    if room_data["name"] == "Exit":
        if "key" in inventory:
            messagebox.showinfo("Victory", "You unlocked the door and escaped the dungeon! 🎉")
            window.destroy()
        else:
            messagebox.showwarning("Locked Door", "The door is locked! You need a key.")

# ------------------------------
# Map Drawing
# ------------------------------

def draw_map():
    """Draw 3x3 grid map with discovered rooms."""
    map_canvas.delete("all")
    cell_size = 80

    for pos, data in rooms.items():
        x, y = pos
        color = "#888"  # unexplored
        label = ""

        if pos in discovered:
            if "monster" in data:
                color = "#ff6961"
            elif "item" in data:
                color = "#ffd700"
            elif data["name"] == "Exit":
                color = "#90ee90"
            else:
                color = "#add8e6"
            label = data["name"]

        outline = "red" if pos == current_pos else "black"

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
window.title("Escape the Dungeon 🏰 — 3x3 Random Adventure")
window.geometry("600x550")

title_label = tk.Label(window, text="Escape the Dungeon: 3x3 Grid Random Adventure", font=("Arial", 16, "bold"))
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
map_canvas = tk.Canvas(window, width=300, height=300, bg="#ddd")
map_canvas.pack(pady=10)

# Start game
update_status()
window.mainloop()
