import tkinter as tk
from tkinter import ttk, messagebox
import requests
from trivia_shorts_generator import TriviaVideoGenerator
import threading
import webbrowser
from PIL import Image, ImageTk
import io
import urllib.request
import os
import sys

class TriviaGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Trivia Video Generator")
        self.root.geometry("400x400")
        self.root.minsize(400, 400)
        self.root.maxsize(400, 400)
        
        # Modern color scheme
        self.colors = {
            'bg': '#1a1a1a',            # Darker background
            'secondary_bg': '#2d2d2d',   # Slightly lighter background
            'accent': '#0078d4',         # Microsoft Blue
            'text': '#ffffff',           # White text
            'text_secondary': '#cccccc', # Light gray text
            'success': '#4CAF50',        # Green
            'error': '#dc3545',          # Red
            'button_hover': '#005fb3'    # Darker blue for hover
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Style configuration
        self.setup_styles()
        self.setup_ui()
        self.load_categories()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('default')
        
        # Configure frame style
        style.configure('Custom.TFrame', 
                       background=self.colors['bg'])
        
        # Configure notebook style
        style.configure('Custom.TNotebook', 
                       background=self.colors['bg'],
                       borderwidth=0)
        style.layout('Custom.TNotebook', [('Custom.TNotebook.client', {'sticky': 'nswe'})])
        
        style.configure('Custom.TNotebook.Tab',
                       background=self.colors['secondary_bg'],
                       foreground=self.colors['text'],
                       padding=[10, 5],
                       font=('Segoe UI', 9, 'bold'),
                       borderwidth=0)
        
        style.layout('TNotebook.Tab', [
            ('Notebook.tab', {
                'sticky': 'nswe',
                'children': [
                    ('Notebook.padding', {
                        'side': 'top',
                        'sticky': 'nswe',
                        'children': [
                            ('Notebook.label', {'side': 'top', 'sticky': ''})
                        ]
                    })
                ]
            })
        ])
        
        style.map('Custom.TNotebook.Tab',
                 background=[('selected', self.colors['accent'])],
                 foreground=[('selected', self.colors['text'])])
        
        # Configure progress bar style
        style.configure('Custom.Horizontal.TProgressbar',
                       troughcolor=self.colors['secondary_bg'],
                       background=self.colors['accent'],
                       darkcolor=self.colors['accent'],
                       lightcolor=self.colors['accent'],
                       bordercolor=self.colors['secondary_bg'])
        
        # Configure label styles
        style.configure('Title.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 14, 'bold'),
                       padding=5)
        
        style.configure('Header.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 10),
                       padding=2)
        
        style.configure('Status.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['text_secondary'],
                       font=('Segoe UI', 9),
                       padding=2)
        
        style.configure('About.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['text_secondary'],
                       font=('Segoe UI', 9),
                       padding=2,
                       wraplength=350)
        
        # Configure button style
        style.configure('Custom.TButton',
                       background=self.colors['accent'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 9, 'bold'),
                       padding=[10, 5])
        
        style.map('Custom.TButton',
                 background=[('active', self.colors['button_hover']),
                           ('disabled', self.colors['secondary_bg'])],
                 foreground=[('disabled', self.colors['text_secondary'])])
        
        # Configure combobox style
        style.configure('Custom.TCombobox',
                       background=self.colors['secondary_bg'],
                       fieldbackground=self.colors['secondary_bg'],
                       foreground=self.colors['text'],
                       arrowcolor=self.colors['text'],
                       font=('Segoe UI', 9))
        
        style.map('Custom.TCombobox',
                 fieldbackground=[('readonly', self.colors['secondary_bg'])],
                 selectbackground=[('readonly', self.colors['secondary_bg'])])

    def setup_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root, style='Custom.TNotebook')
        self.notebook.pack(expand=True, fill='both', padx=0, pady=0)
        
        # Create Home tab
        self.home_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(self.home_frame, text='Home')
        
        # Create About tab
        self.about_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(self.about_frame, text='About')
        
        self.setup_home_tab()
        self.setup_about_tab()

    def setup_home_tab(self):
        # Container frame with padding
        container = ttk.Frame(self.home_frame, style='Custom.TFrame')
        container.pack(expand=True, fill='both', padx=20, pady=15)
        
        # Title
        title_label = ttk.Label(
            container,
            text="Trivia Video Generator",
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 15))
        
        # Category selection
        category_label = ttk.Label(
            container,
            text="Select Category",
            style='Header.TLabel'
        )
        category_label.pack(anchor='w')
        
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            container,
            textvariable=self.category_var,
            style='Custom.TCombobox',
            state='readonly',
            height=5
        )
        self.category_combo.pack(fill='x', pady=(2, 10))
        
        # Number of questions
        questions_label = ttk.Label(
            container,
            text="Number of Questions",
            style='Header.TLabel'
        )
        questions_label.pack(anchor='w')
        
        # Custom entry style
        entry_frame = tk.Frame(container, bg=self.colors['secondary_bg'])
        entry_frame.pack(fill='x', pady=(2, 10))
        
        self.questions_var = tk.StringVar(value="3")
        questions_entry = tk.Entry(
            entry_frame,
            textvariable=self.questions_var,
            font=('Segoe UI', 9),
            bg=self.colors['secondary_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief='flat',
            justify='center'
        )
        questions_entry.pack(fill='x', ipady=5)
        
        # Generate button
        self.generate_button = ttk.Button(
            container,
            text="Generate Video",
            style='Custom.TButton',
            command=self.generate_video
        )
        self.generate_button.pack(pady=15)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            container,
            style='Custom.Horizontal.TProgressbar',
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill='x', pady=5)
        
        # Progress Label
        self.progress_label = ttk.Label(
            container,
            text="",
            style='Status.TLabel',
            justify='center'
        )
        self.progress_label.pack(fill='x')
        
        # Status label
        self.status_label = ttk.Label(
            container,
            text="Ready to generate video",
            style='Status.TLabel',
            justify='center'
        )
        self.status_label.pack(fill='x')

    def setup_about_tab(self):
        # Main container with padding
        container = ttk.Frame(self.about_frame, style='Custom.TFrame')
        container.pack(expand=True, fill='both', padx=20, pady=15)
        
        try:
            # Load and display profile image (smaller size)
            image_url = "https://raw.githubusercontent.com/iTMaster228/iTMaster228/main/dp.png"
            with urllib.request.urlopen(image_url) as url:
                raw_data = url.read()
            image = Image.open(io.BytesIO(raw_data))
            image = image.resize((80, 80), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            image_label = ttk.Label(container, image=photo, style='Custom.TLabel')
            image_label.image = photo
            image_label.pack(pady=5)
        except Exception as e:
            print(f"Error loading profile image: {e}")

        # Name and title
        name_label = ttk.Label(
            container,
            text="Muhammad Saqib",
            style='Title.TLabel'
        )
        name_label.pack(pady=2)

        title_label = ttk.Label(
            container,
            text="Software Developer",
            style='Header.TLabel',
            justify='center'
        )
        title_label.pack(pady=2)

        # Social Links (3x2 grid)
        social_frame = ttk.Frame(container, style='Custom.TFrame')
        social_frame.pack(pady=10)

        # Configure grid columns
        for i in range(3):
            social_frame.grid_columnconfigure(i, weight=1, minsize=100)

        # Main social links in a 3x2 grid
        social_links = [
            ("GitHub", "https://github.com/iTMaster228"),
            ("LinkedIn", "https://www.linkedin.com/in/iTMaster228"),
            ("YouTube", "https://youtube.com/@pakflutterdev"),
            ("Fiverr", "https://www.fiverr.com/itsaqibdev"),
            ("Email", "mailto:itsaqib228@gmail.com"),
            ("WhatsApp", "https://wa.link/yks0k7")
        ]

        for i, (platform, url) in enumerate(social_links):
            btn = ttk.Button(
                social_frame,
                text=platform,
                style='Custom.TButton',
                command=lambda u=url: webbrowser.open(u)
            )
            btn.grid(row=i//3, column=i%3, padx=3, pady=3, sticky='ew')

    def load_categories(self):
        try:
            response = requests.get('https://opentdb.com/api_category.php')
            categories = response.json()['trivia_categories']
            self.categories = {cat['name']: cat['id'] for cat in categories}
            self.category_combo['values'] = list(self.categories.keys())
            self.category_combo.set(list(self.categories.keys())[0])
            self.status_label.config(text="Categories loaded successfully")
        except Exception as e:
            self.status_label.config(text="Failed to load categories")
            messagebox.showerror("Error", f"Failed to load categories: {str(e)}")

    def update_status(self, message, is_error=False):
        self.status_label.config(
            text=message,
            foreground=self.colors['error'] if is_error else self.colors['text']
        )

    def update_progress(self, percentage, message):
        def update():
            self.progress_var.set(percentage)
            self.progress_label.config(text=f"{int(percentage)}%")
            if message:
                self.progress_label.config(text=message)

        self.root.after(0, update)

    def generate_video(self):
        if not hasattr(self, 'categories'):
            self.update_status("Categories not loaded", True)
            return
            
        try:
            num_questions = int(self.questions_var.get())
            if num_questions < 1:
                raise ValueError("Number of questions must be positive")
        except ValueError as e:
            self.update_status(str(e), True)
            return
            
        self.generate_button.state(['disabled'])
        self.update_status("Generating video...")
        self.progress_label.config(text="Fetching questions...")
        
        thread = threading.Thread(target=self._generate_video_thread)
        thread.daemon = True
        thread.start()

    def _generate_video_thread(self):
        try:
            selected_category = self.category_combo.get()
            category_id = self.categories[selected_category]
            num_questions = int(self.questions_var.get())
            
            url = f'https://opentdb.com/api.php?amount={num_questions}&category={category_id}&type=multiple'
            response = requests.get(url)
            data = response.json()
            
            if data['response_code'] != 0:
                raise Exception("Failed to fetch questions")
                
            generator = TriviaVideoGenerator()
            try:
                output_file = generator.generate_video(data['results'], self.update_progress)
                self.update_status("Video generated successfully!", False)
                
                # Get relative path for display
                if getattr(sys, 'frozen', False):
                    base_dir = os.path.dirname(sys.executable)
                else:
                    base_dir = os.path.dirname(os.path.abspath(__file__))
                    
                rel_path = os.path.relpath(output_file, base_dir)
                messagebox.showinfo("Success", f"Video has been generated!\nSaved as: {rel_path}")
                
            except PermissionError as e:
                error_msg = "Permission denied. Please run the application as administrator."
                self.update_status(error_msg, True)
                messagebox.showerror("Error", error_msg)
            except Exception as e:
                error_msg = f"Failed to generate video: {str(e)}"
                self.update_status(error_msg, True)
                messagebox.showerror("Error", error_msg)
            
        except Exception as e:
            self.progress_label.config(text="")
            error_msg = f"Error: {str(e)}"
            self.update_status(error_msg, True)
            messagebox.showerror("Error", error_msg)
        
        finally:
            self.generate_button.state(['!disabled'])
            self.progress_var.set(0)
            self.progress_label.config(text="")

    def run(self):
        # Center the window on the screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()

if __name__ == "__main__":
    app = TriviaGUI()
    app.run()
