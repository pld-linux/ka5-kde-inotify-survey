#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	23.08.3
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kde-inotify-survey
Summary:	Kde inotify survey
Name:		ka5-%{kaname}
Version:	23.08.3
Release:	1
License:	BSD 3 Clause/GPL v2/GPL v3
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	9f7375f1a83aab190de348cb951612df
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= 5.15.2
BuildRequires:	Qt5DBus-devel >= 5.15.2
BuildRequires:	Qt5Test-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	kf5-extra-cmake-modules >= 5.93.0
BuildRequires:	kf5-kauth-devel >= 5.93.0
BuildRequires:	kf5-kcoreaddons-devel >= 5.109.0
BuildRequires:	kf5-kdbusaddons-devel >= 5.93.0
BuildRequires:	kf5-ki18n-devel >= 5.93.0
BuildRequires:	kf5-knotifications-devel >= 5.93.0
BuildRequires:	kf5-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
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
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
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
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kded/inotify.so
%attr(755,root,root) %{_prefix}/libexec/kauth/kded-inotify-helper
%{_datadir}/dbus-1/system-services/org.kde.kded.inotify.service
%{_datadir}/dbus-1/system.d/org.kde.kded.inotify.conf
%{_datadir}/knotifications5/org.kde.kded.inotify.notifyrc
%{_datadir}/metainfo/org.kde.inotify-survey.metainfo.xml
%{_datadir}/polkit-1/actions/org.kde.kded.inotify.policy
