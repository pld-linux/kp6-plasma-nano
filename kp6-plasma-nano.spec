#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.3.4
%define		qtver		5.15.2
%define		kpname		plasma-nano
%define		kf6ver		5.39.0

Summary:	plasma-nano
Name:		kp6-%{kpname}
Version:	6.3.4
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	e0eb90ac39f7d15b69533dbf702f5305
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= 5.15.0
BuildRequires:	Qt6Gui-devel >= 5.15.0
BuildRequires:	Qt6Network-devel >= 5.15.2
BuildRequires:	Qt6Qml-devel
BuildRequires:	Qt6Quick-devel
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf6-extra-cmake-modules >= 0.0.9
BuildRequires:	kf6-kwindowsystem-devel >= 5.82
BuildRequires:	kp6-kwayland-devel >= 5.82
BuildRequires:	kp6-libplasma-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
Obsoletes:	kp5-%{kpname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
A minimal plasma shell package intended for embedded devices.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%{_libdir}/qt6/qml/org/kde/plasma/private/nanoshell
%{_datadir}/plasma/shells/org.kde.plasma.nano
