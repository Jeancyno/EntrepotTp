import asyncio
import threading

# from ui import setup_ui
from detection import actualiser
from window import Window



def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    threading.Thread(target=start_loop, args=(loop,), daemon=True).start()

    win = Window(loop, 500) 
    win.setActualizer(actualiser)
    # .appExec()
    win.updateAfter()
    win.mainLoop()
    # root, update_callback = setup_ui(actualiser)
    # update_callback()
    # root.mainloop()
