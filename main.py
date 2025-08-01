from customtkinter import *
from CTkListbox import *
from PIL import Image
import music_tag
import os
import time
import shutil
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import  showerror
import pygame

app=CTk()
app.geometry("1300x720")
app.title("Music Player")


pygame.mixer.init()

set_appearance_mode("dark")
all_font=CTkFont(family="MV Boli",size=35,weight='bold')

# -------------------------------- functions ----------------------------------------

# control time music and get now time music
music_len=IntVar(value=0)
real_time=IntVar(value=0)
def get_current_time_music():

    cur_time=real_time.get() +(int((pygame.mixer_music.get_pos()+1)/1000))

    # convert time format to 00:00
    convert_current_time=time.strftime("%M:%S",time.gmtime(cur_time))
    start_time_lb.configure(text=convert_current_time)

    # change position slider Location
    position_slider_state.set(value=cur_time)

    # if music is the end go to next play list
    index=play_list_box.curselection()
    if cur_time+1 == music_len.get():
        stop_music()
        # if end of play list
        if index+1 < play_list_box.size():
            play_list_box.activate(index+1)
            play_music()
        else:
            play_list_box.activate(index=0)
            play_music()

        real_time.set(value=0)

    start_time_lb.after(1000,get_current_time_music)


# get music time and change end time music label
def get_music_time_len():
    active_index=play_list_box.curselection()
    music_name=play_list_box.get(active_index)

    mp3=music_tag.load_file(f"play_list/{music_name}")
    mp3_len=int(mp3["#length"])

    music_len.set(value=mp3_len)
    #convert time format to 00:00
    convert_music_len = time.strftime("%M:%S", time.gmtime(mp3_len))
    end_time_lb.configure(text=convert_music_len)

    #get music len for position slider
    position_slider.configure(to=mp3_len)

# show play list from directory (play_list)
def show_play_list():
    play_list_box.delete(0, END)
    musics=os.listdir("play_list")
    for music in musics:
        play_list_box.insert(END,music)

# add music in list box
def add_music():
    try:
        music=askopenfilename(title="choose a music",filetypes=(("MP3 Songs","*.mp3"),))
        shutil.copy(music,"play_list")
        show_play_list()
    except FileNotFoundError:
        showerror("add error","file not select for add list")

# remove music from list box
def remove_music():
    try:
        index=play_list_box.curselection()
        music_choice=play_list_box.get(index)
        os.remove(f"play_list/{music_choice}")
        show_play_list()
    except FileNotFoundError:
        showerror('remove error','file not select for remove list')

# play music
def play_music():
    position_slider_state.set(value=0)
    real_time.set(value=0)
    if is_paused.get():
        pygame.mixer.music.unpause()
        is_paused.set(value=False)

    else:
        try:

            index=play_list_box.curselection()
            music_name=play_list_box.get(index)
                # load mp3 file
            mp3 = music_tag.load_file(f"play_list/{music_name}")
                #load binary picture
            album_art=mp3["artwork"].first.data

                #convert binary to image and save "image"
            with open("images/new_image.jpg","wb") as picture:
                picture.write(album_art)

            # change music image
            album_image.configure(light_image=Image.open("images/new_image.jpg"),size=(380,320))
            #change music name in bar
            music_name_lb.configure(text=music_name.replace(".mp3",""))
            # play music
            pygame.mixer_music.load(f"play_list/{music_name}")
            pygame.mixer_music.play()

            get_current_time_music() #music now time
            get_music_time_len() # music end time
        except :
            showerror("music error","file not select in the playlist")

# in listbox music choice next music button
def next_music():
    try:
        active_index=play_list_box.curselection()
        play_list_box.activate(active_index+1)

        play_music()
    #if list of end return the list
    except :
        play_list_box.activate(0)
        play_music()

# in listbox music back music button
def previous_music():

    active_index=play_list_box.curselection()
    play_list_box.activate(active_index-1)
    play_music()

# stop button music function
def stop_music():
    active_index=play_list_box.curselection()
    play_list_box.deactivate(active_index)
    album_image.configure(light_image=Image.open("images/album.jpeg"),size=(400,380))
    music_name_lb.configure(text="music name")
    pygame.mixer_music.stop()

# pause button music function
is_paused=BooleanVar(value=False)
def pause_music():
    if not is_paused.get():
        is_paused.set(value=True)
        pygame.mixer.music.pause()
    else:
        is_paused.set(value=False)
        pygame.mixer.music.unpause()

# change slide time music
def slide_music(time_):
    try:
        real_time.set(value=time_)
        index=play_list_box.curselection()
        music_name=play_list_box.get(index)
        pygame.mixer_music.load(f"play_list/{music_name}")
        pygame.mixer_music.play(start=time_)
    except:
        showerror("position slid error","any music not play")
        position_slider_state.set(value=0)

# change volume music
def volume_music(volume):
    pygame.mixer_music.set_volume(volume)

# change volume from mouse wheel
def volume_set_event(event):
    volume_ = volume_state_var.get()

    if event.delta == 120:
        volume_state_var.set(volume_  +0.25)
        pygame.mixer_music.set_volume(volume_  +0.25)
    elif event.delta == -120:
        volume_state_var.set(volume_  -0.25)
        pygame.mixer_music.set_volume(volume_  -0.25)

app.bind('<MouseWheel>', func=volume_set_event)

# ------------------------------------ images ----------------------------------------------
album_image=CTkImage(Image.open("images/album.jpeg"),size=(400,380))

