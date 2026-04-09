import os
import json
import datetime

# ── CONFIG ───────────────────────────────────────────
WIDTH = 80
DATA_FILE = "notes.json"

# ── UI COLORS ────────────────────────────────────────
RESET = "\033[0m"
BOLD  = "\033[1m"
DIM   = "\033[2m"
CYAN  = "\033[96m"
GREEN = "\033[92m"
YELLOW= "\033[93m"
RED   = "\033[91m"

# ── UI HELPERS ───────────────────────────────────────
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def truncate(text, length):
    return text if len(text) <= length else text[:length-3] + "..."

def header(title):
    print(f"\n{BOLD}{CYAN}{'═'*WIDTH}{RESET}")
    print(f"{BOLD}{CYAN}{title.center(WIDTH)}{RESET}")
    print(f"{BOLD}{CYAN}{'═'*WIDTH}{RESET}")

def footer(msg=""):
    print(f"{DIM}{'─'*WIDTH}{RESET}")
    if msg:
        print(f"{DIM}{msg.center(WIDTH)}{RESET}")

# ── NOTE MODEL ───────────────────────────────────────
class Note:
    def __init__(self, nid, title, content, tag, priority, created=None):
        self.id = nid
        self.title = title
        self.content = content
        self.tag = tag.lower()
        self.priority = priority
        self.created = created or datetime.datetime.now()

    def show(self):
        clear()
        header(f"NOTE #{self.id}")
        print(f"{BOLD}{self.title}{RESET}")
        print(f"{CYAN}[{self.tag}]{RESET}  {YELLOW}{'★'*self.priority}{RESET}")
        print(f"{DIM}{self.created.strftime('%Y-%m-%d %H:%M')}{RESET}")
        print(f"{DIM}{'─'*WIDTH}{RESET}")
        print(self.content)
        footer("Press Enter to go back")
        input()

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "tag": self.tag,
            "priority": self.priority,
            "created": self.created.isoformat()
        }

    @staticmethod
    def deserialize(data):
        return Note(
            data["id"],
            data["title"],
            data["content"],
            data["tag"],
            data["priority"],
            datetime.datetime.fromisoformat(data["created"])
        )

# ── STACK (UNDO) ─────────────────────────────────────
class Stack:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)

    def pop(self):
        return self.data.pop() if self.data else None

# ── STORE ────────────────────────────────────────────
class Store:
    def __init__(self):
        self.notes = []
        self.undo = Stack()
        self.next_id = 1
        self.load()

    def add(self, title, content, tag, priority):
        note = Note(self.next_id, title, content, tag, priority)
        self.notes.append(note)
        self.undo.push(("add", note.id))
        self.next_id += 1
        self.save()
        return note

    def delete(self, nid):
        note = self.find_by_id(nid)
        if not note:
            return False
        self.notes.remove(note)
        self.undo.push(("del", note))
        self.save()
        return True

    def find_by_id(self, nid):
        for note in self.notes:
            if note.id == nid:
                return note
        return None

    def undo_last(self):
        action = self.undo.pop()
        if not action:
            return "Nothing to undo"

        t, value = action

        if t == "add":
            note = self.find_by_id(value)
            if note:
                self.notes.remove(note)
            self.save()
            return f"Removed #{value}"

        if t == "del":
            self.notes.append(value)
            self.save()
            return f"Restored '{value.title}'"

    def save(self):
        with open(DATA_FILE, "w") as f:
            json.dump([n.serialize() for n in self.notes], f, indent=2)

    def load(self):
        if not os.path.exists(DATA_FILE):
            return

        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        for item in data:
            note = Note.deserialize(item)
            self.notes.append(note)

        if self.notes:
            self.next_id = max(n.id for n in self.notes) + 1

# ── ALGORITHMS ───────────────────────────────────────
def quick_sort(notes):
    if len(notes) <= 1:
        return notes

    pivot = notes[len(notes)//2].title.lower()

    left  = [n for n in notes if n.title.lower() < pivot]
    mid   = [n for n in notes if n.title.lower() == pivot]
    right = [n for n in notes if n.title.lower() > pivot]

    return quick_sort(left) + mid + quick_sort(right)

def sort_notes(notes, mode):
    if mode == "p":
        return sorted(notes, key=lambda x: -x.priority)
    if mode == "d":
        return sorted(notes, key=lambda x: x.created, reverse=True)
    return quick_sort(notes)

def search(notes, keyword):
    keyword = keyword.lower()
    results = []

    for note in notes:
        if keyword in note.title.lower() or keyword in note.tag:
            results.append(note)

    return results

# ── TABLE VIEW ───────────────────────────────────────
def render_table(notes):
    print(f"{BOLD}ID   Title                Tag        Priority  Date{RESET}")
    print(f"{DIM}{'─'*WIDTH}{RESET}")

    for n in notes:
        print(
            f"{BOLD}#{n.id:<3}{RESET} "
            f"{truncate(n.title,20):<20} "
            f"{CYAN}{truncate(n.tag,10):<10}{RESET} "
            f"{YELLOW}{'★'*n.priority:<8}{RESET} "
            f"{DIM}{n.created.strftime('%Y-%m-%d')}{RESET}"
        )

# ── INPUT HELPERS ────────────────────────────────────
def get_priority():
    try:
        value = int(input("Priority (1-5): ") or 1)
        return max(1, min(5, value))
    except:
        return 1

# ── MENU ─────────────────────────────────────────────
def main_menu(count):
    clear()
    header("📝 NOTES SYSTEM 📝")
    print(f"{DIM}{f'Total Notes: {count}'.center(WIDTH)}{RESET}\n")

    print(f"{CYAN}[1]{RESET} List Notes")
    print(f"{CYAN}[2]{RESET} Add Note")
    print(f"{CYAN}[3]{RESET} Delete Note")
    print(f"{CYAN}[4]{RESET} Search Notes")
    print(f"{CYAN}[5]{RESET} Undo Last Action")
    print(f"{CYAN}[0]{RESET} Exit\n")

    footer("Select option")

# ── MAIN LOOP ────────────────────────────────────────
def main():
    store = Store()

    while True:
        main_menu(len(store.notes))
        choice = input("> ").strip()

        if choice == "1":
            clear()
            mode = input("Sort (t/p/d): ") or "t"
            header(f"LIST VIEW | sort={mode}")

            if not store.notes:
                print(f"{DIM}No notes available{RESET}")
            else:
                render_table(sort_notes(store.notes, mode))

            input("\nPress Enter...")

        elif choice == "2":
            clear()
            header("ADD NOTE")

            title = input("Title: ")
            if not title:
                continue

            note = store.add(
                title,
                input("Content: "),
                input("Tag: ") or "gen",
                get_priority()
            )

            print(f"{GREEN}Added #{note.id}{RESET}")
            input()

        elif choice == "3":
            try:
                nid = int(input("ID: "))
                msg = "Deleted" if store.delete(nid) else "Not found"
                print(f"{GREEN if msg=='Deleted' else RED}{msg}{RESET}")
            except:
                print(f"{RED}Invalid input{RESET}")
            input()

        elif choice == "4":
            clear()
            header("SEARCH")

            results = search(store.notes, input("Keyword: "))
            render_table(results)
            print(f"\n{DIM}{len(results)} result(s){RESET}")
            input()

        elif choice == "5":
            print(store.undo_last())
            input()

        elif choice == "0":
            break

if __name__ == "__main__":
    main()
