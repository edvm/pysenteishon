from cx_Freeze import setup, Executable

packages = ['jinja2', 'netifaces']
build_exe_options = {
    "packages": packages,
    "include_files": [
        ('src/static/', 'static'),
        ('src/templates/', 'templates'),
    ]
}
executables = [
    Executable('src/web.py',
               targetName='pysenteishon',
               )
]

setup(name='pysenteishon',
      version='0.1',
      options={'build_exe': build_exe_options},
      description='Control your slides with your smartphone touchscreen',
      executables=executables
      )
