from invoke import task
from os import path, getcwd

@task
def extracredit(
    c,
    division,
    results,
    survey=path.join('credit', 'survey.csv'),
    config=path.join('..', 'config', 'development.py'),
):

    output_folder = path.join(getcwd(), 'credit', division)

    with c.prefix(f"export FLASK_CONFIG={config}"):
        c.run(f"mkdir -p {output_folder}")
        c.run(f"python extra_credit.py {results} {survey} {output_folder}")

