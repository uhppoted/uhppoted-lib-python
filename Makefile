DIST ?= development
CMD   = cd examples/cli && python3 main.py --debug --bind 192.168.1.100 --broadcast 192.168.1.255 --listen 192.168.1.100:60001
TCP   = cd examples/cli && python3 main.py --debug --tcp --dest 192.168.1.100

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
	# python3 -m unittest integration-tests/uhppoted/udp_dest_addr.py 
	# export UHPPOTED_ENV=DEV && cd examples/cli && python3 main.py --debug --bind 192.168.1.100 --broadcast 192.168.1.255 --udp get-controller
	# export UHPPOTED_ENV=DEV && cd examples/cli && python3 main.py --debug --tcp --bind 192.168.1.100 --dest 192.168.1.100 get-controller
	python3 -m unittest integration-tests/uhppoted/tcp.py 

usage: build
	$(CMD)

get-all-controllers: build
	export UHPPOTED_ENV=DEV && $(CMD) get-all-controllers

get-controller: build
	export UHPPOTED_ENV=DEV && $(CMD) get-controller
	export UHPPOTED_ENV=DEV && $(TCP) get-controller

set-ip: build
	export UHPPOTED_ENV=DEV && $(CMD) set-ip
	export UHPPOTED_ENV=DEV && $(TCP) set-ip

get-status: build
	export UHPPOTED_ENV=DEV && $(CMD) get-status
	export UHPPOTED_ENV=DEV && $(TCP) get-status

get-time: build
	export UHPPOTED_ENV=DEV && $(CMD) get-time
	export UHPPOTED_ENV=DEV && $(TCP) get-time

set-time: build
	export UHPPOTED_ENV=DEV && $(CMD) set-time
	export UHPPOTED_ENV=DEV && $(TCP) set-time

get-listener: build
	export UHPPOTED_ENV=DEV && $(CMD) get-listener
	export UHPPOTED_ENV=DEV && $(TCP) get-listener

set-listener: build
	export UHPPOTED_ENV=DEV && $(CMD) set-listener
	export UHPPOTED_ENV=DEV && $(TCP) set-listener

get-door-control: build
	export UHPPOTED_ENV=DEV && $(CMD) get-door-control
	export UHPPOTED_ENV=DEV && $(TCP) get-door-control

set-door-control: build
	export UHPPOTED_ENV=DEV && $(CMD) set-door-control
	export UHPPOTED_ENV=DEV && $(TCP) set-door-control

open-door: build
	export UHPPOTED_ENV=DEV && $(CMD) open-door
	export UHPPOTED_ENV=DEV && $(TCP) open-door

get-cards: build
	export UHPPOTED_ENV=DEV && $(CMD) get-cards
	export UHPPOTED_ENV=DEV && $(TCP) get-cards

get-card: build
	export UHPPOTED_ENV=DEV && $(CMD) get-card
	export UHPPOTED_ENV=DEV && $(TCP) get-card

get-card-by-index: build
	export UHPPOTED_ENV=DEV && $(CMD) get-card-by-index
	export UHPPOTED_ENV=DEV && $(TCP) get-card-by-index

put-card: build
	export UHPPOTED_ENV=DEV && $(CMD) put-card
	export UHPPOTED_ENV=DEV && $(TCP) put-card

delete-card: build
	export UHPPOTED_ENV=DEV && $(CMD) delete-card
	export UHPPOTED_ENV=DEV && $(TCP) delete-card

delete-cards: build
	export UHPPOTED_ENV=DEV && $(CMD) delete-all-cards
	export UHPPOTED_ENV=DEV && $(TCP) delete-all-cards

get-event-index: build
	export UHPPOTED_ENV=DEV && $(CMD) get-event-index
	export UHPPOTED_ENV=DEV && $(TCP) get-event-index

set-event-index: build
	export UHPPOTED_ENV=DEV && $(CMD) set-event-index
	export UHPPOTED_ENV=DEV && $(TCP) set-event-index

get-event: build
	export UHPPOTED_ENV=DEV && $(CMD) get-event
	export UHPPOTED_ENV=DEV && $(TCP) get-event

record-special-events: build
	export UHPPOTED_ENV=DEV && $(CMD) record-special-events
	export UHPPOTED_ENV=DEV && $(TCP) record-special-events

get-time-profile: build
	export UHPPOTED_ENV=DEV && $(CMD) get-time-profile
	export UHPPOTED_ENV=DEV && $(TCP) get-time-profile

set-time-profile: build
	export UHPPOTED_ENV=DEV && $(CMD) set-time-profile
	export UHPPOTED_ENV=DEV && $(TCP) set-time-profile

clear-time-profiles: build
	export UHPPOTED_ENV=DEV && $(CMD) clear-time-profiles
	export UHPPOTED_ENV=DEV && $(TCP) clear-time-profiles

add-task: build
	export UHPPOTED_ENV=DEV && $(CMD) add-task
	export UHPPOTED_ENV=DEV && $(TCP) add-task

refresh-tasklist: build
	export UHPPOTED_ENV=DEV && $(CMD) refresh-tasklist
	export UHPPOTED_ENV=DEV && $(TCP) refresh-tasklist

clear-tasklist: build
	export UHPPOTED_ENV=DEV && $(CMD) clear-tasklist
	export UHPPOTED_ENV=DEV && $(TCP) clear-tasklist

set-pc-control: build
	export UHPPOTED_ENV=DEV && $(CMD) set-pc-control
	export UHPPOTED_ENV=DEV && $(TCP) set-pc-control

set-interlock: build
	export UHPPOTED_ENV=DEV && $(CMD) set-interlock
	export UHPPOTED_ENV=DEV && $(TCP) set-interlock

activate-keypads: build
	export UHPPOTED_ENV=DEV && $(CMD) activate-keypads
	export UHPPOTED_ENV=DEV && $(TCP) activate-keypads

set-door-passcodes: build
	export UHPPOTED_ENV=DEV && $(CMD) set-door-passcodes
	export UHPPOTED_ENV=DEV && $(TCP) set-door-passcodes

get-antipassback: build
	export UHPPOTED_ENV=DEV && $(CMD) get-antipassback
	export UHPPOTED_ENV=DEV && $(TCP) get-antipassback

set-antipassback: build
	export UHPPOTED_ENV=DEV && $(CMD) set-antipassback # 405419896 '(1,3):(2,4)'
	export UHPPOTED_ENV=DEV && $(TCP) set-antipassback # 405419896 '(1,3):(2,4)'

restore-default-parameters: build
	export UHPPOTED_ENV=DEV && $(CMD) restore-default-parameters
	export UHPPOTED_ENV=DEV && $(TCP) restore-default-parameters

listen: build
	export UHPPOTED_ENV=DEV && $(CMD) listen

all: build
	# export UHPPOTED_ENV=DEV && $(CMD) all
	export UHPPOTED_ENV=DEV && $(CMD) all --destination 192.168.1.100:60000 --timeout 0.5

event-listener: build
	export UHPPOTED_ENV=DEV    && \
	cd examples/event-listener && \
	python3 main.py --debug --bind 192.168.1.100 --broadcast 192.168.1.255 --listen 192.168.1.100:60001

	
