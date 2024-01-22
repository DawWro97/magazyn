import openpyxl
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox, filedialog
import hashlib
import datetime
import mysql.connector


###################################### Wyświetlanie ekranów #####################################################


# Ekran administratora
def wyswietl_ekran_logowania():
    # Funkcja do utworzenia skrótu hasła
    def utworz_skrot_hasla(haslo):
        skrot = hashlib.sha256(haslo.encode()).hexdigest()
        return skrot

    logged_in_user = ""
    user_id = ""

    def set_logged_in_user(username):
        global logged_in_user
        logged_in_user = username

    def set_user_id(id):
        global user_id
        user_id = id

    # Funkcja do sprawdzania danych logowania
    def sprawdz_logowanie():
        email = email_entry.get()
        haslo = haslo_entry.get()

        conn = mysql.connector.connect(
            host="db4free.net",
            user="magazyn",
            password="Inzynierka",
            database="magazyn_pd"
        )
        cursor = conn.cursor()

        # Wykonaj zapytanie SQL, aby pobrać użytkownika o określonym adresie e-mail
        cursor.execute('SELECT * FROM uzytkownicy WHERE email=%s', (email,))

        # Pobierz jednego użytkownika (jeśli istnieje)
        uzytkownik = cursor.fetchone()

        if uzytkownik:
            haslo_w_bazie = uzytkownik[5]
            haslo_skrot = utworz_skrot_hasla(haslo)
            if haslo_w_bazie == haslo_skrot:
                imie = uzytkownik[1]
                nazwisko = uzytkownik[2]
                rola = uzytkownik[3]
                u_id = uzytkownik[6]

                # Połącz imię i nazwisko w jedną zmienną
                full_name = f"{imie} {nazwisko}"

                # Ustaw nazwę zalogowanego użytkownika
                set_logged_in_user(full_name)
                set_user_id(u_id)

                if rola == "admin":
                    root.destroy()
                    wyswietl_ekran_admina()
                elif rola == "pracownik":
                    root.destroy()
                    wyswietl_ekran_pracownika()
                elif rola == "magazyn":
                    root.destroy()
                    wyswietl_ekran_magazynu()
            else:
                wynik_label.config(text="Błąd logowania")
        else:
            wynik_label.config(text="Błąd logowania")

    # Inicjalizacja okna
    root = ThemedTk(theme="arc")
    root.title("Logowanie")

    # Dodanie ramki dla estetyki
    frame = ttk.Frame(root, padding=(30, 30, 30, 30))
    frame.grid(row=0, column=0, sticky="nsew")

    # Etykiety i pola tekstowe dla emaila i hasła
    email_label = ttk.Label(frame, text="Email:")
    email_label.grid(row=0, column=0, sticky="w", pady=(20, 5))
    email_entry = ttk.Entry(frame, width=50, font=('Arial', 12), justify='left')
    email_entry.grid(row=0, column=1, padx=5, pady=(20, 5), ipady=10)

    haslo_label = ttk.Label(frame, text="Hasło:")
    haslo_label.grid(row=1, column=0, sticky="w", pady=(5, 10))
    haslo_entry = ttk.Entry(frame, show="*", width=50, font=('Arial', 12), justify='left')
    haslo_entry.grid(row=1, column=1, padx=5, pady=(5, 10), ipady=10)

    # Przycisk do logowania
    login_button = ttk.Button(frame, text="Zaloguj", command=sprawdz_logowanie)
    login_button.grid(row=2, column=0, columnspan=2, pady=(20, 15), ipadx=20, ipady=10)

    # Etykieta do wyświetlania komunikatów o błędach
    wynik_label = ttk.Label(frame, text="", foreground="red")
    wynik_label.grid(row=3, column=0, columnspan=2, pady=(15, 20))

    # Uruchomienie pętli głównej
    root.mainloop()


def wyswietl_ekran_admina():
    global users_tree

    root = ThemedTk(theme="arc")
    root.title("Ekran Admina")

    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid(row=0, column=20, sticky="nsew")
    logged_in_label = ttk.Label(main_frame, text=f"Jesteś zalogowany jako: {logged_in_user}")
    logged_in_label.grid(row=1, column=0, pady=(0, 10), padx=(20, 0), sticky="ew")
    # Dodaj przycisk "Wyloguj"
    logout_button = ttk.Button(main_frame, text="Wyloguj", command=lambda: on_close(root), width=15)
    logout_button.grid(row=1, column=19, pady=(0, 10), padx=(0, 20), sticky="e", ipadx=10, ipady=5)
    # Dodaj przycisk "Zmień hasło"
    change_password_button = ttk.Button(main_frame, text="Zmień hasło", command=zmien_haslo, width=15)
    change_password_button.grid(row=1, column=18, pady=(0, 10), sticky="e", ipadx=10, ipady=5)
    # Frame dla widoku użytkowników
    users_frame = ttk.Frame(main_frame, padding=10)
    users_frame.grid(row=0, column=0, columnspan=20, padx=10, pady=10, sticky="nsew")

    users_button = ttk.Button(users_frame, text="Pokaż użytkowników", command=populate_tree3)
    users_button.grid(row=0, column=0, pady=(0, 10), sticky="ew", ipadx=20, ipady=10)

    users_tree = ttk.Treeview(users_frame)
    users_tree["columns"] = ("ID", "Imie", "Nazwisko", "Rola", "Email", "Haslo", "Identyfikator")
    users_tree.heading("ID", text="ID", anchor='center')
    users_tree.heading("Imie", text="Imie", anchor='center')
    users_tree.heading("Nazwisko", text="Nazwisko", anchor='center')
    users_tree.heading("Rola", text="Rola", anchor='center')
    users_tree.heading("Email", text="Email", anchor='center')
    users_tree.heading("Haslo", text="Haslo", anchor='center')
    users_tree.heading("Identyfikator", text="Identyfikator", anchor='center')

    users_tree.column("#0", width=0, minwidth=0, stretch=tk.NO)
    users_tree.column("ID", width=150, stretch=False)
    users_tree.column("Imie", width=150)
    users_tree.column("Nazwisko", width=150)
    users_tree.column("Rola", width=150)
    users_tree.column("Email", width=150)
    users_tree.column("Haslo", width=150)
    users_tree.column("Identyfikator", width=150)
    users_tree.grid(row=2, column=0, pady=(0, 10), sticky="nsew")

    create_button = ttk.Button(users_frame, text="Utwórz użytkownika", command=utworz)
    create_button.grid(row=3, column=0, pady=(0, 10), sticky="ew")

    create_button = ttk.Button(users_frame, text="Edytuj użytkownika", command=edytuj)
    create_button.grid(row=4, column=0, pady=(0, 10), sticky="ew")

    root.mainloop()


# Ekran pracownika

