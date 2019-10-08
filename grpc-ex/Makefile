default: interface

PWD := $(shell pwd)
USER := $(shell id -u $$USER)
PROTOC := docker run --rm -v $(PWD):$(PWD) -u $(USER) -w $(PWD) znly/protoc \
	--plugin=protoc-gen-grpc=/usr/bin/grpc_python_plugin \
 	--python_out=./ --proto_path=:. \
	--grpc_out=./

.phony: interface
interface:
	$(PROTOC) library.proto

.phony: envoy
envoy:
	docker run -it --rm --name envoy -p 9901:9901 -p 8888:8888 \
		-v "$(PWD)/library.pb:/data/library.pb:ro" \
		-v "$(PWD)/envoy.yaml:/etc/envoy/envoy.yaml:ro" \
		envoyproxy/envoy

.phony: descriptor
descriptor:
	$(PROTOC) \
	  	--include_imports \
        --include_source_info \
        --descriptor_set_out=library.pb \
        library.proto
