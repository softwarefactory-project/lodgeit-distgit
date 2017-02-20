%global commit  62f95b0b1b2f1e50cb8422b3dd7bd2365b3453cf

Name:           lodgeit
Version:        0.1
Release:        2%{?dist}
Summary:        LogdeIt, a Pastebin service

License:        BSD
URL:            https://github.com/openstack-infra/lodgeit
Source0:        https://github.com/openstack-infra/lodgeit/archive/%{commit}.tar.gz
Source1:        setup.py
Source2:        setup.cfg
Source3:        lodgeit.py
Source4:        lodgeit.service
Source5:        lodgeit.conf
Source6:        lodgeit.sysconfig

BuildArch:      noarch

Requires:       python-jinja2
Requires:       python-werkzeug
Requires:       python-pygments
Requires:       python-sqlalchemy
Requires:       python-simplejson
Requires:       python-babel
Requires:       python-pillow
Requires:       pytz
Requires:       python-markupsafe
Requires:       wait4service
Requires:       js-jquery1

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  systemd


%description
Lodgeit is a simple pastebin service.


%prep
%autosetup -n %{name}-%{commit}
rm requirements.txt test-requirements.txt

# Replace bundled libraries
rm lodgeit/static/jquery.js
ln -s /usr/share/web-assets/jquery/1/jquery.min.js lodgeit/static/jquery.js

# Remove unused/not maintained autocomplete plugin
rm lodgeit/statis/jquery.autocomplete.js
sed -i 's|^<script.*jquery.autocomplete.js.*$||' lodgeit/views/layout.html


%build
cp %{SOURCE1} %{SOURCE2} .
PBR_VERSION=%{version} %{__python2} setup.py build


%install
PBR_VERSION=%{version} %{__python2} setup.py install --skip-build --root %{buildroot}
# TODO: use setup.cfg data_files
mv lodgeit/{res,static,views} %{buildroot}/%{python2_sitelib}/lodgeit/

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
%{python2_sitelib}/lodgeit
%{python2_sitelib}/lodgeit-*.egg-info


%changelog
* Mon Feb 20 2017 Tristan Cacqueray - 0.1-2
- Fix typo

* Thu Feb 16 2017 Tristan Cacqueray - 0.1-1
- Initial packaging
