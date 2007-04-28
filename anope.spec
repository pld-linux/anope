Summary:	Internet Relay Chat Services
Summary(pl.UTF-8):Usługi dla sieci IRC
Name:		anope
Version:	1.7.18
Release:	1
License:	BSD-like or any GPL-compatible
Group:		Daemons
Source0:	http://dl.sourceforge.net/anope/%{name}-%{version}.tar.gz
# Source0-md5:	87b9e7a6a6129a9e9c8d07b135da4a4f
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:	%{name}-fhs.patch
URL:		http://www.anope.org
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	mysql-devel
BuildRequires:	rpmbuild(macros) >= 1.202
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts
Provides:	group(anope)
Provides:	user(anope)
Obsoletes:	ircservices
Obsoletes:	ircservices-hybrid
Obsoletes:	ircservices-ptlink
Obsoletes:	ircservices6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/anope

%description
Anope IRC Services is a package of services for IRC networks.

%description -l pl.UTF-8
Anope IRC Services to pakiet z usługami dla sieci IRC (Internet Relay
Chat).

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%configure \
	 --with-bindir=%{_sbindir} \
	 --with-datadir=%{_localstatedir}/lib/%{name}
%{__make} \
	MODULE_PATH=%{_libdir}/%{name}/modules

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_localstatedir}/lib/%{name},%{_libdir}/%{name}/{modules,languages},%{_localstatedir}/log/ircservices,%{_sysconfdir}} \
	$RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT%{_localstatedir}/log/anope/

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDEST=$RPM_BUILD_ROOT%{_sbindir} \
	MODULE_PATH=$RPM_BUILD_ROOT%{_libdir}/%{name}/modules \
	DATDEST=$RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}

mv $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/example.conf $RPM_BUILD_ROOT%{_sysconfdir}/anope.conf

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/anope
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/anope

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -f -g 218 anope
%useradd -g anope -d /var/lib/anope -u 218 -c "Anope IRC services account" -s /bin/true anope

%post
/sbin/chkconfig --add anope
%service %{name} restart "Anope IRC Services"

%preun
%service %{name} stop "Anope IRC Services"
/sbin/chkconfig --del anope

%postun
if [ "$1" = "0" ]; then
	%userremove anope
	%groupremove anope
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%attr(750,root,anope) %dir %{_sysconfdir}
%attr(660,anope,anope) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(770,root,anope) %dir %{_localstatedir}/log/%{name}
%attr(770,root,anope) %dir %{_localstatedir}/lib/%{name}
%dir %{_libdir}/anope
%dir %{_libdir}/anope/modules
%attr(755,root,root) %{_libdir}/anope/modules/*.so
#%{_localstatedir}/lib/%{name}/example.chk
#%{_localstatedir}/lib/%{name}/example.conf
%dir %{_libdir}/anope/languages
%{_localstatedir}/lib/%{name}/languages/*
%{_localstatedir}/lib/%{name}/mydbgen
#%{_localstatedir}/lib/%{name}/tables.sql
