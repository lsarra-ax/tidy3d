from nox_poetry import session

@session(python=["3.10", "3.11", "3.12"])
def tests(session):
    session.install('.[dev]')
    session.run('pytest')

@session
def lint(session):
    session.install('flake8')
    session.run('flake8', '--import-order-style', 'google')
