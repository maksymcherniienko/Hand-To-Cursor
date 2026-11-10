from src.gui import CameraSetupApp

def main():
    app = CameraSetupApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

if __name__ == "__main__":
    main()