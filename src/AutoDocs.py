import os, ast
from enum import Enum
from Log import log, LogTypes
from pathlib import Path

"""
* Eine neue Anzeige für fehlende Dokumentation, am besten im terminal
* entferne with und nutze den FileManager
"""

GC_TEMP_FOLDER = Path('./temp')
GC_DOCUMENTATION_FOLDER = Path('./docs')
GC_DOCUMENTATION_HEADER = "# Automatic-Documentator by Justus Decker\n\n"
GC_DOCUMENTATION_STATUS_HEADER = '# Documentation Status\n\n|file(object)|type|status|\n|---|---|---|\n'

class StatusTypes(Enum):
    nodoc = '🔴'
    tooshortdoc = '🟡'
    okdoc = '🟢'
    
class DocumentationSettings:
    verbose = False
    documentation_progress_file_creation = False
    documentation_file_creation = True
    exclude_if_contains = []
    
def get_python_paths() -> list[str]:
    """
    Gets all filepaths for python files
    """
    l_return = []
    for t_relative_path, t_folders, t_files in os.walk('./'):
        t_relative_path = t_relative_path.replace('\\','/')
        for t_file in t_files:
            
            if t_file.endswith('.py'):
                p = "/".join([t_relative_path, t_file])
                l_return.append(p)
    return l_return

def print_documentationprogess_line(
    p_lineno: int,
    p_path: str,
    p_ast_name: str,
    p_statustype: str,
    p_currentelement_name: str,
):
    l_path = p_path
    l_ast_name = p_ast_name
    LC_PATH_LENGTH = 40
    LC_ASTNAME_LENGTH = 40
    if p_path.__len__() > LC_PATH_LENGTH:
        l_path = '...' + l_path[3:LC_PATH_LENGTH]
    
    if p_ast_name.__len__() > LC_ASTNAME_LENGTH:
        l_ast_name = l_ast_name[:LC_ASTNAME_LENGTH - 3] + '...'
    if p_lineno >= 1_000_000: raise Exception('p_lineno > 1E6 - not implemented')
    l_current_element_short_name = ' '
    match p_currentelement_name:
        case 'function':
            l_current_element_short_name = 'F'
        case 'class':
            l_current_element_short_name = 'C'
        case _:
            l_current_element_short_name = '!'
            
    match p_statustype:
        case StatusTypes.okdoc.value:
            l_statustype = '\033[32mG\033[0m'
        case StatusTypes.tooshortdoc.value:
            l_statustype = '\033[33mS\033[0m'
        case StatusTypes.nodoc.value:
            l_statustype = '\033[31mB\033[0m'
        case _:
            l_statustype = '\033[35mN\033[0m'
    l_lineno = str(p_lineno)
    max_char_length_map = []

    p_line = f"""
│{l_lineno:<6}│{l_statustype}│{l_current_element_short_name}│{l_ast_name:<40}│{l_path:<40}│
"""[1:-1]
    print(p_line)
    
def print_documentationprogress_header():
    l_line01 = '┌──────┬─┬─┬────────────────────────────────────────┬────────────────────────────────────────┐'
    l_line02 = '│lineno│S│O│                  Name                  │                  Path                  │'
    l_line03 = '├──────┼─┼─┼────────────────────────────────────────┼────────────────────────────────────────┤'
    print(l_line01)
    print(l_line02)
    print(l_line03)
    
def print_documentationprogress_footer():
    l_line = '└──────┴─┴─┴────────────────────────────────────────┴────────────────────────────────────────┘'
    print(l_line)

