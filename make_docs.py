from instainteracts import InstaInteracts
from pathlib import Path
import pdoc

folder = Path('docs/')

if __name__ == "__main__":
    # Generate new documentation
    print(f'Generating docs at {folder} folder')
    pdoc.render.configure(docformat='google')
    pdoc.pdoc('instainteracts/InstaInteracts.py', output_directory=folder)
