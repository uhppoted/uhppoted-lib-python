DIST ?= development
CMD   = cd examples/cli && python3 main.py --debug --bind 192.168.1.100 --broadcast 192.168.1.255 --listen 192.168.1.100:60001
TCP   = cd examples/cli && python3 main.py --debug --tcp --dest 192.168.1.100
ASYNC = cd examples/async && python3 main.py --debug --bind 192.168.1.100 --broadcast 192.168.1.255 --listen 192.168.1.100:60001
ASYNC_TCP = cd examples/async && python3 main.py --debug --tcp --dest 192.168.1.100

CONTROLLER ?= 405419896
CARD ?= 1058400

.DEFAULT_GOAL := debug
.PHONY: update
.PHONY: update-release

clean:

update:

update-release:

format: 
	black src
	black examples/cli
	black examples/async
	black examples/event-listener
	black examples/async-event-listener
	black tests
	black integration-tests

build: format
	python3 -m compileall .

test: build
	python3 -m unittest tests/uhppoted/*.py 

integration-tests: build
	python3 -m unittest integration-tests/uhppoted/*.py 

vet: 

lint: 
	pylint --rcfile=.pylintrc  examples/cli

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
#	export UHPPOTED_ENV=DEV && $(ASYNC)     get-time --controller $(CONTROLLER)
#	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) get-time --controller $(CONTROLLER)
	python3 -m unittest integration-tests/uhppoted/async_*.py 

usage: build
	$(CMD)

get-all-controllers: build
	export UHPPOTED_ENV=DEV && $(CMD) get-all-controllers

get-all-controllers-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC) get-all-controllers

get-controller: build
	export UHPPOTED_ENV=DEV && $(CMD) get-controller --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-controller --controller $(CONTROLLER)

get-controller-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     get-controller --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) get-controller --controller $(CONTROLLER)

set-ip: build
	export UHPPOTED_ENV=DEV && $(CMD) set-ip --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) set-ip --controller $(CONTROLLER)

set-ip-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     set-ip --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) set-ip --controller $(CONTROLLER)

get-status: build
	export UHPPOTED_ENV=DEV && $(CMD) get-status --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-status --controller $(CONTROLLER)

get-status-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     get-status --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) get-status --controller $(CONTROLLER)

get-time: build
	export UHPPOTED_ENV=DEV && $(CMD) get-time --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-time --controller $(CONTROLLER)

get-time-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     get-time --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) get-time --controller $(CONTROLLER)

set-time: build
	export UHPPOTED_ENV=DEV && $(CMD) set-time --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) set-time --controller $(CONTROLLER)

set-time-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     set-time --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) set-time --controller $(CONTROLLER)

get-listener: build
	export UHPPOTED_ENV=DEV && $(CMD) get-listener --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-listener --controller $(CONTROLLER)

get-listener-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     get-listener --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) get-listener --controller $(CONTROLLER)

set-listener: build
	export UHPPOTED_ENV=DEV && $(CMD) set-listener --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) set-listener --controller $(CONTROLLER)

set-listener-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     set-listener --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) set-listener --controller $(CONTROLLER)

get-door-control: build
	export UHPPOTED_ENV=DEV && $(CMD) get-door-control --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-door-control --controller $(CONTROLLER)

get-door-control-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     get-door-control --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) get-door-control --controller $(CONTROLLER)

set-door-control: build
	export UHPPOTED_ENV=DEV && $(CMD) set-door-control --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) set-door-control --controller $(CONTROLLER)

set-door-control-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     set-door-control --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) set-door-control --controller $(CONTROLLER)

open-door: build
	export UHPPOTED_ENV=DEV && $(CMD) open-door --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) open-door --controller $(CONTROLLER)

open-door-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     open-door --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) open-door --controller $(CONTROLLER)

get-cards: build
	export UHPPOTED_ENV=DEV && $(CMD) get-cards --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-cards --controller $(CONTROLLER)

get-cards-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     get-cards --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) get-cards --controller $(CONTROLLER)

get-card: build
	export UHPPOTED_ENV=DEV && $(CMD) get-card --controller $(CONTROLLER) --card $(CARD)
	export UHPPOTED_ENV=DEV && $(TCP) get-card --controller $(CONTROLLER) --card $(CARD)

get-card-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     get-card --controller $(CONTROLLER) --card $(CARD)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) get-card --controller $(CONTROLLER) --card $(CARD)

get-card-by-index: build
	export UHPPOTED_ENV=DEV && $(CMD) get-card-by-index --controller $(CONTROLLER) --index 3
	export UHPPOTED_ENV=DEV && $(TCP) get-card-by-index --controller $(CONTROLLER) --index 3

get-card-by-index-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     get-card-by-index --controller $(CONTROLLER) --index 3
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) get-card-by-index --controller $(CONTROLLER) --index 3

put-card: build
	export UHPPOTED_ENV=DEV && $(CMD) put-card --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) put-card --controller $(CONTROLLER)

put-card-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     put-card --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) put-card --controller $(CONTROLLER)

delete-card: build
	export UHPPOTED_ENV=DEV && $(CMD) delete-card --controller $(CONTROLLER) --card $(CARD)
	export UHPPOTED_ENV=DEV && $(TCP) delete-card --controller $(CONTROLLER) --card $(CARD)

delete-card-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     delete-card --controller $(CONTROLLER) --card $(CARD)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) delete-card --controller $(CONTROLLER) --card $(CARD)

delete-all-cards: build
	export UHPPOTED_ENV=DEV && $(CMD) delete-all-cards --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) delete-all-cards --controller $(CONTROLLER)

delete-all-cards-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     delete-all-cards --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) delete-all-cards --controller $(CONTROLLER)

get-event: build
	export UHPPOTED_ENV=DEV && $(CMD) get-event --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-event --controller $(CONTROLLER)

get-event-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     get-event --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) get-event --controller $(CONTROLLER)

get-event-index: build
	export UHPPOTED_ENV=DEV && $(CMD) get-event-index --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-event-index --controller $(CONTROLLER)

get-event-index-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     get-event-index --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) get-event-index --controller $(CONTROLLER)

set-event-index: build
	export UHPPOTED_ENV=DEV && $(CMD) set-event-index --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) set-event-index --controller $(CONTROLLER)

set-event-index-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     set-event-index --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) set-event-index --controller $(CONTROLLER)

record-special-events: build
	export UHPPOTED_ENV=DEV && $(CMD) record-special-events --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) record-special-events --controller $(CONTROLLER)

record-special-events-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     record-special-events --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) record-special-events --controller $(CONTROLLER)

get-time-profile: build
	export UHPPOTED_ENV=DEV && $(CMD) get-time-profile --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-time-profile --controller $(CONTROLLER)

get-time-profile-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     get-time-profile --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) get-time-profile --controller $(CONTROLLER)

set-time-profile: build
	export UHPPOTED_ENV=DEV && $(CMD) set-time-profile --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) set-time-profile --controller $(CONTROLLER)

set-time-profile-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     set-time-profile --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) set-time-profile --controller $(CONTROLLER)

clear-time-profiles: build
	export UHPPOTED_ENV=DEV && $(CMD) clear-time-profiles --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) clear-time-profiles --controller $(CONTROLLER)

clear-time-profiles-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     clear-time-profiles --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) clear-time-profiles --controller $(CONTROLLER)

add-task: build
	export UHPPOTED_ENV=DEV && $(CMD) add-task --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) add-task --controller $(CONTROLLER)

add-task-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     add-task --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) add-task --controller $(CONTROLLER)

refresh-tasklist: build
	export UHPPOTED_ENV=DEV && $(CMD) refresh-tasklist --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) refresh-tasklist --controller $(CONTROLLER)

refresh-tasklist-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     refresh-tasklist --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) refresh-tasklist --controller $(CONTROLLER)

clear-tasklist: build
	export UHPPOTED_ENV=DEV && $(CMD) clear-tasklist --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) clear-tasklist --controller $(CONTROLLER)

clear-tasklist-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     clear-tasklist --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) clear-tasklist --controller $(CONTROLLER)

set-pc-control: build
	export UHPPOTED_ENV=DEV && $(CMD) set-pc-control --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) set-pc-control --controller $(CONTROLLER)

set-pc-control-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     set-pc-control --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) set-pc-control --controller $(CONTROLLER)

set-interlock: build
	export UHPPOTED_ENV=DEV && $(CMD) set-interlock --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) set-interlock --controller $(CONTROLLER)

set-interlock-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     set-interlock --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) set-interlock --controller $(CONTROLLER)

activate-keypads: build
	export UHPPOTED_ENV=DEV && $(CMD) activate-keypads --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) activate-keypads --controller $(CONTROLLER)

activate-keypads-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     activate-keypads --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) activate-keypads --controller $(CONTROLLER)

set-door-passcodes: build
	export UHPPOTED_ENV=DEV && $(CMD) set-door-passcodes --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) set-door-passcodes --controller $(CONTROLLER)

set-door-passcodes-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     set-door-passcodes --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) set-door-passcodes --controller $(CONTROLLER)

get-antipassback: build
	export UHPPOTED_ENV=DEV && $(CMD) get-antipassback --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) get-antipassback --controller $(CONTROLLER)

get-antipassback-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     get-antipassback --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) get-antipassback --controller $(CONTROLLER)

set-antipassback: build
	export UHPPOTED_ENV=DEV && $(CMD) set-antipassback --controller $(CONTROLLER) --antipassback "(1,3):(2,4)"
	export UHPPOTED_ENV=DEV && $(TCP) set-antipassback --controller $(CONTROLLER) --antipassback "(1,3):(2,4)"

set-antipassback-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     set-antipassback --controller $(CONTROLLER) --antipassback "(1,3):(2,4)"
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) set-antipassback --controller $(CONTROLLER) --antipassback "(1,3):(2,4)"

restore-default-parameters: build
	export UHPPOTED_ENV=DEV && $(CMD) restore-default-parameters --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(TCP) restore-default-parameters --controller $(CONTROLLER)

restore-default-parameters-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC)     restore-default-parameters --controller $(CONTROLLER)
	export UHPPOTED_ENV=DEV && $(ASYNC_TCP) restore-default-parameters --controller $(CONTROLLER)

listen: build
	export UHPPOTED_ENV=DEV && $(CMD) listen

listen-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC) listen

all: build
	# export UHPPOTED_ENV=DEV && $(CMD) all
	export UHPPOTED_ENV=DEV && $(CMD) all --destination 192.168.1.100:60000 --timeout 0.5

all-async: build
	export UHPPOTED_ENV=DEV && $(ASYNC) all --destination 192.168.1.100:60000 --timeout 0.5

event-listener: build
	export UHPPOTED_ENV=DEV    && \
	cd examples/event-listener && \
	python3 main.py --debug --bind 192.168.1.100 --broadcast 192.168.1.255 --listen 192.168.1.100:60001

event-listener-async: build
	export UHPPOTED_ENV=DEV          && \
	cd examples/async-event-listener && \
	python3 main.py --debug --bind 192.168.1.100 --broadcast 192.168.1.255 --listen 192.168.1.100:60001

	
