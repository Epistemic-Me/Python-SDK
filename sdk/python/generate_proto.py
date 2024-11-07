import os
import subprocess
import sys
import re
from grpc_tools import protoc

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")

print(f"Using protoc: {subprocess.check_output(['which', 'protoc']).decode().strip()}")
print(f"Protoc version: {subprocess.check_output(['protoc', '--version']).decode().strip()}")

def fix_imports(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace 'from proto.models' with 'from . import'
    content = re.sub(r'from proto\.models', r'from . import', content)

    # Replace 'import proto.models' with 'from . import'
    content = re.sub(r'import proto\.models', r'from . import', content)

    # Replace 'from ..models import import' with 'from . import'
    content = re.sub(r'from \.\.models import import', r'from . import', content)
    content = re.sub(r'from . import import', r'from . import', content)

    # Fix the specific case for epistemic_me_pb2_grpc.py
    content = re.sub(r'from \. import epistemic_me_pb2 as proto_dot_epistemic__me__pb2',
                     r'from . import epistemic_me_pb2 as proto_dot_epistemic__me__pb2', content)

    with open(file_path, 'w') as file:
        file.write(content)

def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    proto_dir = os.path.join(project_root, 'core')
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'epistemic_me', 'generated'))

    # Ensure output directory exists
    os.makedirs(out_dir, exist_ok=True)

    # Find all .proto files
    proto_files = []
    for root, _, files in os.walk(os.path.join(proto_dir, 'proto')):
        for file in files:
            if file.endswith('.proto'):
                proto_files.append(os.path.relpath(os.path.join(root, file), proto_dir))

    # Generate protobuf files
    # cmd = [
    #     sys.executable, '-m', 'grpc_tools.protoc',
    #     f'-I{proto_dir}',
    #     f'--python_out={out_dir}',
    #     f'--grpc_python_out={out_dir}',
    # ] + proto_files



    try:
        # print("Executing command:", ' '.join(cmd))
        # subprocess.run(cmd, check=True, cwd=proto_dir)
        protoc.main([
            'grpc_tools.protoc',
            f'-I{proto_dir}',
            f'--python_out={out_dir}',
            f'--grpc_python_out={out_dir}',
        ] + proto_files)
        print(f"Protobuf files generated in {out_dir}")

        # Fix imports in generated files
        for root, _, files in os.walk(out_dir):
            for file in files:
                if file.endswith('_pb2.py') or file.endswith('_pb2_grpc.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Fix relative imports
                    content = content.replace('from proto.models', 'from .models')
                    content = content.replace('from proto import', 'from . import')
                    
                    with open(file_path, 'w') as f:
                        f.write(content)
                
                # if dir is "models"
                if os.path.basename(root) == "models":
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Fix relative imports
                    content = content.replace('from .models', 'from .')
                    
                    with open(file_path, 'w') as f:
                        f.write(content)

        # Create __init__.py files
        with open(os.path.join(out_dir, 'proto', '__init__.py'), 'w') as f:
            f.write("from . import models\n")
            f.write("from . import epistemic_me_pb2\n")
            f.write("from . import epistemic_me_pb2_grpc\n")

        models_dir = os.path.join(out_dir, 'proto', 'models')
        if os.path.exists(models_dir):
            with open(os.path.join(models_dir, '__init__.py'), 'w') as f:
                for file in os.listdir(models_dir):
                    if file.endswith('_pb2.py'):
                        module_name = file[:-3]  # Remove .py extension
                        f.write(f"from .{module_name} import *\n")

        print("Created __init__.py files")

    except subprocess.CalledProcessError as e:
        print(f"Error generating protobuf files: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
