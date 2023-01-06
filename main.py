import flet as ft 
import moviepy.editor as mv
from pytube import YouTube

def main(page:ft.Page):
    #scroll activado que nos permite desplazarnos dentro de la APP
    page.scroll = True
    # metodo app bar de plet que nos permite agregar un header a nuestra app
    # permitiendo agregar colores y archivos svg
    page.appbar = ft.AppBar(
        bgcolor = ft.colors.RED_900,
        leading=ft.Image(src='<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19c-2.3 0-6.4-.2-8.1-.6-.7-.2-1.2-.7-1.4-1.4-.3-1.1-.5-3.4-.5-5s.2-3.9.5-5c.2-.7.7-1.2 1.4-1.4C5.6 5.2 9.7 5 12 5s6.4.2 8.1.6c.7.2 1.2.7 1.4 1.4.3 1.1.5 3.4.5 5s-.2 3.9-.5 5c-.2.7-.7 1.2-1.4 1.4-1.7.4-5.8.6-8.1.6 0 0 0 0 0 0z"></path><polygon points="10 15 15 12 10 9"></polygon></svg>',color=ft.colors.WHITE70),
        title = ft.Text("Youtube Video Downloader"),
    )
    # alineación centralizada de los elementos de nuestra app 
    page.vertical_alignment= ft.MainAxisAlignment.CENTER
    page.horizontal_alignment= ft.CrossAxisAlignment.CENTER

    # La funcion textchange permite cambiar los nombres de los buttons y cambiar 
    #el logo de la app por una visualizacion del video o audio a descargar
    def textChange(event):
        try:
            video_details = YouTube(event.control.value)
            button1.text = "Descargar video - " + video_details.title
            button2.text = "Descargar audio - " + video_details.title
            image.src = video_details.thumbnail_url
            image.update()
            button1.update()
            button2.update()
        except:
            button1.text ="Descargar Video"
            button2.text = "Descargar Audio"
            image.src = "https://logodownload.org/wp-content/uploads/2014/10/youtube-logo-7-2.png"
            image.update()
            button1.update()
            button2.update()
    
    #Este metodo permite interactuar con el escritorio mediante el dialogo con la 
    # app, metodo nativo de flet llamado FilePickerResultEvent

    def get_directory_result(evento: ft.FilePickerResultEvent):
        directory_path.value = evento.path if evento.path else "Ruta no ingresada!"
        button3.text = directory_path.value
        button3.update()
        directory_path.update()
    
    #variables inicializar la función  FilePicker que cambian mediante el uso de la función get_directory_result

    get_directory_dialog = ft.FilePicker(on_result=get_directory_result)
    directory_path = ft.Text()
    page.overlay.extend([get_directory_dialog])
    


    #funcion que toma un valor de la variable externa llamada "txt" para poder descargar 
    #desde un link un video, se verifica si cumple con la condicion de ser un link valido, y se le comunica al usurio mediante la función SnackBar de flet
    def downloadVideo(event):
        if len(txt.value) == 0:
            print("ingrese un link...")
            page.snack_bar = ft.SnackBar(ft.Text("ingrese un link...",color=ft.colors.WHITE),bgcolor=ft.colors.BLACK38)
            page.snack_bar.open = True
            page.update()
        else:
            try:
                progress.visible = True
                page.update()
                get_link = txt.value
                mp4_video = YouTube(get_link).streams.get_highest_resolution().download(directory_path.value)
                vid_clip = mv.VideoFileClip(mp4_video)
                vid_clip.close
                page.dialog = dlg
                dlg.open = True
                progress.visible = False
                page.update()
                

            except:
                page.snack_bar = ft.SnackBar(ft.Text("Error link no reconocido",color=ft.colors.WHITE),bgcolor=ft.colors.BLACK38)
                page.snack_bar.open = True
                progress.visible = False
                page.update()
                print("no hay link valido")
    #funcion que toma un valor de la variable esterna txt para poder descargar 
    #desde un link de audio, se verifica si cumple con la condicion de ser un link valido y se le comunica al usurio mediante la función SnackBar de flet
    
    def downloadAudio(event):
        if len(txt.value) == 0:
            print("ingrese un link...")
            page.snack_bar = ft.SnackBar(ft.Text("ingrese un link...",color=ft.colors.WHITE),bgcolor=ft.colors.BLACK38)
            page.snack_bar.open = True
            page.update()
        else:
            try:
                progress.visible = True
                page.update()
                get_link = txt.value
                mp4_audio = YouTube(get_link).streams.get_audio_only().download(directory_path.value)
                vid_clip = mv.AudioFileClip(mp4_audio)
                vid_clip.close
                page.dialog = dlg
                dlg.open = True
                progress.visible = False
                page.update()
            except:
                page.snack_bar = ft.SnackBar(ft.Text("Error link no reconocido",color=ft.colors.WHITE),bgcolor=ft.colors.BLACK38)
                page.snack_bar.open = True
                progress.visible = False
                page.update()
                print("no hay link valido")
    

    # Variables externas 
    txt = ft.TextField(hint_text="ingrese un link",on_change=textChange)

    image = ft.Image(src="https://logodownload.org/wp-content/uploads/2014/10/youtube-logo-7-2.png")

    button1 = ft.ElevatedButton("Descargar Video",on_click=downloadVideo,icon=ft.icons.PLAY_CIRCLE,bgcolor=ft.colors.RED_900,color=ft.colors.WHITE70)

    button2 = ft.ElevatedButton("Descargar Audio",on_click=downloadAudio,icon=ft.icons.AUDIOTRACK_SHARP,bgcolor=ft.colors.RED_900,color=ft.colors.WHITE70)

    button3 = ft.ElevatedButton("Seleccionar Carpeta",icon=ft.icons.FOLDER_OPEN,bgcolor=ft.colors.BLUE_800,color=ft.colors.WHITE70 ,on_click=lambda _:         get_directory_dialog.get_directory_path(), disabled=page.web)

    dlg = ft.AlertDialog(title=ft.Text("Descarga Exitosa"), on_dismiss=lambda event: print("dialogo acabado"))

    progress =ft.ProgressBar(width=400,color="red",bgcolor="#eeeeee", visible=False)

    # agregando los elementos creados a nuestra app para su visualización
    page.add(
        image,
        ft.Container(height=4),
        txt,
        progress,
        button3,
        ft.Container(height=4),
        button1,
        ft.Container(height=4),
        button2,
    )

# ejecutando nuestra app 
if __name__ == "__main__":
    ft.app(target=main)

