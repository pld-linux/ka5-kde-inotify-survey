#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.01.95
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kde-inotify-survey
Summary:	Kde inotify survey
Name:		ka5-%{kaname}
Version:	24.01.95
Release:	0.1
License:	BSD 3 Clause/GPL v2/GPL v3
Group:		X11/Libraries
Source0:	https://download.kde.org/unstable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	a4e1785faf84aaa6eacc8a5328f16b80
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= 5.15.2
BuildRequires:	Qt6DBus-devel >= 5.15.2
BuildRequires:	Qt6Test-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= 5.93.0
BuildRequires:	kf6-kauth-devel >= 5.93.0
BuildRequires:	kf6-kcoreaddons-devel >= 5.109.0
BuildRequires:	kf6-kdbusaddons-devel >= 5.93.0
BuildRequires:	kf6-ki18n-devel >= 5.93.0
BuildRequires:	kf6-knotifications-devel >= 5.93.0
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Have you ever wondered why dolphin or any other application stopped
noticing file changes? Chances are you ran out of inotify resources.
kde-inotify-survey to the rescue! Sporting a kded module to tell you
when things are getting dicey and a CLI tool to inspect the state of
affairs.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kde-inotify-survey
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kded/inotify.so
%attr(755,root,root) %{_prefix}/libexec/kf6/kauth/kded-inotify-helper
%{_datadir}/dbus-1/system-services/org.kde.kded.inotify.service
%{_datadir}/dbus-1/system.d/org.kde.kded.inotify.conf
%{_datadir}/knotifications6/org.kde.kded.inotify.notifyrc
%{_datadir}/metainfo/org.kde.inotify-survey.metainfo.xml
%{_datadir}/polkit-1/actions/org.kde.kded.inotify.policy
