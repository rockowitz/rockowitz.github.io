Name:    ddcutil
Version: 0.8.6
Release: 1%{?dist}
Summary: Query and update monitor settings
License: GPLv2
# Using rockowitz.gitub.io instead of www.ddcutil.com does not resolve problem 
# that fedora-review reports Name or Service not known
URL:     http://www.ddcutil.com
Source:  http://www.ddcutil.com/tarballs/%{name}-%{version}.tar.gz

# Alternative architectures build successfully in Koji, but are generally untested
# How best to handle?
ExcludeArch: s390x         # builds successfully in Koji, but makes makes no sense given S390 hardware
# ExcludeArch: ppc64le     # builds successfully in Koji, untested
# ExcludeArch: ppc64       # builds successfully in Koji, tested
# ExcludeArch: ppc         # builds successfully in Koji, untested

BuildRequires: pkgconfig(glib-2.0)   >= 2.32
BuildRequires: pkgconfig(libusb-1.0) >= 1.0.15
BuildRequires: pkgconfig(systemd)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(libdrm) >= 2.4.16

Requires(pre): shadow-utils

Requires: i2c-tools

%description 
Query and change monitor settings

ddcutil communicates with monitors implementing MCCS (Monitor Control Command
Set), using either the DDC/CI protocol on the I2C bus or as a Human Interface
Device on USB.  In general, anything that can be controlled using a monitor's
on-screen display can be controlled by this program.  Examples include 
changing a monitor's input source and adjusting its brightness.

A particular use case for ddcutil is as part of color profile management.
Monitor calibration is relative to the monitor color settings currently in
effect, e.g. red gain.  ddcutil allows color related settings to be saved at
the time a monitor is calibrated, and then restored when the calibration is
applied.

# belt and suspenders:
%global _hardened_build 1

%prep
%setup -q

%build
%configure --enable-lib=no 
%make_build V=1

%check

%install
%make_install
# temporary until v0.8.6: 
rm -f %{buildroot}/usr/share/doc/%{name}/COPYING

%files
%doc     AUTHORS NEWS.md README.md ChangeLog
%license COPYING

%{_datadir}/%{name}

# %%dir %%{_datadir}/%%{name}
# %%dir %%{_datadir}/%%{name}/data
# %%{_datadir}/%%{name}/data/*rules
# %%{_datadir}/%%{name}/data/90-nvidia-i2c.conf

%{_mandir}/man1/ddcutil.1*
%{_bindir}/ddcutil

%changelog

* Fri Jan 19 2018 Sanford Rockowitz <rockowitz@minsoft.com> 0.8.6-1
- Release 0.8.6
- Changed "Recommends: i2c-tools" to "Requires: i2c-tools"
- Minor enhancements and bug fixes.
- For a complete list of changes and bug fixes, 
  see http://www.ddcutil.com/release_notes for details.

* Wed Nov 29 2017 Sanford Rockowitz <rockowitz@minsoft.com> 0.8.5-1
- Release 0.8.5
- Spec file cleanup
- Architecture s390x is execluded since this utility makes no sense in that
  environment.
- Minor enhancements and bug fixes, particularly for 32 bit environments.
- For a complete list of changes and bug fixes, 
  see http://www.ddcutil.com/release_notes for details.

* Thu Nov 16 2017 Sanford Rockowitz <rockowitz@minsoft.com> 0.8.4-1
- Minor enhancements and bug fixes. 
- For a complete list of changes and bug fixes,
  see http://www.ddcutil.com/release_notes

* Sat Jul 22 2017 Sanford Rockowitz <rockowitz@minsoft.com> 0.8.4-1
- Changes to conform to Fedora packaging standards
- Minor enhancements and bug fixes. 
- For a complete list of changes and bug fixes,
  see http://www.ddcutil.com/release_notes

* Sat May 20 2017 Sanford Rockowitz <rockowitz@minsoft.com> 0.8.3-1
- Changes for Fedora packaging

* Wed May 17 2017 Sanford Rockowitz <rockowitz@minsoft.com> 0.8.2-1
- Minor enchancements to diagnostics in the environment and interrogate
  commands
- For a complete list of changes and bug fixes, 
  see http://www.ddcutil.com/release_notes

* Sat May 06 2017 Sanford Rockowitz <rockowitz@minsoft.com> 0.8.1-1
- Fixes a segfault that can occur when scanning for USB connected monitors.
- For a complete list of changes and bug fixes, 
  see http://www.ddcutil.com/release_notes

* Mon May 01 2017 Sanford Rockowitz <rockowitz@minsoft.com> 0.8.0-1
- Added options --async and --nodetect to improve performance
- By default, setvcp and loadvcp read the VCP value after the value has been
  set, to confirm that the monitor has made the change requested.
- Command "getvcp --terse" now reports VCP settings in a form that is easily
  machine readable.
- For a complete list of changes and bug fixes,
  see http://www.ddcutil.com/release_notes

* Sun Mar 05 2017 Sanford Rockowitz <rockowitz@minsoft.com> 0.7.3-1
- For a complete list of changes and bug fixes for this and earlier releases, 
  see http://www.ddcutil.com/release_notes
