%define nethgui_commit c97b82c1d2ea81ba49548517bbb82b62fb13f7d7
%define uideps_commit 4c6534c9089197bfadeba0cc4569a20b994a4b31
%define pimple_commit 2.1.0
%define fontawesome_commit 4.1.0
%define mustachejs_commit 0.8.2
%define mustachephp_commit 2.6.1
%define symfonyprocess_commit 2.5.2
%define extradocs root%{_docdir}/%{name}-%{version}

Summary: apache/mod_php stack for nethserver-manager
Name: nethserver-httpd-admin
Version: 1.2.3
Release: 100%{?dist}
License: GPL
Source0: %{name}-%{version}.tar.gz
Source1: https://github.com/nethesis/nethserver-nethgui/archive/%{nethgui_commit}/nethserver-nethgui-%{nethgui_commit}.tar.gz
Source2: https://github.com/fabpot/Pimple/archive/v%{pimple_commit}/Pimple-%{pimple_commit}.tar.gz
Source3: https://github.com/nethesis/ui-deps-bundle/archive/%{uideps_commit}/ui-deps-bundle-%{uideps_commit}.tar.gz
Source4: https://github.com/FortAwesome/Font-Awesome/archive/v%{fontawesome_commit}/Font-Awesome-%{fontawesome_commit}.tar.gz
Source5: https://github.com/bobthecow/mustache.php/archive/v%{mustachephp_commit}/mustache.php-%{mustachephp_commit}.tar.gz
Source6: https://github.com/janl/mustache.js/archive/%{mustachejs_commit}/mustache.js-%{mustachejs_commit}.tar.gz
Source7: https://github.com/symfony/Process/archive/v%{symfonyprocess_commit}/Process-%{symfonyprocess_commit}.tar.gz

URL: %{url_prefix}/%{name} 

BuildRequires: nethserver-devtools > 1.0.1, git
BuildArch: noarch

Requires: httpd, php, mod_ssl, sudo
Obsoletes: nethserver-nethgui
Requires: nethserver-php
Requires: nethserver-base
Requires: upstart
Requires: perl(IO::Multiplex), perl(Net::Server::Multiplex)

AutoReq: no

%description 
Runs an Apache instance on port 980 with SSL that serves
the nethserver-manager web application

%prep
%setup    
%setup -D -T -b 1
%setup -D -T -b 2
%setup -D -T -b 3
%setup -D -T -b 4
%setup -D -T -b 5
%setup -D -T -b 6
%setup -D -T -b 7

# Nethgui:
# cd $RPM_BUILD_DIR/nethserver-nethgui-%{nethgui_commit}
# %patch0 -p1

%build
perl createlinks

mkdir -p root/usr/share/nethesis/nethserver-manager
cp -av $RPM_BUILD_DIR/ui-deps-bundle-%{uideps_commit}/{css,js} root/usr/share/nethesis/nethserver-manager/
cp -av $RPM_BUILD_DIR/nethserver-nethgui-%{nethgui_commit}/Nethgui    root/usr/share/nethesis/Nethgui
cp -av $RPM_BUILD_DIR/Pimple-%{pimple_commit}/src/Pimple              root/usr/share/nethesis/Pimple
cp -av $RPM_BUILD_DIR/Font-Awesome-%{fontawesome_commit}/{css,fonts}  root/usr/share/nethesis/nethserver-manager/
cp -av $RPM_BUILD_DIR/mustache.js-%{mustachejs_commit}/mustache.js     root/usr/share/nethesis/nethserver-manager/js
cp -av $RPM_BUILD_DIR/mustache.php-%{mustachephp_commit}/src/Mustache  root/usr/share/nethesis/Mustache
pushd $RPM_BUILD_DIR/Process-%{symfonyprocess_commit}; find . -name '*.php' | cpio -dump $RPM_BUILD_DIR/%{name}-%{version}/root/usr/share/nethesis/Symfony/Component/Process; popd

# Copy documentation and licenses from components:
mkdir -p %{extradocs}/Pimple-%{pimple_commit}
cp -av $RPM_BUILD_DIR/Pimple-%{pimple_commit}/{CHANGELOG,LICENSE,README.rst} %{extradocs}/Pimple-%{pimple_commit}/

mkdir -p %{extradocs}/Font-Awesome-%{fontawesome_commit}
cp -av $RPM_BUILD_DIR/Font-Awesome-%{fontawesome_commit}/README.md %{extradocs}/Font-Awesome-%{fontawesome_commit}/

