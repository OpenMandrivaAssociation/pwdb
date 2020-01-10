%define debug_package %{nil}
%define	major 0
%define libname	%mklibname pwdb %{major}
%define devname %mklibname pwdb -d
%define _disable_rebuild_configure 1

Summary:	The password database library
Name:		pwdb
Version:	0.62
Release:	31
License:	GPLv2
Group:		System/Libraries
Source0:	%{name}-%{version}.tar.bz2
Patch0:		%{name}-0.62-includes.patch
Patch1:		pwdb-0.62-makefile.patch
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(libnsl)

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
%rename		pwdb

%description -n	%{libname}
The pwdb package contains libpwdb, the password database library.
Libpwdb is a library which implements a generic user information
database.  Libpwdb was specifically designed to work with Linux's PAM
(Pluggable Authentication Modules).  Libpwdb allows configurable
access to and management of security tools like /etc/passwd,
/etc/shadow and network authentication systems including NIS and
Radius.

%package -n	%{devname}
Summary:	The pwdb include files and link library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	pwdb-devel = %{version}-%{release}

%description -n	%{devname}
The development header / link library for pwdb.

%prep

%setup -q
%autopatch -p1

rm default.defs
ln -s defs/redhat.defs default.defs
# checking out of the CVS sometimes preserves the setgid bit on
# directories...
chmod -R g-s .

%build
%define _disable_lto 1
%setup_compile_flags
%make CC=%{__cc}

%install
mkdir -p %{buildroot}/{%{_lib},%{_sysconfdir},%{_includedir}/pwdb}

make	INCLUDED=%{buildroot}%{_includedir}/pwdb \
	CC=%{__cc} \
	LIBDIR=%{buildroot}/%{_lib} \
	LDCONFIG=":" \
	install

install conf/pwdb.conf %{buildroot}%{_sysconfdir}/pwdb.conf

ln -sf lib%{name}.so.%{version} %{buildroot}/%{_lib}/lib%{name}.so.%{major}

%files conf
%doc Copyright doc/pwdb.txt doc/html
%config(noreplace) %{_sysconfdir}/pwdb.conf

%files -n %{libname}
/%{_lib}/libpwdb.so.%{major}*

%files -n %{devname}
/%{_lib}/libpwdb.so
%{_includedir}/pwdb
/%{_lib}/libpwdb.a

