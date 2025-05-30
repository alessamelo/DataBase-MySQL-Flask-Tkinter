import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
from PIL import Image, ImageTk 
from PIL.Image import Resampling 

API_BASE = "http://127.0.0.1:5000/api"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Cute Music App 🌸")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#ffe6f0")  

        self.user_id = None
        self.main_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_screen(self):
        self.clear_screen()
        tk.Button(self.root, text="Start", command=self.show_auth_options,
                  bg="#ffb3d9", fg="black", activebackground="#ff4da6", font=("Century Gothic", 10, "bold")).pack(pady=20)

    def show_auth_options(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome!! ", bg="#ffe6f0", fg="black", font=("Century Gothic", 11, "bold")).pack(pady=10)
        tk.Button(self.root, text="User Login", command=self.login_screen,
                  bg="#ffb3d9", fg="black", activebackground="#ff4da6", font=("Century Gothic", 10, "bold")).pack(pady=5)
        tk.Button(self.root, text="Artist Login", command=self.artist_login_screen,
                  bg="#ffb3d9", fg="black", activebackground="#ff4da6", font=("Century Gothic", 10, "bold")).pack(pady=5)
        tk.Button(self.root, text="Sign Up", command=self.signup_screen,
                  bg="#ffb3d9", fg="black", activebackground="#ff4da6", font=("Century Gothic", 10, "bold")).pack(pady=10)
        tk.Button(self.root, text="Go back", command=self.main_screen,
                  bg="#d98caa", fg="black", font=("Century Gothic", 10)).pack(pady=5)


    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Username", bg="#ffe6f0", fg="#b30059", font=("Comic Sans MS", 10, "bold")).pack()
        username = tk.Entry(self.root)
        username.pack()
        tk.Label(self.root, text="Password", bg="#ffe6f0", fg="#b30059", font=("Comic Sans MS", 10, "bold")).pack()
        password = tk.Entry(self.root, show="*")
        password.pack()

        def submit():
            res = requests.post(f"{API_BASE}/login", json={
                "username": username.get(),
                "password": password.get()
            })
            if res.ok:
                self.user_id = res.json().get("user", {}).get("user_id")
                messagebox.showinfo("Login Successful", "Welcome back, superstar! <3")
                self.menu_principal()
                #print("ID del usuario guardado:", self.user_id)

            else:
                messagebox.showerror("Error", "Login failed!")

        tk.Button(self.root, text="Submit", command=submit,
          bg="#ffb3d9", fg="black", activebackground="#ff4da6", font=("Century Gothic", 10, "bold")).pack(pady=10)

        tk.Button(self.root, text="Back", command=self.show_auth_options,
          bg="#d98caa", fg="black", font=("Century Gothic", 10)).pack(pady=5)



    def artist_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Username", bg="#ffe6f0", fg="#b30059", font=("Comic Sans MS", 10, "bold")).pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Contraseña", bg="#ffe6f0", fg="#b30059", font=("Comic Sans MS", 10, "bold")).pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        tk.Label(self.root, text="ID de Artista", bg="#ffe6f0", fg="#b30059", font=("Comic Sans MS", 10, "bold")).pack()
        artist_id_entry = tk.Entry(self.root)
        artist_id_entry.pack()

        def login():
            data = {
                "username": username_entry.get(),
                "password": password_entry.get(),
                "artist_id": artist_id_entry.get()
            }
            try:
                res = requests.post(f"{API_BASE}/artist_login", json=data)
                if res.ok:
                    json_data = res.json()
                    self.user_id = json_data.get("user_id")
                    self.artist_id = json_data.get("artist_id")
                    messagebox.showinfo("Éxito", "Inicio de sesión exitoso como artista")
                    self.artist_menu()
                else:
                    error_msg = res.json().get("error", "Fallo en la autenticación")
                    messagebox.showerror("Error", error_msg)
            except Exception as e:
                messagebox.showerror("Error", f"Hubo un error al iniciar sesión: {e}")

        tk.Button(self.root, text="Iniciar sesión", command=login).pack(pady=10)
        tk.Button(self.root, text="Regresar", command=self.show_auth_options).pack(pady=5)


    def artist_menu(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Menú de Artista (ID: {self.artist_id})").pack(pady=10)

        def add_song():
            self.clear_screen()
            entries = {}
            fields = ["collection_id", "title", "duration", "release_year", "genre", "explicit"]
            for field in fields:
                tk.Label(self.root, text=field).pack()
                entry = tk.Entry(self.root)
                entry.pack()
                entries[field] = entry

            def submit():
                try:
                    data = {
                        "collection_id": int(entries["collection_id"].get()),
                        "title": entries["title"].get(),
                        "duration": int(entries["duration"].get()),
                        "release_year": int(entries["release_year"].get()),
                        "genre": entries["genre"].get(),
                        "explicit": entries["explicit"].get().lower() == "true"
                    }
                    res = requests.post(f"{API_BASE}/songs", json=data)
                    if res.ok:
                        song_id = res.json().get("song_id")
                        messagebox.showinfo("Success", f"Song added successfully! 🎵\nID: {song_id}\nPlease keep this number to assign credits later.")
                        self.artist_menu()
                    else:
                        messagebox.showerror("Error", res.text)
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            tk.Button(self.root, text="Enviar", command=submit).pack(pady=5)
            tk.Button(self.root, text="Regresar", command=self.artist_menu).pack(pady=5)

        def add_collection():
            self.clear_screen()
            entries = {}
            fields = ["title", "type", "release_date", "total_tracks"]
            for field in fields:
                tk.Label(self.root, text=field).pack()
                entry = tk.Entry(self.root)
                entry.pack()
                entries[field] = entry

            def submit():
                try:
                    data = {
                        "title": entries["title"].get(),
                        "type": entries["type"].get(),
                        "release_date": entries["release_date"].get(),
                        "total_tracks": int(entries["total_tracks"].get()),
                        "artist_id": self.artist_id
                    }
                    res = requests.post(f"{API_BASE}/collections", json=data)
                    if res.ok:
                        collection_id = res.json().get("collection_id")
                        messagebox.showinfo("Éxito", f"Collection added successfully. \n    Collection_ID = {collection_id} \nPlease keep this number to assign songs later. ")
                        self.artist_menu()
                    else:
                        messagebox.showerror("Error", res.text)
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            tk.Button(self.root, text="Enviar", command=submit).pack(pady=5)
            tk.Button(self.root, text="Regresar", command=self.artist_menu).pack(pady=5)

        def add_credit():
            self.clear_screen()
            entries = {}
            fields = ["song_id", "role"]
            for field in fields:
                tk.Label(self.root, text=field).pack()
                entry = tk.Entry(self.root)
                entry.pack()
                entries[field] = entry

            def submit():
                try:
                    data = {
                        "song_id": int(entries["song_id"].get()),
                        "user_id": self.user_id,
                        "role": entries["role"].get()
                    }
                    res = requests.post(f"{API_BASE}/credits", json=data)
                    if res.ok:
                        messagebox.showinfo("Éxito", "Participación registrada")
                        self.artist_menu()
                    else:
                        messagebox.showerror("Error", res.text)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                    
            tk.Button(self.root, text="Enviar", command=submit).pack(pady=5)
            tk.Button(self.root, text="Regresar", command=self.artist_menu).pack(pady=5)

        tk.Button(self.root, text="Agregar canción", command=add_song).pack(pady=5)
        tk.Button(self.root, text="Agregar colección", command=add_collection).pack(pady=5)
        tk.Button(self.root, text="Agregar participación en canción", command=add_credit).pack(pady=5)
        tk.Button(self.root, text="Cerrar sesión", command=self.main_screen).pack(pady=10)



    
    def signup_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="¿Qué tipo de cuenta deseas crear?").pack(pady=10)
        tk.Button(self.root, text="Cuenta normal", command=self.normal_user_signup).pack(pady=5)
        tk.Button(self.root, text="Cuenta de artista", command=self.artist_user_signup).pack(pady=5)
        tk.Button(self.root, text="Regresar", command=self.show_auth_options).pack(pady=10)



    def normal_user_signup(self):
        self.clear_screen()
        entries = {}
        fields = ["username", "first_name", "last_name", "email", "password", "date_birth", "artist_id"]

        for field in fields:
            tk.Label(self.root, text=field).pack()
            entry = tk.Entry(self.root, show="*" if field == "password" else None)
            entry.pack()
            entries[field] = entry

        def submit():
            try:
                data = {f: entries[f].get() for f in fields}
                data["explicit_content"] = False  # Valor por defecto
                if data["artist_id"] == "":
                    data["artist_id"] = None
                else:
                    data["artist_id"] = int(data["artist_id"])

                res = requests.post(f"{API_BASE}/users", json=data)
                if res.ok:
                    messagebox.showinfo("Éxito", "Usuario creado exitosamente")
                    self.show_auth_options()
                else:
                    messagebox.showerror("Error", f"Fallo al crear usuario: {res.text}")
            except Exception as e:
                messagebox.showerror("Error", f"Datos inválidos: {e}")

        tk.Button(self.root, text="Enviar", command=submit).pack(pady=10)
        tk.Button(self.root, text="Regresar", command=self.signup_screen).pack(pady=5)

    def artist_user_signup(self):
        self.clear_screen()
        entries = {}
        fields = ["name", "bio", "country", "active_since"]
        for field in fields:
            tk.Label(self.root, text=field).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            entries[field] = entry

        def submit():
            try:
                data = {f: entries[f].get() for f in fields}
                res = requests.post(f"{API_BASE}/artists", json=data)
                if res.ok:
                    artist_id = res.json().get("artist_id")
                    messagebox.showinfo("Artista creado",
                        f"Cuenta de artista creada exitosamente. Tu ID de artista es: {artist_id}\nGuárdalo para asociarlo a tu cuenta de usuario. \n Este numero es importante para poder subir contenido musical.")
                    self.signup_screen()
                else:
                    messagebox.showerror("Error", f"Fallo al crear artista: {res.text}")
            except Exception as e:
                messagebox.showerror("Error", f"Datos inválidos: {e}")

        tk.Button(self.root, text="Enviar", command=submit).pack(pady=10)
        tk.Button(self.root, text="Regresar", command=self.signup_screen).pack(pady=5)


    def menu_principal(self):
        self.clear_screen()
        tk.Button(self.root, text="🔍 Buscar canción", command=self.buscar_cancion).pack(pady=10)
        tk.Button(self.root, text="🎤 Buscar artista", command=self.buscar_artista).pack(pady=10)
        tk.Button(self.root, text="Regresar", command=self.main_screen).pack(pady=5)



    def buscar_cancion(self):
        self.clear_screen()
        tk.Label(self.root, text="Nombre de la canción").pack()
        entry = tk.Entry(self.root)
        entry.pack()

        def buscar():
            title = entry.get()
            res = requests.get(f"{API_BASE}/songs/search", params={"title": title})
            if res.ok:
                songs = res.json()
                if not songs:
                    messagebox.showinfo("Sin resultados", "No se encontraron canciones.")
                    return
                for song in songs:
                    info = (
                        f"{song['title']} | "
                        f"{song['collection']['title']} ({song['collection']['release_date']}) | "
                        f"{song['artist']['name']}"
                    )
                    tk.Button(self.root, text=info, wraplength=350, justify="left",
                              command=lambda s=song: self.guardar_escucha(s)).pack(pady=2)
            else:
                messagebox.showerror("Error", "Error al buscar canciones")

        tk.Button(self.root, text="Buscar", command=buscar).pack(pady=5)
        tk.Button(self.root, text="Regresar", command=self.menu_principal).pack(pady=5)



    def guardar_escucha(self, song):
        data = {"user_id": self.user_id, "song_id": song['song_id']}
        res = requests.post(f"{API_BASE}/streamings", json=data)
        if res.ok:
            messagebox.showinfo("Éxito", f"Escucha registrada de '{song['title']}'")
        else:
            messagebox.showerror("Error", "No se pudo registrar la escucha")



    def buscar_artista(self):
        self.clear_screen()
        tk.Label(self.root, text="Nombre del artista").pack()
        entry = tk.Entry(self.root)
        entry.pack()

        def buscar():
            name = entry.get()
            res = requests.get(f"{API_BASE}/artists/songs", params={"name": name})
            if res.ok:
                data = res.json()
                if not data:
                    messagebox.showinfo("Sin resultados", "No se encontraron canciones.")
                    return
                for item in data:
                    artist = item.get("artist", {})
                    collection = item.get("collection", {})
                    song = item.get("song", {})

                    info = (
                        f"{song.get('title', 'Sin título')} | "
                        f"{collection.get('title', 'Sin álbum')} ({collection.get('release_date', '?')}) | "
                        f"{artist.get('name', 'Desconocido')}"
                    )

                    tk.Button(self.root, text=info, wraplength=350, justify="left",
                            command=lambda s=song: self.guardar_escucha(s)).pack(pady=2)
            else:
                messagebox.showerror("Error", f"Error al buscar artista: {res.status_code}")

        tk.Button(self.root, text="Buscar", command=buscar).pack(pady=5)
        tk.Button(self.root, text="Regresar", command=self.menu_principal).pack(pady=5)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
