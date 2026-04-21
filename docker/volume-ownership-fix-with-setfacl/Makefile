.PHONY: help fix-data-volume-permissions
.DEFAULT_GOAL := help

HOST_UID ?= $(shell id -u)
HOST_GID ?= $(shell id -g)
APP_UID ?= 1001
APP_GID ?= 1001

# You may want to install awk if you don't have already
help: ## show make targets
	@printf "\n\033[1mAvailable Commands\033[0m\n\n"
	@printf "Usage:\n  make <target>\n\n"
	@awk 'BEGIN {FS = ":.*## "; cyan = "\033[36m"; bold = "\033[1m"; red = "\033[31m"; reset = "\033[0m"; printf "%sAvailable targets%s\n\n", bold, reset} /^[a-zA-Z0-9_.-]+:.*## / {desc = $$2; is_danger = desc ~ /#__danger /; gsub(/#__danger /, "", desc); printf "  %s%s%s\n", cyan, $$1, reset; printf "      %s%s%s\n\n", is_danger ? red "[DANGER] " : "", desc, reset }' $(MAKEFILE_LIST)

fix-data-volume-permissions: ## fix bidirectional permissions for host and container users on data volume
	@mkdir -p data
	# chmod first to avoid shrinking ACL mask after ACL rules are in place.
	sudo chmod 2775 data
	# Ensure existing files/dirs are writable by both users.
	sudo setfacl -R -m u:$(HOST_UID):rwX,u:$(APP_UID):rwX,m:rwX data
	# Ensure future files inherit the same ACLs from directories.
	sudo setfacl -R -d -m u:$(HOST_UID):rwx,u:$(APP_UID):rwx,m:rwx data
	sudo setfacl -m u:$(HOST_UID):rwx,u:$(APP_UID):rwx,m:rwx data
	sudo setfacl -d -m u:$(HOST_UID):rwx,u:$(APP_UID):rwx,m:rwx data
	@printf "Applied ACLs on ./data for host UID=%s and app UID=%s\n" "$(HOST_UID)" "$(APP_UID)"