mkdir -p %{extradocs}/nethserver-nethgui-%{nethgui_commit}
cp -av $RPM_BUILD_DIR/nethserver-nethgui-%{nethgui_commit}/{COPYING,Documentation/} %{extradocs}/nethserver-nethgui-%{nethgui_commit}/

mkdir -p %{extradocs}/mustache.js-%{mustachejs_commit}
cp -av $RPM_BUILD_DIR/mustache.js-%{mustachejs_commit}/{CHANGES,LICENSE,README.md}  %{extradocs}/mustache.js-%{mustachejs_commit}

mkdir -p %{extradocs}/mustache.php-%{mustachephp_commit}
cp -av $RPM_BUILD_DIR/mustache.php-%{mustachephp_commit}/{CONTRIBUTING.md,LICENSE,README.md}  %{extradocs}/mustache.php-%{mustachephp_commit}

mkdir -p %{extradocs}/Symfony-Process-%{symfonyprocess_commit}
cp -av $RPM_BUILD_DIR/Process-%{symfonyprocess_commit}/{LICENSE,README.md}  %{extradocs}/Symfony-Process-%{symfonyprocess_commit}

# Copy package documentation
mkdir -p %{extradocs}
cp COPYING %{extradocs}/

%install
(cd root ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-%{release}-filelist
%{genfilelist} $RPM_BUILD_ROOT \
    --dir /var/cache/nethserver-httpd-admin 'attr(0750,srvmgr,srvmgr)' \
    --dir /var/log/httpd-admin 'attr(0700,root,root)' \
    > %{name}-%{version}-%{release}-filelist

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)

%pre
# ensure srvmgr user exists:
if ! id srvmgr >/dev/null 2>&1 ; then
   useradd -r -U -G adm srvmgr
fi
/sbin/stop httpd-admin >/dev/null 2>&1 || : 

%post
/sbin/start httpd-admin >/dev/null 2>&1 || : 

%changelog
* Thu Apr 17 2014 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.3-1.ns6
- Fix visualization problems with accented letters - Bug #2701

* Mon Mar 24 2014 Davide Principi <davide.principi@nethesis.it> - 1.2.2-1.ns6
- YUM categories in PackageManager - Feature #2694 [NethServer]

* Wed Feb 26 2014 Davide Principi <davide.principi@nethesis.it> - 1.2.1-1.ns6
- Revamp web UI style - Enhancement #2656 [NethServer]
- Emphasized visual style for mandatory text input fields - Feature #1753 [NethServer]

* Wed Feb 05 2014 Davide Principi <davide.principi@nethesis.it> - 1.2.0-1.ns6
- No feedback from Shutdown UI module - Bug #2629 [NethServer]
- RST format for help files - Enhancement #2627 [NethServer]
- Move httpd-admin web server logs - Feature #2551 [NethServer]
- Default remote access from public networks - Enhancement #2548 [NethServer]
- Restore httpd-admin symlink - Enhancement #2536 [NethServer]
- Move admin user in LDAP DB - Feature #2492 [NethServer]
- Give wings to server-manager - Enhancement #2460 [NethServer]

* Thu Oct 17 2013 Davide Principi <davide.principi@nethesis.it> - 1.0.6-1.ns6
- Add language code to URLs - Enhancement #2113 [Nethgui]

* Wed Aug 28 2013 Davide Principi <davide.principi@nethesis.it> - 1.0.5-1.ns6
- Import nethserver-manager code from nethserver-base - Enhancement #2110 [NethServer]
- RemoteAccess/HttpdAdmin UI module does not expand httpd-admin configuration - Bug #2094 [NethServer]
- Single and double quotes characters escaped - Bug #2068 [NethServer]

* Tue May  7 2013 Davide Principi <davide.principi@nethesis.it> - 1.0.4-1.ns6
- db defaults: added access prop with public default
- httpd/vhost-default template: use Redirect directive, in place of RewriteRule #1838 

* Tue Apr 30 2013 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.3-1.ns6
- Rebuild for automatic package handling. #1870
- Redirect /server-manager to port 980 #1838
- Web UI: show local networks as read-only elements #1021

* Tue Mar 19 2013 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.2-1.ns6
- Add migration code
- Use default SSL configuration

* Thu Jan 31 2013 Davide Principi <davide.principi@nethesis.it> - 1.0.1-1.ns6
- Implemented nethserver-base certificate management
