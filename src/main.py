import os
import sys
from pathlib import Path
from docx import Document
from PyPDF2 import PdfReader
from PIL import Image
from moviepy import VideoFileClip
from pydub import AudioSegment
from fpdf import FPDF
import customtkinter as ctk
from tkinter import messagebox, filedialog, Tk

if hasattr(sys, '_MEIPASS'):
    BasePath = sys._MEIPASS
else:
    BasePath = os.path.abspath(".")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme(os.path.join(BasePath, "metal.json"))

def ConvertFile(InputPath, OutputExtension):
    InputExtension = Path(InputPath).suffix.lower()
    OutputPath = str(Path(InputPath).with_suffix(OutputExtension))

    if InputExtension in ['.docx', '.txt'] and OutputExtension == '.pdf':
        ConvertTextToPDF(InputPath, OutputPath)
    elif InputExtension == '.pdf' and OutputExtension == '.txt':
        ConvertPDFToText(InputPath, OutputPath)
    elif InputExtension in ['.jpg', '.png', '.bmp', '.gif', '.tiff'] and OutputExtension in ['.jpg', '.png', '.bmp', '.gif', '.tiff']:
        ConvertImage(InputPath, OutputPath)
    elif InputExtension in ['.mp3', '.wav', '.ogg'] and OutputExtension in ['.mp3', '.wav', '.ogg']:
        ConvertAudio(InputPath, OutputPath)
    elif InputExtension in ['.mp4', '.avi', '.mov', '.mkv'] and OutputExtension in ['.mp4', '.avi', '.mov', '.mkv']:
        ConvertVideo(InputPath, OutputPath)
    else:
        raise ValueError('Unsupported conversion')

    return OutputPath

def ConvertTextToPDF(InputPath, OutputPath):
    Pdf = FPDF()
    Pdf.add_page()
    Pdf.set_auto_page_break(auto=True, margin=15)
    Pdf.set_font("Arial", size=12)
    with open(InputPath, 'r', encoding='utf-8') as File:
        for Line in File:
            Pdf.cell(200, 10, txt=Line.strip(), ln=True)
    Pdf.output(OutputPath)

def ConvertPDFToText(InputPath, OutputPath):
    Reader = PdfReader(InputPath)
    Text = ''
    for Page in Reader.pages:
        Text += Page.extract_text() or ''
    with open(OutputPath, 'w', encoding='utf-8') as File:
        File.write(Text)

def ConvertImage(InputPath, OutputPath):
    ImageFile = Image.open(InputPath)
    ImageFile.save(OutputPath)

def ConvertAudio(InputPath, OutputPath):
    Audio = AudioSegment.from_file(InputPath)
    Audio.export(OutputPath, format=Path(OutputPath).suffix.replace('.', ''))

def ConvertVideo(InputPath, OutputPath):
    Video = VideoFileClip(InputPath)
    Video.write_videofile(OutputPath, codec='libx264', audio_codec='aac')

def LaunchUI(InputFile):
    Window = ctk.CTk()
    Window.geometry("400x150")
    Window.title("File Converter")
    Window.iconbitmap(os.path.join(BasePath, "Icon.ico"))
    Window.resizable(False, False)

    ExtensionOptions = {
        '.txt': ['.pdf'],
        '.docx': ['.pdf'],
        '.pdf': ['.txt'],
        '.jpg': ['.png', '.bmp', '.gif'],
        '.png': ['.jpg', '.bmp', '.gif'],
        '.bmp': ['.jpg', '.png'],
        '.gif': ['.jpg', '.png'],
        '.tiff': ['.jpg', '.png'],
        '.mp3': ['.wav', '.ogg'],
        '.wav': ['.mp3', '.ogg'],
        '.ogg': ['.mp3', '.wav'],
        '.mp4': ['.avi', '.mov', '.mkv'],
        '.avi': ['.mp4', '.mov'],
        '.mov': ['.mp4'],
        '.mkv': ['.mp4']
    }

    CurrentExt = Path(InputFile).suffix.lower()
    Options = ExtensionOptions.get(CurrentExt, [])
    if not Options:
        messagebox.showerror("Error", "Unsupported file type")
        return sys.exit(1)

    FormatVar = ctk.StringVar(value=Options[0])

    ctk.CTkLabel(Window, text="Convert to:", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 5))
    FormatDropdown = ctk.CTkOptionMenu(Window, values=Options, variable=FormatVar)
    FormatDropdown.pack()

    def OnConvert():
        try:
            TargetExt = FormatVar.get()

            HiddenRoot = Tk()
            HiddenRoot.withdraw()
            HiddenRoot.attributes('-topmost', True)

            OutputFile = filedialog.asksaveasfilename(
                defaultextension=TargetExt,
                filetypes=[(f"{TargetExt.upper()} file", f"*{TargetExt}")],
                initialfile=Path(InputFile).stem + TargetExt,
                title="Save File"
            )

            HiddenRoot.destroy()

            if not OutputFile:
                return

            ConvertFile(InputFile, Path(OutputFile).suffix)
            sys.exit(0)
        except Exception as E:
            messagebox.showerror("Error", str(E))

    ctk.CTkButton(Window, text="Convert", command=OnConvert, width=175).pack(pady=20)
    Window.mainloop()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)

    LaunchUI(sys.argv[1])
