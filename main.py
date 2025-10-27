import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    #  gestione dell'aspetto della page
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti") # creazione dell'oggetto della classe Autonoleggio
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    input_marca=ft.TextField(label='Marca', width=120)
    input_modello=ft.TextField(label='Modello', width=120)
    input_anno=ft.TextField(label='Anno', width=120)

    posti_contatore=ft.TextField(width=120, disabled=True, text_align=ft.TextAlign.CENTER, text_size=18)
    # TODO

    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    posti_contatore.value=0

    def incrementa(e):
        try:
            valore_corrente=posti_contatore.value
            valore_corrente += 1
            posti_contatore.value=valore_corrente
            posti_contatore.update()

        except ValueError:
            alert.show_alert('❌ Inserire valori numerici nel campo posti')

    def decrementa(e):
        try:
            valore_corrente=posti_contatore.value # inizialmente è 0

            if valore_corrente > 0:
                valore_corrente -= 1 # decremento di uno se è maggiore di zero
                posti_contatore.value=valore_corrente
                posti_contatore.update()
            else:
                alert.show_alert('❌ Il numero minimo di posti non può essere negativo o uguale a zero')
        except ValueError:
            alert.show_alert('❌ Inserire valori numerici nel campo posti')

    def aggiungi_automobile_handler(e):
        try:
            # recuperiamo il valore inserito
            marca = input_marca.value
            modello = input_modello.value
            anno = int(input_anno.value)
            posti= int(posti_contatore.value)

            autonoleggio.aggiungi_automobile(marca, modello, anno, posti)  # chiamo il metodo dell'oggetto autonoleggio

            aggiorna_lista_auto() # chiamo la funzione che aggiorna la lista delle auto

            input_marca.value=''
            input_modello.value=''
            input_anno.value=''
            posti_contatore.value=0
            page.update()
            alert.show_alert('✅ Automobile aggiunta con successo')

        except ValueError: # la conversione a int può generare errore
            alert.show_alert('❌ Errore: inserire valori numerici per anno e posti')
        except Exception as error:
            alert.show_alert(f'❌ Errore: {error}')
            # TODO

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    btn_plus=ft.IconButton(ft.Icons.ADD, on_click=incrementa)
    btn_minus=ft.IconButton(ft.Icons.REMOVE, on_click=decrementa)
    # TODO

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        ft.Text('Aggiungi automobile', size=20, weight=ft.FontWeight.BOLD),
        ft.Row(spacing=10,
               controls=[input_marca, input_modello, input_anno, ft.Row(spacing=0,
                                                                        controls=[btn_minus, posti_contatore, btn_plus],
                                                                        alignment=ft.MainAxisAlignment.CENTER)],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.ElevatedButton("Aggiungi automobile", on_click=aggiungi_automobile_handler),
        # TODO

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
