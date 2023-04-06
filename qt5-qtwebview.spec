#
# Conditional build:
%bcond_without	doc		# Documentation
%bcond_without	webengine	# WebEngine plugin

%ifarch x32
%undefine	with_webengine
%endif

%define		orgname		qtwebview
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		%{version}
%define		qtwebengine_ver		%{version}
Summary:	The Qt5 WebView library
Summary(pl.UTF-8):	Biblioteka Qt5 WebView
Name:		qt5-%{orgname}
Version:	5.15.9
Release:	1
License:	LGPL v3 or GPL v2+ or commercial
Group:		X11/Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-opensource-src-%{version}.tar.xz
# Source0-md5:	22b07bf12b2379e2cb9fc8d2d62cde0d
URL:		https://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Gui-devel >= %{qtbase_ver}
BuildRequires:	Qt5Qml-devel >= %{qtdeclarative_ver}
BuildRequires:	Qt5Quick-devel >= %{qtdeclarative_ver}
%{?with_webengine:BuildRequires:	Qt5WebEngine-devel >= %{qtwebengine_ver}}
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
BuildRequires:	qt5-doc-common >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.016
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 WebView library.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera bibliotekę Qt5 WebView.

%package -n Qt5WebView
Summary:	The Qt5 WebView library
Summary(pl.UTF-8):	Biblioteka Qt5 WebView
Group:		X11/Libraries
Requires:	Qt5Core >= %{qtbase_ver}
Requires:	Qt5Gui >= %{qtbase_ver}
Requires:	Qt5Qml >= %{qtdeclarative_ver}
Requires:	Qt5Quick >= %{qtdeclarative_ver}

%description -n Qt5WebView
Qt5 WebView library.

%description -n Qt5WebView -l pl.UTF-8
Biblioteka Qt5 WebView.

%package -n Qt5WebView-devel
Summary:	Qt5 WebView - development files
Summary(pl.UTF-8):	Biblioteka Qt5 WebView - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Gui-devel >= %{qtbase_ver}
Requires:	Qt5WebView = %{version}-%{release}

%description -n Qt5WebView-devel
Qt5 WebView - development files.

%description -n Qt5WebView-devel -l pl.UTF-8
Biblioteka Qt5 WebView - pliki programistyczne.

%package -n Qt5WebView-plugin-webengine
Summary:	Qt5 WebView library WebEngine plugin
Summary(pl.UTF-8):	Wtyczka WebEngine do biblioteki Qt5 WebView
Group:		X11/Libraries
Requires:	Qt5WebEngine >= %{qtwebengine_ver}
Requires:	Qt5WebView = %{version}-%{release}

%description -n Qt5WebView-plugin-webengine
Qt5 WebView library WebEngine plugin.

%description -n Qt5WebView-plugin-webengine -l pl.UTF-8
Wtyczka WebEngine do biblioteki Qt5 WebView.

%package doc
Summary:	Qt5 WebView documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 WebView w formacie HTML
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc
Qt5 WebView documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 WebView w formacie HTML.

%package doc-qch
Summary:	Qt5 WebView documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 WebView w formacie QCH
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc-qch
Qt5 WebView documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 WebView w formacie QCH.

%package examples
Summary:	Qt5 WebView examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 WebView
Group:		X11/Development/Libraries
BuildArch:	noarch

%description examples
Qt5 WebView examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 WebView.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version}

%build
%{qmake_qt5}
%{__make}
%{?with_doc:%{__make} docs}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{without webengine}
install -d $RPM_BUILD_ROOT%{qt5dir}/plugins/webview
%endif

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5WebView -p /sbin/ldconfig
%postun	-n Qt5WebView -p /sbin/ldconfig

%files -n Qt5WebView
%defattr(644,root,root,755)
%doc dist/changes-*
# R: Qt5Core Qt5Qml
%attr(755,root,root) %{_libdir}/libQt5WebView.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5WebView.so.5
%dir %{qt5dir}/plugins/webview
%dir %{qt5dir}/qml/QtWebView
# R: Qt5Core Qt5Qml Qt5Quick Qt5WebView
%attr(755,root,root) %{qt5dir}/qml/QtWebView/libdeclarative_webview.so
%{qt5dir}/qml/QtWebView/plugins.qmltypes
%{qt5dir}/qml/QtWebView/qmldir

%files -n Qt5WebView-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5WebView.so
%{_libdir}/libQt5WebView.prl
%{_includedir}/qt5/QtWebView
%{_pkgconfigdir}/Qt5WebView.pc
%dir %{_libdir}/cmake/Qt5WebView
%{_libdir}/cmake/Qt5WebView/Qt5WebViewConfig*.cmake
%{qt5dir}/mkspecs/modules/qt_lib_webview.pri
%{qt5dir}/mkspecs/modules/qt_lib_webview_private.pri

%if %{with webengine}
%files -n Qt5WebView-plugin-webengine
%defattr(644,root,root,755)
%attr(755,root,root) %{qt5dir}/plugins/webview/libqtwebview_webengine.so
%{_libdir}/cmake/Qt5WebView/Qt5WebView_QWebEngineWebViewPlugin.cmake
%endif

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtwebview

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtwebview.qch
%endif

%files examples
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
%{_examplesdir}/qt5/webview
