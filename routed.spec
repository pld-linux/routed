Summary:	The routing daemon which maintains routing tables
Summary(de):	RIP-Routing-D�mon f�r automatische Route-Tabellenverwaltung
Summary(es):	Servidor RIP para manutenci�n autom�tica de tabla de rutas
Summary(fr):	D�mon de routage RIP pour maintenante automatique de la table de routage
Summary(pl):	Demon zarz�dzaj�cy tablicami rutingu
Summary(pt_BR):	Servidor RIP para manuten��o autom�tica de tabela de rotas
Summary(tr):	RIP - otomatik y�nlendirme protokol�
Name:		routed
Version:	0.17
Release:	12
License:	BSD
Group:		Networking/Daemons
Source0:	ftp://ftp.linux.org.uk/pub/linux/Networking/netkit/netkit-%{name}-%{version}.tar.gz
# Source0-md5:	3a9507876db23109be6d1f41ced5570a
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		netkit-%{name}-install.patch
Requires:	rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The routed routing daemon handles incoming RIP traffic and broadcasts
outgoing RIP traffic about network traffic routes, in order to
maintain current routing tables. These routing tables are essential
for a networked computer, so that it knows where packets need to be
sent.

%description -l de
Es gibt eine Auswahl von Protokollen f�r die automatische
Aktualisierung von TCP/IP-Routing-Tabellen, von denen RIP das
einfachste ist. Dieses Paket enth�lt einen D�mon, der
RIP-Routing-Meldungen rundsendet und hereinkommende RIP-Pakete
abfertigt.

%description -l es
Varios protocolos est�n disponibles para actualizaci�n`` autom�tica de
tablas de rutado TCP/IP. RIP es el m�s sencillo de estos, y este
paquete incluye un servidor que transmite y recibe notificaciones de
rutado en este protocolo.

%description -l fr
Il existe de nombreux protocoles pour la mise � jour automatique des
tables de routage de TCP/IP. RIP est le plus simple d'entre eux et ce
paquetage contient un d�mon qui diffuse la notification de routage RIP
et g�re les paquets RIP entrants.

%description -l pl
Routed to demon routingu obs�uguj�cy przychodz�cy ruch RIP i
rozsy�aj�cy wychodz�cy ruch RIP po trasach w sieci, aby zarz�dza�
aktualnymi tablicami routingu. Te tablice routing to podstawa dla
komputera pod��czonego do wielu sieci, kt�ry dzi�ki nim wie, dok�d
pakiety powinny by� wysy�ane.

%description -l pt_BR
V�rios protocolos est�o dispon�veis para atualiza��o autom�tica de
tabelas de roteamento TCP/IP. O RIP � o mais simples destes, e este
pacote inclui um servidor que transmite e recebe notifica��es de
roteamento neste protocolo.

%description -l tr
Y�nlendirme tablolar�n�n g�ncellenmesi i�in bir dizi y�ntem vard�r.
RIP bunlar�n en basitleri aras�nda yer al�r. Bu sunucu RIP bilgilerini
yay�nlar ve dinledi�i RIP bilgilerine g�re y�nlendirme tablolar�n�
g�nceller.

%prep
%setup -q -n netkit-%{name}-%{version}
%patch0 -p1

%build
./configure --with-c-compiler=gcc
%{__make} \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{rc.d/init.d,sysconfig}

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/routed
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/routed

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add routed
if [ -f /var/lock/subsys/routed ]; then
	/etc/rc.d/init.d/routed restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/routed start\" to start routed server" 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/routed ]; then
		/etc/rc.d/init.d/routed stop 1>&2
	fi
	/sbin/chkconfig --del routed
fi

%files
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/routed
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/routed
%attr(755,root,root) %{_sbindir}/routed
%attr(755,root,root) %{_sbindir}/ripquery
%{_mandir}/man8/*
