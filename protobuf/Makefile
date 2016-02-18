service_pb2.py: service.proto
	protoc --python_out=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_python_plugin` service.proto
