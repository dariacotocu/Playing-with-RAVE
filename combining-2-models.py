from dorothy import Dorothy
import torch
import numpy as np

dot = Dorothy()

class MySketch:

    def __init__(self):
        dot.start_loop(self.setup, self.draw)

    def setup(self):

        self.state = 0
        self.ptr = 0  #let's see 

        #rave models 
        #first sol (orchestral one)
        self.rave_smooth = dot.music.start_rave_stream(
            model_path="rave_model/sol_full.ts",
            fft_size=1024,
            buffer_size=1024,
            sr=44100,
            latent_dim=16,
            output_device=None,
        )
        #second percussion 
        self.rave_drum = dot.music.start_rave_stream(
            model_path="rave_model/percussion.ts",
            fft_size=1024,
            buffer_size=1024,
            sr=44100,
            latent_dim=16,
            output_device=None,
        )

        '''had to give up on latent vectors for sol
        # vector 7 - quiet, nice note
        self.z_soft = torch.tensor([[[ 0.5875], [ 1.9843], [ 0.9438], [ 0.5092], [ 1.5811], [-1.3662], [ 0.4057], [ 0.1376], [-1.2852], [ 0.2440], [ 1.0864], [ 0.0917], [-1.8552], [ 0.2517], [-1.5406], [-0.0297]]])  
        # vector 3 - mid
        self.z_mid = torch.tensor([[[ 1.8010], [-1.0508], [ 0.6969], [ 0.2978], [ 0.2626], [-0.8342], [-0.0286], [-2.8198], [-0.8021], [-2.0158], [-1.3607], [ 0.2676], [ 0.7964], [ 0.1358], [-0.9662], [ 1.5176]]])
        # vector 4 - loud, fave
        self.z_loud = torch.tensor([[[ 0.5944], [-0.8303], [-1.0026], [ 1.5540], [ 0.7035], [-1.3491], [-0.2078], [ 0.7372], [ 1.1593], [ 0.4698], [-1.1297], [-0.4017], [ 0.5462], [-0.3359], [-0.9512], [ 0.1236]]])

        dot.music.audio_outputs[self.rave_smooth].current_latent = self.z_soft
'''
       
        self.blend = 0

        # audio input (guitar / interface)
        self.device_id = dot.music.start_device_stream(
            "Scarlett 4i4 USB, Core Audio",
            buffer_size=1024
        )

        def on_new_frame(buffer=np.zeros(1024)):
         
            #how loud is my guitar, no neg values
            energy = np.mean(np.abs(buffer))
            #mulitply by 30, guitar input is quiet 
            energy = energy * 30  
            #clip to keep between 0 & 1
            energy = np.clip(energy, 0, 1)
            #print(f"energy: {energy:.4f} state: {self.state}")

            # 3 states based on energy playing
            #state 0 = quiet, state 1 = mid, state 2 = loud
            if energy < 0.15:
                new_state = 0
            elif energy < 0.5:
                new_state = 1
            else:
                new_state = 2

            self.state = new_state

            '''0 = Sol only (ambient)
            1 = Mix (transition)
            2 = Drums dominate'''

            if self.state == 0:
                # Sol only
                dot.music.audio_outputs[self.rave_smooth].volume = 1.2
                #dot.music.audio_outputs[self.rave_smooth].current_latent = self.z_soft
                dot.music.audio_outputs[self.rave_drum].volume = 0.001

            elif self.state == 1:
                # Mix
                dot.music.audio_outputs[self.rave_smooth].volume = 1.2
                #dot.music.audio_outputs[self.rave_smooth].current_latent = self.z_mid
                dot.music.audio_outputs[self.rave_drum].volume = 0.2

            else:
                # Drums dominate
                dot.music.audio_outputs[self.rave_smooth].volume = 1
                dot.music.audio_outputs[self.rave_drum].volume = 0.5
                #dot.music.audio_outputs[self.rave_smooth].current_latent = self.z_loud

            #mix the two models, so one always overpowers the other one
            #dot.music.audio_outputs[self.rave_smooth].volume = (1 - self.blend) **2
            #dot.music.audio_outputs[self.rave_drum].volume = self.blend ** 0.6

            #every 20 sec both models jump to a new random point in their latent space
            self.ptr += len(buffer)
            if self.ptr > 44100 * 20:
                z1 = torch.randn((1, 16, 1))
                z2 = torch.randn((1, 16, 1))
                dot.music.audio_outputs[self.rave_smooth].current_latent = z1
                dot.music.audio_outputs[self.rave_drum].current_latent = z2
                self.ptr = 0
                print("NEW LATENT")



        # attach callback


        
        dot.music.audio_outputs[self.rave_smooth].on_new_frame = on_new_frame
        dot.music.audio_outputs[self.rave_drum].on_new_frame = on_new_frame

    def draw(self):
        dot.background((255, 255, 255))
        dot.music.update_rave_from_stream(self.device_id)


MySketch()