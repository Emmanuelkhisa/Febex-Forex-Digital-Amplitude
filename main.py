from modules.data_input import input_block
from modules.plotting import plot_session
from modules.utils import ensure_data_file

if __name__ == "__main__":
    ensure_data_file()

    while True:
        print("\n--- FEBEX HYBRID DIGITAL AMPLITUDE ---")
        print("1. Input Data Block")
        print("2. View Amplitude Chart")
        print("3. Exit")

        c = input("Choose: ")

        if c == "1":
            input_block()
        elif c == "2":
            plot_session()
        elif c == "3":
            break
        else:
            print("Invalid choice.")
