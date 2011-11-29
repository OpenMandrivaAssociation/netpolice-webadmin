%define name netpolice-webadmin
%define version 1.0
%define unmangled_version 1.0
%define release 1

Summary:	Netpolice webadmin
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{unmangled_version}.tar.gz
Source1:	webadmin.conf
Source2:	webadmin-port.conf
Source3:	vhost-webadmin.conf
Source4:	pdns.conf
Source5:	zones.conf
Source6:	export_stat
License:	BSD License
Group:		System/Servers
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:		%{_prefix}
BuildArch:	noarch
Url:		http://www.netpolice.ru/
AutoReq:	0
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	python-django
BuildRequires:	python-suds
BuildRequires:	python-ipaddr
BuildRequires:	PyOFC2
BuildRequires:	python-anyjson
Requires:	pdns
Requires:	c-icap >= 0.1.6
Requires:	apache-base
Requires:	apache-conf
Requires:	apache-mod_wsgi
Requires:	python-memcached
Requires:	python-sqlite2
Requires:	python-django
Requires:	python-suds
Requires:	python-ipaddr
Requires:	PyOFC2
Requires:	python-anyjson

%description
Netpolice webadmin.

%prep
%setup -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
rm -rf %{buildroot}

python setup.py install --root=%{buildroot} --record=INSTALLED_FILES
install -pD -m644 %{SOURCE1} %{buildroot}/etc/netpolice/webadmin.conf
install -pD -m644 %{SOURCE4} %{buildroot}/etc/powerdns/pdns.conf.sample
install -pD -m644 %{SOURCE5} %{buildroot}/etc/powerdns/zones.conf
install -pD -m644 %{SOURCE2} %{buildroot}/etc/httpd/conf/ports-available/webadmin-port.conf
install -pD -m644 %{SOURCE3} %{buildroot}/etc/httpd/conf/sites-available/vhost-webadmin.conf
mkdir -p %{buildroot}/var/lib/netpolice
touch %{buildroot}/var/lib/netpolice/ZONE.root
install -pD -m755 %{SOURCE6} %{buildroot}/var/spool/cron/export_stat
touch %{buildroot}/var/lib/netpolice/stat.db

%post
/usr/sbin/useradd -M -r -d /dev/null -s /dev/null -c "system user for %{name}" -g netpolice netpolice> /dev/null 2>&1 ||:
mkdir -p /etc/httpd/conf/ports-enabled
mkdir -p /etc/httpd/conf/sites-enabled
ln -t /etc/httpd/conf/ports-enabled/ -s /etc/httpd/conf/ports-available/webadmin-port.conf
ln -t /etc/httpd/conf/sites-enabled/ -s /etc/httpd/conf/sites-available/vhost-webadmin.conf
/usr/sbin/usermod -G netpolice apache
sqlite3 -line /var/lib/netpolice/stat.db 'CREATE TABLE statistics (id integer NOT NULL PRIMARY KEY,date datetime NOT NULL,user varchar(255),role varchar(255),client_ip varchar(50),url text NOT NULL,action integer NOT NULL,mod smallint unsigned NOT NULL,categories varchar(255));'> /dev/null 2>&1 ||:
crontab /var/spool/cron/export_stat -u apache