play_img=CTkImage(Image.open("images/play.png"),size=(50,50))
pause_img=CTkImage(Image.open("images/pause.png"),size=(50,50))
stop_img=CTkImage(Image.open("images/stop.png"),size=(50,50))
next_img=CTkImage(Image.open("images/next.png"),size=(50,50))
previous_img=CTkImage(Image.open("images/previous.png"),size=(50,50))
add_playlist_image=CTkImage(Image.open("images/add_music.png"),size=(45,45))
remove_playlist_image=CTkImage(Image.open("images/remove_music.png"),size=(45,45))

# ------------------------------------ app grid ----------------------------------------------------
app.grid_rowconfigure((0,2), weight=0)
app.grid_rowconfigure(1, weight=2)
app.grid_columnconfigure(0, weight=1)

#--------------------------------------- Frames ------------------------------------------------------
# music detail frame

music_detail_frame=CTkFrame(app,fg_color="transparent")
music_detail_frame.grid(column=0,row=1,pady=15,sticky="nsew")
music_detail_frame.grid_columnconfigure((0,2),weight=0)
music_detail_frame.grid_columnconfigure(1,weight=1)
music_detail_frame.grid_rowconfigure(1,weight=1)

# control frame
control_frame=CTkFrame(app,fg_color="transparent")
control_frame.grid(column=0,row=2,sticky="nsew")
control_frame.grid_columnconfigure((0,1,2,3,4,5,6),weight=1)
control_frame.grid_rowconfigure(0,weight=1)

#slide bar frame
side_bar_frame=CTkFrame(app,corner_radius=50)
side_bar_frame.grid(column=1,row=0,rowspan=4,sticky="nsew",pady=20,padx=15)
side_bar_frame.grid_rowconfigure(2,weight=1)

# add and remove music play list in(slide bar frame)
add_remove_frame=CTkFrame(side_bar_frame,fg_color="transparent")
add_remove_frame.grid(column=0,row=3,padx=10,pady=25)

volume_frame=CTkFrame(music_detail_frame,fg_color="transparent")
volume_frame.grid(column=2,row=0,padx=10,pady=25)

#------------------------- widgets -----------------------------
# music name bar label
music_name_lb=CTkLabel(app,text="music name",fg_color="transparent",font=all_font)
music_name_lb.grid(row=0,column=0,pady=10)

# music image
image_label=CTkLabel(music_detail_frame,text="",fg_color="transparent",image=album_image)
image_label.grid(column=1,row=0,padx=35,pady=45,sticky="nsew")

# volume slider
volume_up=CTkLabel(volume_frame,text="up",fg_color="transparent",font=CTkFont(size=12,weight="bold"))
volume_up.grid(row=0,column=0)

volume_state_var=DoubleVar(value=1)
volume_slider=CTkSlider(volume_frame,orientation="vertical",button_color="#7A7A73",fg_color="#000000",progress_color="#7A7A73",from_=0,to=1,height=100,width=20,variable=volume_state_var,command=volume_music)
volume_slider.grid(column=0,row=1)

volume_up=CTkLabel(volume_frame,text="down",fg_color="transparent",font=CTkFont(size=12,weight="bold"))
volume_up.grid(row=2,column=0)

# control button
play_btn=CTkButton(control_frame,text="",fg_color="transparent",image=play_img,command=play_music)
play_btn.grid(column=3,row=0,padx=10,pady=10)

pause_btn=CTkButton(control_frame,text="",fg_color="transparent",image=pause_img,command=pause_music)
pause_btn.grid(column=4,row=0,padx=10,pady=10)

stop_btn=CTkButton(control_frame,text="",fg_color="transparent",image=stop_img,command=stop_music)
stop_btn.grid(column=2,row=0,padx=10,pady=10)

next_btn=CTkButton(control_frame,text="",fg_color="transparent",image=next_img,command=next_music)
next_btn.grid(column=5,row=0,padx=10,pady=10)

previous_btn=CTkButton(control_frame,text="",fg_color="transparent",image=previous_img,command=previous_music)
previous_btn.grid(column=1,row=0,padx=10,pady=10)

# Time Label start and end of music
start_time_lb=CTkLabel(control_frame,text="00:00")
start_time_lb.grid(column=0,row=1)

end_time_lb=CTkLabel(control_frame,text="00:00")
end_time_lb.grid(column=7,row=1)

# time slider music
position_slider_state=IntVar(value=0) #point start slider

position_slider=CTkSlider(control_frame,button_color="#7A7A73",fg_color="#000000",progress_color="#7A7A73",from_=0,to=100,height=20,variable=position_slider_state,command=slide_music)
position_slider.grid(column=1,row=1,columnspan=5,padx=20,pady=25,sticky="ew")

# playList Label
play_list=CTkLabel(side_bar_frame,text="play list",font=CTkFont(size=30,weight="bold"))
play_list.grid(column=0,row=0,padx=10,pady=10)

# play List Box music
play_list_box=CTkListbox(side_bar_frame,width=280,height=350,border_width=10,border_color="#7A7A73",corner_radius=40)
play_list_box.grid(column=0,row=1,padx=10,pady=25)

#add and remove music button play list
add_btn=CTkButton(add_remove_frame,text="",fg_color="transparent",image=add_playlist_image,command=add_music)
add_btn.grid(column=0,row=0,padx=5,pady=5)

remove_btn=CTkButton(add_remove_frame,text="",fg_color="transparent",image=remove_playlist_image,command=remove_music)
remove_btn.grid(column=1,row=0,padx=5,pady=5)

show_play_list()
app.mainloop()

