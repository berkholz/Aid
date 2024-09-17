import tkinter as tk

class LoadingAnimation:
    def __init__(self, master):
        self.master = master
        self.label = tk.Label(master, text="Loading .", fg='black', bg='white', font=('Arial', 12))
        self.label.place(relx=0.5, rely=0.5, anchor='center')  # Center the label
        self.running = False

    def animate(self):
        if self.running:
            current_text = self.label['text']
            if current_text == "Loading .":
                self.label['text'] = "Loading .."
            elif current_text == "Loading ..":
                self.label['text'] = "Loading ..."
            else:
                self.label['text'] = "Loading ."
            self.master.after(500, self.animate)

    def start(self):
        if not self.running:
            self.running = True
            self.label.place(relx=0.5, rely=0.5, anchor='center')  # Make the label visible
            self.master.after(100, lambda: self.label.lift())  # Lift the label after a short delay
            self.animate()

    def stop(self):
        self.running = False
        self.label.place_forget()  # Make the label invisible
