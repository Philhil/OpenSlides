# Development of OpenSlides 4

## Requirements

You need git, bash, docker, docker-compose, make and go installed.

Go is needed to install https://github.com/FiloSottile/mkcert. The development setup uses HTTPS per default. OpenSlides does not work with HTTP anymore since features are required (like http2) that only works in a secure environment.

## First time checkout

Clone this repository:

    $ git clone git@github.com:OpenSlides/OpenSlides.git
    $ git checkout openslides4-dev

TODO: use `--recurse-submodules`, when master is OS4

After checking out the os4-branch you need to initialize all submodules and install a root-cert:

    $ git submodule update --init
    $ go get https://github.com/FiloSottile/mkcert
    $ sudo mkcert -install

If you get an error, you might need to install `certutil`. For Debian: `sudo apt install libnss3-tools`.

Finally, start the dev server:

    $ make run-dev

## Running tests

To run all tests of all services, execute `run-service-tests`. TODO: Systemtests in this repo.

## Adding a new Service

    $ git submodule add <git@myrepo.git>

Append `branch = master` to the new entry in the `.gitmodules` file. Verify,
that it is there (the folder should have 160000 permissions: Submodule) with the
current commit:

    $ git diff --cached

Then, commit changes and create a pull request.

## Work in submodules

- Create your own fork at github.
- Remove the upstream (main) repo as the origin in the submodule:

    $ cd <submodule>
    $ git remote remove origin

- Add your fork and the main repo as origin and upstream

    $ git remote add origin <your fork>
    $ git remote add upstream <main repo>

## Requirements for services

### Environment variables

These environment variables are available:

- `<SERVICE>_HOST`: The host from a required service
- `<SERVICE>_PORT`: The port from a required service

Required services can be `MESSAGE_BUS`, `DATASTORE_WRITER`, `PERMISSION`, `AUTOUPDATE`,
etc. For private services (e.g. a database dedicated to exactly one service),
use the following syntax: `<SERVICE>_<PRIV_SERVICE>_<ATTRIBUTE>`, e.g. the
Postgresql user for the datastore: `DATASTORE_POSTGRESQL_USER`.

### Makefile

A makefile must be provided at the root-level of the service. The currently
required (phony) targets are:

- `run-tests`: Execute all tests from the submodule
- `build-dev`: Build an image with the tag `openslides-<service>-dev`

### Build arguments in the Dockerfile

These build arguments should be supported by every service:

- `REPOSITORY_URL`: The git-url for the repository to use
- `GIT_CHECKOUT`: A branch/tag/commit to check out during the build

Note that meaningful defaults should be provided in the Dockerfile.

## Developing on a single service

Go to the serivce and create a new branch (from master):

    $ cd my-service
    $ git status  # -> on master?
    $ git checkout -b my-feature

Run OpenSlides in development mode (e.g. in a new terminal):

    $ make run-dev

After making some changes in my-service, create a commit and push to your fork

    $ git add -A
    $ git commit -m "A meaningful commit message here"
    $ git push origin my-feature

As the last step, you can create a PR on Github. After merging, these steps are
required to be executed in the main repo:

    $ cd my-service
    $ git pull upstream master
    $ cd ..
    $ git diff  # -> commit hash changed for my-service

If the update commit should be a PR:

    $ git checkout -b updated-my-service
    $ git commit -am "Updated my-service"
    $ git push origin updated-my-service

Or a direct push on master:

    $ git commit -am "Updated my-service"
    $ git push origin master

## Working with Submodules

After working in many services with different branches, this command checks
out `master` (or the given branch in the .gitmodules) in all submodules and
pulls master from upstream (This requres to have `upstream`set up as a remote
in all submodules):

    $ git submodule foreach -q --recursive 'git checkout $(git config -f $toplevel/.gitmodules submodule.$name.branch || echo master); git pull upstream $(git config -f $toplevel/.gitmodules submodule.$name.branch || echo master)'

When changing the branch in the main repo (this one), the submodules do not
automatically gets changed. THis ocmmand checks out all submodules to the given
commits in the main repo:

    $ git submodule update
