import requests
from moviepy.editor import *
import pygame
import html
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from textwrap import wrap
import math
import sys
import datetime

class TriviaVideoGenerator:
    def __init__(self):
        self.width = 1080  # YouTube Shorts dimensions
        self.height = 1920
        self.duration_per_question = 6
        self.countdown_duration = 5
        self.answer_duration = 2  # Reduced answer duration to 2 seconds
        self.margin = 50  # Margin from all sides
        self.background_color = (0, 0, 0)  # Dark background

    def create_clock_animation(self, duration):
        w, h = int(self.width * 0.2), int(self.width * 0.2)
        
        def make_frame(t):
            surface = Image.new('RGBA', (w, h), (0, 0, 0, 0))
            draw = ImageDraw.Draw(surface)
            
            margin = 10
            draw.ellipse([margin, margin, w-margin, h-margin], 
                        outline=(255, 223, 0), width=3)
            
            center = (w/2, h/2)
            angle = (t / duration) * 2 * math.pi
            hand_length = (w/2 - margin) * 0.8
            
            end_x = center[0] + hand_length * math.sin(angle)
            end_y = center[1] - hand_length * math.cos(angle)
            draw.line([center, (end_x, end_y)], fill=(255, 223, 0), width=4)
            
            dot_radius = 5
            draw.ellipse([center[0]-dot_radius, center[1]-dot_radius,
                         center[0]+dot_radius, center[1]+dot_radius],
                        fill=(255, 223, 0))
            
            frame = np.array(surface)
            rgb = frame[..., :3]
            alpha = frame[..., 3:] / 255.0
            return rgb * alpha + (1 - alpha) * np.array([0, 0, 0])
        
        return VideoClip(make_frame, duration=duration)

    def create_think_animation(self, duration):
        try:
            # Get the correct path whether running as script or executable
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                base_path = sys._MEIPASS
            else:
                # Running as script
                base_path = os.path.dirname(os.path.abspath(__file__))
                
            gif_path = os.path.join(base_path, "think.gif")
            clip = VideoFileClip(gif_path)
            
            w = int(self.width * 0.3)  
            h = int(w * clip.h / clip.w)
            
            clip = clip.resize((w, h), resample="lanczos")
            
            clip = clip.loop(duration=duration)
            
            clip = clip.set_color((255, 223, 0))
            
            return clip
        except Exception as e:
            print(f"Warning: Could not load think.gif - {str(e)}")
            return self._create_fallback_think_animation(duration)
            
    def _create_fallback_think_animation(self, duration):
        w, h = int(self.width * 0.3), int(self.width * 0.2)
        
        def make_frame(t):
            surface = Image.new('RGBA', (w, h), (0, 0, 0, 0))
            draw = ImageDraw.Draw(surface)
            
            phase = t * 2 * math.pi
            
            bubbles = [
                (0.2, 0.8, 15, 0),
                (0.4, 0.7, 20, math.pi/3),
                (0.6, 0.6, 25, 2*math.pi/3),
                (0.8, 0.5, 30, math.pi)
            ]
            
            for x_ratio, y_ratio, size, phase_offset in bubbles:
                x = int(w * x_ratio)
                base_y = int(h * y_ratio)
                y_offset = int(20 * math.sin(phase + phase_offset))
                y = base_y + y_offset
                
                opacity = int(255 * (0.5 + 0.5 * math.sin(phase + phase_offset)))
                
                draw.ellipse([x-size, y-size, x+size, y+size],
                           fill=(255, 223, 0, opacity))
            
            frame = np.array(surface)
            rgb = frame[..., :3]
            alpha = frame[..., 3:] / 255.0
            return rgb * alpha + (1 - alpha) * np.array([0, 0, 0])
        
        return VideoClip(make_frame, duration=duration)

    def create_text_image(self, text, font_size=70, color=(255, 255, 255), is_question=True):
        image = Image.new('RGB', (self.width, self.height), self.background_color)
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        max_width = self.width - (2 * self.margin)
        wrapped_text = wrap(text, width=30)  
        
        bbox = draw.textbbox((0, 0), "hg", font=font)
        line_height = bbox[3] - bbox[1] + 10
        total_height = line_height * len(wrapped_text)
        
        y = (self.height - total_height) // 2
        
        for line in wrapped_text:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            x = (self.width - line_width) // 2  
            
            shadow_offset = 3
            draw.text((x + shadow_offset, y + shadow_offset), line, 
                     font=font, fill=(0, 0, 0))  
            draw.text((x, y), line, font=font, fill=color)  
            
            y += line_height
        
        return image

    def create_text_clip(self, text, duration, font_size=70, color=(255, 255, 255), is_question=True):
        image = self.create_text_image(text, font_size, color, is_question)
        base_clip = ImageClip(np.array(image), duration=duration)
        
        if is_question:
            think_clip = self.create_think_animation(duration)
            think_clip = think_clip.set_position(('center', 0.8), relative=True)
            return CompositeVideoClip([base_clip, think_clip])
        
        return base_clip

    def create_countdown_image(self, number):
        image = Image.new('RGB', (self.width, self.height), self.background_color)
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.truetype("arial.ttf", 200)
        except:
            font = ImageFont.load_default()
        
        text = str(number)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2
        
        shadow_offset = 5
        draw.text((x + shadow_offset, y + shadow_offset), text, 
                 font=font, fill=(0, 0, 0))  
        draw.text((x, y), text, font=font, fill=(255, 223, 0))  
        
        return image

    def create_countdown(self, duration):
        frames = []
        frame_duration = duration / self.countdown_duration  
        
        for i in range(self.countdown_duration, 0, -1):
            base_frame = ImageClip(np.array(self.create_countdown_image(i)), 
                                 duration=frame_duration)
            
            clock_clip = self.create_clock_animation(frame_duration)
            clock_clip = clock_clip.set_position(('center', 0.6), relative=True)
            
            frame_clip = CompositeVideoClip([base_frame, clock_clip])
            frames.append(frame_clip)
        
        return concatenate_videoclips(frames)

    def fetch_trivia_facts(self):
        try:
            response = requests.get('https://opentdb.com/api.php?amount=5&type=multiple')
            data = response.json()
            
            if data['response_code'] == 0:
                return data['results']
            else:
                return None
        except:
            return None

    def generate_video(self, facts=None, progress_callback=None):
        if facts is None:
            facts = self.fetch_trivia_facts()
        
        if not facts:
            print("No facts provided")
            return

        clips = []
        total_steps = len(facts) * 3  # 3 steps per fact: question, countdown, answer
        current_step = 0
        
        for fact in facts:
            # Create question clip
            if progress_callback:
                progress_callback(current_step / total_steps * 100, "Creating question clip...")
            question = html.unescape(fact['question'])
            question_clip = self.create_text_clip(
                question,
                self.duration_per_question,
                color=(255, 223, 0),
                is_question=True
            )
            current_step += 1
            
            # Create countdown
            if progress_callback:
                progress_callback(current_step / total_steps * 100, "Creating countdown animation...")
            countdown = self.create_countdown(self.countdown_duration)
            current_step += 1
            
            # Create answer clip
            if progress_callback:
                progress_callback(current_step / total_steps * 100, "Creating answer clip...")
            answer = html.unescape(fact['correct_answer'])
            answer_clip = self.create_text_clip(
                answer,
                self.answer_duration,
                color=(0, 255, 127),
                is_question=False
            )
            current_step += 1
            
            clips.extend([question_clip, countdown, answer_clip])

        if progress_callback:
            progress_callback(95, "Rendering final video...")
            
        final_clip = concatenate_videoclips(clips)
        
        try:
            # Get the directory of the running script/executable
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                script_dir = os.path.dirname(sys.executable)
            else:
                # Running as script
                script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Create output filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(script_dir, f"trivia_video_{timestamp}.mp4")
            
            # Ensure the output directory exists and is writable
            if not os.access(script_dir, os.W_OK):
                raise PermissionError(f"No write permission in the directory: {script_dir}")
                
            final_clip.write_videofile(
                output_file,
                fps=30,
                codec='libx264',
                audio=False,
                logger=None  # Suppress moviepy stdout logging
            )
            
            if not os.path.exists(output_file):
                raise Exception("Failed to write video file")
                
        except Exception as e:
            print(f"Error writing video file: {str(e)}")
            raise Exception(f"Failed to generate video: {str(e)}")
        finally:
            # Clean up the video clip
            final_clip.close()
            
        if progress_callback:
            progress_callback(100, "Video generated successfully!")
            
        return output_file

if __name__ == "__main__":
    generator = TriviaVideoGenerator()
    generator.generate_video()
