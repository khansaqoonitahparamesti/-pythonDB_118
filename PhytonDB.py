import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

#membuat database
def create_database() :
    conn = sqlite3.connect("nilai_siswa.db")
    cur = conn.cursor()
    cur.execute('''
         CREATE TABLE IF NOT EXISTS nilai_siswa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_siswa TEXT ,
        biologi INTEGER ,
        fisika INTEGER ,
        inggris INTEGER ,
        prediksi_fakultas TEXT 
    )
''')
    conn.commit()
    conn.close()

#fungsi mengambil semua data dari database
def fetch_data():
    conn = sqlite3.connect("nilai_siswa.db")
    cur = conn.cursor()
    cur.execute("SELECT* FROM nilai_siswa")
    rows = cur.fetchall()
    conn.close()
    return rows

#menyimpan data baru ke data base
def save_to_database(nama, biologi, fisika, inggris, prediksi):
   conn = sqlite3.connect("nilai_siswa.db")
   cur = conn.cursor()
   cur.execute ('''INSERT INTO nilai_siswa (nama_siswa, biologi, fisika,inggris,prediksi_fakultas)
         VALUES (?, ?, ?,?,?)
    ''', (nama, biologi, fisika, inggris, prediksi))
   conn.commit()
   conn.close()

#memperbarui data di database
def update_database (record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cur = conn.cursor()
    cur.execute(''' 
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika =?, prediksi_fakultas=?
        where id =?)      
    ''',(nama,biologi,fisika,inggris,prediksi, record_id ))
    conn.commit()
    conn.close()

# menghapus  data dari database
def delete_database(record_id):
     conn = sqlite3.connect("nilai_siswa.db")
     cur = conn.cursor()
     cur.execute ('DELETE FROM nilai_siswa WHERE id = ?',(record_id))
     conn.commit()
     conn.close()

# menghitung prediksi fakultas
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "teknik"
    elif inggris > biologi and inggris > fisika:
        return "bahasa"
    else :
        return "tidak diketahui"
    
# menangani tombol submit    
def submit():
    try:
        nama = nama_var.get()
        biologi = int (biologi_var.get())
        fisika = int (fisika_var.get())
        inggris = int (inggris_var.get())

        if not nama:
            raise Exception("nama siswa tidak boleh kosong")
        
        prediksi = calculate_prediction (biologi, fisika, inggris)
        save_to_database (nama, biologi, fisika, inggris,prediksi)

        messagebox.showinfo ("sukses",f"data berhasil disimpan!\nprediksi fakultas :{prediksi}")
        clear_inputs()
        populate_table()

    except ValueError as e:
        messagebox.showerror ("Error",f"input tidak valid: {e}")

# menangani tombol update
def update():
    try:
        if not selected_record_id.get():
            raise Exception ("pilihan data dari tabel untuk di update")
        
        record_id = int (selected_record_id.get())
        nama = nama_var.get()
        biologi = int (biologi_var.get())
        fisika = int (fisika_var.get())
        inggris = int (inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong. ")
        prediksi = calculate_prediction (biologi, fisika, inggris)
        update_database (nama, biologi, fisika, inggris)

        messagebox.showinfo ("sukses", " Data berhasil di perbarui")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"kesalahan : {e}")

def delete():
    try:
        if not selected_record_id.get():
            raise Exception ("pilih data tabel unutk dihapus")
        
        record_id = int (selected_record_id.get())
        delete_database (record_id)
        messagebox.showinfo("sukses", "data berhasil di hapus")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error",f"kesalahan: e")

def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

def populate_table():
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_data():
        tree.insert ('','end', values=row)

#msengisi input data dari database
 
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item (selected_item)['values']

        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("error", "pilih data yang valid")
#inisialisasi database
create_database()
#membuat gui dengan tkinter
root = Tk()
root.title("prediksi fakultas siswa ")
# variabel tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar() #Menyimpan id recor yang di pilih

#elemen GUI
Label (root, text="nama siswa").grid(row=0, column=0, padx=10, pady=5)
Entry (root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label (root, text="nilai biologi").grid(row=1, column=0, padx=10, pady=5)
Entry (root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label (root, text="nilai fisika").grid(row=2, column=0, padx=10, pady=5)
Entry (root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label (root, text="nilai inggris").grid(row=3, column=0, padx=10, pady=5)
Entry (root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

Button(root, text="Add", command= submit).grid(row=4, column=0, pady=10)
Button(root, text="update", command= update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command= delete).grid(row=4, column=2, pady=10)

#Tabel menampilkan data
column = ("id","nama_siswa","biologi","fisika","inggris","Prediksi_Fakultas")
tree = ttk.Treeview (root, column=column, show='headings')

#Menyesuaikan Posisi teks di setiap kolom ke tengah mengatur posisi isi tabel di tengah
for col in column:
    tree.heading(col, text=col.capitalize())
    tree.column (col, anchor='center')

tree.grid(row=0, column=3,padx=10,pady=10)
#event memilih data dari tabel
tree.bind('<ButtonRelease>',fill_inputs_from_table)
#Mengisi tabel data
populate_table()
#Menjalankan aplikasi
root.mainloop()