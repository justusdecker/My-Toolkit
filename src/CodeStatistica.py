from typing import LiteralString
from common.errors import CannotReadFileError
from Log import log, LogTypes
import os
from ConverterUtils import Color, get_colorized_text, convert_byte_ammount
class Language:
    def __init__(self, 
                 p_title: str,
                 p_color: str,
                 p_suffixes: list[str]):
        self.m_color = p_color
        self.m_title = p_title
        self.m_suffixed = p_suffixes
        
class Asset(Language):
    def __init__(self, 
                 p_title: str,
                 p_color: str,
                 p_suffixes: list[str]):
        super().__init__(p_title, p_color, p_suffixes)

GC_LANGUAGES: set[Language] = {
    Language(
        'Python',
        '#3572A5',
        ['py']
    ),
    Language(
        'JavaScript',
        '#F1E05A',
        ['js', 'jsx', 'mjs']
    ),
    Language(
        'TypeScript',
        '#2B7489',
        ['ts', 'tsx']
    ),
    Language(
        'Java',
        '#B07219',
        ['java']
    ),
    Language(
        'C++',
        '#F34B7D',
        ['cpp', 'cc', 'cxx', 'hpp', 'hh', 'hxx']
    ),
    Language(
        'C',
        '#555555',
        ['c', 'h']
    ),
    Language(
        'C#',
        '#178600',
        ['cs']
    ),
    Language(
        'Ruby',
        '#701516',
        ['rb']
    ),
    Language(
        'Go',
        '#00ADD8',
        ['go']
    ),
    Language(
        'PHP',
        '#4F5D95',
        ['php']
    ),
    Language(
        'Swift',
        '#FFAC45',
        ['swift']
    ),
    Language(
        'Kotlin',
        '#F18E33',
        ['kt', 'kts']
    ),
    Language(
        'Rust',
        '#DEA584',
        ['rs']
    ),
    Language(
        'HTML',
        '#E34C26',
        ['html', 'htm']
    ),
    Language(
        'CSS',
        '#563D7C',
        ['css']
    ),
    Language(
        'Shell',
        '#89E051',
        ['sh', 'bash', 'zsh', 'bat', 'cmd']
    ),
    Language(
        'Perl',
        '#0298C3',
        ['pl', 'pm']
    ),
    Language(
        'Lua',
        '#000080',
        ['lua']
    ),
    Language(
        'R',
        '#198CE7',
        ['r']
    ),
    Language(
        'Dart',
        '#00B4AB',
        ['dart']
    ),
    Language(
        'Haskell',
        '#5E5086',
        ['hs']
    ),
    Language(
        'Objective-C',
        '#438EFF',
        ['m', 'mm']
    ),
    Language(  
        'Scala',
        '#C22D40',
        ['scala']
    ),
    Language(
        'Elixir',
        '#6E4A7E',
        ['ex', 'exs']
    ),
    Language(
        'Clojure',
        '#DB5855',
        ['clj', 'cljs', 'cljc']
    ),
    Language(
        'Erlang',
        '#B83998',
        ['erl', 'hrl']
    ),
    Language(
        'F#',
        '#B845FC',
        ['fs', 'fsi', 'fsx']
    ),
    Language(
        'Groovy',
        '#E69F56',
        ['groovy', 'gvy', 'gy', 'gsh']
    ),
    Language(
        'Visual Basis',
        '#945DB7',
        ['vb', 'vbs', 'vbscript']
    ),
    Language(
        'MATLAB',
        '#E16737',
        ['m'] #! Is a duplicate so this will never be selected
    ),
    Language(
        'Julia',
        '#A270BA',
        ['jl']
    ),
    Language(
        'Tcl',
        '#E4CC98',
        ['tcl', 'tk']
    ),
    Language(
        'Markdown',
        '#083FA1',
        ['md']
    ),
    Language(
        'YAML',
        '#CB171E',
        ['yaml', 'yml']
    ),
    Language(
        'JSON',
        '#292929',
        ['json']
    ),
    Language(
        'XML',
        '#0060AC',
        ['xml']
    ),
    Language(
        'Makefile',
        '#427819',
        ['mk', 'makefile']
    ),
    Language(
        'Dockerfile',
        '#384D54',
        ['dockerfile']
    ),
    Language(
        'Terraform',
        '#623CE4',
        ['tf']
    ),
    Language(
        'License',
        '#cccccc',
        ['LICENSE']
    ),
    Language( #! new
        'Config',
        "#515338",
        ['cfg']
    ),
    Language(
        'Text',
        "#666666",
        ['txt']
    )
}

