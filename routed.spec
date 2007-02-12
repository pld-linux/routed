Summary:	The routing daemon which maintains routing tables
Summary(de.UTF-8):   RIP-Routing-Dämon für automatische Route-Tabellenverwaltung
Summary(es.UTF-8):   Servidor RIP para manutención automática de tabla de rutas
Summary(fr.UTF-8):   Démon de routage RIP pour maintenante automatique de la table de routage
Summary(pl.UTF-8):   Demon zarządzający tablicami rutingu
Summary(pt_BR.UTF-8):   Servidor RIP para manutenção automática de tabela de rotas
Summary(tr.UTF-8):   RIP - otomatik yönlendirme protokolü
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
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The routed routing daemon handles incoming RIP traffic and broadcasts
outgoing RIP traffic about network traffic routes, in order to
maintain current routing tables. These routing tables are essential
for a networked computer, so that it knows where packets need to be
sent.

%description -l de.UTF-8
Es gibt eine Auswahl von Protokollen für die automatische
Aktualisierung von TCP/IP-Routing-Tabellen, von denen RIP das
einfachste ist. Dieses Paket enthält einen Dämon, der
RIP-Routing-Meldungen rundsendet und hereinkommende RIP-Pakete
abfertigt.

%description -l es.UTF-8
Varios protocolos están disponibles para actualización`` automática de
tablas de rutado TCP/IP. RIP es el más sencillo de estos, y este
paquete incluye un servidor que transmite y recibe notificaciones de
rutado en este protocolo.

%description -l fr.UTF-8
Il existe de nombreux protocoles pour la mise à jour automatique des
tables de routage de TCP/IP. RIP est le plus simple d'entre eux et ce
paquetage contient un démon qui diffuse la notification de routage RIP
et gère les paquets RIP entrants.

%description -l pl.UTF-8
routed to demon routingu obsługujący przychodzący ruch RIP i
rozsyłający wychodzący ruch RIP po trasach w sieci, aby zarządzać
aktualnymi tablicami routingu. Te tablice routing to podstawa dla
komputera podłączonego do wielu sieci, który dzięki nim wie, dokąd
pakiety powinny być wysyłane.

%description -l pt_BR.UTF-8
Vários protocolos estão disponíveis para atualização automática de
tabelas de roteamento TCP/IP. O RIP é o mais simples destes, e este
pacote inclui um servidor que transmite e recebe notificações de
roteamento neste protocolo.

%description -l tr.UTF-8
Yönlendirme tablolarının güncellenmesi için bir dizi yöntem vardır.
RIP bunların en basitleri arasında yer alır. Bu sunucu RIP bilgilerini
yayınlar ve dinlediği RIP bilgilerine göre yönlendirme tablolarını
günceller.

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
%service routed restart "routed server"

%preun
if [ "$1" = "0" ]; then
	%service routed stop
	/sbin/chkconfig --del routed
fi

%files
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/routed
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/routed
%attr(755,root,root) %{_sbindir}/routed
%attr(755,root,root) %{_sbindir}/ripquery
%{_mandir}/man8/*
