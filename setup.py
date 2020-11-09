import setuptools

setuptools.setup(
    name='eggbot',
    version='0.1.0',
    author='Preocts',
    author_email='preocts@preocts.com',
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    url='https://github.com/Preocts/Egg_Bot',
    license='LICENSE',
    description='A module based Discord bot',
    long_description=open('README.md').read(),
    install_requires=[
        "python-dotenv >= 0.13.0",
        "discord.py >= 1.3.4"
    ],
    scripts=['src/eggbot/egg_bot.py']
)
