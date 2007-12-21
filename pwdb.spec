%define	major 0
%define libname	%mklibname pwdb %{major}

Summary:	The password database library
Name:		pwdb
Version:	0.62
Release:	%mkrel 5
License:	GPL
Group:		System/Libraries
Source:		%{name}-%{version}.tar.bz2
Patch0:		%{name}-0.62-includes.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
The pwdb package contains libpwdb, the password database library.
Libpwdb is a library which implements a generic user information
database.  Libpwdb was specifically designed to work with Linux's PAM
(Pluggable Authentication Modules).  Libpwdb allows configurable
access to and management of security tools like /etc/passwd,
/etc/shadow and network authentication systems including NIS and
Radius.

%package	conf
Summary:	The password database library config
Group:		System/Libraries

%description	conf
Configuration package for the libpwdb, the password database library.

%package -n	%{libname}
Summary:	The password database library
Group:		System/Libraries
Requires:	%{name}-conf
Provides:	pwdb = %{version}-%{release}
Obsoletes:	pwdb

%description -n	%{libname}
The pwdb package contains libpwdb, the password database library.
Libpwdb is a library which implements a generic user information
database.  Libpwdb was specifically designed to work with Linux's PAM
(Pluggable Authentication Modules).  Libpwdb allows configurable
access to and management of security tools like /etc/passwd,
/etc/shadow and network authentication systems including NIS and
Radius.

%package -n	%{libname}-devel
Summary:	The pwdb include files and link library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	pwdb-devel = %{version}-%{release}
Conflicts:	pwdb-devel <= 0.61

%description -n	%{libname}-devel
The development header / link library for pwdb.

%package -n	%{libname}-static-devel
Summary:	The pwdb static library
Group:		Development/C
Requires:	%{libname}-devel = %{version}-%{release}
Provides:	pwdb-static-devel = %{version}-%{release}

%description -n	%{libname}-static-devel
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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}/{%{_lib},%{_sysconfdir},%{_includedir}/pwdb}

make	INCLUDED=%{buildroot}%{_includedir}/pwdb \
	LIBDIR=%{buildroot}/%{_lib} \
	LDCONFIG=":" \
	install

install conf/pwdb.conf %{buildroot}%{_sysconfdir}/pwdb.conf

ln -sf lib%{name}.so.%{version} %{buildroot}/%{_lib}/lib%{name}.so.%{major}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files conf
%defattr(644,root,root,755)
%doc Copyright doc/pwdb.txt doc/html
%config(noreplace) %{_sysconfdir}/pwdb.conf

%files -n %{libname}
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libpwdb.so.%{major}*

%files -n %{libname}-devel
%defattr(644,root,root,755)
/%{_lib}/libpwdb.so
%{_includedir}/pwdb

%files -n %{libname}-static-devel
%defattr(644,root,root,755)
/%{_lib}/libpwdb.a


