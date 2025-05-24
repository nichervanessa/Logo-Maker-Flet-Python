import flet as ft
import math
import random
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import json
import os
from datetime import datetime

class LogoMaker:
    def __init__(self):
        self.canvas_width = 400
        self.canvas_height = 400
        self.elements = []
        self.selected_element = None
        self.current_color = "#3366CC"
        self.current_font_size = 24
        self.current_font = "Arial"
        self.background_color = "#FFFFFF"
        self.canvas_image = None
        
    def create_blank_canvas(self):
        """Create a blank canvas"""
        img = Image.new('RGB', (self.canvas_width, self.canvas_height), self.background_color)
        return img
    
    def add_text_element(self, text, x=50, y=50):
        """Add text element to canvas"""
        element = {
            'type': 'text',
            'text': text,
            'x': x,
            'y': y,
            'color': self.current_color,
            'font_size': self.current_font_size,
            'font': self.current_font,
            'id': len(self.elements)
        }
        self.elements.append(element)
        return element
    
    def add_shape_element(self, shape_type, x=100, y=100, width=80, height=80):
        """Add shape element to canvas"""
        element = {
            'type': 'shape',
            'shape': shape_type,
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'color': self.current_color,
            'fill': True,
            'id': len(self.elements)
        }
        self.elements.append(element)
        return element
    
    def render_logo(self):
        """Render the complete logo"""
        img = self.create_blank_canvas()
        draw = ImageDraw.Draw(img)
        
        for element in self.elements:
            if element['type'] == 'text':
                try:
                    font = ImageFont.truetype("arial.ttf", element['font_size'])
                except:
                    font = ImageFont.load_default()
                
                draw.text(
                    (element['x'], element['y']),
                    element['text'],
                    fill=element['color'],
                    font=font
                )
            
            elif element['type'] == 'shape':
                x1, y1 = element['x'], element['y']
                x2, y2 = x1 + element['width'], y1 + element['height']
                
                if element['shape'] == 'rectangle':
                    if element['fill']:
                        draw.rectangle([x1, y1, x2, y2], fill=element['color'])
                    else:
                        draw.rectangle([x1, y1, x2, y2], outline=element['color'], width=2)
                
                elif element['shape'] == 'circle':
                    if element['fill']:
                        draw.ellipse([x1, y1, x2, y2], fill=element['color'])
                    else:
                        draw.ellipse([x1, y1, x2, y2], outline=element['color'], width=2)
                
                elif element['shape'] == 'triangle':
                    points = [
                        (x1 + element['width']//2, y1),  # Top
                        (x1, y2),  # Bottom left
                        (x2, y2)   # Bottom right
                    ]
                    if element['fill']:
                        draw.polygon(points, fill=element['color'])
                    else:
                        draw.polygon(points, outline=element['color'], width=2)
        
        return img
    
    def save_logo(self, filename):
        """Save logo to file"""
        img = self.render_logo()
        if not os.path.exists("logos"):
            os.makedirs("logos")
        filepath = os.path.join("logos", filename)
        img.save(filepath)
        return filepath

def get_color_palette():
    """Return predefined color palettes"""
    return {
        "Professional": ["#1E3A8A", "#3B82F6", "#60A5FA", "#93C5FD", "#DBEAFE"],
        "Vibrant": ["#DC2626", "#EA580C", "#F59E0B", "#10B981", "#3B82F6"],
        "Pastel": ["#FEE2E2", "#FEF3C7", "#D1FAE5", "#DBEAFE", "#E0E7FF"],
        "Monochrome": ["#000000", "#374151", "#6B7280", "#D1D5DB", "#FFFFFF"],
        "Sunset": ["#7C2D12", "#EA580C", "#F59E0B", "#FDE047", "#FEF3C7"],
        "Ocean": ["#0F172A", "#1E293B", "#0EA5E9", "#38BDF8", "#7DD3FC"]
    }

def main(page: ft.Page):
    page.title = "Professional Logo Maker"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1200
    page.window_height = 800
    page.padding = 0
    
    # Initialize logo maker
    logo_maker = LogoMaker()
    
    # Canvas container
    canvas_container = ft.Container(
        width=420,
        height=420,
        bgcolor=ft.colors.WHITE,
        border=ft.border.all(2, ft.colors.GREY_300),
        border_radius=10,
        padding=10
    )
    
    # Preview image container
    preview_image = ft.Image(
        width=400,
        height=400,
        fit=ft.ImageFit.CONTAIN,
        border_radius=5
    )
    
    canvas_container.content = preview_image
    
    # Current settings
    current_color = ft.Container(
        width=40,
        height=40,
        bgcolor=logo_maker.current_color,
        border_radius=20,
        border=ft.border.all(2, ft.colors.GREY_400)
    )
    
    def update_preview():
        """Update the canvas preview"""
        try:
            img = logo_maker.render_logo()
            
            # Convert PIL image to base64 for Flet
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_bytes = buffer.getvalue()
            img_base64 = base64.b64encode(img_bytes).decode()
            
            preview_image.src_base64 = img_base64
            page.update()
        except Exception as e:
            print(f"Preview update error: {e}")
    
    def add_text(e):
        text = text_input.value if text_input.value else "Sample Text"
        logo_maker.add_text_element(text)
        update_preview()
        update_elements_list()
    
    def add_shape(shape_type):
        def handler(e):
            logo_maker.add_shape_element(shape_type)
            update_preview()
            update_elements_list()
        return handler
    
    def change_color(color):
        def handler(e):
            logo_maker.current_color = color
            current_color.bgcolor = color
            page.update()
        return handler
    
    def change_font_size(e):
        try:
            size = int(font_size_slider.value)
            logo_maker.current_font_size = size
            font_size_text.value = f"Font Size: {size}px"
            page.update()
        except:
            pass
    
    def change_background_color(color):
        def handler(e):
            logo_maker.background_color = color
            update_preview()
        return handler
    
    def clear_canvas(e):
        logo_maker.elements = []
        logo_maker.selected_element = None
        update_preview()
        update_elements_list()
    
    def save_logo(e):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"logo_{timestamp}.png"
        try:
            filepath = logo_maker.save_logo(filename)
            show_success_dialog(f"Logo saved as {filename}")
        except Exception as ex:
            show_error_dialog(f"Error saving logo: {str(ex)}")
    
    def show_success_dialog(message):
        dialog = ft.AlertDialog(
            title=ft.Text("Success"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: page.close_dialog())]
        )
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    def show_error_dialog(message):
        dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: page.close_dialog())]
        )
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    def update_elements_list():
        elements_list.controls.clear()
        for i, element in enumerate(logo_maker.elements):
            if element['type'] == 'text':
                icon = ft.icons.TEXT_FIELDS
                desc = f"Text: {element['text'][:20]}..."
            else:
                icon = ft.icons.SHAPE_LINE
                desc = f"Shape: {element['shape']}"
            
            elements_list.controls.append(
                ft.ListTile(
                    leading=ft.Icon(icon),
                    title=ft.Text(desc),
                    trailing=ft.IconButton(
                        icon=ft.icons.DELETE,
                        on_click=lambda e, idx=i: delete_element(idx)
                    )
                )
            )
        page.update()
    
    def delete_element(index):
        if 0 <= index < len(logo_maker.elements):
            logo_maker.elements.pop(index)
            # Update IDs
            for i, element in enumerate(logo_maker.elements):
                element['id'] = i
            update_preview()
            update_elements_list()
    
    def apply_template(template_name):
        def handler(e):
            logo_maker.elements = []
            
            if template_name == "Tech Company":
                logo_maker.background_color = "#1E293B"
                logo_maker.current_color = "#3B82F6"
                logo_maker.add_shape_element("rectangle", 50, 150, 300, 100)
                logo_maker.current_color = "#FFFFFF"
                logo_maker.current_font_size = 32
                logo_maker.add_text_element("TECH CORP", 120, 175)
                
            elif template_name == "Creative Studio":
                logo_maker.background_color = "#FFFFFF"
                logo_maker.current_color = "#EC4899"
                logo_maker.add_shape_element("circle", 100, 100, 200, 200)
                logo_maker.current_color = "#FFFFFF"
                logo_maker.current_font_size = 28
                logo_maker.add_text_element("CREATIVE", 135, 185)
                
            elif template_name == "Minimalist":
                logo_maker.background_color = "#F8FAFC"
                logo_maker.current_color = "#0F172A"
                logo_maker.current_font_size = 36
                logo_maker.add_text_element("BRAND", 140, 180)
                logo_maker.current_color = "#3B82F6"
                logo_maker.add_shape_element("rectangle", 130, 220, 140, 4)
            
            update_preview()
            update_elements_list()
        return handler
    
    # UI Components
    text_input = ft.TextField(
        label="Enter text",
        width=200,
        value="Sample Text"
    )
    
    font_size_slider = ft.Slider(
        min=12,
        max=72,
        value=24,
        divisions=60,
        on_change=change_font_size
    )
    
    font_size_text = ft.Text("Font Size: 24px")
    
    elements_list = ft.Column(height=200, scroll=ft.ScrollMode.AUTO)
    
    # Color palette
    color_palette = get_color_palette()
    color_sections = []
    
    for palette_name, colors in color_palette.items():
        color_row = ft.Row([
            ft.Container(
                width=30,
                height=30,
                bgcolor=color,
                border_radius=15,
                on_click=change_color(color),
                tooltip=color
            ) for color in colors
        ])
        
        color_sections.append(
            ft.Column([
                ft.Text(palette_name, size=12, weight=ft.FontWeight.BOLD),
                color_row
            ])
        )
    
    # Background colors
    bg_colors = ["#FFFFFF", "#F8FAFC", "#1E293B", "#000000", "#FEF3C7", "#D1FAE5"]
    bg_color_row = ft.Row([
        ft.Container(
            width=30,
            height=30,
            bgcolor=color,
            border_radius=15,
            border=ft.border.all(1, ft.colors.GREY_400),
            on_click=change_background_color(color),
            tooltip=f"Background: {color}"
        ) for color in bg_colors
    ])
    
    # Create main layout
    page.add(
        ft.Row([
            # Left Panel - Tools
            ft.Container(
                width=300,
                height=800,
                bgcolor=ft.colors.GREY_50,
                padding=20,
                content=ft.Column([
                    ft.Text("Logo Maker", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    
                    # Text Section
                    ft.Text("Add Text", size=16, weight=ft.FontWeight.BOLD),
                    text_input,
                    ft.ElevatedButton("Add Text", on_click=add_text, width=200),
                    
                    # Font controls
                    font_size_text,
                    font_size_slider,
                    
                    ft.Divider(),
                    
                    # Shapes Section
                    ft.Text("Add Shapes", size=16, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.ElevatedButton("Rectangle", on_click=add_shape("rectangle")),
                        ft.ElevatedButton("Circle", on_click=add_shape("circle")),
                    ]),
                    ft.ElevatedButton("Triangle", on_click=add_shape("triangle"), width=200),
                    
                    ft.Divider(),
                    
                    # Current Color
                    ft.Row([
                        ft.Text("Current Color: "),
                        current_color
                    ]),
                    
                    # Templates
                    ft.Text("Templates", size=16, weight=ft.FontWeight.BOLD),
                    ft.Column([
                        ft.ElevatedButton("Tech Company", on_click=apply_template("Tech Company"), width=200),
                        ft.ElevatedButton("Creative Studio", on_click=apply_template("Creative Studio"), width=200),
                        ft.ElevatedButton("Minimalist", on_click=apply_template("Minimalist"), width=200),
                    ]),
                    
                ], scroll=ft.ScrollMode.AUTO)
            ),
            
            # Center Panel - Canvas
            ft.Container(
                width=450,
                padding=20,
                content=ft.Column([
                    ft.Text("Canvas", size=20, weight=ft.FontWeight.BOLD),
                    canvas_container,
                    
                    # Canvas controls
                    ft.Row([
                        ft.ElevatedButton("Clear All", on_click=clear_canvas, color=ft.colors.RED),
                        ft.ElevatedButton("Save Logo", on_click=save_logo, color=ft.colors.GREEN),
                    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                ])
            ),
            
            # Right Panel - Colors and Elements
            ft.Container(
                width=350,
                height=800,
                bgcolor=ft.colors.GREY_50,
                padding=20,
                content=ft.Column([
                    ft.Text("Color Palettes", size=16, weight=ft.FontWeight.BOLD),
                    
                    ft.Column(color_sections, height=300, scroll=ft.ScrollMode.AUTO),
                    
                    ft.Divider(),
                    
                    ft.Text("Background Colors", size=16, weight=ft.FontWeight.BOLD),
                    bg_color_row,
                    
                    ft.Divider(),
                    
                    ft.Text("Elements", size=16, weight=ft.FontWeight.BOLD),
                    elements_list,
                    
                ], scroll=ft.ScrollMode.AUTO)
            ),
        ])
    )
    
    # Initialize with blank canvas
    update_preview()

if __name__ == "__main__":
    ft.app(target=main)