def wyswietl_ekran_pracownika():
    global tree
    global order_tree
    global order__tree
    global root

    root = ThemedTk(theme="arc")
    root.title("Magazyn")

    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid(row=0, column=20, sticky="nsew")
    logged_in_label = ttk.Label(main_frame, text=f"Jesteś zalogowany jako: {logged_in_user}")
    logged_in_label.grid(row=1, column=0, pady=(0, 10), padx=(20, 0), sticky="ew")
    # Dodaj przycisk "Wyloguj"
    logout_button = ttk.Button(main_frame, text="Wyloguj", command=lambda: on_close(root), width=15)
    logout_button.grid(row=1, column=19, pady=(0, 10), padx=(0, 20), sticky="e", ipadx=10, ipady=5)
    # Dodaj przycisk "Zmień hasło"
    change_password_button = ttk.Button(main_frame, text="Zmień hasło", command=zmien_haslo, width=15)
    change_password_button.grid(row=1, column=18, pady=(0, 10), sticky="e", ipadx=10, ipady=5)

    # Frame dla widoku magazynu
    inventory_frame = ttk.Frame(main_frame, padding=10)
    inventory_frame.grid(row=0, column=0, columnspan=10, padx=10, pady=10, sticky="nsew")

    data_entry_button = ttk.Button(inventory_frame, text="Pokaż stan magazynowy", command=populate_tree)
    data_entry_button.grid(row=0, column=0, pady=(0, 10), sticky="ew")

    tree = ttk.Treeview(inventory_frame)
    tree["columns"] = ("ID", "Nazwa", "Ilosc")
    tree.heading("ID", text="ID", anchor='center', command=lambda: sort_treeview(tree, "ID", False))
    tree.heading("Nazwa", text="Nazwa", anchor='center', command=lambda: sort_treeview2(tree, "Nazwa", False))
    tree.heading("Ilosc", text="Ilość", anchor='center', command=lambda: sort_treeview(tree, "Ilosc", False))
    tree.column("#0", width=0, minwidth=0, stretch=tk.NO)
    tree.column("ID", width=150, stretch=False)
    tree.column("Nazwa", width=150)
    tree.column("Ilosc", width=150)
    tree.grid(row=2, column=0, pady=(0, 10), sticky="nsew")

    add_to_order_button = ttk.Button(inventory_frame, text="Dodaj do zlecenia", command=add_to_order)
    add_to_order_button.grid(row=3, column=0, pady=(0, 10), sticky="ew", ipadx=20, ipady=10)

    # Frame dla zleceń
    order_frame = ttk.Frame(main_frame, padding=10)
    order_frame.grid(row=0, column=10, columnspan=10, padx=10, pady=10, sticky="nsew")

    button = ttk.Button(inventory_frame, text="Wyszukaj", command=wyszukaj)
    button.grid(row=1, column=0, pady=(0, 10), sticky="ew")

    order_tree = ttk.Treeview(order_frame)
    order_tree["columns"] = ("ID", "Nazwa", "Ilosc", "Numer")
    order_tree.heading("ID", text="ID", anchor='center')
    order_tree.heading("Nazwa", text="Nazwa", anchor='center')
    order_tree.heading("Ilosc", text="Ilość", anchor='center')
    order_tree.heading("Numer", text="Numer Zlecenia", anchor='center')
    order_tree.column("#0", width=0, minwidth=0, stretch=tk.NO)
    order_tree.column("ID", width=100, stretch=False)
    order_tree.column("Nazwa", width=150)
    order_tree.column("Ilosc", width=100)
    order_tree.column("Numer", width=100, stretch=False)
    order_tree.grid(row=1, column=0, pady=(0, 10), columnspan=2, sticky="nsew")

    remove_from_order_button = ttk.Button(order_frame, text="Usuń zaznaczony", command=remove_from_order)
    remove_from_order_button.grid(row=2, column=0, pady=(0, 10), sticky="ew", columnspan=2)

    clear_order_button = ttk.Button(order_frame, text="Wyczyść listę", command=czyszczenie_okna_bez_wyslania)
    clear_order_button.grid(row=3, column=0, pady=(0, 10), columnspan=2, sticky="ew")

    save_to_db_button = ttk.Button(order_frame, text="Wyślij zlecenie", command=save_to_database)
    save_to_db_button.grid(row=4, column=0, pady=(0, 10), columnspan=2, sticky="ew", ipadx=20, ipady=10)

    root.mainloop()


# Ekran magazyniera

def wyswietl_ekran_magazynu():
    global tree
    global order_tree
    global order__tree
    global root

    root = ThemedTk(theme="arc")
    root.title("Magazyn")

    main_frame = ttk.Frame(root, padding=10)
    main_frame.grid(row=0, column=20, sticky="nsew")
    logged_in_label = ttk.Label(main_frame, text=f"Jesteś zalogowany jako: {logged_in_user}")
    logged_in_label.grid(row=1, column=0, pady=(0, 10), padx=(20, 0), sticky="ew")
    # Dodaj przycisk "Wyloguj"
    logout_button = ttk.Button(main_frame, text="Wyloguj", command=lambda: on_close(root), width=15)
    logout_button.grid(row=1, column=19, pady=(0, 10), padx=(0, 20), sticky="e", ipadx=10, ipady=5)
    # Dodaj przycisk "Zmień hasło"
    change_password_button = ttk.Button(main_frame, text="Zmień hasło", command=zmien_haslo, width=15)
    change_password_button.grid(row=1, column=18, pady=(0, 10), sticky="e", ipadx=10, ipady=5)

    # Frame dla zleceń
    order_frame = ttk.Frame(main_frame, padding=10)
    order_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    empty_row = ttk.Label(order_frame, text="")
    empty_row.grid(row=0, column=0, pady=(0, 40))

    data_add_button = ttk.Button(order_frame, text="Dodaj produkt", command=dodaj_do_bazy)
    data_add_button.grid(row=1, column=0, pady=(0, 10), sticky="ew")

    button = ttk.Button(order_frame, text="Usuń zaznaczony", command=usun_zaznaczony_element)
    button.grid(row=2, column=0, pady=(0, 10), sticky="ew")

    button = ttk.Button(order_frame, text="Zwiększ ilość", command=zwieksz_ilosc)
    button.grid(row=3, column=0, pady=(0, 10), sticky="ew")

    button = ttk.Button(order_frame, text="Zmniejsz ilość", command=zmniejsz_ilosc)
    button.grid(row=4, column=0, pady=(0, 10), sticky="ew")

    button = ttk.Button(order_frame, text="Wyszukaj", command=wyszukaj)
    button.grid(row=5, column=0, pady=(0, 10), sticky="ew")

    button = ttk.Button(order_frame, text="Wygeneruj excel", command=wygeneruj_excel)
    button.grid(row=6, column=0, pady=(0, 10), sticky="ew")

    button = ttk.Button(order_frame, text="Przyjęcie produktów", command=przyjmij)
    button.grid(row=7, column=0, pady=(0, 10), sticky="ew")

    button = ttk.Button(order_frame, text="Historia przyjęć", command=wyswietl_historie)
    button.grid(row=8, column=0, pady=(0, 10), sticky="ew")

    # Frame dla widoku magazynu
    inventory_frame = ttk.Frame(main_frame, padding=10)
    inventory_frame.grid(row=0, column=2, columnspan=8, padx=10, pady=10, sticky="nsew")

    data_entry_button = ttk.Button(inventory_frame, text="Pokaż stan magazynowy", command=populate_tree)
    data_entry_button.grid(row=0, column=1, pady=(0, 10), sticky="ew")

    tree = ttk.Treeview(inventory_frame)
    tree["columns"] = ("ID", "Nazwa", "Ilosc")
    tree.heading("ID", text="ID", anchor='center', command=lambda: sort_treeview(tree, "ID", False))
    tree.heading("Nazwa", text="Nazwa", anchor='center', command=lambda: sort_treeview2(tree, "Nazwa", False))
    tree.heading("Ilosc", text="Ilość", anchor='center', command=lambda: sort_treeview(tree, "Ilosc", False))
    tree.column("#0", width=0, minwidth=0, stretch=tk.NO)
    tree.column("ID", width=150, stretch=False)
    tree.column("Nazwa", width=150)
    tree.column("Ilosc", width=150)
    tree.grid(row=1, column=1, pady=(0, 10), sticky="nsew")

    add_to_order_button = ttk.Button(inventory_frame, text="Dodaj do zlecenia", command=add_to_order)
    add_to_order_button.grid(row=2, column=1, pady=(0, 10), sticky="ew", ipadx=20, ipady=10)

    order_tree = ttk.Treeview(inventory_frame)
    order_tree["columns"] = ("ID", "Nazwa", "Ilosc", "Numer")
    order_tree.heading("ID", text="ID", anchor='center')
    order_tree.heading("Nazwa", text="Nazwa", anchor='center')
    order_tree.heading("Ilosc", text="Ilość", anchor='center')
    order_tree.heading("Numer", text="Numer Zlecenia", anchor='center')
    order_tree.column("#0", width=0, minwidth=0, stretch=tk.NO)
    order_tree.column("ID", width=100, stretch=False)
    order_tree.column("Nazwa", width=150)
    order_tree.column("Ilosc", width=100)
    order_tree.column("Numer", width=100, stretch=False)
    order_tree.grid(row=3, column=1, pady=(0, 10), columnspan=2, sticky="nsew")

    remove_from_order_button = ttk.Button(inventory_frame, text="Usuń zaznaczony", command=remove_from_order)
    remove_from_order_button.grid(row=4, column=1, pady=(0, 10), sticky="ew")

    clear_order_button = ttk.Button(inventory_frame, text="Wyczyść listę", command=czyszczenie_okna_bez_wyslania)
    clear_order_button.grid(row=5, column=1, pady=(0, 10), sticky="ew")

    save_to_db_button = ttk.Button(inventory_frame, text="Wyślij zlecenie", command=save_to_database)
    save_to_db_button.grid(row=6, column=1, pady=(0, 10), columnspan=2, sticky="ew", ipadx=20, ipady=10)

    # Frame dla zleceń
    order__frame = ttk.Frame(main_frame, padding=10)
    order__frame.grid(row=0, column=12, columnspan=8, padx=10, pady=10, sticky="nsew")

    data_entry_button = ttk.Button(order__frame, text="Pokaż zamówienia", command=populate_order_tree)
    data_entry_button.grid(row=0, column=0, pady=(0, 10), columnspan=2, sticky="ew")

    done_order_button = ttk.Button(order__frame, text="Zakończ zamówienie", command=remove_order_by_number)
    done_order_button.grid(row=2, column=0, pady=(0, 10), columnspan=2, sticky="ew", ipadx=20, ipady=10)

    done_order_button = ttk.Button(order__frame, text="Historia zamówień", command=historia)
    done_order_button.grid(row=3, column=0, pady=(0, 10), columnspan=2, sticky="ew")

    order__tree = ttk.Treeview(order__frame)
    order__tree["columns"] = (
    "ID", "Nazwa", "Ilosc", "Numer", "DataDodania", "Zamawiajacy")  # Dodaj kolumnę "DataDodania"
    order__tree.heading("ID", text="ID", anchor='center')
    order__tree.heading("Nazwa", text="Nazwa", anchor='center')
    order__tree.heading("Ilosc", text="Ilość", anchor='center')
    order__tree.heading("Numer", text="Numer", anchor='center')
    order__tree.heading("DataDodania", text="Data Dodania", anchor='center')  # Dodaj nagłówek dla kolumny daty
    order__tree.heading("Zamawiajacy", text="Zamawiajacy", anchor='center')  # Dodaj nagłówek dla kolumny daty

    order__tree.column("#0", width=0, minwidth=0, stretch=tk.NO)
    order__tree.column("ID", width=150, stretch=False)
    order__tree.column("Nazwa", width=150)
    order__tree.column("Ilosc", width=150)
    order__tree.column("Numer", width=150)
    order__tree.column("DataDodania", width=200)  # Dostosuj szerokość kolumny daty
    order__tree.column("Zamawiajacy", width=100)  # Dostosuj szerokość kolumny daty
    order__tree.grid(row=1, column=0, pady=(0, 10), columnspan=2, sticky="nsew")

    order__tree.heading("Numer", text="Numer", anchor='center',
                        command=lambda: sort_treeview(order__tree, "Numer", False))

    root.mainloop()


