DIST ?= development
CMD   = cd examples/cli && python3 main.py --debug --bind 192.168.1.100 --broadcast 192.168.1.255 --listen 192.168.1.100:60001
TCP   = cd examples/cli && python3 main.py --debug --tcp --dest 192.168.1.100

CONTROLLER ?= 405419896

.DEFAULT_GOAL := debug
.PHONY: update
.PHONY: update-release

clean:

update:

update-release:

format: 
	yapf -ri src
	yapf -ri examples/cli
	yapf -ri examples/event-listener
	yapf -ri tests
	yapf -ri integration-tests

build: format
	python3 -m compileall .

test: build
	python3 -m unittest tests/uhppoted/*.py 

integration-tests: build
	python3 -m unittest integration-tests/uhppoted/*.py 

vet: 

lint: 

build-all: test vet lint

release: build-all integration-tests
	rm -rf dist/*
	python3 -m build
	python3 -m twine check dist/* 

publish: release
	echo "Releasing version $(VERSION)"
	gh release create "$(VERSION)" dist/*.tar.gz --draft --prerelease --title "$(VERSION)-beta" --notes-file release-notes.md
	python3 -m twine upload --repository testpypi -u __token__ --skip-existing --verbose dist/*
	python3 -m twine upload --repository pypi     -u __token__ --skip-existing --verbose dist/*

debug: build
	# export UHPPOTED_ENV=DEV && cd examples/async && python3 main.py --debug --timeout 2.5 get-all-controllers
	python3 -m unittest integration-tests/uhppoted/udp_async.py 

usage: build
	$(CMD)

get-all-controllers: build
	export UHPPOTED_ENV=DEV && $(CMD) get-all-controllers

get-controller: build
	export UHPPOTED_ENV=DEV && $(CMD) get-controller --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-controller --controller $(CONTROLLER)

set-ip: build
	export UHPPOTED_ENV=DEV && $(CMD) set-ip --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) set-ip --controller $(CONTROLLER)

get-status: build
	export UHPPOTED_ENV=DEV && $(CMD) get-status --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-status --controller $(CONTROLLER)

get-time: build
	export UHPPOTED_ENV=DEV && $(CMD) get-time --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-time --controller $(CONTROLLER)

set-time: build
	export UHPPOTED_ENV=DEV && $(CMD) set-time --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) set-time --controller $(CONTROLLER)

get-listener: build
	export UHPPOTED_ENV=DEV && $(CMD) get-listener --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-listener --controller $(CONTROLLER)

set-listener: build
	export UHPPOTED_ENV=DEV && $(CMD) set-listener --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) set-listener --controller $(CONTROLLER)

get-door-control: build
	export UHPPOTED_ENV=DEV && $(CMD) get-door-control --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-door-control --controller $(CONTROLLER)

set-door-control: build
	export UHPPOTED_ENV=DEV && $(CMD) set-door-control --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) set-door-control --controller $(CONTROLLER)

open-door: build
	export UHPPOTED_ENV=DEV && $(CMD) open-door --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) open-door --controller $(CONTROLLER)

get-cards: build
	export UHPPOTED_ENV=DEV && $(CMD) get-cards --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-cards --controller $(CONTROLLER)

get-card: build
	export UHPPOTED_ENV=DEV && $(CMD) get-card --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-card --controller $(CONTROLLER)

get-card-by-index: build
	export UHPPOTED_ENV=DEV && $(CMD) get-card-by-index $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-card-by-index $(CONTROLLER)

put-card: build
	export UHPPOTED_ENV=DEV && $(CMD) put-card $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) put-card $(CONTROLLER)

delete-card: build
	export UHPPOTED_ENV=DEV && $(CMD) delete-card $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) delete-card $(CONTROLLER)

delete-all-cards: build
	export UHPPOTED_ENV=DEV && $(CMD) delete-all-cards $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) delete-all-cards $(CONTROLLER)

get-event-index: build
	export UHPPOTED_ENV=DEV && $(CMD) get-event-index $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-event-index $(CONTROLLER)

set-event-index: build
	export UHPPOTED_ENV=DEV && $(CMD) set-event-index $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) set-event-index $(CONTROLLER)

get-event: build
	export UHPPOTED_ENV=DEV && $(CMD) get-event $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-event $(CONTROLLER)

record-special-events: build
	export UHPPOTED_ENV=DEV && $(CMD) record-special-events $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) record-special-events $(CONTROLLER)

get-time-profile: build
	export UHPPOTED_ENV=DEV && $(CMD) get-time-profile $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-time-profile $(CONTROLLER)

set-time-profile: build
	export UHPPOTED_ENV=DEV && $(CMD) set-time-profile $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) set-time-profile $(CONTROLLER)

clear-time-profiles: build
	export UHPPOTED_ENV=DEV && $(CMD) clear-time-profiles $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) clear-time-profiles $(CONTROLLER)

add-task: build
	export UHPPOTED_ENV=DEV && $(CMD) add-task $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) add-task $(CONTROLLER)

refresh-tasklist: build
	export UHPPOTED_ENV=DEV && $(CMD) refresh-tasklist $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) refresh-tasklist $(CONTROLLER)

clear-tasklist: build
	export UHPPOTED_ENV=DEV && $(CMD) clear-tasklist $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) clear-tasklist $(CONTROLLER)

set-pc-control: build
	export UHPPOTED_ENV=DEV && $(CMD) set-pc-control $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) set-pc-control $(CONTROLLER)

set-interlock: build
	export UHPPOTED_ENV=DEV && $(CMD) set-interlock $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) set-interlock $(CONTROLLER)

activate-keypads: build
	export UHPPOTED_ENV=DEV && $(CMD) activate-keypads $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) activate-keypads $(CONTROLLER)

set-door-passcodes: build
	export UHPPOTED_ENV=DEV && $(CMD) set-door-passcodes $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) set-door-passcodes $(CONTROLLER)

get-antipassback: build
	export UHPPOTED_ENV=DEV && $(CMD) get-antipassback $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-antipassback $(CONTROLLER)

set-antipassback: build
	export UHPPOTED_ENV=DEV && $(CMD) set-antipassback --controller $(CONTROLLER) --antipassback "(1,3):(2,4)"
	export UHPPOTED_ENV=DEV && $(TCP) set-antipassback --controller $(CONTROLLER) --antipassback "(1,3):(2,4)"

restore-default-parameters: build
	export UHPPOTED_ENV=DEV && $(CMD) restore-default-parameters $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) restore-default-parameters $(CONTROLLER)

listen: build
	export UHPPOTED_ENV=DEV && $(CMD) listen

all: build
	# export UHPPOTED_ENV=DEV && $(CMD) all
	export UHPPOTED_ENV=DEV && $(CMD) all --destination 192.168.1.100:60000 --timeout 0.5

event-listener: build
	export UHPPOTED_ENV=DEV    && \
	cd examples/event-listener && \
	python3 main.py --debug --bind 192.168.1.100 --broadcast 192.168.1.255 --listen 192.168.1.100:60001

	
