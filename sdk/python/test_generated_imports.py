import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_imports():
    imports_to_test = [
        ('epistemic_me.generated.proto.epistemic_me_pb2', 'epistemic_me_pb2'),
        ('epistemic_me.generated.proto.epistemic_me_pb2_grpc', 'epistemic_me_pb2_grpc'),
        ('epistemic_me.generated.proto.models.beliefs_pb2', 'beliefs_pb2'),
        ('epistemic_me.generated.proto.models.dialectic_pb2', 'dialectic_pb2')
    ]

    for import_path, module_name in imports_to_test:
        try:
            __import__(import_path)
            print(f"Successfully imported {module_name}")
        except ImportError as e:
            print(f"Failed to import {module_name}: {e}")

if __name__ == "__main__":
    test_imports()
