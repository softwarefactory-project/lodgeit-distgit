%global commit  c6c6db6ca06a4edcafa1f425d0d36e16264cfd51

Name:           lodgeit
Version:        0.3
Release:        1%{?dist}
Summary:        LogdeIt, a Pastebin service

License:        BSD
URL:            https://opendev.org/opendev/lodgeit
Source0:        https://opendev.org/opendev/lodgeit/archive/%{commit}.tar.gz
Source1:        setup.py
Source2:        setup.cfg
Source3:        lodgeit.py
Source4:        lodgeit.service
Source5:        lodgeit.conf
Source6:        lodgeit.sysconfig
Source7:        werkzeug-script.py

Patch1:         0001-Add-sub-url-deployment-fixes.patch

BuildArch:      noarch

Requires:       python3-jinja2
Requires:       python3-werkzeug
Requires:       python3-pygments
Requires:       python3-sqlalchemy
Requires:       python3-simplejson
Requires:       python3-babel
Requires:       python3-pillow
Requires:       python3-PyMySQL
Requires:       pytz
Requires:       python3-markupsafe
Requires:       wait4service
Requires:       python3-XStatic-jQuery

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  systemd


%description
Lodgeit is a simple pastebin service.


%prep
%autosetup -n %{name} -p1
rm requirements.txt test-requirements.txt

# Replace bundled libraries
rm lodgeit/static/jquery.js
ln -s /usr/lib/python3.6/site-packages/xstatic/pkg/jquery/data/jquery.min.js lodgeit/static/jquery.js

# Remove unused/not maintained autocomplete plugin
rm lodgeit/static/jquery.autocomplete.js
sed -i 's|^<script.*jquery.autocomplete.js.*$||' lodgeit/views/layout.html
cp %{SOURCE7} lodgeit/script.py


%build
cp %{SOURCE1} %{SOURCE2} .
PBR_VERSION=%{version} %{__python3} setup.py build


%install
PBR_VERSION=%{version} %{__python3} setup.py install --skip-build --root %{buildroot}
# TODO: use setup.cfg data_files
mv lodgeit/{res,static,views} %{buildroot}/%{python3_sitelib}/lodgeit/

install -p -D -m 0755 %{SOURCE3} %{buildroot}/usr/bin/lodgeit
install -p -D -m 0644 %{SOURCE4} %{buildroot}%{_unitdir}/lodgeit.service
install -p -D -m 0640 %{SOURCE5} %{buildroot}%{_sysconfdir}/lodgeit/lodgeit.conf
install -p -D -m 0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/lodgeit
install -p -d -m 0700 %{buildroot}%{_sharedstatedir}/lodgeit


%pre
getent group lodgeit >/dev/null || groupadd -r lodgeit
if ! getent passwd lodgeit >/dev/null; then
  useradd -r -g lodgeit -G lodgeit -d %{_sharedstatedir}/lodgeit -s /sbin/nologin -c "Lodgeit Daemon" lodgeit
fi
exit 0


%post
%systemd_post lodgeit.service


%preun
%systemd_preun lodgeit.service


%postun
%systemd_postun_with_restart lodgeit.service


%files
%{_bindir}/lodgeit
%{_unitdir}/lodgeit.service
%dir %{_sysconfdir}/lodgeit/
%config(noreplace) %attr(0640, root, lodgeit) %{_sysconfdir}/lodgeit/lodgeit.conf
%dir %attr(0700, lodgeit, lodgeit) %{_sharedstatedir}/lodgeit
%{_sysconfdir}/sysconfig/lodgeit
%{python3_sitelib}/lodgeit
%{python3_sitelib}/lodgeit-*.egg-info


%changelog
* Mon Nov  4 2019 Tristan Cacqueray <tdecacqu@redhat.com> - 0.2-2
- Add werkzeug.script module

* Thu May 31 2018 Tristan Cacqueray <tdecacqu@redhat.com> - 0.2-1
- Bump version and include sub-url patch


* Wed Apr 19 2017 Tristan Cacqueray <tdecacqu@redhat.com> - 0.1-3
- use python-XStatic-jQuery instead of js-jquery1

* Mon Feb 20 2017 Tristan Cacqueray - 0.1-2
- Fix typo

* Thu Feb 16 2017 Tristan Cacqueray - 0.1-1
- Initial packaging
