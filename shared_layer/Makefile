.PHONY: build-DragonsAppDependencyLayer

build-DragonsAppDependencyLayer:
	mkdir -p "$(ARTIFACTS_DIR)/python"
	cp requirements.txt "$(ARTIFACTS_DIR)/requirements.txt"
	pip install -r "$(ARTIFACTS_DIR)/requirements.txt" -t "$(ARTIFACTS_DIR)/python"
	cp -r * "$(ARTIFACTS_DIR)/python/"
