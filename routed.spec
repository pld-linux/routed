Summary:	The routing daemon which maintains routing tables.
Name:		routed
Version:	0.10
Release:	14
Copyright:	BSD
Group:		System Environment/Daemons
Source:		ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-routed-0.10.tar.gz
Source1:	routed.init
Patch:		netkit-routed-0.10-misc.patch
Patch1:		netkit-routed-0.10-trace.patch
Patch2:		netkit-routed-0.10-ifreq.patch
Patch3:		netkit-routed-0.10-compat21.patch
Prereq:		/sbin/chkconfig
Requires:	rc-scripts
Buildroot:	/var/tmp/%{name}-root

%description
The routed routing daemon handles incoming RIP traffic and broadcasts
outgoing RIP traffic about network traffic routes, in order to maintain
current routing tables.  These routing tables are essential for a
networked computer, so that it knows where packets need to be sent.

The routed package should be installed on any networked machine.

%prep
%setup -q -n netkit-routed-0.10
%patch0 -p1 -b .misc
%patch1 -p1 -b .trace
%ifarch alpha
%patch2 -p1 -b .ifreq
%endif
%patch3 -p1 -b .compat21

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/usr/man/man8
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
make INSTALLROOT=$RPM_BUILD_ROOT install
install -m 755 $RPM_SOURCE_DIR/routed.init $RPM_BUILD_ROOT/etc/rc.d/init.d/routed

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add routed

%postun
if [ $1 = 0 ]; then
    /sbin/chkconfig --del routed
fi

%files
%defattr(-,root,root)
/usr/sbin/routed
/usr/man/man8/routed.8
%attr(754,root,root) /etc/rc.d/init.d/routed