GC_ASSETS: set[Asset] = {
    Asset(
        'Images',
        '#ff00ff',
        [
            'png',
            'jpg',
            'jpeg',
            'gif',
            'webp',
            'svg',
            'tif',
            'tiff',
            'bmp'
        ]
    ),
    Asset(
        'Videos',
        '#ff00ff',
        [
            'mp4',
            'mov',
            'mkv',
            'webm',
            'avi',
            'wmv',
            'flv'
        ]
    ),
    Asset(
        'Audio',
        '#ff00ff',
        [
            'mp3',
            'wav',
            'aiff',
            'flac',
            'aac',
            'm4a',
            'ogg',
            'wma'
        ]
    )
}

GC_FORBIDDEN_FOLDERS = [
    '.git',
    '.vscode',
    '.pytest',
    'build',
    'dist'
]

class LanguageAnalyzer:
        def __init__(self):
            self.m_filecount = 0
            self.m_assetfilecount = 0
            self.m_langs_and_lines: dict[Language, int] = {}
            self.m_assets_and_size: dict[Asset, int] = {}
            
        def add(self, key: Language, value: int) -> None:
            """
            Set a value in m_langs_and_lines, adding to it if the key already exists.
            """
            if key in self.m_langs_and_lines:
                self.m_langs_and_lines[key] += value
            else:
                self.m_langs_and_lines[key] = value
            self.m_filecount += 1

        def add_asset(self, key: Asset, value: int) -> None:
            """
            Set a value in m_langs_and_lines, adding to it if the key already exists.
            """
            if key in self.m_assets_and_size:
                self.m_assets_and_size[key] += value
            else:
                self.m_assets_and_size[key] = value
            self.m_assetfilecount += 1

def get_language_summary(p_relative_path: str) -> LanguageAnalyzer:
    def get_line_count(p_path: str) -> int | type[CannotReadFileError]:
        """
        Get the number of lines in a file.
        Returns `CannotReadFileError` if the file cannot be read.
        """
        try:
            with open(p_path,'rb') as f:
                return f.read().decode().splitlines().__len__()
        except Exception as E:
            log(
                'GetLineCount Error in $ -> $',
                [p_path, E],
                LogTypes.error
            )
            return CannotReadFileError
    def get_filesize(p_path: str) -> int | type[CannotReadFileError]:
        if not os.path.isfile(p_path): return CannotReadFileError
        return os.path.getsize(p_path)
    
    ANALYZER = LanguageAnalyzer()
    
    for t_root, t_dirs, t_files in os.walk('./'):
        for t_file in t_files:
            t_full_path = os.path.join(t_root, t_file)
            if t_full_path.startswith(tuple(GC_FORBIDDEN_FOLDERS)): continue
            
            t_fileextension = t_file.lower().split('.')[-1]
            for t_languageextension in GC_LANGUAGES:
                if t_fileextension not in t_languageextension.m_suffixed: continue
                
                

                t_linecount = get_line_count(t_full_path)
                if t_linecount == CannotReadFileError: continue
                ANALYZER.add(
                    t_languageextension,
                        t_linecount
                )
            for t_assetextension in GC_ASSETS:
                if t_fileextension not in t_assetextension.m_suffixed: continue
                
                t_filesize = get_filesize(t_full_path)
                if t_filesize == CannotReadFileError: continue
                ANALYZER.add_asset(
                    t_assetextension,
                    t_filesize
                )
    return ANALYZER

def get_bar(p_bar_length: int, p_current: float | int, p_total: float | int) -> LiteralString:
    x = '░'
    o = '█'
    percentage = p_current / p_total
    filled_length = int(p_bar_length * percentage)
    bar = o * filled_length + x * (p_bar_length - filled_length)
    return bar



def print_language_summary():
    gls = get_language_summary('',)
    total = sum(gls.m_langs_and_lines.values())
    for res in gls.m_langs_and_lines:
        col = Color(res.m_color)
        print(f'{get_colorized_text(col, get_bar(50, gls.m_langs_and_lines[res], total))} {res.m_title} {gls.m_langs_and_lines[res]} lines')

def print_asset_summary():
    gls = get_language_summary('',)
    total = sum(gls.m_assets_and_size.values())
    for res in gls.m_assets_and_size:
        col = Color(res.m_color)
        print(f'{get_colorized_text(col, get_bar(50, gls.m_assets_and_size[res], total))} {res.m_title} {convert_byte_ammount(gls.m_assets_and_size[res])}')
        
print_language_summary()
print_asset_summary()