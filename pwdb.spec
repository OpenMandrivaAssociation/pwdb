%define	major 0
%define libname	%mklibname pwdb %{major}
%define develnaname %mklibname pwdb -d
%define staticdevelnaname %mklibname pwdb -d -s

Summary:	The password database library
Name:		pwdb
Version:	0.62
Release:	15
License:	GPL
Group:		System/Libraries
Source:		%{name}-%{version}.tar.bz2
Patch0:		%{name}-0.62-includes.patch
BuildRequires:	tirpc-devel

%description
The pwdb package contains libpwdb, the password database library.
Libpwdb is a library which implements a generic user information
database.  Libpwdb was specifically designed to work with Linux's PAM
(Pluggable Authentication Modules).  Libpwdb allows configurable
access to and management of security tools like /etc/passwd,
/etc/shadow and network authentication systems including NIS and
Radius.

%package conf
Summary:	The password database library config
Group:		System/Base

%description conf
Configuration package for the libpwdb, the password database library.

%package -n	%{libname}
Summary:	The password database library
Group:		System/Libraries
Requires:	%{name}-conf
Provides:	pwdb = %{version}-%{release}
Obsoletes:	pwdb < %{version}-%{release}

%description -n	%{libname}
The pwdb package contains libpwdb, the password database library.
Libpwdb is a library which implements a generic user information
database.  Libpwdb was specifically designed to work with Linux's PAM
(Pluggable Authentication Modules).  Libpwdb allows configurable
access to and management of security tools like /etc/passwd,
/etc/shadow and network authentication systems including NIS and
Radius.

%package -n	%{develname}
Summary:	The pwdb include files and link library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	pwdb-devel = %{version}-%{release}
Obsoletes:	%{mklibname pwdb 0}-devel <= 0.62-14
Conflicts:	pwdb-devel <= 0.61

%description -n	%{develname}
The development header / link library for pwdb.

%package -n	%{staticdevelname}
Summary:	The pwdb static library
Group:		Development/C
Requires:	%{develname} = %{version}-%{release}
Provides:	pwdb-static-devel = %{version}-%{release}
Obsoletes:	%{mklibname pwdb 0}-static-devel <= 0.62-14

%description -n	%{staticdevelname}
The static development library for pwdb.

%prep

%setup -q
%patch0 -p1 -b .includes

rm default.defs
ln -s defs/redhat.defs default.defs
# checking out of the CVS sometimes preserves the setgid bit on
# directories...
chmod -R g-s .

%build
%make

%install

mkdir -p %{buildroot}/{%{_lib},%{_sysconfdir},%{_includedir}/pwdb}

make	INCLUDED=%{buildroot}%{_includedir}/pwdb \
	LIBDIR=%{buildroot}/%{_lib} \
	LDCONFIG=":" \
	install

install conf/pwdb.conf %{buildroot}%{_sysconfdir}/pwdb.conf

ln -sf lib%{name}.so.%{version} %{buildroot}/%{_lib}/lib%{name}.so.%{major}

%files conf
%defattr(644,root,root,755)
%doc Copyright doc/pwdb.txt doc/html
%config(noreplace) %{_sysconfdir}/pwdb.conf

%files -n %{libname}
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libpwdb.so.%{major}*

%files -n %{develname}
%defattr(644,root,root,755)
/%{_lib}/libpwdb.so
%{_includedir}/pwdb

%files -n %{staticdevelname}
%defattr(644,root,root,755)
/%{_lib}/libpwdb.a




%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 0.62-12mdv2011.0
+ Revision: 667900
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.62-11mdv2011.0
+ Revision: 607252
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0.62-10mdv2010.1
+ Revision: 521160
- rebuilt for 2010.1

* Wed Oct 14 2009 Olivier Blin <oblin@mandriva.com> 0.62-9mdv2010.0
+ Revision: 457454
- really fix pwdb-conf group, and do not break library group

* Sun Oct 11 2009 Olivier Blin <oblin@mandriva.com> 0.62-8mdv2010.0
+ Revision: 456648
- fix pwdb-conf group

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.62-7mdv2010.0
+ Revision: 426789
- rebuild

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0.62-6mdv2009.0
+ Revision: 225119
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 0.62-5mdv2008.1
+ Revision: 125758
- kill re-definition of %%buildroot on Pixel's request


* Mon Feb 12 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 0.62-5mdv2007.0
+ Revision: 119968
- Import pwdb

* Sat May 13 2006 Stefan van der Eijk <stefan@eijk.nu> 0.62-4mdk
- rebuild for sparc

* Fri Jan 06 2006 Oden Eriksson <oeriksson@mandriva.com> 0.62-3mdk
- drop selinux support (P1)

* Fri Sep 17 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.62-2mdk
- buildrequires

* Tue Aug 24 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.62-1mdk
- 0.62