def generate_docs(p_skip_contains: list[str], p_paths: list[str] = get_python_paths(), p_only_bads: bool = True):
    """
    Creates automatically a README for the coder, you lazy butt :D
    """
    class DocumentationState:
        docsum = 0
        nodocumentation = 0
        hasdocumentation = 0
        tooshortdocumentation = 0
        documentation_string = GC_DOCUMENTATION_HEADER
        status_string = GC_DOCUMENTATION_STATUS_HEADER
        progress_to_print_later = []
        page_entrys = 30
    
    def get_ast_tree(p_path: str):
        with open(p_path, 'rb') as file:
            data = file.read()
        return ast.parse(data)
    
    def get_file_docstring(p_tree: ast.Module)  -> str | None:
        return ast.get_docstring(p_tree)    
    
    def documentation_add_header(p_path: str):
        DocumentationState.documentation_string += f'# {p_path}\n\n'
    
    def documentation_add_filedocs(p_docs: str | None):
        if p_docs is not None:
            DocumentationState.documentation_string += f'{p_docs}\n\n'
    
    def add_status_markdown_line(p_path:str, p_method_or_class:str, p_documentation_progress: StatusTypes, p_declarator: str) -> str:
        DocumentationState.status_string +=f'|[{p_method_or_class}](../{p_path.replace("./","")})|{p_declarator}|{p_documentation_progress}|\n'
    
    def documentation_add_function(p_function_name: str, p_documentation: str):
        DocumentationState.documentation_string += f'## {p_function_name}\n{p_documentation}\n\n'
        
    def documentation_add_class(p_class_name: str, p_documentation: str):
        DocumentationState.documentation_string += f'## {p_class_name}\n{p_documentation}\n\n'
    
    def get_documentation_from_file(p_path: str, p_tree: ast.Module):
        for t_ast in ast.walk(p_tree):
            if isinstance(t_ast, ast.FunctionDef):
                if t_ast.name == '__init__': continue # This is the init dunder, i usually dont comment this
                DocumentationState.docsum += 1
                t_function_documentation = ast.get_docstring(t_ast)
                t_current_element_name = 'function'
                if t_function_documentation is None:
                    DocumentationState.nodocumentation += 1
                    DocumentationState.progress_to_print_later.append([
                        t_ast.lineno,
                        p_path, 
                        t_ast.name, 
                        StatusTypes.nodoc.value, 
                        t_current_element_name])
                    log(
                        "$ : $ $ -> $",
                        [str(StatusTypes.nodoc.value), t_current_element_name, p_path, t_ast.name]
                    )
                    continue
                if len(t_function_documentation) <= 30:
                    DocumentationState.tooshortdocumentation += 1
                    DocumentationState.progress_to_print_later.append([
                        t_ast.lineno,
                        p_path, 
                        t_ast.name, 
                        StatusTypes.tooshortdoc.value, 
                        t_current_element_name])
                    log(
                        "$ : $ $ -> $",
                        [str(StatusTypes.tooshortdoc.value), t_current_element_name, p_path, t_ast.name]
                    )
                else:
                    DocumentationState.hasdocumentation += 1
                    DocumentationState.progress_to_print_later.append([
                        t_ast.lineno,
                        p_path, 
                        t_ast.name, 
                        StatusTypes.okdoc.value, 
                        t_current_element_name])
                    log(
                        "$ : $ $ -> $",
                        [str(StatusTypes.okdoc.value), t_current_element_name, p_path, t_ast.name]
                    )
                documentation_add_function(t_ast.name, t_function_documentation) 

            if isinstance(t_ast, ast.ClassDef):
                DocumentationState.docsum += 1
                t_class_documentation = ast.get_docstring(t_ast)
                t_current_element_name = 'class'
                if t_class_documentation is None:
                    DocumentationState.nodocumentation += 1
                    DocumentationState.progress_to_print_later.append([
                        t_ast.lineno,
                        p_path, 
                        t_ast.name, 
                        StatusTypes.nodoc.value, 
                        t_current_element_name])
                    log(
                        "$ : $ $ -> $",
                        [str(StatusTypes.nodoc.value), t_current_element_name, p_path, t_ast.name]
                    )
                    continue
                if len(t_class_documentation) <= 30:
                    DocumentationState.tooshortdocumentation += 1
                    DocumentationState.progress_to_print_later.append([
                        t_ast.lineno,
                        p_path, 
                        t_ast.name, 
                        StatusTypes.tooshortdoc.value, 
                        t_current_element_name])
                    log(
                        "$ : $ $ -> $",
                        [str(StatusTypes.tooshortdoc.value), t_current_element_name, p_path, t_ast.name]
                    )
                else:
                    DocumentationState.hasdocumentation += 1
                    DocumentationState.progress_to_print_later.append([
                        t_ast.lineno,
                        p_path, 
                        t_ast.name, 
                        StatusTypes.okdoc.value, 
                        t_current_element_name])
                    log(
                        "$ : $ $ -> $",
                        [str(StatusTypes.okdoc.value), t_current_element_name, p_path, t_ast.name]
                    )
                
                documentation_add_class(t_ast.name, t_class_documentation)
    
    for t_path in p_paths:
        if any([word in t_path for word in p_skip_contains]): continue # skips unwanted files
        t_tree = get_ast_tree(t_path)
        documentation_add_header(t_path)
        documentation_add_filedocs(
            get_file_docstring(t_tree)
        )
        get_documentation_from_file(t_path, t_tree)
    print_documentationprogress_header()
    t_ptpl_length = DocumentationState.progress_to_print_later.__len__()
    t_index_without_okay = 0
    for t_index, t_progress in enumerate(DocumentationState.progress_to_print_later):
        if p_only_bads and t_progress[3] == StatusTypes.okdoc.value: continue
        else: t_index_without_okay += 1
        print_documentationprogess_line(*t_progress)

        if t_index_without_okay % DocumentationState.page_entrys == 0 and t_index != 0:
            input(f'Next Page ({t_index // DocumentationState.page_entrys} / {t_ptpl_length // DocumentationState.page_entrys}) ->')
    print_documentationprogress_footer()
    log(
        "$% $ of $",
        [float(f'{(1 - (DocumentationState.nodocumentation / DocumentationState.docsum)) * 100:.2f}'),
         DocumentationState.docsum - DocumentationState.nodocumentation,
         DocumentationState.docsum
         ],
        LogTypes.info
    )
    if not GC_TEMP_FOLDER.is_dir():
        os.mkdir(GC_TEMP_FOLDER)
    with open(str(GC_TEMP_FOLDER)+'/doc_press.yml', 'w') as file:
        file.write(f'progress: {(1 - (DocumentationState.nodocumentation / DocumentationState.docsum)) * 100:.2f}')
    if not GC_DOCUMENTATION_FOLDER.is_dir():
        log(
            "$ does not exist and will be created now",
            [str(GC_DOCUMENTATION_FOLDER)],
            LogTypes.warning
        )
        os.mkdir(GC_DOCUMENTATION_FOLDER)
    from FileManager import overwrite_file
    overwrite_file('./docs/auto-docs.md', DocumentationState.documentation_string.encode())
    overwrite_file('./docs/docs-progress.md', DocumentationState.status_string.encode())



if __name__ == '__main__':
    generate_docs(
        [

        ]
    )