%files
%defattr(-,root,root)
%config(noreplace) /etc/httpd/conf/ports-available/webadmin-port.conf
%config(noreplace) /etc/httpd/conf/sites-available/vhost-webadmin.conf
%config(noreplace) %attr(644,apache,netpolice) /etc/netpolice/webadmin.conf
%config(noreplace) /etc/powerdns/pdns.conf.sample
%config(noreplace) /etc/powerdns/zones.conf
%config(noreplace) %attr(644,apache,netpolice) /var/lib/netpolice/ZONE.root
%config(noreplace) %attr(644,apache,netpolice) /var/lib/netpolice/stat.db
#%attr(644,apache,netpolice) /etc/netpolice/webadmin.conf
#%attr(644,apache,netpolice) /var/lib/netpolice/ZONE.root
#%attr(644,apache,netpolice) /var/lib/netpolice/stat.db
%attr(644,apache,netpolice) /var/spool/cron/export_stat
%{py_sitedir}/webadmin/*.py
%{py_sitedir}/webadmin/utils/*.py
%{py_sitedir}/webadmin/templates/*.html
%{py_sitedir}/webadmin/templates/manual/ru/*.html
%{py_sitedir}/webadmin/static/swf/*.swf
%{py_sitedir}/webadmin/static/js/*.js
%{py_sitedir}/webadmin/static/img/*.jpg
%{py_sitedir}/webadmin/static/img/*.png
%{py_sitedir}/webadmin/static/img/*.ico
%{py_sitedir}/webadmin/static/css/*.css
%{py_sitedir}/webadmin/locale/ru/LC_MESSAGES/*.po
%{py_sitedir}/webadmin/locale/ru/LC_MESSAGES/*.mo
%{py_sitedir}/webadmin/conf/*.sample
%{py_sitedir}/webadmin/apps/users/*.py
%{py_sitedir}/webadmin/apps/users/lib/*.py
%{py_sitedir}/webadmin/apps/users/tests/*.py
%{py_sitedir}/webadmin/apps/users/templates/users/*.html
%{py_sitedir}/webadmin/apps/statistics/*.py
%{py_sitedir}/webadmin/apps/statistics/tests/*.py
%{py_sitedir}/webadmin/apps/statistics/templates/statistics/*.html
%{py_sitedir}/webadmin/apps/statistics/lib/*.py
%{py_sitedir}/webadmin/apps/statistics/management/*.py
%{py_sitedir}/webadmin/apps/statistics/management/commands/*.py
%{py_sitedir}/webadmin/apps/roles/*.py
%{py_sitedir}/webadmin/apps/roles/tests/*.py
%{py_sitedir}/webadmin/apps/roles/templates/roles/*.html
%{py_sitedir}/webadmin/apps/manual_categorization/*.py
%{py_sitedir}/webadmin/apps/manual_categorization/tests/*.py
%{py_sitedir}/webadmin/apps/manual_categorization/templates/manual_categorization/*.html
%{py_sitedir}/webadmin/apps/main/*.py
%{py_sitedir}/webadmin/apps/main/tests/*.py
%{py_sitedir}/webadmin/apps/main/templates/main/*.html
%{py_sitedir}/webadmin/apps/license/*.py
%{py_sitedir}/webadmin/apps/license/tests/*.py
%{py_sitedir}/webadmin/apps/license/lib/*.py
%{py_sitedir}/webadmin/apps/license/templates/license/*.html
%{py_sitedir}/webadmin/apps/categories/*.py
%{py_sitedir}/webadmin/apps/categories/tests/*.py
%{py_sitedir}/webadmin/apps/categories/templates/categories/*.html
%{py_sitedir}/webadmin/apps/core/*.py
%{py_sitedir}/webadmin/apps/core/templatetags/*.py
%{py_sitedir}/webadmin/apps/auth/*.py
%{py_sitedir}/webadmin/apps/auth/tests/*.py
%{py_sitedir}/webadmin/apps/auth/templates/auth/*.html
%{py_sitedir}/webadmin/apps/admins/*.py
%{py_sitedir}/webadmin/apps/admins/tests/*.py
%{py_sitedir}/webadmin/apps/admins/templates/admins/*.html
%{py_sitedir}/webadmin/apps/manual_categorization/lib/*.py
%{py_sitedir}/webadmin/apps/*.py
%{py_sitedir}/*.egg-info
/usr/bin/*.wsgi

%clean
rm -rf %{buildroot}

%changelog
* Fri Sep 02 2011 L.Butorina <l.butorina@cair.ru> 1.0-alt1
- Stat log migrate to sql database

* Fri Jul 29 2011 L.Butorina <l.butorina@cair.ru> 2
- New test version webadmin 0.9.1 for Mandriva.

* Fri Jul 29 2011 L.Butorina <l.butorina@cair.ru> 1
- New test version webadmin 0.9.0 for Mandriva.
