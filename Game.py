# ------------------------------

# Dungeon Generatorz
# Student Number: 2504 3634 01 
# Student Name: Muhammad Moazzam Kiani 
# y6a12@students.keele.ac.uk
# ------------------------------ 
# "This project was developed with the assistance of ChatGPT (GPT-5-mini) for guidance, code suggestions, and debugging support."

# ------------------------------




import tkinter as tk
from tkinter import messagebox
import random




# ------------------------------
grid_rows = 4
grid_cols = 3
cell_size = 80  # size of each room in pixels
# ------------------------------

def generate_dungeon(rows=grid_rows, cols=grid_cols):
    """Generate a dungeon with random special rooms."""
    positions = [(x, y) for x in range(cols) for y in range(rows)]
    random.shuffle(positions)

    # Assign rooms to coordinates
    rooms = {}
    for idx, pos in enumerate(positions):
        rooms[pos] = {"name": f"Room {idx+1}"}

    # Randomly assign special rooms
    special_rooms = random.sample(positions, 4)
    cell_pos, exit_pos, sword_pos, monster_pos = special_rooms

    rooms[cell_pos]["name"] = "Cell"
    rooms[cell_pos]["discovered"] = True  # start discovered

    rooms[exit_pos]["name"] = "Exit"
    rooms[sword_pos]["item"] = "sword"
    rooms[monster_pos]["monster"] = True

    # Add a key to a random room that isn't Cell or Exit
    remaining_positions = [pos for pos in positions if pos not in (cell_pos, exit_pos)]
    key_pos = random.choice(remaining_positions)
    rooms[key_pos]["item"] = "key"

    return rooms, cell_pos, exit_pos

# ------------------------------
# Game State
# ------------------------------
rooms, current_pos, exit_pos = generate_dungeon()
inventory = []
discovered = {current_pos}

# ------------------------------
# Game Logic
# ------------------------------
def update_status():
    room_data = rooms[current_pos]
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, f"You are in the {room_data['name']}\n")
    if "item" in room_data:
        text_area.insert(tk.END, f"You see a {room_data['item']} here.\n")
    text_area.insert(tk.END, "Where do you want to go?\n")
    inventory_label.config(text=f"Inventory: {', '.join(inventory) or 'empty'}")
    draw_map()

def move(direction):
    global current_pos
    x, y = current_pos
    target = {
        "north": (x, y-1),
        "south": (x, y+1),
        "east":  (x+1, y),
        "west":  (x-1, y)
    }.get(direction, None)

    if target and target in rooms:
        current_pos = target
        discovered.add(current_pos)
        room_data = rooms[current_pos]

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
    room_data = rooms[current_pos]
    if room_data["name"] == "Exit":
        if "key" in inventory:
            messagebox.showinfo("Victory", "You unlocked the door and escaped the dungeon! 🎉")
            window.destroy()
        else:
            messagebox.showwarning("Locked Door", "The door is locked! You need a key.")

def restart_game():
    global rooms, current_pos, exit_pos, inventory, discovered
    rooms, current_pos, exit_pos = generate_dungeon()
    inventory = []
    discovered = {current_pos}
    update_status()

# ------------------------------
# Map Drawing
# ------------------------------
def draw_map():
    map_canvas.delete("all")
    for pos, data in rooms.items():
        x, y = pos
        color = "#888"  # unexplored
        label = ""

        if pos in discovered:
            if "monster" in data:
                color = "#ff6961"
                label = "👹"
            elif "item" in data:
                color = "#ffd700"
                label = "🗡️" if data["item"]=="sword" else "🗝️"
            elif data["name"] == "Exit":
                color = "#90ee90"
                label = "🚪"
            else:
                color = "#add8e6"
                label = "🏠"

        outline = "red" if pos == current_pos else "black"

        map_canvas.create_rectangle(
            x*cell_size, y*cell_size,
            x*cell_size+cell_size, y*cell_size+cell_size,
            fill=color, outline=outline, width=2
        )

        if label:
            try:
                map_canvas.create_text(
                    x*cell_size + cell_size/2,
                    y*cell_size + cell_size/2,
                    text=label, font=("Segoe UI Emoji", 24)
                )
            except:
                fallback = {"👹": "M", "🗡️": "S", "🗝️": "K", "🚪": "E", "🏠": "R"}
                map_canvas.create_text(
                    x*cell_size + cell_size/2,
                    y*cell_size + cell_size/2,
                    text=fallback.get(label, "?"),
                    font=("Arial", 20)
                )

# ------------------------------
# GUI Setup
# ------------------------------
window = tk.Tk()
window.title("Escape the Dungeon 🏰 — 4x3 Grid Adventure")
window.geometry(f"{grid_cols*cell_size+50}x{grid_rows*cell_size+250}")

title_label = tk.Label(window, text="Escape the Dungeon: 4x3 Grid Adventure", font=("Arial", 16, "bold"))
title_label.pack(pady=5)

# Restart Button
restart_button = tk.Button(window, text="Restart Game", command=restart_game, bg="#a0e7e5", width=20)
restart_button.pack(pady=5)

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

# Map canvas
map_canvas = tk.Canvas(window, width=grid_cols*cell_size, height=grid_rows*cell_size, bg="#ddd")
map_canvas.pack(pady=10)

# Start game
update_status()
window.mainloop()