Summary:	The routing daemon which maintains routing tables
Summary(de):	RIP-Routing-Dämon für automatische Route-Tabellenverwaltung
Summary(fr):	Démon de routage RIP pour maintenante automatique de la table de routage
Summary(tr):	RIP - otomatik yönlendirme protokolü
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

%description -l de
Es gibt eine Auswahl von Protokollen für die automatische Aktualisierung 
von TCP/IP-Routing-Tabellen, von denen RIP das einfachste ist. Dieses 
Paket enthält einen Dämon, der RIP-Routing-Meldungen rundsendet und
hereinkommende RIP-Pakete abfertigt.

%description -l fr
Il existe de nombreux protocoles pour la mise à jour automatique des
tables de routage de TCP/IP. RIP est le plus simple d'entre eux et ce
paquetage contient un démon qui diffuse la notification de routage RIP
et gère les paquets RIP entrants.

%description -l tr
Yönlendirme tablolarýnýn güncellenmesi için bir dizi yöntem vardýr. RIP
bunlarýn en basitleri arasýnda yer alýr. Bu sunucu RIP bilgilerini yayýnlar
ve dinlediði RIP bilgilerine göre yönlendirme tablolarýný günceller.

%prep
%setup -q -n netkit-routed-0.16
%patch0 -p1
%patch1 -p1

%build
./configure
%{__make} CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

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
