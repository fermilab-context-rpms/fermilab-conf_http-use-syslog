Name:		fermilab-conf_http-use-syslog
Version:	2.0
Release:	1%{?dist}

Group:		Fermilab
License:	MIT
URL:		https://github.com/fermilab-context-rpms/fermilab-conf_http-use-syslog

Source0:	30-apache-httpd-stdout-log.conf
Source1:	30-nginx-stdout-log.conf

BuildArch:	noarch
Requires:	systemd
Requires:	fermilab-conf_system-logger

Requires:	(%{name}-apache-httpd == %{version}-%{release} if httpd)
Requires:	(%{name}-nginx == %{version}-%{release} if nginx)

%description
This meta-package will pull in config files to send webserver logs to STDOUT.
It is expected that journald will forward these to syslog.

%package apache-httpd
Summary:	Send apache-httpd access logs to stdout
Requires:	systemd
Requires:	httpd >= 2.4.17

# this is the old name, keep until EL11?
Obsoletes:	fermilab-conf_apache-use-syslog

%description apache-httpd
Drop in a GlobalLog for apache-httpd to use stdout.

%package nginx
Summary:	Send apache-httpd access logs to stdout
Requires:	systemd
Requires:	nginx >= 1.12

%description nginx
Drop in an access_log for nginx to use stdout.

%prep

%build

%install
%{__install} -D %{SOURCE0} %{buildroot}%{_sysconfdir}/httpd/conf.d/
%{__install} -D %{SOURCE1} %{buildroot}%{_sysconfdir}/nginx/conf.d/

%post apache-httpd
systemctl condrestart httpd.service

%post nginx
systemctl condrestart nginx.service

%files
%defattr(0644,root,root,0755)

%files apache-httpd
%defattr(0644,root,root,0755)
%{_sysconfdir}/httpd/conf.d/*

%files
%defattr(0644,root,root,0755)
%{_sysconfdir}/nginx/conf.d/*

%changelog
* Wed Sep 18 2024 Pat Riehecky <riehecky@fnal.gov> 2.0
- Update to use new name format
- Convert apache-httpd to use GlobalLog
- Add nginx config

* Thu Feb 25 2016 Pat Riehecky <riehecky@fnal.gov> 1.1-3.1
- Check to make sure the services are enabled before restarting them

* Wed Nov 11 2015 Pat Riehecky <riehecky@fnal.gov> 1.1-3
- Should just trigger on httpd, not require it

* Wed Nov 11 2015 Kevin M. Hill <kevinh@fnal.gov> 1.1-2
- switch back to using Augeas, just in case.

* Tue Nov 10 2015 Kevin M. Hill <kevinh@fnal.gov> 1.1-1
- Initial SL7 version.

* Wed Jan 30 2013 Pat Riehecky <riehecky@fnal.gov> 1.0-1
- Initial build
