from argparse import ArgumentParser, BooleanOptionalAction

#TODO
def autocomplete(project: str) -> None:
    pass

#TODO
def generate_report(project: str, template: str) -> None:
    pass

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