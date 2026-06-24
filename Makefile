DIST ?= development
CMD   = python3 -m examples.cli.main --debug --bind 192.168.1.125 --broadcast 192.168.1.255 --listen 192.168.1.125:60001
TCP   = python3 -m examples.cli.main --debug --tcp --dest 192.168.1.125
ASYNC = python3 -m examples.async.cli.main --debug --bind 192.168.1.125 --broadcast 192.168.1.255 --listen 192.168.1.125:60001
ASYNC_TCP = python3 -m examples.async.cli.main --debug --tcp --dest 192.168.1.125

CONTROLLER ?= 405419896
DOOR ?= 3
EVENT ?= 37
LISTENER ?= 192.168.1.125:60001
CARD ?= 1058400
PROFILE ?= 29
ANTIPASSBACK ?= (1,3):(2,4)
FIRSTCARD ?= 08:30,16:45,normally open,firstcard only,[Mon,Tues,Fri]

.DEFAULT_GOAL := debug
.PHONY: update
.PHONY: update-release

clean:

update:

update-release:

format: 
	. .venv/bin/activate; black src
	. .venv/bin/activate; black examples/cli
	. .venv/bin/activate; black examples/event_listener
	. .venv/bin/activate; black examples/async/cli
	. .venv/bin/activate; black examples/async/event_listener
	. .venv/bin/activate; black tests
	. .venv/bin/activate; black integration_tests

build: format
	. .venv/bin/activate; python3 -m compileall .

