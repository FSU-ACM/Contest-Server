from invoke import task
from os import path, getcwd

@task
def extracredit(
    c,
    division,
    results,
    survey=path.join('credit', 'survey.csv'),
    config=path.join('..', 'config', 'production.py'),
):

    output_folder = path.join(getcwd(), 'credit', division)
    if division.lower() == 'lower':
        division = 2
    else:
        division = 1

    with c.prefix(f"export FLASK_CONFIG={config}"):
        c.run(f"mkdir -p {output_folder}")
        c.run(f"python extra_credit_new.py {results} {output_folder} {division}")