###################################### Pobieranie danych z bazy #####################################################

# Pobieranie zleceń z bazy danych i wyświetlanie

def data_entry2():
    def wyczysc_treeview2():
        for item in order__tree.get_children():
            order__tree.delete(item)

    wyczysc_treeview2()


def populate_order_tree():
    data_entry2()
    conn = mysql.connector.connect(
        host="db4free.net",
        user="magazyn",
        password="Inzynierka",
        database="magazyn_pd"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * from Zlecenie")
    rows = cursor.fetchall()
    for row in rows:
        order__tree.insert("", "end", values=row)
    conn.close()


# Pobieranie danych magazynowych z bazy danych i wyświetlanie

def data_entry():
    def wyczysc_treeview():
        for item in tree.get_children():
            tree.delete(item)

    wyczysc_treeview()


def populate_tree():
    data_entry()
    conn = mysql.connector.connect(
        host="db4free.net",
        user="magazyn",
        password="Inzynierka",
        database="magazyn_pd"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * from Magazyn")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)
    conn.close()


# Pobieranie użytkowników z bazy danych i wyświetlanie

def data_entry3():
    def wyczysc_treeview3():
        for item in users_tree.get_children():
            users_tree.delete(item)

    wyczysc_treeview3()


def populate_tree3():
    data_entry3()
    conn = mysql.connector.connect(
        host="db4free.net",
        user="magazyn",
        password="Inzynierka",
        database="magazyn_pd"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * from uzytkownicy")
    rows = cursor.fetchall()
    for row in rows:
        users_tree.insert("", "end", values=row)
    conn.close()


# Pobieranie historii z bazy danych i wyświetlanie

def data_entry4():
    def wyczysc_treeview4():
        for item in history_tree.get_children():
            history_tree.delete(item)

    wyczysc_treeview4()


def populate_tree4():
    data_entry4()
    conn = mysql.connector.connect(
        host="db4free.net",
        user="magazyn",
        password="Inzynierka",
        database="magazyn_pd"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * from Historia")
    rows = cursor.fetchall()
    for row in rows:
        history_tree.insert("", "end", values=row)
    conn.close()


def data_entry5():
    def wyczysc_treeview5():
        for item in history_receipt_tree.get_children():
            history_receipt_tree.delete(item)

    wyczysc_treeview5()


def populate_tree5():
    data_entry5()
    conn = mysql.connector.connect(
        host="db4free.net",
        user="magazyn",
        password="Inzynierka",
        database="magazyn_pd"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * from HistoriaPrzyjec")
    rows = cursor.fetchall()
    for row in rows:
        history_receipt_tree.insert("", "end", values=row)
    conn.close()


###################################### Podstawowe funkcjonalności magazynu #####################################################

# Usuwanie elementu ze stanu magazynowego

def usun_zaznaczony_element():
    # Pobierz zaznaczony element z widoku drzewa
    zaznaczone_elementy = tree.selection()
    if len(zaznaczone_elementy) == 0:
        # Jeśli nic nie jest zaznaczone, nie rób nic
        return

    # Pobierz identyfikator zaznaczonego elementu
    zaznaczony_element = zaznaczone_elementy[0]

    # Pobierz dane zaznaczonego elementu
    dane_zaznaczonego_elementu = tree.item(zaznaczony_element, 'values')

    # Pobierz identyfikator zaznaczonego elementu (na przykład w pierwszej kolumnie)
    id_elementu = dane_zaznaczonego_elementu[0]

    # Wyświetl pytanie o potwierdzenie przed usunięciem
    potwierdzenie = messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć ten element?")
    if potwierdzenie:
        # Usuń zaznaczony element z bazy danych
        usun_rekord(id_elementu)

        # Usuń zaznaczony element z widoku drzewa
        tree.delete(zaznaczony_element)


def usun_rekord(id):
    conn = mysql.connector.connect(
        host="db4free.net",
        user="magazyn",
        password="Inzynierka",
        database="magazyn_pd"
    )
    cursor = conn.cursor()

    # Wykonaj zapytanie SQL, aby usunąć rekord o określonym identyfikatorze
    cursor.execute("DELETE FROM Magazyn WHERE id=%s", (id,))

    conn.commit()
    conn.close()


# Wyszukiwanie elementu po ID

def wyszukaj():
    root = ThemedTk(theme="arc")
    root.title("Wyszukiwanie po ID")

    # Dodanie ramki dla estetyki
    frame = ttk.Frame(root, padding=(30, 30, 30, 30))
    frame.grid(row=0, column=0, sticky="nsew")

    # Etykieta i pole tekstowe do wprowadzania ID
    label5 = ttk.Label(frame, text="Wyszukaj po ID:")
    label5.grid(row=0, column=0, sticky="w", pady=(20, 5))

    entry5 = ttk.Entry(frame, width=50, font=('Arial', 12), justify='left')
    entry5.grid(row=0, column=1, padx=5, pady=(20, 5), ipady=10)  # Ustawienie ipady dla zwiększenia wysokości

    def wyszukaj_po_id():
        id_to_search = entry5.get()
        conn = mysql.connector.connect(
            host="db4free.net",
            user="magazyn",
            password="Inzynierka",
            database="magazyn_pd"
        )
        cursor = conn.cursor()

        # Wykonaj zapytanie SQL, aby znaleźć rekord na podstawie ID
        cursor.execute("SELECT * FROM Magazyn WHERE id=%s", (id_to_search,))
        result = cursor.fetchone()

        conn.close()

        if result is not None:
            # Wyczyść wcześniejsze wyniki w Treeview
            for item in tree.get_children():
                tree.delete(item)
            # Dodaj wynik do Treeview
            tree.insert("", "end", values=result)
        else:
            tk.messagebox.showinfo("Wynik wyszukiwania", "Brak rekordu o podanym ID.")

    # Przyciski dodane w nowym fragmencie kodu
    button2 = ttk.Button(frame, text="Wyszukaj po ID", command=wyszukaj_po_id)
    button2.grid(row=2, column=0, columnspan=2, pady=(20, 15), ipadx=20, ipady=10)

    data_entry_button = ttk.Button(frame, text="Pokaż wszystkie", command=populate_tree)
    data_entry_button.grid(row=3, column=0, columnspan=2, pady=(20, 15), ipadx=20, ipady=10)


# Dodawanie produktu do stanu magazynowego

def dodaj_do_bazy():
    root = ThemedTk(theme="arc")
    root.title("Dodawanie danych do bazy")

    frame = ttk.Frame(root, padding=(30, 30, 30, 30))
    frame.grid(row=0, column=0, sticky="nsew")

    label1 = ttk.Label(frame, text="ID:")
    label1.grid(row=0, column=0, sticky="w", pady=(20, 5))
    entry1 = ttk.Entry(frame, width=50, font=('Arial', 12), justify='left')
    entry1.grid(row=0, column=1, padx=5, pady=(20, 5), ipady=10)

    label2 = ttk.Label(frame, text="Nazwa:")
    label2.grid(row=1, column=0, sticky="w", pady=(5, 10))
    entry2 = ttk.Entry(frame, width=50, font=('Arial', 12), justify='left')
    entry2.grid(row=1, column=1, padx=5, pady=(5, 10), ipady=10)

    label3 = ttk.Label(frame, text="Ilość:")
    label3.grid(row=2, column=0, sticky="w", pady=(5, 10))
    entry3 = ttk.Entry(frame, width=50, font=('Arial', 12), justify='left')
    entry3.grid(row=2, column=1, padx=5, pady=(5, 10), ipady=10)

    wynik_label = ttk.Label(frame, text="", foreground="red")
    wynik_label.grid(row=4, column=0, columnspan=2, pady=(15, 20))

    def is_numeric(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def sprawdz_i_dodaj():
        id_value = entry1.get()
        nazwa_value = entry2.get()
        ilosc_value = entry3.get()

        if not is_numeric(id_value):
            tk.messagebox.showerror("Błąd", "Pole 'ID' musi zawierać wartość numeryczną.")
            return

        if not is_numeric(ilosc_value):
            tk.messagebox.showerror("Błąd", "Pole 'Ilość' musi zawierać wartość numeryczną.")
            return

        dane = (id_value, nazwa_value, ilosc_value)

        # Sprawdź, czy wartość w pierwszej kolumnie już istnieje
        if czy_wartosc_istnieje(id_value):
            tk.messagebox.showerror("Błąd", "Towar o podanym numerze magazynowym już istnieje.")
        else:
            # Wartość jest unikalna, dodaj do bazy danych
            dodaj_do_bazy2(dane)
            tk.messagebox.showinfo("Sukces", "Produkt został dodany.")

    def czy_wartosc_istnieje(wartosc):
        conn = mysql.connector.connect(
            host="db4free.net",
            user="magazyn",
            password="Inzynierka",
            database="magazyn_pd"
        )
        cursor = conn.cursor()
        # Wykonaj zapytanie SQL, aby sprawdzić, czy wartość już istnieje w pierwszej kolumnie
        cursor.execute("SELECT * FROM Magazyn WHERE id=%s", (wartosc,))
        result = cursor.fetchone()

        conn.close()

        return result is not None

    def dodaj_do_bazy2(dane):
        conn = mysql.connector.connect(
            host="db4free.net",
            user="magazyn",
            password="Inzynierka",
            database="magazyn_pd"
        )
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Magazyn VALUES (%s, %s, %s)", dane)

        conn.commit()
        conn.close()
        populate_tree()

    button = ttk.Button(frame, text="Dodaj do bazy", command=sprawdz_i_dodaj)
    button.grid(row=3, column=0, columnspan=2, pady=(20, 15), ipadx=20, ipady=10)


def przyjmij():
    def is_numeric(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def populate_receipt_tree():
        for child in receipt_tree.get_children():
            receipt_tree.delete(child)
        for item in temp_data:
            receipt_tree.insert("", "end", values=item)

    def add_to_temp_data():
        id_value = entry1.get()
        nazwa_value = entry2.get()
        ilosc_value = entry3.get()

        if not is_numeric(id_value) or not is_numeric(ilosc_value):
            messagebox.showerror("Błąd", "ID i Ilość muszą być wartościami numerycznymi.")
            return

        temp_data.append((id_value, nazwa_value, ilosc_value))
        populate_receipt_tree()
        entry1.delete(0, tk.END)
        entry2.delete(0, tk.END)
        entry3.delete(0, tk.END)

    def przyjmij():
        for item in temp_data:
            id_value, nazwa_value, ilosc_value = item

            conn = mysql.connector.connect(
                host="db4free.net",
                user="magazyn",
                password="Inzynierka",
                database="magazyn_pd"
            )
            cursor = conn.cursor()

            # Aktualizuj ilość w tabeli Magazyn
            cursor.execute("SELECT * FROM Magazyn WHERE id=%s", (id_value,))
            existing_row = cursor.fetchone()
            if existing_row:
                nowa_ilosc = int(existing_row[2]) + int(ilosc_value)
                cursor.execute("UPDATE Magazyn SET ilosc=%s WHERE id=%s", (nowa_ilosc, id_value))
            else:
                dane = (id_value, nazwa_value, ilosc_value)
                cursor.execute("INSERT INTO Magazyn VALUES (%s, %s, %s)", dane)

            # Dodaj do historii przyjęć w tabeli HistoriaPrzyjec
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Uzyskaj bieżącą datę i godzinę
            historia_dane = (id_value, nazwa_value, ilosc_value, current_datetime, user_id)
            cursor.execute("INSERT INTO HistoriaPrzyjec VALUES (%s, %s, %s, %s, %s)", historia_dane)

            conn.commit()
            conn.close()

        messagebox.showinfo("Sukces", "Wszystkie produkty zostały przyjęte.")
        temp_data.clear()
        populate_receipt_tree()

    def import_z_excel():
        file_path = filedialog.askopenfilename(filetypes=[("Pliki Excela", "*.xlsx;*.xls")])

        if not file_path:
            return

        try:
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active

            for row in sheet.iter_rows(min_row=2, values_only=True):
                id_value, nazwa_value, ilosc_value = map(str, row)

                if not is_numeric(id_value) or not is_numeric(ilosc_value):
                    messagebox.showerror("Błąd", "ID i Ilość muszą być wartościami numerycznymi.")
                    return

                temp_data.append((id_value, nazwa_value, ilosc_value))
            populate_receipt_tree()
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas importu z Excela:\n{str(e)}")

    def remove_selected_item():
        selected_item = receipt_tree.selection()
        if selected_item:
            for item in selected_item:
                values = receipt_tree.item(item, 'values')
                temp_data.remove(tuple(values))
                receipt_tree.delete(item)

    root = ThemedTk(theme="arc")
    root.title("Dodawanie danych do bazy")

    frame = ttk.Frame(root, padding=(30, 30, 30, 30))
    frame.grid(row=0, column=0, sticky="nsew")

    label1 = ttk.Label(frame, text="ID:")
    label1.grid(row=0, column=0, sticky="w", pady=(20, 5))
    entry1 = ttk.Entry(frame, width=50, font=('Arial', 12), justify='left')
    entry1.grid(row=0, column=1, padx=5, pady=(20, 5), ipady=10)

    label2 = ttk.Label(frame, text="Nazwa:")
    label2.grid(row=1, column=0, sticky="w", pady=(5, 10))
    entry2 = ttk.Entry(frame, width=50, font=('Arial', 12), justify='left')
    entry2.grid(row=1, column=1, padx=5, pady=(5, 10), ipady=10)

    label3 = ttk.Label(frame, text="Ilość:")
    label3.grid(row=2, column=0, sticky="w", pady=(5, 10))
    entry3 = ttk.Entry(frame, width=50, font=('Arial', 12), justify='left')
    entry3.grid(row=2, column=1, padx=5, pady=(5, 10), ipady=10)

    wynik_label = ttk.Label(frame, text="", foreground="red")
    wynik_label.grid(row=5, column=0, columnspan=2, pady=(15, 20))

    button_add = ttk.Button(frame, text="Dodaj do tymczasowego przyjęcia", command=add_to_temp_data)
    button_add.grid(row=3, column=0, columnspan=2, pady=(20, 15), ipadx=20, ipady=10)

    button_import = ttk.Button(frame, text="Import z Excela", command=import_z_excel)
    button_import.grid(row=4, column=0, columnspan=2, pady=(20, 15), ipadx=20, ipady=10)

    button_remove = ttk.Button(frame, text="Usuń zaznaczone", command=remove_selected_item)
    button_remove.grid(row=7, column=0, columnspan=2)

    receipt_tree = ttk.Treeview(frame, columns=("ID", "Nazwa", "Ilość"))
    receipt_tree["show"] = "headings"
    receipt_tree.heading("ID", text="ID")
    receipt_tree.heading("Nazwa", text="Nazwa")
    receipt_tree.heading("Ilość", text="Ilość")
    receipt_tree.grid(row=6, column=0, columnspan=2, pady=(20, 15))

    button_accept = ttk.Button(frame, text="Przyjmij", command=przyjmij)
    button_accept.grid(row=8, column=0, columnspan=2, pady=(20, 15), ipadx=20, ipady=10)

    temp_data = []

    root.mainloop()


def wyswietl_historie():
    global history_receipt_tree

    root = ThemedTk(theme="arc")
    root.title("Historia Przyjęć")

    frame = ttk.Frame(root, padding=(30, 30, 30, 30))
    frame.grid(row=0, column=0, sticky="nsew")

    history_receipt_tree = ttk.Treeview(frame, columns=("ID", "Nazwa", "Ilość", "Data Przyjęcia", "Przyjmujący"))
    history_receipt_tree["show"] = "headings"
    history_receipt_tree.heading("ID", text="ID")
    history_receipt_tree.heading("Nazwa", text="Nazwa")
    history_receipt_tree.heading("Ilość", text="Ilość")
    history_receipt_tree.heading("Data Przyjęcia", text="Data Przyjęcia")
    history_receipt_tree.heading("Przyjmujący", text="Przyjmujący")
    history_receipt_tree.grid(row=1, column=0, columnspan=2, pady=(20, 15))

    data_entry_button = ttk.Button(frame, text="Pokaż historię", command=populate_tree5)
    data_entry_button.grid(row=8, column=0, columnspan=2, pady=(20, 15), ipadx=20, ipady=10)

    root.mainloop()


def zwieksz_ilosc():
    # Pobierz zaznaczony element z widoku drzewa
    zaznaczone_elementy = tree.selection()
    if len(zaznaczone_elementy) == 0:
        # Jeśli nic nie jest zaznaczone, nie rób nic
        return

    # Pobierz identyfikator zaznaczonego elementu
    zaznaczony_element = zaznaczone_elementy[0]

    # Pobierz dane zaznaczonego elementu
    dane_zaznaczonego_elementu = tree.item(zaznaczony_element, 'values')

    # Pobierz identyfikator zaznaczonego elementu (na przykład w pierwszej kolumnie)
    id_elementu = dane_zaznaczonego_elementu[0]

    # Zwiększ wartość kolumny "ilość" o 1 w bazie danych
    zwieksz_ilosc_w_bazie(id_elementu)

    # Aktualizuj wartość w widoku drzewa
    aktualizuj_widok_drzewa(zaznaczony_element)


def zwieksz_ilosc_w_bazie(id):
    conn = mysql.connector.connect(
        host="db4free.net",
        user="magazyn",
        password="Inzynierka",
        database="magazyn_pd"
    )
    cursor = conn.cursor()

    # Wykonaj zapytanie SQL, które zwiększa wartość kolumny "ilość" o 1
    cursor.execute("UPDATE Magazyn SET Ilosc = Ilosc + 1 WHERE id=%s", (id,))

    conn.commit()
    conn.close()


def aktualizuj_widok_drzewa(element):
    obecna_ilosc = int(tree.item(element, 'values')[2])

    nowa_ilosc = obecna_ilosc + 1

    tree.item(element, values=(tree.item(element, 'values')[0], tree.item(element, 'values')[1], nowa_ilosc))


# Zmiejszanie ilości produktów w stanie magazynowym

def zmniejsz_ilosc():
    zaznaczone_elementy = tree.selection()
    if len(zaznaczone_elementy) == 0:
        return

    # Pobierz identyfikator zaznaczonego elementu
    zaznaczony_element = zaznaczone_elementy[0]

    # Pobierz dane zaznaczonego elementu
    dane_zaznaczonego_elementu = tree.item(zaznaczony_element, 'values')

    # Pobierz identyfikator zaznaczonego elementu (na przykład w pierwszej kolumnie)
    id_elementu = dane_zaznaczonego_elementu[0]

    # Zwiększ wartość kolumny "ilość" o 1 w bazie danych
    zmniejsz_ilosc_w_bazie(id_elementu)

    # Aktualizuj wartość w widoku drzewa
    aktualizuj_widok_drzewa2(zaznaczony_element)


def zmniejsz_ilosc_w_bazie(id):
    conn = mysql.connector.connect(
        host="db4free.net",
        user="magazyn",
        password="Inzynierka",
        database="magazyn_pd"
    )
    cursor = conn.cursor()
    # Wykonaj zapytanie SQL, które zwiększa wartość kolumny "ilość" o 1
    cursor.execute("UPDATE Magazyn SET Ilosc = Ilosc - 1 WHERE id=%s", (id,))

    conn.commit()
    conn.close()


def aktualizuj_widok_drzewa2(element):
    # Pobierz obecną wartość kolumny "ilość" z widoku drzewa
    obecna_ilosc = int(tree.item(element, 'values')[2])  # Zakładamy, że "ilość" jest trzecią kolumną (0, 1, 2)

    # Zwiększ wartość o 1
    nowa_ilosc = obecna_ilosc - 1

    # Zaktualizuj widok drzewa z nową wartością "ilość"
    tree.item(element, values=(tree.item(element, 'values')[0], tree.item(element, 'values')[1], nowa_ilosc))


# Wygenerowanie excela ze stanem magazynowym

def wygeneruj_excel():
    # Połączenie z bazą danych SQLite
    conn = mysql.connector.connect(
        host="db4free.net",
        user="magazyn",
        password="Inzynierka",
        database="magazyn_pd"
    )
    cursor = conn.cursor()

    # Pobranie danych z bazy danych
    cursor.execute("SELECT * FROM Magazyn")
    data = cursor.fetchall()

    # Poproś użytkownika o wybór nazwy pliku
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Pliki Excel", "*.xlsx")])

    if file_path:
        # Tworzenie nowego arkusza kalkulacyjnego
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Dane z bazy"

        # Nagłówki kolumn
        headers = ["ID", "Nazwa", "Ilość"]
        for col_num, header in enumerate(headers, 1):
            ws.cell(row=1, column=col_num, value=header)

        # Wprowadzenie danych
        for row_num, row_data in enumerate(data, 2):
            for col_num, cell_value in enumerate(row_data, 1):
                ws.cell(row=row_num, column=col_num, value=cell_value)

        # Zapisanie arkusza kalkulacyjnego do pliku Excel
        wb.save(file_path)

        # Zakończenie połączenia z bazą danych
        conn.close()

        # Wyświetl komunikat o sukcesie
        messagebox.showinfo("Sukces", f"Plik Excel został wygenerowany pomyślnie.")


# Sortowanie elementów w drzewie od stanu magazynowego

def sort_treeview(tree, col, descending):
    data = [(int(tree.set(child, col)), child) for child in tree.get_children('')]
    data.sort(reverse=descending)
    for i, (val, child) in enumerate(data):
        tree.move(child, '', i)
    tree.heading(col, command=lambda: sort_treeview(tree, col, not descending))


def sort_treeview2(tree, col, descending):
    data = [(tree.set(child, col).lower(), child) for child in tree.get_children('')]
    data.sort(reverse=descending)
    for i, (val, child) in enumerate(data):
        tree.move(child, '', i)
    tree.heading(col, command=lambda: sort_treeview2(tree, col, not descending))


###################################### Tworzenie zlecenia #####################################################

# Zmienna globalna przechowująca numer bieżącego zlecenia
current_order_number = 1

added_products = set()


# Dodawanie produktu do zlecenia

def add_to_order():
    selected_items = tree.selection()

    for item_id in selected_items:
        item = tree.item(item_id, 'values')
        product_id = item[0]

        available_quantity = int(item[2])

        # Okno ThemedTk do wprowadzania ilości
        quantity_window = ThemedTk(theme="arc")
        quantity_window.title("Ilość")

        frame = ttk.Frame(quantity_window, padding=(30, 30, 30, 30))
        frame.grid(row=0, column=0, sticky="nsew")

        entry_label = ttk.Label(frame, text=f" {item[1]} (dostępna ilość: {available_quantity}):")
        entry_label.grid(row=0, column=0, sticky="w", pady=(20, 5))
        entry = ttk.Entry(frame, width=50, font=('Arial', 12), justify='left')
        entry.grid(row=0, column=1, padx=5, pady=(20, 5), ipady=10)

        def confirm_quantity():
            nonlocal quantity_window
            quantity_str = entry.get()
            if quantity_str.isdigit():
                quantity = int(quantity_str)
                if 0 < quantity <= available_quantity:
                    # Aktualizuj bazę danych - zmniejsz ilość produktu
                    zmniejsz_ilosc_w_bazie2(product_id, quantity)
                    populate_tree()

                    order_number = current_order_number
                    while check_order_exists(order_number):
                        order_number += 1

                    new_item = item[:2] + (quantity, order_number)
                    order_tree.insert('', 'end', values=new_item)

                    quantity_window.destroy()  # Zamknij okno ThemedTk po potwierdzeniu ilości
                else:
                    tk.messagebox.showerror("Błąd",
                                            f"Podana ilość jest nieprawidłowa lub przekracza dostępną ilość ({available_quantity}).")

        confirm_button = ttk.Button(frame, text="Potwierdź", command=confirm_quantity)
        confirm_button.grid(row=1, column=0, columnspan=2, pady=(20, 15), ipadx=20, ipady=10)

        quantity_window.mainloop()


# Sprawdzanie aktulanych numerów zleceń w bazie danych w celu wybrania wolnego numeru zamówienia
def check_order_exists(order_number):
    conn = mysql.connector.connect(
        host="db4free.net",
        user="magazyn",
        password="Inzynierka",
        database="magazyn_pd"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Zlecenie WHERE Numer = %s", (order_number,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0


# Zmniejszanie ilości produktów o liczbę dodanych produktów do zlecenia

def zmniejsz_ilosc_w_bazie2(id, quantity):
    conn = mysql.connector.connect(
        host="db4free.net",
        user="magazyn",
        password="Inzynierka",
        database="magazyn_pd"
    )
    cursor = conn.cursor()

    cursor.execute("UPDATE Magazyn SET Ilosc = Ilosc - %s WHERE id=%s", (quantity, id))

    conn.commit()
    conn.close()


# Usuwanie produktów ze zlecenia

removed_products = {}


def remove_from_order():
    selected_items = order_tree.selection()
    for item_id in selected_items:
        item = order_tree.item(item_id, 'values')
        product_id = item[0]
        quantity = item[2]

        # Dodaj informacje o usuniętym produkcie do słownika
        if product_id in removed_products:
            removed_products[product_id] += quantity
        else:
            removed_products[product_id] = quantity

        # Usuń element z zamówienia
        order_tree.delete(item_id)

    przywroc_do_bazy()
    populate_tree()


# Przywracanie elementów do bazy danych po usunięciu ze zlecenia
def przywroc_do_bazy():
    conn = mysql.connector.connect(
        host="db4free.net",
        user="magazyn",
        password="Inzynierka",
        database="magazyn_pd"
    )
    cursor = conn.cursor()

    for product_id, quantity in removed_products.items():
        # Wykonaj zapytanie SQL, które zwiększa ilość produktu w bazie danych
        cursor.execute("UPDATE Magazyn SET Ilosc = Ilosc + %s WHERE id=%s", (quantity, product_id))

    conn.commit()
    conn.close()

    # Wyczyść słownik po przywróceniu do bazy danych
    removed_products.clear()


# Zapisywanie zlecenia w bazie danych

def save_to_database():
    conn = mysql.connector.connect(
        host="db4free.net",
        user="magazyn",
        password="Inzynierka",
        database="magazyn_pd"
    )
    cursor = conn.cursor()

    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Uzyskaj bieżącą datę i godzinę

    # Przykładowe założenie: logged_in_user zawiera aktualnie zalogowanego użytkownika
    user_name = user_id

    for item in order_tree.get_children():
        values = order_tree.item(item, 'values')
        product_id, name, quantity, order_number = values  # Usunięto date_added z wartości

        cursor.execute(
            "INSERT INTO Zlecenie (ID, Nazwa, Ilosc, Numer, DataDodania, identyfikator) VALUES (%s, %s, %s, %s, %s, %s)",
            (product_id, name, quantity, order_number, current_datetime,
             user_name))  # Dodaj imię użytkownika i bieżącą datę i godzinę

    conn.commit()
    conn.close()
    czyszczenie_okna()


# Czyszczenie okna po wysłaniu zlecenia

def czyszczenie_okna():
    # Wyczyść okno zlecenia magazynowego
    for item in order_tree.get_children():
        order_tree.delete(item)


def czyszczenie_okna_bez_wyslania():
    # Przenieś usunięte przedmioty do słownika przed wyczyszczeniem okna
    for item_id in order_tree.get_children():
        item = order_tree.item(item_id, 'values')
        product_id = item[0]
        quantity = item[2]

        if product_id in removed_products:
            removed_products[product_id] += quantity
        else:
            removed_products[product_id] = quantity

    # Wyczyść okno zlecenia magazynowego
    for item in order_tree.get_children():
        order_tree.delete(item)

    przywroc_do_bazy()
    populate_tree()


###################################### Potwierdzanie zlecenia #####################################################


# Potwierdzanie wydania zlecenia przez magazyniera

def remove_order_by_number():
    root = ThemedTk(theme="arc")
    root.title("Usuń zamówienie")

    frame = ttk.Frame(root, padding=(30, 30, 30, 30))
    frame.grid(row=0, column=0, sticky="nsew")

    # Dodaj pole do wprowadzania liczby
    entry_label = ttk.Label(frame, text="Numer zamówienia:")
    entry_label.grid(row=0, column=0, sticky="w", pady=(20, 5))
    entry = ttk.Entry(frame, width=50, font=('Arial', 12), justify='left')
    entry.grid(row=0, column=1, padx=5, pady=(20, 5), ipady=10)

    def show_order_details(orders_data):
        details_text = ""
        for order_data in orders_data:
            details_text += f"Nazwa: {order_data[1]}\nIlość: {order_data[2]}\nNumer: {order_data[3]}\nData dodania: {order_data[4]}\nID_Uzytkownika: {order_data[5]}\n\n"

        result = messagebox.askokcancel("Potwierdzenie zamówienia",
                                        f"Czy na pewno chcesz przenieść te zamówienia do historii?\n\n{details_text}")
        return result

    def Zakonczone():
        order_number = entry.get()

        if order_number.isdigit():
            order_number = int(order_number)

            conn = mysql.connector.connect(
                host="db4free.net",
                user="magazyn",
                password="Inzynierka",
                database="magazyn_pd"
            )
            cursor = conn.cursor()

            # Pobierz dane wszystkich zamówień o danym numerze
            cursor.execute("SELECT * FROM Zlecenie WHERE Numer = %s", (order_number,))
            orders_data = cursor.fetchall()

            # Pokaż okno potwierdzające raz dla wszystkich zamówień
            if show_order_details(orders_data):
                for order_data in orders_data:
                    # Zapytanie do przeniesienia do tabeli Historia
                    insert_query = "INSERT INTO Historia (ID, Nazwa, Ilosc, Numer, DataDodania, Status, DataZakonczenia, Zamawiajacy, Realizujacy) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

                    # Uzyskaj aktualną datę
                    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    history_data = (
                        order_data[0], order_data[1], order_data[2], order_data[3], order_data[4], 'Zakończone',
                        current_date, order_data[5], user_id)
                    cursor.execute(insert_query, history_data)

                    # Usuń z bazy danych
                    cursor.execute("DELETE FROM Zlecenie WHERE Numer = %s AND ID = %s", (order_number, order_data[0]))

                conn.commit()

                # Usuń wszystkie elementy z drzewa
                for item in order_tree.get_children():
                    order_tree.delete(item)

                # Ponownie załaduj zamówienia z bazy danych
                populate_order_tree()

            conn.close()

    def Anulowane():
        order_number = entry.get()

        if order_number.isdigit():
            order_number = int(order_number)

            conn = mysql.connector.connect(
                host="db4free.net",
                user="magazyn",
                password="Inzynierka",
                database="magazyn_pd"
            )
            cursor = conn.cursor()

            # Pobierz dane wszystkich zamówień o danym numerze
            cursor.execute("SELECT * FROM Zlecenie WHERE Numer = %s", (order_number,))
            orders_data = cursor.fetchall()

            # Pokaż okno potwierdzające raz dla wszystkich zamówień
            if show_order_details(orders_data):
                for order_data in orders_data:
                    # Zapytanie do przeniesienia do tabeli Historia
                    insert_query = "INSERT INTO Historia (ID, Nazwa, Ilosc, Numer, DataDodania, Status, DataZakonczenia) VALUES (%s, %s, %s, %s, %s, %s, %s)"

                    # Uzyskaj aktualną datę
                    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    history_data = (
                        order_data[0], order_data[1], order_data[2], order_data[3], order_data[4], 'Anulowane',
                        current_date)
                    cursor.execute(insert_query, history_data)

                    # Usuń z bazy danych
                    cursor.execute("DELETE FROM Zlecenie WHERE Numer = %s AND ID = %s", (order_number, order_data[0]))

                conn.commit()

                # Usuń wszystkie elementy z drzewa
                for item in order_tree.get_children():
                    order_tree.delete(item)

                # Ponownie załaduj zamówienia z bazy danych
                populate_order_tree()

            conn.close()

    # Dodaj przycisk do uruchamiania funkcji usuwającej zamówienie
    remove_order_button = ttk.Button(frame, text="Potwierdź zamówienie", command=Zakonczone)
    remove_order_button.grid(row=1, column=1, columnspan=2, pady=(20, 15), ipadx=20, ipady=10)

    remove_order_button = ttk.Button(frame, text="Anuluj zamówienie", command=Anulowane)
    remove_order_button.grid(row=2, column=1, columnspan=2, pady=(20, 15), ipadx=20, ipady=10)


# Historia zamówień

def historia():
    global history_tree

    root = ThemedTk(theme="arc")
    root.title("Historia Zleceń Magazynowych")

    frame = ttk.Frame(root, padding=(30, 30, 30, 30))
    frame.grid(row=0, column=0, sticky="nsew")

    history_tree = ttk.Treeview(frame, columns=(
    "ID", "Nazwa", "Ilosc", "Numer", "DataDodania", "Status", "DataZakonczenia", "Zamawiajacy", "Realizujacy"))
    history_tree["show"] = "headings"
    history_tree.heading("ID", text="ID", anchor='center')
    history_tree.heading("Nazwa", text="Nazwa", anchor='center')
    history_tree.heading("Ilosc", text="Ilość", anchor='center')
    history_tree.heading("Numer", text="Numer Zlecenia", anchor='center')
    history_tree.heading("DataDodania", text="Data Dodania", anchor='center')
    history_tree.heading("Status", text="Status", anchor='center')
    history_tree.heading("DataZakonczenia", text="Data Zakonczenia", anchor='center')
    history_tree.heading("Zamawiajacy", text="Zamawiajacy", anchor='center')
    history_tree.heading("Realizujacy", text="Realizujacy", anchor='center')
    history_tree.grid(row=1, column=0, columnspan=2, pady=(20, 15))

    data_entry_button = ttk.Button(frame, text="Pokaż historię", command=populate_tree4)
    data_entry_button.grid(row=8, column=0, columnspan=2, pady=(20, 15), ipadx=20, ipady=10)

    # Uruchomienie głównej pętli
    root.mainloop()


###################################### Funkcje administratora #####################################################

# Tworzenie szyfrowania hasła

def utworz_skrot_hasla(haslo):
    # Używamy funkcji sha256 z modułu hashlib do utworzenia skrótu hasła
    skrot = hashlib.sha256(haslo.encode()).hexdigest()
    return skrot


# Tworzenie użytkownika
def user_edit1(id):
    def zapisz_edycje():
        nowe_imie = imie_entry.get()
        nowe_nazwisko = nazwisko_entry.get()
        nowa_rola = rola_var.get()
        nowy_email = email_entry.get()
        nowy_identyfikator = identyfikator_entry.get()

        conn = mysql.connector.connect(
            host="db4free.net",
            user="magazyn",
            password="Inzynierka",
            database="magazyn_pd"
        )
        cursor = conn.cursor()

        cursor.execute('SELECT imie, nazwisko, email FROM uzytkownicy WHERE id=%s', (id,))
        stare = cursor.fetchone()
        stare_imie = stare[0]
        stare_nazwisko = stare[1]
        stary_email = stare[2]

        # Sprawdź, czy imię lub nazwisko uległy zmianie
        if nowe_imie != stare_imie or nowe_nazwisko != stare_nazwisko:
            # Jeśli tak, zaktualizuj adres e-mail
            stary_email = f"{nowe_imie.lower()}.{nowe_nazwisko.lower()}@email.com"
            print(stary_email)
        elif nowy_email != stary_email:
            print(nowy_email)
            # Jeśli imię i nazwisko się nie zmieniły, ale administrator chce zmienić ręcznie e-mail
            stary_email = nowy_email

        cursor.execute('UPDATE uzytkownicy SET imie=%s, nazwisko=%s, rola=%s, email=%s, identyfikator=%s WHERE id=%s',
                       (nowe_imie, nowe_nazwisko, nowa_rola, stary_email, nowy_identyfikator, id))

        conn.commit()

        populate_tree3()

        messagebox.showinfo("Sukces", "Edycja użytkownika zakończona pomyślnie.")
    root = ThemedTk(theme="arc")
    root.title("Edycja użytkownika")

    conn = mysql.connector.connect(
        host="db4free.net",
        user="magazyn",
        password="Inzynierka",
        database="magazyn_pd"
    )
    cursor = conn.cursor()
    cursor.execute('SELECT imie, nazwisko, rola, email, identyfikator FROM uzytkownicy WHERE id=%s', (id,))
    dane_uzytkownika = cursor.fetchone()
    conn.close()

    frame = ttk.Frame(root, padding=(30, 30, 30, 30))
    frame.grid(row=0, column=0, sticky="nsew")

    imie_label = ttk.Label(frame, text="Imię:")
    imie_label.grid(row=0, column=0, sticky="w", pady=(20, 5))
    imie_entry = ttk.Entry(frame)
    imie_entry.grid(row=0, column=1, pady=(20, 5), ipady=10)
    imie_entry.insert(0, dane_uzytkownika[0])  # Ustawienie domyślnej wartości

    nazwisko_label = ttk.Label(frame, text="Nazwisko:")
    nazwisko_label.grid(row=1, column=0, sticky="w", pady=(5, 10))
    nazwisko_entry = ttk.Entry(frame)
    nazwisko_entry.grid(row=1, column=1, pady=(5, 10), ipady=10)
    nazwisko_entry.insert(0, dane_uzytkownika[1])  # Ustawienie domyślnej wartości

    rola_label = ttk.Label(frame, text="Rola:")
    rola_label.grid(row=2, column=0, sticky="w", pady=(5, 10))
    role = ["admin", "pracownik", "magazyn"]
    rola_var = ttk.Combobox(frame, values=role)
    rola_var.grid(row=2, column=1, pady=(5, 10), ipady=10)
    rola_var.set(dane_uzytkownika[2])  # Ustawienie domyślnej wartości

    email_label = ttk.Label(frame, text="Email:")
    email_label.grid(row=3, column=0, sticky="w", pady=(5, 10))
    email_entry = ttk.Entry(frame)
    email_entry.grid(row=3, column=1, pady=(5, 10), ipady=10)
    email_entry.insert(0, dane_uzytkownika[3])  # Ustawienie domyślnej wartości

    identyfikator_label = ttk.Label(frame, text="Identfikator:")
    identyfikator_label.grid(row=4, column=0, sticky="w", pady=(5, 10))
    identyfikator_entry = ttk.Entry(frame)
    identyfikator_entry.grid(row=4, column=1, pady=(5, 10), ipady=10)
    identyfikator_entry.insert(0, dane_uzytkownika[4])  # Ustawienie domyślnej wartości

    zapisz_button = ttk.Button(frame, text="Zapisz edycję", command=zapisz_edycje)
    zapisz_button.grid(row=5, column=0, columnspan=2, pady=(10, 20))

    root.mainloop()

def edytuj():
    # Pobierz zaznaczony element z widoku drzewa
    zaznaczone_elementy = users_tree.selection()
    if len(zaznaczone_elementy) == 0:
        # Jeśli nic nie jest zaznaczone, nie otwieraj okna
        return

    root = ThemedTk(theme="arc")
    root.title("Formularz edycji")

    # Pobierz identyfikator zaznaczonego elementu
    zaznaczony_element = zaznaczone_elementy[0]

    # Pobierz dane zaznaczonego elementu
    dane_zaznaczonego_elementu = users_tree.item(zaznaczony_element, 'values')

    # Pobierz identyfikator zaznaczonego elementu (na przykład w pierwszej kolumnie)
    id_elementu = dane_zaznaczonego_elementu[0]
    # Dodaj ramkę dla estetyki
    frame = ttk.Frame(root, padding=30)
    frame.grid(row=0, column=0, sticky="nsew")

    create_button = ttk.Button(frame, text="Edytuj użytkownika", command=lambda: user_edit1(id_elementu))
    create_button.grid(row=1, column=0, pady=(0, 10), sticky="ew")

    create_button = ttk.Button(frame, text="Usuń użytkownika",
                               command=lambda: usun_zaznaczony_element2(id_elementu, zaznaczony_element))
    create_button.grid(row=1, column=1, pady=(0, 10), sticky="ew")

    create_button = ttk.Button(frame, text="Resetuj hasło użytkownika", command=lambda: reset_password(id_elementu))
    create_button.grid(row=1, column=3, pady=(0, 10), sticky="ew")

    root.mainloop()



def utworz():
    root = ThemedTk(theme="arc")
    root.title("Formularz logowania")

    # Dodaj ramkę dla estetyki
    frame = ttk.Frame(root, padding=(30, 30, 30, 30))
    frame.grid(row=0, column=0, sticky="nsew")

    # Etykieta i pole tekstowe dla imienia
    imie_label = ttk.Label(frame, text="Imię:")
    imie_label.grid(row=0, column=0, sticky="w", pady=(20, 5))
    imie_entry = ttk.Entry(frame)
    imie_entry.grid(row=0, column=1, pady=(20, 5), ipady=10)

    # Etykieta i pole tekstowe dla nazwiska
    nazwisko_label = ttk.Label(frame, text="Nazwisko:")
    nazwisko_label.grid(row=1, column=0, sticky="w", pady=(5, 10))
    nazwisko_entry = ttk.Entry(frame)
    nazwisko_entry.grid(row=1, column=1, pady=(5, 10), ipady=10)

    haslo_label = ttk.Label(frame, text="Hasło:")
    haslo_label.grid(row=2, column=0, sticky="w", pady=(5, 10))
    haslo_entry = ttk.Entry(frame, show="*")
    haslo_entry.grid(row=2, column=1, pady=(5, 10), ipady=10)

    # Etykieta i rozwijalne menu dla nowej roli użytkownika
    nowa_rola_label = ttk.Label(frame, text="Rola:")
    nowa_rola_label.grid(row=3, column=0, sticky="w", pady=(5, 10))

    role = ["admin", "pracownik", "magazyn"]
    nowa_rola_var = tk.StringVar()
    nowa_rola_var.set(role[0])
    rola_menu = ttk.Combobox(frame, values=role, state="readonly")
    rola_menu.grid(row=3, column=1, pady=(5, 10), ipady=10)

    # Etykieta do wyświetlania komunikatów o błędach
    wynik_label = ttk.Label(frame, text="")
    wynik_label.grid(row=6, column=0, columnspan=2, pady=(15, 20))

    # Funkcja do tworzenia użytkownika
    def utworz_uzytkownika():
        imie = imie_entry.get()
        nazwisko = nazwisko_entry.get()
        haslo = haslo_entry.get()
        nowa_rola = rola_menu.get()  # Pobierz wartość bezpośrednio z rozwijalnego menu

        if not nowa_rola:
            wynik_label.config(text="Wybierz rolę użytkownika.")
            return


        # Automatyczne generowanie emaila na podstawie imienia i nazwiska
        nowy_email = f"{imie.lower()}.{nazwisko.lower()}@email.com"

        # Tworzenie Indentyfikatora
        identyfikator = f"{nowa_rola[0].upper()}_{imie[0].upper()}{nazwisko[0].upper()}"
        print(identyfikator)
        conn = mysql.connector.connect(
            host="db4free.net",
            user="magazyn",
            password="Inzynierka",
            database="magazyn_pd"
        )
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM uzytkownicy WHERE email=%s', (nowy_email,))
        istniejacy_uzytkownik = cursor.fetchone()

        if istniejacy_uzytkownik:
            wynik_label.config(text="Użytkownik o podanym adresie email już istnieje.")
        else:
            cursor.execute(
                'INSERT INTO uzytkownicy (email, haslo, imie, nazwisko, rola, identyfikator) VALUES (%s, %s, %s, %s, %s, %s)',
                (nowy_email, utworz_skrot_hasla(haslo), imie, nazwisko, nowa_rola, identyfikator))
            conn.commit()
            conn.close()
            populate_tree3()

            wynik_label.config(text="Nowy użytkownik został utworzony.")

            imie_entry.delete(0, tk.END)
            nazwisko_entry.delete(0, tk.END)

    # Przycisk do tworzenia użytkownika
    create_user_button = ttk.Button(frame, text="Utwórz użytkownika", command=utworz_uzytkownika, width=20)
    create_user_button.grid(row=5, column=0, columnspan=2, pady=(20, 15), ipadx=20, ipady=10)

    # Uruchomienie głównej pętli
    root.mainloop()


# Usuwanie użytkownika przez administratora

def usun_zaznaczony_element2(id_elementu, zaznaczony_element):
    # Wyświetl pytanie o potwierdzenie przed usunięciem
    potwierdzenie = messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć ten element?")
    if potwierdzenie:
        # Usuń zaznaczony element z bazy danych
        usun_rekord2(id_elementu)

        # Usuń zaznaczony element z widoku drzewa
        users_tree.delete(zaznaczony_element)


def usun_rekord2(id):
    conn = mysql.connector.connect(
        host="db4free.net",
        user="magazyn",
        password="Inzynierka",
        database="magazyn_pd"
    )
    cursor = conn.cursor()

    # Wykonaj zapytanie SQL, aby usunąć rekord o określonym identyfikatorze
    cursor.execute("DELETE FROM uzytkownicy WHERE id=%s", (id,))

    conn.commit()
    conn.close()


def on_close(root):
    root.destroy()
    wyswietl_ekran_logowania()


def reset_password(id):
    def sprawdz_haslo2():
        nowe_haslo_1 = nowe_haslo_entry_1.get()
        nowe_haslo_2 = nowe_haslo_entry_2.get()

        if nowe_haslo_1 != nowe_haslo_2:
            messagebox.showerror("Błąd", "Podane hasła nie są identyczne.")
            return

        conn = mysql.connector.connect(
            host="db4free.net",
            user="magazyn",
            password="Inzynierka",
            database="magazyn_pd"
        )
        cursor = conn.cursor()

        # Aktualizacja hasła w bazie danych
        cursor.execute('UPDATE uzytkownicy SET haslo=%s WHERE id=%s', (utworz_skrot_hasla(nowe_haslo_1), id))
        conn.commit()

        messagebox.showinfo("Sukces", "Hasło zostało pomyślnie zmienione.")

    root = ThemedTk(theme="arc")
    root.title("Formularz resetowania hasła")

    frame = ttk.Frame(root, padding=(30, 30, 30, 30))
    frame.grid(row=0, column=0, sticky="nsew")

    nowe_haslo_label_1 = ttk.Label(frame, text="Nowe hasło:")
    nowe_haslo_label_1.grid(row=0, column=0, sticky="w", pady=(20, 5))
    nowe_haslo_entry_1 = ttk.Entry(frame, show="*")
    nowe_haslo_entry_1.grid(row=0, column=1, pady=(20, 5), ipady=10)

    nowe_haslo_label_2 = ttk.Label(frame, text="Potwierdź nowe hasło:")
    nowe_haslo_label_2.grid(row=1, column=0, sticky="w", pady=(5, 10))
    nowe_haslo_entry_2 = ttk.Entry(frame, show="*")
    nowe_haslo_entry_2.grid(row=1, column=1, pady=(5, 10), ipady=10)

    zmien_haslo_button = ttk.Button(frame, text="Zmień hasło", command=sprawdz_haslo2)
    zmien_haslo_button.grid(row=2, column=0, columnspan=2, pady=(10, 20))


def zmien_haslo():
    print(user_id)

    def sprawdz_haslo():
        stare_haslo = stare_haslo_entry.get()
        nowe_haslo = nowe_haslo_entry.get()

        conn = mysql.connector.connect(
            host="db4free.net",
            user="magazyn",
            password="Inzynierka",
            database="magazyn_pd"
        )
        cursor = conn.cursor()
        print(user_id)
        cursor.execute('SELECT haslo FROM uzytkownicy WHERE identyfikator=%s', (user_id,))
        result = cursor.fetchone()
        print(result)

        if result:
            print(result[0])
            haslo_w_bazie = result[0]
            haslo_skrot = utworz_skrot_hasla(stare_haslo)

            if haslo_w_bazie == haslo_skrot:
                # Aktualizacja hasła
                cursor.execute('UPDATE uzytkownicy SET haslo=%s WHERE identyfikator=%s',
                               (utworz_skrot_hasla(nowe_haslo), user_id))
                conn.commit()
                messagebox.showinfo("Sukces", "Hasło zostało pomyślnie zmienione.")
            else:
                messagebox.showerror("Błąd", "Podane stare hasło jest nieprawidłowe.")
        else:
            messagebox.showerror("Błąd", "Wystąpił błąd podczas pobierania hasła z bazy danych.")

    root = ThemedTk(theme="arc")
    root.title("Formularz zmiany hasła")

    frame = ttk.Frame(root, padding=(30, 30, 30, 30))
    frame.grid(row=0, column=0, sticky="nsew")

    stare_haslo_label = ttk.Label(frame, text="Stare hasło:")
    stare_haslo_label.grid(row=0, column=0, sticky="w", pady=(20, 5))
    stare_haslo_entry = ttk.Entry(frame, show="*")
    stare_haslo_entry.grid(row=0, column=1, pady=(20, 5), ipady=10)

    nowe_haslo_label = ttk.Label(frame, text="Nowe hasło:")
    nowe_haslo_label.grid(row=1, column=0, sticky="w", pady=(5, 10))
    nowe_haslo_entry = ttk.Entry(frame, show="*")
    nowe_haslo_entry.grid(row=1, column=1, pady=(5, 10), ipady=10)

    zmien_haslo_button = ttk.Button(frame, text="Zmień hasło", command=sprawdz_haslo)
    zmien_haslo_button.grid(row=2, column=0, columnspan=2, pady=(10, 20))


wyswietl_ekran_logowania()

#
# def zamknij_wszystkie_okna():
#     for window in ThemedTk.themed_tk_instances():
#         window.destroy()