test: build
	. .venv/bin/activate; python3 -m unittest tests/uhppoted/*.py 

integration-tests: build
	. .venv/bin/activate; python3 -m unittest integration_tests/uhppoted/*.py 

vet: 

lint: 
	. .venv/bin/activate; pylint --rcfile=.pylintrc  --disable=duplicate-code src
	. .venv/bin/activate; pylint --rcfile=.pylintrc examples/cli
	. .venv/bin/activate; pylint --rcfile=.pylintrc examples/event_listener
	. .venv/bin/activate; pylint --rcfile=.pylintrc examples/async/cli
	. .venv/bin/activate; pylint --rcfile=.pylintrc examples/async/event_listener
	. .venv/bin/activate; pylint --rcfile=.pylintrc tests
	. .venv/bin/activate; pylint --rcfile=.pylintrc tests/uhppoted
	. .venv/bin/activate; pylint --rcfile=.pylintrc integration_tests
	. .venv/bin/activate; pylint --rcfile=.pylintrc --disable=duplicate-code integration_tests/uhppoted

build-all: test vet lint

release: build-all integration-tests
	rm -rf dist/*
	. .venv/bin/activate; python3 -m build
	. .venv/bin/activate; python3 -m twine check dist/* 

publish: release
	echo "Releasing version $(VERSION)"
# 	gh release create "$(VERSION)" dist/*.tar.gz --draft --prerelease --title "$(VERSION)-beta" --notes-file release-notes.md
	. .venv/bin/activate; python3 -m twine upload --repository testpypi -u __token__ --skip-existing --verbose dist/*
	. .venv/bin/activate; python3 -m twine upload --repository pypi     -u __token__ --skip-existing --verbose dist/*

debug:
# 	$(ASYNC)                                   get-all-controllers
# 	$(ASYNC) --destination 192.168.1.125 --udp get-controller --controller $(CONTROLLER)
# 	$(ASYNC)                             --udp get-controller --controller $(CONTROLLER)
	python3 -m examples.cli.main --debug --broadcast 192.168.1.255 get-all-controllers

usage: build
	-$(CMD)
	-$(ASYNC)
	-$(CMD)   do-weird-stuff
	-$(ASYNC) do-weird-stuff

get-all-controllers: build
	$(CMD) get-all-controllers

get-all-controllers-async: build
	$(ASYNC) get-all-controllers

get-controller: build
	$(CMD) get-controller --controller $(CONTROLLER)
	$(TCP) get-controller --controller $(CONTROLLER)

get-controller-async: build
	$(ASYNC)     get-controller --controller $(CONTROLLER)
	$(ASYNC_TCP) get-controller --controller $(CONTROLLER)

set-ip: build
	$(CMD) set-ip --controller $(CONTROLLER)
	$(TCP) set-ip --controller $(CONTROLLER)

set-ip-async: build
	$(ASYNC)     set-ip --controller $(CONTROLLER)
	$(ASYNC_TCP) set-ip --controller $(CONTROLLER)

get-status: build
	$(CMD) get-status --controller $(CONTROLLER)
	$(TCP) get-status --controller $(CONTROLLER)

get-status-record: build
	$(CMD) get-status-record --controller $(CONTROLLER)

get-status-async: build
	$(ASYNC)     get-status --controller $(CONTROLLER)
	$(ASYNC_TCP) get-status --controller $(CONTROLLER)

get-status-record-async: build
	$(ASYNC) get-status-record --controller $(CONTROLLER)

get-time: build
	$(CMD) get-time --controller $(CONTROLLER)
	$(TCP) get-time --controller $(CONTROLLER)

get-time-async: build
	$(ASYNC)     get-time --controller $(CONTROLLER)
	$(ASYNC_TCP) get-time --controller $(CONTROLLER)

set-time: build
	$(CMD) set-time --controller $(CONTROLLER)
	$(TCP) set-time --controller $(CONTROLLER)

set-time-async: build
	$(ASYNC)     set-time --controller $(CONTROLLER)
	$(ASYNC_TCP) set-time --controller $(CONTROLLER)

get-listener: build
	$(CMD) get-listener --controller $(CONTROLLER)
	$(TCP) get-listener --controller $(CONTROLLER)

get-listener-async: build
	$(ASYNC)     get-listener --controller $(CONTROLLER)
	$(ASYNC_TCP) get-listener --controller $(CONTROLLER)

set-listener: build
	$(CMD) set-listener --controller $(CONTROLLER)
	$(ASYNC) set-listener --controller $(CONTROLLER) --listener $(LISTENER)

set-listener-async: build
	$(ASYNC)     set-listener --controller $(CONTROLLER)
	$(ASYNC_TCP) set-listener --controller $(CONTROLLER)

get-door-control: build
	$(CMD) get-door-control --controller $(CONTROLLER)
	$(TCP) get-door-control --controller $(CONTROLLER)

get-door-control-async: build
	$(ASYNC)     get-door-control --controller $(CONTROLLER)
	$(ASYNC_TCP) get-door-control --controller $(CONTROLLER)

set-door-control: build
	$(CMD) set-door-control --controller $(CONTROLLER)
	$(TCP) set-door-control --controller $(CONTROLLER)

set-door-control-async: build
	$(ASYNC)     set-door-control --controller $(CONTROLLER)
	$(ASYNC_TCP) set-door-control --controller $(CONTROLLER)

open-door: build
	$(CMD) open-door --controller $(CONTROLLER)
	$(TCP) open-door --controller $(CONTROLLER)

open-door-async: build
	$(ASYNC)     open-door --controller $(CONTROLLER)
	$(ASYNC_TCP) open-door --controller $(CONTROLLER)

get-cards: build
	$(CMD) get-cards --controller $(CONTROLLER)
	$(TCP) get-cards --controller $(CONTROLLER)

get-cards-async: build
	$(ASYNC)     get-cards --controller $(CONTROLLER)
	$(ASYNC_TCP) get-cards --controller $(CONTROLLER)

get-card: build
	$(CMD) get-card --controller $(CONTROLLER) --card $(CARD)
	$(TCP) get-card --controller $(CONTROLLER) --card $(CARD)

get-card-record: build
	$(CMD) get-card-record --controller $(CONTROLLER) --card $(CARD)
	$(TCP) get-card-record --controller $(CONTROLLER) --card $(CARD)

get-card-async: build
	$(ASYNC)     get-card --controller $(CONTROLLER) --card $(CARD)
	$(ASYNC_TCP) get-card --controller $(CONTROLLER) --card $(CARD)

get-card-record-async: build
	$(ASYNC)     get-card-record --controller $(CONTROLLER) --card $(CARD)
	$(ASYNC_TCP) get-card-record --controller $(CONTROLLER) --card $(CARD)

get-card-by-index: build
	$(CMD) get-card-by-index --controller $(CONTROLLER) --index 3
	$(TCP) get-card-by-index --controller $(CONTROLLER) --index 3

get-card-record-by-index: build
	$(CMD) get-card-record-by-index --controller $(CONTROLLER) --index 3
	$(TCP) get-card-record-by-index --controller $(CONTROLLER) --index 3

get-card-by-index-async: build
	$(ASYNC)     get-card-by-index --controller $(CONTROLLER) --index 3
	$(ASYNC_TCP) get-card-by-index --controller $(CONTROLLER) --index 3

get-card-record-by-index-async: build
	$(ASYNC)     get-card-record-by-index --controller $(CONTROLLER) --index 3
	$(ASYNC_TCP) get-card-record-by-index --controller $(CONTROLLER) --index 3

put-card: build
	$(CMD) put-card --controller $(CONTROLLER) --card $(CARD)
	$(TCP) put-card --controller $(CONTROLLER) --card $(CARD)

put-card-record: build
	$(CMD) put-card-record --controller $(CONTROLLER) --card $(CARD)

put-card-async: build
	$(ASYNC)     put-card --controller $(CONTROLLER) --card $(CARD)
	$(ASYNC_TCP) put-card --controller $(CONTROLLER) --card $(CARD)

put-card-record-async: build
	$(ASYNC) put-card-record --controller $(CONTROLLER) --card $(CARD)

delete-card: build
	$(CMD) delete-card --controller $(CONTROLLER) --card $(CARD)
	$(TCP) delete-card --controller $(CONTROLLER) --card $(CARD)

delete-card-async: build
	$(ASYNC)     delete-card --controller $(CONTROLLER) --card $(CARD)
	$(ASYNC_TCP) delete-card --controller $(CONTROLLER) --card $(CARD)

delete-all-cards: build
	$(CMD) delete-all-cards --controller $(CONTROLLER)
	$(TCP) delete-all-cards --controller $(CONTROLLER)

delete-all-cards-async: build
	$(ASYNC)     delete-all-cards --controller $(CONTROLLER)
	$(ASYNC_TCP) delete-all-cards --controller $(CONTROLLER)

get-event: build
	$(CMD) get-event --controller $(CONTROLLER) --index $(EVENT)
	$(TCP) get-event --controller $(CONTROLLER) --index $(EVENT)

get-event-record: build
	$(CMD) get-event-record --controller $(CONTROLLER) --index $(EVENT)

get-event-async: build
	$(ASYNC)     get-event --controller $(CONTROLLER) --index $(EVENT)
	$(ASYNC_TCP) get-event --controller $(CONTROLLER) --index $(EVENT)

get-event-record-async: build
	$(ASYNC) get-event-record --controller $(CONTROLLER) --index $(EVENT)

get-event-index: build
	$(CMD) get-event-index --controller $(CONTROLLER)
	$(TCP) get-event-index --controller $(CONTROLLER)

get-event-index-async: build
	$(ASYNC)     get-event-index --controller $(CONTROLLER)
	$(ASYNC_TCP) get-event-index --controller $(CONTROLLER)

set-event-index: build
	$(CMD) set-event-index --controller $(CONTROLLER)
	$(TCP) set-event-index --controller $(CONTROLLER)

set-event-index-async: build
	$(ASYNC)     set-event-index --controller $(CONTROLLER)
	$(ASYNC_TCP) set-event-index --controller $(CONTROLLER)

record-special-events: build
	$(CMD) record-special-events --controller $(CONTROLLER)
	$(TCP) record-special-events --controller $(CONTROLLER)

record-special-events-async: build
	$(ASYNC)     record-special-events --controller $(CONTROLLER)
	$(ASYNC_TCP) record-special-events --controller $(CONTROLLER)

get-time-profile: build
	$(CMD) get-time-profile --controller $(CONTROLLER) --profile $(PROFILE)
	$(TCP) get-time-profile --controller $(CONTROLLER) --profile $(PROFILE)

get-time-profile-record: build
	$(CMD) get-time-profile-record --controller $(CONTROLLER) --profile $(PROFILE)

get-time-profile-async: build
	$(ASYNC)     get-time-profile --controller $(CONTROLLER) --profile $(PROFILE)
	$(ASYNC_TCP) get-time-profile --controller $(CONTROLLER) --profile $(PROFILE)

get-time-profile-record-async: build
	$(ASYNC) get-time-profile-record --controller $(CONTROLLER) --profile $(PROFILE)

set-time-profile: build
	$(CMD) set-time-profile --controller $(CONTROLLER) --profile $(PROFILE)
	$(TCP) set-time-profile --controller $(CONTROLLER) --profile $(PROFILE)

set-time-profile-record: build
	$(CMD) set-time-profile-record --controller $(CONTROLLER) --profile $(PROFILE)

set-time-profile-async: build
	$(ASYNC)     set-time-profile --controller $(CONTROLLER) --profile $(PROFILE)
	$(ASYNC_TCP) set-time-profile --controller $(CONTROLLER) --profile $(PROFILE)

set-time-profile-record-async: build
	$(ASYNC) set-time-profile-record --controller $(CONTROLLER) --profile $(PROFILE)

clear-time-profiles: build
	$(CMD) clear-time-profiles --controller $(CONTROLLER)
	$(TCP) clear-time-profiles --controller $(CONTROLLER)

clear-time-profiles-async: build
	$(ASYNC)     clear-time-profiles --controller $(CONTROLLER)
	$(ASYNC_TCP) clear-time-profiles --controller $(CONTROLLER)

add-task: build
	$(CMD) add-task --controller $(CONTROLLER)
	$(TCP) add-task --controller $(CONTROLLER)

add-task-record: build
	$(CMD) add-task-record --controller $(CONTROLLER)

add-task-async: build
	$(ASYNC)     add-task --controller $(CONTROLLER)
	$(ASYNC_TCP) add-task --controller $(CONTROLLER)

add-task-record-async: build
	$(ASYNC) add-task-record --controller $(CONTROLLER)

refresh-tasklist: build
	$(CMD) refresh-tasklist --controller $(CONTROLLER)
	$(TCP) refresh-tasklist --controller $(CONTROLLER)

refresh-tasklist-async: build
	$(ASYNC)     refresh-tasklist --controller $(CONTROLLER)
	$(ASYNC_TCP) refresh-tasklist --controller $(CONTROLLER)

clear-tasklist: build
	$(CMD) clear-tasklist --controller $(CONTROLLER)
	$(TCP) clear-tasklist --controller $(CONTROLLER)

clear-tasklist-async: build
	$(ASYNC)     clear-tasklist --controller $(CONTROLLER)
	$(ASYNC_TCP) clear-tasklist --controller $(CONTROLLER)

set-pc-control: build
	$(CMD) set-pc-control --controller $(CONTROLLER)
	$(TCP) set-pc-control --controller $(CONTROLLER)

set-pc-control-async: build
	$(ASYNC)     set-pc-control --controller $(CONTROLLER)
	$(ASYNC_TCP) set-pc-control --controller $(CONTROLLER)

set-interlock: build
	$(CMD) set-interlock --controller $(CONTROLLER)
	$(TCP) set-interlock --controller $(CONTROLLER)

set-interlock-async: build
	$(ASYNC)     set-interlock --controller $(CONTROLLER)
	$(ASYNC_TCP) set-interlock --controller $(CONTROLLER)

activate-keypads: build
	$(CMD) activate-keypads --controller $(CONTROLLER)
	$(TCP) activate-keypads --controller $(CONTROLLER)

activate-keypads-async: build
	$(ASYNC)     activate-keypads --controller $(CONTROLLER)
	$(ASYNC_TCP) activate-keypads --controller $(CONTROLLER)

set-door-passcodes: build
	$(CMD) set-door-passcodes --controller $(CONTROLLER) --door 2 --passcodes 7531,54321,999999
	$(TCP) set-door-passcodes --controller $(CONTROLLER) --door 2 --passcodes 7531,54321,999999

set-door-passcodes-record: build
	$(CMD) set-door-passcodes-record --controller $(CONTROLLER) --door 2 --passcodes 7531,54321,999999

set-door-passcodes-async: build
	$(ASYNC)     set-door-passcodes --controller $(CONTROLLER) --door 2 --passcodes 7531,54321,999999
	$(ASYNC_TCP) set-door-passcodes --controller $(CONTROLLER) --door 2 --passcodes 7531,54321,999999

set-door-passcodes-record-async: build
	$(ASYNC) set-door-passcodes-record --controller $(CONTROLLER) --door 2 --passcodes 7531,54321,999999

get-antipassback: build
	$(CMD) get-antipassback --controller $(CONTROLLER)
	$(TCP) get-antipassback --controller $(CONTROLLER)

get-antipassback-async: build
	$(ASYNC)     get-antipassback --controller $(CONTROLLER)
	$(ASYNC_TCP) get-antipassback --controller $(CONTROLLER)

set-antipassback: build
	$(CMD) set-antipassback --controller $(CONTROLLER) --antipassback "$(ANTIPASSBACK)"
	$(TCP) set-antipassback --controller $(CONTROLLER) --antipassback "$(ANTIPASSBACK)"

set-antipassback-async: build
	$(ASYNC)     set-antipassback --controller $(CONTROLLER) --antipassback "$(ANTIPASSBACK)"
	$(ASYNC_TCP) set-antipassback --controller $(CONTROLLER) --antipassback "$(ANTIPASSBACK)"

set-firstcard: build
	$(CMD) set-firstcard --controller $(CONTROLLER) --door $(DOOR) --firstcard "$(FIRSTCARD)"
	$(TCP) set-firstcard --controller $(CONTROLLER) --door $(DOOR) --firstcard "$(FIRSTCARD)"

set-firstcard-async: build
	$(ASYNC)     set-firstcard --controller $(CONTROLLER) --door $(DOOR) --firstcard "$(FIRSTCARD)"
	$(ASYNC_TCP) set-firstcard --controller $(CONTROLLER) --door $(DOOR) --firstcard "$(FIRSTCARD)"

restore-default-parameters: build
	$(CMD) restore-default-parameters --controller $(CONTROLLER)
	$(TCP) restore-default-parameters --controller $(CONTROLLER)

restore-default-parameters-async: build
	$(ASYNC)     restore-default-parameters --controller $(CONTROLLER)
	$(ASYNC_TCP) restore-default-parameters --controller $(CONTROLLER)

listen: build
	$(CMD) listen

listen-async: build
	$(ASYNC) listen

all: build
	$(CMD) get-all-controllers
	$(CMD) get-controller             --controller $(CONTROLLER)
	$(CMD) set-ip                     --controller $(CONTROLLER)
	$(CMD) get-status                 --controller $(CONTROLLER)
	$(CMD) get-status-record          --controller $(CONTROLLER)
	$(CMD) get-time                   --controller $(CONTROLLER)
	$(CMD) set-time                   --controller $(CONTROLLER)
	$(CMD) get-listener               --controller $(CONTROLLER)
	$(CMD) set-listener               --controller $(CONTROLLER)
	$(CMD) get-door-control           --controller $(CONTROLLER)
	$(CMD) set-door-control           --controller $(CONTROLLER)
	$(CMD) open-door                  --controller $(CONTROLLER)
	$(CMD) get-cards                  --controller $(CONTROLLER)
	$(CMD) put-card                   --controller $(CONTROLLER) --card $(CARD)
	$(CMD) put-card-record            --controller $(CONTROLLER) --card $(CARD)
	$(CMD) get-card                   --controller $(CONTROLLER) --card $(CARD)
	$(CMD) get-card-record            --controller $(CONTROLLER) --card $(CARD)
	$(CMD) get-card-by-index          --controller $(CONTROLLER) --index 3
	$(CMD) get-card-record-by-index   --controller $(CONTROLLER) --index 3
	$(CMD) delete-card                --controller $(CONTROLLER) --card $(CARD)
	$(CMD) delete-all-cards           --controller $(CONTROLLER)
	$(CMD) get-event                  --controller $(CONTROLLER) --index $(EVENT)
	$(CMD) get-event-record           --controller $(CONTROLLER) --index $(EVENT)
	$(CMD) get-event-index            --controller $(CONTROLLER)
	$(CMD) set-event-index            --controller $(CONTROLLER)
	$(CMD) record-special-events      --controller $(CONTROLLER)
	$(CMD) get-time-profile           --controller $(CONTROLLER) --profile $(PROFILE)
	$(CMD) get-time-profile-record    --controller $(CONTROLLER) --profile $(PROFILE)
	$(CMD) set-time-profile           --controller $(CONTROLLER) --profile $(PROFILE)
	$(CMD) set-time-profile-record    --controller $(CONTROLLER) --profile $(PROFILE)
	$(CMD) clear-time-profiles        --controller $(CONTROLLER)
	$(CMD) add-task                   --controller $(CONTROLLER)
	$(CMD) add-task-record            --controller $(CONTROLLER)
	$(CMD) refresh-tasklist           --controller $(CONTROLLER)
	$(CMD) clear-tasklist             --controller $(CONTROLLER)
	$(CMD) set-pc-control             --controller $(CONTROLLER)
	$(CMD) set-interlock              --controller $(CONTROLLER)
	$(CMD) activate-keypads           --controller $(CONTROLLER)
	$(CMD) set-door-passcodes         --controller $(CONTROLLER)
	$(CMD) get-antipassback           --controller $(CONTROLLER)
	$(CMD) set-antipassback           --controller $(CONTROLLER) --antipassback "$(ANTIPASSBACK)"
	$(CMD) set-firstcard              --controller $(CONTROLLER) --door $(DOOR) --firstcard "$(FIRSTCARD)"
	$(CMD) restore-default-parameters --controller $(CONTROLLER)

all-async: build
	$(ASYNC) get-all-controllers
	$(ASYNC) get-controller             --controller $(CONTROLLER)
	$(ASYNC) set-ip                     --controller $(CONTROLLER)
	$(ASYNC) get-status                 --controller $(CONTROLLER)
	$(ASYNC) get-status-record          --controller $(CONTROLLER)
	$(ASYNC) get-time                   --controller $(CONTROLLER)
	$(ASYNC) set-time                   --controller $(CONTROLLER)
	$(ASYNC) get-listener               --controller $(CONTROLLER)
	$(ASYNC) set-listener               --controller $(CONTROLLER)
	$(ASYNC) get-door-control           --controller $(CONTROLLER)
	$(ASYNC) set-door-control           --controller $(CONTROLLER)
	$(ASYNC) open-door                  --controller $(CONTROLLER)
	$(ASYNC) get-cards                  --controller $(CONTROLLER)
	$(ASYNC) put-card-record            --controller $(CONTROLLER) --card $(CARD)
	$(ASYNC) get-card                   --controller $(CONTROLLER) --card $(CARD)
	$(ASYNC) get-card-record            --controller $(CONTROLLER) --card $(CARD)
	$(ASYNC) get-card-by-index          --controller $(CONTROLLER) --index 3
	$(ASYNC) get-card-record-by-index   --controller $(CONTROLLER) --index 3
	$(ASYNC) delete-card                --controller $(CONTROLLER) --card $(CARD)
	$(ASYNC) delete-all-cards           --controller $(CONTROLLER)
	$(ASYNC) get-event                  --controller $(CONTROLLER) --index $(EVENT)
	$(ASYNC) get-event-record           --controller $(CONTROLLER) --index $(EVENT)
	$(ASYNC) get-event-index            --controller $(CONTROLLER)
	$(ASYNC) set-event-index            --controller $(CONTROLLER)
	$(ASYNC) record-special-events      --controller $(CONTROLLER)
	$(ASYNC) get-time-profile           --controller $(CONTROLLER) --profile $(PROFILE)
	$(ASYNC) get-time-profile-record    --controller $(CONTROLLER) --profile $(PROFILE)
	$(ASYNC) set-time-profile           --controller $(CONTROLLER) --profile $(PROFILE)
	$(ASYNC) set-time-profile-record    --controller $(CONTROLLER) --profile $(PROFILE)
	$(ASYNC) clear-time-profiles        --controller $(CONTROLLER)
	$(ASYNC) add-task                   --controller $(CONTROLLER)
	$(ASYNC) add-task-record            --controller $(CONTROLLER)
	$(ASYNC) refresh-tasklist           --controller $(CONTROLLER)
	$(ASYNC) clear-tasklist             --controller $(CONTROLLER)
	$(ASYNC) set-pc-control             --controller $(CONTROLLER)
	$(ASYNC) set-interlock              --controller $(CONTROLLER)
	$(ASYNC) activate-keypads           --controller $(CONTROLLER)
	$(ASYNC) set-door-passcodes         --controller $(CONTROLLER)
	$(ASYNC) get-antipassback           --controller $(CONTROLLER)
	$(ASYNC) set-antipassback           --controller $(CONTROLLER) --antipassback "$(ANTIPASSBACK)"
	$(ASYNC) set-firstcard              --controller $(CONTROLLER) --door $(DOOR) --firstcard "$(FIRSTCARD)"
	$(ASYNC) restore-default-parameters --controller $(CONTROLLER)

event-listener: build
	python3 -m examples.event_listener.main --debug --bind 192.168.1.125 --broadcast 192.168.1.255 --listen 192.168.1.125:60001

event-listener-async: build
	python3 -m examples.async.event_listener.main --debug --bind 192.168.1.125 --broadcast 192.168.1.255 --listen 192.168.1.125:60001 --host 192.168.1.125:60001

	
