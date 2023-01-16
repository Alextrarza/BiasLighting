import tkinter as tk

window = tk.Tk(className = 'Konfiguracja paskow Led')

# Create an empty list to store the cursor positions
cursor_positions = []

def on_click(event):
    cursor_positions.append((event.x, event.y))
    # Draw a black rectangle on the cursor position
    x, y = event.x, event.y
    canvas.create_rectangle(x-10, y-10, x+10, y+10, fill="#ffffff")
    print(cursor_positions)

# Bind keypress event to handle_keypress()
window.bind("q", lambda event: window.destroy())

window.attributes("-fullscreen", True)
window.configure(bg = '#a7f059')
window.bind("<Button-1>", on_click)

# Create the quit button
quit_button = tk.Button(window, text="Quit", command=window.destroy, width = 25, height = 2)
quit_button.place(x=window.winfo_screenwidth()-200,y=4)


# Create the canvas
canvas = tk.Canvas(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight()-50)
canvas.place(x=0,y=50)
canvas.configure(bg = '#707070')
window.mainloop()
