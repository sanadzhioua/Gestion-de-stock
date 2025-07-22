import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
STOCK_FILE = 'stock.csv'
SORTIES_FILE = 'sorties.csv'

def charger_stock():
    stock = {}
    try:
        with open(STOCK_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                stock[row['code_article']] = {
                    'nom_article': row['nom_article'],
                    'quantite': int(row['quantite'])
                }
    except FileNotFoundError:
        with open(STOCK_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['code_article', 'nom_article', 'quantite'])
            writer.writeheader()
    return stock

def sauvegarder_stock(stock):
    with open(STOCK_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['code_article', 'nom_article', 'quantite'])
        writer.writeheader()
        for code, data in stock.items():
            writer.writerow({
                'code_article': code,
                'nom_article': data['nom_article'],
                'quantite': data['quantite']
            })

def ajouter_article():
    code = code_entry.get()
    nom = nom_entry.get()
    try:
        quantite = int(qte_entry.get())
    except ValueError:
        messagebox.showerror("Erreur", "Quantité invalide.")
        return

    if not code or not nom:
        messagebox.showwarning("Champs manquants", "Remplissez tous les champs.")
        return

    stock = charger_stock()
    if code in stock:
        messagebox.showinfo("Info", "Article déjà existant.")
    else:
        stock[code] = {'nom_article': nom, 'quantite': quantite}
        sauvegarder_stock(stock)
        messagebox.showinfo("Succès", "Article ajouté.")
    afficher_stock()

def modifier_quantite():
    code = code_entry.get()
    try:
        quantite = int(qte_entry.get())
    except ValueError:
        messagebox.showerror("Erreur", "Quantité invalide.")
        return

    stock = charger_stock()
    if code in stock:
        stock[code]['quantite'] = quantite
        sauvegarder_stock(stock)
        messagebox.showinfo("Succès", "Quantité modifiée.")
    else:
        messagebox.showerror("Erreur", "Article non trouvé.")
    afficher_stock()

def effectuer_sortie():
    code = sortie_code_entry.get()
    date = sortie_date_entry.get()
    heure = sortie_heure_entry.get()
    preleve_par = sortie_nom_entry.get()
    destination = sortie_dest_entry.get()

    try:
        quantite_sortie = int(sortie_qte_entry.get())
    except ValueError:
        messagebox.showerror("Erreur", "Quantité invalide.")
        return

    stock = charger_stock()
    if code not in stock:
        messagebox.showerror("Erreur", "Article introuvable.")
        return

    if stock[code]['quantite'] < quantite_sortie:
        messagebox.showerror("Erreur", "Stock insuffisant.")
        return

    stock[code]['quantite'] -= quantite_sortie
    sauvegarder_stock(stock)

    with open(SORTIES_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['date', 'heure', 'code_article', 'nom_article', 'quantite_sortie', 'preleve_par', 'destination'])
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow({
            'date': date,
            'heure': heure,
            'code_article': code,
            'nom_article': stock[code]['nom_article'],
            'quantite_sortie': quantite_sortie,
            'preleve_par': preleve_par,
            'destination': destination
        })

    messagebox.showinfo("Succès", "Sortie enregistrée.")
    afficher_stock()

def afficher_stock():
    stock = charger_stock()
    stock_text.delete('1.0', tk.END)
    for code, data in stock.items():
        stock_text.insert(tk.END, f"{code} - {data['nom_article']} : {data['quantite']}\n")

# Interface
root = tk.Tk()
root.title("La 6éme etoile")

# Partie 1 : Ajout / Modification
tk.Label(root, text="--- Gestion du Stock ---").pack()

tk.Label(root, text="Code Article").pack()
code_entry = tk.Entry(root)
code_entry.pack()

tk.Label(root, text="Nom Article").pack()
nom_entry = tk.Entry(root)
nom_entry.pack()

tk.Label(root, text="Quantité").pack()
qte_entry = tk.Entry(root)
qte_entry.pack()

tk.Button(root, text="Ajouter Article", command=ajouter_article).pack()
tk.Button(root, text="Modifier Quantité", command=modifier_quantite).pack()

# Partie 2 : Sortie
tk.Label(root, text="--- Sortie d'Article ---").pack()

tk.Label(root, text="Date (ex: 04/06/2025)").pack()
sortie_date_entry = tk.Entry(root)
sortie_date_entry.pack()

tk.Label(root, text="Heure (ex: 14:30)").pack()
sortie_heure_entry = tk.Entry(root)
sortie_heure_entry.pack()

tk.Label(root, text="Code Article").pack()
sortie_code_entry = tk.Entry(root)
sortie_code_entry.pack()

tk.Label(root, text="Quantité Sortie").pack()
sortie_qte_entry = tk.Entry(root)
sortie_qte_entry.pack()

tk.Label(root, text="Prélevé par").pack()
sortie_nom_entry = tk.Entry(root)
sortie_nom_entry.pack()

tk.Label(root, text="Destination").pack()
sortie_dest_entry = tk.Entry(root)
sortie_dest_entry.pack()

tk.Button(root, text="Effectuer Sortie", command=effectuer_sortie).pack()

# Affichage du stock
tk.Label(root, text="--- État du Stock ---").pack()
stock_text = tk.Text(root, height=10)
stock_text.pack()

afficher_stock()

root.mainloop()

