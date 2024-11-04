import pyautogui
import random
import tkinter as tk

cycle = 0
check = 1
idle_num = [1, 2, 3, 4]
sleep_num = [10, 11, 12, 13, 15]
walk_left = [6, 7]
walk_right = [8, 9]
event_number = random.randrange(1, 3, 1)

# Update the path for your system
impath = r'C:\Users\76852\Desktop\Desktop.gif\\'


# Function definitions remain the same
def event(cycle, check, event_number):
    if event_number in idle_num:
        check = 0
        print('idle')
        window.after(400, update, cycle, check, event_number)
    elif event_number == 5:
        check = 1
        print('from idle to sleep')
        window.after(100, update, cycle, check, event_number)
    elif event_number in walk_left:
        check = 4
        print('walking towards left')
        window.after(100, update, cycle, check, event_number)
    elif event_number in walk_right:
        check = 5
        print('walking towards right')
        window.after(100, update, cycle, check, event_number)
    elif event_number in sleep_num:
        check = 2
        print('sleep')
        window.after(1000, update, cycle, check, event_number)
    elif event_number == 14:
        check = 3
        print('from sleep to idle')
        window.after(100, update, cycle, check, event_number)


def gif_work(cycle, frames, event_number, first_num, last_num):
    if cycle < len(frames) - 1:
        cycle += 1
    else:
        cycle = 0
        event_number = random.randrange(first_num, last_num + 1, 1)
    return cycle, event_number


def update(cycle, check, event_number):
    global window_x  # Access the window's current X position
    if check == 0:
        frame = idle[cycle]
        cycle, event_number = gif_work(cycle, idle, event_number, 1, 9)
        delay = 200  # Slow down idle animation
    elif check == 1:
        frame = idle_to_sleep[cycle]
        cycle, event_number = gif_work(cycle, idle_to_sleep, event_number, 10, 10)
        delay = 150  # Slow down transition to sleep
    elif check == 2:  # Sleeping state
        frame = sleep[cycle]
        cycle, event_number = gif_work(cycle, sleep, event_number, 10, 15)
        delay = 1000  # Sleep animations are slower
    elif check == 3:  # Transition from sleep to idle
        frame = sleep_to_idle[cycle]
        cycle, event_number = gif_work(cycle, sleep_to_idle, event_number, 1, 9)  # Transition back to idle events
        delay = 150  # Slow down transition
    elif check == 4:  # Walking left
        frame = walk_negative[cycle]
        cycle, event_number = gif_work(cycle, walk_negative, event_number, 1, 9)
        window_x -= 3  # Move the window left by 3 pixels
        delay = 100  # Moderate speed for walking
    elif check == 5:  # Walking right
        frame = walk_positive[cycle]
        cycle, event_number = gif_work(cycle, walk_positive, event_number, 1, 9)
        window_x += 3  # Move the window right by 3 pixels
        delay = 100  # Moderate speed for walking

    # Update window's geometry based on new window_x
    window.geometry(f'100x100+{window_x}+{window_y}')
    label.configure(image=frame)

    # Keep the event flow moving with new event number
    if check == 2:  # If the cat is sleeping, ensure transition back to idle (add this logic)
        event_number = 14  # Manually set event number to transition back from sleep
        window.after(1000, event, cycle, check, event_number)  # Trigger waking up after 1 second
    else:
        window.after(delay, event, cycle, check, event_number)  # Apply the delay for each state


# Function to start dragging
def start_drag(event):
    global last_click_x, last_click_y
    last_click_x = event.x
    last_click_y = event.y


# Function to handle dragging
def drag_window(event):
    x = event.x_root - last_click_x
    y = event.y_root - last_click_y
    window.geometry(f'+{x}+{y}')  # Move the window based on the new position


# Create the window
window = tk.Tk()

# Load your GIFs
idle = [tk.PhotoImage(file=impath + 'idle_cat.gif', format='gif -index %i' % (i)) for i in range(5)]
idle_to_sleep = [tk.PhotoImage(file=impath + 'idle_transition.gif', format='gif -index %i' % (i)) for i in range(9)]
sleep = [tk.PhotoImage(file=impath + 'sleep_cat.gif', format='gif -index %i' % (i)) for i in range(6)]
sleep_to_idle = [tk.PhotoImage(file=impath + 'sleep_transition.gif', format='gif -index %i' % (i)) for i in range(9)]
walk_positive = [tk.PhotoImage(file=impath + 'walk_right.gif', format='gif -index %i' % (i)) for i in range(4)]
walk_negative = [tk.PhotoImage(file=impath + 'walk_left.gif', format='gif -index %i' % (i)) for i in range(4)]

print("Loaded GIF frames:", len(idle), len(idle_to_sleep), len(sleep), len(sleep_to_idle), len(walk_positive),
      len(walk_negative))

# Get screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Window dimensions (adjust to your window's size)
window_width = 100
window_height = 100

# Set the window position to the bottom right, above the taskbar
window_x = screen_width - window_width  # Align to the right edge of the screen
window_y = screen_height - window_height - 60  # Align to the bottom edge, adjusting for the taskbar height (40 px is common)

# Set the geometry of the window
window.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')

# Configure window for transparency and topmost
window.overrideredirect(True)  # Remove window frame and title bar
window.wm_attributes('-topmost', True)  # Keep the pet on top

# Set transparent color to black, assuming the GIFs have transparent backgrounds
window.wm_attributes('-transparentcolor', 'black')

# Set the label background to black to match the transparent color
label = tk.Label(window, bd=0, bg='black')
label.pack()

# Bind mouse events for dragging
label.bind("<Button-1>", start_drag)  # Bind the left mouse button click to start dragging
label.bind("<B1-Motion>", drag_window)  # Bind mouse movement with the left button held down to drag the window

# Start the program
window.after(1, update, cycle, check, event_number)
window.mainloop()