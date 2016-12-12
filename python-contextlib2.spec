%if 0%{?fedora}
%global with_python3 1
%endif

%{!?_licensedir: %global license %%doc}

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2:        %global __python2 /usr/bin/python2}
%{!?python2_sitelib:  %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%global modname contextlib2

Name:               python-contextlib2
Version:            0.5.4
Release:            2%{?dist}
Summary:            Backports and enhancements for the contextlib module

Group:              Development/Libraries
License:            Python
URL:                https://pypi.io/project/contextlib2
Source0:            https://pypi.io/packages/source/c/%{modname}/%{modname}-%{version}.tar.gz

BuildArch:          noarch

BuildRequires:      python2-devel
# needed for check: assertRaisesRegex in unittest.TestCase
BuildRequires:      python-unittest2

%if 0%{?with_python3}
BuildRequires:      python3-devel
%endif

%if 0%{?el6}
Patch0:             contextlib2-skip-tests-on-el6.patch
%endif

%description
contextlib2 is a backport of the standard library's contextlib module to
earlier Python versions.

It also serves as a real world proving ground for possible future
enhancements to the standard library version.

%if 0%{?with_python3}
%package -n python3-contextlib2
Summary:            Backports and enhancements for the contextlib module
Group:              Development/Libraries

%description -n python3-contextlib2
contextlib2 is a backport of the standard library's contextlib module to
earlier Python versions.

It also serves as a real world proving ground for possible future
enhancements to the standard library version.
%endif

%prep
%setup -q -n %{modname}-%{version}
%if 0%{?el6}
%patch0 -p1 -b skip-tests-on-el6
%endif

# Remove bundled egg-info in case it exists
rm -rf %{modname}.egg-info
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python2} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
popd
%endif
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}

%check
%{__python2} test_contextlib2.py
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} test_contextlib2.py
popd
%endif

%files
%doc README.rst VERSION.txt NEWS.rst
%license LICENSE.txt
%{python2_sitelib}/%{modname}.py*
%{python2_sitelib}/%{modname}-%{version}*

%if 0%{?with_python3}
%files -n python3-contextlib2
%doc README.rst VERSION.txt NEWS.rst
%license LICENSE.txt
%{python3_sitelib}/%{modname}.py*
%{python3_sitelib}/__pycache__/%{modname}*
%{python3_sitelib}/%{modname}-%{version}-*
%endif

%changelog
* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.5.4-2
- Rebuild for Python 3.6

* Tue Sep 27 2016 Ralph Bean <rbean@redhat.com> - 0.5.4-1
- new version

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon May 02 2016 Ralph Bean <rbean@redhat.com> - 0.5.3-1
- new version

* Fri Apr 01 2016 Sander Hoentjen <sander@hoentjen.eu> 0.5.1-1
- Update to latest upstream (#1297768)
- add BuildReq for python-unittest2 for tests to pass
- skip some tests on el6 because python-unittest2 is too old there

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Apr 11 2015 Ralph Bean <rbean@redhat.com> - 0.4.0-1
- Initial package for Fedora
