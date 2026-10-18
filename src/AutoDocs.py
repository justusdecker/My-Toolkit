import os, ast
from enum import Enum
from Log import log, LogTypes
from pathlib import Path

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

def generate_docs(p_skip_contains: list[str], p_paths: list[str] = get_python_paths()):
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
                    add_status_markdown_line(p_path, t_ast.name, StatusTypes.nodoc.value, t_current_element_name)
                    log(
                        "$ : $ $ -> $",
                        [str(StatusTypes.nodoc.value), t_current_element_name, p_path, t_ast.name]
                    )
                    continue
                if len(t_function_documentation) <= 30:
                    DocumentationState.tooshortdocumentation += 1
                    add_status_markdown_line(p_path, t_ast.name, StatusTypes.tooshortdoc.value, t_current_element_name)
                    log(
                        "$ : $ $ -> $",
                        [str(StatusTypes.tooshortdoc.value), t_current_element_name, p_path, t_ast.name]
                    )
                else:
                    DocumentationState.hasdocumentation += 1
                    add_status_markdown_line(p_path, t_ast.name, StatusTypes.tooshortdoc.value, t_current_element_name)
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
                    add_status_markdown_line(p_path, t_ast.name, StatusTypes.nodoc.value, t_current_element_name)
                    log(
                        "$ : $ $ -> $",
                        [str(StatusTypes.nodoc.value), t_current_element_name, p_path, t_ast.name]
                    )
                    continue
                if len(t_class_documentation) <= 30:
                    DocumentationState.tooshortdocumentation += 1
                    add_status_markdown_line(p_path, t_ast.name, StatusTypes.tooshortdoc.value, t_current_element_name)
                    log(
                        "$ : $ $ -> $",
                        [str(StatusTypes.tooshortdoc.value), t_current_element_name, p_path, t_ast.name]
                    )
                else:
                    DocumentationState.hasdocumentation += 1
                    add_status_markdown_line(p_path, t_ast.name, StatusTypes.okdoc.value, t_current_element_name)
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
    with open('./docs/auto-docs.md', 'wb') as file:
        file.write(DocumentationState.documentation_string.encode())
    with open('./docs/docs-progress.md','wb') as file:
        file.write(DocumentationState.status_string.encode())
if __name__ == '__main__':
    generate_docs(
        [

        ]
    )