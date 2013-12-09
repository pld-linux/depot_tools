%define		snap	20130619
%define		rel		0.3
Summary:	A package of scripts called used to manage checkouts and code reviews
Name:		depot_tools
Version:	0.1
Release:	0.%{snap}.%{rel}
License:	BSD
Group:		Development/Tools
Source0:	https://src.chromium.org/svn/trunk/tools/depot_tools.zip?/%{name}-svn%{snap}.zip
# Source0-md5:	6cf6483d6da8d15848cbaa8857aae3ae
URL:		http://dev.chromium.org/developers/how-tos/depottools
BuildRequires:	unzip
Requires:	python
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
%setup -qc
mv depot_tools/* .
rm -r depot_tools

# python 2.4 components
rm -r third_party/pymox
rm cpplint.py

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a . $RPM_BUILD_ROOT%{_datadir}/%{name}
install -d $RPM_BUILD_ROOT%{_bindir}
cat > $RPM_BUILD_ROOT%{_bindir}/gclient <<'EOF'
#!/bin/sh
%{_datadir}/%{name}/gclient "$@"
EOF
chmod +x $RPM_BUILD_ROOT%{_bindir}/gclient

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README README.gclient
%attr(755,root,root) %{_bindir}/gclient
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
