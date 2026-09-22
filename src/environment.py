import shutil

def check_environment():
    tools={name:shutil.which(name) for name in ('iverilog','vvp')}
    return {'python':True,'iverilog':bool(tools['iverilog']),'vvp':bool(tools['vvp']),'paths':tools}
