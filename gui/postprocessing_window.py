from customtkinter import CTkFrame, CTkImage, CTkLabel, CTkButton, StringVar, filedialog, CTkProgressBar
from PIL import Image
from gui.components.spinbox import Spinbox
from utils.data_imputator import ImputeData
import mediapipe as mp
import cv2
import os
import copy 
import json

class PostprocessingWindow(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color='#949494')
        self.parent = parent
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        for i in range(4): self.grid_rowconfigure(i, weight=1)
        
        self.logo = CTkImage(light_image=Image.open("assets/images/logo.png"), size=(450*100//130, 100))
        self.logo2 = CTkImage(light_image=Image.open("assets/images/logo2.png"), size=(769*250//317, 250))
        self.search_icon = CTkImage(light_image=Image.open("assets/images/search.png"), size=(30, 30))
        self.return_btn = CTkImage(light_image=Image.open("assets/images/previous.png"), size=(70, 70))

        self.setup_ui()
    
    def setup_ui(self):

        #Imagenes
        self.container_img = CTkFrame(self, fg_color='#636363', border_color='#000000', border_width=2)
        self.container_img.grid(row=0, column=0, rowspan=4, sticky='NSEW', padx=30, pady=20)
        self.container_img.grid_rowconfigure(0, weight=1)
        
        CTkLabel(self.container_img, image=self.logo, text='').grid(row=1, column=0, pady=10)
        CTkLabel(self.container_img, image=self.logo2, text='').grid(row=0, column=0, padx=30, pady=100)
        CTkButton(self.container_img, 
                  image=self.return_btn, 
                  command=self.return_menu, 
                  fg_color='transparent',
                  hover_color='#4a4a4a',
                  text='', 
                  width=75,
                  height=75,
                  corner_radius=10).grid(row=0, column=0, padx=10, pady=10, sticky='NW')

        self.container_1 = CTkFrame(self, fg_color='#DAE3F3', border_color='#172C51', border_width=2)
        self.container_1.grid(row=0, column=1, sticky='EW', padx=30, pady=20)

        self.container_2 = CTkFrame(self, fg_color='#DAE3F3', border_color='#172C51', border_width=2)
        self.container_2.grid(row=1, column=1, sticky='EW', padx=30, pady=20)

        self.container_3 = CTkFrame(self, fg_color='#DAE3F3', border_color='#172C51', border_width=2)
        self.container_3.grid(row=3, column=1, sticky='EW', padx=30, pady=20)

        #------------------- Container 1 -------------------

        self.title_label3 = CTkLabel(self.container_1, 
                                         text=self.controller.language_manager.get_text("postprocessing_window", "title"), 
                                         font=("Arial", 30), 
                                         text_color='#000000')
        self.title_label3.grid(row=0, column=0, columnspan=2, padx= 10, pady=10)

        self.dest_folder_var = StringVar(value='C:/Users/Lenovo-PC/Videos/DataSet')
        self.l1 = CTkLabel(self.container_1, 
                               text=self.dest_folder_var.get(), 
                               font=("Arial", 25), 
                               wraplength=350, 
                               fg_color='#dcd9d8',
                               corner_radius=6, 
                               text_color='#000000')
        self.l1.grid(row=1, column=0, padx= 5, pady=10)

        self.btn_search = CTkButton(self.container_1, 
                                        text=self.controller.language_manager.get_text("postprocessing_window", "search_button"), 
                                        command=self.select_origin, 
                                        font=("Arial", 25), 
                                        text_color='#b6d5ea',
                                        image=self.search_icon)
        self.btn_search.grid(row=1, column=1, padx=10, pady=10, stick='NS')


        self.title_label2_2 = CTkLabel(self.container_1, 
                                         text=self.controller.language_manager.get_text("postprocessing_window", "Spinbox_label"), 
                                         font=("Arial", 30), 
                                         wraplength=550, 
                                         text_color='#000000')
        self.title_label2_2.grid(row=2, column=0, sticky='W', padx=10, pady=10)

        self.spinbox = Spinbox(self.container_1, from_=1, to=10, default_value=3)
        self.spinbox.grid(column = 1, row=2, padx=5)

        #------------------ Container 2 ------------------

        CTkLabel(self.container_2, 
                text=self.controller.language_manager.get_text("postprocessing_window", "title2"), 
                font=("Arial", 30), 
                text_color='#000000').grid(row=0, column=0, columnspan=2, padx= 10, pady=10)

        self.save_folder_var = StringVar(value='C:/Users/Lenovo-PC/Documents')

        self.l2 = CTkLabel(self.container_2, 
                               text=self.save_folder_var.get(), 
                               font=("Arial", 25), 
                               wraplength=350, 
                               fg_color='#dcd9d8',
                               corner_radius=6, 
                               text_color='#000000')
        self.l2.grid(row=1, column=0, padx= 5, pady=10)

        self.btn_search = CTkButton(self.container_2, 
                                        text=self.controller.language_manager.get_text("postprocessing_window", "search_button"), 
                                        command=self.select_destination, 
                                        font=("Arial", 25), 
                                        text_color='#b6d5ea',
                                        image=self.search_icon)
        self.btn_search.grid(row=1, column=1, padx=10, pady=10, stick='NS')

        #------------------ Container 3 ------------------
        self.container_3.grid_columnconfigure(0, weight=1)

        CTkButton(self.container_3, 
                   text=self.controller.language_manager.get_text("postprocessing_window", "start_button"), 
                   command=self.start_processing, 
                   font=("Arial", 25)).grid(row=0, column=0, padx=10, pady=10, sticky='NS')
        
        self.prog_container = CTkFrame(self.container_3, fg_color='#DAE3F3', border_color='#172C51', border_width=2)
        self.prog_container.grid(row=1, column=0, sticky='EW', padx=10, pady=10)
        self.prog_container.grid_columnconfigure(0, weight=1)

        self.progressbar = CTkProgressBar(self.prog_container, orientation="horizontal", mode="determinate")
        self.progressbar.grid(row=0, column=0, padx=15, pady=15, sticky='NSEW')
        self.progressbar.set(0)

        self.progressbar_label = CTkLabel(self.prog_container,
                                          text='0%',
                                          font=("Arial", 25),
                                          text_color='#000000')
        self.progressbar_label.grid(row=0, column=1, pady=10, padx=15)
        
    def start_processing(self):


        BaseOptions = mp.tasks.BaseOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions

        FaceLandmarker = mp.tasks.vision.FaceLandmarker
        FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions

        PoseLandmarker = mp.tasks.vision.PoseLandmarker
        PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions

        hand_path = 'models/hand_landmarker.task'
        face_path = 'models/face_landmarker.task'
        pose_path = 'models/pose_landmarker_full.task'

        hand_options = HandLandmarkerOptions(base_options=BaseOptions(model_asset_path=hand_path),
                                             running_mode=VisionRunningMode.VIDEO,
                                             num_hands=2)

        face_options = FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path=face_path),
                                             running_mode=VisionRunningMode.VIDEO)

        pose_options = PoseLandmarkerOptions(base_options=BaseOptions(model_asset_path=pose_path),
                                             running_mode=VisionRunningMode.VIDEO)
        
        self.create_paths()
        
        for j, video_path in enumerate(self.archivos):
            self.update()
            self.progressbar.set((j+1)/len(self.archivos))
            self.progressbar_label.configure(text=f'{int((j+1)/len(self.archivos)*100)}%')

            with HandLandmarker.create_from_options(hand_options) as hand_landmarker, FaceLandmarker.create_from_options(face_options) as face_landmarker, PoseLandmarker.create_from_options(pose_options) as pose_landmarker:
                print(video_path)
                #Descriptores del video actual
                signer = 'Signer_' + video_path[len(self.dest_folder_var.get())+1:].split('/')[0]
                categorie = video_path[len(self.dest_folder_var.get())+1:].split('/')[1]
                label = video_path[len(self.dest_folder_var.get())+1:].split('/')[2]
                video_num = 'vid_' + video_path[len(self.dest_folder_var.get())+1:].split('/')[3].split('.')[0]

                #Captura del video y propiedades
                cap = cv2.VideoCapture(video_path)
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                
                #Datos iniciales
                timestamp = 0
                video_data = {}
                previous_result = {'face':[],
                                'pose':[],
                                'r_hand':[],
                                'l_hand':[]}
                
                #Objeto para imputar datos
                imputator = ImputeData()
                
                for i in range(frame_count):
                    ret, frame = cap.read()
                    
                    if ret:
                        #Imagen para MediPipe
                        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                        
                        #Extraer puntos
                        results = {'face':face_landmarker.detect_for_video(mp_image, timestamp).face_landmarks,
                                'pose':pose_landmarker.detect_for_video(mp_image, timestamp).pose_landmarks}

                        results = self.hand_array(hand_landmarker.detect_for_video(mp_image, timestamp), results)
                        imputator.main(results, previous_result)
                        video_data[f'frame_{i}'] = copy.deepcopy(imputator.result)
                        
                        previous_result = results    

                    timestamp += int(1000/fps)
                x_mins = []
                x_maxs = []

                for frame in video_data:
                    for body_part in video_data[frame]:
                        if not None in video_data[frame][body_part]['x']:
                            x_mins.append(min(video_data[frame][body_part]['x']))
                            x_maxs.append(max(video_data[frame][body_part]['x']))

                x_step = ((1 - max(x_maxs)) - (- min(x_mins))) / (self.spinbox.get()-1)

                x_translations = [- min(x_mins) + (x_step*i)  for i in range(int(self.spinbox.get()))]

                for i, x_add in enumerate(x_translations):
                    translated_data = copy.deepcopy(video_data)
                    for frame in translated_data:
                        for body_part in translated_data[frame]:
                            if not None in translated_data[frame][body_part]['x']:
                                translated_data[frame][body_part]['x'] = [x_i + x_add for x_i in translated_data[frame][body_part]['x']]
                                self.data[signer][categorie][label][video_num][f'rep_{i}'] = translated_data

                cap.release()
        
        with open(self.save_folder_var.get() + '/datos.json', 'w', encoding='utf-8') as archivo:
            json.dump(self.data, archivo, ensure_ascii=False, indent=4)

    def select_origin(self):
        """Permite seleccionar la carpeta de destino."""
        self.dest_folder_var.set(filedialog.askdirectory())
        self.l1.configure(text=self.dest_folder_var.get())

    def select_destination(self):
        """Permite seleccionar la carpeta de destino."""
        self.save_folder_var.set(filedialog.askdirectory())
        self.l2.configure(text=self.save_folder_var.get())
        print(self.save_folder_var.get() + '/datos.json')

    def create_paths(self):
        """Crea las rutas de los archivos de salida."""
        carpeta_base = self.dest_folder_var.get()

        self.data ={}
        self.archivos = []

        for signer in os.listdir(carpeta_base):
            self.data[f'Signer_{signer}'] = {}
            for categorie in os.listdir(f'{carpeta_base}\\{signer}'):
                self.data[f'Signer_{signer}'][categorie] = {}
                for label in os.listdir(f'{carpeta_base}\\{signer}\\{categorie}'):
                    self.data[f'Signer_{signer}'][categorie][label] = {}
                    for video in os.listdir(f'{carpeta_base}\\{signer}\\{categorie}\\{label}'):
                        self.data[f'Signer_{signer}'][categorie][label][f'vid_{video.split('.')[0]}'] = {}
                        self.archivos.append(f'{carpeta_base}/{signer}/{categorie}/{label}/{video}')
                        for repeticion in range(self.spinbox.get()): # Repeticones
                            self.data[f'Signer_{signer}'][categorie][label][f'vid_{video.split(".")[0]}'][f'rep_{repeticion}'] = {}
        
        
    
    def hand_array(self, prediction, results):
        #print(prediction)

        wrist_coords_pose = [(results['pose'][0][15].x, results['pose'][0][15].y),
                             (results['pose'][0][16].x, results['pose'][0][16].y)]
        
        if not prediction.hand_landmarks:
                results['r_hand'] = []
                results['l_hand'] = []

        elif len(prediction.hand_landmarks) == 1:
                wrist_coords = [prediction.hand_landmarks[0][0].x, 
                                prediction.hand_landmarks[0][0].y]
                
                euc_dist = [((wrist_coords[0] - wrist[0])**2 + (wrist_coords[1] - wrist[1])**2)**0.5 for wrist in wrist_coords_pose]

                indice = euc_dist.index(min(euc_dist))

                if indice:
                        results['l_hand'] = prediction.hand_landmarks
                        results['r_hand'] = []
                else:
                        results['l_hand'] = []
                        results['r_hand'] = prediction.hand_landmarks

        else:
                wrist_coords = [[prediction.hand_landmarks[0][0].x, prediction.hand_landmarks[0][0].y],
                                [prediction.hand_landmarks[1][0].x, prediction.hand_landmarks[1][0].y]]
                
                euc_dist = [[((wrist_hand[0] - wrist[0])**2 + (wrist_hand[1] - wrist[1])**2)**0.5 for wrist in wrist_coords_pose] for wrist_hand in wrist_coords]

                indices = [euc.index(min(euc)) for euc in euc_dist]
                
                min_idx = [min(euc) for euc in euc_dist].index(min([min(euc) for euc in euc_dist]))

                if indices == [0, 1]:
                        results['l_hand'] = [prediction.hand_landmarks[1]]
                        results['r_hand'] = [prediction.hand_landmarks[0]]
                elif indices == [1, 0]:
                        results['l_hand'] = [prediction.hand_landmarks[0]]
                        results['r_hand'] = [prediction.hand_landmarks[1]]

                # Si ambas están cerca de solo una muñeca se toma la mas cercana
                elif indices == [0, 0]:
                        results['l_hand'] = [prediction.hand_landmarks[min_idx]]
                        results['r_hand'] = []
                else:
                        results['l_hand'] = []
                        results['r_hand'] = [prediction.hand_landmarks[min_idx]]

        return results
    
    def return_menu(self):
        self.controller.show_menu_window()