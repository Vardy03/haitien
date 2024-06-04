import os
import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

tasks = []

def load_tasks():
    if os.path.exists("tasks.json"):
        with open("tasks.json","r") as file:
            return json.load(file)
    return []

def save_tasks():
    with open("tasks.json","w") as file:
        json.dump(tasks, file)

def add_task():
    task = input("Entrez une nouvelle tache: ")
    due_date = input("Entrez la date limite (YYY-MM-DD): ")
    priority = input("Entrez une priorite (eleve, moyen, faible): ")
    try:
        due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        tasks.append({"task": task, "due_date": str(due_date), "priority": priority, "completed": False})
        save_tasks()
        print("Tache ajoutee.")
    except ValueError:
        print("Format de la date invalide. Tache non ajoutee.")

def view_tasks():
    if not tasks:
        print("Aucune tache a afficher.")
    else:
        for i, task in enumerate(tasks, 1):
            status = "Terminee" if task["completed"] else "A faire"
            print(f"{i}. {task['task']} (A faire avant le {task['due_date']}, Priorite: {task['priority']}) - [{status}]")

def complete_task():
    view_tasks()
    task_num = int(input("entrez le numero de la tache terminee: "))
    if 0 < task_num <= len(tasks):
        tasks[task_num - 1]["completed"] = True
        save_tasks()
        print("Tache marquee comme terminee.")
    else:
        print("Numero de tache invalide.")

def delete_task():
    view_tasks()
    task_num = int(input("Entrez le numero de la tache a supprimer: "))
    if 0 < task_num <= len(tasks):
        tasks.pop(task_num - 1)
        save_tasks()
        print("Tache supprimee.")
    else:
        print("Numero de tache invalide.")

def sort_task():
    sorted_tasks = sorted(tasks, key=lambda x: (x["priority"], x["due_date"]))
    for i, task in enumerate(sorted_tasks, 1):
        status = "Terminee" if task["completed"] else "A faire"
        print(f"{i}. {task['task']} (A faire avant le {task['due_date']}, Priorite: {task['priority']}) - [{status}]")

def search_task():
    keyword = input("Entrez un mot-cle pour rechercher une tache: ")
    for i, task in enumerate(tasks, 1):
        if keyword.lower() in task["task"].lower():
            status = "Terminee" if task["completed"] else "A faire"
            print(f"{i}. {task['task']} (A faire avant le {task['due_date']}, Priorite: {task['priority']}) - [{status}]")

def add_task_gui():
    def add_task():
        task_text = task_entry.get()
        due_date = due_date_entry.get()
        priority = priority_var.get()
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
            if task_text:
                tasks.append({"task": task_text, "due_date": str(due_date), "priority": priority, "completed": False})
                save_tasks()
                task_entry.delete(0, tk.END)
                update_tasks()
            else:
                messagebox.showwarning("Format de date invalide", "La date doit etre au format YYY-MM-DD.")
        except ValueError:
            messagebox.showwarning("Format de date invalide", "La date doit etre au format YYY-MM-DD.")
    
    root = tk.Tk()
    root.title("Gestionaire de taches")

    tk.Label(root, text="Tache:").pack()
    task_entry = tk.Entry(root)
    task_entry.pack()

    tk.Label(root, text="Date limite (YYY-MM-DD):").pack()
    due_date_entry = tk.Entry(root)
    due_date_entry.pack()

    priority_var = tk.StringVar(value="moyen")
    tk.Radiobutton(root, text="Eleve", variable=priority_var, value="eleve").pack(anchor=tk.W)
    tk.Radiobutton(root, text="Moyen", variable=priority_var, value="moyen").pack(anchor=tk.W)
    tk.Radiobutton(root, text="Faible", variable=priority_var, value="faible").pack(anchor=tk.W)

    add_button = tk.Button(root, text="Ajouter tache", command=add_task)
    add_button.pack()
                
    task_list = tk.Listbox(root, width=80)
    task_list.pack()
    update_tasks()

    root.mainloop()

def update_tasks():
    tasks_list.delete(0, tk.END)
    for task in tasks:
        status = "Terminee" if task["completed"] else "A faire"
        tasks_list.insert(tk.END, f"{task['task']} (A faire avant le {task['due_date']}, Priorite: {task['priority']}) - [{status}]")

def main():
    global tasks
    tasks = load_tasks()
    while True:
        print("\nGestionnaire de Tache")
        print("1. Ajouter une tache")
        print("2. Afficher les taches")
        print("3. Marquer une tache comme terminee")
        print("4. Supprimer une tache")
        print("5. Trier les taches")
        print("6. Rechercher une tache")
        print("7. Interface graphique")
        print("8. Quitter")
        choice = input("Choisissez une option: ")
        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            complete_task()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            sort_task()
        elif choice == '6':
            search_task()
        elif choice == '7':
            add_task_gui()
        elif choice == '8':
            break
        else:
            print("Choix invalide, veuillez reessayer.")

if __name__=="__main__":
    main()