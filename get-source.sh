#!/bin/sh
# Make snapshot of depot_tools
# Author: Elan Ruusamäe <glen@pld-linux.org>
set -e

repo_url=https://chromium.googlesource.com/chromium/tools/depot_tools.git
package=depot_tools
specfile=$package.spec

export GIT_DIR=$package.git

if [ ! -d $GIT_DIR ]; then
	install -d $GIT_DIR
	git init --bare
	git remote add origin $repo_url
	git fetch --depth 1 origin refs/heads/master:refs/remotes/origin/master
else
	git fetch origin refs/heads/master:refs/remotes/origin/master
fi

git update-ref HEAD refs/remotes/origin/master

githash=$(git rev-parse --short HEAD)
gitdate=$(git log -1 --date=short --pretty='format:%cd' HEAD | tr -d -)
prefix=$package-$gitdate
archive=$prefix-$githash.tar.xz

if [ -f $archive ]; then
	echo "Tarball $archive already exists at $githash"
	exit 0
fi

git -c tar.tar.xz.command="xz -9c" archive $githash --prefix $prefix/ -o $archive

../dropin $archive
