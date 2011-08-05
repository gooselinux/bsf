# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           bsf
Version:        2.4.0
Release:        4.1%{?dist}
Epoch:          0
Summary:        Bean Scripting Framework
License:        ASL 2.0
URL:            http://jakarta.apache.org/bsf/
Group:          Development/Libraries
#http://jakarta.apache.org/builds/jakarta-%{name}/dev/v%{version}/src/%{name}-src-%{version}.tar.gz
Source0:        %{name}-src-%{version}.tar.gz
Patch0:         build-file.patch
Patch1:         build.properties.patch
BuildRequires:  jpackage-utils >= 1.6
BuildRequires:  ant
BuildRequires:  xalan-j2
BuildRequires:  jython
BuildRequires:  jakarta-commons-logging
Requires:       jakarta-commons-logging
Requires:       xalan-j2
Requires:       jpackage-utils
BuildArch:      noarch
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Bean Scripting Framework (BSF) is a set of Java classes which provides
scripting language support within Java applications, and access to Java
objects and methods from scripting languages. BSF allows one to write
JSPs in languages other than Java while providing access to the Java
class library. In addition, BSF permits any Java application to be
implemented in part (or dynamically extended) by a language that is
embedded within it. This is achieved by providing an API that permits
calling scripting language engines from within Java, as well as an
object registry that exposes Java objects to these scripting language
engines.

BSF supports several scripting languages currently:
* Javascript (using Rhino ECMAScript, from the Mozilla project)
* Python (using either Jython or JPython)
* Tcl (using Jacl)
* NetRexx (an extension of the IBM REXX scripting language in Java)
* XSLT Stylesheets (as a component of Apache XML project's Xalan and
Xerces)

In addition, the following languages are supported with their own BSF
engines:
* Java (using BeanShell, from the BeanShell project)
* JRuby
* JudoScript

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
# remove all binary libs
find . -name "*.jar" -exec %{__rm} -f {} \;
%{__rm} -fr bsf

%patch0 -p1
%patch1 -p1

%build
[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java 
export CLASSPATH=$(build-classpath jakarta-commons-logging jython xalan-j2)
ant jar 
%{__rm} -rf bsf/src/org/apache/bsf/engines/java
ant javadocs

%install
%{__rm} -fr %{buildroot}
# jar
%{__install} -d -m 755 %{buildroot}%{_javadir}
%{__install} -m 644 build/lib/%{name}.jar \
%{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)
# javadoc
%{__install} -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -pr build/javadocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && ln -sf %{name}-%{version} %{name})
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE.txt AUTHORS.txt CHANGES.txt NOTICE.txt README.txt TODO.txt RELEASE-NOTE.txt
%{_javadir}/*

%files javadoc
%defattr(-,root,root)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%{_javadocdir}/%{name}

%changelog
* Tue Feb 2 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.0-4.1
- Drop gcj_support.
- Remove servlet and jspapi BR/Rs.

* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 0:2.4.0-4
- Fix License (ASL 2.0, not 1.1)

* Mon Sep 14 2009 Christoph Höger <choeger@cs.tu-berlin.de> - 0:2.4.0-3
- Fix typo in Requires

* Wed Sep 09 2009 Christoph Höger <choeger@cs.tu-berlin.de> - 0:2.4.0-1
- New Upstream release: 2.4.0
- Add jython build dependency to include bsf-jython engine

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:2.3.0-13
- drop repotag
- fix license

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:2.3.0-12jpp.2
- Autorebuild for GCC 4.3

* Wed Mar 07 2007 Permaine Cheung <pcheung@redhat.com> 0:2.3.0-11jpp.2
- Update spec file as per Fedora guidelines

* Thu Aug 03 2006 Deepak Bhole <dbhole@redhat.com> 0:2.3.0-11jpp.1
- Added missing requirements.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> 0:2.3.0-10jpp_2fc
- Rebuilt

* Fri Jul 21 2006 Deepak Bhole <dbhole@redhat.com> 0:2.3.0-10jpp_2fc
- Removing vendor and distribution tags.

* Thu Jul 20 2006 Deepak Bhole <dbhole@redhat.com> 0:2.3.0-10jpp_1fc
- Added conditional native compilation.
- From gbenson@redhat:
-   Build without Jython or Rhino for now.
-   Build with servletapi5.
-   Avoid Sun-specific classes.

* Wed Apr 26 2006 Fernando Nasser <fnasser@redhat.com>  0:2.3.0-9jpp
- First JPP 1.7 build

* Wed Nov 3 2004 Nicolas Mailhot <nim@jpackage.org>  0:2.3.0-8jpp
- Clean up specfile a bit

* Fri Aug 20 2004 Ralph Apel <r.apel at r-apel.de> 0:2.3.0-7jpp
- Build with ant-1.6.2

* Thu Oct 09 2003 David Walluck <david@anti-microsoft.org> 0:2.3.0-6jpp
- add javadoc symlinks
- change Apache Software License to Apache License

* Tue Aug 26 2003 David Walluck <david@anti-microsoft.org> 0:2.3.0-5jpp
- remove all Requires

* Fri Apr 12 2003 David Walluck <david@anti-microsoft.org> 0:2.3.0-4jpp
- fix strange permissions

* Fri Apr 11 2003 David Walluck <david@anti-microsoft.org> 0:2.3.0-3jpp
- rebuild for jpackage 1.5

* Wed Jan 22 2003 David Walluck <david@anti-microsoft.org> 2.3.0-2jpp
- Requires/BuildRequires: xalan-j2
- update %%description

* Mon Jan 13 2003 David Walluck <david@anti-microsoft.org> 2.3.0-1jpp
- version 2.3.0 (first jakarta release)

* Tue May 07 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.2-5jpp 
- vendor, distribution, group tags
- versioned dir for javadoc
- section macro

* Sat Dec 1 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.2-4jpp
- javadoc in javadoc package

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 2.2-3jpp
- removed packager tag
- new jpp extension
- fixed url

* Sat Oct 6 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.2-2jpp
- first unified release
- used original tarball
- s/jPackage/JPackage

* Thu Aug 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.2-1jpp
- first Mandrake release
