%define		subver	20131210
%define		rel		0.12
Summary:	A package of scripts called used to manage checkouts and code reviews
Name:		depot_tools
Version:	0.1
Release:	0.%{subver}.%{rel}
License:	BSD
Group:		Development/Tools
Source0:	%{name}-%{subver}-aeab41a.tar.xz
# Source0-md5:	5dd469c8ec03d03d48b7db886475bbfa
Patch0:		adjust-path.patch
URL:		http://dev.chromium.org/developers/how-tos/depottools
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	python
Obsoletes:	gclient
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Chromium uses a package of scripts, the depot_tools, to manage
interaction with the Chromium source code repository and the Chromium
development process. It contains the following utilities:

- gclient: Meta-checkout tool managing both subversion and git
  checkouts. It is similar to repo tool except that it works on Linux,
  OS X, and Windows and supports both svn and git. On the other hand,
  gclient doesn't integrate any code review functionality.
- gcl: Rietveld code review tool for subversion. The gcl tool runs
  presubmit scripts.
- git-cl: Rietveld code review tool for git. The git-cl tool runs
  presubmit scripts.
- hammer: (Obsolete) Wrapper script for building Chromium with the
  SCons software construction tool.
- drover: Quickly revert svn commits.
- cpplint.py: Checks for C++ style compliance.
- presubmit_support.py: Runs PRESUBMIT.py presubmit checks.
- repo: The repo tool.
- trychange.py: Try server tool. It is wrapped by gcl try and git-try.
- git-try: Try change tool for git users
- wtf: Displays the active git branches in a chromium os checkout.
- weekly: Displays the log of checkins for a particular developer
  since a particular date for git checkouts.
- git-gs: Wrapper for git grep with relevant source types.
- zsh-goodies: Completion for zsh users.

%prep
%setup -qn %{name}-%{subver}
%patch -P0 -p1

cat > py-wrap.sh <<'EOF'
#!/bin/sh
exec %{__python} -B %{_datadir}/%{name}/$(basename "$0").py "$@"
EOF
chmod +x *.sh
ln -s git_cl.py git-cl.py

# python 2.4 components
rm -r third_party/pymox

# screw binaries and shipped dependencies and things useless to this platform
rm ninja*
find -type f '(' -name '*.exe' -o -name '*.bat' ')' | xargs rm -v
rm create-ntfs-junction.c

# tests
rm -r testing_support
rm -r tests

# other irrelevant junk
rm -r bootstrap
rm .gitignore
rm OWNERS WATCHLISTS

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_bindir}}
cp -a . $RPM_BUILD_ROOT%{_datadir}/%{name}
# already in %doc
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/{LICENSE,README*}

for a in gclient gcl git-cl fetch; do
	ln -s %{_datadir}/%{name}/py-wrap.sh $RPM_BUILD_ROOT%{_bindir}/$a
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README README.gclient
%attr(755,root,root) %{_bindir}/gcl
%attr(755,root,root) %{_bindir}/gclient
%attr(755,root,root) %{_bindir}/git-cl
%attr(755,root,root) %{_bindir}/fetch
%dir %{_datadir}/%{name}
%attr(755,root,root) %{_datadir}/%{name}/apply_issue
%attr(755,root,root) %{_datadir}/%{name}/cbuildbot
%attr(755,root,root) %{_datadir}/%{name}/chrome_set_ver
%attr(755,root,root) %{_datadir}/%{name}/codereview.settings
%attr(755,root,root) %{_datadir}/%{name}/create-chromium-git-src
%attr(755,root,root) %{_datadir}/%{name}/cros
%attr(755,root,root) %{_datadir}/%{name}/cros_sdk
%attr(755,root,root) %{_datadir}/%{name}/crup-runner.sh
%attr(755,root,root) %{_datadir}/%{name}/download_from_google_storage
%attr(755,root,root) %{_datadir}/%{name}/drover
%attr(755,root,root) %{_datadir}/%{name}/fetch
%attr(755,root,root) %{_datadir}/%{name}/gcl
%attr(755,root,root) %{_datadir}/%{name}/gclient
%attr(755,root,root) %{_datadir}/%{name}/git-cl
%attr(755,root,root) %{_datadir}/%{name}/git-cl-upload-hook
%attr(755,root,root) %{_datadir}/%{name}/git-crsync
%attr(755,root,root) %{_datadir}/%{name}/git-crup
%attr(755,root,root) %{_datadir}/%{name}/git-gs
%attr(755,root,root) %{_datadir}/%{name}/git-lkgr
%attr(755,root,root) %{_datadir}/%{name}/git-number
%attr(755,root,root) %{_datadir}/%{name}/git-runhooks
%attr(755,root,root) %{_datadir}/%{name}/git-try
%attr(755,root,root) %{_datadir}/%{name}/gn
%attr(755,root,root) %{_datadir}/%{name}/hammer
%attr(755,root,root) %{_datadir}/%{name}/py-wrap.sh
%attr(755,root,root) %{_datadir}/%{name}/pylint
%attr(755,root,root) %{_datadir}/%{name}/pylintrc
%attr(755,root,root) %{_datadir}/%{name}/repo
%attr(755,root,root) %{_datadir}/%{name}/update_depot_tools
%attr(755,root,root) %{_datadir}/%{name}/weekly
%attr(755,root,root) %{_datadir}/%{name}/wtf

%{_datadir}/%{name}/*.py
%{_datadir}/%{name}/profile.xml
%{_datadir}/%{name}/git-templates/
%{_datadir}/%{name}/git_utils/
%{_datadir}/%{name}/recipes/
%{_datadir}/%{name}/support/
%{_datadir}/%{name}/third_party/
%{_datadir}/%{name}/zsh-goodies/
