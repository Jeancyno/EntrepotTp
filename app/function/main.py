from ui import setup_ui
from detection import actualiser

if __name__ == "__main__":
    root, update_callback = setup_ui(actualiser)
    update_callback()
    root.mainloop()
