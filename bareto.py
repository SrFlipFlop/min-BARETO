from os import listdir
from yaml import load, dump
from datetime import datetime
from docxtpl import DocxTemplate
from yaml.loader import SafeLoader
from yaml.dumper import SafeDumper
from os.path import isfile, dirname, realpath, join
from argparse import ArgumentParser, BooleanOptionalAction

def check_vuln_template(template: dict) -> bool:
    vuln_required_fields = ['name', 'description', 'impact', 'recomendations']
    for field in vuln_required_fields:
        if field not in template:
            print(f'[!] Vulnerability template not valid {template} - Field {field} not found')
            return False
    return True

def load_template(path: str) -> dict:
    if isfile(path) and path.endswith('.yaml'):
        with open(path, 'r') as f:
            template = load(f, SafeLoader)
            if check_vuln_template(template):
                return template

def get_vuln_templates() -> list:
    templates = []
    path = join(dirname(realpath(__file__)), 'templates/vulnerabilities/')
    for file in listdir(path):
        file_path = join(path, file)
        templates.append(load_template(file_path))
    return templates

def load_project(path: str) -> dict:
    if isfile(path) and path.endswith('.yaml'):
        with open(path, 'r') as f:
            return load(f, SafeLoader)

def merge_template(template: dict, project: dict) -> None:
    if template['name'] in project['autocomplete']:
        vuln = {template['name']: {}}
        for field in ['description', 'impact', 'recomendations']:
            vuln[template['name']][field] = template[field]['fields']

        project['vulnerabilities'].append(vuln)
        print(f'[+] Updated {template["name"]} vulnerability')

def autocomplete(path: str) -> None:
    project = load_project(path)
    project['vulnerabilities'] = []
    
    for template in get_vuln_templates():
        merge_template(template, project)
    
    with open(path, 'w') as f:
        dump(project, f, SafeDumper)

#TODO
def create_executive(project: dict, context: dict) -> None:
    pass

#TODO
def create_summary(project: dict, context: dict) -> None:
    pass

#TODO
def create_vulnerabilities(project: dict, context: dict) -> None:
    pass

def generate_report(project: str, template: str) -> None: 
    context = {}
    project = load_project(project)
    create_executive(project, context) 
    create_summary(project, context)
    create_vulnerabilities(project, context)   
    
    doc = DocxTemplate(template)
    doc.render(context)
    doc.save(template.replace('.docx', f'_v0.1.docx'))

def main():
    parser = ArgumentParser(description='min-BARETO is a lightweight report generator tool that uses YAML templates for the vulnerabilities.')
    parser.add_argument('-p', '--project', required=True, help='TODO')
    parser.add_argument('-a', '--autocomplete', action=BooleanOptionalAction, help='TODO')
    parser.add_argument('-t', '--template', help='TODO')
    args = parser.parse_args()

    if args.autocomplete:
        autocomplete(args.project)

    if args.template:
        generate_report(args.project, args.template)

if __name__ == '__main__':
    main()