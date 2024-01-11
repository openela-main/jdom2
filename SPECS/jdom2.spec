Name:          jdom2
Version:       2.0.6
Release:       12%{?dist}
Summary:       Java manipulation of XML made easy
License:       Saxpath
URL:           http://www.jdom.org/
# ./generate-tarball.sh
Source0:       %{name}-%{version}.tar.gz
# originally taken from http://repo1.maven.org/maven2/org/jdom/jdom-contrib/1.1.3/jdom-contrib-1.1.3.pom
Source1:       jdom-contrib-template.pom
Source2:       jdom-junit-template.pom
# Bnd tool configuration
Source3:       bnd.properties
# Remove bundled jars that might not have clear licensing
Source4:       generate-tarball.sh
# Use system libraries
# Disable gpg signatures
# Process contrib and junit pom files
Patch0:        0001-Adapt-build.patch

BuildRequires: javapackages-local
BuildRequires: ant
BuildRequires: ant-junit
BuildRequires: isorelax
BuildRequires: jaxen
BuildRequires: xalan-j2
BuildRequires: xerces-j2
BuildRequires: xml-commons-apis
BuildRequires: log4j12
BuildRequires: aqute-bnd

BuildArch:     noarch

%description
JDOM is a Java-oriented object model which models XML documents.
It provides a Java-centric means of generating and manipulating
XML documents. While JDOM inter-operates well with existing
standards such as the Simple API for XML (SAX) and the Document
Object Model (DOM), it is not an abstraction layer or
enhancement to those APIs. Rather, it seeks to provide a robust,
light-weight means of reading and writing XML data without the
complex and memory-consumptive options that current API
offerings provide.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n jdom-JDOM-%{version}

%patch0 -p1

cp -p %{SOURCE1} maven/contrib.pom
cp -p %{SOURCE2} maven/junit.pom

sed -i 's/\r//' LICENSE.txt README.txt

# Unable to run coverage: use log4j12 but switch to log4j 2.x
sed -i.coverage "s|coverage, jars|jars|" build.xml

mkdir lib
build-jar-repository lib xerces-j2 xml-commons-apis jaxen junit isorelax xalan-j2 xalan-j2-serializer

%build
ant -Dversion=%{version} -Dj2se.apidoc=%{_javadocdir}/java maven

# Make jar into an OSGi bundle
bnd wrap --output build/package/jdom-%{version}.bar --properties %{SOURCE3} \
         --version %{version} build/package/jdom-%{version}.jar
mv build/package/jdom-%{version}.bar build/package/jdom-%{version}.jar

%install
%mvn_artifact build/maven/core/%{name}-%{version}.pom build/package/jdom-%{version}.jar
%mvn_artifact build/maven/core/%{name}-%{version}-contrib.pom build/package/jdom-%{version}-contrib.jar
%mvn_artifact build/maven/core/%{name}-%{version}-junit.pom build/package/jdom-%{version}-junit.jar
%mvn_install -J build/apidocs

%files -f .mfiles
%doc CHANGES.txt COMMITTERS.txt README.txt TODO.txt
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Mon Jul 23 2018 Michael Simacek <msimacek@redhat.com> - 2.0.6-12
- Repack tarball without bundled jars
- The repacked jar contains slightly different source (force push by upstream?)
- Correct license tag

* Tue Jul 17 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.6-11
- Remove unneeded buildrequires

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 31 2017 Michael Simacek <msimacek@redhat.com> - 2.0.6-7
- Avoid hardcoded jar paths

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Apr 14 2016 Mat Booth <mat.booth@redhat.com> - 2.0.6-6
- Add OSGi metadata to main jar
- Fix file listed twice warning

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.6-3
- Remove unneeded BR on cobertura

* Fri Feb 06 2015 gil cattaneo <puntogil@libero.it> 2.0.6-2
- introduce license macro

* Tue Oct 21 2014 gil cattaneo <puntogil@libero.it> 2.0.6-1
- update to 2.0.6 (rhbz#1118627)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.0.5-3
- Use Requires: java-headless rebuild (#1067528)

* Thu Nov 14 2013 gil cattaneo <puntogil@libero.it> 2.0.5-2
- use objectweb-asm3

* Thu Sep 12 2013 gil cattaneo <puntogil@libero.it> 2.0.5-1
- initial rpm
