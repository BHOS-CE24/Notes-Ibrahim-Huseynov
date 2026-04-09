# 📝 Notes System (CLI)

A terminal-based note-taking application built in Python, designed to demonstrate core Data Structures and Algorithms (DSA) concepts in a practical, usable way.

---

## 🚀 Features

### Create & Delete
- Add notes with title, content, tag, priority, and timestamp
- Delete notes instantly
- Undo protection prevents accidental data loss

### Search & Filter
- Search notes by title or tag using **linear search**
- Sort notes by:
  - Title (Quick Sort)
  - Priority
  - Date

### Undo System
- Stack-based undo (LIFO)
- Reverses last add/delete operation safely

### Persistent Storage
- Notes are saved to a JSON file
- Automatically reloads data on restart

---

## 🧠 Data Structures & Algorithms Used

| Feature        | Implementation        | Complexity |
|----------------|---------------------|-----------|
| Storage        | List                | O(n) space |
| Undo           | Stack              | O(1) push/pop |
| Search         | Linear Search      | O(n) |
| Sorting        | Quick Sort         | O(n log n) avg |
| Delete         | List remove        | O(n) |

---

## 🖥️ UI Preview

- Terminal-based interface with:
  - Structured layout (headers, tables)
  - Color-coded output
  - Clean note display with truncation

---
