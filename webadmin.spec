%define name webadmin
%define version 1.0
%define unmangled_version 1.0
%define release alt1

Summary:	Netpolice webadmin.
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
Group:		Development/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:		%{_prefix}
BuildArch:	noarch
Vendor:		MegaVersiya, LTD <netpolice@support.cair.ru>
Url:		http://www.netpolice.ru/
AutoReq:	0
BuildPreReq:	python-devel
BuildPreReq:	python-setuptools
BuildPreReq:	Django
BuildPreReq:	suds
BuildPreReq:	ipaddr
BuildPreReq:	PyOFC2
BuildPreReq:	anyjson
Requires:	pdns
Requires:	c-icap >= 0.1.6
Requires:	apache-base
Requires:	apache-conf
Requires:	apache-mod_wsgi
Requires:	python-memcached
Requires:	python-sqlite2
Requires:	Django
Requires:	suds
Requires:	ipaddr
Requires:	PyOFC2
Requires:	anyjson

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
/usr/lib/python2.6/site-packages/webadmin/*.py
/usr/lib/python2.6/site-packages/webadmin/utils/*.py
/usr/lib/python2.6/site-packages/webadmin/templates/*.html
/usr/lib/python2.6/site-packages/webadmin/templates/manual/ru/*.html
/usr/lib/python2.6/site-packages/webadmin/static/swf/*.swf
/usr/lib/python2.6/site-packages/webadmin/static/js/*.js
/usr/lib/python2.6/site-packages/webadmin/static/img/*.jpg
/usr/lib/python2.6/site-packages/webadmin/static/img/*.png
/usr/lib/python2.6/site-packages/webadmin/static/img/*.ico
/usr/lib/python2.6/site-packages/webadmin/static/css/*.css
/usr/lib/python2.6/site-packages/webadmin/locale/ru/LC_MESSAGES/*.po
/usr/lib/python2.6/site-packages/webadmin/locale/ru/LC_MESSAGES/*.mo
/usr/lib/python2.6/site-packages/webadmin/conf/*.sample
/usr/lib/python2.6/site-packages/webadmin/apps/users/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/users/lib/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/users/tests/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/users/templates/users/*.html
/usr/lib/python2.6/site-packages/webadmin/apps/statistics/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/statistics/tests/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/statistics/templates/statistics/*.html
/usr/lib/python2.6/site-packages/webadmin/apps/statistics/lib/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/statistics/management/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/statistics/management/commands/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/roles/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/roles/tests/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/roles/templates/roles/*.html
/usr/lib/python2.6/site-packages/webadmin/apps/manual_categorization/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/manual_categorization/tests/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/manual_categorization/templates/manual_categorization/*.html
/usr/lib/python2.6/site-packages/webadmin/apps/main/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/main/tests/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/main/templates/main/*.html
/usr/lib/python2.6/site-packages/webadmin/apps/license/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/license/tests/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/license/lib/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/license/templates/license/*.html
/usr/lib/python2.6/site-packages/webadmin/apps/categories/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/categories/tests/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/categories/templates/categories/*.html
/usr/lib/python2.6/site-packages/webadmin/apps/core/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/core/templatetags/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/auth/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/auth/tests/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/auth/templates/auth/*.html
/usr/lib/python2.6/site-packages/webadmin/apps/admins/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/admins/tests/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/admins/templates/admins/*.html
/usr/lib/python2.6/site-packages/webadmin/apps/manual_categorization/lib/*.py
/usr/lib/python2.6/site-packages/webadmin/apps/*.py
/usr/lib/python2.6/site-packages/*.egg-info
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
