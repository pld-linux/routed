Summary:	The routing daemon which maintains routing tables.
Name:		routed
Version:	0.16
Release:	6
Copyright:	BSD
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-%{name}-%{version}.tar.gz
Source1:	routed.init
Source2:	routed.sysconfig
Patch0:		netkit-routed-fork.patch
Patch1:		netkit-routed-install.patch
Prereq:		/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The routed routing daemon handles incoming RIP traffic and broadcasts
outgoing RIP traffic about network traffic routes, in order to maintain
current routing tables.  These routing tables are essential for a
networked computer, so that it knows where packets need to be sent.

The routed package should be installed on any networked machine.

%prep
%setup -q -n netkit-routed-0.16
%patch0 -p1
%patch1 -p1

%build
./configure
%{__make} CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_mandir}/man8}
mkdir -p $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/routed
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/routed

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man8/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add routed
if [ -f /var/lock/subsys/routed ]; then
	/etc/rc.d/init.d/routed restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/routed start\" to start routed server" 1>&2
fi
	
%postun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/routed ]; then
		/etc/rc.d/init.d/routed stop 1>&2
	fi
	/sbin/chkconfig --del routed
fi

%files
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/routed
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/routed
%attr(755,root,root) %{_sbindir}/routed
%{_mandir}/man8/*
