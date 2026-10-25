
GC_GITIGNORE = {
    'default': [
        '.vscode/',
        '.env',
        '*.exe',
        'todo.md',
        'docs-progess.md',
        'test.*',
        'database/*',
        '*.db'
    ],
    'on_python': [
        '*.pyc',
        ],
    'assets': [
        # Images
        '*.png',
        '*.jpg',
        '*.jpeg',
        '*.gif',
        '*.webp',
        '*.svg',
        '*.tif',
        '*.tiff',
        '*.bmp',
        # Videos
        '*.mp4',
        '*.mov',
        '*.mkv',
        '*.webm',
        '*.avi',
        '*.wmv',
        '*.flv',
        # Audio
        '*.mp3',
        '*.wav',
        '*.aiff',
        '*.flac',
        '*.aac',
        '*.m4a',
        '*.ogg',
        '*.wma',
        
        # Not if in assets/
        '!assets/*.png',
        '!assets/*.jpg',
        '!assets/*.jpeg',
        '!assets/*.gif',
        '!assets/*.webp',
        '!assets/*.svg',
        '!assets/*.tif',
        '!assets/*.tiff',
        '!assets/*.bmp',
        # Videos
        '!assets/*.mp4',
        '!assets/*.mov',
        '!assets/*.mkv',
        '!assets/*.webm',
        '!assets/*.avi',
        '!assets/*.wmv',
        '!assets/*.flv',
        # Audio
        '!assets/*.mp3',
        '!assets/*.wav',
        '!assets/*.aiff',
        '!assets/*.flac',
        '!assets/*.aac',
        '!assets/*.m4a',
        '!assets/*.ogg',
        '!assets/*.wma',
        
        # Not if in demo/
        '!demo/*.png',
        '!demo/*.jpg',
        '!demo/*.jpeg',
        '!demo/*.gif',
        '!demo/*.webp',
        '!demo/*.svg',
        '!demo/*.tif',
        '!demo/*.tiff',
        '!demo/*.bmp',
        # Videos
        '!demo/*.mp4',
        '!demo/*.mov',
        '!demo/*.mkv',
        '!demo/*.webm',
        '!demo/*.avi',
        '!demo/*.wmv',
        '!demo/*.flv',
        # Audio
        '!demo/*.mp3',
        '!demo/*.wav',
        '!demo/*.aiff',
        '!demo/*.flac',
        '!demo/*.aac',
        '!demo/*.m4a',
        '!demo/*.ogg',
        '!demo/*.wma',
    ]
}

def create_gitignore(p_options: list[str]):
    with open('.gitignore', 'w') as f:
        for t_option in p_options:
            if t_option not in GC_GITIGNORE:
                continue
            f.write(f'# {t_option}\n\n')
            for t_entry in GC_GITIGNORE[t_option]:
                f.write(f'{t_entry}\n')
            f.write('\n')
            
create_gitignore(
    [
        'default',
        'on_python',
        'assets'
    ]
)